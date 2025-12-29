from django.contrib import admin
from .models import (
    WasteType, WasteItem, WasteLocation, 
    JenisSampah, BankSampah, KategoriArtikel, 
    Artikel, Transaksi, PendaftaranAnggota
)

# Register your models here.

@admin.register(WasteType)
class WasteTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

@admin.register(WasteItem)
class WasteItemAdmin(admin.ModelAdmin):
    list_display = ['waste_type', 'weight', 'status', 'collection_date']
    list_filter = ['status', 'collection_date']
    search_fields = ['waste_type__name']

@admin.register(WasteLocation)
class WasteLocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'capacity', 'current_occupancy', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'address']

@admin.register(JenisSampah)
class JenisSampahAdmin(admin.ModelAdmin):
    list_display = ['nama', 'harga_per_kg']
    search_fields = ['nama']

@admin.register(BankSampah)
class BankSampahAdmin(admin.ModelAdmin):
    list_display = ['nama', 'alamat', 'telepon', 'email']
    search_fields = ['nama', 'alamat']
    filter_horizontal = ['jenis_sampah']

@admin.register(KategoriArtikel)
class KategoriArtikelAdmin(admin.ModelAdmin):
    list_display = ['nama', 'slug']
    prepopulated_fields = {'slug': ('nama',)}

@admin.register(Artikel)
class ArtikelAdmin(admin.ModelAdmin):
    list_display = ['judul', 'kategori', 'penulis', 'tanggal_publikasi', 'dilihat']
    list_filter = ['kategori', 'tanggal_publikasi']
    search_fields = ['judul', 'konten']
    prepopulated_fields = {'slug': ('judul',)}

@admin.register(Transaksi)
class TransaksiAdmin(admin.ModelAdmin):
    list_display = ['user', 'bank_sampah', 'jenis_sampah', 'berat', 'total_harga', 'status', 'tanggal_transaksi']
    list_filter = ['status', 'tanggal_transaksi', 'bank_sampah']
    search_fields = ['user__username', 'bank_sampah__nama']

@admin.register(PendaftaranAnggota)
class PendaftaranAnggotaAdmin(admin.ModelAdmin):
    list_display = ['nama_lengkap', 'nik', 'nomor_telepon', 'status', 'nomor_anggota', 'tanggal_daftar']
    list_filter = ['status', 'tanggal_daftar', 'bank_sampah']
    search_fields = ['nama_lengkap', 'nik', 'nomor_telepon', 'nomor_anggota']
    readonly_fields = ['tanggal_daftar', 'tanggal_disetujui', 'nomor_anggota']
    filter_horizontal = ['jenis_sampah_disetor']
    
    fieldsets = (
        ('Data Pribadi', {
            'fields': ('user', 'nama_lengkap', 'nik', 'nomor_telepon', 'email')
        }),
        ('Alamat', {
            'fields': ('alamat_lengkap', 'rt_rw', 'kelurahan', 'kecamatan', 'kota', 'kode_pos')
        }),
        ('Informasi Tambahan', {
            'fields': ('bank_sampah', 'jenis_sampah_disetor', 'estimasi_volume', 'foto_ktp', 'alasan_bergabung')
        }),
        ('Status & Verifikasi', {
            'fields': ('status', 'nomor_anggota', 'tanggal_daftar', 'tanggal_disetujui', 'keterangan_admin')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        # Auto-generate nomor anggota when status changed to approved
        if obj.status == 'approved' and not obj.nomor_anggota:
            from django.utils import timezone
            obj.nomor_anggota = obj.generate_nomor_anggota()
            obj.tanggal_disetujui = timezone.now()
        super().save_model(request, obj, form, change)
