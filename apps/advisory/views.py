from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from .models import CropSuitability, CropSuitabilityTrend, WaterBalance, IrrigationAdvisory, YieldRisk
from .serializers import (
    CropSuitabilitySerializer, CropSuitabilityTrendSerializer,
    WaterBalanceSerializer, IrrigationAdvisorySerializer, YieldRiskSerializer,
)


@extend_schema_view(
    list=extend_schema(
        summary='Crop suitability records for user\'s farms',
        tags=['advisory'],
        parameters=[
            OpenApiParameter('farm', int, description='Filter by farm ID'),
            OpenApiParameter('season', str, description='Filter by season'),
            OpenApiParameter('year', int, description='Filter by year'),
        ],
    ),
    retrieve=extend_schema(summary='Single crop suitability record', tags=['advisory']),
)
class CropSuitabilityViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = CropSuitabilitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = CropSuitability.objects.filter(farm__user=self.request.user).select_related('crop')
        farm_id = self.request.query_params.get('farm')
        season = self.request.query_params.get('season')
        year = self.request.query_params.get('year')
        if farm_id:
            qs = qs.filter(farm_id=farm_id)
        if season:
            qs = qs.filter(season__iexact=season)
        if year:
            qs = qs.filter(year=year)
        return qs.order_by('-suitability_pct')


@extend_schema_view(
    list=extend_schema(
        summary='Future crop suitability trend data',
        tags=['advisory'],
        parameters=[
            OpenApiParameter('farm', int, description='Filter by farm ID'),
            OpenApiParameter('scenario', str, description='SSP scenario'),
            OpenApiParameter('crop', int, description='Filter by crop ID'),
        ],
    ),
)
class CropSuitabilityTrendViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = CropSuitabilityTrendSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = CropSuitabilityTrend.objects.filter(farm__user=self.request.user).select_related('crop')
        farm_id = self.request.query_params.get('farm')
        scenario = self.request.query_params.get('scenario')
        crop_id = self.request.query_params.get('crop')
        if farm_id:
            qs = qs.filter(farm_id=farm_id)
        if scenario:
            qs = qs.filter(scenario=scenario)
        if crop_id:
            qs = qs.filter(crop_id=crop_id)
        return qs.order_by('year')


@extend_schema_view(
    list=extend_schema(
        summary='Monthly water balance for user\'s farms',
        tags=['advisory'],
        parameters=[
            OpenApiParameter('farm', int, description='Filter by farm ID'),
            OpenApiParameter('season', str, description='Filter by season'),
        ],
    ),
)
class WaterBalanceViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = WaterBalanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = WaterBalance.objects.filter(farm__user=self.request.user)
        farm_id = self.request.query_params.get('farm')
        season = self.request.query_params.get('season')
        if farm_id:
            qs = qs.filter(farm_id=farm_id)
        if season:
            qs = qs.filter(season__iexact=season)
        return qs


@extend_schema_view(
    list=extend_schema(
        summary='Irrigation advisories for user\'s farms',
        tags=['advisory'],
        parameters=[OpenApiParameter('farm', int, description='Filter by farm ID')],
    ),
)
class IrrigationAdvisoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = IrrigationAdvisorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = IrrigationAdvisory.objects.filter(farm__user=self.request.user)
        farm_id = self.request.query_params.get('farm')
        if farm_id:
            qs = qs.filter(farm_id=farm_id)
        return qs


@extend_schema_view(
    list=extend_schema(
        summary='Yield risk records for user\'s farms',
        tags=['advisory'],
        parameters=[
            OpenApiParameter('farm', int, description='Filter by farm ID'),
            OpenApiParameter('season', str, description='Filter by season'),
        ],
    ),
)
class YieldRiskViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = YieldRiskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = YieldRisk.objects.filter(farm__user=self.request.user).select_related('crop')
        farm_id = self.request.query_params.get('farm')
        season = self.request.query_params.get('season')
        if farm_id:
            qs = qs.filter(farm_id=farm_id)
        if season:
            qs = qs.filter(season__iexact=season)
        return qs
