@echo off
REM Force script to run from the directory where the script is located
cd /d "%~dp0"
echo ================================================
echo Django + Tailwind CSS Project Installation
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.8+ and add it to your PATH.
    pause
    exit /b 1
)

echo Step 1: Creating virtual environment...
if exist "venv" (
    echo Virtual environment already exists. Skipping creation.
) else (
    python -m venv wvenv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment!
        pause
        exit /b 1
    )
    echo Virtual environment created successfully.
)

echo.
echo Step 2: Activating virtual environment...
call "wvenv\Scripts\activate.bat"
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment!
    pause
    exit /b 1
)

echo.
echo Step 3: Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo ERROR: Failed to upgrade pip!
    pause
    exit /b 1
)

echo.
echo Step 4: Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install Python dependencies!
    pause
    exit /b 1
)

echo.
echo Step 5: Running Django development server...
python manage.py runserver
if errorlevel 1 (
    echo ERROR: Failed to start Django development server!
    pause
    exit /b 1
)

echo.
echo ================================================
echo Installation completed and server started!
echo ================================================
echo.
echo Note: Make sure to activate the virtual environment before running Django commands:
echo       venv\Scripts\activate
echo.
pause
