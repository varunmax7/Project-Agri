from django.db import models

class Crop(models.Model):
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

class CropCalendar(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='calendars')
    agro_zone = models.CharField(max_length=100)
    sowing_start = models.DateField()
    sowing_end = models.DateField()
    vegetative = models.IntegerField(help_text="Days for vegetative stage")
    flowering = models.IntegerField(help_text="Days for flowering stage")
    harvest = models.IntegerField(help_text="Days for harvest stage")

    def __str__(self):
        return f"{self.crop.name} Calendar ({self.agro_zone})"

class BestPractice(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='best_practices')
    stage = models.CharField(max_length=100)
    text = models.TextField()

    def __str__(self):
        return f"{self.crop.name} - {self.stage}"
