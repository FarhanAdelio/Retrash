from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth import login, logout
from django.contrib import messages
from django.db import transaction
from django.views import View
from .forms import CustomUserCreationForm
from .models import User, Profile

# Create your views here.

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Akun berhasil dibuat! Silakan login.')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Terjadi kesalahan dalam pendaftaran. Silakan coba lagi.')
        return super().form_invalid(form)

class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Anda telah berhasil keluar.')
        return redirect('/')

class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'accounts/profile.html'
    fields = ['first_name', 'last_name', 'email', 'phone_number']
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        with transaction.atomic():
            # Save User model
            user = form.save(commit=False)
            user.save()

            # Get or create Profile
            profile, created = Profile.objects.get_or_create(user=user)

            # Update Profile fields
            profile.address = self.request.POST.get('address', '')
            profile.city = self.request.POST.get('city', '')
            profile.postal_code = self.request.POST.get('postal_code', '')

            # Handle profile picture upload
            if 'profile_picture' in self.request.FILES:
                profile.profile_picture = self.request.FILES['profile_picture']
            
            profile.save()

            messages.success(self.request, 'Profil berhasil diperbarui!')
            return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Terjadi kesalahan dalam memperbarui profil. Silakan coba lagi.')
        return super().form_invalid(form)

