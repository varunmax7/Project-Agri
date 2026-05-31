from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

from .models import Farm
from .serializers import FarmSerializer
from apps.climate.models import LocationClimateIndex, VegetationObservation, StressAssessment, ClimateProjection, ClimateRiskZone
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
        
        scenario = request.query_params.get('scenario', 'ssp245')
        year_str = request.query_params.get('year', '2030')
        year = int(year_str) if year_str.isdigit() else 2030
        
        # Snap year to available dataset years
        if year < 2030: year = 2030
        elif 2031 <= year <= 2034: year = 2035
        elif 2036 <= year <= 2039: year = 2040
        elif year > 2040: year = 2040
        
        # --- Climate Indices & Future Outlook from GeoJSON properties ---
        climate_zone = ClimateRiskZone.objects.filter(
            district__iexact=farm.district, 
            scenario=scenario, 
            year=year
        ).first()
        
        climate_indices = None
        props = {}
        if climate_zone and isinstance(climate_zone.geometry, dict):
            props = climate_zone.geometry.get('properties', {})
            climate_indices = {
                'rainfall_outlook_pct': round(float(props.get('rainfall_change') or 0) + 100.0, 1),
                'water_stress_score': round(float(props.get('drought_hazard_score') or 0), 2),
                'heat_stress_score': round(float(props.get('temperature_change') or 0) * 20.0, 2),
                'agri_resilience_score': round(100.0 - float(props.get('ag_stress_score') or 0), 1),
                'climate_stress_index': round(float(props.get('overall_risk_score') or 0), 2),
                'rainfall_confidence': float(props.get('climate_confidence_score') or 80),
                'water_stress_confidence': float(props.get('climate_confidence_score') or 80),
                'heat_stress_confidence': float(props.get('climate_confidence_score') or 80),
                'agri_resilience_confidence': float(props.get('climate_confidence_score') or 80),
                'csi_confidence': float(props.get('climate_confidence_score') or 80),
            }
            
        # --- Recommended Crops & Future Outlook ---
        from apps.cropdata.models import CropSuitability
        
        search_district = farm.district
        if search_district and search_district.lower() == 'nagarkarnool':
            search_district = 'Nagarkurnool'
            
        suit_qs = CropSuitability.objects.filter(district__iexact=search_district)
        
        def suit_to_pct(suit_str):
            s = str(suit_str)
            if 'Highly' in s: return 90
            elif 'Suitable' in s: return 75
            elif 'Moderate' in s: return 60
            elif 'Marginal' in s: return 40
            else: return 20

        recommended_crops_list = []
        future_outlook = {
            'scenario': scenario,
            'suitability_trends': [],
            'climate_projections': []
        }
        
        for s in suit_qs[:6]:
            curr_pct = suit_to_pct(s.suitability_current)
            proj_pct = suit_to_pct(s.suitability_projected)
            
            # Interpolate for years 2030, 2035, 2040
            pct_2030 = int(curr_pct + (proj_pct - curr_pct) * 0.33)
            pct_2035 = int(curr_pct + (proj_pct - curr_pct) * 0.66)
            pct_2040 = proj_pct
            
            # Select the pct for the requested year
            target_pct = pct_2030
            if year == 2035: target_pct = pct_2035
            elif year == 2040: target_pct = pct_2040
            
            risk = (s.risk_level or 'low').lower()
            if 'high risk' in risk: risk = 'high'
            elif 'moderate risk' in risk: risk = 'moderate'
            else: risk = 'low'
            
            recommended_crops_list.append({
                'id': s.id,
                'crop_details': {
                    'name': s.crop,
                    'icon': '🌱'
                },
                'suitability_pct': target_pct,
                'risk_level': risk
            })
            
            if len(future_outlook['suitability_trends']) < 9: # top 3 crops * 3 decades
                for dec, d_pct in [(2030, pct_2030), (2035, pct_2035), (2040, pct_2040)]:
                    future_outlook['suitability_trends'].append({
                        'id': f"{s.id}_{dec}",
                        'crop_details': {'name': s.crop},
                        'crop_name': s.crop,
                        'year': dec,
                        'suitability_pct': d_pct
                    })
                    
        # Populate climate_projections across the 3 decades for the selected scenario
        actual_scenario = 'ssp245' if scenario == 'ssp370' else scenario
        multiplier = 1.2 if scenario == 'ssp370' else 1.0

        projections = ClimateRiskZone.objects.filter(
            district__iexact=farm.district,
            scenario=actual_scenario
        ).order_by('year')
        
        for p in projections:
            if not isinstance(p.geometry, dict): continue
            pr = p.geometry.get('properties', {})
            t_change = float(pr.get('temperature_change') or 0) * multiplier
            r_change = float(pr.get('rainfall_change') or 0) * multiplier
            d_score = float(pr.get('drought_hazard_score') or 0) * multiplier
            
            heat_stress = t_change * 30
            future_outlook['climate_projections'].append({
                'id': f"proj_{p.year}",
                'decade': p.year,
                'rainfall_change_pct': round(r_change, 1),
                'heat_stress_index': round(heat_stress, 1),
                'dry_days_change': int(d_score / 10),
                'soil_moisture_trend': -int(d_score / 5),
                'water_stress_trend': int(d_score / 4)
            })

        alerts = Alert.objects.filter(farm=farm, is_read=False).order_by('-created_at')[:5]
        unread_count = Alert.objects.filter(farm=farm, is_read=False).count()

        ctx = {'request': request}

        # --- Dynamic Farm-Level Metrics (Derived from District Climate Data) ---
        d_risk = float(props.get('drought_hazard_score') or 0)
        t_change = float(props.get('temperature_change') or 0)
        r_change = float(props.get('rainfall_change') or 0)
        o_risk = float(props.get('overall_risk_score') or 0)
        o_class = props.get('overall_risk_class') or 'Low'

        # --- Dynamic Charts Data based on climate risk ---
        water_req = (600 if recommended_crops_list and 'Cotton' in recommended_crops_list[0]['crop_details']['name'] else 400) + (t_change * 30)
        water_balance = [
            {'month': 'Jun', 'availability_mm': max(0, 120 + (r_change * 0.2)), 'requirement_mm': water_req * 0.1},
            {'month': 'Jul', 'availability_mm': max(0, 280 + (r_change * 0.4)), 'requirement_mm': water_req * 0.3},
            {'month': 'Aug', 'availability_mm': max(0, 250 + (r_change * 0.3)), 'requirement_mm': water_req * 0.4},
            {'month': 'Sep', 'availability_mm': max(0, 150 + (r_change * 0.1)), 'requirement_mm': water_req * 0.2},
            {'month': 'Oct', 'availability_mm': 50, 'requirement_mm': 0},
        ]
        
        yield_risks = [{'risk_label': 'low', 'risk_pct': 100 - int(float(props.get('overall_risk_score') or 0))}]

        latest_vegetation = {
            'ndvi': round(max(0.2, 0.85 - (o_risk / 200)), 2),
            'soil_moisture': max(10, 45 - int(d_risk / 2)),
            'lst': round(32.0 + t_change, 1)
        }
        
        def get_stress_label(score):
            if score > 60: return 'High'
            if score > 30: return 'Moderate'
            return 'Low'
            
        stress_assessment = {
            'vegetation_stress': get_stress_label(o_risk),
            'water_stress': get_stress_label(d_risk),
            'heat_stress': get_stress_label(t_change * 30),
            'climate_stress': o_class.capitalize(),
            'drought_score': round(d_risk, 1),
            'overall_score': round(o_risk, 1)
        }
        
        irrigation_advisory = {
            'next_irrigation_date': 'Tomorrow',
            'recommended_amount_mm': 25 + int(d_risk / 4),
            'recommended_cycles': max(0, 10 - int(d_risk / 15)),
            'window': 'Jul 10 - Jul 15',
            'next_activity': 'Start critical vegetative stage irrigation',
            'note': 'Drip/Sprinkler' if d_risk > 50 else 'Flood Irrigation',
            'advisory_text': 'Adjusted for projected drought risk levels in your district.'
        }

        return Response({
            'farm': FarmSerializer(farm, context=ctx).data,
            'season': 'Kharif',
            'year': year,
            'climate_indices': climate_indices,
            'recommended_crops': recommended_crops_list,
            'water_balance': water_balance,
            'yield_risks': yield_risks,
            'future_outlook': future_outlook,
            'latest_vegetation': latest_vegetation,
            'stress_assessment': stress_assessment,
            'irrigation_advisory': irrigation_advisory,
            'alerts': AlertSerializer(alerts, many=True, context=ctx).data,
            'unread_alert_count': unread_count,
        })
