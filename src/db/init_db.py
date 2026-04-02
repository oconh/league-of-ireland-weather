"""
Replaces sql/create_tables.sql, sql/fixtures.sql,
sql/weekly_points.sql, sql/weekly_table.sql (DDL part).
Run once to initialise the database schema.
"""
import os
from sqlalchemy import (
    create_engine, MetaData, Table, Column,
    Integer, Float, Text, Date, Numeric, UniqueConstraint,
)

engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('DB_USER', 'weather_user')}:"
    f"{os.getenv('DB_PASS', 'weather_pass')}@"
    f"{os.getenv('DB_HOST', 'localhost')}:"
    f"{os.getenv('DB_PORT', '5432')}/"
    f"{os.getenv('DB_NAME', 'weather')}"
)

metadata = MetaData()

Table("weather_daily", metadata,
    Column("date", Date),
    Column("county", Text),
    Column("rain_sum", Float),
    Column("wind_speed", Float),
    Column("temp_min", Float),
)

Table("fixtures", metadata,
    Column("fixture_id", Integer, primary_key=True, autoincrement=True),
    Column("week_start", Date, nullable=False),
    Column("home_county", Text, nullable=False),
    Column("away_county", Text, nullable=False),
)

Table("weekly_points", metadata,
    Column("week_start", Date),
    Column("county", Text),
    Column("points", Integer, default=0),
    UniqueConstraint("week_start", "county", name="uq_weekly_points"),
)

Table("county_weekly_misery", metadata,
    Column("county", Text, nullable=False),
    Column("week_start", Date, nullable=False),
    Column("avg_rain_mm", Numeric(6, 2)),
    Column("avg_wind_kmh", Numeric(6, 2)),
    Column("avg_min_temp", Numeric(5, 2)),
    Column("misery_score", Numeric(6, 2)),
    UniqueConstraint("county", "week_start", name="uq_county_misery"),
)

metadata.create_all(engine)
print("All tables created.")
