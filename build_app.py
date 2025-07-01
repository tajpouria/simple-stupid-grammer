#!/usr/bin/env python3
"""
Build script for creating macOS application bundle
Run this script to bundle the app into a macOS .app bundle
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    try:
        import PyInstaller
        print("[SUCCESS] PyInstaller is already installed")
        return True
    except ImportError:
        print("Installing PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("[SUCCESS] PyInstaller installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Failed to install PyInstaller: {e}")
            return False

def create_spec_file():
    """Create a PyInstaller spec file for macOS"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'google.genai',
        'google.genai.types',
        'keyring.backends.macOS',
        'pystray._darwin',
        'PIL._tkinter_finder'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SimpleStupidGrammar',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

app = BUNDLE(
    exe,
    name='Simple Stupid Grammar.app',
    icon=None,
    bundle_identifier='com.simplestupidgrammar.app',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSAppleScriptEnabled': False,
        'LSBackgroundOnly': False,
        'NSHighResolutionCapable': True,
        'LSUIElement': True,  # This makes it not show in dock but allows menu bar
    },
)
'''
    
    with open('SimpleStupidGrammar.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    print("[SUCCESS] Created PyInstaller spec file for macOS")

def build_application():
    """Build the macOS application using PyInstaller"""
    try:
        print("Building macOS application... This may take a few minutes...")
        
        # Use the spec file for more control
        cmd = [sys.executable, "-m", "PyInstaller", "--clean", "SimpleStupidGrammar.spec"]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("[SUCCESS] Application built successfully!")
            
            # Check if app was created
            app_path = Path("dist/Simple Stupid Grammar.app")
            if app_path.exists():
                print(f"[SUCCESS] Application created: {app_path}")
                return True
            else:
                print("[ERROR] Application not found in expected location")
                return False
        else:
            print("[ERROR] Build failed!")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except Exception as e:
        print(f"[ERROR] Error during build: {e}")
        return False

def create_installer_script():
    """Create a shell script to install the app to Applications and Login Items"""
    installer_content = '''#!/bin/bash
echo "Simple Stupid Grammar - macOS Installer"
echo "======================================"
echo

# Get the directory where this script is located
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_PATH="$APP_DIR/Simple Stupid Grammar.app"
APPLICATIONS_DIR="/Applications"
TARGET_PATH="$APPLICATIONS_DIR/Simple Stupid Grammar.app"

# Check if app exists
if [ ! -d "$APP_PATH" ]; then
    echo "ERROR: Simple Stupid Grammar.app not found in $APP_DIR"
    echo "Please make sure the application bundle is in the same folder as this installer."
    echo
    read -p "Press Enter to continue..."
    exit 1
fi

echo "Found application: $APP_PATH"
echo "Installing to: $TARGET_PATH"
echo

# Copy app to Applications folder
echo "Installing application to Applications folder..."
if cp -R "$APP_PATH" "$APPLICATIONS_DIR/"; then
    echo "[SUCCESS] Application installed to Applications folder"
else
    echo "[ERROR] Failed to install application (you may need administrator privileges)"
    echo "Try running: sudo ./install_to_applications.sh"
    read -p "Press Enter to continue..."
    exit 1
fi

# Add to Login Items using osascript
echo "Adding to Login Items (auto-start on login)..."
osascript -e "tell application \\"System Events\\" to make login item at end with properties {path:\\"$TARGET_PATH\\", hidden:false}" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "[SUCCESS] Added Simple Stupid Grammar to Login Items"
    echo
    echo "The application will now start automatically when you log in."
    echo "You can also launch it manually from Applications folder."
    echo
    echo "To remove from Login Items:"
    echo "System Preferences > Users & Groups > Login Items"
else
    echo "[WARNING] Could not automatically add to Login Items"
    echo "You can manually add it via System Preferences > Users & Groups > Login Items"
fi

echo
echo "Installation complete!"
read -p "Press Enter to continue..."
'''
    
    with open('install_to_applications.sh', 'w', encoding='utf-8') as f:
        f.write(installer_content)
    
    # Make the script executable
    os.chmod('install_to_applications.sh', 0o755)
    print("[SUCCESS] Created macOS installer script")

def create_uninstaller_script():
    """Create a script to remove from Applications and Login Items"""
    uninstaller_content = '''#!/bin/bash
echo "Simple Stupid Grammar - macOS Uninstaller"
echo "========================================"
echo

APP_PATH="/Applications/Simple Stupid Grammar.app"

