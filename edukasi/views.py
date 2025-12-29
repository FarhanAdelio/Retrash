from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from manajemen.models import Artikel, KategoriArtikel
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import EducationalContent
from .services import ExternalContentService

def artikel_list(request):
    artikel_list = Artikel.objects.all().order_by('-tanggal_publikasi')
    kategori_list = KategoriArtikel.objects.all()
    
    context = {
        'artikel_list': artikel_list,
        'kategori_list': kategori_list,
    }
    return render(request, 'edukasi/edukasi_list.html', context)

def artikel_by_kategori(request, slug):
    kategori = get_object_or_404(KategoriArtikel, slug=slug)
    artikel_list = Artikel.objects.filter(kategori=kategori).order_by('-tanggal_publikasi')
    kategori_list = KategoriArtikel.objects.all()
    
    context = {
        'kategori': kategori,
        'artikel_list': artikel_list,
        'kategori_list': kategori_list,
    }
    return render(request, 'edukasi/edukasi_list.html', context)

def artikel_detail(request, slug):
    artikel = get_object_or_404(Artikel, slug=slug)
    artikel.dilihat += 1
    artikel.save()
    
    # Artikel terkait (dari kategori yang sama)
    artikel_terkait = Artikel.objects.filter(
        kategori=artikel.kategori
    ).exclude(id=artikel.id).order_by('-tanggal_publikasi')[:3]
    
    context = {
        'artikel': artikel,
        'artikel_terkait': artikel_terkait,
    }
    return render(request, 'edukasi/article_detail.html', context)

def artikel_search(request):
    query = request.GET.get('q', '')
    if query:
        artikel_list = Artikel.objects.filter(
            Q(judul__icontains=query) | 
            Q(konten__icontains=query)
        ).order_by('-tanggal_publikasi')
    else:
        artikel_list = Artikel.objects.none()
    
    context = {
        'artikel_list': artikel_list,
        'query': query,
    }
    return render(request, 'edukasi/artikel_search.html', context)

class EdukasiListView(ListView):
    model = EducationalContent
    template_name = 'edukasi/edukasi_list.html'
    context_object_name = 'edukasi_list'
    paginate_by = 9
    
    def get_queryset(self):
        return EducationalContent.objects.filter(is_published=True).order_by('-published_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edukasi'
        return context

class EdukasiDetailView(DetailView):
    model = EducationalContent
    template_name = 'edukasi/edukasi_detail.html'
    context_object_name = 'content'

def edukasi_search(request):
    query = request.GET.get('q', '')
    if query:
        content_list = EducationalContent.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query),
            is_published=True
        ).order_by('-published_date')
    else:
        content_list = EducationalContent.objects.none()
    
    context = {
        'edukasi_list': content_list,
        'query': query,
    }
    return render(request, 'edukasi/edukasi_search.html', context)


def external_news(request):
    """View untuk menampilkan berita dari sumber eksternal"""
    source = request.GET.get('source', 'all')
    
    if source == 'all':
        articles = ExternalContentService.get_all_sources(limit_per_source=10)
    else:
        articles = ExternalContentService.get_rss_articles(source=source, limit=20)
    
    context = {
        'articles': articles,
        'source': source,
        'available_sources': ExternalContentService.RSS_FEEDS.keys(),
        'title': 'Berita Lingkungan Terkini'
    }
    return render(request, 'edukasi/external_news.html', context)
