
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from fpdf import FPDF
import os

# Load the data
df = pd.read_csv("sa3_investment_data.csv")

# Branding Header
st.markdown("""
    <div style='text-align: center; padding: 10px;'>
        <img src='https://raw.githubusercontent.com/yourusername/assets/main/propwealthnext_logo.png' width='150'>
        <h1 style='color: #2E86C1; font-size: 48px;'>PropwealthNext</h1>
        <h4 style='color: #555;'>Regional Investment Intelligence Dashboard</h4>
    </div>
""", unsafe_allow_html=True)

# Sidebar filters
st.sidebar.header("🔍 Filters")
price_range = st.sidebar.slider("💰 Median Price Range", int(df["Median Price"].min()), int(df["Median Price"].max()), (int(df["Median Price"].min()), int(df["Median Price"].max())))
yield_min = st.sidebar.slider("📈 Min Yield (%)", 0.0, 10.0, 0.0, 0.1)

# Apply filters
filtered_df_all = df[(df["Median Price"] >= price_range[0]) & (df["Median Price"] <= price_range[1]) & (df["Yield (%)"] >= yield_min)]

# Sidebar for SA3 selection
selected_sa3s = st.sidebar.multiselect(" Select SA3 Region(s)", filtered_df_all["SA3"].unique())

# Show KPIs only for the first selected SA3
if selected_sa3s:
    sa3 = filtered_df_all[filtered_df_all["SA3"] == selected_sa3s[0]].iloc[0]

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

# Tabs layout
map_tab, chart_tab, download_tab = st.tabs(["🗺 Map View", "📊 Chart View", "📄 Reports & Data"])

with map_tab:
    st.subheader("🗺 SA3 Location Map")
    fig = px.scatter_map(
        filtered_df_all,
        lat="Latitude",
        lon="Longitude",
        hover_name="SA3",
        size="Yield (%)",
        color="12M Growth (%)",
        color_continuous_scale="Viridis",
        zoom=4,
        height=500
    )
    st.plotly_chart(fig)

with chart_tab:
    if selected_sa3s:
        st.subheader("📊 SA3 Score Comparison - Grouped Bar Chart")
        score_columns = ["Median Price", "12M Growth (%)", "Yield (%)", "Rent Change (%)", "Buy Affordability", "Rent Affordability", "10Y Growth (PA)"]
        filtered_df = filtered_df_all[filtered_df_all['SA3'].isin(selected_sa3s)][["SA3"] + score_columns]

        # Melt for bar chart
        bar_df = filtered_df.melt(id_vars="SA3", value_vars=score_columns, var_name="Metric", value_name="Value")

        fig = px.bar(bar_df, x="Metric", y="Value", color="SA3", barmode="group",
                     height=600, labels={"Value": "Score"}, title="SA3 Comparison")
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig)

        # Chart export button
        st.download_button("📸 Download Chart as HTML", data=fig.to_html(), file_name="chart.html")

with download_tab:
    if selected_sa3s:
        def generate_pdf(sa3_data, filename):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.set_text_color(40, 40, 40)

            # Add logo (optional)
            logo_path = "propwealthnext_logo.png"
            if os.path.exists(logo_path):
                pdf.image(logo_path, x=10, y=8, w=30)
                pdf.ln(20)

            pdf.cell(200, 10, txt=f"PropwealthNext Report - {sa3_data['SA3']}", ln=True, align='C')
            pdf.ln(10)

            for col in score_columns:
                pdf.cell(200, 10, txt=f"{col}: {sa3_data[col]}", ln=True)

            pdf.output(filename)

        for sa3 in selected_sa3s:
            row = filtered_df_all[filtered_df_all['SA3'] == sa3].iloc[0]
            filename = f"report_{sa3.replace(' ', '_')}.pdf"
            generate_pdf(row, filename)
            with open(filename, "rb") as f:
                st.download_button(
                    label=f"📄 Download PDF Report - {sa3}",
                    data=f,
                    file_name=filename,
                    mime="application/pdf"
                )
            os.remove(filename)

    csv = filtered_df_all.to_csv(index=False)
    st.download_button("🗃 Download Filtered Dataset", csv, "sa3_investment_data.csv", "text/csv")
