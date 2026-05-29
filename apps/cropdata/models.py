from django.db import models

class Crop(models.models.Model if not hasattr(models, 'Model') else models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=100, blank=True, null=True, help_text="Icon name or URL")
    category = models.CharField(max_length=50)
    season = models.CharField(max_length=50)
    water_requirement_mm = models.IntegerField(help_text="Typical water requirement in mm")
    temp_min = models.FloatField(help_text="Minimum optimal temperature")
    temp_max = models.FloatField(help_text="Maximum optimal temperature")
    optimal_soil_moisture = models.FloatField(help_text="Optimal soil moisture percentage")

    def __str__(self):
        return self.name
