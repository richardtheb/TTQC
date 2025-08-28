# TTQC_flowing.py for Raspberry Pi

This guide will help you set up and run TTQC_flowing.py on your Raspberry Pi.

## Prerequisites

- Raspberry Pi (any model with Python 3.6+)
- Internet connection for initial setup
- SD card with Raspberry Pi OS (formerly Raspbian)

## Quick Setup

1. **Clone or copy the files to your Raspberry Pi**
   ```bash
   # If using git
   git clone <repository-url>
   cd TTQC2
   
   # Or copy files manually via SCP, USB, etc.
   ```

2. **Run the automated setup script**
   ```bash
   ./raspberry_pi_setup.sh
   ```

3. **Test the fonts**
   ```bash
   python3 test_fonts_pi.py
   ```

4. **Run TTQC_flowing.py**
   ```bash
   python3 TTQC_flowing.py
   ```

## Manual Setup (if automated script fails)

### Install System Dependencies
```bash
sudo apt-get update
sudo apt-get install -y python3-pip python3-pil python3-pil.imagetk
sudo apt-get install -y fonts-liberation fonts-dejavu-core fonts-dejavu-extra
```

### Install Python Packages
```bash
pip3 install -r requirements.txt
```

## Usage

### Basic Usage
```bash
# Generate image with local time
python3 TTQC_flowing.py -o my_quote.png

# Generate image with NTP time
python3 TTQC_flowing.py --ntp -o my_quote.png

# Use specific NTP server
python3 TTQC_flowing.py --ntp --ntp-server time.google.com -o my_quote.png

# Display on Inky Impressions e-paper display
python3 TTQC_flowing.py --inky

# Combine NTP time and Inky display
python3 TTQC_flowing.py --ntp --inky
```

### Command Line Options
- `-o, --output`: Specify output filename (default: flowing_time_image.png)
- `--ntp`: Use NTP server instead of local time
- `--ntp-server`: Specify custom NTP server
- `--inky`: Display image on Inky Impressions e-paper display

## Font Compatibility

The script has been updated to use Raspberry Pi compatible fonts:

### Serif Fonts (for quotes)
- Liberation Serif (regular, italic, bold, bold-italic)
- DejaVu Serif (regular, oblique, bold, bold-oblique)

### Sans-Serif Fonts (for attribution)
- Liberation Sans (regular, italic, bold, bold-italic)
- DejaVu Sans (regular, oblique, bold, bold-oblique)

## Troubleshooting

### Font Issues
If fonts don't load, check if they're installed:
```bash
ls /usr/share/fonts/truetype/liberation/
ls /usr/share/fonts/truetype/dejavu/
```

### NTP Issues
If NTP doesn't work, the script will fall back to local time automatically.

### Inky Display Issues
If Inky display doesn't work:
```bash
# Test Inky functionality
python3 test_inky.py

# Check if Inky library is installed
pip3 list | grep inky

# Install Inky library manually
pip3 install inky
```

### Permission Issues
Make sure the script is executable:
```bash
chmod +x TTQC_flowing.py
```

## Performance Tips

- The script works well on all Raspberry Pi models
- For headless operation, ensure you have enough disk space for generated images
- Consider using a cron job for automated generation

## Example Cron Job

To run the script every hour:
```bash
# Edit crontab
crontab -e

# Add this line to run every hour (save to file)
0 * * * * cd /path/to/TTQC2 && python3 TTQC_flowing.py --ntp -o /path/to/output/hourly_quote.png

# Or display on Inky every hour
0 * * * * cd /path/to/TTQC2 && python3 TTQC_flowing.py --ntp --inky
```

## Files Included

- `TTQC_flowing.py`: Main script
- `TTQC_quotes.tsv`: Quote database
- `config.json`: Configuration file
- `requirements.txt`: Python dependencies
- `raspberry_pi_setup.sh`: Automated setup script
- `test_fonts_pi.py`: Font testing script
- `test_inky.py`: Inky display testing script
- `README_RaspberryPi.md`: This file
