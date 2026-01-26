# app.py
import streamlit as st
import pandas as pd
import psycopg2

# --------------------------
# 1. Connect to PostgreSQL
# --------------------------
def get_connection():
    conn = psycopg2.connect(
        host="localhost",       # or your Docker/container host
        port=5432,              # Docker port mapping
        database="weather",
        user="weather_user",
        password="weather_pass"  # match docker-compose.yml
    )
    return conn

# --------------------------
# 2. Fetch league table
# --------------------------
@st.cache_data
def fetch_league_table():
    query = """
        SELECT
            county,
            ROUND(AVG(rain_sum)::numeric, 2) AS avg_rain_mm,
            ROUND(AVG(wind_speed)::numeric, 2) AS avg_wind_kmh,
            ROUND(AVG(temp_min)::numeric, 2) AS avg_temp_min,
            ROUND(AVG(rain_sum + wind_speed - temp_min)::numeric, 2) AS avg_misery_score
        FROM weather_daily
        GROUP BY county
        ORDER BY avg_misery_score DESC;
    """
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# --------------------------
# 3. Streamlit layout
# --------------------------
st.set_page_config(page_title="Irish Weather League Table", layout="wide")
st.title("☔ League of Ireland: Worst Weather Counties")

st.markdown("""
This dashboard ranks Irish counties based on a **misery score**, calculated as:

**Misery Score = Average Rain + Average Wind - Average Minimum Temperature**
""")

# Fetch data
df = fetch_league_table()

# Rename columns to be cleaner for display
df_display = df[["county", "avg_misery_score"]].rename(columns={
    "county": "County",
    "avg_misery_score": "Avg Misery Score"
})

# Display table
st.subheader("League Table")
st.dataframe(df_display, use_container_width=True)