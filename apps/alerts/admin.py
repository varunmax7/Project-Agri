from django.contrib import admin
from .models import Alert

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'severity', 'farm', 'district', 'is_read', 'created_at')
    list_filter = ('category', 'severity', 'is_read', 'created_at')
    search_fields = ('title', 'message')
    actions = ['mark_as_read']

    @admin.action(description='Mark selected as read')
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
