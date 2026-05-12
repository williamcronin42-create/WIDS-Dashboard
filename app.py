import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import calendar

st.set_page_config(layout="wide")

# Title and introduction

st.title("Geographic and Seasonal Variation in Wildfire Evacuation Lead Times")

st.markdown(
    """
    <p style='font-size:20px;'>
    This dashboard analyzes WatchDuty wildfire incident data to explore geographic and seasonal variation in evacuation response timing across the United States. Lead time was calculated as the time difference between wildfire creation and the first evacuation-related update.
    </p>
    """,
    unsafe_allow_html=True
)

# Load processed data

df = pd.read_csv("processed_wildfire_data.csv")

# Filter states with at least 15 wildfires

valid_states = (
    df["state"]
    .value_counts()
)

valid_states = valid_states[
    valid_states >= 15
].index

df = df[
    df["state"].isin(valid_states)
]

# Wildfire frequency graph

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

fig1, ax1 = plt.subplots(figsize=(9,4))

sns.barplot(
    x=month_names,
    y=fires_per_month.values,
    palette="crest",
    ax=ax1
)

ax1.set_xlabel("Month")
ax1.set_ylabel("Number of Wildfires")

plt.xticks(rotation=45)

for i, value in enumerate(fires_per_month.values):
    ax1.text(
        i,
        value,
        str(value),
        ha='center',
        va='bottom'
    )

st.pyplot(fig1)

st.markdown(
    """
    <p style='font-size:20px;'>
    Wildfire frequency peaked during the summer months, particularly June through August. However, wildfire frequency alone did not fully explain evacuation response timing patterns observed later in the analysis.
    </p>
    """,
    unsafe_allow_html=True
)

# Dropdown selector

view_option = st.selectbox(
    "Median Evacuation Lead Time By:",
    (
        "State",
        "Month",
        "State with Rural Population Percentage"
    )
)

# State summary calculations

state_summary = (
    df.groupby("state")["lead_time_minutes"]
    .agg(["count", "median"])
    .sort_values("median")
)

filtered_states = state_summary.sort_values("median")

# State graph

if view_option == "State":

    st.header("Median Evacuation Lead Time by State")

    fig2, ax2 = plt.subplots(figsize=(10,4))

    sns.barplot(
        x=filtered_states.index,
        y=filtered_states["median"],
        palette="crest",
        ax=ax2
    )

    ax2.set_xlabel("State")
    ax2.set_ylabel("Median Lead Time (minutes)")

    plt.xticks(rotation=45)

    for i, value in enumerate(filtered_states["median"]):
        ax2.text(
            i,
            value,
            f"{value:.2f}",
            ha='center',
            va='bottom'
        )

    st.pyplot(fig2)

# Month graph

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

    fig3, ax3 = plt.subplots(figsize=(9,4))

    sns.barplot(
        x=month_names,
        y=monthly.values,
        palette="crest",
        ax=ax3
    )

    ax3.set_xlabel("Month")
    ax3.set_ylabel("Median Lead Time (minutes)")

    plt.xticks(rotation=45)

    for i, value in enumerate(monthly.values):
        ax3.text(
            i,
            value,
            f"{value:.2f}",
            ha='center',
            va='bottom'
        )

    st.pyplot(fig3)

# Rural population graph

elif view_option == "State with Rural Population Percentage":

    factor_data = pd.DataFrame({
        "state": [
            "Oklahoma", "Colorado", "Nevada", "California", "Washington", "Utah",
            "Oregon", "Arizona", "Wyoming", "Montana", "New Mexico", "Idaho"
        ],
        "rural_pct": [
            35.8, 14.4, 6.2, 5.8, 16.6, 10.8,
            19.7, 11.5, 37.4, 47.1, 24.7, 30.8
        ]
    })

    state_rural_summary = (
        filtered_states
        .merge(factor_data, left_index=True, right_on="state")
    )

    st.header(
        "Median Evacuation Lead Time by State with Rural Population Percentage"
    )

    fig4, ax4 = plt.subplots(figsize=(10,4))

    sns.barplot(
        x=state_rural_summary["state"],
        y=state_rural_summary["median"],
        palette="crest",
        ax=ax4
    )

    ax4.set_xlabel("State")
    ax4.set_ylabel("Median Lead Time (minutes)")

    plt.xticks(rotation=45)

    for i, rural_pct in enumerate(
        state_rural_summary["rural_pct"]
    ):
        ax4.text(
            i,
            state_rural_summary["median"].iloc[i],
            f"{rural_pct:.1f}% rural",
            ha="center",
            va="bottom",
            fontsize=8
        )

    st.pyplot(fig4)

# Conclusion

st.header("Key Takeaways")

st.markdown(
    """
    <p style='font-size:20px;'>
    Evacuation lead times varied substantially across states and seasons. Rural and geographically isolated regions generally experienced slower evacuation response times. Wildfire frequency alone did not fully explain evacuation delays, suggesting that operational preparedness and infrastructure likely play a significant role.
    </p>
    """,
    unsafe_allow_html=True
)

# Divider

st.markdown("---")

# Interactive analysis section

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

interactive_summary = (
    df.groupby("state")["lead_time_minutes"]
    .agg(["count", "median"])
)

median_lead_time = df["lead_time_minutes"].median()

total_wildfires = len(df)

fastest_state = interactive_summary["median"].idxmin()

slowest_state = interactive_summary["median"].idxmax()

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
    f"{median_lead_time:.2f} min"
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
    states,
    key="interactive_state"
)

state_df = df[
    df["state"] == selected_state
]

# State overview

st.header(f"{selected_state} Overview")

state_col1, state_col2 = st.columns(2)

state_col1.metric(
    "Median Lead Time",
    f"{state_df['lead_time_minutes'].median():.2f} min"
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

fig5, ax5 = plt.subplots(figsize=(9,4))

sns.lineplot(
    x=month_names,
    y=monthly.values,
    marker="o",
    ax=ax5
)

ax5.set_xlabel("Month")
ax5.set_ylabel("Median Lead Time (minutes)")

plt.xticks(rotation=45)

st.pyplot(fig5)

# Environmental data

factor_data = pd.DataFrame({
    "state": [
        "Oklahoma", "Colorado", "Nevada", "California", "Washington", "Utah",
        "Oregon", "Arizona", "Wyoming", "Montana", "New Mexico", "Idaho"
    ],
    "rural_pct": [
        35.8, 14.4, 6.2, 5.8, 16.6, 10.8,
        19.7, 11.5, 37.4, 47.1, 24.7, 30.8
    ],
    "precipitation": [
        36.5, 15.9, 9.5, 22.2, 38.4, 12.2,
        27.4, 13.6, 12.9, 15.3, 14.6, 18.9
    ],
    "wind_speed": [
        16.46, 20.16, 17.43, 13.54, 15.03, 18.26,
        16.38, 15.92, 20.88, 21.03, 17.82, 20.59
    ]
})

selected_factor = factor_data[
    factor_data["state"] == selected_state
]

# Environmental factors

st.header("Environmental Factors")

env1, env2, env3 = st.columns(3)

env1.metric(
    "Rural Population %",
    f"{selected_factor['rural_pct'].iloc[0]:.1f}%"
)

env2.metric(
    "Avg Annual Precipitation",
    f"{selected_factor['precipitation'].iloc[0]:.1f} in"
)

env3.metric(
    "Average Wind Speed",
    f"{selected_factor['wind_speed'].iloc[0]:.2f} mph"
)
