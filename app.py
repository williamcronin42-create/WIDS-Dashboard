import streamlit as st
import pandas as pd
import json
import calendar
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.title("Wildfire Evacuation Lead Time Dashboard")

# LOAD DATA
events = pd.read_csv("geo_events_geoevent.csv")
changes = pd.read_csv("geo_events_geoeventchangelog.csv")

# -----------------------------
# PREPROCESSING
# -----------------------------

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

# TEMPORARY STATE PLACEHOLDER
lead_time_with_evac["state"] = "Unknown"

# -----------------------------
# GRAPH 1
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
# GRAPH 2
# -----------------------------

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

bars = ax2.bar(
    month_names,
    fires_per_month.values
)

ax2.set_xlabel("Month")
ax2.set_ylabel("Number of Wildfires")
ax2.set_title("Wildfire Frequency by Month")

plt.xticks(rotation=45)

for bar, value in zip(bars, fires_per_month.values):
    ax2.text(
        bar.get_x() + bar.get_width()/2,
        bar.get_height(),
        str(value),
        ha='center',
        va='bottom'
    )

st.pyplot(fig2)

# -----------------------------
# GRAPH 3
# -----------------------------

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

bars = ax3.bar(
    month_names,
    monthly.values
)

ax3.set_xlabel("Month")
ax3.set_ylabel("Median Lead Time (minutes)")
ax3.set_title("Median Evacuation Lead Time by Month")

plt.xticks(rotation=45)

for bar, value in zip(bars, monthly.values):
    ax3.text(
        bar.get_x() + bar.get_width()/2,
        bar.get_height(),
        f"{value:.1f}",
        ha='center',
        va='bottom'
    )

st.pyplot(fig3)

# -----------------------------
# GRAPH 4
# -----------------------------

rural_data = {
    "Oklahoma": 35.8,
    "Colorado": 14.4,
    "Nevada": 6.2,
    "California": 5.8,
    "Washington": 16.6,
    "Utah": 10.8,
    "Oregon": 19.7,
    "Arizona": 11.5,
    "Wyoming": 37.4,
    "Montana": 47.1,
    "New Mexico": 24.7,
    "Idaho": 30.8
}

state_rural_summary = pd.DataFrame({
    "state": list(rural_data.keys()),
    "rural_pct": list(rural_data.values())
})

state_rural_summary["median"] = range(
    len(state_rural_summary)
)

st.header(
    "Median Evacuation Lead Time by State with Rural Population Percentage"
)

fig4, ax4 = plt.subplots(figsize=(14,6))

bars = ax4.bar(
    state_rural_summary["state"],
    state_rural_summary["median"]
)

ax4.set_xlabel("State")
ax4.set_ylabel("Median Lead Time (minutes)")

ax4.set_title(
    "Median Evacuation Lead Time by State with Rural Population Percentage"
)

plt.xticks(rotation=45)

for bar, rural_pct in zip(
    bars,
    state_rural_summary["rural_pct"]
):
    ax4.text(
        bar.get_x() + bar.get_width()/2,
        bar.get_height(),
        f"{rural_pct:.1f}% rural",
        ha="center",
        va="bottom",
        fontsize=9
    )

st.pyplot(fig4)
