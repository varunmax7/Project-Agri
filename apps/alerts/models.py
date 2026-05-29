from django.db import models

class Alert(models.Model):
    class Category(models.TextChoices):
        WEATHER = 'weather', 'Weather'
        CROP = 'crop', 'Crop'
        ADVISORY = 'advisory', 'Advisory'
        STRATEGIC = 'strategic', 'Strategic'

    class Severity(models.TextChoices):
        LOW = 'low', 'Low'
        MEDIUM = 'medium', 'Medium'
        HIGH = 'high', 'High'

    farm = models.ForeignKey('farms.Farm', on_delete=models.CASCADE, related_name='alerts', null=True, blank=True)
    district = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=15, choices=Category.choices)
    severity = models.CharField(max_length=10, choices=Severity.choices)
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateTimeField(null=True, blank=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.severity.upper()}] {self.title}"
