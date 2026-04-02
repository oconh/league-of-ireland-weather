"""
Replaces the INSERT in sql/weekly_table.sql.
Reads weather_daily, computes weekly misery scores, writes to county_weekly_misery.
"""
import os
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('DB_USER', 'weather_user')}:"
    f"{os.getenv('DB_PASS', 'weather_pass')}@"
    f"{os.getenv('DB_HOST', 'localhost')}:"
    f"{os.getenv('DB_PORT', '5432')}/"
    f"{os.getenv('DB_NAME', 'weather')}"
)

weather = pd.read_sql_table("weather_daily", engine)
weather["date"] = pd.to_datetime(weather["date"])
weather["week_start"] = weather["date"] - pd.to_timedelta(weather["date"].dt.dayofweek, unit="D")

misery = weather.groupby(["county", "week_start"]).agg(
    avg_rain_mm=("rain_sum", "mean"),
    avg_wind_kmh=("wind_speed", "mean"),
    avg_min_temp=("temp_min", "mean"),
).reset_index()

misery["avg_rain_mm"] = misery["avg_rain_mm"].round(2)
misery["avg_wind_kmh"] = misery["avg_wind_kmh"].round(2)
misery["avg_min_temp"] = misery["avg_min_temp"].round(2)
misery["misery_score"] = (
    misery["avg_rain_mm"] + misery["avg_wind_kmh"] - misery["avg_min_temp"]
).round().astype(int)
misery["week_start"] = misery["week_start"].dt.date

misery.to_sql("county_weekly_misery", engine, if_exists="replace", index=False)
print("County weekly misery scores computed and saved.")
