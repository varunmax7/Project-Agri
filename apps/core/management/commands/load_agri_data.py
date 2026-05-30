import os
import json
import csv
import glob
from django.core.management.base import BaseCommand
from apps.climate.models import ClimateRiskZone, DistrictInsight
from apps.cropdata.models import CropSuitability

class Command(BaseCommand):
    help = 'Loads agricultural data (GeoJSON and CSVs) into the database'

    def handle(self, *args, **options):
        # Base dir is FloodGuard Agri Intelligence 
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
        data_dir = os.path.join(base_dir, 'data')

        self.stdout.write("Loading GeoJSON files...")
        self.load_geojson(data_dir)

        self.stdout.write("Loading District Insights...")
        self.load_insights(data_dir)

        self.stdout.write("Loading Crop Suitability Data...")
        self.load_crop_suitability(data_dir)

        self.stdout.write(self.style.SUCCESS("Successfully loaded all agricultural data."))

    def load_geojson(self, data_dir):
        geojson_files = glob.glob(os.path.join(data_dir, 'final', 'dashboard', 'frontend_package', 'district_risk_*.geojson'))
        
        for file_path in geojson_files:
            filename = os.path.basename(file_path)
            parts = filename.split('_')
            if len(parts) >= 4:
                scenario = parts[2]
                year_str = parts[3].split('.')[0]
                year = int(year_str) if year_str.isdigit() else 2030
            else:
                continue

            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                features = data.get('features', [])
                for feature in features:
                    props = feature.get('properties', {})
                    district = props.get('district', '')
                    state = props.get('state', '')
                    risk_level = props.get('overall_risk_class', 'Unknown')
                    
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

        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                district = row.get('district', '')
                scenario = row.get('scenario', '')
                year = row.get('year', '')
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

    def load_crop_suitability(self, data_dir):
        file_path = os.path.join(data_dir, 'crop_suitability_final_output.csv')
        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING(f"File not found: {file_path}"))
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            try:
                headers = next(reader)
            except StopIteration:
                return
            for row in reader:
                if len(row) < 20:
                    continue
                state = row[0]
                district = row[1]
                crop = row[2]
                suitability_current = row[8]
                suitability_projected = row[14]
                try:
                    change_class = int(row[16]) if row[16].lstrip('-').isdigit() else 0
                except (ValueError, IndexError):
                    change_class = 0
                
                recommendation = row[19] if len(row) > 19 else ''

                CropSuitability.objects.update_or_create(
                    state=state,
                    district=district,
                    crop=crop,
                    defaults={
                        'suitability_current': suitability_current,
                        'suitability_projected': suitability_projected,
                        'change_class': change_class,
                        'recommendation': recommendation,
                    }
                )
