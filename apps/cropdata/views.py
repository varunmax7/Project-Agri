from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import Crop, CropCalendar, BestPractice
from .serializers import CropSerializer, CropDetailSerializer, CropCalendarSerializer, BestPracticeSerializer


@extend_schema_view(
    list=extend_schema(summary='List all crops', tags=['cropdata']),
    retrieve=extend_schema(summary='Crop detail with calendar & best practices', tags=['cropdata']),
)
class CropViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Crop.objects.all().order_by('name')
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CropDetailSerializer
        return CropSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        season = self.request.query_params.get('season')
        category = self.request.query_params.get('category')
        if season:
            qs = qs.filter(season__iexact=season)
        if category:
            qs = qs.filter(category__iexact=category)
        return qs


@extend_schema_view(
    list=extend_schema(summary='List crop calendars', tags=['cropdata']),
)
class CropCalendarViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = CropCalendarSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        crop_pk = self.kwargs.get('crop_pk')
        return CropCalendar.objects.filter(crop_id=crop_pk)


@extend_schema_view(
    list=extend_schema(summary='List best practices for a crop', tags=['cropdata']),
)
class BestPracticeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = BestPracticeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        crop_pk = self.kwargs.get('crop_pk')
        return BestPractice.objects.filter(crop_id=crop_pk)
