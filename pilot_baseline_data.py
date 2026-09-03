import duckdb

con = duckdb.connect("metropulse.duckdb")

print("=" * 60)
print("BASELINE DATA FOR PILOT DESIGN")
print("=" * 60)

print("\n--- Pilot 1 baseline: Non-Manhattan borough trip volume + revenue ---")
baseline1 = con.execute("""
    SELECT pickup_borough, COUNT(*) AS trips,
           ROUND(COUNT(*) / 91.0, 0) AS avg_trips_per_day,
           ROUND(AVG(total_amount), 2) AS avg_fare,
           ROUND(SUM(total_amount), 0) AS total_revenue
    FROM mart_trips_clean
    WHERE pickup_borough IN ('Brooklyn', 'Bronx', 'Queens', 'Staten Island')
    GROUP BY pickup_borough
    ORDER BY trips DESC
""").fetchall()
for borough, trips, per_day, fare, revenue in baseline1:
    print(f"{borough}: {trips:,} trips total, {per_day:,.0f}/day avg, avg fare ${fare}, total revenue ${revenue:,.0f}")

print("\n--- Pilot 2 baseline: Airport pickup daily volume (for sample size reasoning) ---")
baseline2 = con.execute("""
    SELECT COUNT(*) AS total_trips,
           ROUND(COUNT(*) / 91.0, 0) AS avg_per_day,
           ROUND(STDDEV(daily_count), 1) AS std_daily
    FROM mart_trips_clean t
    JOIN (
        SELECT pickup_date, COUNT(*) AS daily_count
        FROM mart_trips_clean
        WHERE pickup_zone_name IN ('JFK Airport', 'LaGuardia Airport')
        GROUP BY pickup_date
    ) d ON t.pickup_date = d.pickup_date
    WHERE t.pickup_zone_name IN ('JFK Airport', 'LaGuardia Airport')
""").fetchone()
print(f"Total airport trips: {baseline2[0]:,}")
print(f"Average per day: {baseline2[1]:,.0f}")
print(f"Std dev of daily count: {baseline2[2]}")

con.close()