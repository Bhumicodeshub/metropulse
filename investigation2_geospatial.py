import duckdb

con = duckdb.connect("metropulse.duckdb")

print("=" * 60)
print("INVESTIGATION 2: GEOSPATIAL PATTERNS")
print("=" * 60)

print("\n--- Top 10 busiest pickup zones ---")
top_pickup = con.execute("""
    SELECT pickup_zone_name, pickup_borough, COUNT(*) AS trip_count
    FROM mart_trips_clean
    WHERE pickup_zone_name IS NOT NULL
    GROUP BY pickup_zone_name, pickup_borough
    ORDER BY trip_count DESC
    LIMIT 10
""").fetchall()
for zone, borough, count in top_pickup:
    print(f"{zone} ({borough}): {count:,} trips")

print("\n--- Top 10 busiest dropoff zones ---")
top_dropoff = con.execute("""
    SELECT dropoff_zone_name, dropoff_borough, COUNT(*) AS trip_count
    FROM mart_trips_clean
    WHERE dropoff_zone_name IS NOT NULL
    GROUP BY dropoff_zone_name, dropoff_borough
    ORDER BY trip_count DESC
    LIMIT 10
""").fetchall()
for zone, borough, count in top_dropoff:
    print(f"{zone} ({borough}): {count:,} trips")

print("\n--- Top 10 busiest routes (pickup -> dropoff pairs) ---")
top_routes = con.execute("""
    SELECT pickup_zone_name, dropoff_zone_name, COUNT(*) AS trip_count,
           ROUND(AVG(trip_distance), 2) AS avg_distance,
           ROUND(AVG(total_amount), 2) AS avg_fare
    FROM mart_trips_clean
    WHERE pickup_zone_name IS NOT NULL AND dropoff_zone_name IS NOT NULL
    GROUP BY pickup_zone_name, dropoff_zone_name
    ORDER BY trip_count DESC
    LIMIT 10
""").fetchall()
for pu, do, count, dist, fare in top_routes:
    print(f"{pu} -> {do}: {count:,} trips, avg {dist} mi, avg ${fare}")

print("\n--- Cross-borough vs within-borough trips ---")
cross_borough = con.execute("""
    SELECT
        CASE WHEN pickup_borough = dropoff_borough THEN 'Within-borough' ELSE 'Cross-borough' END AS trip_type,
        COUNT(*) AS trip_count,
        ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS pct
    FROM mart_trips_clean
    WHERE pickup_borough IS NOT NULL AND dropoff_borough IS NOT NULL
    GROUP BY trip_type
""").fetchall()
for trip_type, count, pct in cross_borough:
    print(f"{trip_type}: {count:,} trips ({pct}%)")

con.close()