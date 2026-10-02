import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="CoinGecko Live Dashboard", layout="wide")
st.markdown(
    """
    <div style="background-color:#1E1E2F;padding:20px;border-radius:10px;margin-bottom:20px;">
        <h1 style="color:white;text-align:center;">🪙 Live Crypto Price Dashboard</h1>
        <p style="color:#AAAAAA;text-align:center;">Real-time prices, updated hourly</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Connect to the database
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    ssl_disabled=False
)

# Load all data into a table
df = pd.read_sql("SELECT * FROM prices ORDER BY fetched_at ASC", conn)
conn.close()

# Show latest prices
st.subheader("Latest Prices")
latest = df.sort_values("fetched_at").groupby("coin").tail(1)
col1, col2 = st.columns(2)
for i, row in latest.iterrows():
    col = col1 if row["coin"] == "bitcoin" else col2
    change_color = "#4CAF50" if row["change_24h"] >= 0 else "#F44336"
    arrow = "▲" if row["change_24h"] >= 0 else "▼"
    col.markdown(
        f"""
        <div style="background-color:#2A2A3C;padding:20px;border-radius:10px;text-align:center;">
            <p style="color:#AAAAAA;margin:0;font-size:16px;">{row['coin'].capitalize()}</p>
            <h2 style="color:white;margin:5px 0;">${row['price_usd']:,.2f}</h2>
            <p style="color:{change_color};margin:0;">{arrow} {row['change_24h']:.2f}%</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Price trend chart
st.subheader("Price Trend Over Time")
fig = px.line(df, x="fetched_at", y="price_usd", color="coin", markers=True)
fig.update_layout(
    plot_bgcolor="#1E1E2F",
    paper_bgcolor="#1E1E2F",
    font_color="white",
    legend_title_text="Coin",
    xaxis_title="Time",
    yaxis_title="Price (USD)"
)
st.plotly_chart(fig, use_container_width=True)
# Raw data table
st.markdown("---")
st.subheader("📊 Raw Data")
st.caption("Full history of fetched prices, most recent first")
st.dataframe(
    df.sort_values("fetched_at", ascending=False),
    use_container_width=True,
    hide_index=True
)