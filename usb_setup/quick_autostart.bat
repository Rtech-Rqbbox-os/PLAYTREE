@echo off
echo.
echo  Adding PLAYTREE watcher to Windows Startup...
echo.

REM Copy watcher to Startup folder (runs every login)
mkdir "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup" 2>nul
copy /Y "%~dp0start_watcher.bat" "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\playtree_watcher.bat" >nul

echo  [OK] Done!
echo.
echo  The watcher now starts automatically when you
echo  log into Windows. Plug in USB and game launches.
echo.
pause
