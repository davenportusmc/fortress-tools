"""Plate utilities for tap-to-build barbell calculator."""

from typing import Dict, List, Tuple

# Available plate weights in pounds (heaviest to lightest)
PLATE_WEIGHTS = [45, 35, 25, 15, 10, 5, 2.5, 1]

# Plate thickness in pixels for visualization
PLATE_THICKNESS = {
    45: 40,
    35: 36, 
    25: 32,
    15: 26,
    10: 22,
    5: 18,
    2.5: 14,
    1: 10
}

# Plate colors for visualization and buttons (Fortress theme)
PLATE_COLORS = {
    45: "#2563EB",    # Primary blue
    35: "#1D4ED8",    # Primary dark blue
    25: "#60A5FA",    # Primary light blue
    15: "#FACC15",    # Accent yellow
    10: "#F97316",    # Orange
    5: "#0F172A",     # Text dark
    2.5: "#475569",   # Muted
    1: "#C0C0C0"      # Silver
}

def calculate_total_weight(bar_weight: float, pair_counts: Dict[float, int]) -> float:
    """Calculate total barbell weight."""
    plate_weight = sum(weight * count * 2 for weight, count in pair_counts.items())
    return bar_weight + plate_weight

def calculate_per_side_weight(pair_counts: Dict[float, int]) -> float:
    """Calculate weight per side."""
    return sum(weight * count for weight, count in pair_counts.items())

def get_per_side_breakdown(pair_counts: Dict[float, int]) -> List[Tuple[float, int]]:
    """Get per-side breakdown sorted by weight (heaviest first)."""
    breakdown = []
    for weight in PLATE_WEIGHTS:  # Already sorted heaviest to lightest
        count = pair_counts.get(weight, 0)
        if count > 0:
            breakdown.append((weight, count))
    return breakdown

def format_per_side_breakdown(pair_counts: Dict[float, int]) -> str:
    """Format per-side breakdown as vertical text."""
    breakdown = get_per_side_breakdown(pair_counts)
    if not breakdown:
        return "No plates added."
    
    lines = []
    for weight, count in breakdown:
        weight_str = f"{int(weight)}" if weight == int(weight) else f"{weight}"
        lines.append(f"{weight_str} x {count}")
    
    return "\n".join(lines)

def generate_barbell_visualization(bar_weight: float, pair_counts: Dict[float, int]) -> str:
    """Generate HTML for barbell visualization."""
    # Get plates sorted by weight for proper ordering (heaviest innermost)
    plates_per_side = get_per_side_breakdown(pair_counts)
    
    # Build left side plates (lightest to heaviest for proper visual stacking)
    left_plates = []
    for weight, count in plates_per_side:
        color = PLATE_COLORS[weight]
        thickness = PLATE_THICKNESS[weight]
        for _ in range(count):
            left_plates.append(f'<div style="display: inline-block; width: {thickness}px; height: 80px; background-color: {color}; border: 2px solid #333; margin: 1px; vertical-align: middle;"></div>')
    
    # Reverse left plates so heaviest appears closest to bar
    left_plates_html = ''.join(reversed(left_plates))
    
    # Bar (sleeve and shaft)
    bar_html = '<div style="display: inline-block; width: 200px; height: 20px; background-color: #444; margin: 30px 10px; vertical-align: middle; border-radius: 10px;"></div>'
    
    # Build right side plates (heaviest to lightest for proper visual stacking)
    right_plates = []
    for weight, count in plates_per_side:
        color = PLATE_COLORS[weight]
        thickness = PLATE_THICKNESS[weight]
        for _ in range(count):
            right_plates.append(f'<div style="display: inline-block; width: {thickness}px; height: 80px; background-color: {color}; border: 2px solid #333; margin: 1px; vertical-align: middle;"></div>')
    
    right_plates_html = ''.join(right_plates)
    
    # Complete barbell visualization with theme classes
    barbell_html = f'''
    <div class="barbell-container" style="text-align: center; overflow-x: auto; white-space: nowrap;">
        {left_plates_html}{bar_html}{right_plates_html}
    </div>
    '''
    
    return barbell_html
