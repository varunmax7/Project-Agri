from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
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
class CropSuitabilityViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        farm_id = request.query_params.get('farm')
        if not farm_id:
            return Response([])
            
        year_str = request.query_params.get('year', '2030')
        year = int(year_str) if year_str.isdigit() else 2030
        
        # Snap year to available dataset years
        if year < 2030: year = 2030
        elif 2031 <= year <= 2034: year = 2035
        elif 2036 <= year <= 2039: year = 2040
        elif year > 2040: year = 2040
            
        from apps.farms.models import Farm
        from apps.cropdata.models import CropSuitability
        
        farm = Farm.objects.filter(id=farm_id, user=request.user).first()
        if not farm:
            return Response([])
            
        suit_qs = CropSuitability.objects.filter(district__iexact=farm.district)
        
        def suit_to_pct(suit_str):
            s = str(suit_str)
            if 'Highly' in s: return 90
            elif 'Suitable' in s: return 75
            elif 'Moderate' in s: return 60
            elif 'Marginal' in s: return 40
            else: return 20

        from apps.cropdata.models import Crop, CropCalendar, BestPractice

        results = []
        for s in suit_qs:
            cur_pct = suit_to_pct(s.suitability_current)
            proj_pct = suit_to_pct(s.suitability_projected)
            
            # Interpolate
            if year <= 2024: pct = cur_pct
            elif year >= 2040: pct = proj_pct
            else:
                ratio = (year - 2024) / (2040 - 2024)
                pct = round(cur_pct + ratio * (proj_pct - cur_pct))
                
            # Dynamic Risk based on pct
            if pct < 50: risk = 'high'
            elif pct < 70: risk = 'medium'
            else: risk = 'low'
            
            # Fetch real Crop data if it exists in the database
            c = Crop.objects.filter(name__iexact=s.crop).first()
            
            crop_detail = {
                'name': s.crop,
                'icon': '🌱',
                'water_requirement_mm': 500,
                'temp_min': 20,
                'temp_max': 30,
                'calendars': [],
                'best_practices': []
            }
            
            if c:
                if c.icon: crop_detail['icon'] = c.icon
                if c.water_requirement_mm: crop_detail['water_requirement_mm'] = c.water_requirement_mm
                if c.temp_min: crop_detail['temp_min'] = c.temp_min
                if c.temp_max: crop_detail['temp_max'] = c.temp_max
                
                # Calendars
                for cal in c.calendars.all():
                    crop_detail['calendars'].append({
                        'id': cal.id,
                        'agro_zone': cal.agro_zone,
                        'sowing_start': cal.sowing_start.strftime('%b %d'),
                        'sowing_end': cal.sowing_end.strftime('%b %d'),
                        'vegetative': cal.vegetative,
                        'flowering': cal.flowering,
                        'harvest': cal.harvest
                    })
                    
                # Practices
                for bp in c.best_practices.all():
                    crop_detail['best_practices'].append({
                        'id': bp.id,
                        'stage': bp.stage,
                        'text': bp.text
                    })
            
            results.append({
                'id': s.id,
                'season': 'Kharif',
                'year': year,
                'suitability_pct': pct,
                'risk_level': risk,
                'expected_yield_min': 15.0,  # Could be derived from CSV yields later
                'expected_yield_max': 25.0,
                'recommendation_label': s.recommendation or 'Recommended based on real data.',
                'reasons': [
                    f"Current Suitability: {s.suitability_current}",
                    f"Projected Suitability: {s.suitability_projected}",
                    f"Class Change: {s.change_class}"
                ],
                'crop_detail': crop_detail
            })
            
        # Sort by pct
        results.sort(key=lambda x: x['suitability_pct'], reverse=True)
        return Response(results)


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
