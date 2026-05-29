# FloodGuard Agri Intelligence — Django Build Roadmap

> A climate intelligence platform that helps farmers make long-term crop, water, and investment decisions — **not** a weather or generic advisory app. Every screen reinforces *future-driven farm planning*.

This roadmap is written so each **Phase** is a self-contained chunk you can hand to Antigravity as one task. Build in order — later phases depend on earlier ones.

---

## 1. Final Feature Set (Build NOW — MVP Web App)

These are locked from your two mockups + the positioning doc. Eleven sidebar modules:

| # | Module | What it contains (from mockups) |
|---|--------|---------------------------------|
| 1 | **Dashboard** | 5 index cards (Rainfall Outlook, Water Stress, Heat Stress, Agricultural Resilience, Climate Stress Index) + Climate Risk Map (choropleth, layer switcher) + Recommended Crops table + Key Indices gauges + Crop Timeline + Water Requirement vs Availability chart + Yield Risk donut + Future Outlook suitability strip |
| 2 | **My Farm** | Farm profile (area, soil, irrigation, primary crops, village, elevation) + tabs: Overview / Field Summary / Soil & Water / Irrigation Plan / Activity Log + current field condition (NDVI, Soil Moisture, LST) + irrigation advisory + next activity |
| 3 | **Weather & Climate** | Current conditions + recent rainfall/temperature + seasonal climate summary |
| 4 | **Crop Advisory** | Suitability Ranking + Crop Suitability Map + tabs: Suitability / Comparison / Calendar / Best Practices + "Why is X suitable" reasons + expected yield range + risk level |
| 5 | **Water Management** | Soil moisture status + water stress trend + requirement vs availability + irrigation scheduling advisory |
| 6 | **Future Outlook (2030–2040)** | Scenario selector (SSP2-4.5) + tabs: Climate Outlook / Crop Suitability Trend / Water Outlook / Risk Outlook + trend line charts + per-decade resilience scores + key insights |
| 7 | **Alerts & Notifications** | Tabs: All / Weather / Crop / Advisories + strategic alerts with severity (High/Medium/Low) |
| 8 | **Market Insights** | (Light MVP — price/demand placeholder; full build = Phase 2) |
| 9 | **Reports** | Generate + download PDFs: Climate Outlook, Crop Suitability, Water Stress, Agri Resilience, Future Outlook report |
| 10 | **Help & Support** | FAQ / contact |
| 11 | **Settings** | Profile, location, season default, units, notifications |

Plus a **mobile-responsive farmer view** of Dashboard / Crop Advisory / Future Outlook / Alerts.

### The 6 "hero" engines behind these screens
1. Climate Risk scoring  2. Rainfall Outlook  3. Crop Suitability (current + 2030/35/40)  4. Water Stress  5. Agricultural Stress  6. Future Climate Explorer

---

## 2. Recommended Tech Stack

**Decision I'm making for you (state it to Antigravity):** build **API-first** so the same backend serves the web dashboard now and a mobile app later.

- **Backend:** Django 5.x + Django REST Framework (DRF)
- **Database:** PostgreSQL + **PostGIS** (needed for the choropleth Climate Risk Map and spatial queries)
- **Web frontend (MVP):** Django templates + **Tailwind CSS** + **Alpine.js** (lightweight interactivity). Single codebase, fastest for Antigravity to produce. *(Scale path: swap to a React/Next SPA consuming the DRF API — not needed for MVP.)*
- **Charts:** Chart.js or ApexCharts (line trends, bar requirement-vs-availability, donut yield risk, gauges)
- **Maps:** Leaflet + GeoJSON for the district choropleth and layer switcher
- **PDF reports:** WeasyPrint (HTML→PDF, easiest for styled reports)
- **Async / scheduled jobs:** Celery + Redis (alert generation, data refresh) — wire up in the final phase
- **Auth:** Django auth + DRF token/JWT (`djangorestframework-simplejwt`)
- **Deploy:** Docker + Gunicorn + Nginx (Render/Railway/AWS)

---

## 3. Core Data Model (the backbone)

Build these as Django apps: `accounts`, `farms`, `cropdata`, `climate`, `advisory`, `alerts`, `reports`.

**accounts**
- `User` (extend AbstractUser; role: farmer / FPO / admin)
- `FarmerProfile` (phone, language, default_season)

**farms**
- `Farm` → user FK; name, village, district, state, latitude, longitude, area_acres, soil_type, irrigation_source, elevation, primary_crops (M2M→Crop)
- `Field` → farm FK; name, area, current_crop
- `ActivityLog` → farm FK; activity, date, note

