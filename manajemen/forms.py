from django import forms
from .models import BankSampah, Artikel, JenisSampah, KategoriArtikel

class BankSampahForm(forms.ModelForm):
    class Meta:
        model = BankSampah
        fields = ['nama', 'alamat', 'telepon', 'email', 'jam_operasional', 
                 'deskripsi', 'latitude', 'longitude', 'gambar', 'jenis_sampah']
        widgets = {
            'alamat': forms.Textarea(attrs={'rows': 3}),
            'deskripsi': forms.Textarea(attrs={'rows': 3}),
            'jam_operasional': forms.TextInput(attrs={'placeholder': 'Contoh: Senin-Jumat 08:00-17:00'}),
        }

class ArtikelForm(forms.ModelForm):
    class Meta:
        model = Artikel
        fields = ['judul', 'slug', 'konten', 'gambar', 'kategori']
        widgets = {
            'konten': forms.Textarea(attrs={'rows': 10}),
            'slug': forms.TextInput(attrs={'placeholder': 'contoh-judul-artikel'}),
        }

class JenisSampahForm(forms.ModelForm):
    class Meta:
        model = JenisSampah
        fields = ['nama', 'deskripsi', 'harga_per_kg']
        widgets = {
            'deskripsi': forms.Textarea(attrs={'rows': 3}),
            'harga_per_kg': forms.NumberInput(attrs={'step': '0.01'}),
        }

class KategoriArtikelForm(forms.ModelForm):
    class Meta:
        model = KategoriArtikel
        fields = ['nama', 'slug']
        widgets = {
            'slug': forms.TextInput(attrs={'placeholder': 'contoh-kategori'}),
        } 