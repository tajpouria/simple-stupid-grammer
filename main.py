#!/usr/bin/env python3
"""
Simple Stupid Grammar - Windows Background App
A system-wide grammar correction tool that runs in the system tray.
"""

import threading
import time
import json
import sys
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import keyboard
import pyperclip
import pyautogui
from google import genai
from google.genai import types
import pystray
from PIL import Image, ImageDraw
import io
import keyring


# Application constants
SERVICE_NAME = "SimpleStupidGrammar"
CREDENTIAL_NAME = "GoogleAPIKey"

# Try different hotkey combinations if ctrl+alt+0 doesn't work:
# KEYBOARD_HOTKEY = "ctrl+shift+g"  # Alternative 1
# KEYBOARD_HOTKEY = "ctrl+alt+g"    # Alternative 2
KEYBOARD_HOTKEY = "f9"  # Alternative 3
# KEYBOARD_HOTKEY = "ctrl+alt+0"

MODEL = "models/gemini-2.0-flash-lite"
PROMPT = "Make the following text grammatically correct: "


class SimpleStupidGrammar:
    def __init__(self):
        try:
            print("Starting app initialization...")
            # Get Google API key before initializing the client
            api_key = self.get_google_api_key()
            print(f"Got API key: {'Yes' if api_key else 'No'}")
            if not api_key:
                print("ERROR: No Google API key provided!")
                sys.exit(1)
            
            # Initialize the client with the API key
            global client
            client = genai.Client(api_key=api_key)
            print("Client initialized successfully")
            
            self.root = tk.Tk()
            self.setup_ui()
            self.is_running = False
            self.hotkey_thread = None
            self.tray_icon = None
            self.hidden = False  # Start visible by default
            
            # Keep the window visible on startup
            # self.root.withdraw()  # Removed - keep window visible
            
            # Create system tray icon
            self.setup_tray()
            
            # Auto-start monitoring
            self.root.after(100, self.start_monitoring)
            
        except Exception as e:
            print(f"ERROR: Failed to initialize application: {str(e)}")
            import traceback
            traceback.print_exc()
            raise

    def get_google_api_key(self):
        """Get Google API key from stored credentials or user input"""
        print("get_google_api_key called")
        try:
            # First, try to get from stored credentials
            print("Checking stored credentials...")
            stored_key = keyring.get_password(SERVICE_NAME, CREDENTIAL_NAME)
            if stored_key:
                print("Found stored key")
                return stored_key
            
            print("No stored key found, prompting user...")
            # If no stored key, prompt user for the key
            return self.prompt_for_api_key()
            
        except Exception as e:
            print(f"Error getting API key: {str(e)}")
            return self.prompt_for_api_key()

    def prompt_for_api_key(self):
        """Prompt user for Google API key using a dialog"""
        try:
            # Create a temporary root window for the dialog if main window doesn't exist yet
            if not hasattr(self, 'root') or not self.root:
                temp_root = tk.Tk()
                temp_root.withdraw()  # Hide the temp window
                parent = temp_root
            else:
                parent = self.root
            
            # Show dialog to get API key
            api_key = simpledialog.askstring(
                "Google API Key Required",
                "Please enter your Google API Key:\n\n"
                "You can get one from:\n"
                "https://aistudio.google.com/app/apikey\n\n"
                "Enter your API key:",
                parent=parent,
                show='*'  # Hide the input like a password
            )
            
            if api_key and api_key.strip():
                api_key = api_key.strip()
                # Store the key securely
                try:
                    keyring.set_password(SERVICE_NAME, CREDENTIAL_NAME, api_key)
                    messagebox.showinfo(
                        "Success", 
                        "API key saved successfully!\n"
                        "The app will remember this key for future use.",
                        parent=parent
                    )
                except Exception as e:
                    messagebox.showwarning(
                        "Warning", 
                        f"API key will be used but couldn't be saved: {str(e)}\n"
                        "You may need to enter it again next time.",
                        parent=parent
                    )
                
                # Clean up temp window if we created one
                if not hasattr(self, 'root') or not self.root:
                    temp_root.destroy()
                
                return api_key
            else:
                # Clean up temp window if we created one
                if not hasattr(self, 'root') or not self.root:
                    temp_root.destroy()
                
                # User cancelled or entered empty key
                messagebox.showerror(
                    "Error", 
                    "Google API key is required for the app to work!\n"
                    "Please restart the app and provide a valid API key.",
                    parent=parent if hasattr(self, 'root') and self.root else None
                )
                return None
                
        except Exception as e:
            print(f"Error prompting for API key: {str(e)}")
            return None

    def reset_api_key(self):
        """Reset the stored API key (for testing or changing keys)"""
        try:
            keyring.delete_password(SERVICE_NAME, CREDENTIAL_NAME)
            messagebox.showinfo("Success", "API key has been reset.\nRestart the app to enter a new one.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to reset API key: {str(e)}")

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
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Restart Monitoring", self.restart_monitoring),
            pystray.MenuItem("Reset API Key", self.reset_api_key),
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

    def setup_ui(self):
        """Setup the application UI"""
        self.root.title("Simple Stupid Grammar")
        self.root.geometry("600x600")
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

        # Instructions
        instructions_frame = ttk.LabelFrame(
            main_frame, text="Instructions", padding="10"
        )
        instructions_frame.grid(
            row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10)
        )

        instructions_text = f"""How to use:
1. App runs in background by default (check system tray)
2. Highlight any text anywhere on your computer
3. Press {KEYBOARD_HOTKEY} to fix grammar
4. The highlighted text will be replaced with corrected version
5. Right-click tray icon for options
6. This window is only for monitoring - app works in background

Current hotkey: {KEYBOARD_HOTKEY}"""

        instructions_label = ttk.Label(
            instructions_frame, text=instructions_text, justify=tk.LEFT
        )
        instructions_label.grid(row=0, column=0, sticky=(tk.W, tk.N))

        # Configure grid weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        instructions_frame.columnconfigure(0, weight=1)
        instructions_frame.rowconfigure(0, weight=1)

        # Bind close event to hide window
        self.root.protocol("WM_DELETE_WINDOW", self.hide_window)

    def quit_app(self, icon=None, item=None):
        """Completely exit the application"""
        if self.is_running:
            self.stop_monitoring()
        if self.tray_icon:
            self.tray_icon.stop()
        self.root.quit()
        self.root.destroy()
        sys.exit(0)

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

        # Show notification
        try:
            if self.tray_icon:
                self.tray_icon.notify("Simple Stupid Grammar", f"Monitoring started! Press {KEYBOARD_HOTKEY} to fix grammar.")
        except:
            pass

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

        # Show notification
        try:
            if self.tray_icon:
                self.tray_icon.notify("Simple Stupid Grammar", "Monitoring stopped.")
        except:
            pass

        # Unhook the hotkey
        try:
            keyboard.unhook_all_hotkeys()
        except:
            pass

    def monitor_hotkey(self):
        """Monitor for the grammar correction hotkey"""
        try:
            # Register the hotkey
            keyboard.add_hotkey(KEYBOARD_HOTKEY, self.fix_grammar)

            # Keep the thread alive while monitoring
            while self.is_running:
                time.sleep(0.1)

        except Exception as e:
            # Show error notification instead of logging
            try:
                if self.tray_icon:
                    self.tray_icon.notify("Error", f"Hotkey error: {str(e)}. Try running as Administrator!")
            except:
                pass

    def fix_grammar(self):
        """Main function to fix grammar of highlighted text"""
        try:
            # Store current clipboard content to restore later
            original_clipboard = ""
            try:
                original_clipboard = pyperclip.paste()
            except:
                pass

            # Copy highlighted text to clipboard (use appropriate modifier key for platform)
            if sys.platform == "darwin":  # macOS
                pyautogui.hotkey("cmd", "c")
            else:  # Windows/Linux
                pyautogui.hotkey("ctrl", "c")
            # Longer delay on macOS as it can be slower with clipboard operations
            time.sleep(0.2 if sys.platform == "darwin" else 0.1)

            # Get the highlighted text
            try:
                highlighted_text = pyperclip.paste()
            except Exception as e:
                return

            if not highlighted_text or highlighted_text.strip() == "":
                return

            # Apply corrections
            corrected_text = self.apply_corrections(highlighted_text)

            # Replace the highlighted text
            pyperclip.copy(corrected_text)
            # Longer delay on macOS to ensure clipboard is ready
            time.sleep(0.2 if sys.platform == "darwin" else 0.1)
            if sys.platform == "darwin":  # macOS
                pyautogui.hotkey("cmd", "v")
            else:  # Windows/Linux
                pyautogui.hotkey("ctrl", "v")

            # Restore original clipboard after a delay
            def restore_clipboard():
                time.sleep(2)
                try:
                    pyperclip.copy(original_clipboard)
                except:
                    pass

            threading.Thread(target=restore_clipboard, daemon=True).start()

            # Show notification
            try:
                if self.tray_icon:
                    self.tray_icon.notify("Grammar Fixed!", "Text has been corrected and replaced.")
            except:
                pass

        except Exception as e:
            # Show error notification instead of logging
            try:
                if self.tray_icon:
                    self.tray_icon.notify("Error", f"Grammar fix failed: {str(e)}")
            except:
                pass

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

    def run(self):
        """Start the application"""        
        # Show initial notification
        try:
            if self.tray_icon:
                self.tray_icon.notify("Simple Stupid Grammar Started!", "App is running in background. Right-click tray icon for options.")
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
        print(f"ERROR: Application failed to start: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
        sys.exit(1)
