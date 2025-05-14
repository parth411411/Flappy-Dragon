@echo off
echo Starting Flappy Dragon...
echo Please wait while the game loads...

REM Try to use Python's built-in HTTP server if Python is installed
python -m http.server 8000 2>nul
if %errorlevel% equ 0 goto :eof

REM If Python is not found, try Python3
python3 -m http.server 8000 2>nul
if %errorlevel% equ 0 goto :eof

REM If neither works, try to open the file directly
start "" "index.html"

echo If the game doesn't start automatically, please open index.html in your web browser.
pause 