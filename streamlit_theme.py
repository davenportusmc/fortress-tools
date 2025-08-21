"""Streamlit theme injection utility for Fortress Athlete branding."""

from pathlib import Path
import streamlit as st


def inject_theme():
    """Inject custom CSS theme into Streamlit app."""
    try:
        css_path = Path("styles/theme.css")
        if css_path.exists():
            css = css_path.read_text(encoding="utf-8")
            st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    except Exception as e:
        # Silently fail if theme can't be loaded
        pass
