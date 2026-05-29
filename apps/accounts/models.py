from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Roles(models.TextChoices):
        FARMER = 'FARMER', 'Farmer'
        FPO = 'FPO', 'Farmer Producer Organization'
        ADMIN = 'ADMIN', 'Admin'

    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.FARMER)

    def __str__(self):
        return self.username

class FarmerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='farmer_profile')
    phone = models.CharField(max_length=15, unique=True)
    
    class Languages(models.TextChoices):
        EN = 'EN', 'English'
        HI = 'HI', 'Hindi'
        TE = 'TE', 'Telugu'

    language = models.CharField(max_length=2, choices=Languages.choices, default=Languages.EN)
    default_season = models.CharField(max_length=20, default='Kharif')

    def __str__(self):
        return f"{self.user.username} Profile"
