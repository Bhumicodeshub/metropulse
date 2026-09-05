import duckdb
import os

os.makedirs("data/raw", exist_ok=True)

months = ["2024-04", "2024-05", "2024-06"]
base_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{}.parquet"

con = duckdb.connect("metropulse.duckdb")

for month in months:
    url = base_url.format(month)
    table_name = f"raw_taxi_{month.replace('-', '_')}"
    print(f"Loading {month}...")
    con.execute(f"""
        CREATE OR REPLACE TABLE {table_name} AS
        SELECT *, '{month}' AS source_month, now() AS ingested_at
        FROM read_parquet('{url}')
    """)
    count = con.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
    print(f"  {table_name}: {count:,} rows loaded")

con.close()
print("Done. Data saved in metropulse.duckdb")