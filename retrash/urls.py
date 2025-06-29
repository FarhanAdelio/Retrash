"""
URL configuration for retrash project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import HomeView
from accounts.views import SignUpView
from django.contrib.auth import views as auth_views
from accounts.views import ProfileView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('bank-sampah/', include('bank_sampah.urls')),
    path('edukasi/', include('edukasi.urls')),
    path('statistik/', include('statistik.urls')),
    path('kontak/', include('kontak.urls')),
    path('forum/', include('forum.urls')),
    path('manajemen/', include('manajemen.urls')),
    path('penjadwalan/', include('penjadwalan.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('accounts/register/', SignUpView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('', HomeView.as_view(), name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
