# Fortress Athlete Tools

A lightweight, mobile-first CrossFit gym app designed for quick access via QR code. Built with Python and Streamlit for fast, simple calculations without data storage.

## Key Design Choices

- **Mobile-First**: Optimized for phone screens with large touch targets
- **No Database**: All calculations are client-side, no data persistence
- **Minimal Dependencies**: Only essential packages for fast loading
- **QR Code Access**: Designed to be accessed by scanning a gym QR code
- **Fortress Athlete Branding**: Uses official logo and clean color scheme

## Features

### Percent Calculator
- Calculate percentage-based weights from a base weight
- Support for lb/kg units with conversion
- Advanced rounding options: Down, Up, Nearest with custom increments (1.0, 2.5, 5.0, 10.0)
- Full percentage table (0-100% in 5% increments) with exact and rounded values
- Individual barbell setup buttons for each percentage row
- Vertical plate pairs display format (e.g., "45's x 4, 25's x 2")
- Copy table functionality

### Barbell Calculator (Tap-to-Build)
- Interactive tap-to-build interface for real-time barbell construction
- Bar selection: 45 lb (male) or 35 lb (female) bars
- Unlimited plate pairs: 45, 35, 25, 15, 10, 5, 2.5, 1 lb
- Visual barbell representation with realistic plate thickness and colors
- Per-side breakdown showing plate counts (heaviest first)
- Clear bar function to reset all plates
- Real-time weight calculations and display

## Setup

Install dependencies:
```bash
pip install streamlit pandas qrcode[pil]
```

## Running the App

Start the Streamlit server:
```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`

## Customization

### Theming
Change colors in `.streamlit/config.toml`:
- `primaryColor`: Main accent color
- `backgroundColor`: Page background
- `secondaryBackgroundColor`: Sidebar/secondary areas
- `textColor`: Main text color

### Logo
- Replace `assets/fortress-logo.png` with your gym's logo, or
- Set `FORTRESS_LOGO_URL` environment variable to use an external URL

### QR Code Generation
Generate a QR code for your deployed app:
```bash
python generate_qr.py --url "https://YOUR-DEPLOYED-URL"
```

## Testing

Run unit tests:
```bash
python -m pytest tests/
```

Or run specific test file:
```bash
python tests/test_packing.py
```

## Project Structure

```
fortress-tools/
├── app.py                    # Main router and landing page
├── pages/
│   ├── 1_Percent_Calculator.py
│   └── 2_Barbell_Calculator.py
├── utils/
│   ├── branding.py          # Logo, styling, mobile CSS
│   ├── units.py             # Unit conversion and rounding
│   └── plates.py            # Plate packing algorithm
├── assets/
│   └── fortress-logo.png    # Gym logo (placeholder)
├── .streamlit/
│   └── config.toml          # Theme configuration
├── generate_qr.py           # QR code generator script
├── tests/
│   └── test_packing.py      # Unit tests for plate algorithm
└── README.md
```

## Mobile Compatibility

Tested on common mobile resolutions:
- iPhone (375x667, 414x896)
- Android (360x640, 412x915)

## Performance Notes

- No external API calls during normal operation
- Minimal JavaScript (Streamlit built-in only)
- System fonts only (no web font downloads)
- Optimized for fast loading on mobile networks

## Algorithm Details

### Tap-to-Build Barbell Calculator
The new barbell calculator uses an interactive approach:
1. **Real-time Building**: Tap plate buttons to add pairs (one per side)
2. **Visual Feedback**: Plates render with realistic thickness and colors
3. **Proper Ordering**: Heaviest plates closest to bar center, lightest on outside
4. **Unlimited Inventory**: No plate availability constraints
5. **Instant Calculations**: Total and per-side weights update immediately

### Plate Visualization
- **Realistic Thickness**: 45lb=40px, 35lb=36px, 25lb=32px, etc.
- **Color Coding**: Red=45lb, Blue=35lb, Green=25lb, Yellow=15lb, Orange=10lb, Black=5lb, Gray=2.5lb, Silver=1lb
- **Proper Placement**: Plates automatically sort by weight for correct visual ordering

### Percentage Calculations
- Advanced rounding: Down, Up, or Nearest to custom increments
- Individual barbell setups for each percentage row
- Supports both exact and rounded value displays

## Customization

### Plate Colors and Thickness
Edit `utils/plates.py` to customize plate appearance:

```python
# Modify plate colors
PLATE_COLORS = {
    45: "#FF0000",    # Red
    35: "#0000FF",    # Blue
    # ... add your preferred colors
}

# Adjust plate thickness (in pixels)
PLATE_THICKNESS = {
    45: 40,    # Thickest
    35: 36,
    # ... customize thickness
}
```
