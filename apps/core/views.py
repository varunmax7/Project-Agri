from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.contrib import messages
from apps.alerts.models import Alert


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


class ReportsView(ModuleView):
    template_name = 'pages/reports.html'
    active_module = 'reports'
    page_title = 'Reports'
    page_subtitle = 'Generate & Download PDF Reports'


class HelpView(ModuleView):
    template_name = 'pages/help.html'
    active_module = 'help'
    page_title = 'Help & Support'
    page_subtitle = 'FAQs, Guides & Contact'


class SettingsView(ModuleView):
    template_name = 'pages/settings.html'
    active_module = 'settings'
    page_title = 'Settings'
    page_subtitle = 'Profile, Location & Preferences'


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
