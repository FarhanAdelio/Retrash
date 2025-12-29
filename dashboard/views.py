from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from manajemen.models import Transaksi, PendaftaranAnggota, BankSampah, Artikel
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.

@login_required
def dashboard(request):
    """Dashboard dengan tampilan berbeda untuk user dan admin"""
    
    # Jika user adalah admin/staff
    if request.user.is_staff or request.user.is_superuser:
        return admin_dashboard(request)
    
    # Jika user biasa
    return user_dashboard(request)


def user_dashboard(request):
    """Dashboard untuk user biasa"""
    
    # Cek status pendaftaran
    try:
        pendaftaran = PendaftaranAnggota.objects.get(user=request.user)
        status_anggota = pendaftaran.status
        nomor_anggota = pendaftaran.nomor_anggota
    except PendaftaranAnggota.DoesNotExist:
        pendaftaran = None
        status_anggota = None
        nomor_anggota = None
    
    # Data transaksi user
    total_transaksi = Transaksi.objects.filter(user=request.user).count()
    transaksi_diproses = Transaksi.objects.filter(user=request.user, status='diproses').count()
    
    # Total poin/saldo
    total_poin = sum(
        transaksi.total_harga for transaksi in 
        Transaksi.objects.filter(user=request.user, status='selesai')
    )
    
    # Transaksi terakhir
    transaksi_terakhir = Transaksi.objects.filter(
        user=request.user
    ).order_by('-tanggal_transaksi')[:5]
    
    context = {
        'is_admin': False,
        'pendaftaran': pendaftaran,
        'status_anggota': status_anggota,
        'nomor_anggota': nomor_anggota,
        'total_transaksi': total_transaksi,
        'transaksi_diproses': transaksi_diproses,
        'total_poin': total_poin,
        'transaksi_terakhir': transaksi_terakhir,
    }
    
    return render(request, 'dashboard/user_dashboard.html', context)


def admin_dashboard(request):
    """Dashboard untuk admin"""
    from forum.models import Diskusi
    
    # Statistik umum
    total_users = User.objects.count()
    total_bank_sampah = BankSampah.objects.count()
    total_artikel = Artikel.objects.count()
    
    # Pendaftaran anggota
    pendaftaran_pending = PendaftaranAnggota.objects.filter(status='pending').count()
    pendaftaran_approved = PendaftaranAnggota.objects.filter(status='approved').count()
    
    # Transaksi
    total_transaksi = Transaksi.objects.count()
    transaksi_pending = Transaksi.objects.filter(status='pending').count()
    transaksi_diproses = Transaksi.objects.filter(status='diproses').count()
    
    # Aktivitas terbaru
    recent_users = User.objects.order_by('-date_joined')[:5]
    recent_pendaftaran = PendaftaranAnggota.objects.order_by('-tanggal_daftar')[:5]
    recent_transaksi = Transaksi.objects.order_by('-tanggal_transaksi')[:5]
    
    context = {
        'is_admin': True,
        'total_users': total_users,
        'total_bank_sampah': total_bank_sampah,
        'total_artikel': total_artikel,
        'pendaftaran_pending': pendaftaran_pending,
        'pendaftaran_approved': pendaftaran_approved,
        'total_transaksi': total_transaksi,
        'transaksi_pending': transaksi_pending,
        'transaksi_diproses': transaksi_diproses,
        'recent_users': recent_users,
        'recent_pendaftaran': recent_pendaftaran,
        'recent_transaksi': recent_transaksi,
    }
    
    return render(request, 'dashboard/admin_dashboard.html', context)

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
