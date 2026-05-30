from django.db import models

class Report(models.Model):
    class Type(models.TextChoices):
        VILLAGE = 'village', 'Village Climate Report'
        FARM = 'farm', 'Farm Climate Report'
        RISK = 'risk', 'Risk Indicator Report'

    farm = models.ForeignKey('farms.Farm', on_delete=models.CASCADE, related_name='reports')
    type = models.CharField(max_length=50, choices=Type.choices)
    period = models.CharField(max_length=50)
    generated_file = models.FileField(upload_to='reports/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.type} for {self.farm.name} - {self.period}"
