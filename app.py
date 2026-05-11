import streamlit as st
import pandas as pd

st.title("Column Debugger")

events = pd.read_csv("geo_events_geoevent.csv")
changes = pd.read_csv("geo_events_geoeventchangelog.csv")

st.header("Events Columns")
st.write(events.columns.tolist())

st.header("Changes Columns")
st.write(changes.columns.tolist())
