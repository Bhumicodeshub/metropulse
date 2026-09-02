import duckdb

con = duckdb.connect("metropulse.duckdb")

con.execute("""
    CREATE OR REPLACE TABLE staging_weather AS
    SELECT
        CAST(time AS DATE) AS weather_date,
        temperature_2m_max AS temp_max_c,
        temperature_2m_min AS temp_min_c,
        precipitation_sum AS precipitation_mm,
        rain_sum AS rain_mm,
        snowfall_sum AS snowfall_cm,
        windspeed_10m_max AS windspeed_max_kmh,
        now() AS staged_at
    FROM raw_weather
    WHERE time IS NOT NULL
""")

total = con.execute("SELECT COUNT(*) FROM staging_weather").fetchone()[0]
raw_total = con.execute("SELECT COUNT(*) FROM raw_weather").fetchone()[0]
print(f"staging_weather: {total} rows")
print(f"raw total: {raw_total} rows")

con.close()
print("Done.")