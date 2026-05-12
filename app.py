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

bars = sns.barplot(
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

state_summary = state_summary[
    state_summary["count"] >= 15
]

filtered_states = state_summary.sort_values("median")

# State graph

if view_option == "State":

    st.header("Median Evacuation Lead Time by State")

    fig2, ax2 = plt.subplots(figsize=(10,4))

    bars = sns.barplot(
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
            f"{value:.1f}",
            ha='center',
            va='bottom'
        )

    st.pyplot(fig2)

    st.markdown(
        """
        <p style='font-size:20px;'>
        California demonstrated relatively fast evacuation update timing despite having the largest wildfire volume in the dataset. This suggests that operational maturity and wildfire preparedness infrastructure may significantly improve evacuation responsiveness.
        </p>
        """,
        unsafe_allow_html=True
    )

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

    bars = sns.barplot(
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
            f"{value:.1f}",
            ha='center',
            va='bottom'
        )

    st.pyplot(fig3)

    st.markdown(
        """
        <p style='font-size:20px;'>
        September exhibited the highest median evacuation lead times despite not having the highest wildfire frequency. This suggests operational and environmental factors beyond wildfire volume may contribute to delayed evacuation responses.
        </p>
        """,
        unsafe_allow_html=True
    )

# Rural population graph

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

    fig4, ax4 = plt.subplots(figsize=(10,4))

    bars = sns.barplot(
        x=state_rural_summary.index,
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

    st.markdown(
        """
        <p style='font-size:20px;'>
        States with larger rural populations generally exhibited longer evacuation lead times. However, the relationship was not perfectly linear, suggesting that operational preparedness and infrastructure can partially mitigate rural response challenges.
        </p>
        """,
        unsafe_allow_html=True
    )

# Conclusion

st.header("Key Takeaways")

st.markdown(
    """
    <p style='font-size:20px;'>
    Evacuation lead times varied substantially across states and seasons. Rural and geographically isolated regions generally experienced slower evacuation response times. Wildfire frequency alone did not fully explain evacuation delays, suggesting that operational preparedness and infrastructure likely play a significant role. These findings support targeted investments in rural wildfire response systems, staffing readiness, and evacuation communication infrastructure.
    </p>
    """,
    unsafe_allow_html=True
)

# Navigation

st.markdown(
    """
    <br><br>
    ### [Next Page → Interactive Analysis](./Interactive_Analysis)
    """,
    unsafe_allow_html=True
)
