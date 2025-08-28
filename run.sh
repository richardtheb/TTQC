#!/bin/bash
# Run TTQC in virtual environment

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."
    ./venv_setup.sh
fi

# Activate virtual environment
source venv/bin/activate

# Run TTQC with all arguments passed to this script
python TTQC.py "$@"

# Deactivate virtual environment
deactivate
