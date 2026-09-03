import duckdb

con = duckdb.connect("metropulse.duckdb")

con.execute("""
    CREATE OR REPLACE TABLE mart_daily_summary_clean AS
    WITH daily_taxi AS (
        SELECT
            pickup_date AS the_date,
            COUNT(*) AS total_trips,
            SUM(total_amount) AS total_revenue,
            AVG(trip_distance) AS avg_trip_distance,
            AVG(trip_duration_minutes) AS avg_trip_duration_minutes,
            AVG(tip_percentage) AS avg_tip_percentage
        FROM mart_trips_clean
        GROUP BY pickup_date
    ),
    daily_subway AS (
        SELECT
            CAST(ridership_timestamp AS DATE) AS the_date,
            SUM(ridership) AS total_subway_ridership
        FROM staging_subway
        GROUP BY CAST(ridership_timestamp AS DATE)
    )
    SELECT
        dt.the_date,
        dt.total_trips,
        dt.total_revenue,
        dt.avg_trip_distance,
        dt.avg_trip_duration_minutes,
        dt.avg_tip_percentage,
        ds.total_subway_ridership,
        w.temp_max_c,
        w.temp_min_c,
        w.precipitation_mm,
        w.rain_mm,
        w.snowfall_cm,
        w.windspeed_max_kmh,
        CASE WHEN w.rain_mm > 0 OR w.snowfall_cm > 0 THEN TRUE ELSE FALSE END AS is_precipitation_day,
        now() AS mart_created_at
    FROM daily_taxi dt
    LEFT JOIN daily_subway ds ON dt.the_date = ds.the_date
    LEFT JOIN staging_weather w ON dt.the_date = w.weather_date
    WHERE w.weather_date IS NOT NULL
    ORDER BY dt.the_date
""")

total = con.execute("SELECT COUNT(*) FROM mart_daily_summary_clean").fetchone()[0]
print(f"mart_daily_summary_clean: {total} rows")

date_range = con.execute("SELECT MIN(the_date), MAX(the_date) FROM mart_daily_summary_clean").fetchone()
print(f"Date range: {date_range[0]} to {date_range[1]}")

con.close()
print("Done.")