**cropdata**
- `Crop` → name, icon, category, season, water_requirement_mm, temp_min, temp_max, optimal_soil_moisture
- `CropCalendar` → crop FK, agro_zone, sowing_start, sowing_end, vegetative, flowering, harvest
- `BestPractice` → crop FK, stage, text

**climate** (powers the dashboard cards, maps, future outlook)
- `LocationClimateIndex` → location/Farm, season, year, rainfall_outlook_pct, water_stress_score, heat_stress_score, agri_resilience_score, climate_stress_index, climate_risk_level, confidence_each
- `ClimateRiskZone` → geometry (PostGIS), district, risk_level, season, layer_type *(choropleth source)*
- `VegetationObservation` → farm/field, date, ndvi, lai, soil_moisture, lst
- `StressAssessment` → derived: vegetation_stress, heat_stress, water_stress, climate_stress, resilience_score
- `ClimateProjection` → location, scenario, decade(2030/35/40), rainfall_change_pct, heat_stress_index, dry_days_change, soil_moisture_trend, water_stress_trend

**advisory**
- `CropSuitability` → crop, location, season, year, suitability_pct, recommendation_label, expected_yield_min, expected_yield_max, risk_level, reasons(JSON)
- `CropSuitabilityTrend` → crop, location, scenario, year, suitability_pct *(future trend line)*
- `WaterBalance` → farm, season, month, requirement_mm, availability_mm
- `IrrigationAdvisory` → farm, season, recommended_cycles, note, next_activity, window
- `YieldRisk` → farm, season, crop, risk_pct, risk_label, yield_low_pct, yield_high_pct

**alerts**
- `Alert` → farm/location, category(weather/crop/advisory/strategic), severity, title, message, created_at, valid_until, is_read

**reports**
- `Report` → farm, type, period, generated_file, created_at

---

## 4. The Hard Part — Data Sourcing (read before Phase 2)

The UI numbers (NDVI, rainfall %, SSP projections) have to come from somewhere. **Strategy: build the whole app on a clean, well-typed mock/seed dataset first**, then swap in real pipelines without touching the UI.

- **Now (MVP):** Management command (`seed_demo_data`) that populates realistic values for 1–2 demo districts (e.g. Nizamabad) so every screen renders. Keep all numbers in the models above so the source is swappable.
- **Later (Phase 2 pipelines):** rainfall → IMD; NDVI/LAI/LST/soil moisture → Google Earth Engine / Sentinel / MODIS; future projections → CMIP6 / SSP scenarios. Each becomes a Celery ingestion task writing to the same tables.

Tell Antigravity explicitly: *"All displayed metrics read from the database; never hardcode in templates."*

---

## 5. Step-by-Step Build Roadmap (hand each Phase to Antigravity)

### Phase 0 — Scaffolding
- Create Django project `floodguard` + apps listed above.
- Configure PostgreSQL + PostGIS, environment variables (`.env`), `settings` split (base/dev/prod).
- Install: DRF, simplejwt, django-tailwind (or Tailwind CLI), Pillow, weasyprint, celery, redis, psycopg2.
- Set up Docker + docker-compose (web, db, redis).
- **Deliverable:** project runs, DB connects, `/admin` loads.

### Phase 1 — Auth & Farmer Onboarding
- Custom `User` + `FarmerProfile`; JWT endpoints (register/login/refresh).
- Onboarding flow: create Farm (village, area, soil type, irrigation source, location pin, primary crops).
- **Deliverable:** a farmer can sign up, log in, and create their farm.

### Phase 2 — Data Models + Admin + Seed Data
- Implement all models from Section 3; register everything in Django admin.
- Write `seed_demo_data` management command (Nizamabad demo farm "Ramesh Kumar", Kharif 2030, all indices, crops, projections, alerts, water balance).
- **Deliverable:** admin shows fully populated demo data driving every future screen.

### Phase 3 — API Layer (DRF)
- Serializers + viewsets + URLs for: farm, dashboard summary, climate indices, crop suitability, future projections, water balance, alerts, reports.
- One aggregated `dashboard/` endpoint returning everything Screen 1 needs in a single call.
- **Deliverable:** documented API (DRF browsable / Swagger) returning the demo data.

