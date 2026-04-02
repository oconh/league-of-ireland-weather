import os
import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path

CSV_FILE = Path("data/processed/weather_clean.csv")

engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('DB_USER', 'weather_user')}:"
    f"{os.getenv('DB_PASS', 'weather_pass')}@"
    f"{os.getenv('DB_HOST', 'localhost')}:"
    f"{os.getenv('DB_PORT', '5432')}/"
    f"{os.getenv('DB_NAME', 'weather')}"
)

df = pd.read_csv(CSV_FILE)
df.to_sql("weather_daily", engine, if_exists="replace", index=False)
print("CSV loaded into Postgres table 'weather_daily'")
