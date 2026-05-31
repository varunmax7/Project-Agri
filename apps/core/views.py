from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.contrib import messages
from django.http import JsonResponse
from apps.alerts.models import Alert
from apps.climate.models import ClimateRiskZone, DistrictInsight
from apps.cropdata.models import CropSuitability


# ---------------------------------------------------------------------------
# Base mixin — injects active_module + page_title into every template
# ---------------------------------------------------------------------------
class ModuleView(LoginRequiredMixin, TemplateView):
    active_module = ''
    page_title = ''
    page_subtitle = ''

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['active_module'] = self.active_module
        ctx['page_title'] = self.page_title
        ctx['page_subtitle'] = self.page_subtitle
        # Inject the user's first farm for the topbar farm switcher
        farms = self.request.user.farms.all()
        ctx['user_farms'] = farms
        ctx['current_farm'] = farms.first()
        if ctx['current_farm']:
            ctx['unread_alert_count'] = Alert.objects.filter(farm=ctx['current_farm'], is_read=False).count()
        else:
            ctx['unread_alert_count'] = 0
        return ctx


# ---------------------------------------------------------------------------
# Module views
# ---------------------------------------------------------------------------
class DashboardView(ModuleView):
    template_name = 'pages/dashboard.html'
    active_module = 'dashboard'
    page_title = 'My Farm Overview'
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if ctx.get('current_farm'):
            farm = ctx['current_farm']
            ctx['page_subtitle'] = f"{farm.village}, {farm.district}" if farm.village else farm.district
        else:
            ctx['page_subtitle'] = 'Climate Intelligence Overview'
        return ctx


class MyFarmView(ModuleView):
    template_name = 'pages/myfarm.html'
    active_module = 'myfarm'
    page_title = 'My Farm'
    page_subtitle = 'Farm Profile & Field Management'


class WeatherView(ModuleView):
    template_name = 'pages/weather.html'
    active_module = 'weather'
    page_title = 'Weather & Climate'
    page_subtitle = 'Current Conditions & Seasonal Summary'


