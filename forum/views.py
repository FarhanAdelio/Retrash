from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Kategori, Diskusi, Komentar
from django.db.models import F, Count, Q
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
from datetime import datetime, timedelta
from django.utils import timezone

class KategoriListView(ListView):
    model = Kategori
    template_name = 'forum/kategori_list.html'
    context_object_name = 'kategori_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for kategori in context['kategori_list']:
            kategori.jumlah_diskusi = kategori.diskusi.count()
        return context

class DiskusiListView(ListView):
    model = Diskusi
    template_name = 'forum/diskusi_list.html'
    ordering = ['-created_at']
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        kategori_slug = self.request.GET.get('kategori')
        sort_by = self.request.GET.get('sort', 'terbaru')
        
        # Search functionality
        if q:
            queryset = queryset.filter(judul__icontains=q) | queryset.filter(isi__icontains=q)
        
        # Category filter
        if kategori_slug:
            queryset = queryset.filter(kategori__slug=kategori_slug)
        
        # Sorting logic
        if sort_by == 'populer':
            # Sort by views (most viewed first)
            queryset = queryset.order_by('-view_count', '-created_at')
        elif sort_by == 'aktif':
            # Sort by activity (comment count and recent updates)
            queryset = queryset.annotate(
                komentar_count=Count('komentar')
            ).order_by('-komentar_count', '-updated_at')
        else:  # terbaru (default)
            queryset = queryset.order_by('-created_at')
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_sort'] = self.request.GET.get('sort', 'terbaru')
        return context

    def get_kategori(self):
        return Kategori.objects.all()

class KategoriDetailView(DetailView):
    model = Kategori
    template_name = 'forum/kategori_detail.html'
    context_object_name = 'kategori'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['diskusi_list'] = self.object.diskusi.all()
        return context

class DiskusiCreateView(LoginRequiredMixin, CreateView):
    model = Diskusi
    template_name = 'forum/diskusi_form.html'
    fields = ['judul', 'isi']

    def form_valid(self, form):
        form.instance.penulis = self.request.user
        messages.success(self.request, 'Diskusi berhasil dibuat!')
        return super().form_valid(form)

class DiskusiDetailView(DetailView):
    model = Diskusi
    template_name = 'forum/diskusi_detail.html'
    context_object_name = 'diskusi'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['komentar_list'] = self.object.komentar.all().order_by('created_at')
        return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Increment view count
        obj.view_count += 1
        obj.save(update_fields=['view_count'])
        # Refresh from DB to get the actual value
        obj.refresh_from_db()
        return obj

class DiskusiUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Diskusi
    template_name = 'forum/diskusi_form.html'
    fields = ['judul', 'isi']

    def test_func(self):
        diskusi = self.get_object()
        return self.request.user == diskusi.penulis

    def form_valid(self, form):
        messages.success(self.request, 'Diskusi berhasil diperbarui!')
        return super().form_valid(form)

class DiskusiDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Diskusi
    template_name = 'forum/diskusi_confirm_delete.html'
    success_url = reverse_lazy('forum:list')

    def test_func(self):
        diskusi = self.get_object()
        return self.request.user == diskusi.penulis

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Diskusi berhasil dihapus!')
        return super().delete(request, *args, **kwargs)

class KomentarCreateView(LoginRequiredMixin, CreateView):
    model = Komentar
    fields = ['isi']
    template_name = 'forum/komentar_form.html'

    def form_valid(self, form):
        diskusi = get_object_or_404(Diskusi, slug=self.kwargs['slug'])
        form.instance.diskusi = diskusi
        form.instance.penulis = self.request.user
        messages.success(self.request, 'Komentar berhasil ditambahkan!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('forum:diskusi_detail', kwargs={'slug': self.kwargs['slug']})

class KomentarUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Komentar
    template_name = 'forum/komentar_form.html'
    fields = ['isi']

    def test_func(self):
        komentar = self.get_object()
        return self.request.user == komentar.penulis

    def form_valid(self, form):
        messages.success(self.request, 'Komentar berhasil diperbarui!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('forum:diskusi_detail', kwargs={'slug': self.object.diskusi.slug})

class KomentarDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Komentar
    template_name = 'forum/komentar_confirm_delete.html'

    def test_func(self):
        komentar = self.get_object()
        return self.request.user == komentar.penulis

    def get_success_url(self):
        return reverse_lazy('forum:diskusi_detail', kwargs={'slug': self.object.diskusi.slug})

@require_http_methods(["POST"])
def edit_komentar_ajax(request, komentar_id):
    try:
        komentar = Komentar.objects.get(id=komentar_id, penulis=request.user)
        data = json.loads(request.body)
        komentar.isi = data.get('isi', '').strip()
        
        if not komentar.isi:
            return JsonResponse({
                'success': False,
                'message': 'Komentar tidak boleh kosong'
            }, status=400)
            
        komentar.is_edited = True
        komentar.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Komentar berhasil diperbarui',
            'content': komentar.isi
        })
    except Komentar.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Komentar tidak ditemukan'
        }, status=404)
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Format data tidak valid'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)
