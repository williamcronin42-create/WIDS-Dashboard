import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import calendar

st.set_page_config(layout="wide")

st.title("Wildfire Evacuation Lead Time Dashboard")

# LOAD DATA
df = pd.read_csv("processed_wildfire_data.csv")

# -----------------------------
# DROPDOWN
# -----------------------------

view_option = st.selectbox(
    "Median Evacuation Lead Time By:",
    (
        "State",
        "Month",
        "State with Rural Population Percentage"
    )
)

# -----------------------------
# STATE SUMMARY
# -----------------------------

state_summary = (
    df.groupby("state")["lead_time_minutes"]
    .agg(["count", "median"])
    .sort_values("median")
)

state_summary = state_summary[
    state_summary["count"] >= 15
]

filtered_states = state_summary.sort_values("median")

# -----------------------------
# GRAPH OPTION 1
# -----------------------------

if view_option == "State":

    st.header("Median Evacuation Lead Time by State")

    fig1, ax1 = plt.subplots(figsize=(14,6))

    bars = ax1.bar(
        filtered_states.index,
        filtered_states["median"]
    )

    ax1.set_xlabel("State")
    ax1.set_ylabel("Median Lead Time (minutes)")

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
# GRAPH OPTION 2
# -----------------------------

elif view_option == "Month":

    monthly = (
        df.groupby("month")["lead_time_minutes"]
        .median()
    )

    month_names = [
        calendar.month_name[m]
        for m in monthly.index
    ]

    st.header("Median Evacuation Lead Time by Month")

    fig2, ax2 = plt.subplots(figsize=(12,6))

    bars = ax2.bar(
        month_names,
        monthly.values
    )

    ax2.set_xlabel("Month")
    ax2.set_ylabel("Median Lead Time (minutes)")

    plt.xticks(rotation=45)

    for bar, value in zip(bars, monthly.values):
        ax2.text(
            bar.get_x() + bar.get_width()/2,
            bar.get_height(),
            f"{value:.1f}",
            ha='center',
            va='bottom'
        )

    st.pyplot(fig2)

# -----------------------------
# GRAPH OPTION 3
# -----------------------------

elif view_option == "State with Rural Population Percentage":

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

    state_rural_summary = state_summary.copy()

    state_rural_summary["rural_pct"] = (
        state_rural_summary.index.map(rural_data)
    )

    state_rural_summary = state_rural_summary.dropna()

    st.header(
        "Median Evacuation Lead Time by State with Rural Population Percentage"
    )

    fig3, ax3 = plt.subplots(figsize=(14,6))

    bars = ax3.bar(
        state_rural_summary.index,
        state_rural_summary["median"]
    )

    ax3.set_xlabel("State")
    ax3.set_ylabel("Median Lead Time (minutes)")

    plt.xticks(rotation=45)

    for bar, rural_pct in zip(
        bars,
        state_rural_summary["rural_pct"]
    ):
        ax3.text(
            bar.get_x() + bar.get_width()/2,
            bar.get_height(),
            f"{rural_pct:.1f}% rural",
            ha="center",
            va="bottom",
            fontsize=9
        )

    st.pyplot(fig3)

# -----------------------------
# STANDALONE GRAPH
# -----------------------------

fires_per_month = (
    df["month"]
    .value_counts()
    .sort_index()
)

month_names = [
    calendar.month_name[m]
    for m in fires_per_month.index
]

st.header("Wildfire Frequency by Month")

fig4, ax4 = plt.subplots(figsize=(12,6))

bars = ax4.bar(
    month_names,
    fires_per_month.values
)

ax4.set_xlabel("Month")
ax4.set_ylabel("Number of Wildfires")

plt.xticks(rotation=45)

for bar, value in zip(bars, fires_per_month.values):
    ax4.text(
        bar.get_x() + bar.get_width()/2,
        bar.get_height(),
        str(value),
        ha='center',
        va='bottom'
    )

st.pyplot(fig4)
