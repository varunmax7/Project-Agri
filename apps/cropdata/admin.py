from django.contrib import admin
from .models import Crop, CropCalendar, BestPractice

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'season', 'water_requirement_mm', 'temp_min', 'temp_max')
    list_filter = ('category', 'season')
    search_fields = ('name',)

@admin.register(CropCalendar)
class CropCalendarAdmin(admin.ModelAdmin):
    list_display = ('crop', 'agro_zone', 'sowing_start', 'sowing_end')

@admin.register(BestPractice)
class BestPracticeAdmin(admin.ModelAdmin):
    list_display = ('crop', 'stage')
