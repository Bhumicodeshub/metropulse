import duckdb
import requests
import pandas as pd

# NYC Open Data: MTA Subway Hourly Ridership dataset
# We fetch in a paginated loop since the API caps rows per request
base_url = "https://data.ny.gov/resource/wujg-7c2s.json"

all_records = []
limit = 50000
offset = 0

print("Fetching MTA subway ridership data (this may take a few minutes)...")

while True:
    params = {
        "$where": "transit_timestamp between '2024-04-01T00:00:00' and '2024-06-30T23:59:59'",
        "$limit": limit,
        "$offset": offset
    }
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    batch = response.json()

    if not batch:
        break

    all_records.extend(batch)
    print(f"  Fetched {len(all_records):,} rows so far...")
    offset += limit

subway_df = pd.DataFrame(all_records)

con = duckdb.connect("metropulse.duckdb")
con.execute("CREATE OR REPLACE TABLE raw_subway AS SELECT *, now() AS ingested_at FROM subway_df")

count = con.execute("SELECT COUNT(*) FROM raw_subway").fetchone()[0]
print(f"raw_subway: {count:,} rows loaded")

con.close()
print("Done.")