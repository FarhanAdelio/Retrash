from django.urls import path
from . import views

app_name = 'bank_sampah'

urlpatterns = [
    path('', views.BankSampahListView.as_view(), name='list'),
    path('<int:pk>/', views.bank_detail, name='detail'),
    path('search/', views.bank_search, name='search'),
] 