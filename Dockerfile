FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    # build dependencies
    build-essential \
    # PostGIS/GeoDjango dependencies
    binutils \
    libproj-dev \
    gdal-bin \
    libgdal-dev \
    # WeasyPrint dependencies
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libharfbuzz-subset0 \
    libglib2.0-0 \
    libgdk-pixbuf-2.0-0 \
    shared-mime-info \
    # Utilities
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . /app/

# Expose port
EXPOSE 8000

# Set entrypoint
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
