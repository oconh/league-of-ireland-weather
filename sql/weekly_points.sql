-- ==================================================
-- 3️⃣ Create weekly points table
-- ==================================================
CREATE TABLE IF NOT EXISTS weekly_points (
    week_start DATE,
    county TEXT,
    points INT DEFAULT 0,
    PRIMARY KEY (week_start, county)
);