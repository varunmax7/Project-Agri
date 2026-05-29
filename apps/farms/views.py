from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Farm
from .serializers import FarmSerializer

class FarmViewSet(viewsets.ModelViewSet):
    serializer_class = FarmSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Users can only see and edit their own farms
        return Farm.objects.filter(user=self.request.user)
