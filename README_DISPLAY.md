# TTQC Display System

This system runs TTQC.py once a minute and displays the generated time-based quote images fullscreen on the main Pi display.

**NEW: Fullscreen display and minute-based updates are now built into TTQC.py!** Use `--fullscreen` and `--interval` flags for automatic updates at the top of each minute.

## Features

- **Automatic Updates**: Generates new quote images every minute
- **Fullscreen Display**: Shows images fullscreen on the main Pi display
- **Auto-start**: Can be configured to start automatically on boot
- **Graceful Shutdown**: Handles Ctrl+C and system signals properly
- **Manual Refresh**: Press Spacebar to force a refresh
- **Escape to Exit**: Press Escape key to exit the display

## Installation

### 1. Install Dependencies

```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install -y python3-pip python3-pygame

# Install Python packages
pip3 install -r requirements.txt
```

### 2. Quick Start

**Option A: Single image with fullscreen display**
```bash
python3 TTQC.py --fullscreen
```

**Option B: Continuous display (updates at the top of each minute)**
```bash
python3 TTQC.py --fullscreen --interval
```

### 3. Manual Testing

To test the display manually:

```bash
# Generate and display a single image
python3 TTQC.py --fullscreen -o my_image.png

# Run continuous display
python3 TTQC.py --fullscreen --interval
```

## Usage

### Command Line Options

```bash
# Generate image with fullscreen display
python3 TTQC.py --fullscreen

# Generate image with custom output file
python3 TTQC.py --fullscreen -o my_quote.png

# Use NTP time with fullscreen display
python3 TTQC.py --fullscreen --ntp

# Combine options
python3 TTQC.py --fullscreen --ntp --ntp-server time.google.com
```

### Continuous Display

```bash
# Run continuous display (updates at the top of each minute)
python3 TTQC.py --fullscreen --interval
```

### Manual Control

When running manually:
- **Ctrl+C**: Stop the script
- **Escape**: Exit fullscreen display (if supported)

## Configuration

The display system uses the same configuration as TTQC.py:

- `config.json`: Image styling and layout settings
- `TTQC_quotes.tsv`: Quote database

### Update Interval

To change how often the display updates, edit `ttqc_display.py` and modify:

```python
self.update_interval = 60  # Update every 60 seconds
```

## Troubleshooting

### Display Issues

1. **No display**: Make sure you're running on a Pi with a display connected
2. **Permission errors**: Run with sudo or ensure proper X11 permissions
3. **Pygame errors**: Install pygame: `sudo apt-get install python3-pygame`

### Service Issues

1. **Service won't start**: Check logs: `sudo journalctl -u ttqc-display.service`
2. **Permission denied**: Ensure the service file has correct paths and permissions
3. **Display not found**: Verify DISPLAY environment variable is set correctly

### Manual Debugging

```bash
# Test TTQC.py directly
python3 TTQC.py

# Test display script manually
python3 ttqc_display.py

# Check display environment
echo $DISPLAY
xrandr
```

## Files

- `TTQC.py`: Main script with fullscreen display and minute-based updates
- `requirements.txt`: Python dependencies

## Requirements

- Raspberry Pi with display
- Python 3.6+
- pygame
- All TTQC.py dependencies
- X11 display server running
