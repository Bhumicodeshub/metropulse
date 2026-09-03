import duckdb

con = duckdb.connect("metropulse.duckdb")

print("=" * 60)
print("INVESTIGATION 4: WEATHER IMPACT (corrected)")
print("=" * 60)

print("\n--- Demand on precipitation vs non-precipitation days ---")
precip_compare = con.execute("""
    SELECT
        is_precipitation_day,
        COUNT(*) AS num_days,
        ROUND(AVG(total_trips), 0) AS avg_daily_trips,
        ROUND(AVG(avg_tip_percentage), 2) AS avg_tip_pct,
        ROUND(AVG(avg_trip_duration_minutes), 2) AS avg_duration_min
    FROM mart_daily_summary_clean
    GROUP BY is_precipitation_day
""").fetchall()
for is_precip, num_days, avg_trips, avg_tip, avg_dur in precip_compare:
    label = "Rain/Snow day" if is_precip else "Dry day"
    print(f"{label}: {num_days} days, avg {avg_trips:,.0f} trips/day, avg tip {avg_tip}%, avg duration {avg_dur} min")

print("\n--- Correlation: temperature vs daily trip count ---")
temp_corr = con.execute("""
    SELECT ROUND(CORR(temp_max_c, total_trips), 4)
    FROM mart_daily_summary_clean
""").fetchone()[0]
print(f"Correlation (max temp vs trip count): {temp_corr}")

print("\n--- Correlation: precipitation amount vs daily trip count ---")
precip_corr = con.execute("""
    SELECT ROUND(CORR(precipitation_mm, total_trips), 4)
    FROM mart_daily_summary_clean
""").fetchone()[0]
print(f"Correlation (precipitation vs trip count): {precip_corr}")

print("\n--- Correlation: wind speed vs daily trip count ---")
wind_corr = con.execute("""
    SELECT ROUND(CORR(windspeed_max_kmh, total_trips), 4)
    FROM mart_daily_summary_clean
""").fetchone()[0]
print(f"Correlation (wind speed vs trip count): {wind_corr}")

print("\n--- Top 5 highest-demand days and their weather ---")
top_days = con.execute("""
    SELECT the_date, total_trips, temp_max_c, precipitation_mm
    FROM mart_daily_summary_clean
    ORDER BY total_trips DESC
    LIMIT 5
""").fetchall()
for date, trips, temp, precip in top_days:
    print(f"{date}: {trips:,} trips, temp {temp}C, precip {precip}mm")

print("\n--- Bottom 5 lowest-demand days and their weather ---")
bottom_days = con.execute("""
    SELECT the_date, total_trips, temp_max_c, precipitation_mm
    FROM mart_daily_summary_clean
    ORDER BY total_trips ASC
    LIMIT 5
""").fetchall()
for date, trips, temp, precip in bottom_days:
    print(f"{date}: {trips:,} trips, temp {temp}C, precip {precip}mm")

con.close()