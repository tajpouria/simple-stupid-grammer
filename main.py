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
from tkinter import ttk, scrolledtext, messagebox
import keyboard
import pyperclip
import pyautogui
from google import genai
from google.genai import types
from dotenv import load_dotenv
import pystray
from PIL import Image, ImageDraw
import io

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
        logging.StreamHandler(),
    ],
)


class SimpleStupidGrammar:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_ui()
        self.is_running = False
        self.hotkey_thread = None
        self.tray_icon = None
        self.hidden = False
        
        # Create system tray icon
        self.setup_tray()
        
        # Auto-start monitoring
        self.root.after(100, self.start_monitoring)

    def create_tray_icon(self):
        """Create a simple icon for the system tray"""
        # Create a simple icon using PIL
        width = 64
        height = 64
        
        # Create an image with transparent background
        image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Draw a simple "G" icon for Grammar
        draw.rectangle([10, 10, width-10, height-10], fill='blue', outline='darkblue', width=2)
        draw.text((width//2-8, height//2-8), "G", fill='white', font_size=24)
        
        return image

    def setup_tray(self):
        """Setup system tray icon"""
        icon_image = self.create_tray_icon()
        
        # Create context menu for tray icon
        menu = pystray.Menu(
            pystray.MenuItem("Show Window", self.show_window),
            pystray.MenuItem("Hide Window", self.hide_window),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Start Monitoring", self.start_monitoring, enabled=lambda item: not self.is_running),
            pystray.MenuItem("Stop Monitoring", self.stop_monitoring, enabled=lambda item: self.is_running),
            pystray.MenuItem("Restart Monitoring", self.restart_monitoring),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Exit", self.quit_app)
        )
        
        self.tray_icon = pystray.Icon("SimpleStupidGrammar", icon_image, "Simple Stupid Grammar", menu)
        
        # Start tray icon in a separate thread
        self.tray_thread = threading.Thread(target=self.tray_icon.run, daemon=True)
        self.tray_thread.start()

    def show_window(self, icon=None, item=None):
        """Show the main window"""
        self.root.deiconify()
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after_idle(self.root.attributes, '-topmost', False)
        self.hidden = False

    def hide_window(self, icon=None, item=None):
        """Hide the main window to system tray"""
        self.root.withdraw()
        self.hidden = True

    def minimize_to_tray(self):
        """Minimize to system tray instead of taskbar"""
        self.hide_window()

    def setup_ui(self):
        """Setup the application UI"""
        self.root.title("Simple Stupid Grammar")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Set window icon (optional)
        try:
            # Convert PIL image to PhotoImage for tkinter
            icon_image = self.create_tray_icon()
            icon_image = icon_image.resize((32, 32))
            
            # Convert to bytes for tkinter
            with io.BytesIO() as output:
                icon_image.save(output, format="PNG")
                icon_data = output.getvalue()
            
            # This might not work on all systems, so we'll try/except it
            photo = tk.PhotoImage(data=icon_data)
            self.root.iconphoto(False, photo)
        except:
            pass  # If icon setting fails, just continue without it

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
            status_frame, text="Starting...", foreground="orange", font=("Arial", 12, "bold")
        )
        self.status_label.grid(row=0, column=0)

        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(0, 20))

        self.restart_button = ttk.Button(
            button_frame, text="Restart Monitoring", command=self.restart_monitoring
        )
        self.restart_button.grid(row=0, column=0, padx=(0, 10))

        self.hide_button = ttk.Button(
            button_frame, text="Hide to Tray", command=self.hide_window
        )
        self.hide_button.grid(row=0, column=1)

        # Instructions
        instructions_frame = ttk.LabelFrame(
            main_frame, text="Instructions", padding="10"
        )
        instructions_frame.grid(
            row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10)
        )

        instructions_text = f"""How to use:
1. App starts monitoring automatically
2. Highlight any text anywhere on your computer
3. Press {KEYBOARD_HOTKEY} to fix grammar
4. The highlighted text will be replaced with corrected version
5. Use 'Restart Monitoring' to reset if needed
6. Click 'Hide to Tray' or close window to run in background
7. Right-click tray icon for options

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

        # Bind close event to minimize to tray instead of closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_window_close)
        
        # Bind minimize event
        self.root.bind('<Unmap>', self.on_minimize)

    def on_minimize(self, event):
        """Handle window minimize event"""
        if event.widget == self.root and self.root.state() == 'iconic':
            self.minimize_to_tray()

    def on_window_close(self):
        """Handle window close event - minimize to tray instead of exiting"""
        if messagebox.askyesno("Hide to Tray", 
                              "Do you want to hide the application to the system tray?\n\n"
                              "Click 'Yes' to hide to tray (app keeps running)\n"
                              "Click 'No' to completely exit the application"):
            self.hide_window()
        else:
            self.quit_app()

    def quit_app(self, icon=None, item=None):
        """Completely exit the application"""
        if self.is_running:
            self.stop_monitoring()
        if self.tray_icon:
            self.tray_icon.stop()
        self.root.quit()
        self.root.destroy()
        sys.exit(0)

    def log_message(self, message):
        """Add message to UI log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"

        # Log to console
        logging.info(message)

        # Update UI log only if window exists and is not destroyed
        try:
            if self.root and self.root.winfo_exists():
                self.log_text.insert(tk.END, formatted_message + "\n")
                self.log_text.see(tk.END)
                self.root.update_idletasks()
        except tk.TclError:
            pass  # Window might be destroyed, just continue

    def start_monitoring(self, icon=None, item=None):
        """Start the hotkey monitoring"""
        if self.is_running:
            return

        self.is_running = True
        try:
            self.restart_button.config(state="disabled")
            self.status_label.config(text="Running", foreground="green")
        except tk.TclError:
            pass  # Window might be hidden

        self.log_message(f"Started monitoring for {KEYBOARD_HOTKEY}")

        # Start hotkey monitoring in separate thread
        self.hotkey_thread = threading.Thread(target=self.monitor_hotkey, daemon=True)
        self.hotkey_thread.start()

    def restart_monitoring(self, icon=None, item=None):
        """Restart the hotkey monitoring"""
        if self.is_running:
            self.stop_monitoring()
        self.start_monitoring()

    def stop_monitoring(self, icon=None, item=None):
        """Stop the hotkey monitoring"""
        if not self.is_running:
            return

        self.is_running = False
        try:
            self.restart_button.config(state="normal")
            self.status_label.config(text="Stopped", foreground="red")
        except tk.TclError:
            pass  # Window might be hidden

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
        """Handle application closing (deprecated - use quit_app instead)"""
        self.quit_app()

    def run(self):
        """Start the application"""
        self.log_message("Simple Stupid Grammar started")
        self.log_message("Monitoring will start automatically...")
        self.log_message("You can minimize this window to system tray")
        
        # Show initial notification
        try:
            if self.tray_icon:
                self.tray_icon.notify("Simple Stupid Grammar is running!", "The app is ready to correct your grammar!")
        except:
            pass
            
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
