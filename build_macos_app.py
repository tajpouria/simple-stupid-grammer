#!/usr/bin/env python3
"""
Build script for creating macOS app bundle for Simple Stupid Grammar
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_requirements():
    """Check if required tools are available"""
    print("Checking build requirements...")
    
    # Check if we're on macOS
    if sys.platform != "darwin":
        print("[ERROR] This script must be run on macOS")
        return False
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("[ERROR] Python 3.7 or higher is required")
        return False
    
    print("[SUCCESS] Requirements check passed")
    return True

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    try:
        import PyInstaller
        print("[SUCCESS] PyInstaller is already installed")
        return True
    except ImportError:
        print("PyInstaller not found. Installing...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
            print("[SUCCESS] PyInstaller installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("[ERROR] Failed to install PyInstaller")
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
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='SimpleStupidGrammar',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SimpleStupidGrammar',
)

app = BUNDLE(
    coll,
    name='Simple Stupid Grammar.app',
    icon=None,
    bundle_identifier='com.simplestupidgrammar.app',
    info_plist={
        'NSHighResolutionCapable': 'True',
        'LSUIElement': '1',  # Hide from dock (background app)
        'NSAppleEventsUsageDescription': 'This app needs to send keystrokes to correct grammar.',
        'NSSystemAdministrationUsageDescription': 'This app needs system access to monitor hotkeys globally.',
    },
)
'''
    
    with open('SimpleStupidGrammar_macOS.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    print("[SUCCESS] Created PyInstaller spec file for macOS")

def build_app():
    """Build the macOS app bundle using PyInstaller"""
    try:
        print("Building macOS app bundle... This may take a few minutes...")
        
        # Use the spec file for more control
        cmd = [sys.executable, "-m", "PyInstaller", "--clean", "SimpleStupidGrammar_macOS.spec"]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("[SUCCESS] App bundle built successfully!")
            
            # Check if app was created
            app_path = Path("dist/Simple Stupid Grammar.app")
            if app_path.exists():
                size_mb = sum(f.stat().st_size for f in app_path.rglob('*') if f.is_file()) / (1024 * 1024)
                print(f"[SUCCESS] App bundle created: {app_path} ({size_mb:.1f} MB)")
                return True
            else:
                print("[ERROR] App bundle not found in expected location")
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
    """Create a shell script to install the app to Applications"""
    installer_content = '''#!/bin/bash

echo "Simple Stupid Grammar - macOS Installer"
echo "======================================="
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_PATH="$SCRIPT_DIR/Simple Stupid Grammar.app"
APPLICATIONS_DIR="/Applications"
TARGET_PATH="$APPLICATIONS_DIR/Simple Stupid Grammar.app"

# Check if app bundle exists
if [ ! -d "$APP_PATH" ]; then
    echo "ERROR: Simple Stupid Grammar.app not found in $SCRIPT_DIR"
    echo "Please make sure the app bundle is in the same folder as this installer."
    echo ""
    exit 1
fi

echo "Found app bundle: $APP_PATH"
echo "Installing to: $TARGET_PATH"
echo ""

# Remove existing installation if it exists
if [ -d "$TARGET_PATH" ]; then
    echo "Removing existing installation..."
    rm -rf "$TARGET_PATH"
fi

# Copy the app to Applications
echo "Installing Simple Stupid Grammar to Applications folder..."
cp -R "$APP_PATH" "$APPLICATIONS_DIR/"

if [ $? -eq 0 ]; then
    echo "[SUCCESS] Simple Stupid Grammar installed successfully!"
    echo ""
    echo "IMPORTANT: You need to grant accessibility permissions:"
    echo "1. Go to System Preferences > Security & Privacy > Privacy"
    echo "2. Select 'Accessibility' from the left sidebar"  
    echo "3. Click the lock to make changes (enter your password)"
    echo "4. Add 'Simple Stupid Grammar' to the list"
    echo ""
    echo "You can now:"
    echo "• Launch the app from Applications folder"
    echo "• Or run it from Spotlight (Cmd+Space, type 'Simple Stupid Grammar')"
    echo ""
    echo "The app will appear in your menu bar with a 'G' icon."
else
    echo "[ERROR] Failed to install the application"
    echo "You may need to run this installer with sudo or check permissions"
fi

echo ""
echo "Press any key to continue..."
read -n 1
'''
    
    with open('install_macos.sh', 'w', encoding='utf-8') as f:
        f.write(installer_content)
    
    # Make the script executable
    os.chmod('install_macos.sh', 0o755)
    print("[SUCCESS] Created macOS installer script")

def create_uninstaller_script():
    """Create a shell script to remove the app from Applications"""
    uninstaller_content = '''#!/bin/bash

echo "Simple Stupid Grammar - macOS Uninstaller"
echo "========================================="
echo ""

TARGET_PATH="/Applications/Simple Stupid Grammar.app"

if [ -d "$TARGET_PATH" ]; then
    echo "Removing Simple Stupid Grammar from Applications..."
    rm -rf "$TARGET_PATH"
    
    if [ ! -d "$TARGET_PATH" ]; then
        echo "[SUCCESS] Simple Stupid Grammar has been removed from Applications"
    else
        echo "[ERROR] Failed to remove the application - you may need administrator privileges"
    fi
else
    echo "Simple Stupid Grammar is not currently installed in Applications"
fi

echo ""
echo "Press any key to continue..."
read -n 1
'''
    
    with open('uninstall_macos.sh', 'w', encoding='utf-8') as f:
        f.write(uninstaller_content)
    
    # Make the script executable
    os.chmod('uninstall_macos.sh', 0o755)
    print("[SUCCESS] Created macOS uninstaller script")

def create_readme():
    """Create a README with macOS-specific instructions"""
    readme_content = '''# Simple Stupid Grammar - macOS App Bundle Distribution

## Files Included

- **Simple Stupid Grammar.app** - The main application bundle
- **install_macos.sh** - Install the app to Applications folder
- **uninstall_macos.sh** - Remove the app from Applications folder
- **README_macOS.txt** - This file

## Installation Instructions

### Option 1: Install to Applications (Recommended)
1. Double-click `install_macos.sh` (or run it from Terminal)
2. Follow the prompts to install the app to Applications folder
3. Grant accessibility permissions when prompted:
   - Go to System Preferences > Security & Privacy > Privacy
   - Select 'Accessibility' from the left sidebar
   - Click the lock to make changes (enter your password)
   - Add 'Simple Stupid Grammar' to the list
4. Launch the app from Applications or Spotlight

### Option 2: Run Directly
1. Double-click `Simple Stupid Grammar.app` to run the application
2. The app will appear in your menu bar (look for the "G" icon)
3. On first run, you'll be prompted to enter your Google API key

## Usage

- Press **F9** to correct grammar in selected text
- Right-click the menu bar icon for options
- The app runs quietly in the background

## Google API Key Setup

On first run, you'll need to provide a Google API key:
1. Visit https://aistudio.google.com/app/apikey
2. Create a new API key
3. Enter the key when prompted
4. The key will be securely stored in macOS Keychain for future use

## Accessibility Permissions

macOS requires explicit permission for apps to:
- Monitor global hotkeys
- Send keystrokes to other applications

To grant these permissions:
1. Go to System Preferences > Security & Privacy > Privacy
2. Select 'Accessibility' from the left sidebar
3. Click the lock icon and enter your password
4. Click '+' and add 'Simple Stupid Grammar' to the list
5. Restart the application

## Uninstallation

To remove the app:
1. Run `uninstall_macos.sh`
2. Or manually delete `Simple Stupid Grammar.app` from Applications

## Troubleshooting

- **App doesn't start**: Check if it's blocked by Gatekeeper. Go to System Preferences > Security & Privacy > General and allow the app
- **Hotkey doesn't work**: Ensure accessibility permissions are granted
- **Menu bar icon missing**: Look for the "G" icon in the menu bar. Some versions of macOS may hide icons when space is limited

## System Requirements

- macOS 10.14 (Mojave) or later
- Internet connection (for Google AI API)
- Google API key (free from Google AI Studio)

## Technical Notes

- The app bundle is self-contained and doesn't require Python to be installed
- Uses macOS Keychain for secure API key storage
- Integrates with macOS menu bar (not dock)
- Supports macOS dark mode
'''
    
    with open('README_macOS.txt', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print("[SUCCESS] Created macOS README")

def main():
    """Main build process for macOS"""
    print("Simple Stupid Grammar - macOS App Builder")
    print("========================================")
    print()
    
    # Check if we're in the right directory
    if not os.path.exists('main.py'):
        print("[ERROR] main.py not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Install PyInstaller
    if not install_pyinstaller():
        sys.exit(1)
    
    # Create spec file for better control
    create_spec_file()
    
    # Build the app bundle
    if not build_app():
        sys.exit(1)
    
    # Create installer and uninstaller scripts
    create_installer_script()
    create_uninstaller_script()
    create_readme()
    
    print("\n" + "="*50)
    print("[SUCCESS] macOS BUILD COMPLETED SUCCESSFULLY!")
    print("="*50)
    print("\nNext steps:")
    print("1. Navigate to the 'dist' folder")
    print("2. You'll find 'Simple Stupid Grammar.app' there")
    print("3. Run 'install_macos.sh' to install to Applications")
    print("4. Grant accessibility permissions in System Preferences")
    print("\nThe app bundle is completely standalone and doesn't require Python to be installed!")

if __name__ == "__main__":
    main() 