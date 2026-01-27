CREATE TABLE IF NOT EXISTS county_weekly_misery (
    county TEXT NOT NULL,
    week_start DATE NOT NULL,
    avg_rain_mm NUMERIC(6,2),
    avg_wind_kmh NUMERIC(6,2),
    avg_min_temp NUMERIC(5,2),
    misery_score NUMERIC(6,2),
    PRIMARY KEY (county, week_start)
);

INSERT INTO county_weekly_misery (
    county,
    week_start,
    avg_rain_mm,
    avg_wind_kmh,
    avg_min_temp,
    misery_score
)
SELECT
    county,
    DATE_TRUNC('week', date::date) AS week_start,
    ROUND(AVG(rain_sum)::numeric, 2) AS avg_rain_mm,
    ROUND(AVG(wind_speed)::numeric, 2) AS avg_wind_kmh,
    ROUND(AVG(temp_min)::numeric, 2) AS avg_min_temp,
    ROUND(AVG(rain_sum + wind_speed - temp_min)::numeric, 2) AS misery_score
FROM weather_daily
GROUP BY county, week_start
ON CONFLICT (county, week_start)
DO UPDATE SET
    avg_rain_mm   = EXCLUDED.avg_rain_mm,
    avg_wind_kmh  = EXCLUDED.avg_wind_kmh,
    avg_min_temp  = EXCLUDED.avg_min_temp,
    misery_score  = EXCLUDED.misery_score;