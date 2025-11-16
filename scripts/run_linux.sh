#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Get the project root directory (parent of scripts directory)
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Change to project root directory
cd "$PROJECT_ROOT"

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

# Run the application as a module
python3 -m src.main "$@"

echo ""
echo "Application closed."

