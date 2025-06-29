from django.shortcuts import render
from django.views.generic import TemplateView
from manajemen.models import Artikel, BankSampah

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['artikel_terbaru'] = Artikel.objects.all().order_by('-tanggal_publikasi')[:3]
        context['bank_terdekat'] = BankSampah.objects.all()[:3]
        context.update({
            'title': 'Selamat Datang di ReTrash',
            'description': 'Platform pengelolaan sampah untuk masa depan yang lebih bersih',
        })
        return context 