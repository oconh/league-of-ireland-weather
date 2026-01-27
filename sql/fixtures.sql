-- ==================================================
-- 2️⃣ Create fixtures table
-- ==================================================
CREATE TABLE IF NOT EXISTS fixtures (
    fixture_id SERIAL PRIMARY KEY,
    week_start DATE NOT NULL,
    home_county TEXT NOT NULL,
    away_county TEXT NOT NULL
);