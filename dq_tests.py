import duckdb

con = duckdb.connect("metropulse.duckdb")

tests = []

def run_test(name, query, threshold=0, description=""):
    """Runs a query that counts violating rows. Test passes if count <= threshold."""
    count = con.execute(query).fetchone()[0]
    status = "PASS" if count <= threshold else "FAIL"
    tests.append({
        "name": name,
        "status": status,
        "violation_count": count,
        "description": description
    })
    print(f"[{status}] {name}: {count:,} violating rows")

print("Running data quality tests on mart_trips and mart_daily_summary...\n")

run_test(
    "no_negative_fares",
    "SELECT COUNT(*) FROM mart_trips WHERE fare_amount < 0",
    description="fare_amount should never be negative"
)

run_test(
    "no_negative_totals",
    "SELECT COUNT(*) FROM mart_trips WHERE total_amount < 0",
    description="total_amount should never be negative"
)

run_test(
    "zero_distance_nonzero_fare",
    "SELECT COUNT(*) FROM mart_trips WHERE trip_distance = 0 AND fare_amount > 5",
    description="trips with 0 distance but a real fare charged suggest GPS/meter errors"
)

run_test(
    "no_zero_passengers",
    "SELECT COUNT(*) FROM mart_trips WHERE passenger_count = 0 OR passenger_count IS NULL",
    description="passenger_count should be at least 1"
)

run_test(
    "no_zero_duration_trips",
    "SELECT COUNT(*) FROM mart_trips WHERE trip_duration_minutes <= 0",
    description="a real trip cannot have zero or negative duration"
)

run_test(
    "no_extreme_duration_trips",
    "SELECT COUNT(*) FROM mart_trips WHERE trip_duration_minutes > 240",
    description="trips longer than 4 hours are almost certainly meter errors, not real trips"
)

run_test(
    "pickup_date_in_range",
    "SELECT COUNT(*) FROM mart_trips WHERE pickup_date < '2024-03-25' OR pickup_date > '2024-07-05'",
    description="pickup dates should fall within the Apr-Jun 2024 study window (small buffer for legitimate month-boundary spillover)"
)

run_test(
    "known_zones_only",
    "SELECT COUNT(*) FROM mart_trips WHERE pickup_borough IN ('Unknown', 'N/A') OR dropoff_borough IN ('Unknown', 'N/A')",
    description="trips should map to a real, identifiable NYC borough"
)

run_test(
    "no_extreme_fare_outliers",
    "SELECT COUNT(*) FROM mart_trips WHERE total_amount > 500",
    description="single-trip fares over $500 are extreme outliers, likely data errors"
)

run_test(
    "reasonable_tip_percentage",
    "SELECT COUNT(*) FROM mart_trips WHERE tip_percentage > 100",
    description="tips exceeding 100% of the fare are unusual and worth flagging"
)

run_test(
    "daily_summary_has_weather",
    "SELECT COUNT(*) FROM mart_daily_summary WHERE temp_max_c IS NULL",
    description="every day in the study window should have matching weather data"
)

run_test(
    "daily_summary_has_subway",
    "SELECT COUNT(*) FROM mart_daily_summary WHERE total_subway_ridership IS NULL",
    description="every day in the study window should have matching subway ridership data"
)

print(f"\n{'='*50}")
passed = sum(1 for t in tests if t["status"] == "PASS")
failed = sum(1 for t in tests if t["status"] == "FAIL")
print(f"Total tests: {len(tests)} | Passed: {passed} | Failed: {failed}")

con.close()