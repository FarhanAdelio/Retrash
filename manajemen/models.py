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
