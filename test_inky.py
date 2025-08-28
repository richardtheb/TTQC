#!/usr/bin/env python3
"""
Test script to verify Inky Impressions display functionality
"""

from PIL import Image, ImageDraw, ImageFont

def test_inky_display():
    print("Testing Inky Impressions display functionality...")
    
    # Check if Inky library is available
    try:
        from inky.auto import auto
        print("✓ Inky library is available")
        
        # Try to initialize display
        try:
            inky_display = auto()
            print(f"✓ Inky display initialized: {inky_display.resolution}")
            
            # Create a test image
            display_width, display_height = inky_display.resolution
            img = Image.new('RGB', (display_width, display_height), "#ffffff")
            draw = ImageDraw.Draw(img)
            
            # Add some test text
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf", 24)
            except:
                font = ImageFont.load_default()
            
            draw.text((50, 50), "Inky Display Test", font=font, fill="black")
            draw.text((50, 100), "TTQC Quote Generator", font=font, fill="black")
            draw.text((50, 150), "Time-based quotes", font=font, fill="black")
            
            # Convert to Inky format
            inky_img = img.convert('L')  # Grayscale
            inky_img = inky_img.point(lambda x: 0 if x < 128 else 255, '1')  # Threshold
            inky_img = inky_img.convert('1')  # Binary
            
            # Display on Inky
            inky_display.set_image(inky_img)
            inky_display.show()
            
            print("✓ Test image displayed on Inky display")
            print("✓ Inky display functionality is working!")
            
        except Exception as e:
            print(f"✗ Failed to initialize Inky display: {e}")
            print("This is normal if no Inky display is connected")
            
    except ImportError:
        print("✗ Inky library not available")
        print("Install with: pip install inky")

if __name__ == "__main__":
    test_inky_display()
