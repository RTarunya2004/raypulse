"""
Generate Payment QR Code
Run this script to create the payment QR code image for subscriptions
"""

import qrcode
from PIL import Image, ImageDraw
import os

# Your payment information (update with actual details)
PAYMENT_UPI_ID = "yourupiid@bank"  # Replace with your actual UPI ID
MERCHANT_NAME = "RayPulse"

def generate_payment_qr():
    """Generate payment QR code"""

    # Create UPI payment link (standard UPI format)
    # Format: upi://pay?pa=UPI_ID&pn=NAME&cu=INR
    upi_link = f"upi://pay?pa={PAYMENT_UPI_ID}&pn={MERCHANT_NAME}&cu=USD"

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(upi_link)
    qr.make(fit=True)

    # Create image
    img = qr.make_image(fill_color="black", back_color="white")

    # Add Google Pay logo in center (optional)
    # You can add a logo overlay here if needed

    # Save
    output_path = os.path.join('static', 'images', 'payment-qr.png')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path)

    print(f"✓ Payment QR code generated: {output_path}")
    print(f"  UPI ID: {PAYMENT_UPI_ID}")
    print(f"  Merchant: {MERCHANT_NAME}")
    print("\nIMPORTANT:")
    print("1. Update PAYMENT_UPI_ID in this script with your actual UPI ID")
    print("2. Re-run the script to regenerate QR code")
    print("3. Test scanning the QR code with a payment app")

if __name__ == '__main__':
    generate_payment_qr()
