# MetroPulse: NYC Urban Mobility Analytics

An end-to-end data pipeline and analytics platform analyzing NYC taxi, weather,
and subway data (April-June 2024), built for the Dexter Platform LLC technical
assessment.

## Live Dashboard
https://metropulse-bhentzcka6eqvjrknrsmwv.streamlit.app/

## Project Structure

metropulse/
- ingest_taxi.py           - Raw layer: NYC TLC taxi trip data (3 months)
- ingest_zones.py          - Raw layer: taxi zone lookup table
- ingest_weather.py        - Raw layer: Open-Meteo weather API
- ingest_subway.py         - Raw layer: MTA subway ridership data
- raw_ingestion_log.py     - Source integrity log (URLs, timestamps, row counts, schema fingerprints)
- stage_taxi.py            - Staging: clean/standardize taxi data
- stage_zones.py           - Staging: clean/standardize zone data
- stage_weather.py         - Staging: clean/standardize weather data
- stage_subway.py          - Staging: clean/standardize subway data
- mart_trips.py            - Mart: taxi trips joined with zone names
- mart_trips_clean.py      - Mart: cleaned trips with documented exclusion rules
- mart_daily_summary_clean.py  - Mart: daily rollup joining taxi + weather + subway
- dq_tests.py              - 12 automated data quality tests
- check_date_range.py      - Investigation: date range anomaly check
- investigation1_demand.py       - Demand patterns by hour/day/borough
- investigation2_geospatial.py   - Top zones, routes, cross-borough analysis
- investigation3_fare_tipping.py - Fare and tipping behavior
- investigation4_weather.py      - Weather impact on demand
- investigation5_subway.py       - Subway-taxi relationship
- investigation6_anomalies.py    - Anomaly detection + contrarian finding
- stats_rigor.py           - Confidence intervals (trip-level and day-level)
- stats_comparisons.py     - Two-sample statistical comparisons (rain vs dry, airport vs non-airport)
- check_transit_disruption.py    - Evidence check for a rejected initiative candidate
- pilot_baseline_data.py   - Baseline numbers supporting the 2 pilot designs
- pilot_designs.md         - 4-week pilot designs for both selected initiatives
- build_dashboard_db.py    - Builds the lightweight pre-aggregated dashboard database
- app.py                   - Streamlit dashboard (6 views)
- requirements.txt         - Python dependencies
- metric_dictionary.md     - Definitions of all metrics used
- AI_USAGE.md              - Disclosure of AI assistance used in this project
- metropulse_dashboard.duckdb  - Lightweight pre-aggregated DB (committed, ~4MB)

Note: metropulse.duckdb (the full raw/staging/mart database, several GB) is
excluded via .gitignore and is rebuilt locally by running the ingestion
scripts in order below.

## How to Rebuild the Full Pipeline From Scratch

pip install duckdb pandas requests streamlit pyarrow

# 1. Raw layer
python ingest_taxi.py
python ingest_zones.py
python ingest_weather.py
python ingest_subway.py
python raw_ingestion_log.py

# 2. Staging layer
python stage_taxi.py
python stage_zones.py
python stage_weather.py
python stage_subway.py

# 3. Mart layer
python mart_trips.py
python mart_trips_clean.py
python mart_daily_summary_clean.py

# 4. Data quality tests
python dq_tests.py

# 5. Investigations
python investigation1_demand.py
python investigation2_geospatial.py
python investigation3_fare_tipping.py
python investigation4_weather.py
python investigation5_subway.py
python investigation6_anomalies.py
python stats_rigor.py
python stats_comparisons.py

# 6. Build dashboard database and run locally
python build_dashboard_db.py
streamlit run app.py

## Data Sources
- NYC TLC Yellow Taxi Trip Data (Apr-Jun 2024): https://d37ci6vzurychx.cloudfront.net/trip-data/
- NYC Taxi Zone Lookup Table: https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv
- Open-Meteo Historical Weather API: https://archive-api.open-meteo.com/v1/archive
- MTA Subway Hourly Ridership: https://data.ny.gov/resource/wujg-7c2s.json

## Key Findings
- Peak taxi demand: 6 PM; quietest: 4 AM. Manhattan = 88.76% of pickups.
- JFK Airport is the #2 busiest single pickup zone; airport trips average
  $51.99 more than non-airport trips (statistically significant, 95% CI:
  $51.93-$52.06).
- Contrarian finding: bad weather does NOT significantly increase taxi demand
  (95% CI for the rain-vs-dry difference includes 0), contrary to common
  assumption.
- Moderate positive correlation (0.66) between subway ridership and taxi
  demand - they move together rather than substituting for each other.

## Data Quality
9,218,187 of 10,773,939 raw trip records (85.56%) retained after cleaning.
1,555,752 rows (14.44%) excluded per documented rules - see mart_trips_clean.py
and the Data Quality Status tab on the dashboard for full breakdown.

## Selected Initiatives
1. Off-Manhattan Demand Development (Brooklyn focus) - see pilot_designs.md
2. Airport-Focused Operations (JFK/LaGuardia) - see pilot_designs.md

Two other candidates (weather-triggered planning, transit-disruption response)
were investigated and explicitly rejected with supporting evidence - see
pilot_designs.md.