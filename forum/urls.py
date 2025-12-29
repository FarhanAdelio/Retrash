from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.DiskusiListView.as_view(), name='list'),
    path('kategori/', views.KategoriListView.as_view(), name='kategori_list'),
    path('kategori/<slug:slug>/', views.KategoriDetailView.as_view(), name='kategori_detail'),
    path('diskusi/baru/', views.DiskusiCreateView.as_view(), name='diskusi_baru'),
    path('diskusi/<slug:slug>/', views.DiskusiDetailView.as_view(), name='diskusi_detail'),
    path('diskusi/<slug:slug>/edit/', views.DiskusiUpdateView.as_view(), name='diskusi_edit'),
    path('diskusi/<slug:slug>/hapus/', views.DiskusiDeleteView.as_view(), name='diskusi_hapus'),
    path('diskusi/<slug:slug>/komentar/', views.KomentarCreateView.as_view(), name='komentar_baru'),
    path('komentar/<int:pk>/edit/', views.KomentarUpdateView.as_view(), name='edit_komentar'),
    path('komentar/<int:pk>/hapus/', views.KomentarDeleteView.as_view(), name='hapus_komentar'),
    path('komentar/<int:komentar_id>/edit/', views.edit_komentar_ajax, name='edit_komentar_ajax'),
] 