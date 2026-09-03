import duckdb
import math

con = duckdb.connect("metropulse.duckdb")

print("=" * 60)
print("STATISTICAL COMPARISON TESTS (two-sample)")
print("=" * 60)

print("\n--- Comparison 1: Rain/Snow days vs Dry days (avg daily trips) ---")
group_stats = con.execute("""
    SELECT is_precipitation_day, AVG(total_trips), STDDEV(total_trips), COUNT(*)
    FROM mart_daily_summary_clean
    GROUP BY is_precipitation_day
""").fetchall()

groups = {}
for is_precip, mean, std, n in group_stats:
    label = "rain" if is_precip else "dry"
    groups[label] = {"mean": mean, "std": std, "n": n}
    print(f"{label}: mean={mean:,.1f}, std={std:,.1f}, n={n}")

m1, s1, n1 = groups["rain"]["mean"], groups["rain"]["std"], groups["rain"]["n"]
m2, s2, n2 = groups["dry"]["mean"], groups["dry"]["std"], groups["dry"]["n"]

se_diff = math.sqrt((s1**2 / n1) + (s2**2 / n2))
t_stat = (m1 - m2) / se_diff
diff = m1 - m2
ci_diff_lower = diff - 1.96 * se_diff
ci_diff_upper = diff + 1.96 * se_diff

print(f"\nDifference in means (rain - dry): {diff:,.1f} trips")
print(f"95% CI for the difference: ({ci_diff_lower:,.1f}, {ci_diff_upper:,.1f})")
print(f"t-statistic: {t_stat:.3f}")
if ci_diff_lower <= 0 <= ci_diff_upper:
    print("CONCLUSION: The 95% CI for the difference includes 0.")
    print("This means we CANNOT conclude there is a statistically significant")
    print("difference in taxi demand between rain and dry days at the 95% level.")
    print("This statistically confirms the contrarian finding.")
else:
    print("CONCLUSION: The 95% CI for the difference does NOT include 0.")
    print("This suggests a statistically significant difference exists.")

print("\n\n--- Comparison 2: Airport pickups vs Non-airport pickups (avg fare) ---")
airport_stats = con.execute("""
    SELECT
        CASE WHEN pickup_zone_name IN ('JFK Airport', 'LaGuardia Airport') THEN 'airport' ELSE 'non_airport' END AS trip_type,
        AVG(total_amount), STDDEV(total_amount), COUNT(*)
    FROM mart_trips_clean
    WHERE total_amount > 0
    GROUP BY trip_type
""").fetchall()

a_groups = {}
for trip_type, mean, std, n in airport_stats:
    a_groups[trip_type] = {"mean": mean, "std": std, "n": n}
    print(f"{trip_type}: mean=${mean:.2f}, std=${std:.2f}, n={n:,}")

m1, s1, n1 = a_groups["airport"]["mean"], a_groups["airport"]["std"], a_groups["airport"]["n"]
m2, s2, n2 = a_groups["non_airport"]["mean"], a_groups["non_airport"]["std"], a_groups["non_airport"]["n"]

se_diff2 = math.sqrt((s1**2 / n1) + (s2**2 / n2))
diff2 = m1 - m2
ci2_lower = diff2 - 1.96 * se_diff2
ci2_upper = diff2 + 1.96 * se_diff2
t_stat2 = diff2 / se_diff2

print(f"\nDifference in means (airport - non_airport): ${diff2:.2f}")
print(f"95% CI for the difference: (${ci2_lower:.2f}, ${ci2_upper:.2f})")
print(f"t-statistic: {t_stat2:.3f}")
if ci2_lower <= 0 <= ci2_upper:
    print("CONCLUSION: No statistically significant difference.")
else:
    print("CONCLUSION: Statistically significant difference - airport trips")
    print("have a meaningfully different average fare than non-airport trips.")
    print("(Given huge sample size here, even small real differences will show as significant -")
    print("worth reporting the effect size in dollars, not just significance, for practical relevance.)")

con.close() 