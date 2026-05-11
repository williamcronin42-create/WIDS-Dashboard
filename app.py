import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.title("Wildfire Evacuation Lead Time Dashboard")

st.markdown("""
This dashboard analyzes geographic and seasonal variation
in wildfire evacuation response timing across U.S. states.

Key findings:
- Rural states often showed slower evacuation lead times
- September had the highest median lead time
- California demonstrated strong operational responsiveness
""")

# LOAD DATA
df = pd.read_csv("geo_events_geoevent.csv")

# OVERVIEW METRICS
st.header("Dataset Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Events", len(df))

with col2:
    st.metric("Total Columns", len(df.columns))

with col3:
    st.metric("Missing Values", int(df.isna().sum().sum()))

# DATA PREVIEW
st.subheader("Dataset Preview")
st.dataframe(df.head())

# INTERACTIVE HISTOGRAM
st.header("Interactive Distribution Analysis")

numeric_cols = df.select_dtypes(include='number').columns

selected_col = st.selectbox(
    "Select Numeric Variable",
    numeric_cols
)

fig, ax = plt.subplots(figsize=(8,4))

ax.hist(df[selected_col].dropna())

ax.set_title(f"Distribution of {selected_col}")

st.pyplot(fig)

# KEY FINDINGS
st.header("Key Findings")

st.markdown("""
### Geographic Variation
California demonstrated relatively fast evacuation response
despite high wildfire frequency.

### Seasonal Variation
September showed the highest median evacuation lead times
despite lower wildfire frequency than peak summer months.

### Rurality Effects
States with larger rural populations generally experienced
longer evacuation lead times.
""")

# POLICY RECOMMENDATIONS
st.header("Operational Recommendations")

st.markdown("""
- Improve rural wildfire communication infrastructure
- Expand cross-state evacuation coordination
- Increase staffing support before peak wildfire season
- Improve wildfire detection systems
""")
