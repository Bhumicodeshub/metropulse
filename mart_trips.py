import duckdb

con = duckdb.connect("metropulse.duckdb")

con.execute("""
    CREATE OR REPLACE TABLE mart_trips AS
    SELECT
        t.vendor_id,
        t.pickup_datetime,
        t.dropoff_datetime,
        t.trip_duration_minutes,
        t.passenger_count,
        t.trip_distance,
        t.rate_code_id,
        t.pickup_zone_id,
        pz.borough AS pickup_borough,
        pz.zone_name AS pickup_zone_name,
        t.dropoff_zone_id,
        dz.borough AS dropoff_borough,
        dz.zone_name AS dropoff_zone_name,
        t.payment_type,
        t.fare_amount,
        t.extra,
        t.mta_tax,
        t.tip_amount,
        t.tolls_amount,
        t.improvement_surcharge,
        t.total_amount,
        t.congestion_surcharge,
        t.source_month,
        CASE WHEN t.fare_amount > 0 THEN ROUND(t.tip_amount / t.fare_amount * 100, 2) ELSE NULL END AS tip_percentage,
        CAST(t.pickup_datetime AS DATE) AS pickup_date,
        EXTRACT(HOUR FROM t.pickup_datetime) AS pickup_hour,
        EXTRACT(DOW FROM t.pickup_datetime) AS pickup_day_of_week,
        now() AS mart_created_at
    FROM staging_taxi t
    LEFT JOIN staging_zones pz ON t.pickup_zone_id = pz.zone_id
    LEFT JOIN staging_zones dz ON t.dropoff_zone_id = dz.zone_id
""")

total = con.execute("SELECT COUNT(*) FROM mart_trips").fetchone()[0]
print(f"mart_trips: {total:,} rows")

unmatched = con.execute("""
    SELECT COUNT(*) FROM mart_trips WHERE pickup_borough IS NULL OR dropoff_borough IS NULL
""").fetchone()[0]
print(f"trips with unmatched zone (no borough found): {unmatched:,}")

con.close()
print("Done.")