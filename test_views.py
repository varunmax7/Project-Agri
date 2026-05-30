import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()
client = Client()
user = User.objects.get(username='ramesh_kumar')
client.force_login(user)

urls = ['/weather/', '/market-insights/', '/settings/', '/help/']
for url in urls:
    response = client.get(url)
    print(f"{url}: {response.status_code}")
