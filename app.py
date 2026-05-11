import streamlit as st
import pandas as pd
import json
import calendar
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim

st.set_page_config(layout="wide")

st.title("Wildfire Evacuation Lead Time Dashboard")

events = pd.read_csv("geo_events_geoevent.csv")
changes = pd.read_csv("geo_events_geoeventchangelog.csv")

def has_evac_change(change_text):
    try:
        change_dict = json.loads(change_text)
        return any(
            "evacuation" in key.lower()
            for key in change_dict.keys()
        )
    except:
        return False

evac_changes = changes[
    changes["changes"].apply(has_evac_change)
].copy()

first_evac = (
    evac_changes
    .groupby("geo_event_id")["date_created"]
    .min()
    .reset_index()
    .rename(columns={"date_created": "first_evac_time"})
)

lead_time_df = events[
    [
        "id",
        "name",
        "date_created",
        "lat",
        "lng",
        "notification_type"
    ]
].copy()

lead_time_df = lead_time_df.merge(
    first_evac,
    left_on="id",
    right_on="geo_event_id",
    how="left"
)

lead_time_df["date_created"] = pd.to_datetime(
    lead_time_df["date_created"],
    errors="coerce",
    utc=True
)

lead_time_df["first_evac_time"] = pd.to_datetime(
    lead_time_df["first_evac_time"],
    errors="coerce",
    utc=True
)

lead_time_df["lead_time_minutes"] = (
    lead_time_df["first_evac_time"]
    - lead_time_df["date_created"]
).dt.total_seconds() / 60

lead_time_with_evac = lead_time_df.dropna(
    subset=["first_evac_time"]
).copy()

lead_time_with_evac["month"] = (
    lead_time_with_evac["date_created"].dt.month
)

# REAL STATE LOOKUP
geolocator = Nominatim(user_agent="wildfire_dashboard")

def get_state(lat, lng):
    try:
        location = geolocator.reverse(
            f"{lat}, {lng}",
            language="en"
        )
        if location and "state" in location.raw["address"]:
            return location.raw["address"]["state"]
    except:
        return None

lead_time_with_evac["state"] = lead_time_with_evac.apply(
    lambda row: get_state(row["lat"], row["lng"]),
    axis=1
)

lead_time_with_evac = lead_time_with_evac.dropna(
    subset=["state"]
)

# GRAPH 1
state_summary = (
    lead_time_with_evac
    .groupby("state")["lead_time_minutes"]
    .agg(["count", "median"])
    .sort_values("median")
)

state_summary = state_summary[
    state_summary["count"] >= 15
]

filtered_states = state_summary.sort_values("median")

st.header("Median Evacuation Lead Time by State")

fig1, ax1 = plt.subplots(figsize=(14,6))

bars = ax1.bar(
    filtered_states.index,
    filtered_states["median"]
)

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

# GRAPH 2
fires_per_month = (
    lead_time_with_evac["month"]
    .value_counts()
    .sort_index()
)

month_names = [
    calendar.month_name[m]
    for m in fires_per_month.index
]

st.header("Wildfire Frequency by Month")

fig2, ax2 = plt.subplots(figsize=(12,6))

ax2.bar(month_names, fires_per_month.values)

plt.xticks(rotation=45)

st.pyplot(fig2)

# GRAPH 3
monthly = (
    lead_time_with_evac
    .groupby("month")["lead_time_minutes"]
    .median()
)

month_names = [
    calendar.month_name[m]
    for m in monthly.index
]

st.header("Median Evacuation Lead Time by Month")

fig3, ax3 = plt.subplots(figsize=(12,6))

ax3.bar(month_names, monthly.values)

plt.xticks(rotation=45)

st.pyplot(fig3)
