import os
from datetime import date, timedelta
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('DB_USER', 'weather_user')}:"
    f"{os.getenv('DB_PASS', 'weather_pass')}@"
    f"{os.getenv('DB_HOST', 'localhost')}:"
    f"{os.getenv('DB_PORT', '5432')}/"
    f"{os.getenv('DB_NAME', 'weather')}"
)

counties = sorted(
    pd.read_sql_table("county_weekly_misery", engine)["county"].unique().tolist()
)

if len(counties) % 2:
    counties.append("BYE")

half = len(counties) // 2


def round_robin_schedule(teams):
    schedule = []
    rotating = teams[1:]
    for _ in range(len(teams) - 1):
        left = [teams[0]] + rotating[:half - 1]
        right = rotating[half - 1:][::-1]
        pairs = [(h, a) for h, a in zip(left, right) if h != "BYE" and a != "BYE"]
        schedule.append(pairs)
        rotating = rotating[1:] + rotating[:1]
    return schedule


first_half = round_robin_schedule(counties)
second_half = [[(a, h) for h, a in week] for week in first_half]
full_schedule = first_half + second_half

start_week = date(2026, 1, 26)
rows = []
for i, weekly_matches in enumerate(full_schedule):
    week_start = start_week + timedelta(weeks=i)
    for home, away in weekly_matches:
        rows.append({"week_start": week_start, "home_county": home, "away_county": away})

pd.DataFrame(rows).to_sql("fixtures", engine, if_exists="replace", index=False)
print("Double round-robin fixtures created properly!")
