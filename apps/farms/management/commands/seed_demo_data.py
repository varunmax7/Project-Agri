from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.accounts.models import FarmerProfile
from apps.farms.models import Farm, Field, ActivityLog
from apps.cropdata.models import Crop, CropCalendar, BestPractice
from apps.climate.models import LocationClimateIndex, ClimateRiskZone, VegetationObservation, StressAssessment, ClimateProjection
from apps.advisory.models import CropSuitability, CropSuitabilityTrend, WaterBalance, IrrigationAdvisory, YieldRisk
from apps.alerts.models import Alert
from django.utils import timezone
from datetime import timedelta
import json

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with demo data for Nizamabad'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding demo data...')

        # 1. User & Profile
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
        
        profile, _ = FarmerProfile.objects.get_or_create(
            user=user,
            defaults={
                'phone': '+919876543210',
                'language': 'en',
                'default_season': 'Kharif 2030'
            }
        )

        # 2. Crops
        paddy, _ = Crop.objects.get_or_create(
            name='Paddy',
            defaults={
                'category': 'Cereal', 'season': 'Kharif', 'water_requirement_mm': 1200,
                'temp_min': 20.0, 'temp_max': 35.0, 'optimal_soil_moisture': 80.0
            }
        )
        soybean, _ = Crop.objects.get_or_create(
            name='Soybean',
            defaults={
                'category': 'Legume', 'season': 'Kharif', 'water_requirement_mm': 600,
                'temp_min': 15.0, 'temp_max': 30.0, 'optimal_soil_moisture': 60.0
            }
        )
        maize, _ = Crop.objects.get_or_create(
            name='Maize',
            defaults={
                'category': 'Cereal', 'season': 'Rabi', 'water_requirement_mm': 500,
                'temp_min': 10.0, 'temp_max': 25.0, 'optimal_soil_moisture': 55.0
            }
        )

        CropCalendar.objects.get_or_create(crop=paddy, agro_zone='Northern Telangana', defaults={'sowing_start': '2030-06-15', 'sowing_end': '2030-07-15', 'vegetative': 45, 'flowering': 30, 'harvest': 25})
        CropCalendar.objects.get_or_create(crop=soybean, agro_zone='Northern Telangana', defaults={'sowing_start': '2030-06-20', 'sowing_end': '2030-07-05', 'vegetative': 35, 'flowering': 25, 'harvest': 20})
        
        BestPractice.objects.get_or_create(crop=paddy, stage='Pre-sowing', defaults={'text': 'Ensure field is puddled and leveled to retain standing water.'})
        BestPractice.objects.get_or_create(crop=paddy, stage='Vegetative', defaults={'text': 'Maintain 5cm standing water. Apply first split of Nitrogen.'})
        BestPractice.objects.get_or_create(crop=soybean, stage='Pre-sowing', defaults={'text': 'Deep summer ploughing is recommended to expose pests.'})
        BestPractice.objects.get_or_create(crop=soybean, stage='Vegetative', defaults={'text': 'Monitor for whitefly infestation. Avoid waterlogging.'})

        # 3. Farm & Fields
        # Nizamabad coordinates roughly: 18.67, 78.10
        farm, _ = Farm.objects.get_or_create(
            user=user,
            name='Ramesh Family Farm',
            defaults={
                'village': 'Armoor',
                'district': 'Nizamabad',
                'state': 'Telangana',
                'location': {"type": "Point", "coordinates": [78.10, 18.67]},
                'area_acres': 12.5,
                'soil_type': 'Black Cotton',
                'irrigation_source': 'Borewell',
                'elevation': 395.0
            }
        )
        farm.primary_crops.set([paddy, soybean])

        field1, _ = Field.objects.get_or_create(farm=farm, name='North Plot', defaults={'area': 7.5, 'current_crop': paddy})
        field2, _ = Field.objects.get_or_create(farm=farm, name='South Plot', defaults={'area': 5.0, 'current_crop': soybean})

        # 4. Climate Data (Current Season: Kharif 2030)
        LocationClimateIndex.objects.update_or_create(
            farm=farm, season='Kharif', year=2030,
            defaults={
                'district': 'Nizamabad',
                'rainfall_outlook_pct': -15.5,
                'water_stress_score': 7.2,
                'heat_stress_score': 6.5,
                'agri_resilience_score': 6.8,
                'climate_stress_index': 7.0,
                'climate_risk_level': LocationClimateIndex.RiskLevel.HIGH,
                'rainfall_confidence': 85.0,
                'water_stress_confidence': 90.0,
                'heat_stress_confidence': 88.0,
                'agri_resilience_confidence': 80.0,
                'csi_confidence': 85.0,
            }
        )

        # Dummy Polygon for Nizamabad
        multipolygon = {
            "type": "MultiPolygon",
            "coordinates": [[[[77.5, 18.2], [78.5, 18.2], [78.5, 19.0], [77.5, 19.0], [77.5, 18.2]]]]
        }
        ClimateRiskZone.objects.update_or_create(
            district='Nizamabad', risk_level='high', season='Kharif', layer_type='climate_risk',
            defaults={'geometry': multipolygon, 'state': 'Telangana'}
        )

        obs, _ = VegetationObservation.objects.update_or_create(
            farm=farm, date=timezone.now().date(),
            defaults={'ndvi': 0.65, 'lai': 2.8, 'soil_moisture': 55.0, 'lst': 32.5}
        )
        StressAssessment.objects.update_or_create(
            farm=farm, observation=obs,
            defaults={
                'vegetation_stress': 4.5, 'heat_stress': 6.5, 'water_stress': 7.2,
                'climate_stress': 7.0, 'resilience_score': 6.8
            }
        )

        # 5. Future Projections (2030, 2040)
        ClimateProjection.objects.update_or_create(
            farm=farm, scenario='ssp245', decade=2030,
            defaults={'district': 'Nizamabad', 'rainfall_change_pct': -12.0, 'heat_stress_index': 7.5, 'dry_days_change': 15.0, 'soil_moisture_trend': -8.0, 'water_stress_trend': 7.8}
        )
        ClimateProjection.objects.update_or_create(
            farm=farm, scenario='ssp245', decade=2040,
            defaults={'district': 'Nizamabad', 'rainfall_change_pct': -18.5, 'heat_stress_index': 8.2, 'dry_days_change': 22.0, 'soil_moisture_trend': -12.5, 'water_stress_trend': 8.5}
        )

        # 6. Advisory
        CropSuitability.objects.update_or_create(
            crop=paddy, farm=farm, season='Kharif', year=2030,
            defaults={
                'suitability_pct': 65.0, 'recommendation_label': 'Moderate Risk',
                'expected_yield_min': 45.0, 'expected_yield_max': 55.0,
                'risk_level': 'high', 'reasons': json.dumps(['High water stress expected', 'Delay in monsoon'])
            }
        )
        CropSuitability.objects.update_or_create(
            crop=soybean, farm=farm, season='Kharif', year=2030,
            defaults={
                'suitability_pct': 85.0, 'recommendation_label': 'Highly Suitable',
                'expected_yield_min': 18.0, 'expected_yield_max': 24.0,
                'risk_level': 'low', 'reasons': json.dumps(['Drought tolerant', 'Matches rainfall pattern'])
            }
        )

        CropSuitabilityTrend.objects.update_or_create(
            crop=paddy, farm=farm, scenario='ssp245', year=2030, defaults={'suitability_pct': 65.0}
        )
        CropSuitabilityTrend.objects.update_or_create(
            crop=paddy, farm=farm, scenario='ssp245', year=2040, defaults={'suitability_pct': 45.0}
        )

        for i in range(1, 7):
            WaterBalance.objects.update_or_create(
                farm=farm, season='Kharif 2030', month=i,
                defaults={'requirement_mm': 200.0, 'availability_mm': 150.0 + (i*10)}
            )

        IrrigationAdvisory.objects.update_or_create(
            farm=farm, season='Kharif 2030',
            defaults={'recommended_cycles': 5, 'note': 'Reduce irrigation in vegetative stage.', 'next_activity': 'Borewell pump run', 'window': 'Tomorrow 6AM - 9AM'}
        )
        YieldRisk.objects.update_or_create(
            farm=farm, season='Kharif 2030', crop=paddy,
            defaults={'risk_pct': 75.0, 'risk_label': 'high', 'yield_low_pct': -25.0, 'yield_high_pct': -5.0}
        )

        # 7. Alerts
        Alert.objects.update_or_create(
            farm=farm, title='Paddy Suitability Declining',
            defaults={
                'district': 'Nizamabad', 'category': 'strategic', 'severity': 'high',
                'message': 'Long-term models show Paddy will become highly unsuitable by 2035. Consider transitioning to Maize or Soybean.',
                'valid_until': timezone.now() + timedelta(days=365)
            }
        )
        Alert.objects.update_or_create(
            farm=farm, title='Heatwave Warning',
            defaults={
                'district': 'Nizamabad', 'category': 'weather', 'severity': 'medium',
                'message': 'Temperatures expected to exceed 40C next week. Schedule irrigation.',
                'valid_until': timezone.now() + timedelta(days=7)
            }
        )

        self.stdout.write(self.style.SUCCESS('Successfully seeded demo data for Nizamabad!'))
