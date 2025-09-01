# Tick Tock Quote Clock

*Richard Baguley (with assistance from Cursor AI)*

An overly complex literary clock for the Raspberry Pi Zero 2 W and the Pimoroni Inky Impressions display. Other literary quote clocks just print out a quote. This one highlights the time part of the quote in RED!
How? Magic! Well, no, more a bit of fiddling around. Working from the list of quotes for the origional Guardian project, I sliced the quotes into three parts: the first part, the time and the second part. 
So, this quote:

>If Jill had been more used to adventures, she might have doubted the Owl’s word, but this never occurred to her; and in the exciting idea of a midnight escape she forgot her sleepiness.

Is split into this:

>If Jill had been more used to adventures, she might have doubted the Owl’s word, but this never occurred to her; and in the exciting idea of a

>midnight 

>escape she forgot her sleepiness.

The program takes the three parts and reassembles the quote, but formats each part differently, as copntrolled by the config.json file. By default, the main text is black, but the quote time is in red. 

## Installation

### 1. Install Dependencies

To install TTQC, make sure Python 3 is installed, then clone this repository and move into the directory.

```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install -y python3-pip python3-pygame

git clone TK
cd TTQC
# Create Virtual Environment
python3 -m venv venv

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Enter Virtual Environment
source venv/bin/activate

#Test the Inky Screen
python stripes.py

#Run the main program!
python3 TTQC.py

```

### 2. Quick Start

**Option A: Single image on the Inky display**
```bash
python3 TTQC.py --Inky
```

**Option B: Continuous display (updates at the top of each minute)**
```bash
python3 TTQC.py --Inky --interval
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
python3 TTQC.py --inky --interval
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

To change how often the display updates, change the interval: 

```bash
# Run continuous display (updates at the top of each minute). The default is 60 seconds for a 1-minute clock
python3 TTQC.py --inky --interval 120
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



## Files

- `TTQC.py`: Main script with fullscreen display and minute-based updates
- `requirements.txt`: Python dependencies
- TTQC_quotes.tsv: The quotes in tabl delimited format, with a structure of Time, Quote_Time, Quote_Part1, Quote_Part3, Book, Author. (see the linked spreadsheet for more details. 

## Quotes


## Requirements

- Raspberry Pi with display
- Python 3.6+
- All TTQC.py dependencies, listed in requirements.txt
- X11 display server running
