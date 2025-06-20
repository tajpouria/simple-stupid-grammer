@echo off
REM Startup script for Simple Stupid Grammar
REM Copy this file to: %APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
REM to run automatically when Windows starts

cd /d "%~dp0"
pythonw.exe main.py 