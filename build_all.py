#!/usr/bin/env python3
"""
Unified build script for Simple Stupid Grammar
Automatically detects platform and builds appropriate distribution
"""

import os
import sys
import platform
import subprocess
from pathlib import Path

def get_platform_info():
    """Get platform information"""
    system = platform.system().lower()
    return {
        'system': system,
        'is_windows': system == 'windows',
        'is_macos': system == 'darwin',
        'is_linux': system == 'linux'
    }

def check_python():
    """Check if Python is properly installed"""
    try:
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 7):
            print(f"[ERROR] Python 3.7+ required. Found: {version.major}.{version.minor}")
            return False
        print(f"[SUCCESS] Python {version.major}.{version.minor}.{version.micro} found")
        return True
    except Exception as e:
        print(f"[ERROR] Python check failed: {e}")
        return False

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    try:
        cmd = [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("[SUCCESS] Dependencies installed")
            return True
        else:
            print(f"[ERROR] Failed to install dependencies: {result.stderr}")
            return False
    except Exception as e:
        print(f"[ERROR] Dependency installation failed: {e}")
        return False

def build_windows():
    """Build Windows executable"""
    print("Building Windows executable...")
    try:
        # Run the Windows build script
        result = subprocess.run([sys.executable, "build_exe.py"], capture_output=True, text=True)
        if result.returncode == 0:
            print("[SUCCESS] Windows executable built")
            return True
        else:
            print(f"[ERROR] Windows build failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"[ERROR] Windows build failed: {e}")
        return False

def build_macos():
    """Build macOS app bundle"""
    print("Building macOS app bundle...")
    try:
        # Run the macOS build script
        result = subprocess.run([sys.executable, "build_macos_app.py"], capture_output=True, text=True)
        if result.returncode == 0:
            print("[SUCCESS] macOS app bundle built")
            return True
        else:
            print(f"[ERROR] macOS build failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"[ERROR] macOS build failed: {e}")
        return False

def create_windows_distribution():
    """Create Windows distribution package"""
    print("Creating Windows distribution package...")
    try:
        # Check if executable exists
        exe_path = Path("dist/SimpleStupidGrammar.exe")
        if not exe_path.exists():
            print("[ERROR] Windows executable not found")
            return False
        
        # Create distribution folder
        dist_folder = Path("SimpleStupidGrammar_Windows_Distribution")
        if dist_folder.exists():
            import shutil
            shutil.rmtree(dist_folder)
        
        dist_folder.mkdir()
        
        # Copy files
        import shutil
        shutil.copy2(exe_path, dist_folder)
        
        # Copy installer scripts if they exist
        files_to_copy = [
            "install_to_startup.bat",
            "remove_from_startup.bat", 
            "README.txt"
        ]
        
        for file in files_to_copy:
            if Path(file).exists():
                shutil.copy2(file, dist_folder)
        
        print(f"[SUCCESS] Windows distribution created: {dist_folder}")
        return True
        
    except Exception as e:
        print(f"[ERROR] Windows distribution creation failed: {e}")
        return False

def create_macos_distribution():
    """Create macOS distribution package"""
    print("Creating macOS distribution package...")
    try:
        # Check if app bundle exists
        app_path = Path("dist/Simple Stupid Grammar.app")
        if not app_path.exists():
            print("[ERROR] macOS app bundle not found")
            return False
        
        # Create distribution folder
        dist_folder = Path("SimpleStupidGrammar_macOS_Distribution")
        if dist_folder.exists():
            import shutil
            shutil.rmtree(dist_folder)
        
        dist_folder.mkdir()
        
        # Copy files
        import shutil
        shutil.copytree(app_path, dist_folder / "Simple Stupid Grammar.app")
        
        # Copy installer scripts if they exist
        files_to_copy = [
            "install_macos.sh",
            "uninstall_macos.sh",
            "README_macOS.txt"
        ]
        
        for file in files_to_copy:
            if Path(file).exists():
                shutil.copy2(file, dist_folder)
        
        print(f"[SUCCESS] macOS distribution created: {dist_folder}")
        return True
        
    except Exception as e:
        print(f"[ERROR] macOS distribution creation failed: {e}")
        return False

def main():
    """Main build process"""
    print("Simple Stupid Grammar - Unified Build System")
    print("=" * 45)
    print()
    
    # Check if we're in the right directory
    if not Path("main.py").exists():
        print("[ERROR] main.py not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    # Get platform info
    platform_info = get_platform_info()
    print(f"Detected platform: {platform_info['system']}")
    
    # Check Python
    if not check_python():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("[WARNING] Dependency installation failed, continuing anyway...")
    
    print()
    print("=" * 45)
    print("BUILDING APPLICATION")
    print("=" * 45)
    
    # Build based on platform
    build_success = False
    if platform_info['is_windows']:
        build_success = build_windows()
    elif platform_info['is_macos']:
        build_success = build_macos()
    else:
        print(f"[ERROR] Unsupported platform: {platform_info['system']}")
        print("This script supports Windows and macOS only.")
        sys.exit(1)
    
    if not build_success:
        print("[ERROR] Build failed!")
        sys.exit(1)
    
    print()
    print("=" * 45)
    print("CREATING DISTRIBUTION")
    print("=" * 45)
    
    # Create distribution based on platform
    dist_success = False
    if platform_info['is_windows']:
        dist_success = create_windows_distribution()
    elif platform_info['is_macos']:
        dist_success = create_macos_distribution()
    
    if not dist_success:
        print("[ERROR] Distribution creation failed!")
        sys.exit(1)
    
    print()
    print("=" * 45)
    print("BUILD COMPLETED SUCCESSFULLY!")
    print("=" * 45)
    
    if platform_info['is_windows']:
        print("\nWindows build completed:")
        print("• Executable: dist/SimpleStupidGrammar.exe")
        print("• Distribution: SimpleStupidGrammar_Windows_Distribution/")
        print("• Share the distribution folder with users")
        print("• Users should run install_to_startup.bat")
        
    elif platform_info['is_macos']:
        print("\nmacOS build completed:")
        print("• App bundle: dist/Simple Stupid Grammar.app")
        print("• Distribution: SimpleStupidGrammar_macOS_Distribution/")
        print("• Share the distribution folder with users")
        print("• Users should run install_macos.sh")
        print("• Remind users to grant accessibility permissions")
    
    print(f"\nThe application is ready for distribution on {platform_info['system']}!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[INTERRUPTED] Build process cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1) 