from django.contrib import admin

from .models import Farm, Field, ActivityLog

@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'village', 'district', 'state', 'area_acres', 'soil_type')
    list_filter = ('state', 'district', 'soil_type', 'irrigation_source')
    search_fields = ('name', 'village', 'district', 'user__email')

@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'farm', 'area', 'current_crop')

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('farm', 'activity', 'date')
    list_filter = ('date',)
