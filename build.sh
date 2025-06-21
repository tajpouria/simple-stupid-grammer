#!/bin/bash

echo "Simple Stupid Grammar - macOS App Builder"
echo "========================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.7 or higher from https://python.org"
    echo "Or install via Homebrew: brew install python"
    exit 1
fi

echo "Python 3 found. Running build script..."
python3 build_macos_app.py

echo ""
echo "Build process completed. Check above for any errors."
echo "Press any key to continue..."
read -n 1 