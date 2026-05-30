from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CropSuitabilityViewSet, CropSuitabilityTrendViewSet,
    WaterBalanceViewSet, IrrigationAdvisoryViewSet, YieldRiskViewSet,
)

app_name = 'advisory'

router = DefaultRouter()
router.register(r'advisory/suitability', CropSuitabilityViewSet, basename='crop-suitability')
router.register(r'advisory/suitability-trends', CropSuitabilityTrendViewSet, basename='suitability-trend')
router.register(r'advisory/water-balance', WaterBalanceViewSet, basename='water-balance')
router.register(r'advisory/irrigation', IrrigationAdvisoryViewSet, basename='irrigation')
router.register(r'advisory/yield-risk', YieldRiskViewSet, basename='yield-risk')

urlpatterns = [
    path('', include(router.urls)),
]
