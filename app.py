"""Fortress Athlete Tools - Main Application"""

import streamlit as st
import pandas as pd
from streamlit_theme import inject_theme
from utils.branding import display_logo_and_title, apply_mobile_styles
from utils.units import get_default_bar_weight, get_default_plates, convert_weight, format_weight, round_weight
from utils.plates import (
    PLATE_WEIGHTS, PLATE_COLORS, calculate_total_weight, 
    calculate_per_side_weight, format_per_side_breakdown, 
    generate_barbell_visualization
)

# Configure page
st.set_page_config(
    page_title="Fortress Athlete Tools",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply styling
inject_theme()
apply_mobile_styles()

# Initialize session state for navigation
if 'page' not in st.session_state:
    st.session_state.page = 'home'

def show_home_page():
    """Display the home page with navigation buttons."""
    display_logo_and_title()
    st.markdown("---")
    
    # Navigation buttons
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("Percent Calculator", use_container_width=True):
            st.session_state.page = 'percent'
            st.rerun()
    
    with col2:
        if st.button("Barbell Calculator", use_container_width=True):
            st.session_state.page = 'barbell'
            st.rerun()
    
    # Footer text
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: #666; font-size: 0.9rem;'>"
        "Tap a tool. No data is stored."
        "</p>", 
        unsafe_allow_html=True
    )

def apply_rounding(value, direction, increment):
    """Apply rounding based on direction and increment."""
    if direction == "Down":
        return (int(value / increment)) * increment
    elif direction == "Up":
        return (int(value / increment) + (1 if value % increment > 0 else 0)) * increment
    else:  # Nearest
        return round(value / increment) * increment

def calculate_barbell_setup(target_weight, bar_weight, unit="lb"):
    """Calculate plate setup for a barbell."""
    plates_available = [45, 35, 25, 10, 5, 2.5]  # Available plate weights
    
    if target_weight <= bar_weight:
        return [], 0, "Target weight is less than or equal to bar weight"
    
    plate_weight_needed = target_weight - bar_weight
    per_side_weight = plate_weight_needed / 2
    
    plates_used = []
    remaining_weight = per_side_weight
    
    for plate in plates_available:
        if remaining_weight >= plate:
            count = int(remaining_weight / plate)
            if count > 0:
                plates_used.append((plate, count))
                remaining_weight -= plate * count
    
    achieved_per_side = sum(plate * count for plate, count in plates_used)
    achieved_total = bar_weight + (achieved_per_side * 2)
    
    if remaining_weight > 0.1:  # Small tolerance for floating point
        status = f"Closest achievable: {achieved_total:.1f} {unit}"
    else:
        status = "Exact match"
    
    return plates_used, achieved_total, status

def format_barbell_pairs(plates_used):
    """Format plate pairs for vertical display."""
    if not plates_used:
        return "No plates needed"
    
    pairs_list = []
    for plate, count in plates_used:
        pairs = count * 2  # Convert per-side to total pairs
        plate_str = f"{int(plate)}'s" if plate == int(plate) else f"{plate}'s"
        pairs_list.append(f"{plate_str} x {pairs}")
    
    return "\n".join(pairs_list)

def show_percent_calculator():
    """Display the percent calculator page."""
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
    
    # Initialize session state for barbell setup visibility
    if 'show_barbell' not in st.session_state:
        st.session_state.show_barbell = {}
    
    # Generate percentage table with barbell setup buttons
    st.markdown("#### Full Percentage Table")
    if base_weight > 0:
        # Get advanced options from session state or use defaults
        rounding_direction = st.session_state.get('rounding_direction', 'Down')
        smallest_increment = st.session_state.get('smallest_increment', 5.0)
        
        percentages = list(range(0, 105, 5))  # 0% to 100% in 5% increments
        
        for pct in percentages:
            exact_value = base_weight * (pct / 100)
            rounded_value = apply_rounding(exact_value, rounding_direction, smallest_increment)
            
            # Create columns for each row
            row_col1, row_col2, row_col3, row_col4 = st.columns([1, 2, 2, 2])
            
            with row_col1:
                st.write(f"**{pct}%**")
            
            with row_col2:
                st.write(f"{exact_value:.2f} {unit}")
            
            with row_col3:
                st.write(f"{rounded_value:.1f} {unit}")
            
            with row_col4:
                button_key = f"barbell_{pct}"
                if st.button("Show Barbell Setup", key=button_key):
                    if button_key in st.session_state.show_barbell:
                        del st.session_state.show_barbell[button_key]
                    else:
                        st.session_state.show_barbell[button_key] = True
            
            # Show barbell setup if button was clicked
            if st.session_state.show_barbell.get(button_key, False):
                setup_col1, setup_col2 = st.columns([1, 1])
                
                with setup_col1:
                    st.markdown("**Male (45 lb bar):**")
                    male_plates, male_total, male_status = calculate_barbell_setup(rounded_value, 45, unit)
                    if male_plates:
                        male_pairs = format_barbell_pairs(male_plates)
                        st.code(male_pairs)
                        st.write(f"Total: {male_total:.1f} {unit}")
                    else:
                        st.write(male_status)
                
                with setup_col2:
                    st.markdown("**Female (35 lb bar):**")
                    female_plates, female_total, female_status = calculate_barbell_setup(rounded_value, 35, unit)
                    if female_plates:
                        female_pairs = format_barbell_pairs(female_plates)
                        st.code(female_pairs)
                        st.write(f"Total: {female_total:.1f} {unit}")
                    else:
                        st.write(female_status)
                
                st.markdown("---")
        
        # Copy table functionality
        data = []
        for pct in percentages:
            weight = base_weight * (pct / 100)
            rounded_weight = apply_rounding(weight, rounding_direction, smallest_increment)
            data.append({
                "Percent": f"{pct}%",
                "Exact": f"{weight:.2f} {unit}",
                "Rounded": f"{rounded_weight:.1f} {unit}"
            })
        
        df = pd.DataFrame(data)
        csv_data = df.to_csv(index=False)
        
        if st.button("Copy Table", use_container_width=True):
            st.code(csv_data, language=None)
            st.success("Table data shown above - copy manually")
    
    else:
        st.info("Enter a base weight to see percentage calculations")
    
    # Advanced options moved to bottom
    st.markdown("---")
    st.markdown("#### Advanced Options")
    adv_col1, adv_col2 = st.columns([1, 1])
    
    with adv_col1:
        rounding_direction = st.selectbox(
            "Rounding Direction",
            ["Down", "Up", "Nearest"],
            index=0,
            help="How to round the calculated weight",
            key="rounding_direction_select"
        )
        st.session_state.rounding_direction = rounding_direction
    
    with adv_col2:
        smallest_increment = st.selectbox(
            "Smallest Increment",
            [1.0, 2.5, 5.0, 10.0],
            index=2,  # Default to 5.0
            help="Round to nearest increment",
            key="smallest_increment_select"
        )
        st.session_state.smallest_increment = smallest_increment

