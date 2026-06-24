from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse
from .models import Report
from .serializers import ReportSerializer
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from django.utils import timezone

@extend_schema_view(
    list=extend_schema(
        summary='List generated reports for user\'s farms',
        tags=['reports'],
        parameters=[OpenApiParameter('farm', int, description='Filter by farm ID')],
    ),
    retrieve=extend_schema(summary='Report detail and download URL', tags=['reports']),
    destroy=extend_schema(summary='Delete a report record', tags=['reports']),
)
class ReportViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Report.objects.all()
        farm_id = self.request.query_params.get('farm')
        report_type = self.request.query_params.get('type')
        if farm_id:
            qs = qs.filter(farm_id=farm_id)
        if report_type:
            qs = qs.filter(type=report_type)
        return qs

    @extend_schema(
        summary='Generate a PDF report for a farm',
        tags=['reports'],
        request=ReportSerializer,
        responses={
            201: ReportSerializer,
            400: OpenApiResponse(description='Missing farm or type'),
            500: OpenApiResponse(description='PDF rendering failed'),
        },
    )
    @action(detail=False, methods=['post'], url_path='generate')
    def generate(self, request):
        farm_id = request.data.get('farm')
        report_type = request.data.get('type')
        period = request.data.get('period', '')

        if not farm_id or not report_type:
            return Response(
                {'detail': 'farm and type are required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        from apps.farms.models import Farm
        try:
            farm = Farm.objects.get(pk=farm_id)
        except Farm.DoesNotExist:
            return Response({'detail': 'Farm not found.'}, status=status.HTTP_404_NOT_FOUND)

        report = Report.objects.create(
            farm=farm,
            type=report_type,
            period=period or timezone.now().strftime('%b %Y'),
        )

        # ── Gather all data for the report ──────────────────────────
        from apps.cropdata.models import CropSuitability
        from apps.climate.models import ClimateRiskZone, DistrictInsight

        # 1. Crop Suitability
        suitability_data = CropSuitability.objects.filter(
            district__iexact=farm.district
        ).order_by('-change_class')

        # 2. Climate Risk Zones (SSP245 across all available years)
        climate_zones = ClimateRiskZone.objects.filter(
            district__iexact=farm.district,
            scenario='ssp245',
        ).order_by('year')

        # Build the 2030 baseline summary card
        climate_summary = None
        climate_projections = []
        for zone in climate_zones:
            if not isinstance(zone.geometry, dict):
                continue
            props = zone.geometry.get('properties', {})
            row = {
                'year': zone.year,
                'overall_risk_score': _fmt(props.get('overall_risk_score')),
                'overall_risk_class': props.get('overall_risk_class', '—'),
                'temperature_change': _fmt(props.get('temperature_change')),
                'rainfall_change': _fmt(props.get('rainfall_change')),
                'drought_hazard_score': _fmt(props.get('drought_hazard_score')),
                'drought_hazard_class': props.get('drought_hazard_class', '—'),
                'flood_hazard_score': _fmt(props.get('flood_hazard_score')),
                'flood_hazard_class': props.get('flood_hazard_class', '—'),
                'ag_stress_score': _fmt(props.get('ag_stress_score')),
                'ag_stress_class': props.get('ag_stress_class', '—'),
                'water_availability_index': _fmt(props.get('water_availability_index')),
                'heat_stress_days': _fmt(props.get('heat_stress_days')),
            }
            climate_projections.append(row)
            if zone.year == 2030 and climate_summary is None:
                climate_summary = row

        # 3. District Insights
        district_insights = DistrictInsight.objects.filter(
            district__iexact=farm.district,
        ).order_by('scenario', 'year')

        # 4. Check if there are high-risk crops
        has_high_risk_crops = suitability_data.filter(change_class__gte=2).exists()

        # Report title
        type_titles = {
            'village': f'Village Climate Report — {farm.village}, {farm.district}',
            'farm': f'Farm Climate Report — {farm.name}',
            'risk': f'Risk Indicator Report — {farm.district} District',
        }
        report_title = type_titles.get(report_type, 'Climate & Agriculture Report')

        context = {
            'farm': farm,
            'report': report,
            'report_title': report_title,
            'user': request.user,
            'suitability_data': suitability_data,
            'climate_summary': climate_summary,
            'climate_projections': climate_projections,
            'district_insights': district_insights,
            'has_high_risk_crops': has_high_risk_crops,
            'generation_date': timezone.now(),
        }

        # ── Render HTML → PDF with weasyprint ───────────────────────
        try:
            import weasyprint
            html_string = render_to_string(
                'reports/pdf/village_climate_report.html', context
            )
            pdf_bytes = weasyprint.HTML(string=html_string).write_pdf()

            filename = (
                f"{report_type}_{farm.district.lower().replace(' ', '_')}"
                f"_{timezone.now().strftime('%Y%m%d_%H%M')}.pdf"
            )
            report.generated_file.save(filename, ContentFile(pdf_bytes))
        except Exception as e:
            import traceback
            traceback.print_exc()
            report.delete()
            return Response(
                {'detail': f'PDF Generation Failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            ReportSerializer(report, context={'request': request}).data,
            status=status.HTTP_201_CREATED,
        )


def _fmt(value, decimals=2):
    """Safely format a numeric value from GeoJSON properties."""
    if value is None:
        return '—'
    try:
        return round(float(value), decimals)
    except (ValueError, TypeError):
        return str(value)
