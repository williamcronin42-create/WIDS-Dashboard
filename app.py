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

# SHOW AVAILABLE COLUMNS
st.subheader("Available Columns")
st.write(df.columns.tolist())
