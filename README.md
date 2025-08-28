# TTQC - Time-based TSV Quote Generator

A Python script that generates beautiful quote images based on the current time, with support for flowing text formatting, NTP time synchronization, and Inky Impressions e-paper display output.

## Features

- **Time-based quotes**: Finds quotes from a TSV database based on current time
- **Flowing text formatting**: Natural text flow with mixed formatting and colors
- **NTP time synchronization**: Accurate time from network servers
- **Inky Impressions support**: Display on e-paper displays
- **Raspberry Pi compatible**: Optimized for Raspberry Pi with proper font support
- **Customizable styling**: JSON configuration for fonts, colors, and layout

## Quick Start

### Basic Usage
```bash
# Generate image with local time
python3 TTQC.py

# Generate image with NTP time
python3 TTQC.py --ntp

# Display on Inky Impressions e-paper display
python3 TTQC.py --inky

# Combine features
python3 TTQC.py --ntp --inky -o my_quote.png
```

### Command Line Options
- `-o, --output`: Specify output filename (default: time_image.png)
- `--ntp`: Use NTP server instead of local time
- `--ntp-server`: Specify custom NTP server (e.g., time.google.com)
- `--inky`: Display image on Inky Impressions e-paper display
- `--generate-config`: Generate sample configuration file

## Installation

### Virtual Environment (Recommended)

#### macOS
```bash
# Set up virtual environment (macOS optimized)
./venv_setup_macos.sh

# Run TTQC
./run.sh

# Or activate manually
source venv/bin/activate
python TTQC.py
deactivate
```

#### Linux/Raspberry Pi
```bash
# Set up virtual environment
./venv_setup.sh

# Run TTQC
./run.sh

# Or activate manually
source venv/bin/activate
python TTQC.py
deactivate
```

#### Windows
```bash
# Set up virtual environment
venv_setup.bat

# Run TTQC
run.bat

# Or activate manually
venv\Scripts\activate.bat
python TTQC.py
deactivate
```

### Standard Installation
```bash
pip3 install -r requirements.txt
```

### Raspberry Pi Installation
```bash
./raspberry_pi_setup.sh
```

## Configuration

The script uses `config.json` for styling configuration:

```json
{
    "image_size": [800, 600],
    "background_color": "#ffffff",
    "quote_text": {
        "font_family": "Lora",
        "font_size": 32,
        "max_width": 700,
        "line_spacing": 10
    },
    "quote_highlight": {
        "font_family": "Lora",
        "font_size": 32,
        "font_weight": "italic",
        "color": "#ff0000"
    },
    "quote_normal": {
        "color": "#2c3e50"
    },
    "attribution_section": {
        "font_family": "Open Sans",
        "font_size": 20,
        "font_weight": "regular",
        "color": "#95a5a6"
    }
}
```

## File Structure

- `TTQC.py`: Main script (flowing text version)
- `TTQC_original.py`: Original separate-parts version (backup)
- `TTQC_quotes.tsv`: Quote database
- `config.json`: Configuration file
- `requirements.txt`: Python dependencies (full version)
- `requirements_macos.txt`: macOS-compatible dependencies
- `venv_setup.sh`: Virtual environment setup (Linux/Raspberry Pi)
- `venv_setup_macos.sh`: Virtual environment setup (macOS)
- `venv_setup.bat`: Virtual environment setup (Windows)
- `run.sh`: Run script (macOS/Linux)
- `run.bat`: Run script (Windows)
- `raspberry_pi_setup.sh`: Raspberry Pi setup script
- `test_fonts_pi.py`: Font testing script
- `test_inky.py`: Inky display testing script
- `README_RaspberryPi.md`: Detailed Raspberry Pi guide
- `.gitignore`: Git ignore file

## Examples

### Local Time
```bash
# Using virtual environment
./run.sh -o local_quote.png

# Or manually
source venv/bin/activate
python TTQC.py -o local_quote.png
deactivate
```

### NTP Time with Custom Server
```bash
./run.sh --ntp --ntp-server time.apple.com -o ntp_quote.png
```

### Inky Display
```bash
./run.sh --inky
```

### Automated Updates (Cron)
```bash
# Update every hour (using virtual environment)
0 * * * * cd /path/to/TTQC2 && ./run.sh --ntp --inky

# Or without virtual environment
0 * * * * cd /path/to/TTQC2 && python3 TTQC.py --ntp --inky
```

## Troubleshooting

### Font Issues
```bash
python3 test_fonts_pi.py
```

### Inky Display Issues
```bash
python3 test_inky.py
```

### NTP Issues
The script automatically falls back to local time if NTP fails.

## Requirements

- Python 3.6+
- Pillow (PIL)
- ntplib (for NTP time)
- inky (for e-paper display)
- requests

## License

This project is open source and available under the MIT License.
