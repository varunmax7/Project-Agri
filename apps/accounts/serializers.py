from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import FarmerProfile

User = get_user_model()

class FarmerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmerProfile
        fields = ['phone', 'language', 'default_season']

class UserSerializer(serializers.ModelSerializer):
    farmer_profile = FarmerProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'farmer_profile']

class RegisterSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(write_only=True, required=True, max_length=15)
    language = serializers.ChoiceField(choices=FarmerProfile.Languages.choices, write_only=True, default=FarmerProfile.Languages.EN)
    default_season = serializers.CharField(write_only=True, default='Kharif')
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'phone', 'language', 'default_season']

    def create(self, validated_data):
        phone = validated_data.pop('phone')
        language = validated_data.pop('language', FarmerProfile.Languages.EN)
        default_season = validated_data.pop('default_season', 'Kharif')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=User.Roles.FARMER
        )

        FarmerProfile.objects.create(
            user=user,
            phone=phone,
            language=language,
            default_season=default_season
        )

        return user
