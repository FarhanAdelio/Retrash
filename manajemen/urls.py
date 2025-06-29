from django.urls import path
from . import views

app_name = 'manajemen'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('bank-sampah/', views.bank_sampah_list, name='bank_sampah_list'),
    path('bank-sampah/tambah/', views.bank_sampah_create, name='bank_sampah_create'),
    path('bank-sampah/<int:pk>/edit/', views.bank_sampah_update, name='bank_sampah_update'),
    path('bank-sampah/<int:pk>/hapus/', views.bank_sampah_delete, name='bank_sampah_delete'),
    path('artikel/', views.artikel_list, name='artikel_list'),
    path('artikel/tambah/', views.artikel_create, name='artikel_create'),
    path('artikel/<int:pk>/edit/', views.artikel_update, name='artikel_update'),
    path('artikel/<int:pk>/hapus/', views.artikel_delete, name='artikel_delete'),
    path('statistik/', views.statistik, name='statistik'),
] 