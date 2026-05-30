FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    binutils \
    libproj-dev \
    gdal-bin \
    libgdal-dev \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libharfbuzz-subset0 \
    libglib2.0-0 \
    libgdk-pixbuf-2.0-0 \
    shared-mime-info \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . /app/

# Collect static files (uses dummy SECRET_KEY for build only)
RUN SECRET_KEY=build-only-not-used \
    DJANGO_SETTINGS_MODULE=config.settings.prod \
    DATABASE_URL=sqlite:////tmp/build.db \
    python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Startup: migrate then serve
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 120"]
