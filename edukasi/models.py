from django.db import models
from django.utils.translation import gettext_lazy as _

class RecyclingCenter(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    operating_hours = models.TextField()
    accepted_materials = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class EducationalContent(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('article', 'Article'),
        ('guide', 'Guide'),
        ('video', 'Video'),
        ('infographic', 'Infographic'),
    ]

    title = models.CharField(max_length=200)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES)
    content = models.TextField()
    thumbnail = models.ImageField(upload_to='educational_content/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    is_published = models.BooleanField(default=False)
    published_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
