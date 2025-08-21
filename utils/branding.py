"""Branding utilities for Fortress Athlete tools."""

import os
import base64
import streamlit as st


def get_logo_path():
    """Get the local logo path."""
    return "assets/fortress-logo.png"


def _get_logo_base64(logo_path):
    """Convert logo image to base64 for inline embedding."""
    try:
        with open(logo_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception:
        return ""


def display_logo_and_title():
    """Display the logo and app title in the header."""
    logo_path = get_logo_path()
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        try:
            # Display logo with black background using HTML
            logo_base64 = _get_logo_base64(logo_path)
            if logo_base64:
                st.markdown(f"""
                <div style="background-color: #000000; padding: 8px; border-radius: 8px; display: inline-block; margin-bottom: 8px;">
                    <img src="data:image/png;base64,{logo_base64}" style="width: 60px; height: auto;">
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("**FORTRESS**")
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
