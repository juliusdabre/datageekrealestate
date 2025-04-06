
import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
df = pd.read_csv("sa3_investment_data.csv")

# Branding Header
st.markdown("""
    <div style='text-align: center; padding: 10px;'>
        <h1 style='color: #FFC0CB; font-size: 48px;'>SA3Trends</h1>
        <h4 style='color: #555;'>Regional Investment Intelligence Dashboard</h4>
    </div>
""", unsafe_allow_html=True)

# Sidebar for SA3 selection
selected_sa3 = st.sidebar.selectbox(" Select an SA3 Region", df["SA3"].unique())

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
#csv = df.to_csv(index=False)
#st.download_button("📥 Download Full Dataset", csv, "sa3_investment_data.csv", "text/csv")

# Plot radar chart
if selected_sa3s:
    fig = go.Figure()
    for sa3 in selected_sa3s:
        row = filtered_df[filtered_df['SA3'] == sa3][score_columns].iloc[0]
        fig.add_trace(go.Scatterpolar(
            r=row.values,
            theta=score_columns,
            fill='toself',
            name=sa3
        ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[1, 5])),
        showlegend=True,
        title="Radar Chart: SA3 Comparison"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Download CSV
    csv_data = filtered_df[filtered_df['SA3'].isin(selected_sa3s)][['SA3'] + score_columns]
    csv = csv_data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Selected Data as CSV",
        data=csv,
        file_name='selected_sa3s.csv',
        mime='text/csv'
    )

    # Download Radar Chart as PDF
    pdf_bytes = pio.to_image(fig, format='pdf')
    st.download_button(
        label="📄 Download Radar Chart as PDF",
        data=pdf_bytes,
        file_name='radar_chart.pdf',
        mime='application/pdf'
    )
else:
    st.info("Please select SA3 regions from the list above.")
