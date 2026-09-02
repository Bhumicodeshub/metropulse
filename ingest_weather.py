import duckdb
import requests
import pandas as pd

# NYC coordinates
latitude = 40.7128
longitude = -74.0060

url = "https://archive-api.open-meteo.com/v1/archive"
params = {
    "latitude": latitude,
    "longitude": longitude,
    "start_date": "2024-04-01",
    "end_date": "2024-06-30",
    "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,rain_sum,snowfall_sum,windspeed_10m_max",
    "timezone": "America/New_York"
}

print("Calling Open-Meteo API...")
response = requests.get(url, params=params)
response.raise_for_status()  # will error out clearly if the API call fails
data = response.json()

# Convert the JSON "daily" section into a table (DataFrame)
weather_df = pd.DataFrame(data["daily"])

con = duckdb.connect("metropulse.duckdb")
con.execute("CREATE OR REPLACE TABLE raw_weather AS SELECT *, now() AS ingested_at FROM weather_df")

count = con.execute("SELECT COUNT(*) FROM raw_weather").fetchone()[0]
print(f"raw_weather: {count} rows loaded")

con.close()
print("Done.")