from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Auth
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('auth/register/', views.register_view, name='register'),

    # Modules
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('farm/', views.MyFarmView.as_view(), name='myfarm'),
    path('weather/', views.WeatherView.as_view(), name='weather'),
    path('district-outlook/', views.DistrictOutlookView.as_view(), name='district_outlook'),
    path('crop-advisory/', views.CropAdvisoryView.as_view(), name='crop_advisory'),
    path('water-management/', views.WaterManagementView.as_view(), name='water_management'),
    path('future-outlook/', views.FutureOutlookView.as_view(), name='future_outlook'),
    path('alerts/', views.AlertsView.as_view(), name='alerts'),
    path('market-insights/', views.MarketInsightsView.as_view(), name='market_insights'),
    path('reports/', views.ReportsView.as_view(), name='reports'),
    path('help/', views.HelpView.as_view(), name='help'),
    path('settings/', views.SettingsView.as_view(), name='settings'),
    path('interactive-map/', views.InteractiveMapView.as_view(), name='interactive_map'),
    path('inspector/', __import__('apps.farms.views', fromlist=['parcel_inspector_view']).parcel_inspector_view, name='parcel_inspector'),

    # API endpoints
    path('api/map-data/risk/', views.api_map_risk, name='api_map_risk'),
    path('api/map-data/suitability/', views.api_map_suitability, name='api_map_suitability'),
    path('api/map-data/insights/', views.api_district_insights, name='api_district_insights'),
]
