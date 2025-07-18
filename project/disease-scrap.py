import requests
import pandas as pd

BASE_URL = "https://ghoapi.azureedge.net/api/"
INDICATOR = "MDG_0000000001"  # Confirmed malaria indicator with Country/Year

def fetch_who_data(indicator=INDICATOR, country="India", year_start=2010, year_end=2020):
    query = f"?$filter=Country eq '{country}' and Year ge {year_start} and Year le {year_end}"
    url = BASE_URL + indicator + query
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data["value"])
    except Exception as e:
        print(f"Error: {e}\nURL: {url}")
        return None

df = fetch_who_data()
if df is not None:
    df.to_csv("who_malaria_confirmed.csv", index=False)
    print("Data saved successfully!")