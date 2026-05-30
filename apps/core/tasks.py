from celery import shared_task
from django.utils import timezone
import random

@shared_task
def generate_alerts_task():
    """
    Scheduled task that runs every minute to generate sample alerts for active farms.
    """
    # Disabled dummy alert generation as we are now using real data in views.py
    return "Dummy alerts disabled."

@shared_task
def refresh_climate_data_task():
    """
    Placeholder task for Phase 2 data ingest pipeline.
    """
    import logging
    logger = logging.getLogger(__name__)
    logger.info("Starting nightly climate data refresh from GEE and IMD (Placeholder)...")
    return "Climate data refreshed successfully."
