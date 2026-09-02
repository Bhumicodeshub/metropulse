import duckdb

con = duckdb.connect("metropulse.duckdb")

con.execute("""
    CREATE OR REPLACE TABLE staging_taxi AS
    SELECT
        VendorID AS vendor_id,
        tpep_pickup_datetime AS pickup_datetime,
        tpep_dropoff_datetime AS dropoff_datetime,
        passenger_count,
        trip_distance,
        RatecodeID AS rate_code_id,
        PULocationID AS pickup_zone_id,
        DOLocationID AS dropoff_zone_id,
        payment_type,
        fare_amount,
        extra,
        mta_tax,
        tip_amount,
        tolls_amount,
        improvement_surcharge,
        total_amount,
        congestion_surcharge,
        source_month,
        date_diff('second', tpep_pickup_datetime, tpep_dropoff_datetime) / 60.0 AS trip_duration_minutes,
        now() AS staged_at
    FROM (
        SELECT * FROM raw_taxi_2024_04
        UNION ALL BY NAME
        SELECT * FROM raw_taxi_2024_05
        UNION ALL BY NAME
        SELECT * FROM raw_taxi_2024_06
    )
    WHERE tpep_pickup_datetime IS NOT NULL
      AND tpep_dropoff_datetime IS NOT NULL
      AND tpep_pickup_datetime < tpep_dropoff_datetime
""")

total = con.execute("SELECT COUNT(*) FROM staging_taxi").fetchone()[0]
print(f"staging_taxi: {total:,} rows")

raw_total = con.execute("""
    SELECT
        (SELECT COUNT(*) FROM raw_taxi_2024_04) +
        (SELECT COUNT(*) FROM raw_taxi_2024_05) +
        (SELECT COUNT(*) FROM raw_taxi_2024_06)
""").fetchone()[0]
print(f"raw total: {raw_total:,} rows")
print(f"filtered out: {raw_total - total:,} rows (bad pickup/dropoff timestamps)")

con.close()
print("Done.")