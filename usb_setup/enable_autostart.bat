@echo off
echo.
echo  ==========================================
echo   PLAYTREE Auto-Start Setup
echo  ==========================================
echo.
echo  This sets up Windows to automatically
echo  run the USB watcher when you log in.
echo.

net session >nul 2>&1
if %errorlevel% neq 0 (
    echo  Requesting admin rights...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

echo  Creating scheduled task...
schtasks /Create /TN "PLAYTREE USB Watcher" /TR "powershell -ExecutionPolicy Bypass -WindowStyle Hidden -File D:\PLAYTREE\watch_usb.ps1" /SC ONLOGON /RL HIGHEST /F

if %errorlevel% equ 0 (
    echo.
    echo  [OK] Task created!
    echo  The USB watcher now starts when you log in.
) else (
    echo.
    echo  [FALLBACK] Adding to Startup folder...
    copy /Y "%~dp0start_watcher.bat" "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\playtree_watcher.bat" >nul
    echo  [OK] Added to Startup folder.
)

echo.
echo  Plug in your USB and the game will auto-launch.
echo  Unplug and the game will auto-close.
echo  ==========================================
pause
