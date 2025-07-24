import requests
import pandas as pd
import time

cities = {
    "jammu": (32.7266, 74.8570),
    "delhi": (28.6139, 77.2090),
    "mumbai": (19.0760, 72.8777),
    "chennai": (13.0827, 80.2707),
    "kolkata": (22.5726, 88.3639),
    "bangalore": (12.9716, 77.5946),
    "hyderabad": (17.3850, 78.4867),
    "ahmedabad": (23.0225, 72.5714),
    "pune": (18.5204, 73.8567),
    "jaipur": (26.9124, 75.7873),
    "lucknow": (26.8467, 80.9462),
    "kanpur": (26.4499, 80.3319),
    "nagpur": (21.1458, 79.0882),
    "visakhapatnam": (17.6868, 83.2185),
    "kochi": (9.9312, 76.2673),
    "chandigarh": (30.7333, 76.7794),
    "bhopal": (23.2599, 77.4126),
    "vadodara": (22.3072, 73.1812),
    "mysore": (12.2958, 76.6394),
    "coimbatore": (11.0168, 76.9558)
}

start_date = "2020-06-28"
end_date = "2025-06-30"

all_data = []

for city, (lat, lon) in cities.items():
    print(f"\n🌍 Fetching weather for {city}...")
    
    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={lat}&longitude={lon}"
        f"&start_date={start_date}&end_date={end_date}"
        f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,"
        f"rain_sum,snowfall_sum,windspeed_10m_max,relative_humidity_2m_max,relative_humidity_2m_min"
        f"&timezone=Asia%2FKolkata"
    )

    try:
        response = requests.get(url)
        data = response.json()

        if "daily" not in data:
            print(f"⚠️  No 'daily' data returned for {city}")
            continue

        df = pd.DataFrame(data["daily"])
        df["city"] = city
        all_data.append(df)

        print(f"✅ Success for {city}: {len(df)} rows")
        time.sleep(10)  # delay to prevent throttling

    except Exception as e:
        print(f"❌ Error fetching data for {city}: {e}")

# Combine and save
if all_data:
    final_df = pd.concat(all_data, ignore_index=True)
    final_df.to_csv("weather_2020_2025.csv", index=False)
    print("\n✅ All data saved to 'weather_2020_2025.csv'")
else:
    print("\n❌ No data collected.")
