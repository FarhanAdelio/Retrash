from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from manajemen.models import Transaksi

# Create your views here.

@login_required
def dashboard(request):
    # Hitung total transaksi
    total_transaksi = Transaksi.objects.filter(user=request.user).count()
    
    # Hitung transaksi yang sedang diproses
    transaksi_diproses = Transaksi.objects.filter(
        user=request.user,
        status='diproses'
    ).count()
    
    # Hitung total poin
    total_poin = sum(
        transaksi.total_harga for transaksi in 
        Transaksi.objects.filter(user=request.user, status='selesai')
    )
    
    # Ambil 5 transaksi terakhir
    transaksi_terakhir = Transaksi.objects.filter(
        user=request.user
    ).order_by('-tanggal_transaksi')[:5]
    
    context = {
        'total_transaksi': total_transaksi,
        'transaksi_diproses': transaksi_diproses,
        'total_poin': total_poin,
        'transaksi_terakhir': transaksi_terakhir,
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        # Update profil user
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()
    
    return render(request, 'dashboard/profile.html')

@login_required
def transaksi_list(request):
    transaksi_list = Transaksi.objects.filter(
        user=request.user
    ).order_by('-tanggal_transaksi')
    
    context = {
        'transaksi_list': transaksi_list,
    }
    return render(request, 'dashboard/transaksi_list.html', context)

@login_required
def transaksi_detail(request, pk):
    transaksi = get_object_or_404(Transaksi, pk=pk, user=request.user)
    
    context = {
        'transaksi': transaksi,
    }
    return render(request, 'dashboard/transaksi_detail.html', context)

@login_required
def poin_list(request):
    # Hitung total poin
    total_poin = sum(
        transaksi.total_harga for transaksi in 
        Transaksi.objects.filter(user=request.user, status='selesai')
    )
    
    # Ambil riwayat transaksi yang sudah selesai
    transaksi_selesai = Transaksi.objects.filter(
        user=request.user,
        status='selesai'
    ).order_by('-tanggal_transaksi')
    
    context = {
        'total_poin': total_poin,
        'transaksi_selesai': transaksi_selesai,
    }
    return render(request, 'dashboard/poin_list.html', context)
