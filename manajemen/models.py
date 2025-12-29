from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Create your models here.

class WasteType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    recycling_instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class WasteItem(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('collected', 'Collected'),
        ('recycled', 'Recycled'),
        ('disposed', 'Disposed'),
    ]

    waste_type = models.ForeignKey(WasteType, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    collection_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.waste_type.name} - {self.weight}kg"

class WasteLocation(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    capacity = models.DecimalField(max_digits=10, decimal_places=2)
    current_occupancy = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class JenisSampah(models.Model):
    nama = models.CharField(max_length=100)
    deskripsi = models.TextField()
    harga_per_kg = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nama

class BankSampah(models.Model):
    nama = models.CharField(max_length=200)
    alamat = models.TextField()
    telepon = models.CharField(max_length=20)
    email = models.EmailField()
    jam_operasional = models.CharField(max_length=100)
    deskripsi = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    gambar = models.ImageField(upload_to='bank_sampah/')
    jenis_sampah = models.ManyToManyField(JenisSampah)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nama

class KategoriArtikel(models.Model):
    nama = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.nama

class Artikel(models.Model):
    judul = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    konten = models.TextField()
    gambar = models.ImageField(upload_to='artikel/')
    kategori = models.ForeignKey(KategoriArtikel, on_delete=models.CASCADE)
    penulis = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tanggal_publikasi = models.DateTimeField(auto_now_add=True)
    tanggal_update = models.DateTimeField(auto_now=True)
    dilihat = models.IntegerField(default=0)

    def __str__(self):
        return self.judul

class Transaksi(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('diproses', 'Diproses'),
        ('selesai', 'Selesai'),
        ('dibatalkan', 'Dibatalkan'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bank_sampah = models.ForeignKey(BankSampah, on_delete=models.CASCADE)
    jenis_sampah = models.ForeignKey(JenisSampah, on_delete=models.CASCADE)
    berat = models.DecimalField(max_digits=10, decimal_places=2)
    total_harga = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    tanggal_transaksi = models.DateTimeField(auto_now_add=True)
    tanggal_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.bank_sampah.nama} - {self.tanggal_transaksi}"


class PendaftaranAnggota(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Menunggu Verifikasi'),
        ('approved', 'Disetujui'),
        ('rejected', 'Ditolak'),
    ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pendaftaran')
    
    # Data Pribadi
    nama_lengkap = models.CharField(max_length=200, verbose_name='Nama Lengkap')
    nik = models.CharField(max_length=16, unique=True, verbose_name='NIK')
    nomor_telepon = models.CharField(max_length=15, verbose_name='Nomor Telepon/WhatsApp')
    email = models.EmailField(verbose_name='Email')
    
    # Data Alamat
    alamat_lengkap = models.TextField(verbose_name='Alamat Lengkap')
    rt_rw = models.CharField(max_length=10, verbose_name='RT/RW')
    kelurahan = models.CharField(max_length=100, verbose_name='Kelurahan/Desa')
    kecamatan = models.CharField(max_length=100, verbose_name='Kecamatan')
    kota = models.CharField(max_length=100, verbose_name='Kota/Kabupaten')
    kode_pos = models.CharField(max_length=6, verbose_name='Kode Pos')
    
    # Data Tambahan
    bank_sampah = models.ForeignKey(BankSampah, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Bank Sampah Terdekat')
    jenis_sampah_disetor = models.ManyToManyField(JenisSampah, blank=True, verbose_name='Jenis Sampah yang Disetor')
    estimasi_volume = models.CharField(max_length=50, help_text='Estimasi volume sampah per bulan (kg)', verbose_name='Estimasi Volume')
    foto_ktp = models.ImageField(upload_to='ktp_anggota/', null=True, blank=True, verbose_name='Foto KTP')
    alasan_bergabung = models.TextField(blank=True, verbose_name='Alasan Bergabung')
    
    # Status dan Tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Status')
    tanggal_daftar = models.DateTimeField(auto_now_add=True, verbose_name='Tanggal Pendaftaran')
    tanggal_disetujui = models.DateTimeField(null=True, blank=True, verbose_name='Tanggal Disetujui')
    keterangan_admin = models.TextField(blank=True, help_text='Catatan dari admin', verbose_name='Keterangan Admin')
    
    # Nomor Anggota (auto-generated setelah approved)
    nomor_anggota = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name='Nomor Anggota')
    
    class Meta:
        verbose_name = 'Pendaftaran Anggota'
        verbose_name_plural = 'Pendaftaran Anggota'
        ordering = ['-tanggal_daftar']
    
    def __str__(self):
        return f"{self.nama_lengkap} - {self.get_status_display()}"
    
    def generate_nomor_anggota(self):
        """Generate nomor anggota unik"""
        from datetime import datetime
        year = datetime.now().year
        count = PendaftaranAnggota.objects.filter(status='approved').count() + 1
        return f"BS{year}{count:05d}"
