import duckdb

con = duckdb.connect("metropulse.duckdb")

# NYC TLC also publishes a lookup table mapping zone IDs to borough/zone names
zone_url = "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv"

con.execute(f"""
    CREATE OR REPLACE TABLE raw_taxi_zones AS
    SELECT *, now() AS ingested_at
    FROM read_csv_auto('{zone_url}')
""")

count = con.execute("SELECT COUNT(*) FROM raw_taxi_zones").fetchone()[0]
print(f"raw_taxi_zones: {count} rows loaded")

con.close()
print("Done.")