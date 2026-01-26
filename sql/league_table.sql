-- Ranking counties by worst weather

SELECT
    county,
    COUNT(*) AS days_recorded,
    ROUND(AVG(rain_sum), 2) AS avg_rain_mm,
    ROUND(AVG(wind_speed), 2) AS avg_wind_kmh,
    ROUND(AVG(temp_min), 2) AS avg_temp_min,
    ROUND(AVG(rain_sum + wind_speed - temp_min), 2) AS avg_misery_score
FROM
    weather_daily
GROUP BY
    county
ORDER BY
    avg_misery_score DESC;
