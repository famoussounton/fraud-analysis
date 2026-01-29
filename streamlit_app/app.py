import streamlit as st
import polars as pl
from utils import load_data, apply_style

# Page config
st.set_page_config(
    page_title="FraudSense Analytics",
    page_icon="🛡️",
    layout="wide",
)

# Apply global styles
apply_style()

# --- MAIN PAGE CONTENT ---
st.title("🛡️ FraudSense Analytics")
st.markdown("#### Enterprise-Grade Financial Security & Analysis")

st.divider()

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("""
    ### Welcome
    
    This platform provides advanced analytical capabilities for detecting money laundering and fraudulent transaction patterns.
    
    **Key Modules:**
    
    *   **📊 Overview**: Executive summary and key performance indicators.
    *   **🔍 Fraud Analysis**: Deep dive into fraud typologies like "TRANSFER-CASH_OUT" schemes.
    *   **🕵️ Account Investigation**: Forensic tool for tracing individual account activities.
    """)
    
    st.info("👈 Select a module from the sidebar to begin.")

with col2:
    # A professional, darker, more abstract image
    st.image("https://images.unsplash.com/photo-1551288049-bebda4e38f71?ixlib=rb-4.0.3&auto=format&fit=crop&w=1470&q=80", 
             caption="Real-time Transaction Monitoring", use_container_width=True)

# Pre-load data status check
df = load_data()
if df is not None:
    size_mb = df.estimated_size("mb")
    st.success(f"✅ System Online. Connected to Data Lake. Records: {df.height:,} | Size: {size_mb:.2f} MB")
else:
    st.error("❌ System Offline. Data source not found.")
