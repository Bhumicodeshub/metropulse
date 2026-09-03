import duckdb

con = duckdb.connect("metropulse.duckdb")

con.execute("""
    CREATE OR REPLACE TABLE mart_trips_clean AS
    SELECT *
    FROM mart_trips
    WHERE
        fare_amount >= 0
        AND total_amount >= 0
        AND NOT (trip_distance = 0 AND fare_amount > 5)
        AND passenger_count > 0
        AND trip_duration_minutes <= 240
        AND pickup_date >= '2024-03-25' AND pickup_date <= '2024-07-05'
        AND total_amount <= 500
""")

clean_count = con.execute("SELECT COUNT(*) FROM mart_trips_clean").fetchone()[0]
original_count = con.execute("SELECT COUNT(*) FROM mart_trips").fetchone()[0]
excluded = original_count - clean_count
pct_excluded = round(excluded / original_count * 100, 2)

print(f"Original mart_trips: {original_count:,} rows")
print(f"Clean mart_trips_clean: {clean_count:,} rows")
print(f"Excluded: {excluded:,} rows ({pct_excluded}%)")

con.close()
print("Done.")