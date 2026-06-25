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
        return Farm.objects.all().prefetch_related(
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

from django.shortcuts import render
from django.http import JsonResponse
import json
import time
from datetime import datetime, timedelta

def parcel_inspector_view(request):
    """
    Renders the frontend template with Leaflet map and Chart.js for the Parcel Inspector.
    """
    return render(request, 'farms/parcel_inspector.html', {'active_module': 'parcel_inspector', 'page_title': 'Parcel Inspector'})

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def stac_ndvi_timeseries(request):
    """
    Receives a GeoJSON polygon and returns an NDVI time series. Tries the real
    AWS Earth Search Sentinel-2 STAC pipeline first; if it times out or fails,
    falls back to a seasonal simulated NDVI series so the chart always renders.
    """
    try:
        body = json.loads(request.body)
        polygon_coords = body.get('polygon')

        if not polygon_coords:
            return JsonResponse({'error': 'No polygon coordinates provided.'}, status=400)

        # Ensure it's a closed ring
        if polygon_coords[0] != polygon_coords[-1]:
            polygon_coords.append(polygon_coords[0])

        # 120 days of recent Sentinel-2 history. Long enough to see two clear
        # crop-growth inflections in either season, short enough that the
        # search returns in seconds instead of timing out the whole request.
        end_date = datetime.today().strftime('%Y-%m-%d')
        start_date = (datetime.today() - timedelta(days=120)).strftime('%Y-%m-%d')

        # Run the STAC pipeline as a completely isolated subprocess.
        # This completely bypasses GDAL/osgeo deadlocks in Django's threading model,
        # and prevents the macOS socket DNS resolution bug from hanging the server.
        import os
        import subprocess
        from django.conf import settings

        script_path = os.path.join(settings.BASE_DIR, 'scripts', 'stac_pipeline.py')
        input_data = json.dumps({
            'polygon': polygon_coords,
            'start_date': start_date,
            'end_date': end_date
        })

        live_results = None
        stac_error = None

        try:
            process = subprocess.run(
                ['python3', script_path],
                input=input_data,
                text=True,
                capture_output=True,
                timeout=55,
            )

            if process.returncode != 0:
                print(f"[STAC ERROR] Subprocess failed:\n{process.stderr}")
                stac_error = 'pipeline_failed'
            else:
                live_results = json.loads(process.stdout.strip())

        except subprocess.TimeoutExpired:
            print("[STAC WARN] Subprocess timed out; falling back to simulated NDVI.")
            stac_error = 'timeout'
        except json.JSONDecodeError:
            print(f"[STAC ERROR] Invalid JSON from subprocess.")
            stac_error = 'invalid_json'

        if live_results:
            return JsonResponse({'data': live_results, 'source': 'live'})

        # Fallback: realistic seasonal NDVI model so the chart always renders.
        # Source is flagged so the UI can show the "Simulated Model" badge.
        sim_results = _generate_realistic_ndvi(polygon_coords, start_date, end_date)
        return JsonResponse({
            'data': sim_results,
            'source': 'simulated',
            'fallback_reason': stac_error or 'no_observations',
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)


def _generate_realistic_ndvi(polygon_coords, start_date, end_date):
    """
    Generates a realistic NDVI time series based on the coordinates, season, and typical
    agricultural patterns for the Indian subcontinent. Uses a sinusoidal crop growth model
    with monsoon-driven seasonality and random cloud-gap simulation.
    """
    import random, math
    
    # Derive a seed from the polygon centroid for consistency
    avg_lng = sum(c[0] for c in polygon_coords) / len(polygon_coords)
    avg_lat = sum(c[1] for c in polygon_coords) / len(polygon_coords)
    seed = int((avg_lat * 1000 + avg_lng * 100) % 100000)
    rng = random.Random(seed)
    
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    
    results = []
    current = start
    
    # Simulate ~5-day revisit intervals (Sentinel-2 cadence) with some gaps
    while current <= end:
        day_of_year = current.timetuple().tm_yday
        month = current.month
        
        # Indian agricultural NDVI model:
        # Kharif season (Jun-Oct): NDVI rises, peaks Aug-Sep, falls Oct
        # Rabi season (Nov-Mar): NDVI rises, peaks Jan-Feb, falls Mar
        # Lean period (Apr-May): Low NDVI
        
        # Base NDVI from seasonal sinusoidal model
        # Phase 1: Kharif (peak around day 240 = late Aug)
        kharif_ndvi = 0.35 * math.exp(-((day_of_year - 240) ** 2) / (2 * 45 ** 2))
        
        # Phase 2: Rabi (peak around day 45 = mid Feb)
        rabi_offset = day_of_year if day_of_year < 180 else day_of_year - 365
        rabi_ndvi = 0.30 * math.exp(-((rabi_offset - 45) ** 2) / (2 * 40 ** 2))
        
        # Combine with a base soil/vegetation background
        base_ndvi = 0.15
        ndvi = base_ndvi + kharif_ndvi + rabi_ndvi
        
        # Add latitude-based variation (tropical regions have higher base NDVI)
        lat_factor = 1.0 + max(0, (25 - abs(avg_lat - 20))) * 0.01
        ndvi *= lat_factor
        
        # Add realistic noise
        noise = rng.gauss(0, 0.03)
        ndvi = max(0.05, min(0.92, ndvi + noise))
        
        # Simulate cloud gaps (~20% of observations are cloudy/missing)
        if rng.random() > 0.20:
            results.append({
                'date': current.strftime('%Y-%m-%d'),
                'ndvi': round(ndvi, 4)
            })
        
        # Next observation (5-10 day interval like Sentinel-2)
        current += timedelta(days=rng.randint(5, 10))

    return results


# ---------------------------------------------------------------------------
# Parcel Intelligence: real-time location/weather/climate/soil/terrain bundle.
# All upstream APIs are free and require no key. Each helper isolates its own
# failure so one bad source can't take down the whole response.
# ---------------------------------------------------------------------------

import requests
import concurrent.futures


def _fetch_location(lat, lng):
    try:
        r = requests.get(
            'https://nominatim.openstreetmap.org/reverse',
            params={'lat': lat, 'lon': lng, 'format': 'json', 'zoom': 12, 'addressdetails': 1},
            headers={'User-Agent': 'FloodGuard-Agri-Intelligence/1.0'},
            timeout=8,
        )
        data = r.json()
        addr = data.get('address', {}) or {}
        return {
            'display_name': data.get('display_name'),
            'village': addr.get('village') or addr.get('hamlet') or addr.get('town') or addr.get('suburb'),
            'district': addr.get('state_district') or addr.get('county') or addr.get('district'),
            'state': addr.get('state'),
            'country': addr.get('country'),
            'country_code': addr.get('country_code'),
            'postcode': addr.get('postcode'),
        }
    except Exception as e:
        return {'error': str(e)}


def _fetch_weather(lat, lng):
    # Open-Meteo's EU edge can sit at 10–25 s latency from South Asia under
    # load. A short timeout was masking real responses, so the panel always
    # rendered "unavailable" even though the API was about to answer.
    try:
        r = requests.get(
            'https://api.open-meteo.com/v1/forecast',
            params={
                'latitude': lat,
                'longitude': lng,
                'current': 'temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,weather_code,cloud_cover,surface_pressure,wind_speed_10m,wind_direction_10m,wind_gusts_10m',
                'daily': 'weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,wind_speed_10m_max,sunrise,sunset,uv_index_max',
                'forecast_days': 7,
                'timezone': 'auto',
            },
            timeout=30,
        )
        return r.json()
    except Exception as e:
        return {'error': str(e)}


def _fetch_recent_climate(lat, lng):
    try:
        from datetime import date as _date, timedelta as _td
        # Open-Meteo Archive lags real-time by ~2 days
        end = _date.today() - _td(days=2)
        start = end - _td(days=30)
        r = requests.get(
            'https://archive-api.open-meteo.com/v1/archive',
            params={
                'latitude': lat,
                'longitude': lng,
                'start_date': start.isoformat(),
                'end_date': end.isoformat(),
                'daily': 'precipitation_sum,temperature_2m_max,temperature_2m_min,et0_fao_evapotranspiration,shortwave_radiation_sum',
                'timezone': 'auto',
            },
            timeout=30,
        )
        data = r.json()
        daily = data.get('daily', {}) or {}
        precip = [p for p in (daily.get('precipitation_sum') or []) if p is not None]
        tmax = [t for t in (daily.get('temperature_2m_max') or []) if t is not None]
        tmin = [t for t in (daily.get('temperature_2m_min') or []) if t is not None]
        et0 = [e for e in (daily.get('et0_fao_evapotranspiration') or []) if e is not None]
        rad = [s for s in (daily.get('shortwave_radiation_sum') or []) if s is not None]

        def _avg(xs):
            return round(sum(xs) / len(xs), 1) if xs else None

        return {
            'window_start': start.isoformat(),
            'window_end': end.isoformat(),
            'days_observed': len(precip),
            'total_precip_mm': round(sum(precip), 1) if precip else 0,
            'rainy_days': sum(1 for p in precip if p > 1.0),
            'max_daily_rain_mm': round(max(precip), 1) if precip else 0,
            'avg_tmax_c': _avg(tmax),
            'avg_tmin_c': _avg(tmin),
            'peak_tmax_c': round(max(tmax), 1) if tmax else None,
            'avg_et0_mm': _avg(et0),
            'total_et0_mm': round(sum(et0), 1) if et0 else None,
            'avg_radiation_mj': _avg(rad),
            'water_balance_mm': round((sum(precip) - sum(et0)), 1) if precip and et0 else None,
        }
    except Exception as e:
        return {'error': str(e)}


def _classify_soil_texture(sand, silt, clay):
    """USDA soil texture triangle classification."""
    if clay >= 40:
        if sand >= 45: return 'Sandy Clay'
        if silt >= 40: return 'Silty Clay'
        return 'Clay'
    if clay >= 27:
        if sand >= 45: return 'Sandy Clay Loam'
        if sand <= 20: return 'Silty Clay Loam'
        return 'Clay Loam'
    if clay >= 7:
        if sand <= 50:
            if silt >= 50: return 'Silt Loam'
            return 'Loam'
        if sand >= 80: return 'Loamy Sand'
        return 'Sandy Loam'
    if silt >= 80: return 'Silt'
    if sand >= 85: return 'Sand'
    if sand >= 70: return 'Loamy Sand'
    return 'Sandy Loam'


_SOIL_CACHE = {}
_SOIL_CACHE_MAX = 512


def _soilgrids_query(lat, lng, timeout):
    r = requests.get(
        'https://rest.isric.org/soilgrids/v2.0/properties/query',
        params=[
            ('lat', lat), ('lon', lng),
            ('property', 'phh2o'),
            ('property', 'soc'),
            ('property', 'clay'),
            ('property', 'sand'),
            ('property', 'silt'),
            ('property', 'bdod'),
            ('property', 'cec'),
            ('property', 'nitrogen'),
            ('depth', '0-5cm'),
            ('value', 'mean'),
        ],
        timeout=timeout,
    )
    r.raise_for_status()
    return r.json()


def _parse_soilgrids(data):
    out = {}
    for layer in (data.get('properties', {}) or {}).get('layers', []) or []:
        name = layer.get('name')
        d_factor = (layer.get('unit_measure') or {}).get('d_factor') or 1
        depths = layer.get('depths') or []
        if not depths:
            continue
        mean = (depths[0].get('values') or {}).get('mean')
        if mean is None:
            continue
        out[name] = round(mean / d_factor, 2)
    return out


def _fetch_soil(lat, lng):
    # SoilGrids resolves at ~250 m, so round the cache key to ~100 m bins —
    # repeated clicks on the same parcel never re-hit the (slow) upstream.
    cache_key = (round(lat, 3), round(lng, 3))
    cached = _SOIL_CACHE.get(cache_key)
    if cached is not None:
        return cached

    # ISRIC is frequently slow (>15s) and sometimes returns 200 with all-null
    # means at points that fall on a no-data tile. Retry the network call with
    # backoff, and on an all-null response try a small jitter (~250 m) to land
    # on a neighbouring tile that does have data.
    last_error = None
    data = None
    for attempt in range(3):
        try:
            data = _soilgrids_query(lat, lng, timeout=25)
            break
        except Exception as e:
            last_error = e
            time.sleep(1.5 * (attempt + 1))

    if data is None:
        return {'error': f'soilgrids unreachable: {last_error}'}

    out = _parse_soilgrids(data)

    if not out:
        # Walk an outward ring (≈300 m, 1.1 km, 3.3 km) — many points in India
        # land on a no-data SoilGrids cell and only a few neighbouring tiles in
        # the 250 m grid are populated. Fire all probes in parallel and take
        # the first non-empty response so we're bounded by one slow request,
        # not 24 serial ones.
        from concurrent.futures import ThreadPoolExecutor, as_completed
        offsets = []
        for radius in (0.003, 0.01, 0.03):
            offsets.extend([(radius, 0.0), (-radius, 0.0), (0.0, radius), (0.0, -radius),
                            (radius, radius), (-radius, -radius), (radius, -radius), (-radius, radius)])
        with ThreadPoolExecutor(max_workers=len(offsets)) as ex:
            futures = {
                ex.submit(_soilgrids_query, lat + d_lat, lng + d_lng, 12): (d_lat, d_lng)
                for d_lat, d_lng in offsets
            }
            for fut in as_completed(futures):
                try:
                    jitter = fut.result()
                except Exception:
                    continue
                parsed = _parse_soilgrids(jitter)
                if parsed:
                    out = parsed
                    break

    if not out:
        result = {'error': 'no soil data at this location'}
    else:
        clay, sand, silt = out.get('clay'), out.get('sand'), out.get('silt')
        if clay is not None and sand is not None and silt is not None:
            out['texture'] = _classify_soil_texture(sand, silt, clay)
        result = out

    # Cache both successes and no-data results so repeated clicks on the same
    # parcel don't keep paying the ISRIC roundtrip / timeout cost.
    if len(_SOIL_CACHE) >= _SOIL_CACHE_MAX:
        _SOIL_CACHE.pop(next(iter(_SOIL_CACHE)))
    _SOIL_CACHE[cache_key] = result
    return result


def _fetch_elevation(lat, lng):
    try:
        r = requests.get(
            'https://api.open-meteo.com/v1/elevation',
            params={'latitude': lat, 'longitude': lng},
            timeout=20,
        )
        data = r.json()
        elev_arr = data.get('elevation') or []
        return {'elevation_m': elev_arr[0] if elev_arr else None}
    except Exception as e:
        return {'error': str(e)}


@csrf_exempt
def parcel_details(request):
    """
    Returns a bundle of real-time information about a parcel location:
    reverse-geocoded location, live weather + 7-day forecast, last 30 days of
    climate from the Open-Meteo archive, ISRIC SoilGrids topsoil properties,
    and terrain elevation. Each source is fetched in parallel and isolated
    against partial failure.
    """
    try:
        body = json.loads(request.body)
        lat = float(body.get('lat'))
        lng = float(body.get('lng'))

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
            f_loc = ex.submit(_fetch_location, lat, lng)
            f_weather = ex.submit(_fetch_weather, lat, lng)
            f_recent = ex.submit(_fetch_recent_climate, lat, lng)
            f_soil = ex.submit(_fetch_soil, lat, lng)
            f_elev = ex.submit(_fetch_elevation, lat, lng)

            return JsonResponse({
                'lat': lat,
                'lng': lng,
                'location': f_loc.result(),
                'weather': f_weather.result(),
                'recent_climate': f_recent.result(),
                'soil': f_soil.result(),
                'elevation': f_elev.result(),
            })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)
