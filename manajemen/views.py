from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from .models import BankSampah, Artikel, PendaftaranAnggota
from .forms import BankSampahForm, ArtikelForm, PendaftaranAnggotaForm

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


# ============ PENDAFTARAN ANGGOTA VIEWS ============

@login_required(login_url='/accounts/login/')
def pendaftaran_anggota(request):
    """View untuk user mendaftar sebagai anggota bank sampah"""
    
    # Cek apakah user sudah pernah mendaftar
    existing_pendaftaran = PendaftaranAnggota.objects.filter(user=request.user).first()
    
    if existing_pendaftaran:
        messages.warning(request, f'Anda sudah terdaftar dengan status: {existing_pendaftaran.get_status_display()}')
        return redirect('manajemen:status_pendaftaran')
    
    if request.method == 'POST':
        form = PendaftaranAnggotaForm(request.POST, request.FILES)
        if form.is_valid():
            pendaftaran = form.save(commit=False)
            pendaftaran.user = request.user
            pendaftaran.save()
            form.save_m2m()  # Save many-to-many relationships
            
            messages.success(request, 'Pendaftaran berhasil dikirim! Mohon menunggu verifikasi dari admin.')
            return redirect('manajemen:status_pendaftaran')
    else:
        # Pre-fill dengan data dari user profile jika ada
        initial_data = {
            'nama_lengkap': request.user.get_full_name() or request.user.username,
            'email': request.user.email,
        }
        form = PendaftaranAnggotaForm(initial=initial_data)
    
    return render(request, 'manajemen/pendaftaran_anggota.html', {'form': form})


@login_required
def status_pendaftaran(request):
    """View untuk melihat status pendaftaran"""
    pendaftaran = get_object_or_404(PendaftaranAnggota, user=request.user)
    return render(request, 'manajemen/status_pendaftaran.html', {'pendaftaran': pendaftaran})


# Helper function untuk cek apakah user adalah admin/staff
def is_admin(user):
    return user.is_staff or user.is_superuser


@user_passes_test(is_admin)
def admin_verifikasi_pendaftaran(request):
    """View untuk admin melihat dan memverifikasi pendaftaran"""
    pendaftaran_list = PendaftaranAnggota.objects.all().order_by('-tanggal_daftar')
    
    context = {
        'pending': pendaftaran_list.filter(status='pending'),
        'approved': pendaftaran_list.filter(status='approved'),
        'rejected': pendaftaran_list.filter(status='rejected'),
    }
    
    return render(request, 'manajemen/admin_verifikasi.html', context)


@user_passes_test(is_admin)
def admin_approve_pendaftaran(request, pk):
    """View untuk admin menyetujui pendaftaran"""
    pendaftaran = get_object_or_404(PendaftaranAnggota, pk=pk)
    
    if request.method == 'POST':
        pendaftaran.status = 'approved'
        pendaftaran.tanggal_disetujui = timezone.now()
        pendaftaran.nomor_anggota = pendaftaran.generate_nomor_anggota()
        pendaftaran.keterangan_admin = request.POST.get('keterangan', '')
        pendaftaran.save()
        
        messages.success(request, f'Pendaftaran {pendaftaran.nama_lengkap} berhasil disetujui!')
        return redirect('manajemen:admin_verifikasi')
    
    return render(request, 'manajemen/admin_approve.html', {'pendaftaran': pendaftaran})


@user_passes_test(is_admin)
def admin_reject_pendaftaran(request, pk):
    """View untuk admin menolak pendaftaran"""
    pendaftaran = get_object_or_404(PendaftaranAnggota, pk=pk)
    
    if request.method == 'POST':
        pendaftaran.status = 'rejected'
        pendaftaran.keterangan_admin = request.POST.get('keterangan', '')
        pendaftaran.save()
        
        messages.success(request, f'Pendaftaran {pendaftaran.nama_lengkap} ditolak.')
        return redirect('manajemen:admin_verifikasi')
    
    return render(request, 'manajemen/admin_reject.html', {'pendaftaran': pendaftaran})
