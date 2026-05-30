import json
from rest_framework import serializers
from .models import (
    LocationClimateIndex, ClimateRiskZone,
    VegetationObservation, StressAssessment, ClimateProjection,
)


class LocationClimateIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationClimateIndex
        fields = [
            'id', 'farm', 'district', 'season', 'year',
            'rainfall_outlook_pct', 'water_stress_score', 'heat_stress_score',
            'agri_resilience_score', 'climate_stress_index', 'climate_risk_level',
            'rainfall_confidence', 'water_stress_confidence', 'heat_stress_confidence',
            'agri_resilience_confidence', 'csi_confidence',
        ]


class ClimateRiskZoneSerializer(serializers.ModelSerializer):
    geometry = serializers.SerializerMethodField()

    class Meta:
        model = ClimateRiskZone
        fields = ['id', 'district', 'state', 'risk_level', 'season', 'layer_type', 'geometry']

    def get_geometry(self, obj):
        if obj.geometry:
            return obj.geometry
        return None


class ClimateRiskZoneGeoJSONSerializer(serializers.BaseSerializer):
    """Returns a FeatureCollection for direct Leaflet consumption."""

    def to_representation(self, queryset):
        features = []
        for zone in queryset:
            features.append({
                'type': 'Feature',
                'geometry': zone.geometry if zone.geometry else None,
                'properties': {
                    'id': zone.id,
                    'district': zone.district,
                    'state': zone.state,
                    'risk_level': zone.risk_level,
                    'season': zone.season,
                    'layer_type': zone.layer_type,
                },
            })
        return {'type': 'FeatureCollection', 'features': features}


class VegetationObservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VegetationObservation
        fields = ['id', 'farm', 'field', 'date', 'ndvi', 'lai', 'soil_moisture', 'lst']


class StressAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StressAssessment
        fields = [
            'id', 'farm', 'observation',
            'vegetation_stress', 'heat_stress', 'water_stress',
            'climate_stress', 'resilience_score',
        ]


class ClimateProjectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClimateProjection
        fields = [
            'id', 'farm', 'district', 'scenario', 'decade',
            'rainfall_change_pct', 'heat_stress_index',
            'dry_days_change', 'soil_moisture_trend', 'water_stress_trend',
        ]
