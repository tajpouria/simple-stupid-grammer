#!/bin/bash
echo "Creating macOS Distribution Package..."
echo "===================================="
echo

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "WARNING: This script is designed for macOS"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Build the application first
echo "Step 1: Building the application..."
python3 build_app.py

if [ $? -ne 0 ]; then
    echo "ERROR: Application build failed!"
    exit 1
fi

# Check if the app was created
if [ ! -d "dist/Simple Stupid Grammar.app" ]; then
    echo "ERROR: Application not found in dist folder"
    exit 1
fi

echo
echo "Step 2: Creating distribution folder..."
DIST_NAME="SimpleStupidGrammar_macOS_Distribution"
DIST_DIR="$DIST_NAME"

# Remove existing distribution folder
if [ -d "$DIST_DIR" ]; then
    rm -rf "$DIST_DIR"
fi

# Create distribution folder
mkdir -p "$DIST_DIR"

# Copy the application
echo "Copying application..."
cp -R "dist/Simple Stupid Grammar.app" "$DIST_DIR/"

# Copy installation scripts
echo "Copying installation scripts..."
cp install_to_applications.sh "$DIST_DIR/"
cp uninstall.sh "$DIST_DIR/"
cp README_DISTRIBUTION.txt "$DIST_DIR/"

# Create a main README for the distribution
cat > "$DIST_DIR/README.txt" << 'EOF'
================================================================================
                      SIMPLE STUPID GRAMMAR - macOS
                         System-Wide Grammar Correction
================================================================================

QUICK START:
1. Double-click "install_to_applications.sh" to install
2. Enter your password when prompted
3. Get a Google API key from: https://aistudio.google.com/app/apikey
4. Enter the API key when the app starts
5. Look for the "G" icon in your menu bar
6. Select text anywhere and press F9 to correct grammar

WHAT'S INCLUDED:
• Simple Stupid Grammar.app - The main application
• install_to_applications.sh - Installer (adds to Applications & Login Items)
• uninstall.sh - Uninstaller (removes completely)
• README_DISTRIBUTION.txt - Detailed instructions

SYSTEM REQUIREMENTS:
• macOS 10.14 or later
• Internet connection for AI processing
• Google API key (free from Google AI Studio)

TROUBLESHOOTING:
If the app doesn't work, you may need to:
1. Grant Accessibility permissions in System Preferences
2. Right-click the app and select "Open" for first run
3. Check that no other app is using the F9 key

For detailed instructions, see README_DISTRIBUTION.txt

================================================================================
EOF

echo "Step 3: Creating ZIP archive..."
zip -r "${DIST_NAME}.zip" "$DIST_DIR"

if [ $? -eq 0 ]; then
    echo
    echo "SUCCESS! Distribution created:"
    echo "  ${DIST_NAME}.zip"
    echo
    echo "Contents:"
    ls -la "$DIST_DIR"
    echo
    echo "You can now distribute the ZIP file to macOS users."
    echo "They just need to extract it and run install_to_applications.sh"
else
    echo "ERROR: Failed to create ZIP archive"
    exit 1
fi

# Clean up
echo
read -p "Clean up temporary files? (Y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Nn]$ ]]; then
    echo "Temporary files kept in: $DIST_DIR"
else
    rm -rf "$DIST_DIR"
    echo "Temporary files cleaned up"
fi

echo "Done!" 