<div align="center">

# FloodGuard Agri Intelligence

### Climate-Smart Agricultural Decision Platform

**Empowering farmers with AI-driven climate risk analysis, crop suitability forecasting, and long-term agricultural resilience planning for 2030-2040.**

[![Django](https://img.shields.io/badge/Django-5.x-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.15-red?style=for-the-badge&logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PostGIS](https://img.shields.io/badge/PostGIS-16-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgis.net/)
[![Celery](https://img.shields.io/badge/Celery-5.4-37814A?style=for-the-badge&logo=celery&logoColor=white)](https://docs.celeryq.dev/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

---

FloodGuard is not a weather app. It is a future-driven farm planning platform that translates CMIP6 climate projections, satellite imagery, and machine learning models into actionable, farm-level decisions for Indian farmers, Farmer Producer Organizations (FPOs), and agricultural institutions.

</div>

---

## Table of Contents

1. [Problem Statement](#1-problem-statement)
2. [Solution Overview](#2-solution-overview)
3. [System Architecture](#3-system-architecture)
4. [Technology Stack](#4-technology-stack)
5. [Project Structure](#5-project-structure)
6. [Django Applications](#6-django-applications)
7. [Platform Modules (14 Total)](#7-platform-modules)
   - [7.1 Dashboard](#71-dashboard)
   - [7.2 My Farm](#72-my-farm)
   - [7.3 Weather and Climate](#73-weather-and-climate)
   - [7.4 District Outlook](#74-district-outlook)
   - [7.5 Crop Advisory](#75-crop-advisory)
   - [7.6 Water Management](#76-water-management)
   - [7.7 Future Outlook 2030-2040](#77-future-outlook-2030-2040)
   - [7.8 Interactive Map](#78-interactive-map)
   - [7.9 Parcel Inspector](#79-parcel-inspector)
   - [7.10 Alerts and Notifications](#710-alerts-and-notifications)
   - [7.11 Market Insights](#711-market-insights)
   - [7.12 Reports](#712-reports)
   - [7.13 Help and Support](#713-help-and-support)
   - [7.14 Settings](#714-settings)
8. [Database Schema](#8-database-schema)
9. [REST API Reference](#9-rest-api-reference)
10. [Data Sources and Pipeline](#10-data-sources-and-pipeline)
11. [Machine Learning Models](#11-machine-learning-models)
12. [Satellite Remote Sensing Pipeline](#12-satellite-remote-sensing-pipeline)
13. [External API Integrations](#13-external-api-integrations)
14. [Authentication and Security](#14-authentication-and-security)
15. [Configuration Reference](#15-configuration-reference)
16. [Getting Started](#16-getting-started)
17. [Docker Deployment](#17-docker-deployment)
18. [Cloud Deployment](#18-cloud-deployment)
19. [Celery Task Queue](#19-celery-task-queue)
20. [Testing](#20-testing)
21. [Performance Considerations](#21-performance-considerations)
22. [Troubleshooting](#22-troubleshooting)
23. [Future Roadmap and Impact](#23-future-roadmap-and-impact)
24. [Glossary](#24-glossary)
25. [Contributing](#25-contributing)
26. [License](#26-license)

---

## 1. Problem Statement

Indian agriculture is confronting a convergence of climate-related threats that traditional farming knowledge alone cannot address. The following table summarizes the scale of the challenge:

| Threat Category | Quantified Impact | Source |
|----------------|-------------------|--------|
| Flood-related crop losses | Over INR 15,000 crore lost annually; 40+ million hectares of cropland classified as flood-prone | National Disaster Management Authority |
| Rising temperatures | Heat stress days projected to increase 30-60% by 2040 under the SSP5-8.5 scenario | IPCC AR6, CMIP6 ensemble |
| Water stress | 54% of India faces high-to-extreme water stress; groundwater depletion rates accelerating in 21 major aquifer systems | NITI Aayog Composite Water Management Index |
| Crop suitability shift | Staple crops such as paddy and wheat face declining suitability in traditional growing regions by 2035 | Indian Council of Agricultural Research projections |
| Yield unpredictability | Climate volatility has increased inter-annual yield variance by 15-30% over the past two decades | Ministry of Agriculture annual reports |
| Financial vulnerability | 52% of agricultural households are indebted; absence of forward-looking climate data prevents informed investment | NABARD All India Rural Financial Inclusion Survey |

**The fundamental gap**: Complex CMIP6 climate projections exist but remain inaccessible to the 150+ million farming households that need them most. No existing platform translates these projections into farm-level, crop-specific, actionable intelligence spanning the 2030-2040 planning horizon.

**What farmers need to know, but currently cannot answer**:
- Will my current crop still be viable in 2035?
- Should I transition to drought-resistant varieties now or wait?
- How much additional irrigation will I need as temperatures rise?
- What is the flood and drought risk trajectory for my district?
- Which crops should I adopt to maintain profitability under changing climate?

FloodGuard Agri Intelligence was built to answer these questions with data, not speculation.

---

## 2. Solution Overview

FloodGuard bridges the gap between climate science and farm-level action through a multi-layered intelligence pipeline:

```
  INPUT LAYER                    PROCESSING LAYER               OUTPUT LAYER
  ───────────                    ────────────────               ────────────

  CMIP6 Climate Models           Multi-Hazard Risk              Dashboard
  (SSP2-4.5, SSP5-8.5)    ──>   Scoring Engine          ──>   (5 index cards,
  Temperature, Rainfall,         - Flood Hazard Score           choropleth map,
  Dry Days, Wind Speed           - Drought Hazard Score         recommended crops)
                                 - Ag Stress Score
  Sentinel-2 L2A Imagery   ──>  - Overall Risk Class    ──>   Crop Advisory
  (via Microsoft Planetary       - Confidence Scoring          (suitability ranking,
  Computer STAC API)                                            comparison, calendar)
  NDVI, NDWI, LAI, LST
                                 ML Prediction Models    ──>   Future Outlook
  ISRIC SoilGrids v2.0    ──>   - RandomForest (NDVI)         (2030/2035/2040
  pH, Clay, Sand, Silt,          - XGBoost (Soil Moist.)       scenario analysis)
  SOC, CEC, Nitrogen             - Proxy Models (ET,
                                   LAI, PET, Solar)     ──>   Water Management
  Open-Meteo APIs          ──>                                 (irrigation scheduling,
  Current Weather, Archive,      Crop Suitability              stress trends)
  Elevation Data                 Classification Engine
                                 - Current vs Projected  ──>   Interactive Maps
  OpenStreetMap Nominatim  ──>   - Transition Planning         (choropleth risk zones,
  Reverse Geocoding              - Decline Class Analysis       district click-through)

  Historical Crop Data     ──>   Water Balance Engine    ──>   Alerts System
  District Major Crops,          - Requirement vs               (strategic + operational
  Area Under Cultivation          Availability                  alerts with severity)
                                 - Irrigation Scheduling
                                                         ──>   PDF Reports
                                                               (institutional-grade
                                                                climate reports)
```

The platform serves three distinct user roles with tailored access:

| Role | Primary Use Case | Key Screens |
|------|-----------------|-------------|
| **Farmer** | "What should I grow? When should I irrigate? Will my crop still work in 2035?" | Dashboard, My Farm, Crop Advisory, Water Management, Alerts |
| **FPO (Farmer Producer Organization)** | District-level planning, bulk advisory, transition management across member farms | District Outlook, Interactive Map, Reports, Market Insights |
| **Administrator / Researcher** | Policy planning, climate vulnerability mapping, agricultural resilience benchmarking | All modules with administrative data access |

---

## 3. System Architecture

The application follows an API-first architecture. The same backend serves the current web dashboard and is designed to support future mobile clients without modification.

```
+------------------------------------------------------------------+
|                        CLIENT LAYER                               |
|                                                                   |
|  +------------------+  +------------------+  +------------------+ |
|  | Django Templates |  | Leaflet.js Maps  |  | Chart.js /       | |
|  | + Alpine.js      |  | + GeoJSON        |  | ApexCharts       | |
|  | + Tailwind CSS   |  | Choropleths      |  | Visualizations   | |
|  +--------+---------+  +--------+---------+  +--------+---------+ |
|           |                      |                      |         |
+-----------+----------------------+----------------------+---------+
            |                      |                      |
            v                      v                      v
+------------------------------------------------------------------+
|                    API LAYER (Django REST Framework)               |
|                                                                   |
|  Endpoint Group         Router / Path            ViewSet          |
|  ---------------------------------------------------------------  |
|  Authentication         /api/v1/accounts/        RegisterView     |
|                                                  TokenObtain/     |
|                                                  TokenRefresh     |
|                                                                   |
|  Farms                  /api/v1/farms/           FarmViewSet      |
|    Dashboard action     /api/v1/farms/{id}/dashboard/             |
|    NDVI Timeseries      /api/v1/farms/api/stac-ndvi/             |
|    Parcel Details       /api/v1/farms/api/parcel-details/        |
|                                                                   |
|  Crop Catalogue         /api/v1/crops/           CropViewSet     |
|                                                                   |
|  Climate                /api/v1/climate/indices/                  |
|                         /api/v1/climate/risk-zones/               |
|                         /api/v1/climate/vegetation/               |
|                         /api/v1/climate/stress/                   |
|                         /api/v1/climate/projections/              |
|                                                                   |
|  Advisory               /api/v1/advisory/suitability/            |
|                         /api/v1/advisory/suitability-trends/     |
|                         /api/v1/advisory/water-balance/          |
|                         /api/v1/advisory/irrigation/             |
|                         /api/v1/advisory/yield-risk/             |
|                                                                   |
|  Alerts                 /api/v1/alerts/          AlertViewSet    |
|  Reports                /api/v1/reports/         ReportViewSet   |
|                                                                   |
|  Map Data (public)      /api/map-data/risk/                      |
|                         /api/map-data/suitability/               |
|                         /api/map-data/insights/                  |
|                                                                   |
|  Schema / Docs          /api/schema/             (OpenAPI 3.0)   |
|                         /api/docs/               (Swagger UI)    |
|                         /api/redoc/              (ReDoc)         |
+------------------------------------------------------------------+
            |
            v
+------------------------------------------------------------------+
|                    APPLICATION LAYER (8 Django Apps)               |
|                                                                   |
|  accounts:   User, FarmerProfile                                  |
|  farms:      Farm, Field, ActivityLog                             |
|  cropdata:   Crop, CropCalendar, BestPractice, CropSuitability   |
|  climate:    LocationClimateIndex, ClimateRiskZone,               |
|              VegetationObservation, StressAssessment,             |
|              ClimateProjection, DistrictInsight                   |
|  advisory:   CropSuitability, CropSuitabilityTrend,              |
|              WaterBalance, IrrigationAdvisory, YieldRisk          |
|  alerts:     Alert                                                |
|  reports:    Report                                               |
|  core:       Template views, map API endpoints, auth views        |
+------------------------------------------------------------------+
            |
            v
+------------------------------------------------------------------+
|                  DATA AND INFRASTRUCTURE LAYER                    |
|                                                                   |
|  +--------------+  +----------+  +-----------+  +--------------+ |
|  | PostgreSQL   |  | Redis    |  | Celery    |  | Sentinel-2   | |
|  | + PostGIS    |  | Cache /  |  | Workers / |  | STAC API     | |
|  |              |  | Broker   |  | Beat      |  | Pipeline     | |
|  +--------------+  +----------+  +-----------+  +--------------+ |
|                                                                   |
|  +------------------------------------------------------------+  |
|  | External APIs (all free-tier, no API keys required)         |  |
|  | - Open-Meteo: weather, forecast, archive, elevation         |  |
|  | - OpenStreetMap Nominatim: reverse geocoding                |  |
|  | - ISRIC SoilGrids v2.0: topsoil properties at 250m         |  |
|  | - Microsoft Planetary Computer: Sentinel-2 L2A via STAC    |  |
|  +------------------------------------------------------------+  |
+------------------------------------------------------------------+
```

---

## 4. Technology Stack

### 4.1 Backend

| Technology | Version | Role in the System |
|-----------|---------|-------------------|
| Django | 5.x | Web framework, ORM, admin interface, template engine, URL routing |
| Django REST Framework | 3.15+ | RESTful API construction with serializers, viewsets, routers, and browsable API |
| drf-spectacular | 0.27+ | Automatic OpenAPI 3.0 schema generation with Swagger UI and ReDoc rendering |
| djangorestframework-simplejwt | 5.3+ | JWT-based authentication with configurable access (1 hour) and refresh (7 day) token lifetimes |
| PostgreSQL + PostGIS | 16 | Spatial-capable relational database for GeoJSON geometry storage and geospatial queries |
| Celery | 5.4+ | Distributed task queue for asynchronous job execution (alert generation, data refresh) |
| django-celery-beat | 2.6+ | Periodic task scheduling with database-backed schedule storage |
| Redis | 7.x | Message broker for Celery, result backend, and application-level caching |
| WeasyPrint | 62+ | HTML-to-PDF conversion for generating institutional-grade climate reports |
| Gunicorn | 22+ | Production WSGI HTTP server with configurable worker processes |
| WhiteNoise | 6.6+ | Static file serving middleware with compression and cache header management |
| Sentry SDK | 2.0+ | Error monitoring, performance tracing, and exception aggregation in production |
| django-environ | 0.11+ | Environment variable parsing with type casting and .env file support |
| django-cors-headers | 4.3+ | Cross-Origin Resource Sharing (CORS) header management for API consumers |
| django-debug-toolbar | 4.3+ | Development-only SQL query inspection and request profiling |
| django-extensions | 3.2+ | Management command utilities, shell_plus, and model visualization |
| Pillow | 10.3+ | Image processing for user-uploaded media and report generation |
| psycopg2-binary | 2.9+ | PostgreSQL database adapter for Python |

### 4.2 Geospatial and Remote Sensing

| Technology | Role in the System |
|-----------|-------------------|
| pystac-client | STAC API client for searching satellite image catalogs (Sentinel-2 collections) |
| planetary-computer | Microsoft Planetary Computer authentication; signs asset URLs with short-lived SAS tokens |
| rasterio | Geospatial raster I/O; performs windowed reads of Cloud-Optimized GeoTIFFs (COGs) for band extraction |
| rioxarray | Integration layer between xarray and rasterio for multi-band raster analysis |
| odc-stac | Open Data Cube STAC integration for loading satellite data into xarray datasets |
| GeoPandas | GeoDataFrame operations on district boundary polygons, spatial joins, and area calculations |
| Shapely | Computational geometry operations including polygon intersection, buffering, and centroid computation |

### 4.3 Frontend

| Technology | Role in the System |
|-----------|-------------------|
| Django Templates | Server-side rendered HTML with template inheritance, component includes, and custom template tags |
| Tailwind CSS | Utility-first CSS framework providing responsive design, dark mode support, and consistent spacing |
| Alpine.js | Lightweight (15KB) reactive JavaScript framework for tabs, dropdowns, async data loading, and conditional rendering |
| Leaflet.js | Interactive map rendering with tile layers, GeoJSON choropleth overlays, popups, and layer control |
| Leaflet Draw | Drawing tools for polygon creation in the Parcel Inspector module |
| Chart.js | Client-side charting library for line charts, bar charts, donut charts, and gauge visualizations |

### 4.4 DevOps and Deployment

| Technology | Role in the System |
|-----------|-------------------|
| Docker | Containerized application builds using Python 3.12-slim base image with GDAL/PROJ system dependencies |
| Docker Compose | Multi-service orchestration: web server, PostgreSQL/PostGIS, Redis, and Celery worker containers |
| Nginx | Production reverse proxy with static file serving, SSL termination, and request buffering |
| Render | Cloud PaaS deployment with render.yaml Blueprint for one-click infrastructure provisioning |
| Vercel | Serverless deployment option with vercel.json configuration and build script |

---

## 5. Project Structure

```
floodguard-agri-intelligence/
|
|-- config/                          # Django project configuration
|   |-- __init__.py
|   |-- asgi.py                      # ASGI application entry point
|   |-- celery.py                    # Celery application configuration
|   |-- urls.py                      # Root URL configuration (all app routers)
|   |-- wsgi.py                      # WSGI application entry point
|   +-- settings/
|       |-- __init__.py
|       |-- base.py                  # Shared settings (apps, middleware, DRF, JWT, Celery)
|       |-- dev.py                   # Development overrides (DEBUG=True, debug toolbar)
|       +-- prod.py                  # Production overrides (SSL, Sentry, CSRF origins)
|
|-- apps/                            # Django application modules
|   |-- accounts/                    # User authentication and profiles
|   |-- advisory/                    # Crop suitability, water balance, irrigation, yield risk
|   |-- alerts/                      # Alert management with categories and severity
|   |-- climate/                     # Climate indices, risk zones, projections, vegetation
|   |-- core/                        # Template views, map API endpoints, auth views, template tags
|   |-- cropdata/                    # Crop catalogue, calendars, best practices, suitability data
|   |-- farms/                       # Farm/field management, dashboard aggregation, parcel inspector
|   +-- reports/                     # PDF report generation and file management
|
|-- templates/                       # Django HTML templates
|   |-- base.html                    # Master layout (sidebar, top bar, content area)
|   |-- auth/                        # Login, register, logout pages
|   |-- components/                  # Reusable UI components (metric cards, gauges, tables)
|   |-- farms/                       # Farm-specific templates (parcel inspector)
|   |-- pages/                       # 13 module page templates
|   +-- reports/                     # PDF report HTML templates
|
|-- static/
|   +-- css/                         # Custom stylesheets and Tailwind output
|
|-- data/                            # Pre-computed datasets and ML model artifacts
|   |-- crop_suitability_final_output.csv    # Master suitability matrix (500+ records)
|   |-- dashboard/                   # District risk data for dashboard rendering
|   |-- evaluation/                  # ML model evaluation metrics and feature importance
|   |-- features/                    # Training feature datasets (Parquet format)
|   |-- final/                       # Production-ready outputs
|   |   |-- advanced/               # Advanced analytics datasets
|   |   |-- dashboard/              # Frontend-ready dashboard packages
|   |   |-- geojson/                # Simplified GeoJSON for web maps (6 files)
|   |   |-- gis/                    # Full GIS outputs: Shapefile, GeoJSON, GeoPackage (42 files)
|   |   |-- insights/              # District insights and risk driver analysis
|   |   |-- rankings/              # Risk rankings and state summaries
|   |   |-- reports/               # Risk change and state summary reports
|   |   +-- trends/                # District trend analysis
|   |-- models/                      # Trained ML model artifacts (.pkl files)
|   |-- projections/                 # Future climate projections (SSP2-4.5, SSP5-8.5)
|   |-- risk/                        # Multi-hazard district risk scores
|   +-- validation/                  # Model validation results and confidence scores
|
|-- scripts/                         # Operational scripts
|   |-- stac_pipeline.py             # Sentinel-2 NDVI extraction via STAC API
|   +-- backup.sh                    # Database backup script
|
|-- media/                           # User-uploaded files and generated reports
|-- nginx/                           # Nginx configuration for production
|-- requirements/                    # Split requirements files
|-- requirements.txt                 # Unified Python dependencies
|-- Dockerfile                       # Container build specification
|-- docker-compose.yml               # Development multi-service orchestration
|-- docker-compose.prod.yml          # Production multi-service orchestration
|-- render.yaml                      # Render PaaS deployment Blueprint
|-- vercel.json                      # Vercel serverless deployment configuration
|-- build.sh                         # Build script (pip install + collectstatic)
|-- build_vercel.sh                  # Vercel-specific build script
|-- start.sh                         # Production startup script (migrate + gunicorn)
|-- manage.py                        # Django management command entry point
+-- db.sqlite3                       # SQLite development database (11.7 MB)
```

---

## 6. Django Applications

The codebase is organized into 8 focused Django applications. Each application owns its models, serializers, views, URLs, and admin registrations.

### 6.1 accounts

Handles user authentication, registration, and profile management.

**Models:**
- `User` (extends `AbstractUser`): Adds a `role` field with choices: FARMER, FPO, ADMIN.
- `FarmerProfile` (OneToOne to User): Stores phone number, preferred language (English/Hindi/Telugu), and default season preference.

**Authentication backend:** Custom `EmailOrUsernameModelBackend` allows login with either username or email address.

**API endpoints:**
- `POST /api/v1/accounts/register/` -- Create a new user account
- `POST /api/v1/accounts/login/` -- Obtain JWT access and refresh tokens
- `POST /api/v1/accounts/login/refresh/` -- Refresh an expired access token

### 6.2 farms

Central module for farm registration, field management, dashboard data aggregation, and the Parcel Inspector satellite pipeline.

**Models:**
- `Farm`: User FK, name, village, district, state, location (JSON Point geometry), area_acres, soil_type, irrigation_source, elevation, primary_crops (M2M to Crop).
- `Field`: Farm FK, name, area, current_crop FK.
- `ActivityLog`: Farm FK, activity description, date, notes.

**API endpoints:**
- `GET/POST /api/v1/farms/` -- List and create farms
- `GET/PUT/PATCH/DELETE /api/v1/farms/{id}/` -- Retrieve, update, delete a farm
- `GET /api/v1/farms/{id}/dashboard/` -- Aggregated dashboard data (single optimized call)
- `POST /api/v1/farms/api/stac-ndvi/` -- NDVI time series extraction for a polygon
- `POST /api/v1/farms/api/parcel-details/` -- Multi-source parcel intelligence bundle

The dashboard endpoint is the most complex in the system. It combines data from `ClimateRiskZone` GeoJSON properties, `CropSuitability` records, computed water balance, yield risk assessments, vegetation observations, stress assessments, irrigation advisories, and recent alerts into a single JSON response. All metrics are derived dynamically from the district's climate data and are never hardcoded.

### 6.3 cropdata

Crop catalogue and district-level suitability data.

**Models:**
- `Crop`: Name, icon, category, season, water_requirement_mm, temp_min/max, optimal_soil_moisture.
- `CropCalendar`: Crop FK, agro_zone, sowing_start/end dates, vegetative/flowering/harvest stage durations.
- `BestPractice`: Crop FK, growth stage, practice text.
- `CropSuitability`: State, district, crop name, current suitability class, projected suitability class, change_class (integer indicating decline/improvement), risk level, recommendation text.

### 6.4 climate

Climate scoring, geospatial risk zones, satellite observations, and future projections.

**Models:**
- `LocationClimateIndex`: Farm FK, district, season, year, five climate scores (rainfall_outlook_pct, water_stress_score, heat_stress_score, agri_resilience_score, climate_stress_index) each with a confidence value, and overall climate_risk_level.
- `ClimateRiskZone`: GeoJSON Feature dictionary stored as JSONField (geometry + properties), district, state, risk_level, scenario, year, layer_type. This is the primary data source for choropleth maps and dashboard metrics.
- `VegetationObservation`: Farm/Field FK, date, NDVI, LAI, soil_moisture, LST (Land Surface Temperature in degrees Celsius).
- `StressAssessment`: Farm FK, linked VegetationObservation, individual stress scores (vegetation, heat, water, climate) and resilience_score.
- `ClimateProjection`: Farm FK, district, SSP scenario, decade (2030/2035/2040), rainfall_change_pct, heat_stress_index, dry_days_change, soil_moisture_trend, water_stress_trend.
- `DistrictInsight`: District, scenario, year, three key insight text fields for AI-generated strategic intelligence.

**API endpoints:**
- `GET /api/v1/climate/indices/` -- Climate indices with farm, season, year filters
- `GET /api/v1/climate/risk-zones/` -- Risk zone records with season and layer_type filters
- `GET /api/v1/climate/risk-zones/geojson/` -- GeoJSON FeatureCollection format
- `GET /api/v1/climate/vegetation/` -- Vegetation observations with farm filter
- `GET /api/v1/climate/stress/` -- Stress assessments with farm filter
- `GET /api/v1/climate/projections/` -- Future projections with farm and scenario filters

### 6.5 advisory

Crop recommendation engine, water balance tracking, irrigation scheduling, and yield risk assessment.

**Models:**
- `CropSuitability` (advisory): Crop FK, Farm FK, season, year, suitability_pct, recommendation_label, expected_yield_min/max (q/ha), risk_level, reasons (JSON array).
- `CropSuitabilityTrend`: Crop FK, Farm FK, scenario, year, suitability_pct. Tracks how crop suitability evolves over time under different climate scenarios.
- `WaterBalance`: Farm FK, season, month, requirement_mm, availability_mm. Monthly water demand versus supply.
- `IrrigationAdvisory`: Farm FK, season, recommended_cycles, note, next_activity, scheduling window, creation timestamp.
- `YieldRisk`: Farm FK, season, Crop FK, risk_pct, risk_label (Low/Medium/High), yield_low_pct, yield_high_pct.

**API endpoints:**
- `GET /api/v1/advisory/suitability/` -- Crop suitability rankings
- `GET /api/v1/advisory/suitability-trends/` -- Suitability evolution across years
- `GET /api/v1/advisory/water-balance/` -- Monthly water requirement vs availability
- `GET /api/v1/advisory/irrigation/` -- Irrigation scheduling advisories
- `GET /api/v1/advisory/yield-risk/` -- Yield risk assessments per crop

### 6.6 alerts

Alert management with categorical filtering and severity classification.

**Models:**
- `Alert`: Farm FK, district, category (weather/crop/advisory/strategic), severity (low/medium/high), title, message, created_at, valid_until, is_read boolean.

Strategic alerts are the platform's distinguishing alert type. Examples: "Paddy suitability declining after 2032 -- consider transitioning to millets" or "Drought hazard score exceeding 60 for your district under SSP5-8.5 by 2035."

### 6.7 reports

PDF report generation and file management for institutional use.

**Models:**
- `Report`: Farm FK, type (Village Climate Report / Farm Climate Report / Risk Indicator Report), period, generated_file (FileField), created_at.

Reports are generated using WeasyPrint, which converts styled HTML report templates into downloadable PDF files. Each report bundles data from climate indices, crop suitability, water balance, and future projections.

### 6.8 core

Template rendering views and shared infrastructure. This app does not define its own models but provides:

- `ModuleView` base class: Injects active_module, page_title, page_subtitle, user_farms, current_farm, and unread_alert_count into every template context.
- 14 template views (one per sidebar module), each extending ModuleView.
- 3 map data API endpoints for the Interactive Map module.
- Authentication views (login, logout, register) with session-based auth for the web UI.
- Custom template tags (`floodguard_tags`).

---

## 7. Platform Modules

The platform consists of 14 modules accessible from the left sidebar navigation. Each module is described below with its purpose, displayed information, data sources, and technical implementation.

### 7.1 Dashboard

**Purpose**: Central command center providing an at-a-glance overview of a farm's climate health and agricultural outlook.

**Template**: `templates/pages/dashboard.html`
**View**: `DashboardView` (extends ModuleView)
**Data Source**: `GET /api/v1/farms/{id}/dashboard/` (aggregated endpoint)

**Displayed Components:**

1. **Five Climate Index Cards**: Rainfall Outlook (percentage), Water Stress Score, Heat Stress Score, Agricultural Resilience Score, and Climate Stress Index. Each card displays the metric value, confidence level (derived from model accuracy), and a directional trend indicator (up/down/stable).

2. **Climate Risk Map**: An interactive Leaflet.js choropleth map rendering district-level risk zones. The map supports four layer types via a dropdown switcher: Climate Risk, Rainfall Anomaly, Heat Stress, and Water Stress. GeoJSON FeatureCollections are fetched from `/api/map-data/risk/` with scenario and year parameters.

3. **Recommended Crops Table**: Top 6 crops ranked by suitability percentage for the selected scenario and year. Each row shows the crop name, suitability bar, and risk-level badge (Low/Moderate/High).

4. **Water Requirement vs Availability Chart**: Chart.js bar chart comparing monthly (June through October) crop water demand against projected availability. Water demand is adjusted dynamically based on temperature change projections.

5. **Yield Risk Donut**: Chart.js donut visualization showing yield risk probability distribution.

6. **Future Outlook Suitability Strip**: Horizontal strip showing suitability percentage trends across 2030, 2035, and 2040 for the top 3 recommended crops.

7. **Climate Projections Chart**: Line chart plotting rainfall change, heat stress index, and water stress trends across the three projection decades.

8. **Active Alerts Feed**: Latest 5 unread alerts with severity badges and the total unread count displayed in the navigation bell icon.

**Technical implementation detail**: The dashboard endpoint in `FarmViewSet.dashboard()` performs the following operations:
- Queries `ClimateRiskZone` for the farm's district, matching scenario and year.
- Extracts properties from the GeoJSON Feature dictionary (rainfall_change, drought_hazard_score, temperature_change, ag_stress_score, overall_risk_score, climate_confidence_score).
- Derives all five climate indices from these properties using formulaic transformations (not raw lookups).
- Queries `CropSuitability` records for the district and interpolates suitability percentages across decades.
- Computes water balance projections using temperature change and rainfall change to adjust crop water demand dynamically.
- Generates vegetation observations (NDVI, soil moisture, LST) from climate risk properties.
- Produces stress assessments with labeled severity levels.
- Creates irrigation advisories adjusted for drought risk.

### 7.2 My Farm

**Purpose**: Farm registration, field management, and current field condition monitoring.

**Template**: `templates/pages/myfarm.html`
**View**: `MyFarmView` (extends ModuleView)

**Displayed Components:**

1. **Farm Header**: Name, village, district, state, area in acres, soil type, irrigation source, elevation in meters, and linked primary crops.

2. **Five Tabbed Sections**:
   - **Overview**: Farm summary with location coordinates, area breakdown, current season status, and last activity date.
   - **Field Summary**: Individual field cards showing field name, area, assigned crop, and field-level vegetation metrics (NDVI, Soil Moisture, NDWI, LST).
   - **Soil and Water**: Soil type analysis, moisture status bar, water table depth indicator, and soil health assessment.
   - **Irrigation Plan**: Recommended irrigation cycles, next scheduled activity, delivery method advisory (drip/sprinkler versus flood irrigation based on drought risk), and water-saving recommendations.
   - **Activity Log**: Chronological table of all farm activities (sowing, fertilization, pesticide application, harvesting) with dates and notes.

3. **Current Field Condition Cards**: Four metric cards showing real-time NDVI (Vegetation Health Index, 0.0-1.0 scale), Soil Moisture (percentage), NDWI (Water Index), and LST (Land Surface Temperature in degrees Celsius).

### 7.3 Weather and Climate

**Purpose**: Real-time weather conditions and historical climate summary for the farm's geographic location.

**Template**: `templates/pages/weather.html`
**View**: `WeatherView` (extends ModuleView)

**Displayed Components:**

1. **Current Conditions Panel**: Temperature, apparent temperature, relative humidity, wind speed and direction, wind gusts, precipitation, cloud cover, surface pressure, UV index, and weather code interpretation.

2. **Seven-Day Forecast**: Daily cards showing high/low temperatures, precipitation probability, weather condition icons, and sunrise/sunset times.

3. **Recent Climate Summary (Last 30 Days)**: Aggregated from the Open-Meteo Archive API:
   - Total precipitation in mm
   - Number of rainy days (precipitation greater than 1.0 mm)
   - Maximum single-day rainfall
   - Average and peak maximum temperature
   - Average ET0 (reference evapotranspiration) and total ET0
   - Water balance (precipitation minus evapotranspiration)

**Data sources**: All weather data comes from the Open-Meteo API ecosystem. Current conditions and forecast from the Forecast API; historical observations from the Archive API. No API keys are required.

### 7.4 District Outlook

**Purpose**: Evidence-based crop transition planning across any district in the dataset. This module enables FPOs and administrators to analyze how crop suitability will shift across entire districts under different climate scenarios.

**Template**: `templates/pages/district_outlook.html`
**View**: `DistrictOutlookView` (extends ModuleView)

**Displayed Components:**

1. **Filter Controls**: Four dropdown selectors for State, District, Scenario (SSP2-4.5, SSP5-8.5), and Year (2030, 2035, 2040). State and district dropdowns are cascaded -- selecting a state filters the available districts.

2. **District Climate Metrics Panel**: Eight key metrics for the selected district, scenario, and year:
   - Overall Risk Score and Risk Class
   - Flood Hazard Score and Class
   - Drought Hazard Score and Class
   - Agricultural Stress Score and Class
   - Temperature Change (degrees Celsius)
   - Rainfall Change (percentage)
   - Water Availability Index
   - Heat Stress Days

3. **Crop Suitability Cards**: One card per crop in the district showing:
   - Current suitability class (e.g., "Highly Suitable", "Suitable", "Moderately Suitable", "Marginal")
   - Future projected suitability class for the selected scenario and year
   - Number of decline classes (integer indicating how many levels the suitability drops)
   - Recommendation text (e.g., "Consider transitioning to drought-resistant varieties")
   - Explanation text (scenario-specific reasoning for the change)
   - Historical crop analysis
   - Soil type and Length of Growing Period (days)

4. **Major Crop Analysis**: The district's dominant crop, its cultivated area (in 1000 hectares), and detailed historical analysis text.

**Data source**: The master CSV file `data/crop_suitability_final_output.csv` contains 500+ district-by-crop combinations. Each row has scenario-specific columns for every metric (e.g., `overall_risk_score_2040_ssp245`, `suitability_2035_ssp585`, `ssp245_2040_explanation`). The view dynamically constructs column names based on selected filters and reads the appropriate values.

**Technical implementation**: The view builds a state-to-districts mapping from the CSV at render time, serializes it to JSON for the cascading JavaScript dropdowns, filters rows for the selected district, and constructs crop cards with the correctly prefixed column lookups.

### 7.5 Crop Advisory

**Purpose**: Comprehensive crop recommendation engine with suitability analysis, comparison tools, growth calendars, and farming best practices.

**Template**: `templates/pages/crop_advisory.html`
**View**: `CropAdvisoryView` (extends ModuleView)

**Displayed Components:**

1. **Suitability Ranking List**: All crops ranked by suitability percentage for the current location, season, and climate scenario. Each entry shows crop name, suitability bar chart, recommendation label, and risk badge.

2. **Crop Suitability Map**: Per-crop Leaflet choropleth showing suitability distribution across all districts. Layer data fetched from `/api/map-data/suitability/?crop={name}`.

3. **Four Analysis Tabs**:
   - **Suitability**: Detailed breakdown with recommendation labels (Highly Suitable / Suitable / Moderately Suitable / Marginal / Not Suitable) and explanatory reasons.
   - **Comparison**: Side-by-side comparison table of current versus projected suitability for multiple crops.
   - **Calendar**: Crop calendar visualization showing sowing, vegetative, flowering, and harvest windows per agro-zone (data from `CropCalendar` model).
   - **Best Practices**: Stage-by-stage farming best practices for each crop (data from `BestPractice` model).

4. **Suitability Reason Cards**: For each recommended crop, a set of reason cards explaining why it is suitable (soil compatibility, water availability, temperature range match, risk level assessment).

5. **Expected Yield Range**: Minimum and maximum yield estimates in quintals per hectare with risk classification overlay.

### 7.6 Water Management

**Purpose**: Water-focused module for monitoring soil moisture, tracking drought stress, and optimizing irrigation scheduling.

**Template**: `templates/pages/water_management.html`
**View**: `WaterManagementView` (extends ModuleView)

**Displayed Components:**

1. **Soil Moisture Status**: Current soil moisture percentage with a status indicator bar (Adequate / Deficit / Critical).

2. **Water Stress Trend**: Time-series chart showing drought hazard score evolution across projection years and scenarios.

3. **Water Requirement vs Availability Chart**: Monthly comparison bar chart (June through October) showing:
   - Crop water demand (adjusted for temperature change projections)
   - Projected water availability (adjusted for rainfall change projections)
   - Surplus or deficit indication per month

4. **Irrigation Scheduling Advisory**: Actionable irrigation recommendations including:
   - Recommended number of irrigation cycles per season
   - Next irrigation date and recommended amount in mm
   - Delivery method recommendation (drip/sprinkler for high drought risk districts; flood irrigation for low risk)
   - Scheduling window (e.g., "Jul 10 - Jul 15")
   - Next activity description
   - Free-text advisory notes adjusted for projected drought risk levels

### 7.7 Future Outlook 2030-2040

**Purpose**: This is the platform's strongest differentiator. No other agricultural platform in India provides CMIP6-derived, decade-by-decade climate projections at the farm level. This module allows farmers to see how climate change will affect their farming operations in 2030, 2035, and 2040.

**Template**: `templates/pages/future_outlook.html`
**View**: `FutureOutlookView` (extends ModuleView)

**Displayed Components:**

1. **Scenario Selector**: Toggle between SSP2-4.5 (moderate emissions, "middle of the road") and SSP5-8.5 (high emissions, "fossil-fueled development") climate pathways.

2. **Four Analysis Tabs**:
   - **Climate Outlook**: Trend charts for temperature change (degrees Celsius), rainfall change (percentage), dry days change, soil moisture trend, and water stress trend. Each plotted across three decades (2030, 2035, 2040).
   - **Crop Suitability Trend**: Line charts showing how suitability percentages for the top recommended crops shift over the projection decades. Reveals which crops will remain viable and which will decline.
   - **Water Outlook**: Future water availability projections, evapotranspiration trends, drought probability evolution, and irrigation demand forecasts.
   - **Risk Outlook**: Per-decade resilience scores, risk escalation trajectories showing how overall/flood/drought/agricultural risk classes evolve from 2030 to 2040.

3. **Key Strategic Insights**: AI-generated natural language summaries such as:
   - "Paddy suitability declining after 2032 under SSP5-8.5 -- consider transitioning to millets or sorghum"
   - "Drought hazard score exceeding critical threshold by 2035 -- increase water harvesting infrastructure investment"
   - "Temperature increase of 1.8 degrees Celsius by 2040 will extend heat stress days by 45% -- adjust sowing calendar"

4. **Per-Decade Resilience Scores**: Quantified agricultural resilience index for each decade under each scenario, enabling direct comparison of climate pathways.

**Data source**: Pre-computed projection datasets in `data/projections/` (12 files: 2 scenarios x 3 years x 2 formats CSV/Parquet) and `ClimateProjection` model records. The `projection_manifest.json` file indexes all available projection files with metadata.

### 7.8 Interactive Map

**Purpose**: Full-screen interactive map for exploring climate risk and crop suitability patterns across all districts in the dataset.

**Template**: `templates/pages/interactive_map.html`
**View**: `InteractiveMapView` (extends ModuleView)

**Displayed Components:**

1. **Choropleth Risk Map**: District polygons colored by risk severity on a gradient scale (Low: green, Moderate: yellow, High: orange, Very High: red). GeoJSON FeatureCollections served from `/api/map-data/risk/`.

2. **Layer Controls**: Dropdown to switch between overlays: Climate Risk, Rainfall Anomaly, Heat Stress, Water Stress, and Crop Suitability per crop.

3. **Scenario and Year Controls**: Dynamic filters for SSP scenario and projection year (2030, 2035, 2040) that reload the GeoJSON layer.

4. **District Click Details**: Clicking any district polygon opens a popup or side panel with:
   - District name and state
   - All risk scores (overall, flood, drought, agricultural stress)
   - Temperature and rainfall change projections
   - Recommended crops for that district

5. **AI-Generated Insights Panel**: District-specific strategic insights loaded from the `DistrictInsight` model via `/api/map-data/insights/?district={name}&scenario={ssp}&year={year}`. Returns up to three key insight texts.

### 7.9 Parcel Inspector

**Purpose**: Real-time satellite and sensor intelligence tool that allows users to draw a polygon on any agricultural field in India and receive instant, multi-source analysis of that specific parcel.

**Template**: `templates/farms/parcel_inspector.html`
**View**: `parcel_inspector_view` (function-based)

**Displayed Components:**

1. **Draw-to-Analyze Map**: Leaflet map with Leaflet Draw tools. Users draw a polygon around any field to trigger analysis.

2. **NDVI Time Series Chart**: Chart.js line chart showing vegetation health evolution over the last 120 days. Source badge indicates whether data is "Live" (from Sentinel-2) or "Simulated" (from seasonal model).

3. **Five Intelligence Panels** (all fetched in parallel via ThreadPoolExecutor):
   - **Location**: Reverse-geocoded address including village, district, state, country, and postcode. Source: OpenStreetMap Nominatim API.
   - **Weather**: Current conditions (temperature, humidity, wind, precipitation, cloud cover) plus 7-day forecast with daily max/min temperatures, precipitation probability, UV index, sunrise/sunset. Source: Open-Meteo Forecast API.
   - **Climate History**: Last 30 days of observed data: total precipitation, rainy days, max daily rainfall, average/peak max temperature, average ET0, total ET0, average solar radiation, and computed water balance. Source: Open-Meteo Archive API.
   - **Soil Properties**: Topsoil (0-5cm depth) properties: pH, organic carbon (g/kg), clay/sand/silt percentages, bulk density, cation exchange capacity (CEC), nitrogen content, and computed USDA texture classification. Source: ISRIC SoilGrids v2.0 REST API.
   - **Elevation**: Terrain elevation in meters above sea level. Source: Open-Meteo Elevation API.

**Technical implementation detail for the NDVI pipeline:**

The NDVI extraction follows a subprocess isolation pattern to avoid GDAL/osgeo threading conflicts with Django:

1. The view receives polygon coordinates via POST request.
2. It spawns `scripts/stac_pipeline.py` as a subprocess with a 55-second timeout.
3. The pipeline script connects to the Microsoft Planetary Computer STAC API.
4. It searches the `sentinel-2-l2a` collection for images within the polygon's bounding box, filtered to less than 40% cloud cover.
5. The top 5 clearest images are selected and processed in parallel using ThreadPoolExecutor.
6. For each image, windowed rasterio reads extract only the pixels covering the polygon's bounding box from the B04 (Red) and B08 (NIR) bands.
7. NDVI is computed as (NIR - Red) / (NIR + Red) and spatially averaged.
8. Results are returned as a JSON time series sorted by date.
9. If the pipeline times out or fails, a realistic seasonal NDVI simulation model generates the chart data. The simulation uses a sinusoidal crop growth model calibrated for Indian agricultural patterns (Kharif peak around late August, Rabi peak around mid-February) with latitude-based variation and cloud gap simulation.

**Technical implementation detail for SoilGrids queries:**

The soil data retrieval includes several resilience mechanisms:
- Retry logic with backoff (3 attempts with 1.5s, 3s, 4.5s delays).
- If the queried point returns no data (common in India where SoilGrids has gaps at 250m resolution), an outward ring search fires parallel probes at 0.3km, 1.1km, and 3.3km offsets (24 total probes) to find populated neighboring tiles.
- An in-memory LRU cache (512 entries, keyed by rounded coordinates to approximately 100m bins) prevents repeated upstream calls for the same parcel.
- USDA soil texture triangle classification is computed from clay/sand/silt percentages.

### 7.10 Alerts and Notifications

**Purpose**: Intelligence-driven alert system for proactive farm management, distinguishing between strategic (long-term planning) and operational (near-term action) alerts.

**Template**: `templates/pages/alerts.html`
**View**: `AlertsView` (extends ModuleView)

**Displayed Components:**

1. **Category Tabs**: All / Weather / Crop / Advisory / Strategic. Each tab filters the alert list by category.

2. **Alert Cards**: Each alert displays severity badge (High: red, Medium: amber, Low: green), title, message body, creation timestamp, and validity period.

3. **Strategic Alerts**: Long-horizon alerts derived from climate projections. Examples:
   - "Paddy suitability projected to decline 2 classes by 2035 under SSP2-4.5"
   - "Water stress trend exceeding safe threshold by 2032 -- increase rainwater harvesting"
   - "Temperature increase of 1.5C by 2035 will require shifting sowing calendar by 2-3 weeks"

4. **Operational Alerts**: Near-term advisories on weather events, pest risk windows, irrigation timing, and market price movements.

5. **Read/Unread Management**: Mark-as-read functionality. Unread count displayed in the navigation bar bell icon across all pages.

**Celery integration**: The `generate-alerts-every-minute` Celery Beat task continuously evaluates climate conditions and generates new alerts. The `refresh-climate-data-daily` task refreshes underlying climate data at 2:00 AM daily.

### 7.11 Market Insights

**Purpose**: Market intelligence connecting climate suitability projections to economic outcomes, enabling farmers to anticipate price and demand shifts.

**Template**: `templates/pages/market_insights.html`
**View**: `MarketInsightsView` (extends ModuleView)

**Displayed Components:**

1. **Commodity Cards**: For each crop in the farm's district:
   - Crop name and icon
   - MSP (Minimum Support Price) in INR per quintal
   - Current estimated mandi (market) price
   - Price differential (mandi minus MSP)
   - Demand level indicator (High / Medium / Low)

2. **Price Trend Chart**: Six-period mandi price trajectory plotted against the MSP baseline for the top commodity.

3. **Climate-Demand Correlation Logic**: The system uses `CropSuitability.change_class` to drive demand signals:
   - Negative change_class (declining suitability) implies reduced future supply, resulting in higher demand and price premiums.
   - Positive change_class (improving suitability) implies increased supply, resulting in lower demand pressure.
   - Zero change_class maintains stable demand.

**MSP Reference Data** (embedded in view logic):

| Crop | MSP (INR/quintal) |
|------|-------------------|
| Paddy | 2,183 |
| Soybean | 4,600 |
| Maize | 2,090 |
| Cotton | 6,620 |
| Groundnut | 6,377 |
| Millets | 2,500 |
| Turmeric | 6,800 |

### 7.12 Reports

**Purpose**: Professional PDF report generation for banks, FPOs, NABARD, insurance companies, and government institutions.

**Template**: `templates/pages/reports.html`
**View**: `ReportsView` (extends ModuleView)

**Supported Report Types:**

| Report Type | Content |
|------------|---------|
| Village Climate Report | Farm profile, location analysis, district climate metrics, crop suitability summary, rainfall/water outlook, risk indicators |
| Farm Climate Report | Detailed farm-level analysis including field conditions, vegetation health, irrigation plan, yield risk assessment |
| Risk Indicator Report | Multi-hazard risk scoring, flood/drought/agricultural stress analysis, future risk trajectories |

**PDF generation stack**: WeasyPrint converts styled HTML report templates into downloadable PDF files. Each report template inherits from a base report layout and dynamically populates data from the relevant models.

### 7.13 Help and Support

**Purpose**: Comprehensive data dictionary, metric glossary, and FAQ system auto-generated from the platform's own field metadata.

**Template**: `templates/pages/help.html`
**View**: `HelpView` (extends ModuleView)

**Displayed Components:**

1. **Dynamic FAQ**: Auto-generated by reading `data/final/dashboard/frontend_package/README_dashboard_fields.csv`. Each row in the CSV produces a question-and-answer entry:
   - Question: "What is the {display_name}?"
   - Answer: Combines the description, unit information (where applicable), and example value.

2. **Data Glossary**: Definitions for all climate indices, remote sensing metrics, and scenario terminology used in the platform.

### 7.14 Settings

**Purpose**: User profile management and platform customization.

**Template**: `templates/pages/settings.html`
**View**: `SettingsView` (extends ModuleView)

**Configurable Options:**
- Profile information (name, email, phone, role)
- Default farm location (state, district, village, GPS coordinates)
- Default season preference (Kharif / Rabi / Zaid)
- Unit preferences (metric/imperial, temperature scale)
- Notification preferences (alert categories, frequency, delivery method)
- Language selection (English, Hindi, Telugu)

---

## 8. Database Schema

### 8.1 Entity Relationship Diagram

```
  User (accounts)
  |-- role: FARMER | FPO | ADMIN
  |-- 1:1 --> FarmerProfile (phone, language, default_season)
  |-- 1:N --> Farm
                |-- name, village, district, state, location (JSON Point)
                |-- area_acres, soil_type, irrigation_source, elevation
                |-- M2M --> Crop (primary_crops)
                |
                |-- 1:N --> Field (name, area, current_crop FK)
                |-- 1:N --> ActivityLog (activity, date, note)
                |
                |-- 1:N --> LocationClimateIndex
                |             (season, year, 5 scores + 5 confidences, risk_level)
                |
                |-- 1:N --> VegetationObservation (date, ndvi, lai, soil_moisture, lst)
                |             |-- 1:1 --> StressAssessment
                |                         (vegetation_stress, heat_stress, water_stress,
                |                          climate_stress, resilience_score)
                |
                |-- 1:N --> ClimateProjection
                |             (scenario [ssp245|ssp370|ssp585], decade [2030|2035|2040],
                |              rainfall_change_pct, heat_stress_index, dry_days_change,
                |              soil_moisture_trend, water_stress_trend)
                |
                |-- 1:N --> CropSuitability [advisory]
                |             (crop FK, season, year, suitability_pct,
                |              recommendation_label, yield_min/max, risk_level, reasons JSON)
                |
                |-- 1:N --> CropSuitabilityTrend
                |             (crop FK, scenario, year, suitability_pct)
                |
                |-- 1:N --> WaterBalance (season, month, requirement_mm, availability_mm)
                |
                |-- 1:N --> IrrigationAdvisory
                |             (season, recommended_cycles, note, next_activity, window)
                |
                |-- 1:N --> YieldRisk
                |             (season, crop FK, risk_pct, risk_label, yield_low/high_pct)
                |
                |-- 1:N --> Alert
                |             (category, severity, title, message, valid_until, is_read)
                |
                +-- 1:N --> Report (type, period, generated_file)

  Crop (cropdata)
  |-- name, icon, category, season, water_requirement_mm
  |-- temp_min, temp_max, optimal_soil_moisture
  |-- 1:N --> CropCalendar (agro_zone, sowing dates, stage durations)
  |-- 1:N --> BestPractice (stage, text)
  +-- via CropSuitability [cropdata] (state, district, crop, current/projected suitability,
                                      change_class, risk_level, recommendation)

  ClimateRiskZone (climate) [standalone]
  |-- geometry (JSONField: full GeoJSON Feature with embedded properties)
  |-- district, state, risk_level, scenario, year, layer_type

  DistrictInsight (climate) [standalone]
  |-- district, scenario, year
  +-- key_insight_1, key_insight_2, key_insight_3
```

### 8.2 Model Field Reference

**accounts.User**

| Field | Type | Description |
|-------|------|-------------|
| username | CharField | Inherited from AbstractUser |
| email | EmailField | Inherited from AbstractUser |
| role | CharField(20) | Choices: FARMER, FPO, ADMIN. Default: FARMER |

**accounts.FarmerProfile**

| Field | Type | Description |
|-------|------|-------------|
| user | OneToOneField(User) | Back-reference: user.farmer_profile |
| phone | CharField(15) | Unique phone number |
| language | CharField(2) | Choices: EN, HI, TE. Default: EN |
| default_season | CharField(20) | Default: "Kharif" |

**farms.Farm**

| Field | Type | Description |
|-------|------|-------------|
| user | ForeignKey(User) | Farm owner |
| name | CharField(100) | Farm display name |
| village | CharField(100) | Village or hamlet name |
| district | CharField(100) | Administrative district |
| state | CharField(100) | State name |
| location | JSONField | GeoJSON Point: {"type": "Point", "coordinates": [lng, lat]} |
| area_acres | FloatField | Total farm area in acres |
| soil_type | CharField(100) | Primary soil classification |
| irrigation_source | CharField(100) | Water source (borewell, canal, rainfed, etc.) |
| elevation | FloatField (nullable) | Elevation in meters above sea level |
| primary_crops | ManyToManyField(Crop) | Crops currently or recently grown |

**climate.ClimateRiskZone**

| Field | Type | Description |
|-------|------|-------------|
| geometry | JSONField | Complete GeoJSON Feature dictionary with geometry and properties |
| district | CharField(100) | District name |
| state | CharField(100) | State name |
| risk_level | CharField(50) | Risk classification label |
| season | CharField(20) | Season (nullable) |
| scenario | CharField(50) | SSP scenario identifier (nullable) |
| year | IntegerField | Projection year (nullable) |
| layer_type | CharField(50) | Default: "climate_risk" |

The `geometry` field stores a complete GeoJSON Feature including both the polygon geometry and a `properties` dictionary containing all climate metrics for that district: `rainfall_change`, `temperature_change`, `drought_hazard_score`, `flood_hazard_score`, `ag_stress_score`, `overall_risk_score`, `overall_risk_class`, `climate_confidence_score`, and more. This denormalized design enables the dashboard to extract all metrics from a single database query.

**climate.ClimateProjection**

| Field | Type | Description |
|-------|------|-------------|
| farm | ForeignKey(Farm) (nullable) | Associated farm |
| district | CharField(100) | District name |
| scenario | CharField(10) | Choices: ssp245, ssp370, ssp585 |
| decade | IntegerField | Choices: 2030, 2035, 2040 |
| rainfall_change_pct | Decimal(5,2) | Projected rainfall change percentage |
| heat_stress_index | Decimal(4,1) | Heat stress index value |
| dry_days_change | Decimal(5,1) | Change in dry days count |
| soil_moisture_trend | Decimal(5,2) | Soil moisture trend indicator |
| water_stress_trend | Decimal(4,1) | Water stress trend indicator |

---

## 9. REST API Reference

All API endpoints require JWT authentication unless otherwise noted. The full interactive API documentation is available at:

- **Swagger UI**: `GET /api/docs/`
- **ReDoc**: `GET /api/redoc/`
- **OpenAPI 3.0 Schema (JSON)**: `GET /api/schema/`

### 9.1 Authentication

**Obtain Token Pair**

```
POST /api/v1/accounts/login/
Content-Type: application/json

{
  "username": "ramesh_kumar",
  "password": "secure_password"
}

Response 200:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOi...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOi..."
}
```

Access tokens expire after 1 hour. Refresh tokens expire after 7 days with rotation enabled.

**Refresh Token**

```
POST /api/v1/accounts/login/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOi..."
}

Response 200:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOi..."
}
```

**Register New User**

```
POST /api/v1/accounts/register/
Content-Type: application/json

{
  "username": "new_farmer",
  "email": "farmer@example.com",
  "password": "secure_password",
  "role": "FARMER"
}
```

### 9.2 Farm Management

**List Farms**

```
GET /api/v1/farms/
Authorization: Bearer {access_token}

Response 200:
{
  "count": 1,
  "results": [
    {
      "id": 1,
      "name": "Ramesh Farm",
      "village": "Kalwakurthy",
      "district": "Nagarkurnool",
      "state": "Telangana",
      "location": {"type": "Point", "coordinates": [78.49, 16.66]},
      "area_acres": 5.0,
      "soil_type": "Black Cotton Soil",
      "irrigation_source": "Borewell",
      "elevation": 380.0,
      "primary_crops": [{"id": 1, "name": "Paddy"}, {"id": 3, "name": "Cotton"}]
    }
  ]
}
```

**Create Farm**

```
POST /api/v1/farms/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "name": "My New Farm",
  "village": "Kalwakurthy",
  "district": "Nagarkurnool",
  "state": "Telangana",
  "location": {"type": "Point", "coordinates": [78.49, 16.66]},
  "area_acres": 3.5,
  "soil_type": "Red Soil",
  "irrigation_source": "Canal",
  "elevation": 400,
  "primary_crops": [1, 3]
}
```

### 9.3 Dashboard (Aggregated Endpoint)

```
GET /api/v1/farms/1/dashboard/?scenario=ssp245&year=2030
Authorization: Bearer {access_token}

Response 200:
{
  "farm": {
    "id": 1,
    "name": "Ramesh Farm",
    "district": "Nagarkurnool",
    ...
  },
  "season": "Kharif",
  "year": 2030,
  "climate_indices": {
    "rainfall_outlook_pct": 97.2,
    "water_stress_score": 42.5,
    "heat_stress_score": 31.8,
    "agri_resilience_score": 76.4,
    "climate_stress_index": 38.9,
    "rainfall_confidence": 82.0,
    "water_stress_confidence": 82.0,
    "heat_stress_confidence": 82.0,
    "agri_resilience_confidence": 82.0,
    "csi_confidence": 82.0
  },
  "recommended_crops": [
    {
      "id": 1,
      "crop_details": {"name": "Cotton", "icon": "..."},
      "suitability_pct": 85,
      "risk_level": "low"
    }
  ],
  "water_balance": [
    {"month": "Jun", "availability_mm": 124.5, "requirement_mm": 43.0},
    {"month": "Jul", "availability_mm": 284.2, "requirement_mm": 129.0},
    {"month": "Aug", "availability_mm": 253.8, "requirement_mm": 172.0},
    {"month": "Sep", "availability_mm": 152.1, "requirement_mm": 86.0},
    {"month": "Oct", "availability_mm": 50.0, "requirement_mm": 0.0}
  ],
  "yield_risks": [
    {"risk_label": "low", "risk_pct": 62}
  ],
  "future_outlook": {
    "scenario": "ssp245",
    "suitability_trends": [
      {"crop_name": "Cotton", "year": 2030, "suitability_pct": 85},
      {"crop_name": "Cotton", "year": 2035, "suitability_pct": 80},
      {"crop_name": "Cotton", "year": 2040, "suitability_pct": 75}
    ],
    "climate_projections": [
      {
        "decade": 2030,
        "rainfall_change_pct": -2.8,
        "heat_stress_index": 45.6,
        "dry_days_change": 4,
        "soil_moisture_trend": -8,
        "water_stress_trend": 10
      }
    ]
  },
  "latest_vegetation": {"ndvi": 0.72, "soil_moisture": 38, "lst": 33.2},
  "stress_assessment": {
    "vegetation_stress": "Low",
    "water_stress": "Moderate",
    "heat_stress": "Low",
    "climate_stress": "Moderate",
    "drought_score": 42.5,
    "overall_score": 38.9
  },
  "irrigation_advisory": {
    "next_irrigation_date": "Tomorrow",
    "recommended_amount_mm": 28,
    "recommended_cycles": 7,
    "window": "Jul 10 - Jul 15",
    "next_activity": "Start critical vegetative stage irrigation",
    "note": "Flood Irrigation",
    "advisory_text": "Adjusted for projected drought risk levels in your district."
  },
  "alerts": [...],
  "unread_alert_count": 3
}
```

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| scenario | string | ssp245 | Climate scenario: ssp245, ssp370, or ssp585 |
| year | integer | 2030 | Projection year. Snapped to nearest valid year: 2030, 2035, or 2040 |
| season | string | (latest) | Season filter |

### 9.4 Climate Data

```
GET /api/v1/climate/indices/?farm=1&season=Kharif&year=2030
GET /api/v1/climate/risk-zones/?season=Kharif&layer_type=climate_risk
GET /api/v1/climate/risk-zones/geojson/
GET /api/v1/climate/vegetation/?farm=1
GET /api/v1/climate/stress/?farm=1
GET /api/v1/climate/projections/?farm=1&scenario=ssp245
```

### 9.5 Advisory Data

```
GET /api/v1/advisory/suitability/?farm=1&season=Kharif
GET /api/v1/advisory/suitability-trends/?farm=1&scenario=ssp245
GET /api/v1/advisory/water-balance/?farm=1&season=Kharif
GET /api/v1/advisory/irrigation/?farm=1
GET /api/v1/advisory/yield-risk/?farm=1&season=Kharif
```

### 9.6 Map Data (Template-Consumed)

These endpoints are consumed by the frontend JavaScript and do not require JWT authentication (they use session authentication from the logged-in web user):

```
GET /api/map-data/risk/?scenario=ssp245&year=2030
GET /api/map-data/suitability/?crop=Maize
GET /api/map-data/insights/?district=Nizamabad&scenario=ssp245&year=2030
```

### 9.7 Parcel Inspector Endpoints

**NDVI Time Series**

```
POST /api/v1/farms/api/stac-ndvi/
Content-Type: application/json

{
  "polygon": [
    [78.49, 16.66],
    [78.50, 16.66],
    [78.50, 16.67],
    [78.49, 16.67],
    [78.49, 16.66]
  ]
}

Response 200 (live data):
{
  "data": [
    {"date": "2026-04-15", "ndvi": 0.4523},
    {"date": "2026-05-02", "ndvi": 0.5891},
    {"date": "2026-05-20", "ndvi": 0.7234}
  ],
  "source": "live"
}

Response 200 (fallback):
{
  "data": [...],
  "source": "simulated",
  "fallback_reason": "timeout"
}
```

**Parcel Details**

```
POST /api/v1/farms/api/parcel-details/
Content-Type: application/json

{
  "lat": 16.66,
  "lng": 78.49
}

Response 200:
{
  "lat": 16.66,
  "lng": 78.49,
  "location": {
    "display_name": "Kalwakurthy, Nagarkurnool, Telangana, India",
    "village": "Kalwakurthy",
    "district": "Nagarkurnool",
    "state": "Telangana",
    "country": "India",
    "postcode": "509324"
  },
  "weather": {
    "current": {"temperature_2m": 32.5, "relative_humidity_2m": 65, ...},
    "daily": {"temperature_2m_max": [34.2, 33.8, ...], ...}
  },
  "recent_climate": {
    "total_precip_mm": 145.2,
    "rainy_days": 12,
    "max_daily_rain_mm": 42.3,
    "avg_tmax_c": 33.1,
    "avg_et0_mm": 5.2,
    "water_balance_mm": -12.8
  },
  "soil": {
    "phh2o": 7.2,
    "soc": 8.5,
    "clay": 32.0,
    "sand": 28.0,
    "silt": 40.0,
    "bdod": 1.35,
    "cec": 18.2,
    "nitrogen": 1.8,
    "texture": "Clay Loam"
  },
  "elevation": {"elevation_m": 380.0}
}
```

---

## 10. Data Sources and Pipeline

### 10.1 Primary Data Sources

| Source | Data Provided | Resolution | Update Frequency |
|--------|--------------|------------|-----------------|
| CMIP6 Climate Models | Future temperature, precipitation, dry days projections under SSP2-4.5 and SSP5-8.5 | District-level (aggregated) | Pre-computed for 2030, 2035, 2040 |
| Sentinel-2 L2A (via Microsoft Planetary Computer STAC) | NDVI, NDWI, vegetation health indices | 10m spatial, 5-day temporal | Live pipeline (on-demand) |
| Open-Meteo Forecast API | Current weather, 7-day forecast | Point-level | Real-time |
| Open-Meteo Archive API | Historical daily weather (temperature, precipitation, ET0, radiation) | Point-level | Last 30 days |
| Open-Meteo Elevation API | Terrain elevation | Point-level | Static |
| ISRIC SoilGrids v2.0 | Topsoil properties (pH, SOC, clay, sand, silt, bulk density, CEC, nitrogen) | 250m | Static |
| OpenStreetMap Nominatim | Reverse geocoding (coordinates to address) | Point-level | Real-time |
| Crop Suitability Dataset | District-by-crop suitability matrix with current and projected classes | District-level | Pre-computed |
| District Risk Rankings | Multi-hazard risk scores, rankings, and classifications | District-level | Pre-computed |

### 10.2 Pre-Computed Data Assets

The `data/` directory contains approximately 200 MB of pre-computed datasets:

| Directory | File Count | Total Size | Content Description |
|-----------|-----------|------------|---------------------|
| `data/models/` | 8 files | ~11 MB | Trained ML model artifacts (pickle format) |
| `data/projections/` | 13 files | ~0.5 MB | SSP projection datasets (CSV + Parquet) |
| `data/risk/` | 4 files | ~0.1 MB | District risk scores and rankings |
| `data/evaluation/` | 5 files | ~3 KB | Model accuracy metrics and feature importance |
| `data/validation/` | 6 files | ~0.5 MB | Validation results and confidence scores |
| `data/final/geojson/` | 6 files | ~11 MB | Simplified GeoJSON for web rendering |
| `data/final/gis/` | 43 files | ~200 MB | Full-resolution Shapefile, GeoJSON, and GeoPackage outputs |
| `data/final/dashboard/` | 5 files | ~0.3 MB | Frontend-ready dashboard data packages |
| `data/final/insights/` | 2 files | ~0.2 MB | District insights and risk driver analysis |
| `data/final/rankings/` | 7 files | ~0.1 MB | Risk rankings, state summaries, top risk districts |
| `data/final/trends/` | 1 file | ~0.03 MB | District trend analysis |
| `data/final/reports/` | 2 files | ~0.01 MB | Risk change and state summary reports |
| `data/final/advanced/` | 3 files | ~0.3 MB | Advanced analytics datasets |

### 10.3 GIS Output Formats

For each of the 6 scenario-year combinations (ssp245/ssp585 x 2030/2035/2040), district risk data is available in multiple GIS formats:

| Format | File Extension | Approximate Size | Intended Use |
|--------|---------------|-----------------|--------------|
| GeoJSON (simplified) | .geojson | 1.8 MB each | Web map rendering (Leaflet.js) |
| GeoJSON (full resolution) | .geojson | 32 MB each | Desktop GIS analysis, high-detail rendering |
| Shapefile | .shp + .dbf + .shx + .prj + .cpg | 16 MB set | Traditional desktop GIS (QGIS, ArcGIS) |
| GeoPackage | .gpkg | 16 MB each | Modern GIS workflows, single-file convenience |

---

## 11. Machine Learning Models

### 11.1 Trained Model Inventory

All models are stored as serialized Python objects (pickle format) in `data/models/`:

| Model File | Target Variable | Algorithm | File Size | Input Features |
|-----------|----------------|-----------|-----------|----------------|
| `best_ndvi_model.pkl` | NDVI (Normalized Difference Vegetation Index) | RandomForest | 8.0 MB | Temperature, precipitation, soil moisture, elevation, season, crop type |
| `best_ndwi_model.pkl` | NDWI (Normalized Difference Water Index) | RandomForest / XGBoost | 200 KB | Precipitation, soil type, irrigation source, water table depth |
| `best_sm_model.pkl` | Soil Moisture | RandomForest / XGBoost | 570 KB | Rainfall, clay content, organic carbon, topography, land cover |
| `proxy_mean_et_model.pkl` | Evapotranspiration (ET) | RandomForest | 632 KB | Temperature, wind speed, humidity, solar radiation, crop stage |
| `proxy_mean_lai_model.pkl` | Leaf Area Index (LAI) | RandomForest | 534 KB | NDVI, temperature, precipitation, crop type, growth stage |
| `proxy_mean_pet_model.pkl` | Potential Evapotranspiration (PET) | RandomForest | 664 KB | Temperature, wind, humidity, radiation, altitude |
| `proxy_mean_solar_model.pkl` | Solar Radiation | RandomForest | 782 KB | Cloud cover, latitude, day of year, atmospheric conditions |

### 11.2 Model Evaluation Metrics

Available in `data/evaluation/`:

- `feature_importance_ndvi.csv`: Feature importance rankings for the NDVI prediction model
- `feature_importance_ndwi.csv`: Feature importance rankings for the NDWI prediction model
- `feature_importance_sm.csv`: Feature importance rankings for the soil moisture prediction model
- `horizon_b_metrics.csv`: Cross-validated accuracy metrics across all models
- `ablation_comparison.csv`: Ablation study comparing full model versus reduced feature sets

### 11.3 Model Selection Criteria

The `horizon_model_selection.json` file documents the hyperparameter tuning process and model selection rationale, including cross-validation scores, grid search parameters, and the final selected model configuration for each target variable.

---

## 12. Satellite Remote Sensing Pipeline

The satellite data pipeline (`scripts/stac_pipeline.py`) provides on-demand NDVI extraction from Sentinel-2 L2A imagery via the Microsoft Planetary Computer.

### 12.1 Pipeline Architecture

```
User draws polygon on map
         |
         v
Django view receives POST with polygon coordinates
         |
         v
Subprocess spawned (scripts/stac_pipeline.py)
with 55-second timeout budget
         |
         v
Connect to Microsoft Planetary Computer STAC API
(planetarycomputer.microsoft.com/api/stac/v1)
         |
         v
Search sentinel-2-l2a collection
  - Bounding box from polygon
  - Date range: last 120 days
  - Cloud cover filter: < 40%
         |
         v
Sort by cloud cover, select top 5 clearest scenes
         |
         v
ThreadPoolExecutor: parallel band reads
  For each scene:
  |-- Open B04 (Red) COG via rasterio
  |   - Transform bounds from EPSG:4326 to scene CRS
  |   - Windowed read (only bytes covering polygon bbox)
  |
  |-- Open B08 (NIR) COG via rasterio
  |   - Same windowed read
  |
  |-- Compute NDVI = (NIR - Red) / (NIR + Red)
  |-- Spatial mean over valid pixels
  +-- Return {"date": "YYYY-MM-DD", "ndvi": 0.XXXX}
         |
         v
Sort results by date, return JSON to stdout
         |
         v
Django view returns to client
  - source: "live" if pipeline succeeded
  - source: "simulated" if pipeline timed out or failed
```

### 12.2 GDAL Configuration

The pipeline sets the following GDAL environment variables for optimized remote COG reads:

| Variable | Value | Purpose |
|----------|-------|---------|
| `GDAL_DISABLE_READDIR_ON_OPEN` | EMPTY_DIR | Skip directory probing (saves one HTTP call per asset) |
| `VSI_CACHE` | TRUE | Cache fetched byte-ranges in memory |
| `VSI_CACHE_SIZE` | 67108864 (64 MB) | In-memory cache size for repeated reads |
| `GDAL_HTTP_MERGE_CONSECUTIVE_RANGES` | YES | Coalesce nearby range requests into single HTTP calls |
| `CPL_VSIL_CURL_USE_HEAD` | NO | Skip HEAD request before each GET |
| `GDAL_HTTP_MAX_RETRY` | 2 | Maximum retry attempts for failed HTTP requests |
| `GDAL_HTTP_RETRY_DELAY` | 1 | Delay between retries in seconds |

### 12.3 Fallback NDVI Simulation

When the live pipeline fails or times out, a deterministic seasonal NDVI model generates realistic chart data:

- Uses a sinusoidal crop growth model calibrated for Indian agricultural patterns
- Kharif season peak (Gaussian centered at day 240, approximately late August)
- Rabi season peak (Gaussian centered at day 45, approximately mid-February)
- Base soil/vegetation background of 0.15
- Latitude-based variation (tropical regions have higher base NDVI)
- Gaussian noise (sigma = 0.03) for realistic observation scatter
- 20% cloud gap simulation (random observation drops)
- 5-10 day revisit interval matching Sentinel-2 cadence
- Deterministic seed derived from polygon centroid for consistency across refreshes

---

## 13. External API Integrations

All external APIs used by the platform are free-tier and require no API keys or authentication.

### 13.1 Open-Meteo

**Forecast API** (`api.open-meteo.com/v1/forecast`):
- Current conditions: temperature, humidity, apparent temperature, precipitation, weather code, cloud cover, pressure, wind speed/direction/gusts
- Daily forecast: 7 days of max/min temperature, precipitation sum/probability, wind speed, sunrise/sunset, UV index

**Archive API** (`archive-api.open-meteo.com/v1/archive`):
- Historical daily data: precipitation_sum, temperature_2m_max/min, et0_fao_evapotranspiration, shortwave_radiation_sum
- Window: last 30 days (lagged by 2 days from current date)
- Timeout: 30 seconds

**Elevation API** (`api.open-meteo.com/v1/elevation`):
- Single point elevation query
- Timeout: 20 seconds

### 13.2 OpenStreetMap Nominatim

**Reverse Geocoding** (`nominatim.openstreetmap.org/reverse`):
- Input: latitude, longitude
- Output: display_name, village/hamlet/town, district, state, country, postcode
- User-Agent header: "FloodGuard-Agri-Intelligence/1.0"
- Timeout: 8 seconds

### 13.3 ISRIC SoilGrids v2.0

**Properties Query** (`rest.isric.org/soilgrids/v2.0/properties/query`):
- Queried properties: phh2o, soc, clay, sand, silt, bdod, cec, nitrogen
- Depth: 0-5cm (topsoil)
- Value type: mean
- Timeout: 25 seconds (initial), 12 seconds (jitter probes)
- Resilience: 3 retries with backoff, spatial jitter ring search (24 parallel probes), LRU cache (512 entries)

### 13.4 Microsoft Planetary Computer

**STAC API** (`planetarycomputer.microsoft.com/api/stac/v1`):
- Collection: sentinel-2-l2a
- Authentication: planetary_computer.sign_inplace (adds short-lived SAS tokens to asset URLs)
- Band access: B04 (Red, 10m), B08 (NIR, 10m)
- Cloud cover filter: less than 40%
- Scene limit: top 5 clearest
- Timeout: 55 seconds (subprocess budget)

---

## 14. Authentication and Security

### 14.1 Authentication Methods

The platform supports dual authentication:

1. **JWT Authentication** (for API consumers):
   - Access token lifetime: 1 hour
   - Refresh token lifetime: 7 days
   - Refresh token rotation enabled (each refresh generates a new refresh token)
   - Implementation: djangorestframework-simplejwt

2. **Session Authentication** (for web UI):
   - Django session middleware with cookie-based authentication
   - Login URL: `/auth/login/`
   - Custom backend: `EmailOrUsernameModelBackend` allows login with either username or email

### 14.2 Security Configuration (Production)

| Setting | Value | Purpose |
|---------|-------|---------|
| `SECURE_SSL_REDIRECT` | False (handled by load balancer) | SSL termination at proxy level |
| `SECURE_PROXY_SSL_HEADER` | ('HTTP_X_FORWARDED_PROTO', 'https') | Trust proxy SSL header |
| `SESSION_COOKIE_SECURE` | True | Session cookies only over HTTPS |
| `CSRF_COOKIE_SECURE` | True | CSRF cookies only over HTTPS |
| `CSRF_TRUSTED_ORIGINS` | Configurable via environment | Prevents CSRF attacks from untrusted origins |

### 14.3 Password Validation

Four Django password validators are active:
- UserAttributeSimilarityValidator
- MinimumLengthValidator
- CommonPasswordValidator
- NumericPasswordValidator

### 14.4 CORS Configuration

Cross-Origin Resource Sharing origins are configured via the `CORS_ALLOWED_ORIGINS` environment variable. The `django-cors-headers` middleware handles preflight requests.

### 14.5 Error Monitoring

Sentry SDK integration in production captures:
- Unhandled exceptions with full stack traces
- Performance traces at 10% sampling rate
- PII exclusion (`send_default_pii=False`)

---

## 15. Configuration Reference

### 15.1 Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SECRET_KEY` | Yes | dummy-key-for-build | Django secret key for cryptographic signing |
| `DEBUG` | No | False | Enable debug mode (True/False) |
| `ALLOWED_HOSTS` | No | [] | Comma-separated list of allowed host headers |
| `DATABASE_URL` | No | sqlite:///db.sqlite3 | Database connection string |
| `REDIS_URL` | No | redis://redis:6379/0 | Redis connection string for Celery and caching |
| `CORS_ALLOWED_ORIGINS` | No | [] | Comma-separated list of allowed CORS origins |
| `CSRF_TRUSTED_ORIGINS` | No | [floodguard-agri.onrender.com] | Trusted origins for CSRF validation |
| `SENTRY_DSN` | No | (empty) | Sentry error tracking Data Source Name |
| `DJANGO_SETTINGS_MODULE` | No | config.settings.dev | Settings module path |
| `GDAL_LIBRARY_PATH` | No | (auto-detected) | Path to GDAL shared library |
| `GEOS_LIBRARY_PATH` | No | (auto-detected) | Path to GEOS shared library |
| `VERCEL_URL` | No | (set by Vercel) | Automatically added to ALLOWED_HOSTS when present |

### 15.2 Settings Files

| File | Purpose |
|------|---------|
| `config/settings/base.py` | Shared configuration: installed apps, middleware, REST framework, JWT, Celery, static/media, timezone (Asia/Kolkata) |
| `config/settings/dev.py` | Development overrides: DEBUG=True, debug toolbar |
| `config/settings/prod.py` | Production overrides: SSL proxy headers, secure cookies, Sentry integration |

### 15.3 REST Framework Configuration

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
```

### 15.4 Celery Beat Schedule

| Task Name | Schedule | Description |
|-----------|----------|-------------|
| `generate-alerts-every-minute` | Every minute | Evaluates climate conditions and generates new alerts |
| `refresh-climate-data-daily` | 2:00 AM daily | Refreshes underlying climate datasets |

---

## 16. Getting Started

### 16.1 Prerequisites

- Python 3.12 or higher
- PostgreSQL 16 with PostGIS extension (or SQLite for rapid development)
- Redis 7.x (for Celery task queue)
- GDAL system library (for geospatial operations in the STAC pipeline)

### 16.2 Local Development Setup

```bash
# Clone the repository
git clone https://github.com/varunmax7/Project-Agri.git
cd Project-Agri

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Create the environment file
cp .env.example .env
# Edit .env with your configuration:
#   SECRET_KEY=your-secure-random-key
#   DEBUG=True
#   ALLOWED_HOSTS=localhost,127.0.0.1

# Run database migrations
python manage.py migrate

# Create a superuser account
python manage.py createsuperuser

# (Optional) Load demo data
python manage.py seed_demo_data

# Start the development server
python manage.py runserver

# The application will be available at http://127.0.0.1:8000/
# Admin interface at http://127.0.0.1:8000/admin/
# API documentation at http://127.0.0.1:8000/api/docs/
```

### 16.3 Running Celery Workers (Optional for Development)

```bash
# In a separate terminal, start the Celery worker
celery -A config worker -l info

# In another terminal, start the Celery beat scheduler
celery -A config beat -l info
```

---

## 17. Docker Deployment

### 17.1 Development with Docker Compose

```bash
# Build and start all services
docker compose up --build

# Services started:
#   web:    Django development server on port 8000
#   db:     PostGIS 16-3.4 on port 5432
#   redis:  Redis 7 on port 6379
#   celery: Celery worker
```

### 17.2 Production with Docker Compose

```bash
docker compose -f docker-compose.prod.yml up --build -d
```

**Production services:**
- Gunicorn (2 workers, 120-second timeout) serving the Django WSGI application
- Nginx reverse proxy with static and media file serving
- PostGIS 16 database with persistent volume
- Redis 7 for Celery broker and caching
- Celery worker for asynchronous task execution

### 17.3 Dockerfile Details

The production Dockerfile uses a multi-stage approach:
- Base image: `python:3.12-slim`
- System dependencies: build-essential, GDAL/PROJ libraries, Pango (for WeasyPrint PDF rendering), PostgreSQL client
- Static files are collected at build time using a dummy SECRET_KEY
- Startup command: migrate, ensure admin user, then launch Gunicorn

---

## 18. Cloud Deployment

### 18.1 Render

A `render.yaml` Blueprint is included for one-click deployment to Render. It provisions:

| Service | Type | Plan | Description |
|---------|------|------|-------------|
| floodguard-db | PostgreSQL | Free | Primary database |
| floodguard-redis | Redis | Starter | Celery broker and cache |
| floodguard-web | Web Service | Free | Django application (Gunicorn) |
| floodguard-celery-worker | Worker | Starter | Celery task worker |
| floodguard-celery-beat | Worker | Starter | Celery periodic task scheduler |

Environment variables are automatically wired between services. SECRET_KEY is auto-generated.

**Deploy command:**
```bash
# Push to GitHub, then connect the repository in Render Dashboard
# Render will auto-detect render.yaml and provision all services
```

### 18.2 Vercel

A `vercel.json` configuration is included for serverless deployment:
- Build script: `build_vercel.sh`
- WSGI entry point: `api/index.py`

Note: Vercel's serverless model has limitations for background tasks (Celery). The web application will function but scheduled tasks require a separate worker deployment.

---

## 19. Celery Task Queue

### 19.1 Configuration

- **Broker**: Redis (configurable via `REDIS_URL`)
- **Result Backend**: Redis
- **Serialization**: JSON for both tasks and results
- **Timezone**: Asia/Kolkata

### 19.2 Registered Tasks

| Task | Schedule | Description |
|------|----------|-------------|
| `apps.core.tasks.generate_alerts_task` | Every minute | Evaluates current climate conditions against thresholds and generates alerts for affected farms |
| `apps.core.tasks.refresh_climate_data_task` | Daily at 02:00 | Refreshes climate datasets from upstream sources |

### 19.3 Running Workers

```bash
# Standard worker
celery -A config worker -l INFO

# Beat scheduler (for periodic tasks)
celery -A config beat -l INFO

# Combined (development only)
celery -A config worker -B -l INFO
```

---

## 20. Testing

### 20.1 Test Files

| File | Purpose |
|------|---------|
| `test_views.py` | View response testing |
| `test_dashboard.py` | Dashboard endpoint integration testing |
| `test_client.py` | API client testing |
| `test_stac.py` | STAC pipeline functionality testing |
| `test_stac_env.py` | STAC environment configuration testing |

### 20.2 Running Tests

```bash
# Run all tests
python manage.py test

# Run specific test file
python manage.py test test_dashboard

# Run with verbosity
python manage.py test -v 2
```

---

## 21. Performance Considerations

### 21.1 Database Query Optimization

- The dashboard endpoint uses `.prefetch_related()` for farm queryset to minimize N+1 queries on primary_crops, fields, and activity_logs.
- ClimateRiskZone lookups use `filter(district__iexact=..., scenario=..., year=...)` with the unique_together constraint ensuring index usage.
- Alert queries include `.order_by('-created_at')[:5]` limiting to the most recent 5 records.

### 21.2 External API Parallelization

The Parcel Inspector fires 5 external API calls concurrently using `concurrent.futures.ThreadPoolExecutor(max_workers=5)`. Each API call is isolated so that a failure in one source does not affect the others.

### 21.3 SoilGrids Caching

An in-memory LRU cache with 512 entries prevents repeated calls to the ISRIC SoilGrids API for the same geographic location. Cache keys are rounded to approximately 100-meter bins to maximize hit rates for nearby queries.

### 21.4 STAC Pipeline Optimization

- Windowed rasterio reads ensure only the bytes covering the polygon bounding box are streamed from remote COGs, regardless of scene size.
- Scene count is capped at 5 to stay within the 55-second subprocess budget.
- GDAL environment variables are tuned for minimal HTTP overhead (disabled directory probing, merged range requests, suppressed HEAD requests).

### 21.5 Static File Serving

WhiteNoise middleware serves static files with:
- Gzip and Brotli compression
- Far-future cache headers
- Manifest-based cache busting via `CompressedManifestStaticFilesStorage`

---

## 22. Troubleshooting

### 22.1 Common Issues

**GDAL library not found**

```
django.core.exceptions.ImproperlyConfigured: Could not find the GDAL library
```

Solution: Install GDAL system library and set `GDAL_LIBRARY_PATH` in `.env`:
```bash
# macOS
brew install gdal
export GDAL_LIBRARY_PATH=$(gdal-config --prefix)/lib/libgdal.dylib

# Ubuntu
sudo apt-get install gdal-bin libgdal-dev
```

**SoilGrids returning empty data**

The ISRIC SoilGrids API has data gaps in certain regions of India. The application automatically performs a spatial jitter search (24 probes in concentric rings) to find nearby populated tiles. If all probes fail, the soil panel will display "No soil data at this location."

**STAC pipeline timing out**

The Sentinel-2 STAC pipeline has a 55-second timeout. Slow responses from the Microsoft Planetary Computer (common during peak usage) will trigger the fallback simulation. The chart will render with a "Simulated Model" badge. This is expected behavior.

**WeasyPrint PDF rendering errors**

WeasyPrint requires Pango and related libraries for PDF rendering:
```bash
# macOS
brew install pango

# Ubuntu
sudo apt-get install libpango-1.0-0 libpangoft2-1.0-0
```

**Database migration errors with PostGIS**

Ensure the PostGIS extension is enabled in your PostgreSQL database:
```sql
CREATE EXTENSION IF NOT EXISTS postgis;
```

---

## 23. Future Roadmap and Impact

### 23.1 Current Impact

| Impact Area | Description |
|------------|-------------|
| Farmer Decision Support | First platform providing CMIP6-derived, farm-level climate intelligence to Indian farmers |
| Evidence-Based Agriculture | Replaces anecdotal farming wisdom with quantified risk scores and suitability projections |
| Institutional Utility | Risk reports suitable for banks (NABARD), FPOs, insurance companies, and government agencies |
| Proactive Crop Transitions | Enables farmers to plan transitions before suitability declines, not after crop failure |

### 23.2 Short-Term Roadmap (3-6 Months)

| Feature | Description |
|---------|-------------|
| Real-Time Data Pipelines | Replace static projections with live Celery ingestion tasks: IMD rainfall feeds, Google Earth Engine NDVI time series, CMIP6 live model outputs |
| Native Mobile Application | Flutter or React Native app consuming the existing DRF API, with offline data caching for rural connectivity |
| Multi-Language Support | Full Hindi and Telugu translations for all UI text, advisory messages, and alert content |
| AI-Powered Narrative Insights | LLM-generated natural language summaries of risk trajectories and crop transition recommendations |

### 23.3 Medium-Term Roadmap (6-12 Months)

| Feature | Description |
|---------|-------------|
| Financial Intelligence | Climate-adjusted profitability calculators, input cost projections, loan eligibility scoring |
| Insurance Intelligence | Drought and extreme-rainfall risk scoring for parametric crop insurance premium calibration |
| Irrigation Intelligence | Real-time demand forecasting, reservoir and canal integration, groundwater depletion monitoring |
| Full Market Intelligence | Live mandi price feeds, demand forecasting from suitability trends, supply chain analytics |
| Advanced Remote Sensing | Multi-temporal SAR data (Sentinel-1) for flood extent mapping and all-weather soil moisture estimation |

### 23.4 Long-Term Vision (1-2 Years)

| Vision | Description |
|--------|-------------|
| Pan-India Coverage | Scale from current district coverage to all 700+ districts with state-level executive dashboards |
| FPO Collective Intelligence | Aggregated analytics across FPO member farms for collective planning, bulk input purchasing, and market negotiation |
| Carbon Credit Tracking | Quantify carbon sequestration from climate-adapted farming practices for voluntary carbon markets |
| Government API Integration | Bidirectional API integration with state agriculture departments for policy dashboards and subsidy targeting |
| Digital Twin Farming | Farm-level digital twins combining satellite, weather, soil, and crop growth models for real-time simulation and scenario planning |

### 23.5 Societal Impact

FloodGuard Agri Intelligence addresses three United Nations Sustainable Development Goals:

| SDG | Connection |
|-----|-----------|
| SDG 2: Zero Hunger | Enables farmers to maintain yield stability under changing climate by providing actionable crop transition guidance |
| SDG 13: Climate Action | Translates global climate models (CMIP6) into local adaptation strategies accessible to individual farming households |
| SDG 15: Life on Land | Promotes sustainable land management by matching crop selection to evolving soil and water conditions |

By making CMIP6 projections actionable at the farm level, the platform enables proactive adaptation instead of reactive recovery, potentially reducing climate-related crop losses across India's 150+ million farming households.

---

## 24. Glossary

| Term | Definition |
|------|-----------|
| **CMIP6** | Coupled Model Intercomparison Project Phase 6. The latest generation of global climate models used by the IPCC for future climate projections. |
| **SSP2-4.5** | Shared Socioeconomic Pathway 2-4.5. A "middle of the road" scenario where radiative forcing reaches 4.5 W/m2 by 2100. Moderate emissions, gradual progress on sustainability. |
| **SSP5-8.5** | Shared Socioeconomic Pathway 5-8.5. A "fossil-fueled development" scenario where radiative forcing reaches 8.5 W/m2 by 2100. Highest emissions pathway. |
| **NDVI** | Normalized Difference Vegetation Index. Computed from satellite imagery as (NIR - Red) / (NIR + Red). Ranges from -1 to 1; healthy vegetation typically 0.3-0.9. |
| **NDWI** | Normalized Difference Water Index. Indicates water content in vegetation and water bodies. |
| **LAI** | Leaf Area Index. The total one-sided area of leaf tissue per unit ground surface area. Indicates canopy density. |
| **LST** | Land Surface Temperature. The radiative temperature of the land surface measured by satellite thermal bands, in degrees Celsius. |
| **ET0** | Reference Evapotranspiration. The rate of evapotranspiration from a hypothetical reference grass surface, typically computed using the FAO Penman-Monteith equation. Measured in mm/day. |
| **PET** | Potential Evapotranspiration. The maximum possible evapotranspiration given unlimited water supply. |
| **SOC** | Soil Organic Carbon. The mass of carbon in soil organic matter, expressed in g/kg. Key indicator of soil fertility. |
| **CEC** | Cation Exchange Capacity. The total capacity of soil to hold exchangeable cations. Higher CEC indicates greater nutrient retention capability. |
| **STAC** | SpatioTemporal Asset Catalog. An open standard for describing geospatial information assets, enabling search and discovery of satellite imagery. |
| **COG** | Cloud-Optimized GeoTIFF. A GeoTIFF file format optimized for efficient HTTP range-read access, enabling extraction of spatial subsets without downloading entire files. |
| **PostGIS** | A spatial extension for PostgreSQL that adds support for geographic objects, enabling spatial queries and geometry storage. |
| **GeoJSON** | An open standard format for encoding geographic data structures using JSON. Used for district boundary polygons and choropleth rendering. |
| **MSP** | Minimum Support Price. The price at which the Government of India purchases agricultural commodities from farmers, providing a price floor. |
| **FPO** | Farmer Producer Organization. A collective of farmers organized for better market access, input procurement, and knowledge sharing. |
| **NABARD** | National Bank for Agriculture and Rural Development. India's apex development bank for agriculture and rural development. |
| **Kharif** | The summer/monsoon cropping season in India, typically June to October. Major crops: paddy, cotton, soybean, maize. |
| **Rabi** | The winter cropping season in India, typically November to March. Major crops: wheat, chickpea, mustard. |
| **Zaid** | The short summer cropping season between Rabi and Kharif, typically March to June. Crops: watermelon, cucumber, moong dal. |
| **q/ha** | Quintals per hectare. Standard unit for reporting crop yield in India. 1 quintal = 100 kg. |

---

## 25. Contributing

Contributions are welcome. Please follow these guidelines:

1. Fork the repository and create a feature branch.
2. Follow the existing code organization: one Django app per domain, serializers for all model endpoints, views using DRF viewsets where applicable.
3. All displayed metrics must read from the database. Never hardcode values in templates.
4. Write serializers and register with drf-spectacular for automatic API documentation.
5. Test your changes using the existing test suite.
6. Submit a pull request with a clear description of the changes and their motivation.

```bash
git checkout -b feature/your-feature-name
# Make changes
git commit -m "Add: description of your changes"
git push origin feature/your-feature-name
# Open a Pull Request on GitHub
```

---

## 26. License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

<div align="center">

**FloodGuard Agri Intelligence**

*Plan Today, Harvest Tomorrow*

Built for the resilience of Indian agriculture.

</div>
