from django.urls import path
from . import views

app_name = 'edukasi'

urlpatterns = [
    path('', views.EdukasiListView.as_view(), name='list'),
    path('search/', views.edukasi_search, name='search'),
    path('<int:pk>/', views.EdukasiDetailView.as_view(), name='detail'),
] 