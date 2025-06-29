from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import BankSampah, Artikel
from .forms import BankSampahForm, ArtikelForm

@login_required
def dashboard(request):
    return render(request, 'manajemen/dashboard.html')

@login_required
def bank_sampah_list(request):
    banks = BankSampah.objects.all()
    return render(request, 'manajemen/bank_sampah_list.html', {'banks': banks})

@login_required
def bank_sampah_create(request):
    if request.method == 'POST':
        form = BankSampahForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bank sampah berhasil ditambahkan.')
            return redirect('manajemen:bank_sampah_list')
    else:
        form = BankSampahForm()
    return render(request, 'manajemen/bank_sampah_form.html', {'form': form})

@login_required
def bank_sampah_update(request, pk):
    bank = get_object_or_404(BankSampah, pk=pk)
    if request.method == 'POST':
        form = BankSampahForm(request.POST, request.FILES, instance=bank)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bank sampah berhasil diperbarui.')
            return redirect('manajemen:bank_sampah_list')
    else:
        form = BankSampahForm(instance=bank)
    return render(request, 'manajemen/bank_sampah_form.html', {'form': form})

@login_required
def bank_sampah_delete(request, pk):
    bank = get_object_or_404(BankSampah, pk=pk)
    if request.method == 'POST':
        bank.delete()
        messages.success(request, 'Bank sampah berhasil dihapus.')
        return redirect('manajemen:bank_sampah_list')
    return render(request, 'manajemen/bank_sampah_confirm_delete.html', {'bank': bank})

@login_required
def artikel_list(request):
    articles = Artikel.objects.all()
    return render(request, 'manajemen/artikel_list.html', {'articles': articles})

@login_required
def artikel_create(request):
    if request.method == 'POST':
        form = ArtikelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Artikel berhasil ditambahkan.')
            return redirect('manajemen:artikel_list')
    else:
        form = ArtikelForm()
    return render(request, 'manajemen/artikel_form.html', {'form': form})

@login_required
def artikel_update(request, pk):
    article = get_object_or_404(Artikel, pk=pk)
    if request.method == 'POST':
        form = ArtikelForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, 'Artikel berhasil diperbarui.')
            return redirect('manajemen:artikel_list')
    else:
        form = ArtikelForm(instance=article)
    return render(request, 'manajemen/artikel_form.html', {'form': form})

@login_required
def artikel_delete(request, pk):
    article = get_object_or_404(Artikel, pk=pk)
    if request.method == 'POST':
        article.delete()
        messages.success(request, 'Artikel berhasil dihapus.')
        return redirect('manajemen:artikel_list')
    return render(request, 'manajemen/artikel_confirm_delete.html', {'article': article})

@login_required
def statistik(request):
    # Logika untuk menampilkan statistik
    return render(request, 'manajemen/statistik.html')
