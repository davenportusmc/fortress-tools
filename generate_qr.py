"""QR Code Generator for Fortress Athlete Tools"""

import argparse
import qrcode
from qrcode.image.pil import PilImage


def generate_qr_code(url: str, output_file: str = "fortress_tools_qr.png"):
    """Generate QR code for the given URL."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create image
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_file)
    
    print(f"QR code saved to {output_file}")
    print(f"URL: {url}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate QR code for Fortress Athlete Tools")
    parser.add_argument(
        "--url", 
        default="https://fortressathlete-tools.example.com/",
        help="URL to encode in QR code"
    )
    parser.add_argument(
        "--output",
        default="fortress_tools_qr.png", 
        help="Output filename for QR code"
    )
    
    args = parser.parse_args()
    generate_qr_code(args.url, args.output)
