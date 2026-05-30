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
    path('crop-advisory/', views.CropAdvisoryView.as_view(), name='crop_advisory'),
    path('water-management/', views.WaterManagementView.as_view(), name='water_management'),
    path('future-outlook/', views.FutureOutlookView.as_view(), name='future_outlook'),
    path('alerts/', views.AlertsView.as_view(), name='alerts'),
    path('market-insights/', views.MarketInsightsView.as_view(), name='market_insights'),
    path('reports/', views.ReportsView.as_view(), name='reports'),
    path('help/', views.HelpView.as_view(), name='help'),
    path('settings/', views.SettingsView.as_view(), name='settings'),
]
