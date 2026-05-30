#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Applying database migrations..."
python manage.py migrate

# Note: We do not automatically seed demo data here, as it would recreate objects on every deploy.
# To seed demo data on Render, run the command via the Render Shell:
# python manage.py seed_demo_data
