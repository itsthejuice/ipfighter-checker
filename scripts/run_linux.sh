#!/bin/bash

echo "============================================"
echo "IPFighter Checker - Starting Application"
echo "============================================"
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "ERROR: Virtual environment not found!"
    echo "Please run ./scripts/setup_linux.sh first"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi

# Change to src directory and run the application
cd src
python3 main.py "$@"

# Return to root directory
cd ..

echo ""
echo "Application closed."