# Remove from Login Items
echo "Removing from Login Items..."
osascript -e "tell application \\"System Events\\" to delete login item \\"Simple Stupid Grammar\\"" 2>/dev/null

# Remove from Applications
if [ -d "$APP_PATH" ]; then
    echo "Removing application from Applications folder..."
    rm -rf "$APP_PATH"
    
    if [ ! -d "$APP_PATH" ]; then
        echo "[SUCCESS] Simple Stupid Grammar has been uninstalled"
    else
        echo "[ERROR] Failed to remove application (you may need administrator privileges)"
        echo "Try running: sudo ./uninstall.sh"
    fi
else
    echo "Simple Stupid Grammar is not installed in Applications folder"
fi

echo
read -p "Press Enter to continue..."
'''
    
    with open('uninstall.sh', 'w', encoding='utf-8') as f:
        f.write(uninstaller_content)
    
    # Make the script executable
    os.chmod('uninstall.sh', 0o755)
    print("[SUCCESS] Created macOS uninstaller script")

def create_readme():
    """Create a README for the distribution"""
    readme_content = '''# Simple Stupid Grammar - macOS Distribution

## What's Included

- `Simple Stupid Grammar.app` - The main application
- `install_to_applications.sh` - Installer script
- `uninstall.sh` - Uninstaller script
- `README_DISTRIBUTION.txt` - This file

## Installation

1. Double-click `install_to_applications.sh` to install
2. Enter your password if prompted
3. The app will be installed to Applications and added to Login Items

## Usage

1. Launch "Simple Stupid Grammar" from Applications (or it will auto-start)
2. Look for the "G" icon in your menu bar
3. Select text in any application and press F9 to correct grammar
4. Enter your Google API key when prompted (get from: https://aistudio.google.com/app/apikey)

## Uninstallation

Run `uninstall.sh` to remove the application completely.

## System Requirements

- macOS 10.14 or later
- Internet connection for AI processing
- Google API key (free from Google AI Studio)

## Troubleshooting

If the app doesn't work:
1. Check System Preferences > Security & Privacy > Accessibility
2. Add "Simple Stupid Grammar" to allowed apps
3. Try running from Terminal: open "/Applications/Simple Stupid Grammar.app"
'''
    
    with open('README_DISTRIBUTION.txt', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print("[SUCCESS] Created distribution README")

def cleanup_build_files():
    """Clean up build artifacts"""
    try:
        # Remove build directory
        if os.path.exists('build'):
            shutil.rmtree('build')
            print("[SUCCESS] Cleaned up build directory")
        
        # Remove spec file
        if os.path.exists('SimpleStupidGrammar.spec'):
            os.remove('SimpleStupidGrammar.spec')
            print("[SUCCESS] Cleaned up spec file")
            
    except Exception as e:
        print(f"[WARNING] Could not clean up some files: {e}")

def main():
    """Main build process"""
    print("=" * 60)
    print("Simple Stupid Grammar - macOS App Builder")
    print("=" * 60)
    print()
    
    # Check if we're on macOS
    if sys.platform != 'darwin':
        print("[WARNING] This script is designed for macOS")
        print("You can still build, but the result may not work properly")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            return
    
    # Step 1: Install PyInstaller
    print("Step 1: Installing PyInstaller...")
    if not install_pyinstaller():
        print("[ERROR] Cannot continue without PyInstaller")
        return
    print()
    
    # Step 2: Create spec file
    print("Step 2: Creating PyInstaller spec file...")
    create_spec_file()
    print()
    
    # Step 3: Build the application
    print("Step 3: Building macOS application...")
    if not build_application():
        print("[ERROR] Build failed!")
        return
    print()
    
    # Step 4: Create installer scripts
    print("Step 4: Creating installer scripts...")
    create_installer_script()
    create_uninstaller_script()
    print()
    
    # Step 5: Create documentation
    print("Step 5: Creating documentation...")
    create_readme()
    print()
    
    # Step 6: Cleanup
    print("Step 6: Cleaning up...")
    cleanup_build_files()
    print()
    
    print("=" * 60)
    print("BUILD COMPLETE!")
    print("=" * 60)
    print()
    print("Your macOS application has been created in the 'dist' folder:")
    print("  - Simple Stupid Grammar.app")
    print()
    print("Installation files created:")
    print("  - install_to_applications.sh")
    print("  - uninstall.sh")
    print("  - README_DISTRIBUTION.txt")
    print()
    print("To distribute, zip the contents of the 'dist' folder along with")
    print("the installation scripts.")
    print()

if __name__ == "__main__":
    main() 