from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Template UI (all 11 modules + auth pages)
    path('', include('apps.core.urls')),

    # Auth & accounts
    path('api/v1/accounts/', include('apps.accounts.urls')),

    # Farms (includes dashboard/ action at /api/v1/farms/{id}/dashboard/)
    path('api/v1/farms/', include('apps.farms.urls')),

    # Crop catalogue
    path('api/v1/', include('apps.cropdata.urls')),

    # Climate indices, risk zones, projections, vegetation
    path('api/v1/', include('apps.climate.urls')),

    # Advisory — suitability, water balance, irrigation, yield risk
    path('api/v1/', include('apps.advisory.urls')),

    # Alerts
    path('api/v1/', include('apps.alerts.urls')),

    # Reports
    path('api/v1/', include('apps.reports.urls')),

    # OpenAPI schema + Swagger UI + ReDoc
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG and 'debug_toolbar' in settings.INSTALLED_APPS:
    import debug_toolbar
    urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
