from django.contrib import admin
from .models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('farm', 'type', 'period', 'created_at')
    list_filter = ('type', 'created_at')
    search_fields = ('farm__name', 'period')
