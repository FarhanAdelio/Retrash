from django import forms
from .models import BankSampah, Artikel, JenisSampah, KategoriArtikel, PendaftaranAnggota

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


class PendaftaranAnggotaForm(forms.ModelForm):
    class Meta:
        model = PendaftaranAnggota
        fields = [
            'nama_lengkap', 'nik', 'nomor_telepon', 'email',
            'alamat_lengkap', 'rt_rw', 'kelurahan', 'kecamatan', 'kota', 'kode_pos',
            'bank_sampah', 'jenis_sampah_disetor', 'estimasi_volume', 'foto_ktp', 'alasan_bergabung'
        ]
        widgets = {
            'nama_lengkap': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan nama lengkap'}),
            'nik': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan NIK (16 digit)', 'maxlength': '16'}),
            'nomor_telepon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: 08123456789'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'alamat_lengkap': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Alamat lengkap'}),
            'rt_rw': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: 001/002'}),
            'kelurahan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama kelurahan/desa'}),
            'kecamatan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama kecamatan'}),
            'kota': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama kota/kabupaten'}),
            'kode_pos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kode pos', 'maxlength': '6'}),
            'bank_sampah': forms.Select(attrs={'class': 'form-control'}),
            'jenis_sampah_disetor': forms.CheckboxSelectMultiple(),
            'estimasi_volume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: 10-15 kg'}),
            'foto_ktp': forms.FileInput(attrs={'class': 'form-control'}),
            'alasan_bergabung': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Opsional'}),
        }
        
    def clean_nik(self):
        nik = self.cleaned_data.get('nik')
        if not nik.isdigit():
            raise forms.ValidationError('NIK harus berupa angka')
        if len(nik) != 16:
            raise forms.ValidationError('NIK harus 16 digit')
        return nik
    
    def clean_nomor_telepon(self):
        nomor = self.cleaned_data.get('nomor_telepon')
        if not nomor.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            raise forms.ValidationError('Nomor telepon tidak valid')
        return nomor 