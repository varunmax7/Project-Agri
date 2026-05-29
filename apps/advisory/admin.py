from django.contrib import admin
from .models import CropSuitability, CropSuitabilityTrend, WaterBalance, IrrigationAdvisory, YieldRisk

@admin.register(CropSuitability)
class CropSuitabilityAdmin(admin.ModelAdmin):
    list_display = ('crop', 'farm', 'season', 'year', 'suitability_pct', 'recommendation_label', 'risk_level')
    list_filter = ('season', 'year', 'risk_level')

@admin.register(CropSuitabilityTrend)
class CropSuitabilityTrendAdmin(admin.ModelAdmin):
    list_display = ('crop', 'farm', 'scenario', 'year', 'suitability_pct')
    list_filter = ('scenario', 'year')

@admin.register(WaterBalance)
class WaterBalanceAdmin(admin.ModelAdmin):
    list_display = ('farm', 'season', 'month', 'requirement_mm', 'availability_mm')
    list_filter = ('season',)

@admin.register(IrrigationAdvisory)
class IrrigationAdvisoryAdmin(admin.ModelAdmin):
    list_display = ('farm', 'season', 'recommended_cycles', 'next_activity', 'window')

@admin.register(YieldRisk)
class YieldRiskAdmin(admin.ModelAdmin):
    list_display = ('farm', 'crop', 'season', 'risk_pct', 'risk_label')
    list_filter = ('risk_label', 'season')
