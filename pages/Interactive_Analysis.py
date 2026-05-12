import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import calendar

st.set_page_config(layout="wide")

# Load data

df = pd.read_csv("processed_wildfire_data.csv")

# Title

st.title("Interactive Analysis")

st.markdown(
    """
    <p style='font-size:20px;'>
    Explore wildfire evacuation lead time trends interactively by state and season.
    </p>
    """,
    unsafe_allow_html=True
)

# KPI calculations

state_summary = (
    df.groupby("state")["lead_time_minutes"]
    .agg(["count", "median"])
)

median_lead_time = df["lead_time_minutes"].median()

total_wildfires = len(df)

fastest_state = state_summary["median"].idxmin()

slowest_state = state_summary["median"].idxmax()

peak_month = (
    df["month"]
    .value_counts()
    .idxmax()
)

worst_month = (
    df.groupby("month")["lead_time_minutes"]
    .median()
    .idxmax()
)

# KPI cards

col1, col2, col3 = st.columns(3)

col1.metric(
    "Median Lead Time",
    f"{median_lead_time:.1f} min"
)

col2.metric(
    "Total Wildfires",
    total_wildfires
)

col3.metric(
    "Fastest State",
    fastest_state
)

col4, col5, col6 = st.columns(3)

col4.metric(
    "Slowest State",
    slowest_state
)

col5.metric(
    "Peak Month",
    calendar.month_name[peak_month]
)

col6.metric(
    "Worst Lead-Time Month",
    calendar.month_name[worst_month]
)

# State selector

states = sorted(df["state"].dropna().unique())

selected_state = st.selectbox(
    "Select a State",
    states
)

state_df = df[
    df["state"] == selected_state
]

# State overview

st.header(f"{selected_state} Overview")

state_col1, state_col2 = st.columns(2)

state_col1.metric(
    "Median Lead Time",
    f"{state_df['lead_time_minutes'].median():.1f} min"
)

state_col2.metric(
    "Incident Count",
    len(state_df)
)

# Monthly trend graph

monthly = (
    state_df.groupby("month")["lead_time_minutes"]
    .median()
)

month_names = [
    calendar.month_name[m]
    for m in monthly.index
]

st.header("Monthly Lead Time Trend")

fig, ax = plt.subplots(figsize=(9,4))

sns.lineplot(
    x=month_names,
    y=monthly.values,
    marker="o",
    ax=ax
)

ax.set_xlabel("Month")
ax.set_ylabel("Median Lead Time (minutes)")

plt.xticks(rotation=45)

st.pyplot(fig)

# Environmental factors

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

precipitation_data = {
    "California": 22.2,
    "Colorado": 15.9,
    "Idaho": 18.9,
    "Montana": 15.3,
    "Nevada": 9.5,
    "Oklahoma": 36.5,
    "Oregon": 27.4,
    "Washington": 38.4,
    "Wyoming": 12.9
}

wind_data = {
    "California": 7.2,
    "Colorado": 9.3,
    "Idaho": 7.8,
    "Montana": 10.1,
    "Nevada": 8.4,
    "Oklahoma": 12.0,
    "Oregon": 6.5,
    "Washington": 6.7,
    "Wyoming": 12.9
}

st.header("Environmental Factors")

env1, env2, env3 = st.columns(3)

env1.metric(
    "Rural Population %",
    rural_data.get(selected_state, "N/A")
)

env2.metric(
    "Avg Annual Precipitation",
    precipitation_data.get(selected_state, "N/A")
)

env3.metric(
    "Average Wind Speed",
    wind_data.get(selected_state, "N/A")
)

# Navigation

st.markdown(
    """
    <br><br>
    ### [← Back to Main Dashboard](../)
    """,
    unsafe_allow_html=True
)
