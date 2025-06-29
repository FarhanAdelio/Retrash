from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django import forms

class ContactForm(forms.Form):
    nama = forms.CharField(max_length=100)
    email = forms.EmailField()
    subjek = forms.CharField(max_length=200)
    pesan = forms.CharField(widget=forms.Textarea)

class KontakView(FormView):
    template_name = 'kontak/kontak.html'
    form_class = ContactForm
    success_url = reverse_lazy('kontak:index')

    def form_valid(self, form):
        # Di sini Anda bisa menambahkan logika untuk mengirim email
        nama = form.cleaned_data['nama']
        email = form.cleaned_data['email']
        subjek = form.cleaned_data['subjek']
        pesan = form.cleaned_data['pesan']
        
        # Tambahkan logika pengiriman email di sini
        
        messages.success(self.request, 'Terima kasih! Pesan Anda telah terkirim.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Kontak Kami',
            'alamat': 'Jl. Contoh No. 123, Jakarta',
            'telepon': '+62 812-3456-7890',
            'email': 'info@retrash.id',
            'jam_kerja': 'Senin - Jumat: 09:00 - 17:00'
        })
        return context 