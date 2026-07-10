@echo off
title PLAYTREE USB Watcher
echo.
echo  ==========================================
echo   PLAYTREE USB Watcher
echo  ==========================================
echo.
echo  Plug in your USB drive and the game
echo  will auto-launch. Unplug to auto-close.
echo.
echo  Press Ctrl+C to stop watching.
echo.
powershell -ExecutionPolicy Bypass -File "%~dp0watch_usb.ps1"
