import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path

CSV_FILE = Path("data/processed/weather_clean.csv")

# DB connection string
DB_URL = "postgresql+psycopg2://weather_user:weather_pass@localhost:5432/weather"

# Read cleaned CSV
df = pd.read_csv(CSV_FILE)

# Connect to Postgres
engine = create_engine(DB_URL)

# Load into Postgres
df.to_sql("weather_daily", engine, if_exists="replace", index=False)
print("CSV loaded into Postgres table 'weather_daily'")
