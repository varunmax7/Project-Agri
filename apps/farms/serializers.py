from rest_framework import serializers
from django.contrib.gis.geos import Point
from .models import Farm
from apps.cropdata.models import Crop

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

    class Meta:
        model = Farm
        fields = [
            'id', 'name', 'village', 'district', 'state', 
            'latitude', 'longitude', 'location_coordinates', 
            'area_acres', 'soil_type', 'irrigation_source', 'elevation', 
            'primary_crop_ids'
        ]

    def get_location_coordinates(self, obj):
        if obj.location:
            # point.x is longitude, point.y is latitude
            return {"latitude": obj.location.y, "longitude": obj.location.x}
        return None

    def create(self, validated_data):
        lat = validated_data.pop('latitude')
        lng = validated_data.pop('longitude')
        # Create Point object (longitude, latitude)
        validated_data['location'] = Point(lng, lat, srid=4326)
        
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
            instance.location = Point(lng, lat, srid=4326)
        
        primary_crops = validated_data.pop('primary_crops', None)
        if primary_crops is not None:
            instance.primary_crops.set(primary_crops)
            
        return super().update(instance, validated_data)
