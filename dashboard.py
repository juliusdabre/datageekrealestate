
import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
df = pd.read_csv("sa3_investment_data.csv")

# Branding Header
st.markdown("""
    <div style='text-align: center; padding: 10px;'>
        <h1 style='color: #2E86C1; font-size: 48px;'>PropwealthNext</h1>
        <h4 style='color: #555;'>Regional Investment Intelligence Dashboard</h4>
    </div>
""", unsafe_allow_html=True)

# Sidebar for SA3 selection
selected_sa3 = st.sidebar.selectbox("📍 Select an SA3 Region", df["SA3"].unique())

# Filter data
sa3 = df[df["SA3"] == selected_sa3].iloc[0]

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("💰 Median Price", f"${int(sa3['Median Price']):,}")
col2.metric("📈 12M Growth", f"{sa3['12M Growth (%)']}%")
col3.metric("💸 Yield", f"{sa3['Yield (%)']}%")

col4, col5, col6 = st.columns(3)
col4.metric("📊 Rent Change", f"{sa3['Rent Change (%)']}%")
col5.metric("🧮 Buy Affordability", f"{sa3['Buy Affordability']} yrs")
col6.metric("📉 Rent Affordability", f"{sa3['Rent Affordability']}%")

st.metric("📈 10Y Growth (PA)", f"{sa3['10Y Growth (PA)']}%")

# Map visualization
st.subheader("🗺 SA3 Location Map")
fig = px.scatter_mapbox(
    df,
    lat="Latitude",
    lon="Longitude",
    hover_name="SA3",
    size="Yield (%)",
    color="12M Growth (%)",
    color_continuous_scale="Viridis",
    zoom=4,
    height=500
)
fig.update_layout(mapbox_style="open-street-map")
st.plotly_chart(fig)

# Download full data
csv = df.to_csv(index=False)
st.download_button("📥 Download Full Dataset", csv, "sa3_investment_data.csv", "text/csv")
