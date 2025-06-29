from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from manajemen.models import WasteItem
from penjadwalan.models import CollectionSchedule

class DashboardMetrics(models.Model):
    total_users = models.IntegerField(default=0)
    total_waste_collected = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_recycled_waste = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    active_collection_schedules = models.IntegerField(default=0)
    completed_collections = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Metrics for {self.date}"

class UserActivity(models.Model):
    ACTIVITY_TYPE_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('waste_submission', 'Waste Submission'),
        ('schedule_creation', 'Schedule Creation'),
        ('profile_update', 'Profile Update'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPE_CHOICES)
    description = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.activity_type} at {self.created_at}"
