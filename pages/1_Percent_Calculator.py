"""Percent Calculator Page"""

import streamlit as st
import pandas as pd
from utils.branding import display_logo_and_title, apply_mobile_styles
from utils.units import round_weight, format_weight

# Configure page
st.set_page_config(
    page_title="Percent Calculator - Fortress Athlete Tools",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Apply styling
apply_mobile_styles()

# Display header
display_logo_and_title()

# Back button
if st.button("← Back to Tools", use_container_width=True):
    st.session_state.page = 'home'
    st.rerun()

st.markdown("## Percent Calculator")

# Input section
col1, col2 = st.columns([3, 1])

with col1:
    base_weight = st.number_input(
        "Base weight",
        min_value=0.0,
        value=100.0,
        step=1.0,
        format="%.1f"
    )

with col2:
    unit = st.selectbox("Unit", ["lb", "kg"], index=0)

# Rounding options
rounding = st.selectbox(
    "Rounding",
    ["None", "Nearest 0.5", "Nearest 1.0"],
    index=0
)

# Generate percentage table
if base_weight > 0:
    percentages = list(range(0, 105, 5))  # 0% to 100% in 5% increments
    
    data = []
    for pct in percentages:
        weight = base_weight * (pct / 100)
        rounded_weight = round_weight(weight, rounding, unit)
        data.append({
            "Percent": f"{pct}%",
            "Weight": format_weight(rounded_weight, unit)
        })
    
    df = pd.DataFrame(data)
    
    # Display table
    st.markdown("### Results")
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Percent": st.column_config.TextColumn(width="small"),
            "Weight": st.column_config.TextColumn(width="medium")
        }
    )
    
    # Copy to clipboard functionality
    csv_data = df.to_csv(index=False)
    
    if st.button("Copy Table", use_container_width=True):
        # Use Streamlit's built-in clipboard functionality
        st.code(csv_data, language=None)
        st.success("Table data shown above - copy manually")

else:
    st.info("Enter a base weight to see percentage calculations")
