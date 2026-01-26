import requests
import json
from datetime import date
from counties import COUNTIES
from pathlib import Path

BASE_URL = "https://api.open-meteo.com/v1/forecast"
RAW_DIR = Path("data/raw")

def fetch_weather(lat, lon):
    """Fetch daily weather from Open-Meteo API"""
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "rain_sum,wind_speed_10m_max,temperature_2m_min",
        "timezone": "Europe/Dublin"
    }
    response = requests.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()
    return response.json()

def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()

    for county, coords in COUNTIES.items():
        try:
            data = fetch_weather(coords["lat"], coords["lon"])
            filename = RAW_DIR / f"{county.lower()}_{today}.json"
            with open(filename, "w") as f:
                json.dump(data, f, indent=2)
            print(f"Saved weather data for {county}")
        except Exception as e:
            print(f"Error fetching data for {county}: {e}")

if __name__ == "__main__":
    main()