class DistrictOutlookView(ModuleView):
    template_name = 'pages/district_outlook.html'
    active_module = 'district_outlook'
    page_title = 'District Outlook'
    page_subtitle = 'Evidence-based crop transition planning for 2030–2040'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        import csv, os
        from django.conf import settings

        csv_path = os.path.join(settings.BASE_DIR, 'data', 'crop_suitability_final_output.csv')

        # Build full lookup: state -> districts, district -> crops
        all_rows = []
        states_map = {}   # state -> set of districts
        try:
            with open(csv_path, encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    all_rows.append(row)
                    states_map.setdefault(row['state'], set()).add(row['district'])
        except Exception:
            pass

        states = sorted(states_map.keys())
        ctx['all_states'] = states

        # For each state, sorted district list (used for JS dropdowns)
        import json
        state_districts = {s: sorted(d) for s, d in states_map.items()}
        ctx['state_districts_json'] = json.dumps(state_districts)

        # Default selection: farm's state/district OR first in CSV
        farm = ctx.get('current_farm')
        sel_state = self.request.GET.get('state') or (farm.state if farm and hasattr(farm, 'state') else states[0] if states else '')
        sel_district = self.request.GET.get('district') or (farm.district if farm else '')
        sel_scenario = self.request.GET.get('scenario', 'ssp245')
        sel_year = self.request.GET.get('year', '2040')

        # Validate district belongs to state
        if sel_state not in state_districts or sel_district not in state_districts.get(sel_state, set()):
            sel_district = sorted(state_districts.get(sel_state, ['']))[0] if sel_state in state_districts else ''

        ctx['sel_state'] = sel_state
        ctx['sel_district'] = sel_district
        ctx['sel_scenario'] = sel_scenario
        ctx['sel_year'] = sel_year

        # Filter rows for selected district
        district_rows = [r for r in all_rows if r['district'] == sel_district]
        ctx['district_rows'] = district_rows

        # Build crop suitability cards
        suitability_key = f'suitability_{sel_year}_{sel_scenario}'
        crops = []
        for row in district_rows:
            current = row.get('current_suitability', '—')
            future = row.get(suitability_key, '—')
            decline_key = f'{sel_scenario}_decline_classes_by_2040'
            decline = row.get(decline_key, '0')
            try:
                decline_int = int(float(decline))
            except (ValueError, TypeError):
                decline_int = 0

            explanation_key = f'{sel_scenario}_{sel_year}_explanation' if f'{sel_scenario}_{sel_year}_explanation' in row else f'{sel_scenario}_2040_explanation'
            crops.append({
                'name': row.get('crop', ''),
                'current': current,
                'future': future,
                'decline': decline_int,
                'recommendation': row.get('recommendation', ''),
                'explanation': row.get(explanation_key, row.get(f'{sel_scenario}_2040_explanation', '')),
                'historical': row.get('crop_historical_analysis', ''),
                'soil': row.get('soil_type', ''),
                'lgp': row.get('length_of_growing_period_days', ''),
            })
        ctx['crops'] = crops

        # District-level climate metrics (from first row, scenario-specific)
        if district_rows:
            r0 = district_rows[0]
            prefix = f'overall_risk_score_{sel_year}_{sel_scenario}'
            ctx['climate'] = {
                'overall_risk': r0.get(f'overall_risk_score_{sel_year}_{sel_scenario}', '—'),
                'overall_risk_class': r0.get(f'overall_risk_class_{sel_year}_{sel_scenario}', '—'),
                'flood_hazard': r0.get(f'flood_hazard_score_{sel_year}_{sel_scenario}', '—'),
                'flood_class': r0.get(f'flood_hazard_class_{sel_year}_{sel_scenario}', '—'),
                'drought_hazard': r0.get(f'drought_hazard_score_{sel_year}_{sel_scenario}', '—'),
                'drought_class': r0.get(f'drought_hazard_class_{sel_year}_{sel_scenario}', '—'),
                'ag_stress': r0.get(f'ag_stress_score_{sel_year}_{sel_scenario}', '—'),
                'ag_stress_class': r0.get(f'ag_stress_class_{sel_year}_{sel_scenario}', '—'),
                'temp_change': r0.get(f'temperature_change_{sel_year}_{sel_scenario}', '—'),
                'rainfall_change': r0.get(f'rainfall_change_{sel_year}_{sel_scenario}', '—'),
                'water_avail': r0.get(f'water_availability_index_{sel_year}_{sel_scenario}', '—'),
                'heat_stress_days': r0.get(f'heat_stress_days_{sel_year}_{sel_scenario}', '—'),
                'major_crop': r0.get('district_major_crop', '—'),
                'major_crop_area': r0.get('district_major_crop_latest_area_1000ha', '—'),
                'major_crop_analysis': r0.get('district_major_crop_analysis', ''),
            }
        else:
            ctx['climate'] = {}

        return ctx


class CropAdvisoryView(ModuleView):
    template_name = 'pages/crop_advisory.html'
    active_module = 'crop_advisory'
    page_title = 'Crop Advisory'
    page_subtitle = 'Suitability Ranking & Planning'


class WaterManagementView(ModuleView):
    template_name = 'pages/water_management.html'
    active_module = 'water_management'
    page_title = 'Water Management'
    page_subtitle = 'Soil Moisture, Stress & Irrigation Scheduling'


class FutureOutlookView(ModuleView):
    template_name = 'pages/future_outlook.html'
    active_module = 'future_outlook'
    page_title = 'Future Outlook'
    page_subtitle = 'Climate Projections 2030 – 2040'


class AlertsView(ModuleView):
    template_name = 'pages/alerts.html'
    active_module = 'alerts'
    page_title = 'Alerts & Notifications'
    page_subtitle = 'Strategic & Operational Alerts'


class MarketInsightsView(ModuleView):
    template_name = 'pages/market_insights.html'
    active_module = 'market_insights'
    page_title = 'Market Insights'
    page_subtitle = 'Price Trends & Demand Signals'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        farm = ctx.get('current_farm')
        if not farm:
            return ctx
            
        from apps.cropdata.models import CropSuitability
        import random
        
        msp_base = {
            'Paddy': 2183, 'Soybean': 4600, 'Maize': 2090, 
            'Cotton': 6620, 'Groundnut': 6377, 'Millets': 2500, 'Turmeric': 6800
        }
        icons = {
            'Paddy': '🌾', 'Soybean': '🫘', 'Maize': '🌽',
            'Cotton': '🌿', 'Groundnut': '🥜', 'Millets': '🌾', 'Turmeric': '✨'
        }
        
        market_data = []
        # Get unique crops for this district
        crops = CropSuitability.objects.filter(district__iexact=farm.district).values('crop', 'change_class').distinct()
        
        # deduplicate by crop name
        seen = set()
        for c in crops:
            c_name = c['crop'].capitalize()
            if c_name in seen: continue
            seen.add(c_name)
            
            msp = msp_base.get(c_name, 3000)
            icon = icons.get(c_name, '🌱')
            chg = c['change_class']
            
            if chg < 0:
                mandi = msp + int(abs(chg) * 150) + random.randint(10, 50)
                demand = "High"
            elif chg > 0:
                mandi = msp - int(abs(chg) * 60) - random.randint(10, 40)
                demand = "Low"
            else:
                mandi = msp + random.randint(10, 80)
                demand = "Medium"
                
            market_data.append({
                'name': c_name, 'icon': icon, 'msp': msp, 'mandi': mandi,
                'diff': mandi - msp, 'demand': demand
            })
            
        ctx['market_data'] = market_data
        
        if market_data:
            t = market_data[0]
            ctx['trend_crop'] = t['name']
            ctx['trend_mandi'] = [t['mandi'] - 80, t['mandi'] - 40, t['mandi'] - 10, t['mandi'] + 20, t['mandi'] + 5, t['mandi']]
            ctx['trend_msp'] = [t['msp']] * 6
            
        return ctx


class ReportsView(ModuleView):
    template_name = 'pages/reports.html'
    active_module = 'reports'
    page_title = 'Reports'
    page_subtitle = 'Generate & Download PDF Reports'


class HelpView(ModuleView):
    template_name = 'pages/help.html'
    active_module = 'help'
    page_title = 'Help & Support'
    page_subtitle = 'Data Dictionary & Glossary'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        import csv
        import os
        from django.conf import settings
        
        faq_data = []
        csv_path = os.path.join(settings.BASE_DIR, 'data', 'final', 'dashboard', 'frontend_package', 'README_dashboard_fields.csv')
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    q = f"What is the {row.get('display_name', '')}?"
                    ans = f"{row.get('description', '')}"
                    if row.get('units') and row.get('units') != 'text' and row.get('units') != 'class':
                        ans += f" It is measured in {row.get('units')}."
                    if row.get('example'):
                        ans += f" (Example: {row.get('example')})"
                    
                    faq_data.append({
                        'q': q,
                        'a': ans
                    })
        except Exception:
            pass
            
        ctx['faq_data'] = faq_data
        return ctx


class SettingsView(ModuleView):
    template_name = 'pages/settings.html'
    active_module = 'settings'
    page_title = 'Settings'
    page_subtitle = 'Profile, Location & Preferences'


class InteractiveMapView(ModuleView):
    template_name = 'pages/interactive_map.html'
    active_module = 'interactive_map'
    page_title = 'Interactive Data Explorer'
    page_subtitle = 'Visualize Climate Risk & Crop Suitability'


# ---------------------------------------------------------------------------
# API views for Map Data
# ---------------------------------------------------------------------------
def api_map_risk(request):
    scenario = request.GET.get('scenario', 'ssp245')
    year_str = request.GET.get('year', '2030')
    year = int(year_str) if year_str.isdigit() else 2030

    if year < 2030: year = 2030
    elif 2031 <= year <= 2034: year = 2035
    elif 2036 <= year <= 2039: year = 2040
    elif year > 2040: year = 2040

    actual_scenario = 'ssp245' if scenario == 'ssp370' else scenario
    zones = ClimateRiskZone.objects.filter(scenario=actual_scenario, year=year)
    
    features = []
    for zone in zones:
        feature = zone.geometry
        if isinstance(feature, dict):
            features.append(feature)

    return JsonResponse({
        "type": "FeatureCollection",
        "features": features
    })

def api_map_suitability(request):
    crop = request.GET.get('crop', 'Maize')
    
    suitabilities = CropSuitability.objects.filter(crop__icontains=crop)
    
    data = []
    for s in suitabilities:
        data.append({
            "district": s.district.upper(),
            "state": s.state.upper(),
            "suitability_current": s.suitability_current,
            "suitability_projected": s.suitability_projected,
            "change_class": s.change_class,
            "recommendation": s.recommendation
        })
        
    return JsonResponse({"data": data})

def api_district_insights(request):
    district = request.GET.get('district', '')
    scenario = request.GET.get('scenario', 'ssp245')
    year_str = request.GET.get('year', '2030')
    year = int(year_str) if year_str.isdigit() else 2030

    insight = DistrictInsight.objects.filter(district__iexact=district, scenario=scenario, year=year).first()
    
    if insight:
        return JsonResponse({
            "district": insight.district,
            "key_insight_1": insight.key_insight_1,
            "key_insight_2": insight.key_insight_2,
            "key_insight_3": insight.key_insight_3,
        })
    return JsonResponse({}, status=404)


# ---------------------------------------------------------------------------
# Auth views
# ---------------------------------------------------------------------------
def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get('next', 'core:dashboard'))
        messages.error(request, 'Invalid username or password.')
    return render(request, 'auth/login.html')


def logout_view(request):
    logout(request)
    return redirect('core:login')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    return render(request, 'auth/register.html')
