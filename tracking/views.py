from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from .models import Pengiriman, TrackingHistory, PenjemputanSchedule
from django.db.models import Q

def index(request):
    """Halaman utama tracking - search tracking number"""
    context = {
        'title': 'Lacak Pengiriman',
    }
    return render(request, 'tracking/index.html', context)

def track(request, kode_tracking):
    """Halaman detail tracking"""
    pengiriman = get_object_or_404(Pengiriman, kode_tracking=kode_tracking)
    
    context = {
        'title': f'Tracking {kode_tracking}',
        'pengiriman': pengiriman,
        'history': pengiriman.history.all(),
    }
    return render(request, 'tracking/detail.html', context)

def search(request):
    """API endpoint untuk search tracking"""
    kode = request.GET.get('kode', '').strip()
    
    if not kode:
        return JsonResponse({'error': 'Kode tracking tidak boleh kosong'}, status=400)
    
    try:
        pengiriman = Pengiriman.objects.get(kode_tracking__iexact=kode)
        return JsonResponse({
            'success': True,
            'redirect_url': f'/tracking/{pengiriman.kode_tracking}/'
        })
    except Pengiriman.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Kode tracking tidak ditemukan'
        }, status=404)

@login_required
def my_shipments(request):
    """Daftar pengiriman user"""
    pengiriman_list = Pengiriman.objects.filter(user=request.user)
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        pengiriman_list = pengiriman_list.filter(status=status_filter)
    
    context = {
        'title': 'Pengiriman Saya',
        'pengiriman_list': pengiriman_list,
        'status_choices': Pengiriman.STATUS_CHOICES,
    }
    return render(request, 'tracking/my_shipments.html', context)

@login_required
def create_shipment(request):
    """Buat pengiriman baru"""
    if request.method == 'POST':
        jenis_sampah = request.POST.get('jenis_sampah')
        berat_estimasi = request.POST.get('berat_estimasi')
        alamat_jemput = request.POST.get('alamat_jemput')
        catatan = request.POST.get('catatan', '')
        
        # Validasi
        if not all([jenis_sampah, berat_estimasi, alamat_jemput]):
            messages.error(request, 'Mohon lengkapi semua field yang wajib diisi')
            return redirect('tracking:create')
        
        # Buat pengiriman
        pengiriman = Pengiriman.objects.create(
            user=request.user,
            jenis_sampah=jenis_sampah,
            berat_estimasi=berat_estimasi,
            alamat_jemput=alamat_jemput,
            catatan=catatan,
            status='pending'
        )
        
        # Buat history pertama
        TrackingHistory.objects.create(
            pengiriman=pengiriman,
            status='pending',
            keterangan='Permintaan penjemputan dibuat',
            lokasi=alamat_jemput
        )
        
        messages.success(request, f'Pengiriman berhasil dibuat! Kode tracking: {pengiriman.kode_tracking}')
        return redirect('tracking:detail', kode_tracking=pengiriman.kode_tracking)
    
    context = {
        'title': 'Buat Permintaan Penjemputan',
        'jenis_sampah_choices': Pengiriman.JENIS_SAMPAH_CHOICES,
        'schedules': PenjemputanSchedule.objects.filter(aktif=True),
    }
    return render(request, 'tracking/create.html', context)

def schedule(request):
    """Halaman jadwal penjemputan"""
    schedules = PenjemputanSchedule.objects.filter(aktif=True)
    
    context = {
        'title': 'Jadwal Penjemputan',
        'schedules': schedules,
    }
    return render(request, 'tracking/schedule.html', context)

