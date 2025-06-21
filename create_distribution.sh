#!/bin/bash

echo "Creating macOS Distribution Package..."
echo "====================================="
echo ""

# Check if app bundle exists
if [ ! -d "dist/Simple Stupid Grammar.app" ]; then
    echo "ERROR: Simple Stupid Grammar.app not found in dist folder"
    echo "Please run build.sh first to create the app bundle"
    exit 1
fi

# Create distribution folder
DIST_FOLDER="SimpleStupidGrammar_macOS_Distribution"
if [ -d "$DIST_FOLDER" ]; then
    echo "Removing existing distribution folder..."
    rm -rf "$DIST_FOLDER"
fi

echo "Creating distribution folder: $DIST_FOLDER"
mkdir "$DIST_FOLDER"

# Copy files
echo "Copying app bundle..."
cp -R "dist/Simple Stupid Grammar.app" "$DIST_FOLDER/"

echo "Copying installer scripts..."
cp "install_macos.sh" "$DIST_FOLDER/"
cp "uninstall_macos.sh" "$DIST_FOLDER/"
cp "README_macOS.txt" "$DIST_FOLDER/"

echo ""
echo "✓ Distribution package created successfully!"
echo ""
echo "Distribution folder: $DIST_FOLDER"
echo ""
echo "Contents:"
echo "- Simple Stupid Grammar.app (main application bundle)"
echo "- install_macos.sh (Applications folder installer)"
echo "- uninstall_macos.sh (uninstaller)"
echo "- README_macOS.txt (instructions)"
echo ""
echo "You can now create a ZIP archive of this folder and share it!"
echo "Recipients just need to run install_macos.sh"
echo ""
echo "To create a ZIP archive:"
echo "  zip -r ${DIST_FOLDER}.zip $DIST_FOLDER"
echo ""
echo "Press any key to continue..."
read -n 1 