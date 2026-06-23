import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from django.test import RequestFactory
from apps.farms.views import FarmViewSet
from django.contrib.auth import get_user_model

u = get_user_model().objects.get(username='varunmax7')
rf = RequestFactory()
request = rf.get('/api/v1/farms/1/dashboard/')
request.user = u
view = FarmViewSet.as_view({'get': 'dashboard'})
try:
    response = view(request, pk=1)
    print("Success:", response.data)
except Exception as e:
    import traceback
    traceback.print_exc()
