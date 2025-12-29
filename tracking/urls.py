from django.urls import path
from . import views

app_name = 'tracking'

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('<str:kode_tracking>/', views.track, name='detail'),
    path('my/shipments/', views.my_shipments, name='my_shipments'),
    path('my/create/', views.create_shipment, name='create'),
    path('info/schedule/', views.schedule, name='schedule'),
]
