# queries.py
# All SQL lives here

# --------------------------
# League table (overall)
# --------------------------
LEAGUE_TABLE_QUERY = """
SELECT
    county,
    SUM(points) AS total_points,
    COUNT(*) AS games_played
FROM weekly_points
GROUP BY county
ORDER BY total_points DESC;
"""

# --------------------------
# Available weeks
# --------------------------
WEEKS_QUERY = """
SELECT DISTINCT week_start
FROM fixtures
ORDER BY week_start DESC;
"""

# --------------------------
# Weekly results (W / D / L)
# --------------------------
WEEKLY_RESULTS_QUERY = """
SELECT 
    f.week_start,
    f.home_county,
    f.away_county,
    h.misery_score AS home_score,
    a.misery_score AS away_score,
    CASE
        WHEN h.misery_score > a.misery_score THEN 'W'
        WHEN h.misery_score < a.misery_score THEN 'L'
        ELSE 'D'
    END AS home_result,
    CASE
        WHEN h.misery_score > a.misery_score THEN 'L'
        WHEN h.misery_score < a.misery_score THEN 'W'
        ELSE 'D'
    END AS away_result
FROM fixtures f
JOIN county_weekly_misery h
    ON f.home_county = h.county
   AND f.week_start = h.week_start
JOIN county_weekly_misery a
    ON f.away_county = a.county
   AND f.week_start = a.week_start
WHERE f.week_start = %s
ORDER BY f.fixture_id;
"""
