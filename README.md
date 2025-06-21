```
================================================================================
                            SIMPLE STUPID GRAMMAR
                         System-Wide Grammar Correction Tool
================================================================================

                                WHAT IS THIS?

Simple Stupid Grammar is a cross-platform background application that provides
system-wide grammar correction using Google's Gemini AI. Just press F9 while
any text is selected, and the app will instantly correct the grammar and
replace your selected text with the corrected version.

Supports Windows and macOS!


================================================================================
                              SYSTEM REQUIREMENTS

• Windows 10/11 OR macOS 10.14+ (Mojave or later)
• Python 3.7 or higher (if installing from source)
• Internet connection for AI processing
• Google API key (free from Google AI Studio)


================================================================================
                              INSTALLATION OPTIONS

    Option 1: Download Pre-built Release (Windows Only)
    ──────────────────────────────────────────────────

1. Go to: https://github.com/tajpouria/simple-stupid-grammer/releases

2. Download the latest "SimpleStupidGrammar_Windows_Distribution.zip"

3. Extract the ZIP file to a folder of your choice
   (e.g., C:\Program Files\SimpleStupidGrammar\)

4. Double-click "install_to_startup.bat" to run the application

5. When prompted, enter your Google API key:
   - Get a free API key from: https://aistudio.google.com/app/apikey
   - Copy and paste the key when prompted
   - The key will be securely saved for future use

6. The app will start and appear in your system tray (look for the "G" icon)

7. To use: Select any text in any application and press F9


    Option 2: Install from Source Code (Windows & macOS)
    ───────────────────────────────────────────────────

    For Windows:
    ────────────
1. Install Python 3.7+ from https://python.org
   ⚠️  IMPORTANT: Check "Add Python to PATH" during installation!

2. Download or clone this repository

3. Open Command Prompt as Administrator in the project folder

4. Run the installation script:
   install.bat

5. Start the application:
   run.bat

6. Enter your Google API key when prompted

    For macOS:
    ──────────
1. Install Python 3.7+ from https://python.org
   OR install via Homebrew: brew install python

2. Download or clone this repository

3. Open Terminal in the project folder

4. Run the installation script:
   ./install.sh

5. Grant accessibility permissions when prompted:
   - Go to System Preferences > Security & Privacy > Privacy
   - Select 'Accessibility' from the left sidebar
   - Click the lock to make changes (enter your password)
   - Add Terminal (or your terminal app) to the list
   - Also add Python if it appears in the list

6. Start the application:
   ./run.sh

7. Enter your Google API key when prompted


================================================================================
                            BUILDING FROM SOURCE

If you want to create your own distribution packages:

    Option 1: Platform-Specific Build
    ─────────────────────────────────

    For Windows:
    ────────────
1. Install Python 3.7+ and ensure it's in PATH
2. Open Command Prompt as Administrator in project folder
3. Run: build.bat
4. Run: create_distribution.bat
5. Share the "SimpleStupidGrammar_Windows_Distribution" folder

    For macOS:
    ──────────
1. Install Python 3.7+ (python.org or Homebrew)
2. Open Terminal in project folder
3. Run: ./build.sh
4. Run: ./create_distribution.sh
5. Share the "SimpleStupidGrammar_macOS_Distribution" folder

    Option 2: Unified Build (Cross-Platform)
    ────────────────────────────────────────
1. Install Python 3.7+ on your platform
2. Run: python3 build_all.py (or python build_all.py on Windows)
3. The script will automatically:
   - Detect your platform
   - Install dependencies
   - Build the appropriate executable/app bundle
   - Create distribution package

Build outputs:
• Windows: Creates .exe and distribution folder
• macOS: Creates .app bundle and distribution folder
• Both include installer scripts and documentation


================================================================================
                                   USAGE

1. Start the application (it will appear in system tray/menu bar with a "G" icon)

2. In any application (Windows or macOS):
   - Select the text you want to correct
   - Press F9 (the hotkey)
   - Wait a moment for AI processing
   - Your text will be automatically replaced with the corrected version

3. Right-click the system tray/menu bar icon for options:
   - Show Window: Display the main control window
   - Restart Monitoring: Restart hotkey monitoring if it stops working
   - Reset API Key: Change your Google API key
   - Exit: Close the application

Platform-specific shortcuts:
• Windows: Ctrl+C (copy), Ctrl+V (paste)
• macOS: Cmd+C (copy), Cmd+V (paste)


================================================================================
                                 TROUBLESHOOTING

    Problem: Hotkey F9 doesn't work
    ─────────────────────────────────
    Windows:
    • Try running as Administrator
    • Check if another app is using F9
    • Restart the monitoring from the tray icon menu

    macOS:
    • Grant accessibility permissions in System Preferences
    • Go to Security & Privacy > Privacy > Accessibility
    • Add Terminal and Python to the allowed apps list
    • Restart the application after granting permissions

    Problem: "Python not found" error
    ──────────────────────────────────
    Windows:
    • Install Python from https://python.org
    • Make sure to check "Add Python to PATH" during installation
    • Restart Command Prompt after installation

    macOS:
    • Install Python from https://python.org
    • Or install via Homebrew: brew install python
    • Make sure python3 command is available in Terminal

    Problem: API key errors
    ───────────────────────
    • Get a fresh API key from: https://aistudio.google.com/app/apikey
    • Right-click tray icon → Reset API Key
    • Restart the application and enter the new key

    Problem: Text not being replaced
    ────────────────────────────────
    • Make sure text is properly selected before pressing F9
    • Check your internet connection
    • Try copying text manually first
    • On macOS: Ensure accessibility permissions are granted

    Problem: App doesn't appear in system tray/menu bar
    ──────────────────────────────────────────────────
    Windows:
    • Check if system tray icons are hidden
    • Look for the "G" icon in the system tray area

    macOS:
    • Look for the "G" icon in the menu bar (top right)
    • Some macOS versions may hide menu bar icons when space is limited


================================================================================
                                 CONFIGURATION

The application uses F9 as the default hotkey. To change this:

1. Open main.py in a text editor
2. Find the line: KEYBOARD_HOTKEY = "f9"
3. Change to one of these alternatives:
   - "ctrl+shift+g"
   - "ctrl+alt+g"  
   - "ctrl+alt+0"
4. Save and restart the application


================================================================================
                               PRIVACY & SECURITY

• Your Google API key is stored securely:
  - Windows: Windows Credential Manager
  - macOS: macOS Keychain
• Only selected text is sent to Google AI for processing
• No other data is collected or transmitted
• The app runs locally and only connects to internet for AI requests


================================================================================
                              PLATFORM NOTES

    Windows Specific:
    ─────────────────
    • System tray integration works out of the box
    • May require running as Administrator for some applications
    • Uses Windows Credential Manager for secure key storage

    macOS Specific:
    ───────────────
    • Menu bar integration (look for "G" icon in top menu bar)
    • Requires accessibility permissions for global hotkeys
    • Uses macOS Keychain for secure key storage
    • Some sandboxed applications may require additional permissions
    • Tested on macOS 10.14+ (Mojave and later)


================================================================================
                                  SUPPORT

Having issues? Here's how to get help:

1. Check the Troubleshooting section above
2. Make sure you have the latest version from GitHub releases
3. For macOS: Ensure accessibility permissions are properly granted
4. Create an issue at: https://github.com/tajpouria/simple-stupid-grammer/issues

When reporting issues, please include:
- Your operating system and version
- Python version
- Error messages (if any)
- Steps to reproduce the problem


================================================================================
                                   LICENSE

MIT License - Feel free to use, modify, and distribute this software.

Copyright (c) 2024 Simple Stupid Grammar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
