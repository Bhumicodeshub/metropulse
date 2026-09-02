import duckdb

con = duckdb.connect("metropulse.duckdb")

print("=== Date range in mart_trips (pickup_date) ===")
result = con.execute("SELECT MIN(pickup_date), MAX(pickup_date) FROM mart_trips").fetchone()
print(f"Min: {result[0]}, Max: {result[1]}")

print("\n=== Dates outside Apr 1 - Jun 30 2024 ===")
outliers = con.execute("""
    SELECT pickup_date, COUNT(*) AS trip_count
    FROM mart_trips
    WHERE pickup_date < '2024-04-01' OR pickup_date > '2024-06-30'
    GROUP BY pickup_date
    ORDER BY pickup_date
""").fetchall()
for row in outliers:
    print(row)

print(f"\nTotal out-of-range dates found: {len(outliers)}")

con.close()  