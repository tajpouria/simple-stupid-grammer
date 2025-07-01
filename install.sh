#!/bin/bash
echo "Installing Simple Stupid Grammar for macOS..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.7 or higher from https://python.org"
    echo "Or install via Homebrew: brew install python"
    exit 1
fi

echo "Python found. Installing dependencies..."
python3 -m pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    echo "You may need to install pip or run with sudo:"
    echo "sudo python3 -m pip install -r requirements.txt"
    exit 1
fi

echo
echo "Installation completed successfully!"
echo
echo "To run the application, execute: ./run.sh or python3 main.py"
echo

# Make the run script executable
chmod +x run.sh 2>/dev/null || true

read -p "Press Enter to continue..." 