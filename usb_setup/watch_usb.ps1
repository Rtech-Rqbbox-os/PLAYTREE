# PLAYTREE USB Watcher v2
# Detects USB by looking for PLAYTREE\PLAYTREE.exe on any removable drive
# Auto-launches when USB plugged in, auto-closes when removed

$PROCESS_NAME = "PLAYTREE"
$FOLDER_NAME = "PLAYTREE"
$gameLaunched = $false
$lastDriveState = @()

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  PLAYTREE USB Watcher v2" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

function Find-PlayTreeDrive {
    $drives = Get-WmiObject Win32_LogicalDisk | Where-Object { $_.DriveType -eq 2 }
    foreach ($drive in $drives) {
        $exePath = Join-Path $drive.DeviceID "$FOLDER_NAME\dist\PLAYTREE.exe"
        $exePathAlt = Join-Path $drive.DeviceID "$FOLDER_NAME\PLAYTREE.exe"
        if (Test-Path $exePath) {
            return @{ Drive = $drive.DeviceID; Exe = $exePath }
        }
        if (Test-Path $exePathAlt) {
            return @{ Drive = $drive.DeviceID; Exe = $exePathAlt }
        }
    }
    return $null
}

function Get-RemovableDrives {
    return Get-WmiObject Win32_LogicalDisk | Where-Object { $_.DriveType -eq 2 } | Select-Object -ExpandProperty DeviceID
}

function Start-PlayTree {
    param([string]$ExePath)
    $workingDir = Split-Path $ExePath
    Write-Host "[LAUNCH] Starting PLAYTREE from $ExePath ..." -ForegroundColor Green
    Start-Process -FilePath $ExePath -WorkingDirectory $workingDir
    Start-Sleep -Seconds 2
    $proc = Get-Process -Name $PROCESS_NAME -ErrorAction SilentlyContinue
    if ($proc) {
        Write-Host "[OK] Game running (PID: $($proc.Id))" -ForegroundColor Green
    } else {
        Write-Host "[WARN] Game process not found after launch" -ForegroundColor Yellow
    }
}

function Stop-PlayTree {
    $proc = Get-Process -Name $PROCESS_NAME -ErrorAction SilentlyContinue
    if ($proc) {
        Write-Host "[CLOSE] Stopping PLAYTREE (PID: $($proc.Id)) ..." -ForegroundColor Red
        Stop-Process -Name $PROCESS_NAME -Force -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 1
        $still = Get-Process -Name $PROCESS_NAME -ErrorAction SilentlyContinue
        if ($still) {
            Write-Host "[FORCE] Force killing PLAYTREE ..." -ForegroundColor Red
            Stop-Process -Name $PROCESS_NAME -Force -ErrorAction SilentlyContinue
        }
        Write-Host "[OK] Game closed." -ForegroundColor Red
    }
}

# Check initial state
$found = Find-PlayTreeDrive
$gameRunning = Get-Process -Name $PROCESS_NAME -ErrorAction SilentlyContinue
if ($found -and $gameRunning) {
    Write-Host "[INFO] USB already connected and game is running." -ForegroundColor Yellow
    $gameLaunched = $true
} elseif ($found) {
    Write-Host "[INFO] USB found on $($found.Drive) but game not running." -ForegroundColor Yellow
    $gameLaunched = $false
} else {
    Write-Host "[WAIT] No USB with PLAYTREE detected. Watching..." -ForegroundColor Gray
}

Write-Host ""

# Main loop - poll every 1 second
while ($true) {
    try {
        $usb = Find-PlayTreeDrive
        $running = Get-Process -Name $PROCESS_NAME -ErrorAction SilentlyContinue

        if ($usb -and -not $running -and -not $gameLaunched) {
            # USB plugged in, game not running -> launch
            Start-PlayTree -ExePath $usb.Exe
            $gameLaunched = $true
        }
        elseif ($usb -and $running -and -not $gameLaunched) {
            # USB present, game running but we didn't launch it -> track it
            Write-Host "[INFO] Game already running, tracking..." -ForegroundColor Yellow
            $gameLaunched = $true
        }
        elseif (-not $usb -and $gameLaunched) {
            # USB removed -> close game
            Write-Host "[REMOVE] USB disconnected!" -ForegroundColor Red
            Stop-PlayTree
            $gameLaunched = $false
            Write-Host "[WAIT] Waiting for USB to be plugged back in..." -ForegroundColor Gray
        }
        elseif (-not $usb -and -not $gameLaunched) {
            # No USB, game not running -> waiting
        }
        elseif ($usb -and $running -and $gameLaunched) {
            # Everything normal, USB connected and game running
        }
        elseif ($usb -and -not $running -and $gameLaunched) {
            # USB present, game was closed manually -> reset
            Write-Host "[INFO] Game was closed. Ready to relaunch on next USB insert." -ForegroundColor Yellow
            $gameLaunched = $false
        }
    } catch {
        Write-Host "[ERROR] $($_.Exception.Message)" -ForegroundColor Yellow
    }

    Start-Sleep -Seconds 1
}