### Phase 4 — UI Shell & Design System
- Base template: left sidebar (the 11 modules), top bar (season selector, weather chip, notifications bell, profile), content area.
- Tailwind theme: green primary, card style, status colors (green/amber/orange/red for risk levels), reusable components (metric card, gauge, table, tab bar, badge).
- **Deliverable:** empty but pixel-faithful shell matching the mockups, navigation working.

### Phase 5 — Dashboard Module ⭐
- 5 metric cards (value + label + confidence).
- Climate Risk Map (Leaflet choropleth + layer switcher) reading `ClimateRiskZone`.
- Recommended Crops table (suitability bar + recommendation label).
- Key Indices gauges; Crop Timeline; Water Requirement vs Availability bar chart; Yield Risk donut; Future Outlook suitability strip (2030/35/40).
- **Deliverable:** Screen matching Image 2 end-to-end from the API.

### Phase 6 — My Farm Module
- Farm header (area, soil, irrigation, primary crops, elevation).
- Tabs: Overview / Field Summary / Soil & Water / Irrigation Plan / Activity Log.
- Current field condition cards (NDVI, Soil Moisture, NDWI, LST) + irrigation advisory + next activity.
- **Deliverable:** Screen 3 from Image 1.

### Phase 7 — Crop Advisory Module ⭐
- Suitability Ranking list + Crop Suitability Map (per-crop layer).
- Tabs: Suitability / Comparison / Calendar / Best Practices.
- "Why is X suitable" reasons, expected yield range, risk level.
- **Deliverable:** Screen 2 from Image 1.

### Phase 8 — Water Management Module
- Soil moisture status, water stress trend, requirement vs availability, irrigation scheduling advisory.
- **Deliverable:** water module reading `WaterBalance` + `IrrigationAdvisory`.

### Phase 9 — Future Outlook Module ⭐
- Scenario selector (SSP2-4.5 etc.).
- Tabs: Climate Outlook / Crop Suitability Trend / Water Outlook / Risk Outlook.
- Trend line charts (`CropSuitabilityTrend`), per-decade resilience scores, key insights.
- **Deliverable:** Screen 4 from Image 1 — your strongest differentiator.

### Phase 10 — Alerts & Notifications
- List with category tabs + severity badges; mark-as-read; bell counter in top bar.
- Distinguish **strategic** alerts ("Paddy suitability declining after 2032") from weather/crop alerts.
- **Deliverable:** Screen 5 from Image 1.

### Phase 11 — Reports & PDF
- Report types listing + generate + download (WeasyPrint HTML templates → PDF).
- Village/Farm Climate Report bundling profile + suitability + rainfall/water outlook + risk indicators (useful for banks/FPOs/NABARD).
- **Deliverable:** Screen 6 from Image 1 with working downloads.

### Phase 12 — Weather & Climate + Market Insights + Settings + Help
- Weather & Climate summary screen; light Market Insights placeholder; Settings (profile/location/units/notifications); Help/FAQ.
- **Deliverable:** all 11 sidebar items reachable and functional.

### Phase 13 — Mobile Responsiveness
- Responsive breakpoints; mobile farmer views for Dashboard / Crop Advisory / Future Outlook / Alerts (Screen 7 from Image 1).
- **Deliverable:** usable on phone screens.

### Phase 14 — Automation & Deployment
- Celery + Redis: scheduled alert generation + (placeholder) data-refresh tasks.
- Dockerized deploy (Gunicorn + Nginx), static/media handling, env secrets, backups.
- **Deliverable:** live, scheduled jobs running.

---

## 6. Build Order / Dependency Notes
- Phases **0→4 are mandatory foundation** — don't start UI screens before the API + shell exist.
- Phases **5–12 are independent** once the API exists; you can reorder by priority. Suggested priority: **5 → 7 → 9** (the three ⭐ hero screens) first to get a demo-able product, then 6, 8, 10, 11, 12.
- Keep the rule: *templates read from API/DB only, never hardcode metrics.*

## 7. Phase 2 (Post-MVP, not now)
Real data pipelines (IMD/GEE/CMIP6), Irrigation Intelligence (demand forecasts, reservoir/canal integration), Financial Intelligence (climate-adjusted profitability, lending risk), Insurance Intelligence (drought/extreme-rainfall risk scoring), full Market Insights, native mobile app on the same API.

---

### One-line summary to give Antigravity per task
> "Build Phase N of FloodGuard Agri Intelligence (Django 5 + DRF + PostGIS + Tailwind/Alpine, API-first). Here is the model spec and the target screen. All displayed metrics must read from the database. Match the provided mockup."
