CREATE OR REPLACE VIEW league_table AS
SELECT
    county,
    SUM(points) AS total_points,
    COUNT(*) AS games_played
FROM weekly_points
GROUP BY county
ORDER BY total_points DESC;