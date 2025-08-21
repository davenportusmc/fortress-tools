"""Branding utilities for Fortress Athlete tools."""

import os
import streamlit as st


def get_logo_url():
    """Get the logo URL from environment variable or use Fortress Athlete default."""
    return os.getenv(
        "FORTRESS_LOGO_URL", 
        "https://fortressathlete.com/wp-content/uploads/2024/09/Logo.webp"
    )


def display_logo_and_title():
    """Display the logo and app title in the header."""
    logo_url = get_logo_url()
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        try:
            st.image(logo_url, width=80)
        except Exception:
            # Fallback to text if logo fails to load
            st.markdown("**FORTRESS**")
    
    with col2:
        st.markdown("# Fortress Athlete Tools")


def apply_mobile_styles():
    """Apply mobile-first CSS styles with theme integration."""
    st.markdown("""
    <style>
    /* Mobile-specific overrides that work with theme */
    .stButton > button {
        width: 100%;
        height: 3rem;
        font-size: 1.1rem;
        margin: 0.5rem 0;
    }
    
    .stNumberInput > div > div > input {
        font-size: 1.1rem;
        text-align: center;
    }
    
    .stDataFrame {
        width: 100%;
    }
    
    .stDataFrame table {
        font-family: 'Courier New', monospace;
    }
    
    .stDataFrame td:last-child {
        text-align: right;
    }
    
    @media (max-width: 768px) {
        .main > div {
            padding: 0.5rem;
        }
        
        .stButton > button {
            height: 3.5rem;
            font-size: 1.2rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)