def show_barbell_calculator():
    """Display the tap-to-build barbell calculator page."""
    display_logo_and_title()
    
    # Back button
    if st.button("← Back to Tools", use_container_width=True):
        st.session_state.page = 'home'
        st.rerun()
    
    st.markdown("## Barbell Calculator")
    
    # Initialize session state for tap-to-build
    if 'bar_weight' not in st.session_state:
        st.session_state.bar_weight = 45
    if 'pair_counts' not in st.session_state:
        st.session_state.pair_counts = {weight: 0 for weight in PLATE_WEIGHTS}
    
    # Bar selection buttons
    st.markdown("### Bar Selection")
    bar_col1, bar_col2 = st.columns([1, 1])
    
    with bar_col1:
        if st.button("45 lb Bar", 
                    use_container_width=True,
                    type="primary" if st.session_state.bar_weight == 45 else "secondary"):
            st.session_state.bar_weight = 45
            st.rerun()
    
    with bar_col2:
        if st.button("35 lb Bar", 
                    use_container_width=True,
                    type="primary" if st.session_state.bar_weight == 35 else "secondary"):
            st.session_state.bar_weight = 35
            st.rerun()
    
    # Calculate totals
    total_weight = calculate_total_weight(st.session_state.bar_weight, st.session_state.pair_counts)
    per_side_weight = calculate_per_side_weight(st.session_state.pair_counts)
    
    # Weight display chips
    st.markdown("### Weight Summary")
    chip_col1, chip_col2 = st.columns([1, 1])
    
    with chip_col1:
        st.metric("Total", f"{total_weight:.1f} lb")
    
    with chip_col2:
        st.metric("Per Side", f"{per_side_weight:.1f} lb")
    
    # Barbell visualization
    st.markdown("### Barbell Visualization")
    barbell_html = generate_barbell_visualization(st.session_state.bar_weight, st.session_state.pair_counts)
    st.markdown(barbell_html, unsafe_allow_html=True)
    
    # Plate buttons grid
    st.markdown("### Add Plates")
    
    # Create grid of plate buttons (4 columns for mobile-friendly layout)
    plate_cols = st.columns([1, 1, 1, 1])
    
    for i, weight in enumerate(PLATE_WEIGHTS):
        col_idx = i % 4
        with plate_cols[col_idx]:
            color = PLATE_COLORS[weight]
            current_count = st.session_state.pair_counts[weight]
            
            # Plate button with color
            weight_str = f"{int(weight)}" if weight == int(weight) else f"{weight}"
            
            # Add plate button
            if st.button(f"+ {weight_str} lb", 
                        key=f"add_{weight}",
                        use_container_width=True):
                st.session_state.pair_counts[weight] += 1
                st.rerun()
            
            # Current count and remove button
            if current_count > 0:
                st.write(f"Pairs: {current_count}")
                if st.button(f"- {weight_str}", 
                            key=f"remove_{weight}",
                            use_container_width=True):
                    st.session_state.pair_counts[weight] = max(0, current_count - 1)
                    st.rerun()
            else:
                st.write("Pairs: 0")
    
    # Per-side breakdown
    breakdown_col1, breakdown_col2 = st.columns([1, 1])
    
    with breakdown_col1:
        st.markdown("### Per Side")
        breakdown_text = format_per_side_breakdown(st.session_state.pair_counts)
        st.code(breakdown_text)
    
    with breakdown_col2:
        # Clear bar button
        st.markdown("### Actions")
        if st.button("Clear Bar", use_container_width=True, type="secondary"):
            st.session_state.pair_counts = {weight: 0 for weight in PLATE_WEIGHTS}
            st.rerun()

# Navigation logic
if st.session_state.page == 'percent':
    show_percent_calculator()
elif st.session_state.page == 'barbell':
    show_barbell_calculator()
else:
    show_home_page()
