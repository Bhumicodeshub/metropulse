import duckdb

con = duckdb.connect("metropulse.duckdb")

con.execute("""
    CREATE OR REPLACE TABLE staging_zones AS
    SELECT
        LocationID AS zone_id,
        Borough AS borough,
        Zone AS zone_name,
        service_zone,
        now() AS staged_at
    FROM raw_taxi_zones
    WHERE LocationID IS NOT NULL
""")

total = con.execute("SELECT COUNT(*) FROM staging_zones").fetchone()[0]
print(f"staging_zones: {total} rows")

con.close()
print("Done.")