import psycopg2
from datetime import date

# ----------------------------
# 1️⃣ Connect to Postgres
# ----------------------------
conn = psycopg2.connect(
    host="localhost",
    dbname="weather",
    user="weather_user",
    password="weather_pass",  # replace with your password
    port=5432
)
cur = conn.cursor()

# ----------------------------
# 2️⃣ Define week to calculate
# ----------------------------
week_start = date(2026, 1, 26)  # change as needed

# ----------------------------
# 3️⃣ Fetch fixtures for the week
# ----------------------------
cur.execute("""
    SELECT fixture_id, home_county, away_county
    FROM fixtures
    WHERE week_start = %s
""", (week_start,))
fixtures = cur.fetchall()

# ----------------------------
# 4️⃣ Calculate points
# ----------------------------
for fixture_id, home, away in fixtures:
    # Get misery scores
    cur.execute("""
        SELECT misery_score FROM county_weekly_misery
        WHERE county = %s AND week_start = %s
    """, (home, week_start))
    home_score = cur.fetchone()[0]

    cur.execute("""
        SELECT misery_score FROM county_weekly_misery
        WHERE county = %s AND week_start = %s
    """, (away, week_start))
    away_score = cur.fetchone()[0]

    # Determine points
    if home_score > away_score:
        home_points, away_points = 3, 0
    elif home_score < away_score:
        home_points, away_points = 0, 3
    else:
        home_points = away_points = 1

    # Insert/update points for home county
    cur.execute("""
        INSERT INTO weekly_points (week_start, county, points)
        VALUES (%s, %s, %s)
        ON CONFLICT (week_start, county)
        DO UPDATE SET points = EXCLUDED.points
    """, (week_start, home, home_points))

    # Insert/update points for away county
    cur.execute("""
        INSERT INTO weekly_points (week_start, county, points)
        VALUES (%s, %s, %s)
        ON CONFLICT (week_start, county)
        DO UPDATE SET points = EXCLUDED.points
    """, (week_start, away, away_points))

# ----------------------------
# 5️⃣ Commit and close
# ----------------------------
conn.commit()
cur.close()
conn.close()

print(f"Weekly points for {week_start} calculated and updated!")
