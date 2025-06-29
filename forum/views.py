from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Kategori, Diskusi, Komentar
from django.db.models import F
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json

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
        
        if q:
            queryset = queryset.filter(judul__icontains=q) | queryset.filter(isi__icontains=q)
        
        if kategori_slug:
            queryset = queryset.filter(kategori__slug=kategori_slug)
            
        return queryset

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

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.object.view_count = F('view_count') + 1
        self.object.save()
        return response

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
