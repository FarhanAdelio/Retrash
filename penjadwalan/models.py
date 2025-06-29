from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from manajemen.models import WasteLocation
from django.conf import settings

class CollectionSchedule(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    location = models.ForeignKey(WasteLocation, on_delete=models.CASCADE)
    scheduled_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    assigned_collector = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Collection at {self.location.name} on {self.scheduled_date}"

class CollectionRecord(models.Model):
    schedule = models.ForeignKey(CollectionSchedule, on_delete=models.CASCADE)
    actual_collection_date = models.DateTimeField()
    collected_weight = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Record for {self.schedule}"

class Schedule(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Menunggu'),
        ('confirmed', 'Dikonfirmasi'),
        ('completed', 'Selesai'),
        ('cancelled', 'Dibatalkan'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tanggal = models.DateField()
    waktu = models.TimeField()
    lokasi = models.CharField(max_length=200)
    jenis_sampah = models.CharField(max_length=100)
    berat_perkiraan = models.DecimalField(max_digits=5, decimal_places=2)
    catatan = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['tanggal', 'waktu']

    def __str__(self):
        return f"{self.user.username} - {self.tanggal} {self.waktu}"
