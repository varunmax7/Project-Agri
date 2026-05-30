from rest_framework import serializers
from apps.cropdata.serializers import CropDetailSerializer, CropSerializer
from .models import CropSuitability, CropSuitabilityTrend, WaterBalance, IrrigationAdvisory, YieldRisk


class CropSuitabilitySerializer(serializers.ModelSerializer):
    crop_detail = CropDetailSerializer(source='crop', read_only=True)

    class Meta:
        model = CropSuitability
        fields = [
            'id', 'crop', 'crop_detail', 'farm', 'season', 'year',
            'suitability_pct', 'recommendation_label',
            'expected_yield_min', 'expected_yield_max',
            'risk_level', 'reasons',
        ]


class CropSuitabilityTrendSerializer(serializers.ModelSerializer):
    crop_name = serializers.CharField(source='crop.name', read_only=True)

    class Meta:
        model = CropSuitabilityTrend
        fields = ['id', 'crop', 'crop_name', 'farm', 'scenario', 'year', 'suitability_pct']


class WaterBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterBalance
        fields = ['id', 'farm', 'season', 'month', 'requirement_mm', 'availability_mm']


class IrrigationAdvisorySerializer(serializers.ModelSerializer):
    class Meta:
        model = IrrigationAdvisory
        fields = [
            'id', 'farm', 'season', 'recommended_cycles',
            'note', 'next_activity', 'window', 'created_at',
        ]


class YieldRiskSerializer(serializers.ModelSerializer):
    crop_detail = CropSerializer(source='crop', read_only=True)

    class Meta:
        model = YieldRisk
        fields = [
            'id', 'farm', 'season', 'crop', 'crop_detail',
            'risk_pct', 'risk_label', 'yield_low_pct', 'yield_high_pct',
        ]
