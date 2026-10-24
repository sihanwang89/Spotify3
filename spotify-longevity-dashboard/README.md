# Catalog Revival Planner — Team Resonance

A small Streamlit dashboard for an editorial playlist lead planning a weekly catalog-revival playlist refresh.

## Dataset

**Source:** [Global Spotify Hits & Audio Dynamics (2018–2026)](https://www.kaggle.com/datasets/vedauv/global-spotify-hits-and-audio-dynamics-20182026), Ved, CC0 Public Domain.

The three CSV files are joined one-to-one on `track_id`, producing 1,200 tracks and 21 columns. Each row represents one track. The release dates run from January 2018 through June 2026. The files combine track metadata, audio characteristics, and chart outcomes such as weeks in the Top 100, cumulative streams, and viral-hit status. No sampling or aggregation was needed because every file is well below 25 MB.

The supplied documentation says the data was derived from aggregated streaming analytics and audio analysis, but it does not clearly establish whether the records are actual Spotify exports or synthetic/anonymized data. Generic names such as “Hit Song 1” and “Artist 164” also limit verification. The dashboard therefore presents itself as a planning prototype, not evidence about the current real-world music market.

## Step 1 — Decision-maker and decision

The dashboard is for **one editorial playlist lead at a music streaming service**. They review it every Monday before refreshing a catalog-revival playlist.

The decision sentence is: **“If the editorial playlist lead sees a genre or release cohort with sustained chart longevity and a strong viral-hit share, they will prioritize its tracks for listening and rights review before the next playlist refresh.”**

The app does not automatically place songs. A human still needs to judge musical fit, audience, licensing, and current cultural context.

## Step 2 — Why this dashboard earns its place

1. **Who and how often:** The editorial playlist lead reviews it weekly during playlist planning. In production, the underlying chart and stream data would refresh nightly.
2. **Supported decision:** It focuses a weekly review queue on genres, release cohorts, and individual tracks with evidence of sustained listener attention.
3. **What happens without it:** The lead would manually merge track exports, calculate group summaries, and sort spreadsheets each week. That is repetitive and makes it easier for teams to use inconsistent filters or choose tracks from memory rather than a shared view of past performance.
4. **Why not only an email or report:** A static weekly email could announce a KPI, but it would not let the lead narrow the same view to the genres and release years in a particular playlist brief. The dashboard preserves that interactive comparison and ends in an actionable track queue. It complements, rather than replaces, editorial judgment.

## Step 3 — What matters, what was cut, and page order

### Exploratory checks

The merged data has 1,200 rows, 1,200 unique track IDs, no duplicate rows, and no missing values. Release dates span January 7, 2018 to June 27, 2026. Median chart longevity is 18 weeks, and 28.7% of tracks are labeled viral hits.

Genre medians are fairly close, from 17 to 19 weeks, but viral-hit shares differ more: Rock is 20.2%, while R&B is 33.6%. Release-cohort medians range from 17 weeks in 2025 to 21 weeks in 2021. These findings support showing both genre and cohort views while avoiding a claim that small median differences prove a genre effect.

### Headline metrics — at most three

- **Eligible tracks:** establishes the size of the selected planning pool.
- **Median weeks in Top 100:** summarizes sustained attention while limiting the influence of extreme outliers.
- **Viral-hit share:** shows the proportion with the dataset's viral-hit label.

The latter two include deltas against the full dataset so the lead can interpret the filtered values in context.

### Supporting charts

- **Median weeks by genre:** supports the decision about which genres deserve review capacity.
- **Median weeks by release cohort:** identifies cohorts that sustained attention and supplies context for the filtered KPIs.

### Filters

Only two filters are included:

- **Release-year range:** playlist briefs often distinguish recent catalog from older catalog.
- **Genres:** the lead can match the view to the playlist's musical scope.

Audio-feature sliders were excluded because they would add complexity without helping the weekly placement decision.

### Two things deliberately not shown

1. **Audio-feature scatter plots:** Danceability, energy, and valence are interesting for exploratory modeling, but the lead cannot change an existing catalog track's sound. Showing them would encourage a production discussion rather than a placement decision.
2. **An artist leaderboard:** Artist names are generic and repeated across unequal numbers of tracks, so ranking artists could reward sample size or invent false precision. The useful unit of action is the individual track, which remains in the review queue.

Cumulative streams are not a headline KPI because older tracks have more time to accumulate them. Streams appear only as secondary detail and a tie-breaker in the track table.

### What could mislead the viewer

- **Partial 2026 cohort and unequal exposure time:** The data ends in June 2026, and recent tracks may have had less time to accumulate chart weeks. A caption beside the cohort chart warns against treating this as a creative decline.
- **Unclear provenance:** The documentation does not establish whether observations are actual Spotify exports or synthetic/anonymized. An expandable warning states this limitation and prohibits broad real-world conclusions.
- **Historical outcomes are not placement effects:** Longevity and viral-hit status do not show that a playlist placement will cause future streams. The app calls its table a review queue, not an automatic booking list.

### Page order

1. **Top:** title, decision caption, planning filters, and three metrics answer “what does the current pool look like?”
2. **Middle:** genre and cohort charts explain where the stronger historical outcomes sit.
3. **Bottom:** the top-10 track queue supplies specific records for listening and rights review. The data warning sits last so it is available without crowding the decision path.

## Step 4 — Refresh and review decisions

- **Refresh:** Chart outcomes and stream totals would refresh nightly from the production streaming datastore. Real-time refreshes would add cost without changing a decision made weekly.
- **Review:** The editorial playlist lead reviews the dashboard every Monday before the weekly catalog-playlist update. Review and refresh frequencies intentionally differ.
- **Track over time:** Monitor eligible-track count, median Top 100 longevity, and viral-hit share by genre and release cohort. In production, a genre's viral-hit share falling below **20% with at least 30 eligible tracks** triggers an allocation audit. The minimum sample prevents a tiny genre cohort from causing unnecessary action.
- **Cost of stale data:** Data one day old is unlikely to change a weekly plan. Data a week old can send review time toward a cooling genre or omit a newly sustained hit, making the next playlist refresh less relevant.

## Run locally

This project uses Python 3.14 and `uv`.

```bash
uv sync
uv run streamlit run app.py
```

## Deploy

Push this project to a public GitHub repository. In Streamlit Community Cloud, select `app.py` as the entry point and set Python to **3.14** under Advanced settings.

## Project structure

```text
app.py                         Streamlit application
data/track_metadata.csv        Track and release metadata
data/audio_features.csv        Audio characteristics
data/chart_longevity_panel.csv Chart and streaming outcomes
data/datasheet.md              Supplied source documentation
pyproject.toml                 Python version and dependencies
uv.lock                        Reproducible dependency lockfile
```
