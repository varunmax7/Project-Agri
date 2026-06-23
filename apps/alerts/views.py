from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from .models import Alert
from .serializers import AlertSerializer


@extend_schema_view(
    list=extend_schema(
        summary='List alerts for user\'s farms',
        tags=['alerts'],
        parameters=[
            OpenApiParameter('farm', int, description='Filter by farm ID'),
            OpenApiParameter('category', str, description='weather | crop | advisory | strategic'),
            OpenApiParameter('severity', str, description='low | medium | high'),
            OpenApiParameter('unread', bool, description='Return only unread alerts'),
        ],
    ),
    retrieve=extend_schema(summary='Alert detail', tags=['alerts']),
    partial_update=extend_schema(summary='Mark alert as read', tags=['alerts']),
)
class AlertViewSet(viewsets.ModelViewSet):
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'patch', 'delete', 'head', 'options']

    def _sync_real_alerts(self, farm):
        # To avoid constant DB writes, only sync if there are fewer than 3 alerts
        if Alert.objects.filter(farm=farm).count() >= 3:
            return
            
        from apps.climate.models import ClimateRiskZone
        from apps.cropdata.models import CropSuitability
        
        # 1. Weather/Water Alert from ClimateRiskZone (2030, ssp245)
        climate = ClimateRiskZone.objects.filter(district__iexact=farm.district, scenario='ssp245', year=2030).first()
        if climate and isinstance(climate.geometry, dict):
            props = climate.geometry.get('properties', {})
            t_change = float(props.get('temperature_change') or 0)
            d_score = float(props.get('drought_hazard_score') or 0)
            
            if t_change > 1.0:
                Alert.objects.create(farm=farm, category='weather', severity='high', title='Extreme Heat Projection', message=f'Climate models project a {round(t_change,2)}°C temperature increase.')
            else:
                Alert.objects.create(farm=farm, category='weather', severity='info', title='Temperature Shift', message=f'A moderate {round(t_change,2)}°C temperature shift is projected for your district by 2030.')
                
            if d_score > 30:
                Alert.objects.create(farm=farm, category='water', severity='high', title='Water Stress Warning', message=f'Drought hazard score is projected at {round(d_score,2)}. Immediate irrigation planning recommended.')
            else:
                Alert.objects.create(farm=farm, category='water', severity='info', title='Drought Risk Stable', message=f'Drought hazard score remains manageable at {round(d_score,2)}.')
                
        # 2. Crop Suitability Alerts
        crops = CropSuitability.objects.filter(district__iexact=farm.district).order_by('change_class')
        if crops.exists():
            worst_crop = crops.first()
            if worst_crop.change_class < 0:
                Alert.objects.create(farm=farm, category='strategic', severity='medium', title=f'{worst_crop.crop} Suitability Decline', message=f'Projection indicates a drop in {worst_crop.crop} suitability. Recommendation: {worst_crop.recommendation}')
            else:
                best_crop = crops.last()
                Alert.objects.create(farm=farm, category='strategic', severity='low', title=f'{best_crop.crop} Suitability Improving', message=f'{best_crop.crop} suitability is projected to improve by {best_crop.change_class} classes. Recommendation: {best_crop.recommendation}')

    def get_queryset(self):
        from apps.farms.models import Farm
        for farm in Farm.objects.all():
            self._sync_real_alerts(farm)

        qs = Alert.objects.all()
        farm_id = self.request.query_params.get('farm')
        category = self.request.query_params.get('category')
        severity = self.request.query_params.get('severity')
        unread = self.request.query_params.get('unread')
        if farm_id:
            qs = qs.filter(farm_id=farm_id)
        if category:
            qs = qs.filter(category=category)
        if severity:
            qs = qs.filter(severity=severity)
        if unread and unread.lower() == 'true':
            qs = qs.filter(is_read=False)
        return qs

    @extend_schema(
        summary='Mark all alerts as read for a farm',
        tags=['alerts'],
        parameters=[OpenApiParameter('farm', int, required=True, description='Farm ID')],
    )
    @action(detail=False, methods=['post'], url_path='mark-all-read')
    def mark_all_read(self, request):
        farm_id = request.query_params.get('farm')
        qs = self.get_queryset().filter(is_read=False)
        if farm_id:
            qs = qs.filter(farm_id=farm_id)
        updated = qs.update(is_read=True)
        return Response({'marked_read': updated})

    @extend_schema(summary='Unread alert count per farm', tags=['alerts'])
    @action(detail=False, methods=['get'], url_path='unread-count')
    def unread_count(self, request):
        farm_id = request.query_params.get('farm')
        qs = self.get_queryset().filter(is_read=False)
        if farm_id:
            qs = qs.filter(farm_id=farm_id)
        return Response({'unread_count': qs.count()})
