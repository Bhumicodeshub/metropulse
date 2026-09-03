import duckdb

con = duckdb.connect("metropulse.duckdb")

print("=" * 60)
print("CHECKING: Transit-disruption response angle")
print("=" * 60)

print("\n--- Days with unusually LOW subway ridership (possible disruptions) ---")
low_subway_days = con.execute("""
    WITH stats AS (
        SELECT AVG(total_subway_ridership) AS mean_sub, STDDEV(total_subway_ridership) AS std_sub
        FROM mart_daily_summary_clean
    )
    SELECT d.the_date, d.total_subway_ridership, d.total_trips
    FROM mart_daily_summary_clean d, stats s
    WHERE d.total_subway_ridership < (s.mean_sub - 1.5 * s.std_sub)
    ORDER BY d.total_subway_ridership ASC
""").fetchall()

if len(low_subway_days) == 0:
    print("No days found with subway ridership more than 1.5 std devs below average.")
    print("This suggests the dataset does not contain clear 'disruption' days -")
    print("subway ridership is fairly stable day-to-day (mostly weekday/weekend variation).")
else:
    for date, subway, taxi in low_subway_days:
        print(f"{date}: subway {subway:,.0f} (low), taxi {taxi:,.0f}")

print("\n--- On the lowest-subway days found, did taxi demand rise relative to normal? ---")
if len(low_subway_days) > 0:
    avg_normal_taxi = con.execute("SELECT AVG(total_trips) FROM mart_daily_summary_clean").fetchone()[0]
    print(f"Normal average taxi demand: {avg_normal_taxi:,.0f}")
    for date, subway, taxi in low_subway_days:
        diff_pct = round((taxi - avg_normal_taxi) / avg_normal_taxi * 100, 1)
        print(f"{date}: taxi demand was {diff_pct:+.1f}% vs normal")

con.close()