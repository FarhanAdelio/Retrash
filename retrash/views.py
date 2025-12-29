from django.shortcuts import render
from django.views.generic import TemplateView
from manajemen.models import Artikel, BankSampah
from django.db.models import Count

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Ambil 6 artikel terbaru dengan kategori
        artikel_terbaru = Artikel.objects.select_related('kategori', 'penulis').order_by('-tanggal_publikasi')[:6]
        
        # Ambil 6 bank sampah dengan jenis sampah
        bank_terdekat = BankSampah.objects.prefetch_related('jenis_sampah').all()[:6]
        
        context.update({
            'artikel_terbaru': artikel_terbaru,
            'bank_terdekat': bank_terdekat,
            'total_artikel': Artikel.objects.count(),
            'total_bank': BankSampah.objects.count(),
            'title': 'Selamat Datang di ReTrash',
            'description': 'Platform pengelolaan sampah untuk masa depan yang lebih bersih',
        })
        return context 