@echo off
REM ============================================
REM  PLAYTREE USB Setup - Copy game to USB drive
REM ============================================
echo.
echo  ==========================================
echo   PLAYTREE PORTABLE USB SETUP
echo  ==========================================
echo.

REM Check for admin (needed to rename USB)
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Requesting admin rights for USB rename...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

REM Find the USB drive (named "usb drive")
set USB_DRIVE=
for %%d in (C D E F G H I J K L M N O P Q R S T U V W X Y Z) do (
    if exist "%%d:\" (
        for /f "tokens=3*" %%a in ('vol %%d: 2^>nul ^| findstr /i "Volume in drive"') do (
            if /i "%%a"=="usb" (
                set USB_DRIVE=%%d:
                goto :found
            )
        )
    )
)

REM Also try by label
for /f "tokens=*" %%a in ('wmic logicaldisk where "drivetype=2" get DeviceID^,VolumeName 2^>nul ^| findstr /i "usb drive"') do (
    for %%b in (%%a) do (
        set USB_DRIVE=%%b
        goto :found
    )
)

echo [ERROR] No USB drive named "usb drive" found!
echo Please insert a USB drive and rename it to "usb drive"
pause
exit /b 1

:found
echo [OK] Found USB drive: %USB_DRIVE%
echo.

REM Create folder structure
echo [SETUP] Creating folders...
mkdir "%USB_DRIVE%\PLAYTREE" 2>nul
mkdir "%USB_DRIVE%\PLAYTREE\src" 2>nul
mkdir "%USB_DRIVE%\PLAYTREE\dist" 2>nul

REM Copy game files
echo [SETUP] Copying game files...
copy /Y "%~dp0..\playtree\dist\PLAYTREE.exe" "%USB_DRIVE%\PLAYTREE\dist\PLAYTREE.exe" >nul
copy /Y "%~dp0autorun.inf" "%USB_DRIVE%\autorun.inf" >nul
copy /Y "%~dp0watch_usb.ps1" "%USB_DRIVE%\PLAYTREE\watch_usb.ps1" >nul

REM Copy source files for portability
echo [SETUP] Copying source files...
xcopy /Y /E /Q "%~dp0..\playtree\src" "%USB_DRIVE%\PLAYTREE\src\" >nul
copy /Y "%~dp0..\playtree\config.py" "%USB_DRIVE%\PLAYTREE\config.py" >nul
copy /Y "%~dp0..\playtree\main.py" "%USB_DRIVE%\PLAYTREE\main.py" >nul

REM Copy icon
if exist "%~dp0playtree.ico" (
    copy /Y "%~dp0playtree.ico" "%USB_DRIVE%\PLAYTREE\playtree.ico" >nul
    copy /Y "%~dp0playtree.ico" "%USB_DRIVE%\playtree.ico" >nul
)

REM Set USB icon via registry
echo [SETUP] Setting USB icon...
reg add "HKLM\SYSTEM\CurrentControlSet\Services\usbstor\Enum" /f >nul 2>&1

REM Create desktop.ini for custom icon
echo [.ShellClassInfo] > "%USB_DRIVE%\desktop.ini"
echo IconResource=PLAYTREE\playtree.ico,0 >> "%USB_DRIVE%\desktop.ini"
echo [ViewState] >> "%USB_DRIVE%\desktop.ini"
echo FolderType=Generic >> "%USB_DRIVE%\desktop.ini"

REM Hide desktop.ini
attrib +s +h "%USB_DRIVE%\desktop.ini" 2>nul

REM Rename USB drive label
echo [SETUP] Renaming USB drive to "PLAYTREE PORTABLE USB"...
label %USB_DRIVE% PLAYTREE PORTABLE USB

echo.
echo  ==========================================
echo   SETUP COMPLETE!
echo  ==========================================
echo.
echo  USB Drive: %USB_DRIVE%
echo  Label: PLAYTREE PORTABLE USB
echo  Game: %USB_DRIVE%\PLAYTREE\dist\PLAYTREE.exe
echo.
echo  To use: Plug in USB, game auto-launches.
echo  To stop: Unplug USB, game auto-closes.
echo.
echo  You can also run watch_usb.ps1 for
echo  auto-launch/close on any PC.
echo.

REM Ask to start watcher
set /p START_WATCHER="Start USB watcher now? (Y/N): "
if /i "%START_WATCHER%"=="Y" (
    echo [LAUNCH] Starting USB watcher...
    powershell -ExecutionPolicy Bypass -File "%USB_DRIVE%\PLAYTREE\watch_usb.ps1"
)

pause
