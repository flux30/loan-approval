@echo off
REM Rule-Based Expert System Startup Script (Windows)

echo.
echo ====================================================
echo  LoanExpert AI - Rule-Based Expert System
echo  Starting Application...
echo ====================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/update requirements
echo Installing dependencies...
pip install -q -r requirements.txt

REM Start the application
echo.
echo ====================================================
echo Starting Flask Server...
echo ====================================================
echo.
echo Application will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

python app.py

pause
