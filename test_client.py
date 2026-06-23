import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

u = get_user_model().objects.get(username='varunmax7')
c = Client()
c.force_login(u)
response = c.get('/api/v1/farms/1/dashboard/?season=Kharif&year=2030')
print("Status Code:", response.status_code)
if response.status_code != 200:
    print(response.content.decode('utf-8')[:500])
