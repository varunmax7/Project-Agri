from rest_framework import serializers
from .models import Alert


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = [
            'id', 'farm', 'district', 'category', 'severity',
            'title', 'message', 'created_at', 'valid_until', 'is_read',
        ]
        read_only_fields = ['created_at']
