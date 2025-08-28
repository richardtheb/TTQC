@echo off
REM Virtual environment setup script for TTQC (Windows)

echo Setting up virtual environment for TTQC...

REM Check if Python 3 is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt

echo.
echo Virtual environment setup complete!
echo.
echo To activate the virtual environment:
echo   venv\Scripts\activate.bat
echo.
echo To run TTQC:
echo   python TTQC.py
echo.
echo To deactivate the virtual environment:
echo   deactivate
echo.
pause
