from celery import shared_task
from django.utils import timezone
import random

@shared_task
def generate_alerts_task():
    """
    Scheduled task that runs every minute to generate sample alerts for active farms.
    """
    from apps.farms.models import Farm
    from apps.alerts.models import Alert
    import logging

    logger = logging.getLogger(__name__)
    farms = Farm.objects.all()
    if not farms:
        logger.info("No farms found. Skipping alert generation.")
        return "No farms found."

    # For demo purposes, we randomly pick a farm and generate an alert
    farm = random.choice(list(farms))
    
    categories = ['weather', 'crop', 'water', 'strategic']
    severities = ['info', 'warning', 'critical']
    
    cat = random.choice(categories)
    
    if cat == 'weather':
        title = "Unexpected Rainfall Forecast"
        msg = f"A 20mm rainfall anomaly is predicted for {farm.village} in the next 48 hours."
        sev = random.choice(['info', 'warning'])
    elif cat == 'crop':
        title = "Sowing Window Approaching"
        msg = f"Optimal sowing conditions for Soybean are expected next week based on soil moisture trends."
        sev = 'info'
    elif cat == 'water':
        title = "Water Stress Warning"
        msg = f"Soil moisture has dropped below 30% threshold. Immediate irrigation recommended."
        sev = 'critical'
    else:
        title = "Suitability Decline Alert"
        msg = f"Long-term projection (2035) indicates a 15% drop in Paddy suitability for your region."
        sev = 'warning'
        
    alert = Alert.objects.create(
        farm=farm,
        title=title,
        message=msg,
        category=cat,
        severity=sev,
        created_at=timezone.now()
    )
    
    logger.info(f"Generated alert {alert.id} for Farm {farm.id}")
    return f"Created alert: {title}"

@shared_task
def refresh_climate_data_task():
    """
    Placeholder task for Phase 2 data ingest pipeline.
    """
    import logging
    logger = logging.getLogger(__name__)
    logger.info("Starting nightly climate data refresh from GEE and IMD (Placeholder)...")
    return "Climate data refreshed successfully."
