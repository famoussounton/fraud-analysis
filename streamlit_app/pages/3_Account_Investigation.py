import streamlit as st
import polars as pl
from utils import load_data, apply_style

st.set_page_config(page_title="Investigation", page_icon="🕵️", layout="wide")
apply_style()

st.title("🕵️ Forensic Account Trace")
st.markdown("Search across millions of transactions to investigate specific entities.")

df = load_data()

if df is not None:
    # Modern input with columns
    col_input, col_status = st.columns([2, 1])
    
    with col_input:
        search_query = st.text_input("Entity ID Search (Origin or Destination)", placeholder="e.g. C12345678")

    if search_query:
        st.divider()
        st.subheader("Investigation Results")
        
        # Search optimized with Polars
        results = df.filter(
            (pl.col("nameOrig") == search_query) | (pl.col("nameDest") == search_query)
        )
        
        if results.height > 0:
            # Fraud check
            fraud_tx = results.filter(pl.col("isFraud") == 1)
            
            # KPI Cards for the entity
            kpi1, kpi2, kpi3 = st.columns(3)
            kpi1.metric("Total Activities", results.height)
            kpi2.metric("Total Volume", f"${results['amount'].sum():,.2f}")
            
            if fraud_tx.height > 0:
                kpi3.metric("Fraudulent Events", fraud_tx.height, delta="CRITICAL", delta_color="inverse")
                st.error(f"🚨 **ALERT**: This entity is linked to {fraud_tx.height} confirmed fraud cases.")
            else:
                kpi3.metric("Fraudulent Events", "0", delta="Clean", delta_color="normal")
                st.success("✅ Clean Record: No fraud flags detected in available history.")
            
            st.markdown("#### Transaction Ledger")
            # Style the dataframe (pandas styler can be used, but keeping it simple for speed)
            st.dataframe(
                results.to_pandas(), 
                use_container_width=True,
                hide_index=True
            )
            
        else:
            st.warning("⚠️ Entity not found in the transaction registry.")
    
    st.divider()
    
    with st.expander("Show Latest Flagged Entities (Live Feed)"):
        fraud_sample = df.filter(pl.col("isFraud") == 1).head(10)
        st.table(fraud_sample.select(["step", "type", "amount", "nameOrig", "isFraud"]).to_pandas())

else:
    st.error("Database connection failed.")
