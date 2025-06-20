================================================================================
                            SIMPLE STUPID GRAMMAR
                         System-Wide Grammar Correction Tool
================================================================================

                                WHAT IS THIS?

Simple Stupid Grammar is a Windows background application that provides
system-wide grammar correction using Google's Gemini AI. Just press F9 while
any text is selected, and the app will instantly correct the grammar and
replace your selected text with the corrected version.


================================================================================
                              SYSTEM REQUIREMENTS

• Windows 10, or 11
• Python 3.7 or higher (if installing from source)
• Internet connection for AI processing
• Google API key (free from Google AI Studio)

================================================================================
                              INSTALLATION OPTIONS

    Option 1: Download Pre-built Release (RECOMMENDED)
    ─────────────────────────────────────────────────

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


    Option 2: Install from Source Code
    ──────────────────────────────────

1. Install Python 3.7+ from https://python.org
   ⚠️  IMPORTANT: Check "Add Python to PATH" during installation!

2. Download or clone this repository

3. Open Command Prompt as Administrator in the project folder

4. Run the installation script:
   install.bat

5. Start the application:
   run.bat

6. Enter your Google API key when prompted (get it from: https://aistudio.google.com/app/apikey)

================================================================================
                                   USAGE

1. Start the application (it will appear in system tray with a "G" icon)

2. In any Windows application:
   - Select the text you want to correct
   - Press F9 (the hotkey)
   - Wait a moment for AI processing
   - Your text will be automatically replaced with the corrected version

3. Right-click the system tray icon for options:
   - Show Window: Display the main control window
   - Restart Monitoring: Restart hotkey monitoring if it stops working
   - Reset API Key: Change your Google API key
   - Exit: Close the application

================================================================================
                                 TROUBLESHOOTING

    Problem: Hotkey F9 doesn't work
    ─────────────────────────────────
    • Try running as Administrator
    • Check if another app is using F9
    • Restart the monitoring from the tray icon menu

    Problem: "Python not found" error
    ──────────────────────────────────
    • Install Python from https://python.org
    • Make sure to check "Add Python to PATH" during installation
    • Restart Command Prompt after installation

    Problem: API key errors
    ───────────────────────
    • Get a fresh API key from: https://aistudio.google.com/app/apikey
    • Right-click tray icon → Reset API Key
    • Restart the application and enter the new key

    Problem: Text not being replaced
    ────────────────────────────────
    • Make sure text is properly selected before pressing F9
    • Check your internet connection
    • Try copying text manually (Ctrl+C) before using F9

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

• Your Google API key is stored securely using Windows Credential Manager
• Only selected text is sent to Google AI for processing
• No other data is collected or transmitted
• The app runs locally and only connects to internet for AI requests

================================================================================
                                  SUPPORT

Having issues? Here's how to get help:

1. Check the Troubleshooting section above
2. Make sure you have the latest version from GitHub releases
3. Create an issue at: https://github.com/tajpouria/simple-stupid-grammer/issues

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
