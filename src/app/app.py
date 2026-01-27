import streamlit as st
import pandas as pd

from db import fetch_df
from queries import (
    LEAGUE_TABLE_QUERY,
    WEEKLY_RESULTS_QUERY,
    WEEKS_QUERY
)

# --------------------------
# Page setup
# --------------------------
st.set_page_config(
    page_title="League of Misery",
    layout="wide"
)

st.title("☔ League of Misery")
st.markdown(
    "Counties compete weekly based on **misery score** "
    "(rain + wind − temperature). Higher misery wins."
)

# --------------------------
# League Table
# --------------------------
league_df = fetch_df(LEAGUE_TABLE_QUERY)

league_df = league_df.rename(columns={
    "county": "County",
    "total_points": "Points",
    "games_played": "Played"
})

league_df.insert(0, "Pos", range(1, len(league_df) + 1))

st.subheader("League Table")
st.dataframe(league_df, use_container_width=True)

# --------------------------
# Weekly Results
# --------------------------
weeks_df = fetch_df(WEEKS_QUERY)
selected_week = st.selectbox("Select week", weeks_df["week_start"])

results_df = fetch_df(WEEKLY_RESULTS_QUERY, (selected_week,))

results_df["Result"] = results_df.apply(
    lambda r: f"{r['home_county']} {r['home_result']} vs {r['away_result']} {r['away_county']}",
    axis=1
)

st.subheader(f"Results – week starting {selected_week}")
for r in results_df["Result"]:
    st.write(r)
