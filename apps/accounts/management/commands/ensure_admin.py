"""
Management command: ensure_admin
Creates a superuser on startup if one doesn't exist.
Reads credentials from env vars:
  DJANGO_SUPERUSER_EMAIL    (default: admin@floodguard.com)
  DJANGO_SUPERUSER_USERNAME (default: admin)
  DJANGO_SUPERUSER_PASSWORD (default: admin123 — CHANGE THIS)
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os


class Command(BaseCommand):
    help = 'Create a superuser if none exists (for initial production setup)'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@floodguard.com')
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')

        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(self.style.WARNING('Superuser already exists, skipping.'))
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )
        self.stdout.write(self.style.SUCCESS(f'Superuser created: {username} / {email}'))
