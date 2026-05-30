from django.db import models
from django.conf import settings
from apps.cropdata.models import Crop

class Farm(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='farms')
    name = models.CharField(max_length=100)
    village = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    
    # Storing longitude, latitude as JSON dict: {"type": "Point", "coordinates": [lng, lat]}
    location = models.JSONField(default=dict)
    
    area_acres = models.FloatField()
    soil_type = models.CharField(max_length=100)
    irrigation_source = models.CharField(max_length=100)
    elevation = models.FloatField(null=True, blank=True)
    
    primary_crops = models.ManyToManyField(Crop, related_name='farms', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.user.username}"

class Field(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='fields')
    name = models.CharField(max_length=100)
    area = models.FloatField(help_text="Area in acres")
    current_crop = models.ForeignKey(Crop, on_delete=models.SET_NULL, null=True, blank=True, related_name='fields')
    
    def __str__(self):
        return f"{self.name} ({self.farm.name})"

class ActivityLog(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='activity_logs')
    activity = models.CharField(max_length=200)
    date = models.DateField()
    note = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.activity} on {self.date} for {self.farm.name}"
