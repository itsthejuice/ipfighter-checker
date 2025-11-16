#!/bin/bash

echo "============================================"
echo "IPFighter Checker - Linux Setup"
echo "============================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    echo "Ubuntu/Debian: sudo apt install python3 python3-venv python3-pip"
    echo "Fedora/RHEL: sudo dnf install python3 python3-pip"
    echo "Arch: sudo pacman -S python python-pip"
    exit 1
fi

echo "Python found!"
python3 --version
echo ""

# Check if venv exists
if [ -d "venv" ]; then
    echo "Virtual environment already exists. Skipping creation..."
else
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create virtual environment"
        echo "Try installing python3-venv package"
        exit 1
    fi
    echo "Virtual environment created!"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi
echo ""

# Upgrade pip
echo "Upgrading pip..."
python3 -m pip install --upgrade pip
echo ""

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
echo ""

echo "============================================"
echo "Setup completed successfully!"
echo "============================================"
echo ""
echo "To run the application, use: ./scripts/run_linux.sh"
echo "Or: chmod +x scripts/run_linux.sh && ./scripts/run_linux.sh"
echo ""

