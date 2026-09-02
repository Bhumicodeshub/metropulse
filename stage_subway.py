import duckdb

con = duckdb.connect("metropulse.duckdb")

con.execute("""
    CREATE OR REPLACE TABLE staging_subway AS
    SELECT
        transit_timestamp::TIMESTAMP AS ridership_timestamp,
        station_complex_id,
        station_complex,
        borough,
        CAST(ridership AS DOUBLE) AS ridership,
        CAST(transfers AS DOUBLE) AS transfers,
        payment_method,
        fare_class_category,
        latitude,
        longitude,
        now() AS staged_at
    FROM raw_subway
    WHERE transit_timestamp IS NOT NULL
      AND ridership IS NOT NULL
""")

total = con.execute("SELECT COUNT(*) FROM staging_subway").fetchone()[0]
raw_total = con.execute("SELECT COUNT(*) FROM raw_subway").fetchone()[0]
print(f"staging_subway: {total:,} rows")
print(f"raw total: {raw_total:,} rows")
print(f"filtered out: {raw_total - total:,} rows")

con.close()
print("Done.")