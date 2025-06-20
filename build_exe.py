#!/usr/bin/env python3
"""
Build script for creating Windows executable
Run this script to bundle the app into a single .exe file
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
    """Create a PyInstaller spec file for better control"""
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
        'keyring.backends.Windows',
        'keyring.backends._Windows_cffi',
        'pystray._win32',
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
    console=False,  # Set to False for no console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon='icon.ico' if you have an icon file
)
'''
    
    with open('SimpleStupidGrammar.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    print("[SUCCESS] Created PyInstaller spec file")

def build_executable():
    """Build the executable using PyInstaller"""
    try:
        print("Building executable... This may take a few minutes...")
        
        # Use the spec file for more control
        cmd = [sys.executable, "-m", "PyInstaller", "--clean", "SimpleStupidGrammar.spec"]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("[SUCCESS] Executable built successfully!")
            
            # Check if exe was created
            exe_path = Path("dist/SimpleStupidGrammar.exe")
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                print(f"[SUCCESS] Executable created: {exe_path} ({size_mb:.1f} MB)")
                return True
            else:
                print("[ERROR] Executable not found in expected location")
                return False
        else:
            print("[ERROR] Build failed!")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except Exception as e:
        print(f"[ERROR] Error during build: {e}")
        return False

def create_installer_batch():
    """Create a batch file to install the exe to startup"""
    installer_content = '''@echo off
echo Simple Stupid Grammar - Windows Startup Installer
echo ================================================
echo.

REM Get the directory where this batch file is located
set "APP_DIR=%~dp0"
set "EXE_PATH=%APP_DIR%SimpleStupidGrammar.exe"
set "STARTUP_DIR=%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"

REM Check if exe exists
if not exist "%EXE_PATH%" (
    echo ERROR: SimpleStupidGrammar.exe not found in %APP_DIR%
    echo Please make sure the executable is in the same folder as this installer.
    echo.
    pause
    exit /b 1
)

echo Found executable: %EXE_PATH%
echo Startup folder: %STARTUP_DIR%
echo.

REM Create a shortcut in startup folder
echo Creating startup shortcut...

REM Use PowerShell to create shortcut
powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%STARTUP_DIR%\\Simple Stupid Grammar.lnk'); $Shortcut.TargetPath = '%EXE_PATH%'; $Shortcut.WorkingDirectory = '%APP_DIR%'; $Shortcut.Description = 'Simple Stupid Grammar - System Tray Grammar Correction Tool'; $Shortcut.Save()}"

if %errorlevel% equ 0 (
    echo [SUCCESS] Successfully installed Simple Stupid Grammar to Windows startup!
    echo.
    echo The application will now start automatically when Windows boots.
    echo You can also run it manually by double-clicking SimpleStupidGrammar.exe
    echo.
    echo To uninstall from startup, simply delete:
    echo "%STARTUP_DIR%\\Simple Stupid Grammar.lnk"
) else (
    echo [ERROR] Failed to create startup shortcut
    echo You may need to run this installer as administrator
)

echo.
pause
'''
    
    with open('install_to_startup.bat', 'w', encoding='utf-8') as f:
        f.write(installer_content)
    print("[SUCCESS] Created startup installer batch file")

def create_uninstaller_batch():
    """Create a batch file to remove from startup"""
    uninstaller_content = '''@echo off
echo Simple Stupid Grammar - Startup Uninstaller
echo ==========================================
echo.

set "STARTUP_DIR=%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
set "SHORTCUT_PATH=%STARTUP_DIR%\\Simple Stupid Grammar.lnk"

if exist "%SHORTCUT_PATH%" (
    echo Removing startup shortcut...
    del "%SHORTCUT_PATH%"
    
    if not exist "%SHORTCUT_PATH%" (
        echo [SUCCESS] Successfully removed Simple Stupid Grammar from Windows startup
    ) else (
        echo [ERROR] Failed to remove shortcut - you may need administrator privileges
    )
) else (
    echo Simple Stupid Grammar is not currently installed in startup
)

echo.
pause
'''
    
    with open('remove_from_startup.bat', 'w', encoding='utf-8') as f:
        f.write(uninstaller_content)
    print("[SUCCESS] Created startup uninstaller batch file")

def create_readme():
    """Create a README with instructions"""
    readme_content = '''# Simple Stupid Grammar - Windows Executable Distribution

## Files Included

- **SimpleStupidGrammar.exe** - The main application executable
- **install_to_startup.bat** - Install the app to run on Windows startup
- **remove_from_startup.bat** - Remove the app from Windows startup
- **README.txt** - This file

## Installation Instructions

### Option 1: Run Manually
1. Double-click `SimpleStupidGrammar.exe` to run the application
2. The app will appear in your system tray
3. On first run, you'll be prompted to enter your Google API key

### Option 2: Install to Windows Startup (Recommended)
1. Right-click `install_to_startup.bat` and select "Run as administrator"
2. Follow the prompts to install the app to Windows startup
3. The app will now start automatically when Windows boots
4. Look for the app icon in your system tray

## Usage

- Press **F9** to correct grammar in selected text
- Right-click the system tray icon for options
- The app runs quietly in the background

## Google API Key Setup

On first run, you'll need to provide a Google API key:
1. Visit https://aistudio.google.com/app/apikey
2. Create a new API key
3. Enter the key when prompted
4. The key will be securely stored for future use

## Uninstallation

To remove from Windows startup:
1. Run `remove_from_startup.bat`

To completely uninstall:
1. Run `remove_from_startup.bat` first
2. Delete the application folder

## Troubleshooting

- If the app doesn't start, try running as administrator
- If hotkey F9 doesn't work, check the system tray menu for alternatives
- For API key issues, right-click the tray icon and select "Reset API Key"

## System Requirements

- Windows 10 or later
- Internet connection (for Google AI API)
- Google API key (free from Google AI Studio)
'''
    
    with open('README.txt', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print("[SUCCESS] Created README.txt")

def main():
    """Main build process"""
    print("Simple Stupid Grammar - Executable Builder")
    print("=========================================")
    print()
    
    # Check if we're in the right directory
    if not os.path.exists('main.py'):
        print("[ERROR] main.py not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    # Install PyInstaller
    if not install_pyinstaller():
        sys.exit(1)
    
    # Create spec file for better control
    create_spec_file()
    
    # Build the executable
    if not build_executable():
        sys.exit(1)
    
    # Create installer and uninstaller batch files
    create_installer_batch()
    create_uninstaller_batch()
    create_readme()
    
    print("\n" + "="*50)
    print("[SUCCESS] BUILD COMPLETED SUCCESSFULLY!")
    print("="*50)
    print("\nNext steps:")
    print("1. Navigate to the 'dist' folder")
    print("2. You'll find SimpleStupidGrammar.exe there")
    print("3. Copy the exe along with the batch files to a permanent location")
    print("4. Run install_to_startup.bat to add to Windows startup")
    print("\nThe executable is completely standalone and doesn't require Python to be installed!")

if __name__ == "__main__":
    main() 