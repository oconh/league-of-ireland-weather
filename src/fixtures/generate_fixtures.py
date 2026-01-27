import psycopg2
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

# If odd number of counties, add a dummy "BYE"
if len(counties) % 2:
    counties.append("BYE")

num_weeks = (len(counties) - 1) * 2  # double round-robin
half = len(counties) // 2

# ----------------------------
# 3️⃣ Round-robin scheduling
# ----------------------------
def round_robin_schedule(teams):
    schedule = []
    n = len(teams)
    teams_fixed = teams[0]
    rotating = teams[1:]
    for week in range(n - 1):
        pairs = []
        left = [teams_fixed] + rotating[:half-1]
        right = rotating[half-1:][::-1]
        for i in range(half):
            home = left[i]
            away = right[i]
            if home != "BYE" and away != "BYE":
                pairs.append((home, away))
        schedule.append(pairs)
        # Rotate teams
        rotating = rotating[1:] + rotating[:1]
    return schedule

# Generate first half of season
first_half = round_robin_schedule(counties)
# Generate second half (reverse home/away)
second_half = [[(away, home) for home, away in week] for week in first_half]

full_schedule = first_half + second_half

# ----------------------------
# 4️⃣ Clear existing fixtures (optional)
# ----------------------------
cur.execute("DELETE FROM fixtures;")

# ----------------------------
# 5️⃣ Insert into fixtures table
# ----------------------------
start_week = date(2026, 1, 26)
week_increment = timedelta(weeks=1)
current_week = start_week

for weekly_matches in full_schedule:
    for home, away in weekly_matches:
        cur.execute(
            "INSERT INTO fixtures (week_start, home_county, away_county) VALUES (%s, %s, %s)",
            (current_week, home, away)
        )
    current_week += week_increment

# ----------------------------
# 6️⃣ Commit and close
# ----------------------------

conn.commit()
cur.close()
conn.close()
print("Double round-robin fixtures created properly!")
