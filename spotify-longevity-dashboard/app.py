from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Catalog Revival Planner", page_icon="🎵", layout="wide")

DATA_DIR = Path(__file__).parent / "data"


@st.cache_data
def load_data() -> pd.DataFrame:
    metadata = pd.read_csv(DATA_DIR / "track_metadata.csv", parse_dates=["release_date"])
    audio = pd.read_csv(DATA_DIR / "audio_features.csv")
    longevity = pd.read_csv(DATA_DIR / "chart_longevity_panel.csv")
    tracks = metadata.merge(audio, on="track_id", validate="one_to_one").merge(
        longevity, on="track_id", validate="one_to_one"
    )
    tracks["release_year"] = tracks["release_date"].dt.year
    return tracks


tracks = load_data()

st.title("🎵 Catalog Revival Planner — Team Resonance")
st.caption(
    "For an editorial playlist lead deciding which genres and release cohorts "
    "to prioritize for the next catalog-revival playlist refresh."
)

with st.sidebar:
    st.header("Planning scope")
    years = sorted(tracks["release_year"].unique())
    selected_years = st.slider(
        "Release years",
        min_value=int(min(years)),
        max_value=int(max(years)),
        value=(int(min(years)), int(max(years))),
        help="Include tracks released within this inclusive year range.",
    )
    genres = sorted(tracks["genre"].unique())
    selected_genres = st.multiselect(
        "Genres",
        options=genres,
        default=genres,
        help="Compare only the genres relevant to the current playlist brief.",
    )
    st.markdown(
        "**Production action trigger**  \nAudit a genre's playlist allocation when its "
        "viral-hit share falls below 20% with at least 30 eligible tracks."
    )

filtered = tracks[
    tracks["release_year"].between(*selected_years)
    & tracks["genre"].isin(selected_genres)
].copy()

if filtered.empty:
    st.warning("No tracks match this scope. Select at least one genre and widen the year range.")
    st.stop()

start_date = tracks["release_date"].min().strftime("%b %Y")
end_date = tracks["release_date"].max().strftime("%b %Y")
st.caption(
    f"Data: {start_date} – {end_date}, Kaggle snapshot. "
    "In production: refresh source data nightly; review every Monday before the weekly playlist refresh."
)

st.subheader("Current selection")
metric_columns = st.columns(3)
median_weeks = filtered["weeks_on_top_100"].median()
viral_rate = filtered["is_viral_hit"].mean()
overall_median = tracks["weeks_on_top_100"].median()
overall_viral_rate = tracks["is_viral_hit"].mean()
metric_columns[0].metric(
    "Eligible tracks",
    f"{len(filtered):,}",
    help="Tracks matching the selected release years and genres.",
)
metric_columns[1].metric(
    "Median weeks in Top 100",
    f"{median_weeks:.0f}",
    delta=f"{median_weeks - overall_median:+.0f} vs full dataset",
    help="The middle track's chart longevity; less sensitive to outliers than an average.",
)
metric_columns[2].metric(
    "Viral-hit share",
    f"{viral_rate:.1%}",
    delta=f"{(viral_rate - overall_viral_rate) * 100:+.1f} pp vs full dataset",
    help="Percentage of selected tracks with is_viral_hit = 1.",
)

left, right = st.columns(2)
with left:
    st.subheader("Which genres sustain attention?")
    genre_summary = (
        filtered.groupby("genre", as_index=False)
        .agg(
            median_weeks=("weeks_on_top_100", "median"),
            tracks=("track_id", "size"),
        )
        .sort_values("median_weeks")
    )
    st.bar_chart(
        genre_summary,
        x="genre",
        y="median_weeks",
        x_label="Genre",
        y_label="Median weeks in Top 100",
        horizontal=True,
    )
    st.caption(
        "Use this to compare playlist candidates within the selected cohorts. "
        "Differences are descriptive, not proof that genre causes longevity."
    )

with right:
    st.subheader("Which release cohorts endured?")
    cohort_summary = (
        filtered.groupby("release_year", as_index=False)
        .agg(
            median_weeks=("weeks_on_top_100", "median"),
            tracks=("track_id", "size"),
        )
        .sort_values("release_year")
    )
    st.line_chart(
        cohort_summary,
        x="release_year",
        y="median_weeks",
        x_label="Release year",
        y_label="Median weeks in Top 100",
    )
    st.caption(
        "The 2026 cohort is a partial year. Newer tracks may have had less time "
        "to accumulate chart weeks, so do not read a decline as a creative trend."
    )

st.subheader("Track review queue")
st.caption(
    "Top 10 tracks by chart longevity in the current scope, with streams as a tie-breaker. "
    "Use this as a listening and rights-review queue, not an automatic booking list."
)
shortlist = filtered.sort_values(
    ["weeks_on_top_100", "total_streams_mil"], ascending=[False, False]
).head(10)
shortlist["is_viral_hit"] = shortlist["is_viral_hit"].map({1: "Yes", 0: "No"})
shortlist["release_date"] = shortlist["release_date"].dt.strftime("%Y-%m-%d")
st.dataframe(
    shortlist[
        [
            "track_title",
            "artist_name",
            "genre",
            "release_date",
            "weeks_on_top_100",
            "is_viral_hit",
            "total_streams_mil",
        ]
    ],
    column_config={
        "track_title": "Track",
        "artist_name": "Artist",
        "genre": "Genre",
        "release_date": "Release date",
        "weeks_on_top_100": st.column_config.NumberColumn("Weeks in Top 100"),
        "is_viral_hit": "Viral hit",
        "total_streams_mil": st.column_config.NumberColumn(
            "Total streams (millions)", format="%.1f"
        ),
    },
    hide_index=True,
    width="stretch",
)

with st.expander("Read before acting on these numbers"):
    st.markdown(
        "- The source documentation does not clearly establish whether these are actual "
        "Spotify exports or synthetic/anonymized records; generic track and artist names "
        "limit external verification. Use this app as a planning prototype.\n"
        "- `total_streams_mil` is cumulative, so older tracks have more exposure time. "
        "It is shown only as secondary track detail, not as a headline KPI.\n"
        "- Chart longevity and viral-hit status describe past outcomes. They do not measure "
        "listener fit, licensing availability, or the incremental effect of playlist placement."
    )
