from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('transaksi/', views.transaksi_list, name='transaksi_list'),
    path('transaksi/<int:pk>/', views.transaksi_detail, name='transaksi_detail'),
    path('poin/', views.poin_list, name='poin_list'),
] 