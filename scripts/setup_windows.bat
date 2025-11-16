@echo off

REM Get the directory where the script is located
set "SCRIPT_DIR=%~dp0"
REM Remove trailing backslash
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"
REM Get the project root directory (parent of scripts directory)
for %%I in ("%SCRIPT_DIR%") do set "PROJECT_ROOT=%%~dpI"
REM Remove trailing backslash
set "PROJECT_ROOT=%PROJECT_ROOT:~0,-1%"

REM Change to project root directory
cd /d "%PROJECT_ROOT%"

echo ============================================
echo IPFighter Checker - Windows Setup
echo ============================================
echo.
echo Working directory: %PROJECT_ROOT%
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo Python found!
python --version
echo.

REM Check if venv exists
if exist venv (
    echo Virtual environment already exists. Skipping creation...
) else (
    echo Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created!
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo.

REM Install Playwright browsers
echo Installing Playwright browsers...
playwright install chromium
if %errorlevel% neq 0 (
    echo WARNING: Failed to install Playwright browsers
    echo You may need to run: playwright install chromium
)
echo.

echo ============================================
echo Setup completed successfully!
echo ============================================
echo.
echo To run the application, use: run_windows.bat
echo.
pause

