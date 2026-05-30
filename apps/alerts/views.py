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

    def get_queryset(self):
        qs = Alert.objects.filter(farm__user=self.request.user)
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
