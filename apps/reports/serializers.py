from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    download_url = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = ['id', 'farm', 'type', 'period', 'generated_file', 'download_url', 'created_at']
        read_only_fields = ['generated_file', 'created_at']

    def get_download_url(self, obj):
        if obj.generated_file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.generated_file.url)
        return None
