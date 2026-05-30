from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LocationClimateIndexViewSet, ClimateRiskZoneViewSet,
    VegetationObservationViewSet, StressAssessmentViewSet, ClimateProjectionViewSet,
)

app_name = 'climate'

router = DefaultRouter()
router.register(r'climate/indices', LocationClimateIndexViewSet, basename='climate-index')
router.register(r'climate/risk-zones', ClimateRiskZoneViewSet, basename='climate-risk-zone')
router.register(r'climate/vegetation', VegetationObservationViewSet, basename='vegetation')
router.register(r'climate/stress', StressAssessmentViewSet, basename='stress')
router.register(r'climate/projections', ClimateProjectionViewSet, basename='climate-projection')

urlpatterns = [
    path('', include(router.urls)),
]
