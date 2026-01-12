from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
import uuid

class Pengiriman(models.Model):
    """Model untuk tracking pengiriman sampah"""
    
    STATUS_CHOICES = [
        ('pending', 'Menunggu Penjemputan'),
        ('picked', 'Sedang Dijemput'),
        ('transit', 'Dalam Perjalanan'),
        ('sorting', 'Sedang Dipilah'),
        ('processed', 'Sedang Diproses'),
        ('completed', 'Selesai'),
        ('cancelled', 'Dibatalkan'),
    ]
    
    JENIS_SAMPAH_CHOICES = [
        ('plastik', 'Plastik'),
        ('kertas', 'Kertas'),
        ('logam', 'Logam'),
        ('kaca', 'Kaca'),
        ('organik', 'Organik'),
        ('elektronik', 'Elektronik'),
        ('campuran', 'Campuran'),
    ]
    
    # Primary Fields
    kode_tracking = models.CharField(
        max_length=20, 
        unique=True, 
        editable=False,
        verbose_name='Kode Tracking'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='pengiriman_sampah',
        verbose_name='Pengirim'
    )
    
    # Detail Pengiriman
    jenis_sampah = models.CharField(
        max_length=20,
        choices=JENIS_SAMPAH_CHOICES,
        verbose_name='Jenis Sampah'
    )
    berat_estimasi = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text='Dalam kilogram (kg)',
        verbose_name='Estimasi Berat'
    )
    berat_actual = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Berat setelah ditimbang (kg)',
        verbose_name='Berat Aktual'
    )
    
    # Lokasi
    alamat_jemput = models.TextField(verbose_name='Alamat Penjemputan')
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name='Latitude'
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name='Longitude'
    )
    
    # Status & Timeline
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Status'
    )
    catatan = models.TextField(
        blank=True,
        null=True,
        verbose_name='Catatan Tambahan'
    )
    
    # Poin & Reward
    poin_didapat = models.IntegerField(
        default=0,
        verbose_name='Poin yang Didapat'
    )
    
    # Petugas
    petugas = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pengiriman_ditangani',
        verbose_name='Petugas'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Dibuat Pada')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Diperbarui Pada')
    estimated_pickup = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Estimasi Penjemputan'
    )
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Selesai Pada'
    )
    
    class Meta:
        verbose_name = 'Pengiriman'
        verbose_name_plural = 'Pengiriman'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['kode_tracking']),
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['status']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.kode_tracking:
            # Generate kode tracking: RTR-YYYYMMDD-XXXXX
            today = timezone.now()
            prefix = f"RTR-{today.strftime('%Y%m%d')}"
            random_code = str(uuid.uuid4().hex[:5].upper())
            self.kode_tracking = f"{prefix}-{random_code}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.kode_tracking} - {self.user.username}"
    
    def get_status_display_color(self):
        """Return Bootstrap color class for status"""
        colors = {
            'pending': 'warning',
            'picked': 'info',
            'transit': 'primary',
            'sorting': 'secondary',
            'processed': 'dark',
            'completed': 'success',
            'cancelled': 'danger',
        }
        return colors.get(self.status, 'secondary')
    
    def get_status_icon(self):
        """Return icon for each status"""
        icons = {
            'pending': 'fa-clock',
            'picked': 'fa-truck-pickup',
            'transit': 'fa-shipping-fast',
            'sorting': 'fa-sort',
            'processed': 'fa-cogs',
            'completed': 'fa-check-circle',
            'cancelled': 'fa-times-circle',
        }
        return icons.get(self.status, 'fa-question-circle')


class TrackingHistory(models.Model):
    """Model untuk menyimpan history setiap perubahan status"""
    
    pengiriman = models.ForeignKey(
        Pengiriman,
        on_delete=models.CASCADE,
        related_name='history',
        verbose_name='Pengiriman'
    )
    status = models.CharField(
        max_length=20,
        choices=Pengiriman.STATUS_CHOICES,
        verbose_name='Status'
    )
    keterangan = models.TextField(
        blank=True,
        null=True,
        verbose_name='Keterangan'
    )
    lokasi = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Lokasi'
    )
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )
    petugas = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Petugas'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Waktu')
    
    class Meta:
        verbose_name = 'History Tracking'
        verbose_name_plural = 'History Tracking'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.pengiriman.kode_tracking} - {self.get_status_display()} ({self.created_at})"


class PenjemputanSchedule(models.Model):
    
    HARI_CHOICES = [
        ('senin', 'Senin'),
        ('selasa', 'Selasa'),
        ('rabu', 'Rabu'),
        ('kamis', 'Kamis'),
        ('jumat', 'Jumat'),
        ('sabtu', 'Sabtu'),
        ('minggu', 'Minggu'),
    ]
    
    area = models.CharField(max_length=100, verbose_name='Area/Kelurahan')
    hari = models.CharField(
        max_length=10,
        choices=HARI_CHOICES,
        verbose_name='Hari'
    )
    jam_mulai = models.TimeField(verbose_name='Jam Mulai')
    jam_selesai = models.TimeField(verbose_name='Jam Selesai')
    petugas = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Petugas'
    )
    aktif = models.BooleanField(default=True, verbose_name='Aktif')
    
    class Meta:
        verbose_name = 'Jadwal Penjemputan'
        verbose_name_plural = 'Jadwal Penjemputan'
        ordering = ['hari', 'jam_mulai']
    
    def __str__(self):
        return f"{self.area} - {self.get_hari_display()} ({self.jam_mulai}-{self.jam_selesai})"

