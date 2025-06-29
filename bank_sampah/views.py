from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from manajemen.models import BankSampah
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

class BankSampahListView(ListView):
    model = BankSampah
    template_name = 'bank_sampah/bank_list.html'
    context_object_name = 'bank_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Bank Sampah'
        return context

def bank_detail(request, pk):
    bank = get_object_or_404(BankSampah, pk=pk)
    return render(request, 'bank_sampah/bank_detail.html', {
        'bank': bank
    })

def bank_search(request):
    query = request.GET.get('q', '')
    if query:
        bank_list = BankSampah.objects.filter(
            Q(nama__icontains=query) |
            Q(alamat__icontains=query) |
            Q(deskripsi__icontains=query)
        )
    else:
        bank_list = BankSampah.objects.none()
    
    return render(request, 'bank_sampah/bank_search.html', {
        'bank_list': bank_list,
        'query': query
    }) 