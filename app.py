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
    st.markdown("""
    <div style="max-width: 768px; margin: 0 auto; padding: 2rem 1rem;">
        <!-- Back link -->
        <div style="margin-bottom: 1rem;">
            <a href="#" onclick="window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'home'}, '*')" class="back-link">
                <svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                    <path d="M12.293 16.293a1 1 0 010 1.414l-6-6a1 1 0 010-1.414l6-6a1 1 0 111.414 1.414L8.414 10l5.293 5.293a1 1 0 01-1.414 1.414z"/>
                </svg>
                Back to Tools
            </a>
        </div>

        <!-- Title -->
        <h1 style="font-size: 1.5rem; font-weight: 600; margin-bottom: 0.25rem;">Percent Calculator</h1>
        <p style="font-size: 0.875rem; color: var(--muted); margin-bottom: 1.5rem;">Compute plate percentages quickly.</p>

        <!-- Form -->
        <div class="percent-form" style="margin-bottom: 2rem;">
            <div>
                <label style="display: block; font-size: 0.875rem; font-weight: 500; margin-bottom: 0.25rem;">Base weight</label>
                <div class="input-group" id="baseWeightGroup">
                    <button type="button" id="dec" aria-label="decrease">−</button>
                    <input id="baseWeight" type="number" step="0.5" value="100" style="text-align: center;">
                    <button type="button" id="inc" aria-label="increase">+</button>
                </div>
            </div>

            <div>
                <label style="display: block; font-size: 0.875rem; font-weight: 500; margin-bottom: 0.25rem;">Unit</label>
                <select id="unit" style="width: 100%; padding: 8px 12px; border: 1px solid var(--border); border-radius: 12px; background: white;">
                    <option value="lb">lb</option>
                    <option value="kg">kg</option>
                </select>
            </div>

            <div>
                <label style="display: block; font-size: 0.875rem; font-weight: 500; margin-bottom: 0.25rem;">Rounding</label>
                <select id="rounding" style="width: 100%; padding: 8px 12px; border: 1px solid var(--border); border-radius: 12px; background: white;">
                    <option value="none">None</option>
                    <option value="2.5">2.5</option>
                    <option value="5">5</option>
                </select>
            </div>
        </div>

        <!-- Results -->
        <section>
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.5rem;">
                <h2 style="font-size: 1.125rem; font-weight: 600;">Results</h2>
                <button id="copyBtn" type="button" class="btn-ghost">Copy table</button>
            </div>

            <div style="overflow-x: auto; border-radius: 12px; border: 1px solid var(--border);">
                <table id="resultsTable" class="results-table">
                    <thead>
                        <tr>
                            <th>Percent</th>
                            <th style="text-align: right;">Weight</th>
                        </tr>
                    </thead>
                    <tbody>
                        <!-- Rows injected by JS -->
                    </tbody>
                </table>
            </div>
        </section>
    </div>

    <script>
    (function () {
        const w = document.getElementById('baseWeight');
        const unit = document.getElementById('unit');
        const rounding = document.getElementById('rounding');
        const inc = document.getElementById('inc');
        const dec = document.getElementById('dec');
        const body = document.querySelector('#resultsTable tbody');
        const copyBtn = document.getElementById('copyBtn');

        function roundTo(val, step) {
            if (!step || step === 'none') return val;
            const s = parseFloat(step);
            return Math.round(val / s) * s;
        }

        function fmt(val) {
            return `${val} ${unit.value}`;
        }

        function render() {
            const base = parseFloat(w.value || '0');
            const steps = Array.from({length: 21}, (_, i) => i * 5); // 0..100 by 5s
            body.innerHTML = steps.map(p => {
                const raw = (base * p) / 100;
                const r = roundTo(raw, rounding.value);
                const v = Number.isFinite(r) ? r.toFixed(1) : '0.0';
                return `<tr>
                          <td>${p}%</td>
                          <td style="text-align: right;">${v} ${unit.value}</td>
                        </tr>`;
            }).join('');
        }

        inc?.addEventListener('click', () => { w.stepUp(); render(); });
        dec?.addEventListener('click', () => { w.stepDown(); render(); });
        [w, unit, rounding].forEach(el => el?.addEventListener('input', render));
        render();

        copyBtn?.addEventListener('click', () => {
            const rows = [['Percent','Weight']].concat(
                [...body.querySelectorAll('tr')].map(tr => {
                    const tds = tr.querySelectorAll('td');
                    return [tds[0].textContent.trim(), tds[1].textContent.trim()];
                })
            );
            const tsv = rows.map(r => r.join('\\t')).join('\\n');
            navigator.clipboard.writeText(tsv);
            copyBtn.textContent = 'Copied!';
            setTimeout(() => copyBtn.textContent = 'Copy table', 1200);
        });
    })();
    </script>
    """, unsafe_allow_html=True)
    
    # Back button functionality
    if st.button("← Back to Tools", key="back_btn", help="Return to main tools"):
        st.session_state.page = 'home'
        st.rerun()

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
    
    # Barbell visualization with weight display above it
    barbell_html = generate_barbell_visualization(st.session_state.bar_weight, st.session_state.pair_counts)
    
    # Combine weight display and barbell visualization
    combined_html = f'''
    <div style="text-align: center; margin: 1rem 0;">
        <div class="weight-display" style="margin-bottom: 0.5rem;">{total_weight:.0f} lbs</div>
        {barbell_html}
    </div>
    '''
    st.markdown(combined_html, unsafe_allow_html=True)
    
    # Plate buttons grid
    st.markdown("### Add Weights")
    
    # Create grid of plate buttons (4 columns for mobile-friendly layout)
    plate_cols = st.columns([1, 1, 1, 1])
    
    for i, weight in enumerate(PLATE_WEIGHTS):
        col_idx = i % 4
        with plate_cols[col_idx]:
            color = PLATE_COLORS[weight]
            current_count = st.session_state.pair_counts[weight]
            
            # Plate button with color
            weight_str = f"{int(weight)}" if weight == int(weight) else f"{weight}"
            
            if st.button(f"{weight_str} lb", 
                        use_container_width=True,
                        key=f"plate_{weight}"):
                st.session_state.pair_counts[weight] += 1
                st.rerun()
            
            # Show current count only
            if current_count > 0:
                st.write(f"Pairs: {current_count}")
            else:
                st.write("Pairs: 0")
    
    # Clear bar button
    if st.button("Clear Bar", use_container_width=True, type="secondary"):
        # Reset all plate counts but keep bar selection
        for weight in PLATE_WEIGHTS:
            st.session_state.pair_counts[weight] = 0
        st.rerun()

# Navigation logic
if st.session_state.page == 'percent':
    show_percent_calculator()
elif st.session_state.page == 'barbell':
    show_barbell_calculator()
else:
    show_home_page()
