@echo off
REM RayPulse Setup Script for Windows

echo ======================================
echo   RayPulse Installation Script
echo ======================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo ✓ Python found
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo.
echo Installing dependencies...
pip install -r requirements.txt

REM Download NLTK data
echo.
echo Downloading NLTK data...
python -c "import nltk; nltk.download('brown', quiet=True); nltk.download('punkt', quiet=True)"

REM Initialize database
echo.
echo Initializing database...
python init_db.py

echo.
echo ======================================
echo   Installation Complete!
echo ======================================
echo.
echo To start RayPulse:
echo   1. Activate virtual environment: venv\Scripts\activate.bat
echo   2. Run the application: python app.py
echo   3. Open browser: http://localhost:5000
echo.
echo ======================================
pause
