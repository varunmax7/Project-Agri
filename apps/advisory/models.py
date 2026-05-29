from django.db import models

class CropSuitability(models.Model):
    class RiskLevel(models.TextChoices):
        LOW = 'low', 'Low'
        MEDIUM = 'medium', 'Medium'
        HIGH = 'high', 'High'

    crop = models.ForeignKey('cropdata.Crop', on_delete=models.CASCADE, related_name='suitability_records')
    farm = models.ForeignKey('farms.Farm', on_delete=models.CASCADE, related_name='crop_suitabilities')
    season = models.CharField(max_length=20)
    year = models.PositiveIntegerField()
    suitability_pct = models.DecimalField(max_digits=5, decimal_places=2)
    recommendation_label = models.CharField(max_length=50)
    expected_yield_min = models.DecimalField(max_digits=8, decimal_places=2, help_text='q/ha')
    expected_yield_max = models.DecimalField(max_digits=8, decimal_places=2, help_text='q/ha')
    risk_level = models.CharField(max_length=10, choices=RiskLevel.choices)
    reasons = models.JSONField(default=list, help_text='List of reason strings')

    class Meta:
        unique_together = ('crop', 'farm', 'season', 'year')

    def __str__(self):
        return f"{self.crop.name} @ {self.farm.name} — {self.season} {self.year}"


class CropSuitabilityTrend(models.Model):
    crop = models.ForeignKey('cropdata.Crop', on_delete=models.CASCADE, related_name='suitability_trends')
    farm = models.ForeignKey('farms.Farm', on_delete=models.CASCADE, related_name='crop_suitability_trends')
    scenario = models.CharField(max_length=10)
    year = models.PositiveIntegerField()
    suitability_pct = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ('crop', 'farm', 'scenario', 'year')

    def __str__(self):
        return f"{self.crop.name} @ {self.farm.name} — {self.scenario} {self.year}"


class WaterBalance(models.Model):
    farm = models.ForeignKey('farms.Farm', on_delete=models.CASCADE, related_name='water_balances')
    season = models.CharField(max_length=20)
    month = models.PositiveSmallIntegerField()
    requirement_mm = models.DecimalField(max_digits=7, decimal_places=2)
    availability_mm = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        unique_together = ('farm', 'season', 'month')
        ordering = ['month']

    def __str__(self):
        return f"{self.farm.name} — {self.season} month {self.month}"


class IrrigationAdvisory(models.Model):
    farm = models.ForeignKey('farms.Farm', on_delete=models.CASCADE, related_name='irrigation_advisories')
    season = models.CharField(max_length=20)
    recommended_cycles = models.PositiveSmallIntegerField()
    note = models.TextField(blank=True)
    next_activity = models.CharField(max_length=200, blank=True)
    window = models.CharField(max_length=100, blank=True, help_text='e.g. Jun 15 – Jun 22')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.farm.name} — {self.season}"


class YieldRisk(models.Model):
    class RiskLabel(models.TextChoices):
        LOW = 'low', 'Low Risk'
        MEDIUM = 'medium', 'Medium Risk'
        HIGH = 'high', 'High Risk'

    farm = models.ForeignKey('farms.Farm', on_delete=models.CASCADE, related_name='yield_risks')
    season = models.CharField(max_length=20)
    crop = models.ForeignKey('cropdata.Crop', on_delete=models.CASCADE)
    risk_pct = models.DecimalField(max_digits=5, decimal_places=2)
    risk_label = models.CharField(max_length=10, choices=RiskLabel.choices)
    yield_low_pct = models.DecimalField(max_digits=5, decimal_places=2)
    yield_high_pct = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.farm.name} — {self.crop.name} {self.season}"
