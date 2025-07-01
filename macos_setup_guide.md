# macOS Setup Guide for Simple Stupid Grammar

## Required Permissions

On macOS, the app needs special permissions to work properly. Follow these steps:

### 1. Grant Accessibility Permissions

The app needs Accessibility permissions to:
- Listen for the F9 hotkey globally
- Simulate keyboard input to replace text

**Steps:**
1. Open **System Preferences** (or **System Settings** on macOS 13+)
2. Go to **Security & Privacy** → **Privacy** → **Accessibility**
3. Click the **lock icon** to make changes (enter your password)
4. Click the **+** button
5. Navigate to and select:
   - If running from source: `/usr/local/bin/python3` or your Python executable
   - If using the app bundle: `/Applications/Simple Stupid Grammar.app`
6. Make sure the checkbox is **checked**
7. **Restart the application**

### 2. Alternative: Run with sudo (Temporary Solution)

If you're testing from source code, you can temporarily run with sudo:

```bash
sudo python3 main.py
```

**Note:** This is not recommended for regular use, but can help verify the app works.

### 3. Finding Your Python Executable

If you're unsure which Python to add to Accessibility:

```bash
which python3
```

This will show the path (e.g., `/usr/local/bin/python3` or `/opt/homebrew/bin/python3`)

### 4. Terminal Permissions (if running from Terminal)

If running from Terminal, you may also need to grant Terminal accessibility permissions:

1. System Preferences → Security & Privacy → Privacy → Accessibility
2. Add **Terminal** to the list
3. Restart Terminal and try again

## Troubleshooting

### Error: "Must be run as administrator"
- This means Accessibility permissions haven't been granted
- Follow step 1 above to grant permissions
- Make sure to restart the app after granting permissions

### App starts but F9 doesn't work
- Check that no other app is using F9
- Verify Accessibility permissions are granted
- Try a different hotkey by editing `main.py`:
  ```python
  KEYBOARD_HOTKEY = "f10"  # or "cmd+f9", etc.
  ```

### Menu bar icon doesn't appear
- The app might be running in the background
- Check Activity Monitor for "SimpleStupidGrammar" or "Python"
- Try restarting the app

## Security Note

These permissions are required because:
- macOS protects against malicious software that could capture keystrokes
- The app needs to "see" when you press F9 globally
- The app needs to simulate typing to replace your selected text

This is normal and safe for legitimate applications like Simple Stupid Grammar. 