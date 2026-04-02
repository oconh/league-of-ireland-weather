# League of Misery

Which Irish county has the worst weather? This project finds out.

Pulls daily weather from [Open-Meteo](https://open-meteo.com/), scores each county by misery (`rain + wind − temp`), and runs a league table.

## Setup

```bash
python -m venv venv && source venv/Scripts/activate
pip install -r requirements.txt
docker-compose -f docker/docker-compose.yml up -d
```

## Run

```bash
python src/extract/fetch_weather.py       # fetch raw data
python src/transform/clean_weather.py     # clean to CSV
python src/load/load_to_postgres.py       # load into postgres
python src/transform/compute_misery.py    # compute weekly scores
python src/fixtures/generate_fixtures.py  # generate fixtures
python src/fixtures/compute_points.py     # compute league points
streamlit run src/app/app.py              # view the dashboard
```

First time only — create the database tables:

```bash
python src/db/init_db.py
```
