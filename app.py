import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.title("Wildfire Evacuation Lead Time Dashboard")

# LOAD DATA
events = pd.read_csv("geo_events_geoevent.csv")
changes = pd.read_csv("geo_events_geoeventchangelog.csv")

# -----------------------------
# BASIC CLEANING
# -----------------------------

events["date_created"] = pd.to_datetime(events["date_created"])
changes["date_created"] = pd.to_datetime(changes["date_created"])

# FILTER WILDFIRES
wildfires = events[
    events["geo_event_type"].astype(str).str.contains(
        "wildfire",
        case=False,
        na=False
    )
].copy()

# EVACUATION UPDATES
evac_changes = changes[
    changes["changes"].astype(str).str.contains(
        "evac",
        case=False,
        na=False
    )
].copy()

# FIRST EVAC UPDATE
first_evac = (
    evac_changes
    .sort_values("date_created")
    .groupby("geo_event_id")
    .first()
    .reset_index()
)

# MERGE
lead_time_with_evac = wildfires.merge(
    first_evac[["geo_event_id", "date_created"]],
    on="geo_event_id",
    suffixes=("_wildfire", "_evac")
)

# LEAD TIME
lead_time_with_evac["lead_time_minutes"] = (
    lead_time_with_evac["date_created_evac"]
    - lead_time_with_evac["date_created_wildfire"]
).dt.total_seconds() / 60

# REMOVE NEGATIVES
lead_time_with_evac = lead_time_with_evac[
    lead_time_with_evac["lead_time_minutes"] >= 0
]

# -----------------------------
# TEMPORARY STATE PLACEHOLDER
# -----------------------------
# REPLACE WITH REAL STATE COLUMN IF YOU HAVE ONE

if "state" not in lead_time_with_evac.columns:
    lead_time_with_evac["state"] = "Unknown"

# -----------------------------
# STATE SUMMARY
# -----------------------------

state_summary = (
    lead_time_with_evac
    .groupby("state")["lead_time_minutes"]
    .agg(["count", "median"])
    .sort_values("median")
)

filtered_states = state_summary[
    state_summary["count"] >= 1
]

# -----------------------------
# GRAPH 1
# -----------------------------

st.header("Median Evacuation Lead Time by State")

fig1, ax1 = plt.subplots(figsize=(14,6))

bars = ax1.bar(
    filtered_states.index,
    filtered_states["median"]
)

ax1.set_xlabel("State")
ax1.set_ylabel("Median Lead Time (minutes)")
ax1.set_title("Median Evacuation Lead Time by State")

plt.xticks(rotation=45)

for bar, value in zip(bars, filtered_states["median"]):
    ax1.text(
        bar.get_x() + bar.get_width()/2,
        bar.get_height(),
        f"{value:.1f}",
        ha='center',
        va='bottom'
    )

st.pyplot(fig1)

# -----------------------------
# MONTH COLUMN
# -----------------------------

lead_time_with_evac["month"] = (
    lead_time_with_evac["date_created_wildfire"]
    .dt.month_name()
)

month_order = [
    "January","February","March","April","May","June",
    "July","August","September","October","November","December"
]

# -----------------------------
# GRAPH 2
# -----------------------------

st.header("Wildfire Frequency by Month")

monthly_counts = (
    lead_time_with_evac["month"]
    .value_counts()
    .reindex(month_order)
)

fig2, ax2 = plt.subplots(figsize=(12,5))

ax2.bar(monthly_counts.index, monthly_counts.values)

ax2.set_ylabel("Wildfire Count")
ax2.set_title("Wildfire Frequency by Month")

plt.xticks(rotation=45)

st.pyplot(fig2)

# -----------------------------
# GRAPH 3
# -----------------------------

st.header("Median Evacuation Lead Time by Month")

monthly_median = (
    lead_time_with_evac
    .groupby("month")["lead_time_minutes"]
    .median()
    .reindex(month_order)
)

fig3, ax3 = plt.subplots(figsize=(12,5))

ax3.bar(monthly_median.index, monthly_median.values)

ax3.set_ylabel("Median Lead Time")
ax3.set_title("Median Evacuation Lead Time by Month")

plt.xticks(rotation=45)

st.pyplot(fig3)

# -----------------------------
# GRAPH 4
# -----------------------------

st.header("Median Lead Time vs Rural Population %")

# EXAMPLE PLACEHOLDER VALUES
# REPLACE WITH REAL NOTEBOOK DATA

rural_data = pd.DataFrame({
    "state": filtered_states.index,
    "rural_pct": range(len(filtered_states)),
    "median_lead_time": filtered_states["median"].values
})

fig4, ax4 = plt.subplots(figsize=(8,6))

ax4.scatter(
    rural_data["rural_pct"],
    rural_data["median_lead_time"]
)

ax4.set_xlabel("Rural Population %")
ax4.set_ylabel("Median Lead Time")

ax4.set_title(
    "Median Evacuation Lead Time by State with Rural Population %"
)

st.pyplot(fig4)
