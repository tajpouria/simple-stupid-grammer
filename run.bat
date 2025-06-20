@echo off
echo Starting Simple Stupid Grammar in background...
pythonw.exe main.py
echo App is now running in system tray (background)
timeout /t 3 /nobreak >nul 