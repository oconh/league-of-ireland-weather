import os
from datetime import date
import pandas as pd
from sqlalchemy import create_engine

week_start = date(2026, 1, 26)  # change as needed

engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('DB_USER', 'weather_user')}:"
    f"{os.getenv('DB_PASS', 'weather_pass')}@"
    f"{os.getenv('DB_HOST', 'localhost')}:"
    f"{os.getenv('DB_PORT', '5432')}/"
    f"{os.getenv('DB_NAME', 'weather')}"
)

fixtures = pd.read_sql_table("fixtures", engine)
misery = pd.read_sql_table("county_weekly_misery", engine)

week_fixtures = fixtures[fixtures["week_start"] == pd.Timestamp(week_start)]
week_misery = (
    misery[misery["week_start"] == pd.Timestamp(week_start)]
    .set_index("county")["misery_score"]
)

rows = []
for _, row in week_fixtures.iterrows():
    home_score = week_misery.get(row["home_county"])
    away_score = week_misery.get(row["away_county"])
    if home_score is None or away_score is None:
        continue
    if home_score > away_score:
        home_points, away_points = 3, 0
    elif home_score < away_score:
        home_points, away_points = 0, 3
    else:
        home_points = away_points = 1
    rows.append({"week_start": week_start, "county": row["home_county"], "points": home_points})
    rows.append({"week_start": week_start, "county": row["away_county"], "points": away_points})

existing = pd.read_sql_table("weekly_points", engine)
existing = existing[existing["week_start"] != pd.Timestamp(week_start)]
updated = pd.concat([existing, pd.DataFrame(rows)], ignore_index=True)
updated.to_sql("weekly_points", engine, if_exists="replace", index=False)

print(f"Weekly points for {week_start} calculated and updated!")
