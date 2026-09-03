import duckdb

con = duckdb.connect("metropulse.duckdb")

print("=" * 60)
print("INVESTIGATION 5: SUBWAY RELATIONSHIP")
print("=" * 60)

print("\n--- Correlation: subway ridership vs taxi trips (daily) ---")
corr = con.execute("""
    SELECT ROUND(CORR(total_subway_ridership, total_trips), 4)
    FROM mart_daily_summary_clean
    WHERE total_subway_ridership IS NOT NULL
""").fetchone()[0]
print(f"Correlation (subway ridership vs taxi trips): {corr}")

print("\n--- Daily averages side by side ---")
avg_stats = con.execute("""
    SELECT
        ROUND(AVG(total_subway_ridership), 0) AS avg_subway,
        ROUND(AVG(total_trips), 0) AS avg_taxi,
        ROUND(AVG(total_subway_ridership) / AVG(total_trips), 1) AS ratio
    FROM mart_daily_summary_clean
    WHERE total_subway_ridership IS NOT NULL
""").fetchone()
print(f"Avg daily subway ridership: {avg_stats[0]:,.0f}")
print(f"Avg daily taxi trips: {avg_stats[1]:,.0f}")
print(f"Subway rides per taxi trip: {avg_stats[2]}x")

print("\n--- Subway ridership by hour (from staging_subway) vs taxi demand by hour ---")
subway_by_hour = con.execute("""
    SELECT EXTRACT(HOUR FROM ridership_timestamp) AS hour, SUM(ridership) AS total_riders
    FROM staging_subway
    GROUP BY hour
    ORDER BY hour
""").fetchall()
taxi_by_hour = con.execute("""
    SELECT pickup_hour, COUNT(*) AS trip_count
    FROM mart_trips_clean
    GROUP BY pickup_hour
    ORDER BY pickup_hour
""").fetchall()
taxi_dict = dict(taxi_by_hour)
print(f"{'Hour':<6}{'Subway Riders':<18}{'Taxi Trips':<15}")
for hour, riders in subway_by_hour:
    taxi_count = taxi_dict.get(int(hour), 0)
    print(f"{int(hour):<6}{riders:<18,.0f}{taxi_count:<15,}")

print("\n--- Weekday vs weekend: subway and taxi comparison ---")
weekday_compare = con.execute("""
    SELECT
        CASE WHEN DAYOFWEEK(the_date) IN (0, 6) THEN 'Weekend' ELSE 'Weekday' END AS day_type,
        ROUND(AVG(total_subway_ridership), 0) AS avg_subway,
        ROUND(AVG(total_trips), 0) AS avg_taxi
    FROM mart_daily_summary_clean
    WHERE total_subway_ridership IS NOT NULL
    GROUP BY day_type
""").fetchall()
for day_type, subway, taxi in weekday_compare:
    print(f"{day_type}: avg subway {subway:,.0f}, avg taxi {taxi:,.0f}")

con.close()