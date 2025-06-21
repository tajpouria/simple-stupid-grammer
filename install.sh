#!/bin/bash

echo "Installing Simple Stupid Grammar for macOS..."
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.7 or higher from https://python.org"
    echo "Or install via Homebrew: brew install python"
    exit 1
fi

echo "Python 3 found. Installing dependencies..."

# Install dependencies
if ! python3 -m pip install -r requirements.txt; then
    echo "ERROR: Failed to install dependencies"
    echo "You may need to install pip first: python3 -m ensurepip --upgrade"
    exit 1
fi

echo ""
echo "Installation completed successfully!"
echo ""
echo "IMPORTANT: On macOS, you need to grant accessibility permissions:"
echo "1. Go to System Preferences > Security & Privacy > Privacy"
echo "2. Select 'Accessibility' from the left sidebar"
echo "3. Click the lock to make changes (enter your password)"
echo "4. Add Terminal (or your terminal app) to the list"
echo "5. Also add Python if it appears in the list"
echo ""
echo "To run the application:"
echo "  ./run.sh"
echo "or:"
echo "  python3 main.py"
echo "" 