from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from .models import (
    LocationClimateIndex, ClimateRiskZone,
    VegetationObservation, StressAssessment, ClimateProjection,
)
from .serializers import (
    LocationClimateIndexSerializer, ClimateRiskZoneSerializer,
    ClimateRiskZoneGeoJSONSerializer, VegetationObservationSerializer,
    StressAssessmentSerializer, ClimateProjectionSerializer,
)


@extend_schema_view(
    list=extend_schema(
        summary='Climate indices for the authenticated user\'s farms',
        tags=['climate'],
        parameters=[
            OpenApiParameter('season', str, description='Filter by season (e.g. Kharif)'),
            OpenApiParameter('year', int, description='Filter by year'),
        ],
    ),
    retrieve=extend_schema(summary='Single climate index record', tags=['climate']),
)
class LocationClimateIndexViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = LocationClimateIndexSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = LocationClimateIndex.objects.all()
        farm_id = self.request.query_params.get('farm')
        season = self.request.query_params.get('season')
        year = self.request.query_params.get('year')
        if farm_id:
            qs = qs.filter(farm_id=farm_id)
        if season:
            qs = qs.filter(season__iexact=season)
        if year:
            qs = qs.filter(year=year)
        return qs


@extend_schema_view(
    list=extend_schema(
        summary='Climate risk zones (JSON)',
        tags=['climate'],
        parameters=[
            OpenApiParameter('season', str, description='Filter by season'),
            OpenApiParameter('layer_type', str, description='Filter by layer type'),
        ],
    ),
    geojson=extend_schema(
        summary='Climate risk zones as GeoJSON FeatureCollection',
        tags=['climate'],
    ),
)
class ClimateRiskZoneViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = ClimateRiskZoneSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = ClimateRiskZone.objects.all()
        season = self.request.query_params.get('season')
        layer_type = self.request.query_params.get('layer_type')
        if season:
            qs = qs.filter(season__iexact=season)
        if layer_type:
            qs = qs.filter(layer_type=layer_type)
        return qs

    @action(detail=False, methods=['get'], url_path='geojson')
    def geojson(self, request):
        queryset = self.get_queryset()
        serializer = ClimateRiskZoneGeoJSONSerializer(queryset)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(
        summary='Vegetation observations for user\'s farms',
        tags=['climate'],
        parameters=[OpenApiParameter('farm', int, description='Filter by farm ID')],
    ),
)
class VegetationObservationViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = VegetationObservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = VegetationObservation.objects.all()
        farm_id = self.request.query_params.get('farm')
        if farm_id:
            qs = qs.filter(farm_id=farm_id)
        return qs


@extend_schema_view(
    list=extend_schema(summary='Stress assessments for user\'s farms', tags=['climate']),
)
class StressAssessmentViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = StressAssessmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = StressAssessment.objects.all()
        farm_id = self.request.query_params.get('farm')
        if farm_id:
            qs = qs.filter(farm_id=farm_id)
        return qs


@extend_schema_view(
    list=extend_schema(
        summary='Future climate projections for user\'s farms',
        tags=['climate'],
        parameters=[
            OpenApiParameter('farm', int, description='Filter by farm ID'),
            OpenApiParameter('scenario', str, description='SSP scenario (ssp245/ssp370/ssp585)'),
        ],
    ),
)
class ClimateProjectionViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = ClimateProjectionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = ClimateProjection.objects.all()
        farm_id = self.request.query_params.get('farm')
        scenario = self.request.query_params.get('scenario')
        if farm_id:
            qs = qs.filter(farm_id=farm_id)
        if scenario:
            qs = qs.filter(scenario=scenario)
        return qs.order_by('decade')
