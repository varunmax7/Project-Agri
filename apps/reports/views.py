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
import weasyprint


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
        qs = Report.objects.filter(farm__user=self.request.user)
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
            501: OpenApiResponse(description='PDF rendering not yet available'),
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

        # Verify the farm belongs to the requesting user
        from apps.farms.models import Farm
        try:
            farm = Farm.objects.get(pk=farm_id, user=request.user)
        except Farm.DoesNotExist:
            return Response({'detail': 'Farm not found.'}, status=status.HTTP_404_NOT_FOUND)

        report = Report.objects.create(farm=farm, type=report_type, period=period or timezone.now().strftime('%b %Y'))

        # Fetch Context for the PDF Template
        from apps.advisory.models import CropSuitability, WaterBalance
        suitability_data = CropSuitability.objects.filter(farm=farm).order_by('-suitability_pct')[:5]
        water_data = WaterBalance.objects.filter(farm=farm).order_by('month')[:6]

        context = {
            'farm': farm,
            'report': report,
            'user': request.user,
            'suitability_data': suitability_data,
            'water_data': water_data,
            'generation_date': timezone.now()
        }

        # Render HTML and generate PDF
        try:
            html_string = render_to_string('reports/pdf/village_climate_report.html', context)
            pdf_bytes = weasyprint.HTML(string=html_string).write_pdf()
            
            # Save the file to the Report model
            filename = f"{report_type}_{farm.id}_{timezone.now().strftime('%Y%m%d%H%M')}.pdf"
            report.generated_file.save(filename, ContentFile(pdf_bytes))
        except Exception as e:
            # If PDF generation fails, we can either return a 500 or just leave the record without a file.
            # We'll print it to terminal for debugging and return an error response
            print("PDF GENERATION FAILED:", str(e))
            report.delete()
            return Response({'detail': f'PDF Generation Failed: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(
            ReportSerializer(report, context={'request': request}).data,
            status=status.HTTP_201_CREATED,
        )
