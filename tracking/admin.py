from django.contrib import admin
from .models import Pengiriman, TrackingHistory, PenjemputanSchedule

@admin.register(Pengiriman)
class PengirimanAdmin(admin.ModelAdmin):
    list_display = ['kode_tracking', 'user', 'jenis_sampah', 'status', 'berat_estimasi', 'poin_didapat', 'created_at']
    list_filter = ['status', 'jenis_sampah', 'created_at']
    search_fields = ['kode_tracking', 'user__username', 'alamat_jemput']
    readonly_fields = ['kode_tracking', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Informasi Tracking', {
            'fields': ('kode_tracking', 'user', 'status', 'petugas')
        }),
        ('Detail Sampah', {
            'fields': ('jenis_sampah', 'berat_estimasi', 'berat_actual', 'poin_didapat')
        }),
        ('Lokasi', {
            'fields': ('alamat_jemput', 'latitude', 'longitude')
        }),
        ('Timeline', {
            'fields': ('estimated_pickup', 'completed_at', 'created_at', 'updated_at')
        }),
        ('Catatan', {
            'fields': ('catatan',),
            'classes': ('collapse',)
        }),
    )

@admin.register(TrackingHistory)
class TrackingHistoryAdmin(admin.ModelAdmin):
    list_display = ['pengiriman', 'status', 'lokasi', 'petugas', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['pengiriman__kode_tracking', 'keterangan']
    readonly_fields = ['created_at']

@admin.register(PenjemputanSchedule)
class PenjemputanScheduleAdmin(admin.ModelAdmin):
    list_display = ['area', 'hari', 'jam_mulai', 'jam_selesai', 'petugas', 'aktif']
    list_filter = ['hari', 'aktif']
    search_fields = ['area']

