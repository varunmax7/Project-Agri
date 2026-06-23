import os
import json
import csv
import glob
from django.core.management.base import BaseCommand
from apps.climate.models import ClimateRiskZone, DistrictInsight
from apps.cropdata.models import CropSuitability

from django.conf import settings

class Command(BaseCommand):
    help = 'Loads agricultural data (GeoJSON and CSVs) into the database'

    def handle(self, *args, **options):
        data_dir = os.path.join(settings.BASE_DIR, 'data')

        self.stdout.write("Loading GeoJSON files...")
        self.load_geojson(data_dir)

        self.stdout.write("Loading District Insights...")
        self.load_insights(data_dir)

        self.stdout.write("Loading Crop Suitability Data...")
        self.load_crop_suitability(data_dir)

        self.stdout.write(self.style.SUCCESS("Successfully loaded all agricultural data."))

    def load_geojson(self, data_dir):
        geojson_files = glob.glob(os.path.join(data_dir, 'final', 'dashboard', 'frontend_package', 'district_risk_*.geojson'))
        if not geojson_files:
            # Fallback: try alternate location
            geojson_files = glob.glob(os.path.join(data_dir, 'final', 'geojson', 'district_risk_*.geojson'))
        
        self.stdout.write(f"  Found {len(geojson_files)} GeoJSON files.")
        
        for file_path in geojson_files:
            filename = os.path.basename(file_path)
            # filename format: district_risk_ssp245_2030.geojson
            parts = filename.replace('.geojson', '').split('_')
            # parts = ['district', 'risk', 'ssp245', '2030']
            if len(parts) >= 4:
                scenario = parts[2]
                year_str = parts[3]
                year = int(year_str) if year_str.isdigit() else 2030
            else:
                continue

            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                features = data.get('features', [])
                self.stdout.write(f"  Loading {filename}: {len(features)} features (scenario={scenario}, year={year})")
                for feature in features:
                    props = feature.get('properties', {})
                    district = props.get('district', '')
                    state = props.get('state', '')
                    risk_level = props.get('overall_risk_class', 'Unknown')
                    
                    # Store the entire GeoJSON Feature (geometry + properties)
                    geometry = feature 
                    
                    ClimateRiskZone.objects.update_or_create(
                        district=district,
                        scenario=scenario,
                        year=year,
                        defaults={
                            'state': state,
                            'risk_level': risk_level,
                            'geometry': geometry,
                            'layer_type': 'climate_risk',
                        }
                    )

    def load_insights(self, data_dir):
        file_path = os.path.join(data_dir, 'final', 'dashboard', 'frontend_package', 'district_insights.csv')
        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING(f"File not found: {file_path}"))
            return

        with open(file_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                district = row.get('district', '').strip()
                scenario = row.get('scenario', '').strip()
                year = row.get('year', '').strip()
                if not year.isdigit():
                    continue
                year = int(year)
                
                DistrictInsight.objects.update_or_create(
                    district=district,
                    scenario=scenario,
                    year=year,
                    defaults={
                        'key_insight_1': row.get('key_insight_1', ''),
                        'key_insight_2': row.get('key_insight_2', ''),
                        'key_insight_3': row.get('key_insight_3', ''),
                    }
                )
                count += 1
            self.stdout.write(f"  Loaded {count} district insights.")

    def load_crop_suitability(self, data_dir):
        file_path = os.path.join(data_dir, 'crop_suitability_final_output.csv')
        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING(f"File not found: {file_path}"))
            return

        with open(file_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                state = row.get('state', '').strip()
                district = row.get('district', '').strip()
                crop = row.get('crop', '').strip()
                if not state or not district or not crop:
                    continue

                suitability_current = row.get('current_suitability', '').strip()
                # Use ssp245 2040 as projected suitability
                suitability_projected = row.get('suitability_2040_ssp245', '').strip()

                try:
                    change_class = int(float(row.get('ssp245_decline_classes_by_2040', '0')))
                except (ValueError, TypeError):
                    change_class = 0

                recommendation = row.get('recommendation', '').strip()

                # Derive risk_level from change_class
                if change_class >= 3:
                    risk_level = 'Very High Risk'
                elif change_class >= 2:
                    risk_level = 'High Risk'
                elif change_class >= 1:
                    risk_level = 'Moderate Risk'
                else:
                    risk_level = 'Low Risk'

                CropSuitability.objects.update_or_create(
                    state=state,
                    district=district,
                    crop=crop,
                    defaults={
                        'suitability_current': suitability_current,
                        'suitability_projected': suitability_projected,
                        'change_class': change_class,
                        'recommendation': recommendation,
                        'risk_level': risk_level,
                    }
                )
                count += 1
            self.stdout.write(f"  Loaded {count} crop suitability records.")
