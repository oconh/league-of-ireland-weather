import psycopg2
from itertools import permutations
from datetime import date, timedelta

# ----------------------------
# 1️⃣ Connect to Postgres
# ----------------------------
conn = psycopg2.connect(
    host="localhost",
    dbname="weather",
    user="weather_user",
    password="weather_pass",
    port=5432
)
cur = conn.cursor()

# ----------------------------
# 2️⃣ Get all counties
# ----------------------------
cur.execute("SELECT DISTINCT county FROM county_weekly_misery ORDER BY county;")
counties = [row[0] for row in cur.fetchall()]

# ----------------------------
# 3️⃣ Generate all home-away pairs (double round-robin)
# ----------------------------
matches = []

# Each county plays every other county twice: home and away
for home, away in permutations(counties, 2):
    matches.append((home, away))

# ----------------------------
# 4️⃣ Assign matches to weeks
# ----------------------------
start_week = date(2026, 1, 26)  # first week
week_increment = timedelta(weeks=1)
current_week = start_week

# number of matches per week (half of counties, each match has 2 counties)
matches_per_week = len(counties) // 2

for i in range(0, len(matches), matches_per_week):
    weekly_matches = matches[i:i+matches_per_week]
    for home, away in weekly_matches:
        cur.execute(
            "INSERT INTO fixtures (week_start, home_county, away_county) VALUES (%s, %s, %s)",
            (current_week, home, away)
        )
    current_week += week_increment

# ----------------------------
# 5️⃣ Commit and close
# ----------------------------
conn.commit()
cur.close()
conn.close()
print(f"Double round-robin fixtures created starting from {start_week}!")
