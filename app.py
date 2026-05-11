import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.title("Wildfire Evacuation Lead Time Dashboard")

# LOAD DATA
df = pd.read_csv("geo_events_geoevent.csv")

# PREVIEW
st.subheader("Dataset Preview")
st.dataframe(df.head())

# CHECK REQUIRED COLUMNS
if "state" in df.columns and "lead_time" in df.columns:

    # STATE SUMMARY
    state_summary = (
        df.groupby("state")["lead_time"]
        .agg(["median", "count"])
    )

    state_summary = state_summary[state_summary["count"] >= 15]

    filtered_states = state_summary.sort_values("median")

    # GRAPH
    st.header("Median Evacuation Lead Time by State")

    fig, ax = plt.subplots(figsize=(14,6))

    bars = ax.bar(
        filtered_states.index,
        filtered_states["median"]
    )

    ax.set_xlabel("State")
    ax.set_ylabel("Median Lead Time (minutes)")
    ax.set_title("Median Evacuation Lead Time by State")

    plt.xticks(rotation=45)

    for bar, value in zip(bars, filtered_states["median"]):
        ax.text(
            bar.get_x() + bar.get_width()/2,
            bar.get_height(),
            f"{value:.1f}",
            ha='center',
            va='bottom'
        )

    st.pyplot(fig)

else:
    st.error("Required columns 'state' and/or 'lead_time' not found in dataset.")
