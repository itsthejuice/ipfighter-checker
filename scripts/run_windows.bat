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
echo IPFighter Checker - Starting Application
echo ============================================
echo.

REM Check if venv exists
if not exist venv (
    echo ERROR: Virtual environment not found!
    echo Please run setup_windows.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Run the application as a module
python -m src.main %*

echo.
echo Application closed.
pause

