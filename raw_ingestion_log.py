import duckdb
import hashlib
from datetime import datetime, timezone

con = duckdb.connect("metropulse.duckdb")

con.execute("""
    CREATE OR REPLACE TABLE raw_ingestion_log (
        source_name VARCHAR,
        source_url VARCHAR,
        extraction_timestamp TIMESTAMP,
        row_count BIGINT,
        column_count INTEGER,
        schema_fingerprint VARCHAR,
        source_period VARCHAR
    )
""")

def log_source(source_name, source_url, table_name, source_period):
    row_count = con.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
    schema = con.execute(f"DESCRIBE {table_name}").fetchall()
    column_count = len(schema)
    schema_string = "|".join(f"{col[0]}:{col[1]}" for col in schema)
    schema_fingerprint = hashlib.sha256(schema_string.encode()).hexdigest()[:16]

    con.execute("""
        INSERT INTO raw_ingestion_log VALUES (?, ?, ?, ?, ?, ?, ?)
    """, [source_name, source_url, datetime.now(timezone.utc), row_count, column_count, schema_fingerprint, source_period])

    print(f"{source_name}: {row_count:,} rows, {column_count} cols, fingerprint {schema_fingerprint}")

log_source(
    "nyc_taxi_april_2024",
    "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-04.parquet",
    "raw_taxi_2024_04",
    "2024-04"
)
log_source(
    "nyc_taxi_may_2024",
    "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-05.parquet",
    "raw_taxi_2024_05",
    "2024-05"
)
log_source(
    "nyc_taxi_june_2024",
    "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-06.parquet",
    "raw_taxi_2024_06",
    "2024-06"
)
log_source(
    "nyc_taxi_zone_lookup",
    "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv",
    "raw_taxi_zones",
    "static reference table"
)
log_source(
    "open_meteo_weather",
    "https://archive-api.open-meteo.com/v1/archive (lat=40.7128, lon=-74.0060)",
    "raw_weather",
    "2024-04-01 to 2024-06-30"
)
log_source(
    "mta_subway_ridership",
    "https://data.ny.gov/resource/wujg-7c2s.json",
    "raw_subway",
    "2024-04-01 to 2024-06-30"
)

print("\n--- Full integrity log ---")
log_rows = con.execute("SELECT * FROM raw_ingestion_log").fetchall()
for row in log_rows:
    print(row)

con.close()
print("\nDone. raw_ingestion_log table created with full source traceability.")
