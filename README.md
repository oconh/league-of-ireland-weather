# league-of-ireland-weather

League table of Irish counties with the worst weather.

# League of Ireland Weather ETL Pipeline

This project demonstrates a complete **ETL pipeline** for Irish county weather data using **Python**, **PostgreSQL**, and **Docker**.

## Project Overview

1. **Extract**: Fetches daily weather data for all counties in Ireland from the [Open-Meteo API](https://open-meteo.com/).
2. **Transform**: Cleans raw JSON, converts units, and standardizes county names.
3. **Load**: Loads the cleaned data into a PostgreSQL database running in Docker.
4. **Analysis**: Computes a **Worst Weather Counties** league table based on rain, wind, and temperature.

---

## Project Structure

league-of-ireland-weather/
│
├─ data/
│ ├─ raw/ # Raw API data (ignored by Git)
│ └─ processed/ # Cleaned CSV (ignored by Git)
│
├─ src/
│ ├─ extract/ # Python scripts to fetch data
│ ├─ transform/ # Python scripts to clean data
│ └─ load/ # Python scripts to load data to Postgres
│
├─ sql/
│ └─ league_table.sql
│
├─ docker/
│ └─ docker-compose.yml
│
├─ notebooks/ # Optional analysis notebooks
├─ .gitignore
└─ requirements.txt

---

## Setup Instructions

### 1. Clone repo & activate virtual environment

```bash
git clone <repo-url>
cd league-of-ireland-weather
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt
```

### 2. Start PostgreSQL via Docker

docker-compose -f docker\docker-compose.yml up -d
Runs PostgreSQL 15 in a Docker container

Database credentials are set in docker-compose.yml

### 3. Extract & Transform Data

python src\extract\fetch_weather.py
python src\transform\clean_weather.py
fetch_weather.py collects raw JSON data from Open-Meteo

clean_weather.py transforms the data into a clean CSV ready for Postgres

### 4. Load Data into PostgreSQL

python src\load\load_to_postgres.py
Loads the cleaned CSV into the weather_daily table in Postgres

### 5. Run League Table Query

-- Preview table
SELECT \* FROM weather_daily LIMIT 5;

-- Or run the league table SQL
\i sql/league_table.sql
Computes Worst Weather Counties by combining:

misery_score = rain_sum + wind_speed - temp_min
Orders counties from worst → best weather

### Notes

data/raw and data/processed are ignored in Git to avoid committing large or dynamic files

The “Worst Weather Counties” ranking uses a misery score to combine rain, wind, and temperature

All stages are modular: Extract → Transform → Load → Analysis
