import duckdb

con = duckdb.connect("metropulse.duckdb")

print("=" * 60)
print("SUPPORTING DATA FOR OPERATIONAL INITIATIVES")
print("=" * 60)

print("\n--- Initiative 1 support: Manhattan concentration risk ---")
borough_share = con.execute("""
    SELECT pickup_borough, COUNT(*) AS trips,
           ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS pct,
           ROUND(AVG(total_amount), 2) AS avg_fare
    FROM mart_trips_clean
    WHERE pickup_borough IN ('Manhattan', 'Brooklyn', 'Bronx', 'Staten Island')
    GROUP BY pickup_borough
    ORDER BY trips DESC
""").fetchall()
for borough, trips, pct, fare in borough_share:
    print(f"{borough}: {trips:,} trips ({pct}%), avg fare ${fare}")

print("\n--- Initiative 2 support: JFK/LGA airport demand consistency ---")
airport_by_hour = con.execute("""
    SELECT pickup_hour, COUNT(*) AS trips
    FROM mart_trips_clean
    WHERE pickup_zone_name IN ('JFK Airport', 'LaGuardia Airport')
    GROUP BY pickup_hour
    ORDER BY pickup_hour
""").fetchall()
print("Airport pickups by hour:")
for hour, trips in airport_by_hour:
    print(f"  Hour {hour}: {trips:,} trips")

airport_total = con.execute("""
    SELECT COUNT(*), ROUND(AVG(total_amount), 2), ROUND(AVG(trip_distance), 2)
    FROM mart_trips_clean
    WHERE pickup_zone_name IN ('JFK Airport', 'LaGuardia Airport')
""").fetchone()
print(f"\nTotal airport pickup trips: {airport_total[0]:,}")
print(f"Average fare: ${airport_total[1]}")
print(f"Average distance: {airport_total[2]} miles")

con.close()