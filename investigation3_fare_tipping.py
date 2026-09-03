import duckdb

con = duckdb.connect("metropulse.duckdb")

print("=" * 60)
print("INVESTIGATION 3: FARE & TIPPING BEHAVIOR")
print("=" * 60)

print("\n--- Overall fare statistics ---")
stats = con.execute("""
    SELECT
        ROUND(AVG(fare_amount), 2) AS avg_fare,
        ROUND(MEDIAN(fare_amount), 2) AS median_fare,
        ROUND(AVG(total_amount), 2) AS avg_total,
        ROUND(AVG(tip_amount), 2) AS avg_tip,
        ROUND(AVG(tip_percentage), 2) AS avg_tip_pct
    FROM mart_trips_clean
    WHERE fare_amount > 0
""").fetchone()
print(f"Average fare: ${stats[0]}")
print(f"Median fare: ${stats[1]}")
print(f"Average total (with extras/tolls/tax): ${stats[2]}")
print(f"Average tip amount: ${stats[3]}")
print(f"Average tip percentage: {stats[4]}%")

print("\n--- Tipping by payment type ---")
by_payment = con.execute("""
    SELECT payment_type, COUNT(*) AS trip_count, ROUND(AVG(tip_percentage), 2) AS avg_tip_pct
    FROM mart_trips_clean
    WHERE fare_amount > 0
    GROUP BY payment_type
    ORDER BY trip_count DESC
""").fetchall()
for ptype, count, tip_pct in by_payment:
    print(f"Payment type {ptype}: {count:,} trips, avg tip {tip_pct}%")

print("\n--- Tipping by pickup borough ---")
by_borough = con.execute("""
    SELECT pickup_borough, ROUND(AVG(tip_percentage), 2) AS avg_tip_pct, COUNT(*) AS trip_count
    FROM mart_trips_clean
    WHERE fare_amount > 0 AND pickup_borough IS NOT NULL
    GROUP BY pickup_borough
    ORDER BY trip_count DESC
""").fetchall()
for borough, tip_pct, count in by_borough:
    print(f"{borough}: avg tip {tip_pct}% ({count:,} trips)")

print("\n--- Tipping by hour of day ---")
by_hour = con.execute("""
    SELECT pickup_hour, ROUND(AVG(tip_percentage), 2) AS avg_tip_pct
    FROM mart_trips_clean
    WHERE fare_amount > 0
    GROUP BY pickup_hour
    ORDER BY pickup_hour
""").fetchall()
for hour, tip_pct in by_hour:
    print(f"Hour {hour:2d}: avg tip {tip_pct}%")

print("\n--- Fare vs trip distance correlation ---")
corr = con.execute("""
    SELECT ROUND(CORR(trip_distance, fare_amount), 4) AS correlation
    FROM mart_trips_clean
    WHERE fare_amount > 0
""").fetchone()[0]
print(f"Correlation between distance and fare: {corr}")

con.close()