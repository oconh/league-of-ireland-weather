import streamlit as st
import pandas as pd

from db import read_table

st.set_page_config(page_title="League of Misery", layout="wide")
st.title("☔ League of Misery")
st.markdown(
    "Counties compete weekly based on **misery score** "
    "(rain + wind − temperature). Higher misery wins."
)

# --------------------------
# League Table
# --------------------------
wp = read_table("weekly_points")
league_df = (
    wp.groupby("county")
    .agg(total_points=("points", "sum"), games_played=("points", "count"))
    .reset_index()
    .sort_values("total_points", ascending=False)
    .rename(columns={"county": "County", "total_points": "Points", "games_played": "Played"})
)
league_df.insert(0, "Pos", range(1, len(league_df) + 1))

st.subheader("League Table")
st.dataframe(league_df, width='stretch')

# --------------------------
# Weekly Results
# --------------------------
fixtures = read_table("fixtures")
misery = read_table("county_weekly_misery")

weeks = sorted(fixtures["week_start"].unique(), reverse=True)
selected_week = st.selectbox("Select week", weeks)

week_fixtures = fixtures[fixtures["week_start"] == selected_week]

home_m = misery[["county", "week_start", "misery_score"]].rename(
    columns={"county": "home_county", "misery_score": "home_score"}
)
away_m = misery[["county", "week_start", "misery_score"]].rename(
    columns={"county": "away_county", "misery_score": "away_score"}
)

results_df = (
    week_fixtures
    .merge(home_m, on=["home_county", "week_start"])
    .merge(away_m, on=["away_county", "week_start"])
)


def get_result(h, a):
    if h > a:
        return "W", "L"
    if h < a:
        return "L", "W"
    return "D", "D"


results_df[["home_result", "away_result"]] = results_df.apply(
    lambda r: pd.Series(get_result(r["home_score"], r["away_score"])), axis=1
)


def colour_result(result, score):
    try:
        score = int(float(score))
    except (ValueError, TypeError):
        score = 0
    colour = {"W": "green", "L": "red", "D": "grey"}[result]
    return f"<span style='color:{colour}; font-weight:600'>{result} ({score})</span>"


results_df["Result"] = results_df.apply(
    lambda r: (
        f"{r['home_county']} "
        f"{colour_result(r['home_result'], r['home_score'])} "
        f"vs "
        f"{colour_result(r['away_result'], r['away_score'])} "
        f"{r['away_county']}"
    ),
    axis=1
)

st.subheader(f"Results – week starting {selected_week}")
for r in results_df["Result"]:
    st.markdown(r, unsafe_allow_html=True)
