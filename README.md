<![CDATA[<div align="center">

# 🌾 FloodGuard Agri Intelligence

### Climate Intelligence Platform for Future-Ready Farming

[![Django](https://img.shields.io/badge/Django-5.x-092E20?style=for-the-badge&logo=django&logoColor=white)](https://djangoproject.com)
[![DRF](https://img.shields.io/badge/DRF-3.15-red?style=for-the-badge&logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Leaflet](https://img.shields.io/badge/Leaflet-1.9-199900?style=for-the-badge&logo=leaflet&logoColor=white)](https://leafletjs.com)
[![Chart.js](https://img.shields.io/badge/Chart.js-4.x-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)](https://www.chartjs.org)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

**FloodGuard Agri Intelligence** is a full-stack climate intelligence platform that empowers Indian farmers to make data-driven, long-term crop, water, and investment decisions. Unlike generic weather apps, FloodGuard analyzes **future climate scenarios (2030–2040)** using CMIP6/SSP projections, district-level risk mapping, and crop suitability modeling to help farmers transition crops proactively — before climate change makes their current farming practices unviable.

[Live Demo](#getting-started) · [API Documentation](#api-reference) · [Architecture](#system-architecture) · [Contributing](#contributing)

</div>

---

## 📋 Table of Contents

- [The Problem](#-the-problem)
- [Our Approach](#-our-approach)
- [Key Features](#-key-features)
- [Screenshots](#-screenshots)
- [System Architecture](#-system-architecture)
- [Technology Stack](#-technology-stack)
- [Data Model](#-data-model)
- [Module Deep Dive](#-module-deep-dive)
- [API Reference](#-api-reference)
- [Getting Started](#-getting-started)
- [Project Structure](#-project-structure)
- [Deployment](#-deployment)
- [Scope & Future Roadmap](#-scope--future-roadmap)
- [Research & Data Sources](#-research--data-sources)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🔥 The Problem

### Climate Change is Destroying Indian Agriculture

India's agriculture sector, which sustains over **58% of the rural population** and contributes ~18% of GDP, faces an existential threat from accelerating climate change:

- **Unpredictable monsoons** — Rainfall variability has increased by 20–30% over the past two decades. Farmers can no longer rely on historical monsoon patterns for planting decisions.
- **Rising temperatures** — Average temperatures in India have risen by 0.7°C since 1901, with projections of +1.5°C to +4.4°C by 2100 under different SSP scenarios. Heat stress directly reduces crop yields for staples like wheat, rice, and cotton.
- **Water stress** — Groundwater depletion rates in states like Punjab, Haryana, and Telangana are alarming. By 2040, over 40% of India's districts could face severe water scarcity, making current irrigation-dependent crops unviable.
- **Flood and drought extremes** — Flash floods and prolonged droughts are becoming more frequent, destroying standing crops and wiping out entire seasons of income for smallholder farmers.
- **Crop suitability shifts** — Crops that are "highly suitable" today may become "marginal" or "unsuitable" by 2040. Without forward-looking intelligence, farmers continue investing in crops that climate models predict will fail.

### Why Existing Solutions Fall Short

| Existing Solution | Limitation |
|---|---|
| **Weather apps** (IMD, Skymet) | Show 7-day forecasts only. No future climate projections, no crop-specific guidance. |
| **Government advisory** (Kisan SMS) | Generic, one-size-fits-all messages. Not location-specific or personalized. |
| **AgriTech startups** | Focus on market prices, input delivery, or satellite monitoring — none provide **climate-scenario-driven crop transition planning**. |
| **Research reports** (ICAR, ICRISAT) | Published as dense PDFs for scientists. Inaccessible to farmers. Data is not actionable. |

### The Gap We Fill

**No existing platform tells a farmer:** *"Your Cotton crop in Adilabad district will decline by 3 suitability classes under SSP2-4.5 by 2040. Here's what to transition to, when, and why."*

FloodGuard Agri Intelligence fills this gap.

---

## 🎯 Our Approach

### Philosophy: Future-Driven Farm Planning

FloodGuard is **not** a weather app. It's not a marketplace. It's a **climate intelligence system** designed around one core principle:

> **Every screen reinforces future-driven farm planning.** Every metric, map, chart, and alert exists to help a farmer decide what to grow, how to manage water, and where to invest — not just today, but through 2030, 2035, and 2040.

### The 6 Hero Engines

The platform is powered by six interconnected analytical engines:

```
┌─────────────────────────────────────────────────────────────────────┐
│                    FloodGuard Intelligence Layer                    │
├──────────────┬──────────────┬──────────────┬────────────────────────┤
│  1. Climate  │ 2. Rainfall  │  3. Crop     │  4. Water             │
│  Risk Scoring│   Outlook    │  Suitability │  Stress               │
│              │              │  (Now + 2040)│  Analysis             │
├──────────────┴──────────────┴──────────────┴────────────────────────┤
│       5. Agricultural Stress Index    │   6. Future Climate        │
│       (Composite resilience metric)   │   Explorer (SSP scenarios) │
└───────────────────────────────────────┴─────────────────────────────┘
```

1. **Climate Risk Scoring** — Computes a composite overall risk score per district combining flood hazard, drought hazard, temperature change, and agricultural stress under specific SSP scenarios and target years.

2. **Rainfall Outlook Engine** — Analyzes projected rainfall changes (% deviation from historical normals) to classify water availability as Above Normal, Normal, or Below Normal with confidence scores.

3. **Crop Suitability Model** — The crown jewel. Maps every major crop's suitability class (Highly Suitable → Suitable → Moderate → Marginal → Unsuitable) for the current period AND projected periods under SSP2-4.5, SSP3-7.0, and SSP5-8.5 scenarios. Computes "decline classes" to quantify how much a crop's viability degrades.

4. **Water Stress Analysis** — Models monthly water requirement vs. availability balance for each farm, factoring in crop water demand, projected rainfall, and drought risk scores. Generates irrigation advisories.

5. **Agricultural Stress Index** — A composite metric combining vegetation stress (NDVI), heat stress (LST), water stress (soil moisture), and climate stress into a single resilience score. Measures how "stressed" a farming system is.

6. **Future Climate Explorer** — The SSP scenario navigator. Lets farmers compare outcomes under moderate warming (SSP2-4.5), high warming (SSP3-7.0), and extreme warming (SSP5-8.5) for any target decade (2030/2035/2040). Shows trend lines for crop suitability, water stress, and heat stress evolution.

### Data Strategy

We follow a clean separation between data and presentation:

```
Phase 1 (Current)     →  Curated research datasets + CMIP6/ICRISAT CSV data
                          loaded into database models
                          
Phase 2 (Planned)     →  Real-time pipelines ingesting from:
                          • IMD (India Meteorological Department) — rainfall
                          • Google Earth Engine — NDVI, LAI, LST, soil moisture
                          • Sentinel/MODIS satellites — vegetation indices
                          • CMIP6 models — SSP climate projections
                          
Architecture Rule     →  All displayed metrics read from the database.
                          Never hardcode values in templates.
                          Data source is swappable without UI changes.
```

---

## ✨ Key Features

### 🌍 Interactive Climate Risk Mapping
- District-level choropleth maps powered by Leaflet + GeoJSON
- Toggle between Climate Risk and Crop Suitability layers
- SSP scenario selector (SSP2-4.5, SSP3-7.0, SSP5-8.5)
- Year selector (2030, 2035, 2040)
- Color-coded risk levels: Low (green) → Moderate (yellow) → High (orange) → Very High (red)
- Coverage: All districts across Telangana, Andhra Pradesh, Maharashtra, Karnataka, and more

### 📊 Comprehensive Farm Dashboard
- 5 real-time climate index cards (Rainfall Outlook, Water Stress, Heat Stress, Agri Resilience, Climate Stress Index) with confidence scores
- Climate Risk Map with layer switching
- Recommended Crops table with suitability percentages and risk badges
- Key Indices gauges (Rainfall, Water Stress)
- Crop Timeline (Sowing → Vegetative → Flowering → Harvest)
- Water Requirement vs. Availability bar chart
- Yield Risk donut chart
- Future Outlook suitability strip (2030/2035/2040 projections)

### 🌾 Intelligent Crop Advisory
- Suitability Ranking — Crops ranked by suitability percentage for the farmer's specific district
- Crop Suitability Map — Per-crop spatial visualization
- Four advisory tabs: Suitability / Comparison / Calendar / Best Practices
- "Why is this crop suitable?" explanations with reasons derived from climate data
- Expected yield ranges (q/ha)
- Risk-level classification (Low / Medium / High)
- Crop calendars with stage-wise timelines

### 🔮 District Outlook (2030–2040)
- State → District → Scenario → Year selection
- District-level climate metrics: Overall Risk, Flood Hazard, Drought Hazard, Agri Stress, Temperature Change, Rainfall Change, Water Availability, Heat Stress Days
- Crop transition cards showing current vs. future suitability with decline classes
- Major crop historical analysis
- Soil type and growing period context
- Actionable recommendations per crop

### 💧 Water Management
- Soil moisture status monitoring
- Water stress trend analysis
- Monthly water requirement vs. availability comparison
- Irrigation scheduling advisory
- Recommended irrigation cycles and timing windows

### 🌡️ Weather & Climate
- Current conditions display (Temperature, Soil Moisture, Rainfall Outlook, Climate Stress)
- Regional Climate Map
- Water Balance visualization (Availability vs. Requirement)
- Seasonal Climate Summary with district risk level and narrative text

### 📈 Future Outlook Explorer
- SSP scenario comparison (SSP2-4.5 vs. SSP3-7.0 vs. SSP5-8.5)
- Four outlook tabs: Climate Outlook / Crop Suitability Trend / Water Outlook / Risk Outlook
- Trend line charts showing per-decade evolution
- Per-crop suitability trajectories across 2030/2035/2040
- Resilience score projections
- Key district insights

### 🔔 Smart Alerts & Notifications
- Category-based alerting: Weather / Crop / Advisory / Strategic
- Severity levels: Low / Medium / High
- Strategic alerts like: *"Paddy suitability declining after 2032 under SSP2-4.5"*
- Unread counter in top navigation bar
- Mark-as-read functionality

### 📄 PDF Report Generation
- Three report types: Village Climate Report, Farm Climate Report, Risk Indicator Report
- Powered by WeasyPrint (HTML → PDF)
- Reports include: Farm Profile, Crop Suitability Table, Climate Risk Data
- Downloadable and shareable — useful for bank loans, FPO meetings, NABARD submissions

### 📊 Market Insights
- MSP (Minimum Support Price) vs. Mandi (market) price comparison
- Demand signals derived from climate-driven crop suitability shifts
- Price trend charts per crop

### ⚙️ Settings & Personalization
- Profile management (name, email, phone)
- Farm location configuration (state, district, village)
- Season preference (Kharif / Rabi / Zaid)
- Unit system selection (Metric / Imperial)
- Notification preferences

### 📚 Help & Data Dictionary
- Auto-generated FAQ from data field definitions
- Data dictionary explaining every metric, unit, and index used in the platform
- Glossary of climate science terms

---

## 📸 Screenshots

### Dashboard — Farm Overview with Climate Intelligence
The main dashboard shows all five climate index cards, the interactive climate risk map, recommended crops, key indices gauges, crop timeline, water balance chart, yield risk analysis, and future outlook strip.

### My Farm — Farm Profile & Field Management
Detailed farm view with NDVI, Soil Moisture, and Land Surface Temperature readings. Tabs for field summary, soil & water analysis, irrigation planning, and activity logging.

### District Outlook — Evidence-Based Crop Transition Planning
The most powerful screen. Select any state, district, climate scenario, and target year to see projected climate metrics, crop suitability changes, decline classes, and transition recommendations.

### Interactive Map — Climate Risk & Crop Suitability Explorer
Full-screen Leaflet map with GeoJSON choropleth overlays. Switch between Climate Risk and Crop Suitability layers, select SSP scenarios and target years.

### PDF Reports — Climate & Agriculture Reports
Generated PDF reports containing farm profiles, crop suitability projections, and climate risk indicators suitable for institutional use.

---

## 🏗️ System Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                          CLIENT LAYER                                  │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────────┐ │
│  │   Django          │  │   Leaflet.js     │  │   Chart.js           │ │
│  │   Templates       │  │   Maps           │  │   Visualizations     │ │
│  │   + Tailwind CSS  │  │   + GeoJSON      │  │   + Gauges           │ │
│  │   + Alpine.js     │  │                  │  │                      │ │
│  └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────────┘ │
│           │                     │                      │               │
│           └─────────────────────┼──────────────────────┘               │
│                                 │                                      │
├─────────────────────────────────┼──────────────────────────────────────┤
│                          API LAYER (DRF)                               │
│  ┌──────────────────────────────┼──────────────────────────────────┐   │
│  │                              ▼                                  │   │
│  │  /api/v1/farms/{id}/dashboard/  ← Aggregated dashboard endpoint │   │
│  │  /api/v1/advisory/suitability/  ← Crop suitability records      │   │
│  │  /api/v1/advisory/trends/       ← Future suitability trends     │   │
│  │  /api/v1/advisory/water-balance/← Monthly water balance         │   │
│  │  /api/v1/advisory/irrigation/   ← Irrigation advisories        │   │
│  │  /api/v1/advisory/yield-risk/   ← Yield risk assessments       │   │
│  │  /api/v1/climate/indices/       ← Climate index records         │   │
│  │  /api/v1/climate/projections/   ← SSP climate projections       │   │
│  │  /api/v1/alerts/                ← Farm alerts                   │   │
│  │  /api/v1/reports/generate/      ← PDF generation                │   │
│  │  /api/map-data/risk/            ← GeoJSON risk zones            │   │
│  │  /api/map-data/suitability/     ← GeoJSON suitability data      │   │
│  │                                                                 │   │
│  │  Auth: JWT (SimpleJWT) + Session Authentication                 │   │
│  │  Docs: OpenAPI 3.0 via drf-spectacular (Swagger + ReDoc)        │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                        │
├────────────────────────────────────────────────────────────────────────┤
│                       APPLICATION LAYER                                │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────────────┐  │
│  │  accounts   │ │   farms    │ │  cropdata  │ │     climate        │  │
│  │  ─────────  │ │  ────────  │ │  ─────────  │ │  ──────────────   │  │
│  │  User       │ │  Farm      │ │  Crop      │ │  ClimateIndex     │  │
│  │  Profile    │ │  Field     │ │  Calendar  │ │  RiskZone         │  │
│  │  Auth       │ │  Activity  │ │  Practice  │ │  Projection       │  │
│  │             │ │  Log       │ │  Suitablty │ │  Vegetation       │  │
│  │             │ │            │ │            │ │  StressAssessment  │  │
│  │             │ │            │ │            │ │  DistrictInsight   │  │
│  └────────────┘ └────────────┘ └────────────┘ └────────────────────┘  │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────────────┐  │
│  │  advisory   │ │   alerts   │ │  reports   │ │      core          │  │
│  │  ─────────  │ │  ────────  │ │  ─────────  │ │  ──────────────   │  │
│  │  Suitablty  │ │  Alert     │ │  Report    │ │  Template Views   │  │
│  │  Trend      │ │  Category  │ │  PDF Gen   │ │  Map API          │  │
│  │  WaterBal   │ │  Severity  │ │  WeasyPrint│ │  Auth Views       │  │
│  │  Irrigation │ │  Read/Unrd │ │            │ │  Module Routing   │  │
│  │  YieldRisk  │ │            │ │            │ │                    │  │
│  └────────────┘ └────────────┘ └────────────┘ └────────────────────┘  │
│                                                                        │
├────────────────────────────────────────────────────────────────────────┤
│                        DATA LAYER                                      │
│  ┌─────────────────┐  ┌──────────────┐  ┌───────────────────────────┐ │
│  │  SQLite / PgSQL  │  │   CSV Data   │  │  GeoJSON District         │ │
│  │  (Primary DB)    │  │   Pipeline   │  │  Boundaries + Risk Zones  │ │
│  └─────────────────┘  └──────────────┘  └───────────────────────────┘ │
│                                                                        │
├────────────────────────────────────────────────────────────────────────┤
│                     INFRASTRUCTURE                                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────────────────┐ │
│  │  Celery   │  │  Redis   │  │  Gunicorn│  │  Docker / Render      │ │
│  │  Workers  │  │  Broker  │  │  WSGI    │  │  Nginx / WhiteNoise   │ │
│  └──────────┘  └──────────┘  └──────────┘  └────────────────────────┘ │
└────────────────────────────────────────────────────────────────────────┘
```

### Architecture Principles

1. **API-First Design** — Every data flow goes through a Django REST Framework API. The same backend serves the web dashboard today and will serve native mobile apps tomorrow.

2. **Data-Driven Templates** — Zero hardcoded metrics in templates. Every number, chart, and map layer reads from the database through the API layer. Data sources are swappable without UI changes.

3. **Modular Django Apps** — 8 loosely-coupled Django apps (`accounts`, `farms`, `cropdata`, `climate`, `advisory`, `alerts`, `reports`, `core`), each owning its own models, serializers, views, and URLs.

4. **Aggregated Dashboard Endpoint** — A single `GET /api/v1/farms/{id}/dashboard/` call returns everything the main dashboard needs: climate indices, recommended crops, water balance, yield risk, future outlook, vegetation data, stress assessments, irrigation advisory, and recent alerts. This minimizes frontend API calls.

5. **Scenario-Aware Computation** — All projections support SSP scenario selection (SSP2-4.5, SSP3-7.0, SSP5-8.5) and year snapping (2030/2035/2040). Year inputs are automatically snapped to the nearest available dataset year.

---

## 🛠️ Technology Stack

### Backend

| Technology | Purpose |
|---|---|
| **Django 5.x** | Web framework — views, ORM, admin, auth, templating |
| **Django REST Framework 3.15** | API layer — serializers, viewsets, authentication, permissions |
| **SimpleJWT** | JSON Web Token authentication for API access |
| **drf-spectacular** | OpenAPI 3.0 schema generation — Swagger UI + ReDoc |
| **Celery 5.x** | Distributed task queue — scheduled alert generation, data refresh |
| **Redis** | Message broker for Celery + caching layer |
| **WeasyPrint** | HTML → PDF report generation engine |
| **django-environ** | Environment variable management (.env file) |
| **WhiteNoise** | Static file serving for production |
| **Gunicorn** | Production WSGI HTTP server |
| **Sentry SDK** | Error tracking and monitoring (production) |

### Frontend

| Technology | Purpose |
|---|---|
| **Tailwind CSS** (CDN) | Utility-first CSS framework for responsive UI |
| **Alpine.js 3.x** | Lightweight reactive JS framework for interactivity |
| **Chart.js 4.x** | Charts — bar, line, doughnut, gauge visualizations |
| **Leaflet 1.9** | Interactive maps — choropleth, GeoJSON layers, markers |
| **Inter (Google Fonts)** | Typography — clean, modern UI typeface |

### Data & Spatial

| Technology | Purpose |
|---|---|
| **SQLite** (development) | Default local database |
| **PostgreSQL + PostGIS** (production) | Spatial database for GeoJSON and geometry queries |
| **GeoJSON** | District boundary polygons + climate risk zone geometries |
| **CSV Data Pipeline** | CMIP6/ICRISAT crop suitability data ingestion |

### DevOps

| Technology | Purpose |
|---|---|
| **Docker + Docker Compose** | Containerized development and production environment |
| **Nginx** | Reverse proxy and static file server (production) |
| **Render / Vercel** | Cloud deployment platforms |
| **GitHub** | Version control and CI/CD |

---

## 📐 Data Model

### Entity Relationship Diagram

```mermaid
erDiagram
    User ||--o{ Farm : owns
    User ||--o| FarmerProfile : has
    Farm ||--o{ Field : contains
    Farm ||--o{ ActivityLog : logs
    Farm }o--o{ Crop : grows
    
    Farm ||--o{ LocationClimateIndex : measured_at
    Farm ||--o{ VegetationObservation : observed_at
    Farm ||--o{ StressAssessment : assessed_at
    Farm ||--o{ ClimateProjection : projected_for
    
    Farm ||--o{ CropSuitability_Advisory : advised_for
    Farm ||--o{ CropSuitabilityTrend : trend_for
    Farm ||--o{ WaterBalance : balanced_for
    Farm ||--o{ IrrigationAdvisory : irrigated_at
    Farm ||--o{ YieldRisk : risk_for
    
    Farm ||--o{ Alert : alerted_for
    Farm ||--o{ Report : reported_for
    
    Crop ||--o{ CropCalendar : scheduled_by
    Crop ||--o{ BestPractice : guided_by
    Crop ||--o{ CropSuitability_Advisory : assessed_for
    Crop ||--o{ YieldRisk : risk_assessed
```

### Model Details

#### `accounts` App

| Model | Fields | Purpose |
|---|---|---|
| **User** | `username`, `email`, `role` (Farmer/FPO/Admin), `first_name`, `last_name` | Extended Django AbstractUser with role-based access |
| **FarmerProfile** | `phone`, `language` (EN/HI/TE), `default_season` | Farmer-specific preferences and regional settings |

#### `farms` App

| Model | Fields | Purpose |
|---|---|---|
| **Farm** | `name`, `village`, `district`, `state`, `location` (GeoJSON), `area_acres`, `soil_type`, `irrigation_source`, `elevation`, `primary_crops` (M2M) | Central entity — a farmer's land holding |
| **Field** | `farm` (FK), `name`, `area`, `current_crop` (FK) | Sub-divisions of a farm for field-level tracking |
| **ActivityLog** | `farm` (FK), `activity`, `date`, `note` | Farm activity journal for record-keeping |

#### `cropdata` App

| Model | Fields | Purpose |
|---|---|---|
| **Crop** | `name`, `icon`, `category`, `season`, `water_requirement_mm`, `temp_min`, `temp_max`, `optimal_soil_moisture` | Master crop catalogue with agronomic parameters |
| **CropCalendar** | `crop` (FK), `agro_zone`, `sowing_start/end`, `vegetative`, `flowering`, `harvest` | Stage-wise crop calendars per agro-climatic zone |
| **BestPractice** | `crop` (FK), `stage`, `text` | Stage-specific farming best practices |
| **CropSuitability** | `state`, `district`, `crop`, `suitability_current`, `suitability_projected`, `change_class`, `risk_level`, `recommendation` | District-level crop suitability data (current + projected) from CMIP6/ICRISAT research |

#### `climate` App

| Model | Fields | Purpose |
|---|---|---|
| **LocationClimateIndex** | `farm` (FK), `district`, `season`, `year`, `rainfall_outlook_pct`, `water_stress_score`, `heat_stress_score`, `agri_resilience_score`, `climate_stress_index`, `climate_risk_level`, confidence fields | Per-farm seasonal climate index records |
| **ClimateRiskZone** | `geometry` (GeoJSON), `district`, `state`, `risk_level`, `season`, `scenario`, `year`, `layer_type` | Spatial risk zone data powering choropleth maps |
| **VegetationObservation** | `farm` (FK), `field` (FK), `date`, `ndvi`, `lai`, `soil_moisture`, `lst` | Field-level vegetation and environmental readings |
| **StressAssessment** | `farm` (FK), `observation` (O2O), stress scores (vegetation/heat/water/climate), `resilience_score` | Computed stress assessments derived from observations |
| **ClimateProjection** | `farm` (FK), `district`, `scenario` (SSP), `decade`, `rainfall_change_pct`, `heat_stress_index`, `dry_days_change`, `soil_moisture_trend`, `water_stress_trend` | Future climate projections per SSP scenario |
| **DistrictInsight** | `district`, `scenario`, `year`, `key_insight_1/2/3` | Narrative insights per district-scenario-year combination |

#### `advisory` App

| Model | Fields | Purpose |
|---|---|---|
| **CropSuitability** | `crop` (FK), `farm` (FK), `season`, `year`, `suitability_pct`, `recommendation_label`, `expected_yield_min/max`, `risk_level`, `reasons` (JSON) | Farm-specific crop suitability assessments |
| **CropSuitabilityTrend** | `crop` (FK), `farm` (FK), `scenario`, `year`, `suitability_pct` | Time-series trend data for future suitability curves |
| **WaterBalance** | `farm` (FK), `season`, `month`, `requirement_mm`, `availability_mm` | Monthly water balance computations |
| **IrrigationAdvisory** | `farm` (FK), `season`, `recommended_cycles`, `note`, `next_activity`, `window` | Actionable irrigation scheduling advice |
| **YieldRisk** | `farm` (FK), `season`, `crop` (FK), `risk_pct`, `risk_label`, `yield_low_pct`, `yield_high_pct` | Crop-specific yield risk assessment |

#### `alerts` App

| Model | Fields | Purpose |
|---|---|---|
| **Alert** | `farm` (FK), `district`, `category` (weather/crop/advisory/strategic), `severity` (low/medium/high), `title`, `message`, `created_at`, `valid_until`, `is_read` | Multi-category alert system with read tracking |

#### `reports` App

| Model | Fields | Purpose |
|---|---|---|
| **Report** | `farm` (FK), `type` (village/farm/risk), `period`, `generated_file` (FileField), `created_at` | Generated PDF report records with file storage |

---

## 🔬 Module Deep Dive

### Module 1: Dashboard (Main Screen)

**Route:** `/` (Home)  
**Template:** `templates/pages/dashboard.html`  
**API Endpoint:** `GET /api/v1/farms/{id}/dashboard/?season=Kharif&year=2030&scenario=ssp245`

The dashboard is the primary landing screen after login. It aggregates data from across all engines into a single unified view:

**Top Row — Climate Index Cards:**
Each card shows a key metric with its value, status label (e.g., "Below Normal", "Moderate"), and confidence level:
- Rainfall Outlook (% of normal)
- Water Stress Score
- Heat Stress Score
- Agri Resilience Score
- Climate Stress Index

**Middle Row:**
- **Climate Risk Map** — Interactive Leaflet choropleth showing district-level risk zones with layer switching (Climate Risk / Crop Suitability)
- **Recommended Crops** — Table of crops ranked by suitability percentage with risk badges

**Bottom Row:**
- **Key Indices Gauges** — Circular gauges for Rainfall and Water Stress
- **Crop Timeline** — Horizontal Gantt-style chart showing Sowing → Vegetative → Flowering → Harvest stages with date ranges
- **Water Requirement vs. Availability** — Monthly bar chart comparing crop water demand against projected supply
- **Yield Risk** — Doughnut chart showing percentage of yield at risk
- **Future Outlook Strip** — 2030/2035/2040 suitability projections at a glance

---

### Module 2: My Farm

**Route:** `/farm/`  
**Template:** `templates/pages/myfarm.html`

The farm management hub displays the farmer's registered farm profile and field-level data:

- **Farm Header** — Name, location, area (acres), soil type, irrigation source, elevation
- **Current Conditions** — NDVI (vegetation health), Soil Moisture (%), Land Surface Temperature (°C)
- **Farm Location Map** — Leaflet map with farm boundary polygon and regional risk overlay
- **Tabs:**
  - **Overview** — Summary of current conditions and farm metrics
  - **Field Summary** — Per-field breakdown with crops and area
  - **Soil & Water** — Soil moisture trends and water availability
  - **Irrigation Plan** — Advisory with recommended cycles and timing
  - **Activity Log** — Chronological record of farm activities

---

### Module 3: Weather & Climate

**Route:** `/weather/`  
**Template:** `templates/pages/weather.html`

Seasonal climate intelligence for the farm's district:

- **Current Conditions Cards** — Temperature (°C), Soil Moisture (%), Rainfall Outlook (%), Climate Stress
- **Regional Climate Map** — District-level visualization
- **Water Balance Chart** — Availability vs. Requirement comparison
- **Seasonal Climate Summary** — Narrative text describing the overall district risk, drought projection, heat stress projection, and rainfall outlook

---

### Module 4: District Outlook ⭐

**Route:** `/district-outlook/`  
**Template:** `templates/pages/district_outlook.html`

**The most research-intensive module.** Powered by a 500,000+ row CSV dataset (`data/crop_suitability_final_output.csv`) containing CMIP6-derived projections for every district-crop-scenario-year combination.

**Selection Controls:**
- State dropdown (auto-populated from dataset)
- District dropdown (cascading from state)
- Climate Scenario selector (SSP2-4.5 / SSP3-7.0 / SSP5-8.5)
- Target Year selector (2030 / 2035 / 2040)

**Climate Dashboard:**
8 metric cards showing district-specific projections:
- Overall Risk Score + Risk Class
- Flood Hazard Score + Hazard Class
- Drought Hazard Score + Hazard Class
- Agricultural Stress Score + Stress Class
- Temperature Change (°C)
- Rainfall Change (%)
- Water Availability Index
- Heat Stress Days

**Crop Transition Cards:**
For each crop in the selected district:
- Current suitability class vs. projected class
- Decline classes (e.g., "-3 class" means dropping 3 levels)
- Stability indicator (Stable / Declining)
- Climate-driven explanation
- Soil type and growing period context
- Actionable recommendation

**Major Crop Analysis:**
Historical analysis of the district's dominant crop including area trends and yield changes from ICRISAT data.

---

### Module 5: Crop Advisory

**Route:** `/crop-advisory/`  
**Template:** `templates/pages/crop_advisory.html`  
**API Endpoint:** `GET /api/v1/advisory/suitability/?farm={id}&year=2030`

- **Suitability Ranking** — All crops ranked by suitability percentage for the farmer's district
- **Crop Suitability Map** — Spatial visualization per selected crop
- **Tabs:**
  - **Suitability** — Detailed view with reasons, risk level, and expected yield range
  - **Comparison** — Side-by-side crop comparison
  - **Calendar** — Stage-wise crop calendars with sowing/harvest dates
  - **Best Practices** — Stage-specific farming recommendations

---

### Module 6: Water Management

**Route:** `/water-management/`  
**Template:** `templates/pages/water_management.html`

- Soil moisture status with trend indicators
- Water stress trend analysis across the growing season
- Monthly requirement vs. availability comparison
- Irrigation scheduling advisory with recommended cycles, timing windows, and irrigation type recommendations

---

### Module 7: Future Outlook

**Route:** `/future-outlook/`  
**Template:** `templates/pages/future_outlook.html`

- SSP scenario selector with side-by-side comparison
- **Climate Outlook Tab** — Temperature, rainfall, and drought projections through 2040
- **Crop Suitability Trend Tab** — Per-crop trend lines showing suitability evolution
- **Water Outlook Tab** — Water stress trajectory and irrigation demand forecasts
- **Risk Outlook Tab** — Composite risk score evolution with decade-by-decade resilience scores

---

### Module 8: Interactive Map

**Route:** `/interactive-map/`  
**Template:** `templates/pages/interactive_map.html`

Full-screen map explorer with:
- **Climate Risk Layer** — District choropleth with risk zones (GeoJSON features with full property sets including risk scores, hazard classes, and confidence)
- **Crop Suitability Layer** — Per-crop suitability overlays
- **Data Explorer Panel** — Layer switching, scenario selection, year selection
- **District Click** — Click any district to see key insights (3 auto-generated insights per district-scenario-year)

---

### Module 9: Alerts & Notifications

**Route:** `/alerts/`  
**Template:** `templates/pages/alerts.html`

- **Category Tabs** — All / Weather / Crop / Advisories
- **Alert Cards** — Title, message, severity badge (High/Medium/Low), timestamp
- **Strategic Alerts** — Long-term alerts like "Cotton suitability declining 3 classes by 2040"
- **Bell Counter** — Real-time unread count in the navigation bar

---

### Module 10: Reports & PDF Generation

**Route:** `/reports/`  
**Template:** `templates/pages/reports.html`  
**API Endpoint:** `POST /api/v1/reports/generate/`

- **Report Types:**
  - Village Climate Report — Comprehensive village-level climate and agriculture assessment
  - Farm Climate Report — Farm-specific metrics and recommendations
  - Risk Indicator Report — Focused risk analysis with indicators
- **Generation Flow:** Select type → Click generate → WeasyPrint renders HTML template → PDF saved to media → Download link provided
- **Report Content:** Farm profile, crop suitability table (current + projected), climate risk data, generation metadata

---

### Module 11: Market Insights

**Route:** `/market-insights/`  
**Template:** `templates/pages/market_insights.html`

- MSP vs. Mandi price comparison for district crops
- Demand signals (High/Medium/Low) derived from crop suitability decline patterns
- Price trend line charts (6-period history)
- Crop icons and market indicators

---

### Module 12 & 13: Help/Support & Settings

- **Help** (`/help/`) — Auto-generated data dictionary from CSV field definitions + FAQ
- **Settings** (`/settings/`) — Profile, location, season defaults, units, notification preferences

---

## 📡 API Reference

### Authentication

The API supports both JWT (for programmatic access) and Session Authentication (for the web dashboard).

```bash
# Register a new user
POST /api/v1/accounts/register/
{
    "username": "farmer1",
    "email": "farmer@example.com",
    "password": "securepassword",
    "first_name": "Ramesh",
    "last_name": "Kumar"
}

# Login (obtain JWT tokens)
POST /api/v1/accounts/token/
{
    "username": "farmer1",
    "password": "securepassword"
}
# Returns: { "access": "eyJ...", "refresh": "eyJ..." }

# Refresh token
POST /api/v1/accounts/token/refresh/
{
    "refresh": "eyJ..."
}
```

### Farm Management

```bash
# List farms
GET /api/v1/farms/
Authorization: Bearer <access_token>

# Create a farm
POST /api/v1/farms/
{
    "name": "Varun Family Farm",
    "village": "Armoor",
    "district": "Nagarkurnool",
    "state": "Telangana",
    "area_acres": 12.5,
    "soil_type": "Black Cotton",
    "irrigation_source": "Borewell",
    "elevation": 600
}

# Get aggregated dashboard data
GET /api/v1/farms/{id}/dashboard/?season=Kharif&year=2030&scenario=ssp245
# Returns: climate_indices, recommended_crops, water_balance, yield_risks,
#          future_outlook, latest_vegetation, stress_assessment,
#          irrigation_advisory, alerts
```

### Advisory APIs

```bash
# Crop suitability for a farm
GET /api/v1/advisory/suitability/?farm={id}&year=2030

# Suitability trends
GET /api/v1/advisory/trends/?farm={id}&scenario=ssp245

# Water balance
GET /api/v1/advisory/water-balance/?farm={id}&season=Kharif

# Irrigation advisory
GET /api/v1/advisory/irrigation/?farm={id}

# Yield risk
GET /api/v1/advisory/yield-risk/?farm={id}&season=Kharif
```

### Map Data APIs

```bash
# Climate risk GeoJSON
GET /api/map-data/risk/?scenario=ssp245&year=2030
# Returns: GeoJSON FeatureCollection with district polygons

# Crop suitability data
GET /api/map-data/suitability/?crop=Maize
# Returns: Per-district suitability data

# District insights
GET /api/map-data/insights/?district=Adilabad&scenario=ssp245&year=2030
# Returns: 3 key insights for the district
```

### Reports

```bash
# List reports
GET /api/v1/reports/?farm={id}

# Generate a PDF report
POST /api/v1/reports/generate/
{
    "farm": 1,
    "type": "village",
    "period": "Kharif 2030"
}
# Returns: Report object with download URL
```

### Interactive API Documentation

- **Swagger UI:** `http://localhost:8000/api/docs/`
- **ReDoc:** `http://localhost:8000/api/redoc/`
- **OpenAPI Schema:** `http://localhost:8000/api/schema/`

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.12+** (tested with 3.14)
- **pip** (Python package manager)
- **Redis** (optional — only required for Celery background tasks)
- **Git**

### Quick Start (Local Development)

```bash
# 1. Clone the repository
git clone https://github.com/varunmax7/FloodGuard-Agri.git
cd FloodGuard-Agri

# 2. Create and activate a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
# Copy the example .env or create your own
cat > .env << EOF
SECRET_KEY=django-insecure-your-secret-key-here
DEBUG=True
DJANGO_ENV=dev
DB_NAME=floodguard
DB_USER=floodguard
DB_PASSWORD=floodguard
DB_HOST=localhost
DB_PORT=5432
REDIS_URL=redis://localhost:6379/0
EOF

# 5. Run database migrations
python3 manage.py migrate

# 6. Create a superuser (admin account)
python3 manage.py createsuperuser

# 7. Start the development server
python3 manage.py runserver

# 8. Open in browser
# Dashboard: http://127.0.0.1:8000/
# Admin:     http://127.0.0.1:8000/admin/
# API Docs:  http://127.0.0.1:8000/api/docs/
```

### Docker Setup

```bash
# Start all services (web, database, redis, celery)
docker-compose up --build

# In a separate terminal, run migrations
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser

# Access the application
# Dashboard: http://localhost:8000/
```

### Running Celery (Background Tasks)

```bash
# Start Celery worker (in a separate terminal)
celery -A config worker -l info

# Start Celery Beat scheduler (in another terminal)
celery -A config beat -l info

# Scheduled tasks:
# - generate_alerts_task: Runs every minute (demo)
# - refresh_climate_data_task: Runs daily at 2:00 AM
```

---

## 📁 Project Structure

```
FloodGuard Agri Intelligence/
│
├── config/                          # Django project configuration
│   ├── settings/
│   │   ├── base.py                  # Base settings (shared)
│   │   ├── dev.py                   # Development overrides
│   │   └── prod.py                  # Production overrides
│   ├── urls.py                      # Root URL configuration
│   ├── celery.py                    # Celery app configuration
│   ├── wsgi.py                      # WSGI application
│   └── asgi.py                      # ASGI application
│
├── apps/                            # Django applications
│   ├── accounts/                    # User auth & profiles
│   │   ├── models.py                # User, FarmerProfile
│   │   ├── serializers.py           # Registration, user serializers
│   │   ├── views.py                 # RegisterView (JWT)
│   │   ├── backends.py              # Email/username auth backend
│   │   └── management/commands/     # ensure_admin command
│   │
│   ├── farms/                       # Farm management
│   │   ├── models.py                # Farm, Field, ActivityLog
│   │   ├── serializers.py           # Farm serializer
│   │   ├── views.py                 # FarmViewSet + dashboard action
│   │   └── utils.py                 # Demo farm creation helper
│   │
│   ├── cropdata/                    # Crop catalogue & suitability data
│   │   ├── models.py                # Crop, CropCalendar, BestPractice, CropSuitability
│   │   ├── serializers.py           # Crop serializers
│   │   └── views.py                 # Crop CRUD viewsets
│   │
│   ├── climate/                     # Climate intelligence
│   │   ├── models.py                # ClimateIndex, RiskZone, VegetationObs, Projection, Insight
│   │   ├── serializers.py           # Climate serializers
│   │   ├── views.py                 # Climate API viewsets
│   │   └── admin.py                 # Admin configuration
│   │
│   ├── advisory/                    # Crop & water advisory
│   │   ├── models.py                # Suitability, Trend, WaterBalance, Irrigation, YieldRisk
│   │   ├── serializers.py           # Advisory serializers
│   │   └── views.py                 # Advisory viewsets (5 endpoints)
│   │
│   ├── alerts/                      # Alert system
│   │   ├── models.py                # Alert (category, severity, read status)
│   │   ├── serializers.py           # Alert serializer
│   │   └── views.py                 # Alert viewset
│   │
│   ├── reports/                     # PDF report generation
│   │   ├── models.py                # Report
│   │   ├── serializers.py           # Report serializer
│   │   └── views.py                 # ReportViewSet + generate action
│   │
│   └── core/                        # Template views & map APIs
│       ├── views.py                 # 13 module views + 3 map API endpoints
│       ├── urls.py                  # All template routes + map APIs
│       ├── tasks.py                 # Celery scheduled tasks
│       └── templatetags/            # Custom template tags
│
├── templates/                       # Django templates
│   ├── base.html                    # Master layout (sidebar + topbar)
│   ├── auth/                        # Login, register pages
│   ├── components/                  # Sidebar, topbar components
│   ├── pages/                       # 13 module page templates
│   │   ├── dashboard.html           # Main dashboard (26KB)
│   │   ├── myfarm.html              # Farm management (22KB)
│   │   ├── crop_advisory.html       # Crop advisory (20KB)
│   │   ├── future_outlook.html      # Future outlook (18KB)
│   │   ├── interactive_map.html     # Interactive map (17KB)
│   │   ├── district_outlook.html    # District outlook (12KB)
│   │   ├── water_management.html    # Water management (12KB)
│   │   ├── reports.html             # Report generation (10KB)
│   │   ├── settings.html            # Settings (10KB)
│   │   ├── alerts.html              # Alerts (8KB)
│   │   ├── weather.html             # Weather & climate (8KB)
│   │   ├── market_insights.html     # Market insights (4KB)
│   │   └── help.html                # Help & support (3KB)
│   └── reports/pdf/                 # PDF report HTML templates
│
├── static/                          # Static assets
│   └── css/floodguard.css           # Custom CSS overrides
│
├── data/                            # Research datasets
│   ├── crop_suitability_final_output.csv  # Master suitability dataset (500K+ rows)
│   ├── dashboard/                   # Dashboard data files
│   ├── final/                       # Final processed data
│   │   ├── geojson/                 # District boundary GeoJSON files
│   │   ├── dashboard/               # Frontend-ready data packages
│   │   ├── insights/                # District insights
│   │   ├── rankings/                # Crop rankings
│   │   ├── reports/                 # Report data
│   │   └── trends/                  # Trend data
│   ├── projections/                 # Climate projection data
│   ├── risk/                        # Risk assessment data
│   └── models/                      # ML model artifacts
│
├── media/                           # User-uploaded files (reports, etc.)
├── scripts/                         # Utility scripts
│   └── backup.sh                    # Database backup script
│
├── nginx/                           # Nginx configuration
│   └── nginx.conf                   # Reverse proxy config
│
├── docker-compose.yml               # Development Docker setup
├── docker-compose.prod.yml          # Production Docker setup
├── Dockerfile                       # Application container definition
├── render.yaml                      # Render deployment blueprint
├── vercel.json                      # Vercel deployment config
├── requirements.txt                 # Python dependencies
├── manage.py                        # Django management script
└── db.sqlite3                       # SQLite database (development)
```

---

## 🌐 Deployment

### Option 1: Render (Recommended)

The project includes a `render.yaml` blueprint for one-click deployment:

```yaml
# render.yaml defines:
# - Web service (Gunicorn)
# - PostgreSQL database
# - Redis instance
# - Celery worker
# - Environment variables
```

Steps:
1. Push code to GitHub
2. Connect to Render Dashboard
3. Create a new Blueprint Instance → Select your repo
4. Render auto-detects `render.yaml` and provisions all services

### Option 2: Docker (Any VPS)

```bash
# Production deployment
docker-compose -f docker-compose.prod.yml up -d --build

# Services started:
# - web (Gunicorn on port 8000)
# - db (PostGIS on port 5432)
# - redis (Redis on port 6379)
# - celery (Background worker)
# - nginx (Reverse proxy on port 80)
```

### Option 3: Vercel (Serverless)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

Note: Vercel deployment requires an external PostgreSQL database (e.g., Supabase, Neon) as Vercel is serverless and cannot run SQLite persistently.

### Environment Variables (Production)

| Variable | Description | Example |
|---|---|---|
| `SECRET_KEY` | Django secret key | `your-random-secret-key` |
| `DEBUG` | Debug mode | `False` |
| `DJANGO_ENV` | Environment | `prod` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/dbname` |
| `REDIS_URL` | Redis connection string | `redis://redis:6379/0` |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `floodguard.com,.onrender.com` |
| `CSRF_TRUSTED_ORIGINS` | Trusted CSRF origins | `https://floodguard.com` |
| `CORS_ALLOWED_ORIGINS` | CORS allowed origins | `https://floodguard.com` |
| `SENTRY_DSN` | Sentry error tracking DSN | `https://xxx@sentry.io/xxx` |
| `GDAL_LIBRARY_PATH` | GDAL library path (if using PostGIS) | `/usr/lib/libgdal.so` |
| `GEOS_LIBRARY_PATH` | GEOS library path (if using PostGIS) | `/usr/lib/libgeos_c.so` |

---

## 🔭 Scope & Future Roadmap

### Current Scope (MVP — Phase 1)

✅ **Completed:**
- Full 13-module web dashboard with responsive design
- API-first architecture with DRF + OpenAPI documentation
- JWT + Session authentication with role-based access
- Interactive climate risk mapping (GeoJSON + Leaflet choropleth)
- District-level crop suitability projections (SSP2-4.5 / SSP3-7.0 / SSP5-8.5)
- Crop transition planning with decline class visualization
- Water balance analysis and irrigation scheduling
- Yield risk assessment
- Strategic alert system (weather / crop / advisory / strategic)
- PDF report generation (WeasyPrint)
- Market insights with MSP vs. Mandi comparisons
- Celery-based background task scheduling
- Docker containerization and multi-platform deployment support
- Admin dashboard for data management

### Phase 2 — Real-Time Data Pipelines (Planned)

| Pipeline | Data Source | Frequency |
|---|---|---|
| Rainfall data | IMD (India Meteorological Department) | Daily |
| NDVI / LAI | Google Earth Engine / Sentinel-2 | Weekly |
| Soil Moisture | SMAP / Google Earth Engine | Weekly |
| Land Surface Temperature | MODIS / Sentinel-3 | Daily |
| SSP Climate Projections | CMIP6 Global Climate Models | Quarterly |
| Crop Price Data | eNAM / AgMarkNet | Daily |

### Phase 3 — Advanced Intelligence (Planned)

- **Irrigation Intelligence** — Demand forecasting, reservoir/canal integration, groundwater level monitoring
- **Financial Intelligence** — Climate-adjusted crop profitability modeling, lending risk assessment for banks/FPOs, ROI calculators for crop transitions
- **Insurance Intelligence** — Parametric insurance risk scoring based on drought/flood probability, extreme rainfall event frequency analysis
- **Pest & Disease Prediction** — Climate-correlated pest outbreak risk modeling, integration with ICAR pest surveillance data
- **Carbon Credit Estimation** — Farm-level carbon sequestration potential, eligible credit programs, revenue projections from carbon markets

### Phase 4 — Mobile & Regional (Planned)

- **Native Mobile App** (React Native / Flutter) consuming the existing DRF API
- **Regional Language Support** — Hindi, Telugu, Marathi, Kannada interfaces
- **Voice-Based Advisory** — IVR system for farmers without smartphones
- **FPO Dashboard** — Aggregate view for Farmer Producer Organizations managing multiple farms
- **NABARD/Bank Reports** — Standardized reports for institutional credit assessment
- **Offline Mode** — Critical farm data and advisories available without internet

### Phase 5 — Scale (Planned)

- **Pan-India Coverage** — Expand from current 5+ states to all 28 states and 8 UTs
- **Block-Level Granularity** — Move from district-level to block/taluk-level projections
- **AI-Powered Advisory** — LLM-based conversational advisory ("Ask FloodGuard")
- **Satellite Integration** — Direct Sentinel-2 / Landsat integration for real-time field monitoring
- **IoT Sensor Network** — Support for ground-based soil moisture, weather station, and water level sensors

---

## 📚 Research & Data Sources

### Climate Science Foundation

FloodGuard's projections are grounded in peer-reviewed climate science:

| Source | Data Used | Reference |
|---|---|---|
| **CMIP6** (Coupled Model Intercomparison Project Phase 6) | SSP scenario projections — temperature change, rainfall change, extreme events | [WCRP CMIP6](https://www.wcrp-climate.org/wgcm-cmip/wgcm-cmip6) |
| **SSP Scenarios** (Shared Socioeconomic Pathways) | SSP2-4.5 (moderate), SSP3-7.0 (high), SSP5-8.5 (extreme) warming scenarios | [IPCC AR6](https://www.ipcc.ch/assessment-report/ar6/) |
| **ICRISAT** (International Crops Research Institute for the Semi-Arid Tropics) | District-level crop area, yield, and production data; agro-ecological characterization | [ICRISAT Data](http://data.icrisat.org/) |
| **IMD** (India Meteorological Department) | Historical and real-time rainfall, temperature data | [IMD](https://mausam.imd.gov.in/) |
| **ICAR** (Indian Council of Agricultural Research) | Crop suitability guidelines, agro-climatic zone definitions | [ICAR](https://icar.org.in/) |

### Risk Scoring Methodology

The overall climate risk score is a composite index computed from:

```
Overall Risk Score = w1 × Flood Hazard Score 
                   + w2 × Drought Hazard Score 
                   + w3 × Temperature Change Index 
                   + w4 × Agricultural Stress Score

where w1 + w2 + w3 + w4 = 1 (weights calibrated per agro-climatic zone)
```

Risk Classification:
| Score Range | Risk Class | Color Code |
|---|---|---|
| 0 – 20 | Low Risk | 🟢 Green |
| 20 – 40 | Moderate Risk | 🟡 Yellow |
| 40 – 60 | High Risk | 🟠 Orange |
| 60 – 100 | Very High Risk | 🔴 Red |

### Crop Suitability Classification

Suitability is assessed on a 5-tier scale:

| Class | Suitability % | Description |
|---|---|---|
| Highly Suitable | 80–100% | Optimal climate/soil conditions for the crop |
| Suitable | 60–80% | Good conditions with minor limitations |
| Moderate | 40–60% | Acceptable with significant management needs |
| Marginal | 20–40% | High risk, requires substantial adaptation |
| Unsuitable | 0–20% | Climate/soil conditions preclude viable cultivation |

**Decline Classes** quantify the shift between current and projected suitability:
- `-1 class` = Minor decline (e.g., Highly Suitable → Suitable)
- `-2 class` = Significant decline (e.g., Highly Suitable → Moderate)
- `-3 class` = Severe decline (e.g., Highly Suitable → Marginal)
- `-4 class` = Critical decline (e.g., Highly Suitable → Unsuitable)

---

## 🤝 Contributing

We welcome contributions! FloodGuard is an ambitious project, and there's a lot to build.

### Areas Where We Need Help

- **Climate Data Scientists** — Improving risk models, validating projections against ground truth
- **GIS Engineers** — Higher-resolution spatial data, block-level boundaries, better choropleth rendering
- **Frontend Developers** — Mobile responsiveness, chart interactions, accessibility improvements
- **ML Engineers** — Crop yield prediction models, pest/disease risk models
- **Regional Language Translators** — Hindi, Telugu, Marathi, Kannada, Tamil translations
- **Domain Experts** — Agricultural scientists, extension officers, FPO managers for validation

### Development Setup

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/FloodGuard-Agri.git
cd FloodGuard-Agri

# Create a branch
git checkout -b feature/your-feature-name

# Install development dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your settings

# Run migrations
python3 manage.py migrate

# Start development server
python3 manage.py runserver

# Make your changes, then submit a PR
git add .
git commit -m "feat: description of your changes"
git push origin feature/your-feature-name
```

### Code Style

- Python: Follow PEP 8
- Templates: Use Django template conventions
- JavaScript: Use Alpine.js patterns established in the codebase
- CSS: Use Tailwind utility classes
- All API endpoints must have drf-spectacular schema decorations
- All models must have `__str__` methods and be registered in admin

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- **ICRISAT** for district-level agricultural data and crop characterization
- **CMIP6 / IPCC AR6** for climate scenario projections
- **India Meteorological Department** for historical climate data
- **OpenStreetMap** contributors for map base layers
- **Leaflet**, **Chart.js**, **Alpine.js**, **Tailwind CSS** open-source communities
- **Django** and **Django REST Framework** communities

---

<div align="center">

**Built with ❤️ for Indian Farmers**

*"The best time to plant a tree was 20 years ago. The second best time is now — but now with climate intelligence."*

---

**FloodGuard Agri Intelligence** — *Because the future of farming should be planned, not gambled.*

[⬆ Back to Top](#-floodguard-agri-intelligence)

</div>
]]>
