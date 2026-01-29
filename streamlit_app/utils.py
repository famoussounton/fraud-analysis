import streamlit as st
import polars as pl
import os

def load_data():
    """Loads the dataset from chunks (optimized for GitHub/Streamlit Cloud)."""
    # Try reading singular local file first (dev mode)
    base_dir = os.path.join(os.path.dirname(__file__), "../data")
    local_file = os.path.join(base_dir, "final.parquet")
    chunk_dir = os.path.join(base_dir, "fraud_data_chunks")

    # If chunks exist, use them (Simulates Cloud Env / GitHub Repo structure)
    if os.path.exists(chunk_dir):
        # Polars can read a directory of parquets automatically!
        # It treats the folder effectively as a single dataset.
        return pl.read_parquet(f"{chunk_dir}/*.parquet")
    
    # Fallback to single file
    elif os.path.exists(local_file):
        return pl.read_parquet(local_file)
    
    return None

def apply_style():
    """Applies a professional CSS style to the streamlit app."""
    st.markdown("""
        <style>
        /* Main App Background */
        .stApp {
            background-color: #0E1117;
            color: #FFFFFF;
        }
        
        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #262730;
            border-right: 1px solid #41424C;
        }
        
        /* Typography - Force White */
        h1, h2, h3, h4, h5, h6, p, div, span, label, .stMarkdown {
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            color: #FFFFFF !important;
        }
        
        /* Metric Cards - Equal Height & White Text */
        div[data-testid="stMetric"] {
            background-color: #1F2937;
            border: 1px solid #374151;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            padding: 20px;
            border-radius: 8px;
            color: #FFFFFF;
            height: 100%; /* Try to fill container */
            min-height: 140px; /* Enforce minimum height */
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        
        div[data-testid="stMetricLabel"] {
            color: #9CA3AF !important; /* Lighter gray for label */
            font-size: 1rem;
            font-weight: 500;
        }
        
        div[data-testid="stMetricValue"] {
            color: #FFFFFF !important;
            font-size: 1.8rem;
            font-weight: 700;
        }
        
        /* DataFrame styling */
        div[data-testid="stDataFrame"] {
            background-color: #1F2937;
            border-radius: 8px;
            padding: 10px;
            border: 1px solid #374151;
        }

        /* Chart/Plotly backgrounds transparent */
        .js-plotly-plot .plotly .main-svg {
            background-color: rgba(0,0,0,0) !important;
        }
        
        /* Dividers */
        hr {
            border-top: 1px solid #374151;
        }
        </style>
    """, unsafe_allow_html=True)

def format_currency(value):
    """Formats a number as currency."""
    return f"${value:,.2f}"

def format_large_number(value):
    """Formats large numbers nicely (K, M, B)."""
    if value >= 1_000_000_000:
        return f"${value / 1_000_000_000:.2f}B"
    elif value >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"
    elif value >= 1_000:
        return f"${value / 1_000:.2f}K"
    else:
        return f"${value:,.2f}"

def format_number(value):
    """Formats a large number with commas."""
    return f"{value:,}"
