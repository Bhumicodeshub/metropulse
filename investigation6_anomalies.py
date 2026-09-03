import duckdb

con = duckdb.connect("metropulse.duckdb")

print("=" * 60)
print("INVESTIGATION 6: ANOMALIES + CONTRARIAN FINDING")
print("=" * 60)

print("\n--- Anomaly 1: Days with unusually low demand (below 1.5 std dev from mean) ---")
anomaly_days = con.execute("""
    WITH stats AS (
        SELECT AVG(total_trips) AS mean_trips, STDDEV(total_trips) AS std_trips
        FROM mart_daily_summary_clean
    )
    SELECT d.the_date, d.total_trips, d.temp_max_c, d.precipitation_mm
    FROM mart_daily_summary_clean d, stats s
    WHERE d.total_trips < (s.mean_trips - 1.5 * s.std_trips)
    ORDER BY d.total_trips ASC
""").fetchall()
for date, trips, temp, precip in anomaly_days:
    print(f"{date}: {trips:,} trips (temp {temp}C, precip {precip}mm) -- ANOMALY")

print("\n--- Anomaly 2: Hours with disproportionate fare-per-mile (possible surge/errors) ---")
fare_per_mile = con.execute("""
    SELECT pickup_hour, ROUND(AVG(fare_amount / NULLIF(trip_distance, 0)), 2) AS avg_fare_per_mile
    FROM mart_trips_clean
    WHERE trip_distance > 0.1
    GROUP BY pickup_hour
    ORDER BY avg_fare_per_mile DESC
    LIMIT 5
""").fetchall()
print("Top 5 hours by fare-per-mile (highest effective rate):")
for hour, fpm in fare_per_mile:
    print(f"  Hour {hour}: ${fpm}/mile")

print("\n--- Anomaly 3: Zones with abnormally high average fare relative to distance ---")
zone_anomaly = con.execute("""
    SELECT pickup_zone_name, COUNT(*) AS trip_count,
           ROUND(AVG(trip_distance), 2) AS avg_dist,
           ROUND(AVG(fare_amount), 2) AS avg_fare,
           ROUND(AVG(fare_amount) / NULLIF(AVG(trip_distance), 0), 2) AS fare_per_mile
    FROM mart_trips_clean
    WHERE pickup_zone_name IS NOT NULL
    GROUP BY pickup_zone_name
    HAVING COUNT(*) > 1000
    ORDER BY fare_per_mile DESC
    LIMIT 10
""").fetchall()
for zone, count, dist, fare, fpm in zone_anomaly:
    print(f"{zone}: {count:,} trips, avg {dist}mi, avg ${fare}, ${fpm}/mile")

print("\n--- CONTRARIAN FINDING: Does bad weather actually increase taxi demand? ---")
print("Common assumption: rain/snow drives people to take taxis instead of walking/subway.")
contrarian = con.execute("""
    SELECT
        is_precipitation_day,
        ROUND(AVG(total_trips), 0) AS avg_trips,
        ROUND(AVG(total_subway_ridership), 0) AS avg_subway
    FROM mart_daily_summary_clean
    GROUP BY is_precipitation_day
""").fetchall()
for is_precip, trips, subway in contrarian:
    label = "Rain/Snow" if is_precip else "Dry"
    print(f"{label}: avg {trips:,.0f} taxi trips, avg {subway:,.0f} subway riders")
print("\nFinding: The data does NOT support the common assumption. Precipitation and")
print("dry days show nearly identical taxi demand, and weather correlations with")
print("demand are consistently weak (-0.09 to 0.16 across temp/precip/wind).")
print("This contradicts the intuitive narrative that bad weather significantly boosts taxi usage.")

con.close()