import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
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

# Sidebar for SA3 selection
selected_sa3s = st.sidebar.multiselect("\ud83d\udccd Select SA3 Region(s)", df["SA3"].unique())

# Show KPIs only for the first selected SA3
if selected_sa3s:
    sa3 = df[df["SA3"] == selected_sa3s[0]].iloc[0]

    # KPIs
    col1, col2, col3 = st.columns(3)
    col1.metric("\ud83d\udcb0 Median Price", f"${int(sa3['Median Price']):,}")
    col2.metric("\ud83d\udcc8 12M Growth", f"{sa3['12M Growth (%)']}%")
    col3.metric("\ud83d\udcb8 Yield", f"{sa3['Yield (%)']}%")

    col4, col5, col6 = st.columns(3)
    col4.metric("\ud83d\udcca Rent Change", f"{sa3['Rent Change (%)']}%")
    col5.metric("\ud83e\uddf6 Buy Affordability", f"{sa3['Buy Affordability']} yrs")
    col6.metric("\ud83d\udcc9 Rent Affordability", f"{sa3['Rent Affordability']}%")

    st.metric("\ud83d\udcc8 10Y Growth (PA)", f"{sa3['10Y Growth (PA)']}%")

# Map visualization
st.subheader("\ud83d\uddfa SA3 Location Map")
fig = px.scatter_map(
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
st.plotly_chart(fig)

# Heatmap instead of Radar Chart
if selected_sa3s:
    st.subheader("\ud83d\udd25 Score Heatmap Comparison")
    score_columns = ["Median Price", "12M Growth (%)", "Yield (%)", "Rent Change (%)", "Buy Affordability", "Rent Affordability", "10Y Growth (PA)"]
    filtered_df = df[df['SA3'].isin(selected_sa3s)].set_index("SA3")[score_columns]

    fig, ax = plt.subplots(figsize=(10, len(selected_sa3s) * 0.5 + 2))
    sns.heatmap(filtered_df, annot=True, fmt=".1f", cmap="coolwarm", linewidths=0.5, ax=ax)
    plt.title("SA3 Comparison Heatmap")
    st.pyplot(fig)

# PDF Report Generation
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
        row = df[df['SA3'] == sa3].iloc[0]
        filename = f"report_{sa3.replace(' ', '_')}.pdf"
        generate_pdf(row, filename)
        with open(filename, "rb") as f:
            st.download_button(
                label=f"\ud83d\udcc4 Download PDF Report - {sa3}",
                data=f,
                file_name=filename,
                mime="application/pdf"
            )
        os.remove(filename)

# Download full data
csv = df.to_csv(index=False)
st.download_button("\ud83d\udcc5 Download Full Dataset", csv, "sa3_investment_data.csv", "text/csv")
