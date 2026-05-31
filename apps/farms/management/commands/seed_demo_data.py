from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.farms.utils import create_demo_farm_for_user

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with demo data for all users who do not have a farm'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding demo data...')

        # Ensure ramesh_kumar exists
        user, created = User.objects.get_or_create(
            username='ramesh_kumar',
            defaults={
                'email': 'ramesh@example.com',
                'first_name': 'Ramesh',
                'last_name': 'Kumar',
                'role': 'farmer',
            }
        )
        if created:
            user.set_password('demo123')
            user.save()
        
        # Give every user a demo farm if they don't have one
        users_without_farm = User.objects.filter(farms__isnull=True)
        count = 0
        for u in users_without_farm:
            create_demo_farm_for_user(u)
            count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded demo data for {count} user(s)!'))
