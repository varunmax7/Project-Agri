#!/usr/bin/env bash
set -o errexit

echo "Applying database migrations..."
python manage.py migrate

echo "Ensuring admin user exists..."
python manage.py ensure_admin

echo "Loading agricultural GeoJSON & CSV data into the database..."
python manage.py load_agri_data

echo "Seeding demo farm data..."
python manage.py seed_demo_data

echo "Starting web server..."
exec gunicorn config.wsgi:application
