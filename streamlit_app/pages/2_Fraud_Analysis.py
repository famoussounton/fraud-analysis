import streamlit as st
import polars as pl
import plotly.express as px
from utils import load_data, apply_style, format_large_number

st.set_page_config(page_title="Fraud Analysis", page_icon="🔍", layout="wide")
apply_style()

st.title("🔍 Fraud Deep Dive")
st.markdown("Advanced forensics and pattern recognition.")

df = load_data()

if df is not None:
    fraud_df = df.filter(pl.col("isFraud") == 1)
    
    # --- Context Counts ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Fraud Cases", f"{fraud_df.height:,}")
    col2.metric("Avg Fraud Amount", f"${fraud_df['amount'].mean():,.2f}")
    col3.metric("Max Single Fraud", format_large_number(fraud_df['amount'].max()))
    
    st.divider()

    # --- Analysis Row 1 ---
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Fraudulent Transaction Methods")
        # Bar chart sorted
        f_counts = fraud_df["type"].value_counts().sort("count", descending=True)
        fig_type = px.bar(
            f_counts.to_pandas(), 
            y="type", 
            x="count", 
            orientation='h',
            title="Most Common Fraud Methods",
            color="count",
            color_continuous_scale="Oranges"
        )
        fig_type.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#FFF")
        st.plotly_chart(fig_type, use_container_width=True)

    with col2:
        st.subheader("Fraud Amount Distribution (Log Scale)")
        # Histogram with Log Y to see small vs large better
        fig_hist = px.histogram(
            fraud_df.to_pandas(), 
            x="amount", 
            nbins=50, 
            title="Distribution of Stolen Amounts",
            color_discrete_sequence=['#EF4444'],
            log_y=True
        )
        fig_hist.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#FFF")
        st.plotly_chart(fig_hist, use_container_width=True)

    # --- Analysis Row 2 : Strategies ---
    st.subheader("Behavioral Patterns")
    
    c1, c2 = st.columns(2)
    
    with c1:
        # Flagged vs Actual
        flagged_analysis = fraud_df.group_by("isFlaggedFraud").agg(pl.len().alias("count"))
        fig_flag = px.pie(
            flagged_analysis.to_pandas(), 
            names="isFlaggedFraud", 
            values="count",
            title="System Detection Rate (Flagged vs Missed)",
            hole=0.6,
            color_discrete_sequence=["#EF4444", "#3B82F6"]
        )
        fig_flag.update_traces(labels=['Missed', 'Flagged']) # Assuming 0 is missed, 1 is flagged
        fig_flag.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#FFF")
        st.plotly_chart(fig_flag, use_container_width=True)
        
    with c2:
        # Step/Time series of fraud
        # Are attacks coordinated in time?
        fraud_over_time = fraud_df.group_by("step").agg(pl.len().alias("attacks")).sort("step")
        fig_time = px.line(
            fraud_over_time.to_pandas(), 
            x="step", 
            y="attacks", 
            title="Timeline of Fraud Attacks (Step)",
            color_discrete_sequence=["#F59E0B"]
        )
        fig_time.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#FFF")
        st.plotly_chart(fig_time, use_container_width=True)

    st.info("💡 **Insight**: 'Step' represents 1 hour of time. Spikes indicate coordinated botnet attacks.")

else:
    st.error("Data could not be loaded.")
