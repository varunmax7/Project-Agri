from django.db import models

class LocationClimateIndex(models.Model):
    class RiskLevel(models.TextChoices):
        LOW = 'low', 'Low'
        MODERATE = 'moderate', 'Moderate'
        HIGH = 'high', 'High'
        VERY_HIGH = 'very_high', 'Very High'

    farm = models.ForeignKey('farms.Farm', on_delete=models.CASCADE, related_name='climate_indices', null=True, blank=True)
    district = models.CharField(max_length=100, blank=True)
    season = models.CharField(max_length=20)
    year = models.PositiveIntegerField()
    rainfall_outlook_pct = models.DecimalField(max_digits=5, decimal_places=2)
    water_stress_score = models.DecimalField(max_digits=4, decimal_places=1)
    heat_stress_score = models.DecimalField(max_digits=4, decimal_places=1)
    agri_resilience_score = models.DecimalField(max_digits=4, decimal_places=1)
    climate_stress_index = models.DecimalField(max_digits=4, decimal_places=1)
    climate_risk_level = models.CharField(max_length=10, choices=RiskLevel.choices)
    rainfall_confidence = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    water_stress_confidence = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    heat_stress_confidence = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    agri_resilience_confidence = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    csi_confidence = models.DecimalField(max_digits=4, decimal_places=1, default=0)

    class Meta:
        unique_together = ('farm', 'season', 'year')

    def __str__(self):
        return f"{self.farm or self.district} — {self.season} {self.year}"


class ClimateRiskZone(models.Model):
    class RiskLevel(models.TextChoices):
        LOW = 'low', 'Low'
        MODERATE = 'moderate', 'Moderate'
        HIGH = 'high', 'High'
        VERY_HIGH = 'very_high', 'Very High'

    # Stored as GeoJSON Feature dictionary: {"type": "MultiPolygon", "coordinates": [...]}
    geometry = models.JSONField(default=dict)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    risk_level = models.CharField(max_length=10, choices=RiskLevel.choices)
    season = models.CharField(max_length=20)
    layer_type = models.CharField(max_length=50, default='climate_risk')

    def __str__(self):
        return f"{self.district} — {self.risk_level} ({self.season})"


class VegetationObservation(models.Model):
    farm = models.ForeignKey('farms.Farm', on_delete=models.CASCADE, related_name='vegetation_observations', null=True, blank=True)
    field = models.ForeignKey('farms.Field', on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()
    ndvi = models.DecimalField(max_digits=5, decimal_places=3, null=True, blank=True)
    lai = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    soil_moisture = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    lst = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text='Land Surface Temp °C')

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.farm} on {self.date}"


class StressAssessment(models.Model):
    farm = models.ForeignKey('farms.Farm', on_delete=models.CASCADE, related_name='stress_assessments')
    observation = models.OneToOneField(VegetationObservation, on_delete=models.CASCADE)
    vegetation_stress = models.DecimalField(max_digits=4, decimal_places=1)
    heat_stress = models.DecimalField(max_digits=4, decimal_places=1)
    water_stress = models.DecimalField(max_digits=4, decimal_places=1)
    climate_stress = models.DecimalField(max_digits=4, decimal_places=1)
    resilience_score = models.DecimalField(max_digits=4, decimal_places=1)

    def __str__(self):
        return f"Stress({self.farm})"


class ClimateProjection(models.Model):
    class Scenario(models.TextChoices):
        SSP245 = 'ssp245', 'SSP2-4.5'
        SSP370 = 'ssp370', 'SSP3-7.0'
        SSP585 = 'ssp585', 'SSP5-8.5'

    class Decade(models.IntegerChoices):
        D2030 = 2030, '2030'
        D2035 = 2035, '2035'
        D2040 = 2040, '2040'

    farm = models.ForeignKey('farms.Farm', on_delete=models.CASCADE, related_name='climate_projections', null=True, blank=True)
    district = models.CharField(max_length=100, blank=True)
    scenario = models.CharField(max_length=10, choices=Scenario.choices)
    decade = models.IntegerField(choices=Decade.choices)
    rainfall_change_pct = models.DecimalField(max_digits=5, decimal_places=2)
    heat_stress_index = models.DecimalField(max_digits=4, decimal_places=1)
    dry_days_change = models.DecimalField(max_digits=5, decimal_places=1)
    soil_moisture_trend = models.DecimalField(max_digits=5, decimal_places=2)
    water_stress_trend = models.DecimalField(max_digits=4, decimal_places=1)

    class Meta:
        unique_together = ('farm', 'scenario', 'decade')

    def __str__(self):
        return f"{self.farm or self.district} — {self.scenario} {self.decade}"
