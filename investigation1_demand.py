import duckdb

con = duckdb.connect("metropulse.duckdb")

print("=" * 60)
print("INVESTIGATION 1: DEMAND PATTERNS")
print("=" * 60)

print("\n--- Trips by hour of day ---")
by_hour = con.execute("""
    SELECT pickup_hour, COUNT(*) AS trip_count
    FROM mart_trips_clean
    GROUP BY pickup_hour
    ORDER BY pickup_hour
""").fetchall()
for hour, count in by_hour:
    print(f"Hour {hour:2d}: {count:,} trips")

print("\n--- Trips by day of week (0=Sunday, 6=Saturday) ---")
by_dow = con.execute("""
    SELECT pickup_day_of_week, COUNT(*) AS trip_count
    FROM mart_trips_clean
    GROUP BY pickup_day_of_week
    ORDER BY pickup_day_of_week
""").fetchall()
for dow, count in by_dow:
    print(f"Day {dow}: {count:,} trips")

print("\n--- Trips by pickup borough ---")
by_borough = con.execute("""
    SELECT pickup_borough, COUNT(*) AS trip_count,
           ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS pct_of_total
    FROM mart_trips_clean
    GROUP BY pickup_borough
    ORDER BY trip_count DESC
""").fetchall()
for borough, count, pct in by_borough:
    print(f"{borough}: {count:,} trips ({pct}%)")

print("\n--- Peak hour identification ---")
peak = con.execute("""
    SELECT pickup_hour, COUNT(*) AS trip_count
    FROM mart_trips_clean
    GROUP BY pickup_hour
    ORDER BY trip_count DESC
    LIMIT 3
""").fetchall()
print("Top 3 busiest hours:")
for hour, count in peak:
    print(f"  Hour {hour}: {count:,} trips")

lowest = con.execute("""
    SELECT pickup_hour, COUNT(*) AS trip_count
    FROM mart_trips_clean
    GROUP BY pickup_hour
    ORDER BY trip_count ASC
    LIMIT 3
""").fetchall()
print("\nQuietest 3 hours:")
for hour, count in lowest:
    print(f"  Hour {hour}: {count:,} trips")

con.close()