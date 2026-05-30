from rest_framework import serializers
from .models import Farm, Field, ActivityLog
from apps.cropdata.models import Crop

class FieldSerializer(serializers.ModelSerializer):
    current_crop_name = serializers.CharField(source='current_crop.name', read_only=True)
    current_crop_icon = serializers.CharField(source='current_crop.icon', read_only=True)

    class Meta:
        model = Field
        fields = ['id', 'name', 'area', 'current_crop', 'current_crop_name', 'current_crop_icon']

class ActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        fields = ['id', 'activity', 'date', 'note', 'created_at']

class FarmSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField(write_only=True)
    longitude = serializers.FloatField(write_only=True)
    
    # Represent location nicely in read
    location_coordinates = serializers.SerializerMethodField(read_only=True)
    primary_crop_ids = serializers.PrimaryKeyRelatedField(
        queryset=Crop.objects.all(), 
        many=True, 
        source='primary_crops',
        required=False
    )
    
    fields = FieldSerializer(many=True, read_only=True)
    activity_logs = ActivityLogSerializer(many=True, read_only=True)

    class Meta:
        model = Farm
        fields = [
            'id', 'name', 'village', 'district', 'state', 
            'latitude', 'longitude', 'location_coordinates', 
            'area_acres', 'soil_type', 'irrigation_source', 'elevation', 
            'primary_crop_ids', 'fields', 'activity_logs'
        ]

    def get_location_coordinates(self, obj):
        if obj.location and isinstance(obj.location, dict) and 'coordinates' in obj.location:
            lng, lat = obj.location['coordinates']
            return {"latitude": lat, "longitude": lng}
        return None

    def create(self, validated_data):
        lat = validated_data.pop('latitude')
        lng = validated_data.pop('longitude')
        validated_data['location'] = {"type": "Point", "coordinates": [lng, lat]}
        
        # User is injected from context in the view
        validated_data['user'] = self.context['request'].user
        
        primary_crops = validated_data.pop('primary_crops', [])
        
        farm = Farm.objects.create(**validated_data)
        if primary_crops:
            farm.primary_crops.set(primary_crops)
            
        return farm

    def update(self, instance, validated_data):
        if 'latitude' in validated_data and 'longitude' in validated_data:
            lat = validated_data.pop('latitude')
            lng = validated_data.pop('longitude')
            instance.location = {"type": "Point", "coordinates": [lng, lat]}
        
        primary_crops = validated_data.pop('primary_crops', None)
        if primary_crops is not None:
            instance.primary_crops.set(primary_crops)
            
        return super().update(instance, validated_data)
