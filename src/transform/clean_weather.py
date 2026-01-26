import json
import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

def main():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    all_data = []

    # Loop through all raw JSON files
    for file in RAW_DIR.glob("*.json"):
        county = file.stem.split("_")[0]  # extract county from filename

        with open(file) as f:
            raw = json.load(f)

        # Convert API daily data to a DataFrame
        df = pd.DataFrame({
            "date": raw["daily"]["time"],
            "rain_sum": raw["daily"]["rain_sum"],
            "wind_speed": raw["daily"]["wind_speed_10m_max"],
            "temp_min": raw["daily"]["temperature_2m_min"]
        })

        df["county"] = county.title()
        all_data.append(df)

    # Combine all counties into one table
    final_df = pd.concat(all_data, ignore_index=True)

    # Save clean CSV
    final_df.to_csv(PROCESSED_DIR / "weather_clean.csv", index=False)
    print(f"Saved cleaned data to {PROCESSED_DIR / 'weather_clean.csv'}")

if __name__ == "__main__":
    main()
