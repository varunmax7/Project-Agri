from rest_framework import serializers
from .models import Crop, CropCalendar, BestPractice


class BestPracticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BestPractice
        fields = ['id', 'stage', 'text']


class CropCalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = CropCalendar
        fields = ['id', 'agro_zone', 'sowing_start', 'sowing_end', 'vegetative', 'flowering', 'harvest']


class CropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crop
        fields = [
            'id', 'name', 'icon', 'category', 'season',
            'water_requirement_mm', 'temp_min', 'temp_max', 'optimal_soil_moisture',
        ]


class CropDetailSerializer(CropSerializer):
    calendars = CropCalendarSerializer(many=True, read_only=True)
    best_practices = BestPracticeSerializer(many=True, read_only=True)

    class Meta(CropSerializer.Meta):
        fields = CropSerializer.Meta.fields + ['calendars', 'best_practices']
