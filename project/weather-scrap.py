from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Setup Selenium WebDriver using webdriver-manager
def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

# Scrape weather data from timeanddate.com (for demonstration)
def scrape_weather_data(city):
    driver = init_driver()
    base_url = f"https://www.timeanddate.com/weather/india/{city.lower()}/historic"
    driver.get(base_url)
    time.sleep(3)

    rows = driver.find_elements(By.CSS_SELECTOR, "table.zebra.tb-wt.tb-hover tbody tr")

    data = []
    for row in rows:
        try:
            columns = row.find_elements(By.TAG_NAME, "td")
            if len(columns) >= 6:
                record = {
                    "time": columns[0].text,
                    "temperature": columns[1].text,
                    "weather": columns[2].text,
                    "wind": columns[3].text,
                    "humidity": columns[5].text,
                    "location": city.title()
                }
                data.append(record)
        except Exception as e:
            print(f"Row error: {e}")

    driver.quit()
    return pd.DataFrame(data)

# Cities to scrape
cities = ["jammu", "delhi", "mumbai", "bangalore"]
all_data = []

for city in cities:
    try:
        print(f"Scraping data for {city.title()}...")
        df = scrape_weather_data(city)
        if not df.empty:
            all_data.append(df)
        time.sleep(2)
    except Exception as e:
        print(f"Error scraping {city}: {e}")

# Save all scraped data
if all_data:
    result = pd.concat(all_data)
    result.to_csv("weather_scraped_from_timeanddate.csv", index=False)
    print("✅ Scraped weather data saved successfully.")
else:
    print("❌ No data scraped.")
