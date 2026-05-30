from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

from .models import Farm
from .serializers import FarmSerializer
from apps.climate.models import LocationClimateIndex, VegetationObservation, StressAssessment, ClimateProjection
from apps.advisory.models import CropSuitability, CropSuitabilityTrend, WaterBalance, IrrigationAdvisory, YieldRisk
from apps.alerts.models import Alert
from apps.climate.serializers import (
    LocationClimateIndexSerializer, VegetationObservationSerializer,
    StressAssessmentSerializer, ClimateProjectionSerializer,
)
from apps.advisory.serializers import (
    CropSuitabilitySerializer, CropSuitabilityTrendSerializer,
    WaterBalanceSerializer, IrrigationAdvisorySerializer, YieldRiskSerializer,
)
from apps.alerts.serializers import AlertSerializer


@extend_schema_view(
    list=extend_schema(summary='List user\'s farms', tags=['farms']),
    retrieve=extend_schema(summary='Farm detail', tags=['farms']),
    create=extend_schema(summary='Create a farm', tags=['farms']),
    update=extend_schema(summary='Update a farm', tags=['farms']),
    partial_update=extend_schema(summary='Partially update a farm', tags=['farms']),
    destroy=extend_schema(summary='Delete a farm', tags=['farms']),
)
class FarmViewSet(viewsets.ModelViewSet):
    serializer_class = FarmSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Farm.objects.filter(user=self.request.user).prefetch_related(
            'primary_crops', 'fields', 'activity_logs'
        )

    @extend_schema(
        summary='Aggregated dashboard data for a single farm (Screen 1)',
        tags=['dashboard'],
        parameters=[
            OpenApiParameter('season', str, description='Season filter (e.g. Kharif). Defaults to latest.'),
            OpenApiParameter('year', int, description='Year filter. Defaults to latest.'),
            OpenApiParameter('scenario', str, description='SSP scenario for projections. Default: ssp245.'),
        ],
        responses={200: None},
    )
    @action(detail=True, methods=['get'], url_path='dashboard')
    def dashboard(self, request, pk=None):
        farm = self.get_object()
        season = request.query_params.get('season')
        year = request.query_params.get('year')
        scenario = request.query_params.get('scenario', 'ssp245')

        # --- Climate indices ---
        ci_qs = LocationClimateIndex.objects.filter(farm=farm)
        if season:
            ci_qs = ci_qs.filter(season__iexact=season)
        if year:
            ci_qs = ci_qs.filter(year=year)
        climate_index = ci_qs.order_by('-year').first()

        # --- Crop suitabilities (top 6 by suitability) ---
        suit_qs = CropSuitability.objects.filter(farm=farm).select_related('crop')
        if season:
            suit_qs = suit_qs.filter(season__iexact=season)
        if year:
            suit_qs = suit_qs.filter(year=year)
        if climate_index and not year:
            suit_qs = suit_qs.filter(year=climate_index.year)
        recommended_crops = suit_qs.order_by('-suitability_pct')[:6]

        # --- Water balance ---
        wb_qs = WaterBalance.objects.filter(farm=farm)
        if season:
            wb_qs = wb_qs.filter(season__iexact=season)
        if climate_index and not season:
            wb_qs = wb_qs.filter(season__iexact=climate_index.season)

        # --- Yield risks ---
        yr_qs = YieldRisk.objects.filter(farm=farm).select_related('crop')
        if season:
            yr_qs = yr_qs.filter(season__iexact=season)
        if climate_index and not season:
            yr_qs = yr_qs.filter(season__iexact=climate_index.season)

        # --- Future outlook: suitability trends across decades ---
        trend_qs = (
            CropSuitabilityTrend.objects
            .filter(farm=farm, scenario=scenario)
            .select_related('crop')
            .order_by('year')
        )

        # --- Climate projections ---
        proj_qs = (
            ClimateProjection.objects
            .filter(farm=farm, scenario=scenario)
            .order_by('decade')
        )

        # --- Latest vegetation observation ---
        veg_obs = (
            VegetationObservation.objects
            .filter(farm=farm)
            .order_by('-date')
            .first()
        )
        stress = None
        if veg_obs:
            stress = StressAssessment.objects.filter(observation=veg_obs).first()

        # --- Latest irrigation advisory ---
        irrigation = (
            IrrigationAdvisory.objects
            .filter(farm=farm)
            .order_by('-created_at')
            .first()
        )

        # --- Top 5 unread alerts ---
        alerts = Alert.objects.filter(farm=farm, is_read=False).order_by('-created_at')[:5]
        unread_count = Alert.objects.filter(farm=farm, is_read=False).count()

        ctx = {'request': request}

        return Response({
            'farm': FarmSerializer(farm, context=ctx).data,
            'season': climate_index.season if climate_index else season,
            'year': climate_index.year if climate_index else year,
            'climate_indices': LocationClimateIndexSerializer(climate_index, context=ctx).data if climate_index else None,
            'recommended_crops': CropSuitabilitySerializer(recommended_crops, many=True, context=ctx).data,
            'water_balance': WaterBalanceSerializer(wb_qs, many=True, context=ctx).data,
            'yield_risks': YieldRiskSerializer(yr_qs, many=True, context=ctx).data,
            'future_outlook': {
                'scenario': scenario,
                'suitability_trends': CropSuitabilityTrendSerializer(trend_qs, many=True, context=ctx).data,
                'climate_projections': ClimateProjectionSerializer(proj_qs, many=True, context=ctx).data,
            },
            'latest_vegetation': VegetationObservationSerializer(veg_obs, context=ctx).data if veg_obs else None,
            'stress_assessment': StressAssessmentSerializer(stress, context=ctx).data if stress else None,
            'irrigation_advisory': IrrigationAdvisorySerializer(irrigation, context=ctx).data if irrigation else None,
            'alerts': AlertSerializer(alerts, many=True, context=ctx).data,
            'unread_alert_count': unread_count,
        })
