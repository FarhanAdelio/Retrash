from django.urls import path
from . import views

app_name = 'statistik'

urlpatterns = [
    path('', views.StatistikView.as_view(), name='index'),
    path('api/', views.StatistikAPIView.as_view(), name='api'),
] 