from django.contrib import admin
from .models import Kategori, Diskusi, Komentar

@admin.register(Kategori)
class KategoriAdmin(admin.ModelAdmin):
    list_display = ('nama', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('nama',)}
    search_fields = ('nama', 'deskripsi')

@admin.register(Diskusi)
class DiskusiAdmin(admin.ModelAdmin):
    list_display = ('judul', 'penulis', 'created_at', 'is_solved', 'view_count')
    list_filter = ('is_solved', 'created_at')
    search_fields = ('judul', 'isi', 'penulis__username')
    prepopulated_fields = {'slug': ('judul',)}
    date_hierarchy = 'created_at'

@admin.register(Komentar)
class KomentarAdmin(admin.ModelAdmin):
    list_display = ('diskusi', 'penulis', 'created_at', 'is_solution')
    list_filter = ('is_solution', 'created_at')
    search_fields = ('isi', 'penulis__username', 'diskusi__judul')
