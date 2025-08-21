"""Barbell Calculator Page"""

import streamlit as st
from utils.branding import display_logo_and_title, apply_mobile_styles
from utils.units import get_default_bar_weight, get_default_plates, convert_weight, format_weight
from utils.plates import PLATE_WEIGHTS, PLATE_COLORS, calculate_total_weight, calculate_per_side_weight, format_per_side_breakdown, generate_barbell_visualization

# Configure page
st.set_page_config(
    page_title="Barbell Calculator - Fortress Athlete Tools",
    page_icon="🏋️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Apply styling
apply_mobile_styles()

# Display header
display_logo_and_title()

# Back button
if st.button("← Back to Tools", use_container_width=True):
    # This page is standalone, redirect to main app
    st.switch_page("app.py")

st.markdown("## Barbell Calculator")

# Initialize session state
if 'unit' not in st.session_state:
    st.session_state.unit = "lb"
if 'plates' not in st.session_state:
    st.session_state.plates = get_default_plates("lb")

# Input section
col1, col2 = st.columns(2)

with col1:
    new_unit = st.selectbox("Units", ["lb", "kg"], index=0 if st.session_state.unit == "lb" else 1)
    
    # Handle unit conversion
    if new_unit != st.session_state.unit:
        # Convert existing plate weights
        old_plates = st.session_state.plates
        new_plates = {}
        for weight, count in old_plates.items():
            new_weight = convert_weight(weight, st.session_state.unit, new_unit)
            new_plates[new_weight] = count
        st.session_state.plates = new_plates
        st.session_state.unit = new_unit

with col2:
    bar_weight = st.number_input(
        "Bar weight",
        min_value=0.0,
        value=get_default_bar_weight(st.session_state.unit),
        step=1.0,
        format="%.1f"
    )

# Target weight
target_total = st.number_input(
    "Target total weight",
    min_value=0.0,
    value=225.0 if st.session_state.unit == "lb" else 100.0,
    step=1.0,
    format="%.1f"
)

# Collars
use_collars = st.checkbox("Include collars")
collar_weight = 0.0
if use_collars:
    collar_weight = st.number_input(
        "Collar weight (total for pair)",
        min_value=0.0,
        value=5.0 if st.session_state.unit == "lb" else 2.5,
        step=0.5,
        format="%.1f"
    )

# Plate configuration
st.markdown("### Available Plates")

# Reset to defaults button
if st.button("Reset to Defaults"):
    st.session_state.plates = get_default_plates(st.session_state.unit)
    st.rerun()

# Plate inputs
plate_cols = st.columns(3)
plate_weights = sorted(st.session_state.plates.keys(), reverse=True)

for i, weight in enumerate(plate_weights):
    col_idx = i % 3
    with plate_cols[col_idx]:
        enabled = st.checkbox(f"{format_weight(weight, st.session_state.unit)}", value=True, key=f"enable_{weight}")
        if enabled:
            count = st.number_input(
                f"Count",
                min_value=0,
                value=st.session_state.plates[weight],
                step=1,
                key=f"count_{weight}"
            )
            st.session_state.plates[weight] = count
        else:
            st.session_state.plates[weight] = 0

# Calculation
st.markdown("### Results")

if target_total < bar_weight:
    st.error("Target weight cannot be less than bar weight")
else:
    # Calculate required plate weight per side
    required_plate_weight = target_total - bar_weight - collar_weight
    target_per_side = required_plate_weight / 2
    
    if target_per_side < 0:
        st.error("Target weight is less than bar + collar weight")
    else:
        # Get available plates (only enabled ones with count > 0)
        available_plates = {w: c for w, c in st.session_state.plates.items() if c > 0}
        
        # Pack plates
        prefer_over = st.checkbox("Prefer going over target", value=False)
        plates, achieved_per_side, delta = pack_plates(target_per_side, available_plates, prefer_over)
        
        achieved_total = bar_weight + collar_weight + (achieved_per_side * 2)
        
        # Summary chips
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Target", format_weight(target_total, st.session_state.unit))
        with col2:
            st.metric("Achieved", format_weight(achieved_total, st.session_state.unit))
        with col3:
            delta_total = achieved_total - target_total
            st.metric("Delta", format_weight(abs(delta_total), st.session_state.unit), 
                     delta=f"{'Over' if delta_total > 0 else 'Under'}" if delta_total != 0 else "Exact")
        
        # Per-side breakdown
        if plates:
            st.markdown("#### Per Side Breakdown")
            plate_text = format_plate_stack(plates, st.session_state.unit)
            st.write(f"**{plate_text}**")
            st.write(f"Per side weight: {format_weight(achieved_per_side, st.session_state.unit)}")
            
            # Visualization
            st.markdown("#### Plate Visualization")
            
            # Create visual representation
            colors = calculate_plate_colors(plates, st.session_state.unit)
            
            # Left side (reversed order for visual effect)
            left_html = ""
            for (color, count), (weight, _) in zip(reversed(colors), reversed(plates)):
                for _ in range(count):
                    left_html += f'<div style="display:inline-block; width:20px; height:60px; background-color:{color}; border:1px solid #333; margin:1px;"></div>'
            
            # Bar
            bar_html = '<div style="display:inline-block; width:100px; height:10px; background-color:#666; margin:25px 5px;"></div>'
            
            # Right side
            right_html = ""
            for color, count in colors:
                for _ in range(count):
                    right_html += f'<div style="display:inline-block; width:20px; height:60px; background-color:{color}; border:1px solid #333; margin:1px;"></div>'
            
            visualization = f'<div style="text-align:center; margin:20px 0;">{left_html}{bar_html}{right_html}</div>'
            st.markdown(visualization, unsafe_allow_html=True)
            
        else:
            st.warning("Cannot achieve target weight with available plates")
            if target_per_side > 0:
                st.write(f"Need {format_weight(target_per_side, st.session_state.unit)} per side")
