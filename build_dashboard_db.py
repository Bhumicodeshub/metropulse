import duckdb
import os

con = duckdb.connect("metropulse.duckdb")
con.execute("ATTACH 'metropulse_dashboard.duckdb' AS dash")

con.execute("CREATE OR REPLACE TABLE dash.mart_daily_summary_clean AS SELECT * FROM mart_daily_summary_clean")

con.execute("""
    CREATE OR REPLACE TABLE dash.agg_hourly_demand AS
    SELECT pickup_borough, pickup_hour, pickup_day_of_week, payment_type, rate_code_id,
           COUNT(*) AS trips,
           ROUND(AVG(total_amount), 2) AS avg_fare, ROUND(AVG(tip_percentage), 2) AS avg_tip_pct
    FROM mart_trips_clean
    GROUP BY pickup_borough, pickup_hour, pickup_day_of_week, payment_type, rate_code_id
""")

con.execute("""
    CREATE OR REPLACE TABLE dash.agg_zone_stats AS
    SELECT pickup_zone_name, pickup_borough, pickup_date, payment_type,
           COUNT(*) AS trips,
           ROUND(AVG(total_amount), 2) AS avg_fare, ROUND(AVG(trip_distance), 2) AS avg_distance
    FROM mart_trips_clean
    WHERE pickup_zone_name IS NOT NULL
    GROUP BY pickup_zone_name, pickup_borough, pickup_date, payment_type
""")

con.execute("""
    CREATE OR REPLACE TABLE dash.agg_payment_stats AS
    SELECT payment_type, rate_code_id, pickup_date, pickup_borough,
           COUNT(*) AS trips,
           ROUND(AVG(tip_percentage), 2) AS avg_tip_pct, ROUND(AVG(total_amount), 2) AS avg_fare
    FROM mart_trips_clean
    GROUP BY payment_type, rate_code_id, pickup_date, pickup_borough
""")

con.execute("""
    CREATE OR REPLACE TABLE dash.agg_daily_borough_totals AS
    SELECT pickup_date, pickup_borough, payment_type, rate_code_id,
           COUNT(*) AS trips,
           SUM(total_amount) AS revenue, AVG(total_amount) AS avg_fare, AVG(tip_percentage) AS avg_tip_pct
    FROM mart_trips_clean
    WHERE pickup_borough IS NOT NULL
    GROUP BY pickup_date, pickup_borough, payment_type, rate_code_id
""")

con.execute("""
    CREATE OR REPLACE TABLE dash.agg_dropoff_stats AS
    SELECT pickup_borough, dropoff_borough, pickup_date, pickup_hour,
           COUNT(*) AS trips,
           ROUND(AVG(total_amount), 2) AS avg_fare
    FROM mart_trips_clean
    WHERE dropoff_borough IS NOT NULL
    GROUP BY pickup_borough, dropoff_borough, pickup_date, pickup_hour
""")

con.execute("CREATE OR REPLACE TABLE dash.raw_ingestion_log AS SELECT * FROM raw_ingestion_log")

con.execute("""
    CREATE OR REPLACE TABLE dash.dq_summary AS
    SELECT * FROM (VALUES
        ('no_negative_fares', 179170),
        ('no_negative_totals', 141530),
        ('zero_distance_nonzero_fare', 93898),
        ('no_zero_passengers', 1337919),
        ('no_extreme_duration_trips', 6255),
        ('pickup_date_in_range', 17),
        ('known_zones_only', 110065),
        ('no_extreme_fare_outliers', 178),
        ('reasonable_tip_percentage', 12978)
    ) AS t(test_name, violation_count)
""")

con.execute("""
    CREATE OR REPLACE TABLE dash.reconciliation AS
    SELECT 'mart_trips (before cleaning)' AS stage, COUNT(*) AS row_count FROM mart_trips
    UNION ALL
    SELECT 'mart_trips_clean (after cleaning)' AS stage, COUNT(*) AS row_count FROM mart_trips_clean
""")

con.execute("DETACH dash")
con.close()

size_mb = os.path.getsize("metropulse_dashboard.duckdb") / (1024 * 1024)
print(f"metropulse_dashboard.duckdb rebuilt: {size_mb:.2f} MB")