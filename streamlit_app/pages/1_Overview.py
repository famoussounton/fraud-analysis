import streamlit as st
import polars as pl
import plotly.express as px
from utils import load_data, apply_style, format_number, format_large_number

st.set_page_config(page_title="Overview", page_icon="📊", layout="wide")
apply_style()

st.title("📊 Executive Overview")
st.markdown("Top-level KPIs and strategic insights for decision making.")

df = load_data()

if df is not None:
    # --- KPIs ---
    total_tx = df.height
    total_amount = df["amount"].sum()
    
    fraud_df = df.filter(pl.col("isFraud") == 1)
    total_fraud = fraud_df.height
    fraud_amount = fraud_df["amount"].sum()
    
    fraud_rate_tx = (total_fraud / total_tx) * 100
    fraud_rate_amt = (fraud_amount / total_amount) * 100

    # Using st.columns with a container class concept (via CSS in utils)
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Transactions", format_number(total_tx))
    with col2:
        st.metric("Total Volume", format_large_number(total_amount))
    with col3:
        st.metric("Fraud Count", format_number(total_fraud))
    with col4:
        st.metric("Fraud Volume", format_large_number(fraud_amount))
    with col5:
        st.metric("Fraud Rate (Tx)", f"{fraud_rate_tx:.3f}%", delta=f"{fraud_rate_amt:.3f}% Vol", delta_color="inverse")

    st.divider()

    # --- ROW 1: Charts for Decision Making ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Transaction Volume by Type")
        # Add labels to make it clearer for decision making
        type_agg = df.group_by("type").agg([
            pl.len().alias("count"),
            pl.sum("amount").alias("volume")
        ]).sort("volume", descending=True)
        
        # Donut Chart for Volume Share
        fig_vol = px.pie(
            type_agg.to_pandas(), 
            values="volume", 
            names="type", 
            title="Volume Market Share by Type ($)",
            hole=0.5,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_vol.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#FFF")
        st.plotly_chart(fig_vol, use_container_width=True)

    with col2:
        st.subheader("Fraud Rate by Transaction Type")
        # Which type is riskiest?
        # Calculate fraud rate per type
        risk_df = df.group_by("type").agg([
            pl.len().alias("total"),
            (pl.col("isFraud") == 1).sum().alias("fraud_count")
        ]).with_columns(
            (pl.col("fraud_count") / pl.col("total") * 100).alias("risk_percentage")
        ).sort("risk_percentage", descending=True)
        
        fig_risk = px.bar(
            risk_df.to_pandas(), 
            x="type", 
            y="risk_percentage",
            color="risk_percentage",
            title="Risk Exposure: Fraud Rate % by Type",
            labels={"risk_percentage": "Fraud Rate (%)"},
            color_continuous_scale="Reds"
        )
        fig_risk.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#FFF")
        st.plotly_chart(fig_risk, use_container_width=True)

    # --- ROW 2: Time Analysis ---
    st.subheader("Operational Heatmap")
    
    # Heatmap of Day vs Hour vs Volume (or Count)
    # Aggregating data
    heat_data = df.group_by(["day", "hour"]).agg(pl.len().alias("tx_count")).sort(["day", "hour"])
    
    fig_heat = px.density_heatmap(
        heat_data.to_pandas(), 
        x="hour", 
        y="day", 
        z="tx_count", 
        title="Transaction Load Heatmap (Day vs Hour)",
        color_continuous_scale="Viridis"
    )
    fig_heat.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#FFF")
    st.plotly_chart(fig_heat, use_container_width=True)

else:
    st.error("Data could not be loaded.")
