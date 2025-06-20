@echo off
echo Simple Stupid Grammar - Windows Executable Builder
echo ==================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher from https://python.org
    pause
    exit /b 1
)

echo Running build script...
python build_exe.py

echo.
echo Build process completed. Check above for any errors.
pause 