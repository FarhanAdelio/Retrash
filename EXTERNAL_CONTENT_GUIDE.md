# PANDUAN INTEGRASI KONTEN EKSTERNAL

## 📋 Overview

Sistem ini memungkinkan website ReTrash untuk mengambil dan menampilkan konten berita/artikel dari sumber eksternal secara otomatis.

## ✅ Yang Sudah Dibuat:

### 1. **Service Layer** (`edukasi/services.py`)
- `ExternalContentService` - Mengambil artikel dari RSS Feed
- `WebScraperService` - Web scraping (opsional, gunakan dengan hati-hati)

### 2. **Views** (`edukasi/views.py`)
- `external_news()` - View untuk menampilkan berita eksternal
- Update `EdukasiListView` dengan konten eksternal

### 3. **Template** 
- `external_news.html` - Tampilan berita dari sumber eksternal
- Update `edukasi_list.html` dengan link ke berita terkini

### 4. **URLs**
- `/edukasi/berita-eksternal/` - Halaman berita eksternal
- `/edukasi/berita-eksternal/?source=mongabay` - Filter by source

---

## 🌐 Sumber RSS Feed yang Tersedia:

1. **Mongabay Indonesia** - https://www.mongabay.co.id/feed/
   - Berita lingkungan dan konservasi

2. **Greeners** - https://www.greeners.co/feed/
   - Media lingkungan Indonesia

### Tambah Sumber Baru:

Edit `edukasi/services.py`:
```python
RSS_FEEDS = {
    'mongabay': 'https://www.mongabay.co.id/feed/',
    'greeners': 'https://www.greeners.co/feed/',
    'nama_sumber_baru': 'https://example.com/feed/',  # Tambah di sini
}
```

---

## 🔧 Cara Menggunakan:

### 1. **Di Template/View:**

```python
from edukasi.services import ExternalContentService

# Ambil dari 1 sumber
articles = ExternalContentService.get_rss_articles(
    source='mongabay',
    limit=10
)

# Ambil dari semua sumber
all_articles = ExternalContentService.get_all_sources(
    limit_per_source=5
)
```

### 2. **Akses URL:**
- Semua sumber: `http://127.0.0.1:8000/edukasi/berita-eksternal/`
- Filter: `http://127.0.0.1:8000/edukasi/berita-eksternal/?source=mongabay`

---

## ⚡ Fitur Cache:

- **Data di-cache selama 1 jam** untuk performa optimal
- Cache otomatis, tidak perlu setup tambahan
- Update manual: restart Django server

---

## 🔄 Auto-Update (Opsional):

### Gunakan Celery Beat untuk auto-update berkala:

1. Install Celery (sudah ada di requirements.txt)

2. Buat file `edukasi/tasks.py`:
```python
from celery import shared_task
from .services import ExternalContentService

@shared_task
def update_external_news():
    """Update cache untuk semua sumber"""
    ExternalContentService.get_all_sources(limit_per_source=10)
    return "External news updated successfully"
```

3. Setup Celery Beat di `settings.py`:
```python
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'update-external-news-hourly': {
        'task': 'edukasi.tasks.update_external_news',
        'schedule': crontab(minute=0),  # Setiap jam
    },
}
```

---

## 🔐 Legal & Best Practices:

### ✅ AMAN (Recommended):
- ✅ Menggunakan RSS Feed (public feed)
- ✅ Menampilkan judul + snippet + link ke sumber asli
- ✅ Mencantumkan credit ke sumber
- ✅ Tidak menyimpan konten lengkap

### ⚠️ HATI-HATI:
- Web scraping tanpa permission
- Menyimpan/republish konten lengkap
- Tidak memberi credit ke sumber

### 📜 Rekomendasi:
1. **Selalu** link ke artikel asli
2. **Hanya** tampilkan snippet/preview
3. **Berikan** credit yang jelas
4. **Patuhi** robots.txt
5. **Respect** rate limits

---

## 🚀 Sumber RSS Feed Tambahan (Recommendations):

```python
RSS_FEEDS = {
    # Lingkungan Indonesia
    'mongabay': 'https://www.mongabay.co.id/feed/',
    'greeners': 'https://www.greeners.co/feed/',
    
    # Bisa tambahkan dari:
    # - Website pemerintah (KLHK, dll)
    # - NGO lingkungan
    # - Media massa (Kompas, Tempo - kategori lingkungan)
    # - Blog teknologi sampah
}
```

---

## 🧪 Testing:

```bash
# Test RSS parsing
python manage.py shell

>>> from edukasi.services import ExternalContentService
>>> articles = ExternalContentService.get_rss_articles('mongabay', 5)
>>> for a in articles:
...     print(a['title'])
```

---

## 📊 Monitoring:

- Cek cache: Django admin > Cache
- Cek logs: File `logs/external_content.log` (jika logging enabled)
- Error handling: Sudah built-in, return empty list jika error

---

## 🔮 Fitur Lanjutan (Future):

1. **News API Integration** - Gunakan API berbayar untuk lebih banyak sumber
2. **ML Content Filtering** - Filter artikel yang relevan dengan sampah
3. **Auto Translation** - Translate artikel bahasa Inggris
4. **Sentiment Analysis** - Analisis sentimen berita lingkungan
5. **Save to Database** - Simpan artikel favorit ke database

---

## ⚙️ Troubleshooting:

### Problem: Artikel tidak muncul
- **Solution**: Cek koneksi internet, cek apakah RSS feed masih aktif

### Problem: Gambar tidak muncul
- **Solution**: Beberapa RSS feed tidak menyertakan gambar, ini normal

### Problem: Cache tidak update
- **Solution**: Clear cache: `python manage.py clear_cache` atau restart server

---

## 📞 Support:

Jika ada error atau butuh bantuan:
1. Cek file `edukasi/services.py`
2. Review error logs
3. Test RSS feed di browser dulu

**Sistem sudah siap digunakan!** 🎉
