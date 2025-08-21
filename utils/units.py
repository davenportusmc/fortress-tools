"""Unit conversion and rounding utilities."""

from typing import Union


def lb_to_kg(weight_lb: float) -> float:
    """Convert pounds to kilograms."""
    return weight_lb * 0.453592


def kg_to_lb(weight_kg: float) -> float:
    """Convert kilograms to pounds."""
    return weight_kg / 0.453592


def convert_weight(weight: float, from_unit: str, to_unit: str) -> float:
    """Convert weight between units."""
    if from_unit == to_unit:
        return weight
    
    if from_unit == "lb" and to_unit == "kg":
        return lb_to_kg(weight)
    elif from_unit == "kg" and to_unit == "lb":
        return kg_to_lb(weight)
    else:
        raise ValueError(f"Unsupported conversion: {from_unit} to {to_unit}")


def round_weight(weight: float, rounding: str, unit: str = "lb") -> float:
    """Round weight according to specified rounding rule."""
    if rounding == "None":
        return weight
    elif rounding == "Nearest 0.5":
        return round(weight * 2) / 2
    elif rounding == "Nearest 1.0":
        return round(weight)
    else:
        return weight


def format_weight(weight: float, unit: str) -> str:
    """Format weight for display."""
    if weight == int(weight):
        return f"{int(weight)} {unit}"
    else:
        return f"{weight:.1f} {unit}"


def get_default_bar_weight(unit: str) -> float:
    """Get default barbell weight for unit."""
    return 45.0 if unit == "lb" else 20.0


def get_default_plates(unit: str) -> dict:
    """Get default plate set for unit."""
    if unit == "lb":
        return {
            45: 2, 35: 2, 25: 2, 15: 2, 10: 2, 5: 2, 2.5: 2
        }
    else:  # kg
        return {
            25: 2, 20: 2, 15: 2, 10: 2, 5: 2, 2.5: 2, 1.25: 2
        }
