from django.contrib.gis.db import models
from django.conf import settings
from apps.cropdata.models import Crop

class Farm(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='farms')
    name = models.CharField(max_length=100)
    village = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    
    # GeoDjango PointField for storing longitude, latitude
    location = models.PointField(srid=4326)
    
    area_acres = models.FloatField()
    soil_type = models.CharField(max_length=100)
    irrigation_source = models.CharField(max_length=100)
    elevation = models.FloatField(null=True, blank=True)
    
    primary_crops = models.ManyToManyField(Crop, related_name='farms', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.user.username}"
