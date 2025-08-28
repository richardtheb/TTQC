#!/bin/bash
# Raspberry Pi setup script for TTQC_flowing.py

echo "Setting up TTQC_flowing.py for Raspberry Pi..."

# Update package list
echo "Updating package list..."
sudo apt-get update

# Install Python dependencies
echo "Installing Python dependencies..."
sudo apt-get install -y python3-pip python3-pil python3-pil.imagetk

# Install fonts
echo "Installing fonts..."
sudo apt-get install -y fonts-liberation fonts-dejavu-core fonts-dejavu-extra

# Install Python packages
echo "Installing Python packages..."
pip3 install -r requirements.txt

# Install Inky display dependencies
echo "Installing Inky display dependencies..."
sudo apt-get install -y python3-gpiozero python3-spidev

# Create a test script to verify fonts
echo "Creating font test script..."
cat > test_fonts_pi.py << 'EOF'
#!/usr/bin/env python3
"""
Test script to verify fonts on Raspberry Pi
"""

from PIL import Image, ImageDraw, ImageFont

def test_raspberry_pi_fonts():
    # Create a test image
    img = Image.new('RGB', (800, 600), "#ffffff")
    draw = ImageDraw.Draw(img)
    
    # Test Raspberry Pi font paths
    font_paths = [
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    ]
    
    y_position = 50
    
    for i, font_path in enumerate(font_paths):
        try:
            # Try to load font
            font = ImageFont.truetype(font_path, 24)
            print(f"✓ Successfully loaded: {font_path}")
            
            # Test text rendering
            text = f"Test {i+1} - Font: {font_path.split('/')[-1]}"
            draw.text((50, y_position), text, font=font, fill="black")
            y_position += 40
                
        except Exception as e:
            print(f"✗ Failed to load {font_path}: {e}")
            y_position += 40
    
    # Test default font
    try:
        default_font = ImageFont.load_default()
        draw.text((50, y_position), "Default font test", font=default_font, fill="black")
        print("✓ Default font loaded")
    except Exception as e:
        print(f"✗ Default font failed: {e}")
    
    # Save test image
    img.save("raspberry_pi_font_test.png")
    print("Test image saved as raspberry_pi_font_test.png")

if __name__ == "__main__":
    test_raspberry_pi_fonts()
EOF

# Make the test script executable
chmod +x test_fonts_pi.py

echo "Setup complete!"
echo "To test the fonts, run: python3 test_fonts_pi.py"
echo "To run TTQC_flowing.py, use: python3 TTQC_flowing.py"
