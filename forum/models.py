from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify

class Kategori(models.Model):
    nama = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    deskripsi = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='fas fa-folder')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Kategori"
        ordering = ['nama']

    def __str__(self):
        return self.nama

    def get_absolute_url(self):
        return reverse('forum:kategori_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nama)
        super().save(*args, **kwargs)

class Diskusi(models.Model):
    judul = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    isi = models.TextField()
    penulis = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    kategori = models.ForeignKey(Kategori, on_delete=models.SET_NULL, null=True, blank=True, related_name='diskusi')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_solved = models.BooleanField(default=False)
    view_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name_plural = "Diskusi"
        ordering = ['-created_at']

    def __str__(self):
        return self.judul

    def get_absolute_url(self):
        return reverse('forum:diskusi_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.judul)
        super().save(*args, **kwargs)

    @property
    def jumlah_komentar(self):
        return self.komentar.count()

class Komentar(models.Model):
    diskusi = models.ForeignKey(Diskusi, on_delete=models.CASCADE, related_name='komentar')
    penulis = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    isi = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_solution = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "Komentar"
        ordering = ['created_at']

    def __str__(self):
        return f'Komentar oleh {self.penulis.username} pada {self.diskusi.judul}'
