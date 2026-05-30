from django.contrib import admin

from .models import LocationClimateIndex, ClimateRiskZone, VegetationObservation, StressAssessment, ClimateProjection

@admin.register(LocationClimateIndex)
class LocationClimateIndexAdmin(admin.ModelAdmin):
    list_display = ('farm', 'district', 'season', 'year', 'climate_risk_level', 'rainfall_outlook_pct')
    list_filter = ('season', 'year', 'climate_risk_level')

@admin.register(ClimateRiskZone)
class ClimateRiskZoneAdmin(admin.ModelAdmin):
    list_display = ('district', 'state', 'risk_level', 'season', 'layer_type')
    list_filter = ('risk_level', 'season', 'state')

@admin.register(VegetationObservation)
class VegetationObservationAdmin(admin.ModelAdmin):
    list_display = ('farm', 'date', 'ndvi', 'soil_moisture', 'lst')
    list_filter = ('date',)

@admin.register(StressAssessment)
class StressAssessmentAdmin(admin.ModelAdmin):
    list_display = ('farm', 'vegetation_stress', 'heat_stress', 'water_stress', 'resilience_score')

@admin.register(ClimateProjection)
class ClimateProjectionAdmin(admin.ModelAdmin):
    list_display = ('farm', 'district', 'scenario', 'decade', 'rainfall_change_pct', 'heat_stress_index')
    list_filter = ('scenario', 'decade')
