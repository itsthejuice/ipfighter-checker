@echo off
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

REM Change to src directory and run the application
cd src
python main.py %*

REM Return to root directory
cd ..

echo.
echo Application closed.
pause

