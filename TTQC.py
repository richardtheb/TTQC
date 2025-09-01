#!/usr/bin/env python3
"""
Time-based TSV Quote Generator with Flowing Text

This script:
1. Gets the current time in HH:MM format (local or NTP)
2. Searches for that time in column 1 of TTQC_quotes.tsv
3. Creates an image using data from columns 2, 3, 4, 5, and 6
4. Uses flowing text with mixed formatting and customizable styling
5. Supports Inky Impressions e-paper display output
"""

from contextlib import redirect_stdout
import csv
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import argparse
import json

# Add NTP support
try:
    import ntplib
    NTP_AVAILABLE = True
except ImportError:
    NTP_AVAILABLE = False
    print("Warning: ntplib not available. Install with: pip install ntplib")

# Add Inky Impressions display support
try:
    from inky.auto import auto
    INKY_AVAILABLE = True
    print("inky detected!")
except ImportError:
    INKY_AVAILABLE = False
    print("Warning: Inky library not available. Install with: pip install inky")

# Add pygame support for fullscreen display
try:
    import pygame
    PYGAME_AVAILABLE = True
    print("pygame detected!")
except ImportError:
    PYGAME_AVAILABLE = False
    print("Warning: pygame not available. Install with: pip install pygame")


class TimeImageGenerator:
    def __init__(self, output_file="time_image.png", use_ntp=False, ntp_server=None, use_inky=False, use_fullscreen=False):
        self.tsv_file = "TTQC_quotes.tsv"
        self.config_file = "config.json"
        self.output_file = output_file
        self.use_ntp = use_ntp
        self.ntp_server = ntp_server
        self.use_inky = use_inky
        self.use_fullscreen = use_fullscreen
        self.fonts_cache = {}
        
        # Initialize pygame for fullscreen display if requested and available
        self.pygame_screen = None
        if self.use_fullscreen and PYGAME_AVAILABLE:
            try:
                pygame.init()
                info = pygame.display.Info()
                screen_width = info.current_w
                screen_height = info.current_h
                self.pygame_screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
                pygame.display.set_caption("TTQC Time Display")
                pygame.mouse.set_visible(False)
                print(f"Initialized pygame fullscreen display: {screen_width}x{screen_height}")
            except Exception as e:
                print(f"Failed to initialize pygame display: {e}")
                self.pygame_screen = None
        
        # Initialize Inky display if requested and available
        self.inky_display = None
        if INKY_AVAILABLE:
            try:
                self.inky_display = auto()
                print(f"Initialized Inky display: {self.inky_display.resolution}")
            except Exception as e:
                print(f"Failed to initialize Inky display: {e}")
                self.inky_display = None

        # Always load config.json
        self.load_config()

    def load_config(self):
        """Load configuration from config.json"""
        # Default configuration
        default_config = {
            "image_size": [640, 400],
            "background_color": [255, 255, 255],  # White
            "quote_text": {
                "font_family": "Lora",
                "font_size": 38,
                "line_spacing": 8,
                "max_width": 600
            },
            "quote_normal": {
                "color": [0, 0, 0]  # Black
            },
            "quote_highlight": {
                "font_family": "Lora",
                "font_size": 38,
                "font_weight": "extra-bold",
                "color": [255, 0, 0]  # Red
            },
            "attribution_section": {
                "font_family": "Open Sans",
                "font_size": 32,
                "font_weight": "italic",
                "line_spacing": 5,
                "color": [0, 128, 0]  # Green
            }
        }
        
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                # Merge with defaults to ensure all required keys exist
                self.config = self.merge_configs(default_config, config)
                print(f"Configuration loaded from {self.config_file}")
        except FileNotFoundError:
            print(f"Config file {self.config_file} not found. Using default configuration.")
            self.config = default_config
            self.generate_sample_config()
        except json.JSONDecodeError:
            print(f"Error parsing config file {self.config_file}. Using default configuration.")
            self.config = default_config

    def merge_configs(self, default_config, user_config):
        """Recursively merge user config with default config"""
        result = default_config.copy()
        for key, value in user_config.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self.merge_configs(result[key], value)
            else:
                result[key] = value
        return result

    def get_font(self, font_family, font_size, font_weight="regular"):
        """Get PIL font object using system fonts"""
        try:
            # Map Google Fonts to similar system fonts
            font_mapping = {
                "Lora": ["Times New Roman", "Times", "serif"],
                "Open Sans": ["Arial", "Helvetica", "sans-serif"],
                "Roboto": ["Arial", "Helvetica", "sans-serif"],
                "Lato": ["Arial", "Helvetica", "sans-serif"],
                "Montserrat": ["Arial", "Helvetica", "sans-serif"]
            }

            # Get potential system font names
            potential_fonts = font_mapping.get(font_family, [font_family])

            # Common system font paths by platform
            font_paths = []

            # Add specific font files based on weight
            is_bold = font_weight.lower() in ["bold", "semibold", "extrabold", "extra-bold", "black"]
            is_italic = font_weight.lower() == "italic"

            for font_name in potential_fonts:
                if font_name.lower() in ["times new roman", "times", "serif"]:
                    # Times/serif fonts - Raspberry Pi compatible paths
                    if is_bold and is_italic:
                        font_paths.extend([
                            "/usr/share/fonts/truetype/liberation/LiberationSerif-BoldItalic.ttf",
                            "/usr/share/fonts/truetype/dejavu/DejaVuSerif-BoldOblique.ttf",
                            "/usr/share/fonts/truetype/liberation/LiberationSerif-BoldItalic.ttf",
                            "timesbi.ttf", "Times Bold Italic.ttf"
                        ])
                    elif is_bold:
                        font_paths.extend([
                            "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
                            "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
                            "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
                            "timesbd.ttf", "Times Bold.ttf"
                        ])
                    elif is_italic:
                        font_paths.extend([
                            "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
                            "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Oblique.ttf",
                            "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
                            "timesi.ttf", "Times Italic.ttf"
                        ])
                    else:
                        font_paths.extend([
                            "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
                            "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
                            "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
                            "times.ttf", "Times.ttf", "Times New Roman.ttf"
                        ])

                elif font_name.lower() in ["arial", "helvetica", "sans-serif"]:
                    # Arial/sans-serif fonts - Raspberry Pi compatible paths
                    if is_bold and is_italic:
                        font_paths.extend([
                            "/usr/share/fonts/truetype/liberation/LiberationSans-BoldItalic.ttf",
                            "/usr/share/fonts/truetype/dejavu/DejaVuSans-BoldOblique.ttf",
                            "/usr/share/fonts/truetype/liberation/LiberationSans-BoldItalic.ttf",
                            "arialbi.ttf", "Arial Bold Italic.ttf"
                        ])
                    elif is_bold:
                        font_paths.extend([
                            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
                            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
                            "arialbd.ttf", "Arial Bold.ttf"
                        ])
                    elif is_italic:
                        font_paths.extend([
                            "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf",
                            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf",
                            "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf",
                            "ariali.ttf", "Arial Italic.ttf"
                        ])
                    else:
                        font_paths.extend([
                            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
                            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
                            "arial.ttf", "Arial.ttf"
                        ])

            # Try each font path
            for font_path in font_paths:
                try:
                    font = ImageFont.truetype(font_path, font_size)
                    print(f"Successfully loaded font: {font_path} at size {font_size}")
                    return font
                except (OSError, IOError):
                    continue

            # If no system fonts found, try using PIL's default font
            print(f"No system fonts found for {font_family} {font_weight}, using default font")
            try:
                # Try to load a larger default font
                default_font = ImageFont.load_default()
                return default_font
            except Exception as e:
                print(f"Error loading default font: {e}")
                # Last resort - create a basic font
                return ImageFont.load_default()

        except Exception as e:
            print(f"Error loading font {font_family}: {e}. Using default font.")
            return ImageFont.load_default()

    def get_current_time(self):
        """Get current time in HH:MM format"""
        if self.use_ntp and NTP_AVAILABLE:
            ntp_client = ntplib.NTPClient()
            
            # If a specific NTP server is provided, try it first
            if self.ntp_server:
                try:
                    print(f"Trying custom NTP server: {self.ntp_server}")
                    response = ntp_client.request(self.ntp_server, version=3, timeout=5)
                    current_time = datetime.fromtimestamp(response.tx_time).strftime("%H:%M")
                    print(f"Current time (NTP from {self.ntp_server}): {current_time}")
                    return current_time
                except Exception as e:
                    print(f"Failed to get time from custom server {self.ntp_server}: {e}")
                    print("Falling back to default NTP servers...")
            
            # Try multiple default NTP servers
            ntp_servers = [
                'time.google.com',
                'time.windows.com', 
                'time.apple.com',
                'pool.ntp.org',
                'time.nist.gov'
            ]
            
            for server in ntp_servers:
                try:
                    print(f"Trying NTP server: {server}")
                    response = ntp_client.request(server, version=3, timeout=5)
                    current_time = datetime.fromtimestamp(response.tx_time).strftime("%H:%M")
                    print(f"Current time (NTP from {server}): {current_time}")
                    return current_time
                except Exception as e:
                    print(f"Failed to get time from {server}: {e}")
                    continue
            
            print("All NTP servers failed. Falling back to local time.")
            current_time = datetime.now().strftime("%H:%M")
            print(f"Current time (local): {current_time}")
            return current_time
        else:
            if self.use_ntp and not NTP_AVAILABLE:
                print("NTP requested but ntplib is not available. Using local time.")
            current_time = datetime.now().strftime("%H:%M")
            print(f"Current time (local): {current_time}")
            return current_time

    def find_time_row(self, target_time):
        """Find row in TSV where time column matches the target time"""
        try:
            with open(self.tsv_file, 'r', newline='', encoding='utf-8') as file:
                # Use tab delimiter for TSV files
                tsv_reader = csv.reader(file, delimiter='\t')

                # Try both formats: with and without leading zero
                time_formats = [target_time]
                if target_time.startswith('0') and len(target_time) == 5:
                    # If time has leading zero (e.g., "08:58"), also try without it ("8:58")
                    time_formats.append(target_time[1:])
                elif len(target_time) == 4:
                    # If time doesn't have leading zero (e.g., "8:58"), also try with it ("08:58")
                    time_formats.append('0' + target_time)

                for row_num, row in enumerate(tsv_reader, 1):
                    if len(row) >= 6:  # Ensure we have at least 6 columns
                        row_time = row[0].strip()
                        if row_time in time_formats:
                            return {
                                'time': row_time,
                                'quote_part1': row[1].strip(),
                                'quote_part2': row[2].strip(),
                                'quote_part3': row[3].strip(),
                                'book_title': row[4].strip(),
                                'book_author': row[5].strip()
                            }

                print(f"Time {target_time} (tried formats: {time_formats}) not found in {self.tsv_file}.")
                return None

        except FileNotFoundError:
            print(f"TSV file {self.tsv_file} not found.")
            return None
        except Exception as e:
            print(f"Error reading TSV file: {e}")
            return None

    def wrap_text(self, text, font, max_width):
        """Wrap text to fit within max_width"""
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            bbox = font.getbbox(test_line)
            text_width = bbox[2] - bbox[0]

            if text_width <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                    current_line = word
                else:
                    lines.append(word)  # Word is too long but we have to include it

        if current_line:
            lines.append(current_line)

        return lines

    def create_flowing_text(self, data):
        """Create flowing text with mixed formatting"""
        if not data:
            return False

        # Create image
        img = Image.new('RGB', tuple(self.config["image_size"]), tuple(self.config["background_color"]))
        draw = ImageDraw.Draw(img)

        # Start position - center the text within the image
        image_width = self.config["image_size"][0]
        max_width = self.config["quote_text"]["max_width"]
        start_x = (image_width - max_width) // 2  # Center the text block
        start_y = 50
        current_y = start_y

        # Combine quote parts into flowing text
        quote_parts = [
            (data['quote_part1'], False),  # Normal text
            (data['quote_part2'], True),   # Highlighted text (italic)
            (data['quote_part3'], False)   # Normal text
        ]

        # Get fonts
        normal_font = self.get_font(
            self.config["quote_text"]["font_family"],
            self.config["quote_text"]["font_size"],
            "regular"
        )
        
        highlight_font = self.get_font(
            self.config["quote_highlight"]["font_family"],
            self.config["quote_highlight"]["font_size"],
            self.config["quote_highlight"]["font_weight"]
        )

        # Build the complete quote text with mixed formatting
        complete_text = ""
        formatting_info = []  # Track which parts are highlighted
        
        for i, (text, is_highlighted) in enumerate(quote_parts):
            if not text:
                continue
                
            # Add space between parts if needed
            if complete_text and not text.startswith(' '):
                complete_text += ' '
                
            start_pos = len(complete_text)
            complete_text += text
            end_pos = len(complete_text)
            
            formatting_info.append({
                'start': start_pos,
                'end': end_pos,
                'is_highlighted': is_highlighted,
                'text': text
            })

        # Wrap the complete text
        lines = self.wrap_text(complete_text, normal_font, max_width)

        # Draw each line with mixed formatting
        for line in lines:
            current_x = start_x
            line_drawn = False
            
            # Check if this line contains any highlighted text
            for format_info in formatting_info:
                if format_info['is_highlighted'] and format_info['text'] in line:
                    # This line contains highlighted text
                    highlight_start = line.find(format_info['text'])
                    
                    # Draw text before highlight
                    if highlight_start > 0:
                        before_text = line[:highlight_start]
                        draw.text((current_x, current_y), before_text, 
                                 font=normal_font, fill=tuple(self.config["quote_normal"]["color"]))
                        current_x += normal_font.getbbox(before_text)[2] - normal_font.getbbox(before_text)[0]
                    
                    # Draw highlighted text
                    draw.text((current_x, current_y), format_info['text'], 
                             font=highlight_font, fill=tuple(self.config["quote_highlight"]["color"]))
                    current_x += highlight_font.getbbox(format_info['text'])[2] - highlight_font.getbbox(format_info['text'])[0]
                    
                    # Draw text after highlight
                    after_text = line[highlight_start + len(format_info['text']):]
                    if after_text:
                        draw.text((current_x, current_y), after_text, 
                                 font=normal_font, fill=tuple(self.config["quote_normal"]["color"]))
                    
                    line_drawn = True
                    break  # Only handle the first highlight in the line
            
            # If no highlight was found, draw the entire line normally
            if not line_drawn:
                draw.text((current_x, current_y), line, 
                         font=normal_font, fill=tuple(self.config["quote_normal"]["color"]))
            
            current_y += self.config["quote_text"]["font_size"] + self.config["quote_text"]["line_spacing"]

        # Calculate total height needed for quote text
        quote_height = current_y - start_y
        
        # Draw attribution section at the bottom
        attribution_parts = []
        if data['book_title']:
            attribution_parts.append(data['book_title'])
        if data['book_author']:
            attribution_parts.append(f"— {data['book_author']}")

        if attribution_parts:
            attribution_config = self.config["attribution_section"]
            attribution_font = self.get_font(
                attribution_config["font_family"],
                attribution_config["font_size"],
                attribution_config["font_weight"]
            )

            # Calculate attribution height
            attribution_height = len(attribution_parts) * (attribution_config["font_size"] + attribution_config["line_spacing"]) - attribution_config["line_spacing"]
            
            # Position attribution at the bottom with margin
            bottom_margin = 50
            attribution_y = self.config["image_size"][1] - bottom_margin - attribution_height
            
            for part in attribution_parts:
                draw.text((start_x, attribution_y), part, font=attribution_font, fill=tuple(attribution_config["color"]))
                attribution_y += attribution_config["font_size"] + attribution_config["line_spacing"]

        # Save image
        try:
            img.save(self.output_file)
            print(f"Image saved as {self.output_file}")
            
            # Display on Inky if available and requested
            if self.use_inky and self.inky_display:
                self.display_on_inky(img)
                print(f"Image sent to inky display")
            
            # Display on fullscreen if requested
            if self.use_fullscreen and self.pygame_screen:
                self.display_on_fullscreen(img)
                print(f"Image sent to fullscreen display")
            
            return True
        except Exception as e:
            print(f"Error saving image: {e}")
            return False

    def display_on_inky(self, img):
        """Display image on Inky Impressions display"""
        try:
            # Get display resolution for logging
            display_width, display_height = self.inky_display.resolution
            
            # Set and display the image
            self.inky_display.set_image(img)
            self.inky_display.show()
            
            print(f"Image displayed on Inky Impressions display ({display_width}x{display_height})")
            
        except Exception as e:
            print(f"Error displaying on Inky: {e}")

    def display_on_fullscreen(self, img):
        """Display image on fullscreen pygame display"""
        try:
            if not self.pygame_screen:
                print("Pygame screen not initialized")
                return False
            
            # Get screen dimensions
            screen_width, screen_height = self.pygame_screen.get_size()
            image_width, image_height = img.size
            
            # Calculate scaling to fit the screen while maintaining aspect ratio
            scale_x = screen_width / image_width
            scale_y = screen_height / image_height
            scale = min(scale_x, scale_y)
            
            # Scale the image
            new_width = int(image_width * scale)
            new_height = int(image_height * scale)
            scaled_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert PIL image to pygame surface
            img_data = scaled_img.convert("RGB").tobytes()
            pygame_surface = pygame.image.fromstring(img_data, scaled_img.size, "RGB")
            
            # Calculate position to center the image
            x = (screen_width - new_width) // 2
            y = (screen_height - new_height) // 2
            
            # Clear screen and display image
            self.pygame_screen.fill((255, 255, 255))  # White background
            self.pygame_screen.blit(pygame_surface, (x, y))
            pygame.display.flip()
            
            print(f"Image displayed on fullscreen display ({screen_width}x{screen_height})")
            return True
            
        except Exception as e:
            print(f"Error displaying on fullscreen: {e}")
            return False

    def generate_sample_config(self):
        """Generate a sample configuration file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
            print(f"Sample configuration saved to {self.config_file}")
        except Exception as e:
            print(f"Error saving sample configuration: {e}")

    def cleanup(self):
        """Clean up pygame resources"""
        if self.pygame_screen and PYGAME_AVAILABLE:
            try:
                pygame.quit()
                print("Pygame display cleaned up")
            except Exception as e:
                print(f"Error cleaning up pygame: {e}")

    def run(self):
        """Main execution function"""
        current_time = self.get_current_time()
        print(f"Current time: {current_time}")
        print(f"Reading from: {self.tsv_file}")

        data = self.find_time_row(current_time)
        if data:
            print(f"Found data for {current_time}:")
            print(f"  Quote Part 1: {data['quote_part1']}")
            print(f"  Quote Part 2: {data['quote_part2']}")
            print(f"  Quote Part 3: {data['quote_part3']}")
            print(f"  Book Title: {data['book_title']}")
            print(f"  Book Author: {data['book_author']}")

            success = self.create_flowing_text(data)
            return success
        else:
            print("No matching time found in TSV file.")
            return False


def main():
    parser = argparse.ArgumentParser(description='Generate time-based quote image from TTQC_quotes.tsv with flowing text')
    parser.add_argument('-o', '--output', default='time_image.png', help='Output image file name')
    parser.add_argument('--ntp', action='store_true', help='Use NTP server to get current time instead of local time')
    parser.add_argument('--ntp-server', help='Specify a custom NTP server (e.g., time.google.com)')
    parser.add_argument('--inky', action='store_true', help='Display image on Inky Impressions e-paper display')
    parser.add_argument('--fullscreen', action='store_true', help='Display image fullscreen on main display')
    parser.add_argument('--interval', action='store_true', help='Run continuously, updating at the top of each minute')
    
    args = parser.parse_args()

    generator = TimeImageGenerator(args.output, use_ntp=args.ntp, ntp_server=args.ntp_server, use_inky=args.inky, use_fullscreen=args.fullscreen)
    
    try:
        if args.interval:
            run_at_minute_top(generator)
        else:
            generator.run()
    finally:
        generator.cleanup()


def run_at_minute_top(generator):
    """Run the generator continuously, updating at the top of each minute"""
    import time
    import signal
    from datetime import datetime, timedelta
    
    # Use a list to store the running state so it can be modified by the signal handler
    running_state = [True]
    
    def signal_handler(signum, frame):
        """Handle shutdown signals gracefully"""
        print(f"\nReceived signal {signum}, shutting down gracefully...")
        running_state[0] = False
    
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("Starting TTQC display (updating at the top of each minute)...")
    print("Press Ctrl+C to exit")
    
    last_minute = None
    
    while running_state[0]:
        now = datetime.now()
        current_minute = now.replace(second=0, microsecond=0)
        
        # Check if we've moved to a new minute
        if last_minute is None or current_minute > last_minute:
            print(f"\nGenerating new image at {now.strftime('%H:%M:%S')}...")
            
            success = generator.run()
            if success:
                print("✓ Image generated and displayed successfully")
                last_minute = current_minute
            else:
                print("✗ Failed to generate image, will retry in 30 seconds...")
                time.sleep(30)
                continue
        
        # Sleep for a short time to avoid high CPU usage
        time.sleep(1)


if __name__ == "__main__":
    main()
