import requests
import pandas as pd
from datetime import datetime
from geopy.geocoders import Nominatim

def get_coordinates(city_name):
    geolocator = Nominatim(user_agent="climate2cure")
    location = geolocator.geocode(city_name)
    if not location:
        raise ValueError(f"City '{city_name}' not found.")
    return location.latitude, location.longitude

def fetch_weather_data(city, start_date, end_date, output_file):
    lat, lon = get_coordinates(city)
    print(f"Coordinates for {city}: {lat}, {lon}")

    url = f"https://archive-api.open-meteo.com/v1/archive?" \
          f"latitude={lat}&longitude={lon}" \
          f"&start_date={start_date}&end_date={end_date}" \
          f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum," \
          f"rain_sum,snowfall_sum,windspeed_10m_max," \
          f"relative_humidity_2m_max,relative_humidity_2m_min" \
          f"&timezone=Asia%2FKolkata"

    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"API request failed: {response.status_code}")

    data = response.json()
    df = pd.DataFrame(data.get("daily", {}))
    df["location"] = city
    df["date"] = pd.to_datetime(df["time"])

    df.to_csv(output_file, index=False)
    print(f"✅ Weather data saved to {output_file}")

# Example usage
fetch_weather_data(
    city="Jammu",
    start_date="2020-01-01",
    end_date="2025-06-30",
    output_file="jammu_weather_2020_2025_improved.csv"
)
