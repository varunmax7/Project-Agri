from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FarmViewSet, parcel_inspector_view, stac_ndvi_timeseries, parcel_details

app_name = 'farms'

router = DefaultRouter()
router.register(r'', FarmViewSet, basename='farm')

urlpatterns = [
    path('inspector/', parcel_inspector_view, name='parcel_inspector'),
    path('api/stac-ndvi/', stac_ndvi_timeseries, name='stac_ndvi'),
    path('api/parcel-details/', parcel_details, name='parcel_details'),
    path('', include(router.urls)),
]
