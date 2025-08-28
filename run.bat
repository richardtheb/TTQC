@echo off
REM Run TTQC in virtual environment (Windows)

REM Check if virtual environment exists
if not exist "venv" (
    echo Virtual environment not found. Creating one...
    call venv_setup.bat
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run TTQC with all arguments passed to this script
python TTQC.py %*

REM Deactivate virtual environment
deactivate
