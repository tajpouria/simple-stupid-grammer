@echo off
echo Creating Distribution Package...
echo =================================
echo.

REM Check if executable exists
if not exist "dist\SimpleStupidGrammar.exe" (
    echo ERROR: SimpleStupidGrammar.exe not found in dist folder
    echo Please run build.bat first to create the executable
    pause
    exit /b 1
)

REM Create distribution folder
set "DIST_FOLDER=SimpleStupidGrammar_Windows_Distribution"
if exist "%DIST_FOLDER%" (
    echo Removing existing distribution folder...
    rmdir /s /q "%DIST_FOLDER%"
)

echo Creating distribution folder: %DIST_FOLDER%
mkdir "%DIST_FOLDER%"

REM Copy files
echo Copying executable...
copy "dist\SimpleStupidGrammar.exe" "%DIST_FOLDER%\"

echo Copying installer scripts...
copy "install_to_startup.bat" "%DIST_FOLDER%\"
copy "remove_from_startup.bat" "%DIST_FOLDER%\"
copy "README.txt" "%DIST_FOLDER%\"

echo.
echo ✓ Distribution package created successfully!
echo.
echo Distribution folder: %DIST_FOLDER%
echo.
echo Contents:
echo - SimpleStupidGrammar.exe (main application)
echo - install_to_startup.bat (startup installer)
echo - remove_from_startup.bat (startup remover)
echo - README.txt (instructions)
echo.
echo You can now zip this folder and share it with others!
echo The recipient just needs to run install_to_startup.bat
echo.
pause 