#!/usr/bin/env python3
"""
Simple Stupid Grammar - Windows Desktop App
A system-wide grammar correction tool that fixes highlighted text.
"""

import os
import threading
import time
import json
import sys
import logging
from datetime import datetime
import tkinter as tk
from tkinter import ttk, scrolledtext
import keyboard
import pyperclip
import pyautogui
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# Try different hotkey combinations if ctrl+alt+0 doesn't work:
# KEYBOARD_HOTKEY = "ctrl+shift+g"  # Alternative 1
# KEYBOARD_HOTKEY = "ctrl+alt+g"    # Alternative 2
KEYBOARD_HOTKEY = "f9"  # Alternative 3
# KEYBOARD_HOTKEY = "ctrl+alt+0"


MODEL = "models/gemini-2.0-flash-lite"
PROMPT = "Make the following text grammatically correct: "


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("grammar_app.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)


class SimpleStupidGrammar:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_ui()
        self.is_running = False
        self.hotkey_thread = None

    def setup_ui(self):
        """Setup the application UI"""
        self.root.title("Simple Stupid Grammar")
        self.root.geometry("600x500")
        self.root.resizable(True, True)

        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Title
        title_label = ttk.Label(
            main_frame, text="Simple Stupid Grammar", font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.grid(
            row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10)
        )

        self.status_label = ttk.Label(
            status_frame, text="Stopped", foreground="red", font=("Arial", 12, "bold")
        )
        self.status_label.grid(row=0, column=0)

        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(0, 20))

        self.start_button = ttk.Button(
            button_frame, text="Start Monitoring", command=self.start_monitoring
        )
        self.start_button.grid(row=0, column=0, padx=(0, 10))

        self.stop_button = ttk.Button(
            button_frame,
            text="Stop Monitoring",
            command=self.stop_monitoring,
            state="disabled",
        )
        self.stop_button.grid(row=0, column=1)

        # Instructions
        instructions_frame = ttk.LabelFrame(
            main_frame, text="Instructions", padding="10"
        )
        instructions_frame.grid(
            row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10)
        )

        instructions_text = f"""How to use:
1. Click 'Start Monitoring' to begin
2. Highlight any text anywhere on your computer
3. Press {KEYBOARD_HOTKEY} to fix grammar
4. The highlighted text will be replaced with corrected version

Current hotkey: {KEYBOARD_HOTKEY}"""

        instructions_label = ttk.Label(
            instructions_frame, text=instructions_text, justify=tk.LEFT
        )
        instructions_label.grid(row=0, column=0, sticky=tk.W)

        # Log display
        log_frame = ttk.LabelFrame(main_frame, text="Activity Log", padding="10")
        log_frame.grid(
            row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10)
        )

        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, width=70)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)

        # Bind close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def log_message(self, message):
        """Add message to both log file and UI"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"

        logging.info(message)

        # Update UI log
        self.log_text.insert(tk.END, formatted_message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def start_monitoring(self):
        """Start the hotkey monitoring"""
        if self.is_running:
            return

        self.is_running = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.status_label.config(text="Running", foreground="green")

        self.log_message(f"Started monitoring for {KEYBOARD_HOTKEY}")

        # Start hotkey monitoring in separate thread
        self.hotkey_thread = threading.Thread(target=self.monitor_hotkey, daemon=True)
        self.hotkey_thread.start()

    def stop_monitoring(self):
        """Stop the hotkey monitoring"""
        if not self.is_running:
            return

        self.is_running = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.status_label.config(text="Stopped", foreground="red")

        self.log_message("Stopped monitoring")

        # Unhook the hotkey
        try:
            keyboard.unhook_all_hotkeys()
        except:
            pass

    def monitor_hotkey(self):
        """Monitor for the grammar correction hotkey"""
        try:
            # Register the hotkey
            self.log_message(f"Registering hotkey: {KEYBOARD_HOTKEY}")
            keyboard.add_hotkey(KEYBOARD_HOTKEY, self.fix_grammar)
            self.log_message("Hotkey registered successfully!")

            # Keep the thread alive while monitoring
            while self.is_running:
                time.sleep(0.1)

        except Exception as e:
            self.log_message(f"Error in hotkey monitoring: {str(e)}")
            self.log_message("Try running the app as Administrator!")

    def fix_grammar(self):
        """Main function to fix grammar of highlighted text"""
        try:
            self.log_message("SUCCESS: Grammar fix hotkey pressed!")

            # Store current clipboard content to restore later
            original_clipboard = ""
            try:
                original_clipboard = pyperclip.paste()
            except:
                pass

            # Copy highlighted text to clipboard
            pyautogui.hotkey("ctrl", "c")
            time.sleep(0.1)  # Small delay to ensure copy completes

            # Get the highlighted text
            try:
                highlighted_text = pyperclip.paste()
            except Exception as e:
                self.log_message(f"Error getting clipboard content: {str(e)}")
                return

            if not highlighted_text or highlighted_text.strip() == "":
                self.log_message("No text was highlighted or copied")
                return

            self.log_message(f"Captured text: '{highlighted_text}'")

            # For now, apply simple corrections and add placeholder text
            corrected_text = self.apply_corrections(highlighted_text)

            self.log_message(f"Corrected text: '{corrected_text}'")

            # Replace the highlighted text
            pyperclip.copy(corrected_text)
            time.sleep(0.1)  # Slightly longer delay to ensure clipboard is ready
            pyautogui.hotkey("ctrl", "v")

            # Restore original clipboard after a delay
            def restore_clipboard():
                time.sleep(2)
                try:
                    pyperclip.copy(original_clipboard)
                except:
                    pass

            threading.Thread(target=restore_clipboard, daemon=True).start()

            self.log_message("Text replacement completed!")

        except Exception as e:
            self.log_message(f"Error during grammar fix: {str(e)}")

    def apply_corrections(self, text):
        """Apply grammar corrections to the text"""
        corrected = text

        response = client.models.generate_content(
            model=MODEL,
            contents=PROMPT + text,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema={
                    "required": [
                        "corrected_text",
                    ],
                    "properties": {
                        "corrected_text": {"type": "STRING"},
                    },
                    "type": "OBJECT",
                },
            ),
        )

        corrected = json.loads(response.text)["corrected_text"]

        return corrected

    def on_closing(self):
        """Handle application closing"""
        if self.is_running:
            self.stop_monitoring()
        self.root.destroy()

    def run(self):
        """Start the application"""
        self.log_message("Simple Stupid Grammar started")
        self.log_message("Click 'Start Monitoring' to begin")
        self.root.mainloop()


if __name__ == "__main__":
    try:
        app = SimpleStupidGrammar()
        app.run()
    except KeyboardInterrupt:
        print("Application interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        sys.exit(1)
