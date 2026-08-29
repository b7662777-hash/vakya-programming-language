# Vākya Programming Language — Windows Standalone Uninstaller
param(
    [string]$InstallDir = "$env:LOCALAPPDATA\Programs\Vakya"
)

$ErrorActionPreference = "SilentlyContinue"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "     VĀKYA PROGRAMMING LANGUAGE — WINDOWS UNINSTALLER       " -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# 1. Remove File Association
Write-Host "`n[1/4] Removing file associations (.vakya) ..." -ForegroundColor Yellow
Remove-Item -Path "HKCU:\Software\Classes\.vakya" -Recurse -Force | Out-Null
Remove-Item -Path "HKCU:\Software\Classes\VakyaSourceFile" -Recurse -Force | Out-Null

# 2. Remove Shortcuts
Write-Host "[2/4] Removing Start Menu and Desktop shortcuts ..." -ForegroundColor Yellow
$startMenuDir = Join-Path $env:APPDATA "Microsoft\Windows\Start Menu\Programs\Vakya"
if (Test-Path $startMenuDir) { Remove-Item -Path $startMenuDir -Recurse -Force | Out-Null }

$desktopShortcut = Join-Path ([Environment]::GetFolderPath("Desktop")) "Vakya.lnk"
if (Test-Path $desktopShortcut) { Remove-Item -Path $desktopShortcut -Force | Out-Null }

# 3. Clean User PATH
Write-Host "[3/4] Removing Vākya from User PATH ..." -ForegroundColor Yellow
$binDir = Join-Path $InstallDir "bin"
$userPath = [Environment]::GetEnvironmentVariable("Path", [EnvironmentVariableTarget]::User)
if ($userPath -like "*$binDir*") {
    $pathParts = $userPath -split ";" | Where-Object { $_ -ne $binDir -and $_ -ne "$binDir\" -and $_ }
    $newPath = $pathParts -join ";"
    [Environment]::SetEnvironmentVariable("Path", $newPath, [EnvironmentVariableTarget]::User)
}

# 4. Remove Files
Write-Host "[4/4] Removing installed files from: $InstallDir ..." -ForegroundColor Yellow
if (Test-Path $InstallDir) {
    Remove-Item -Path $InstallDir -Recurse -Force | Out-Null
}

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "  UNINSTALLATION COMPLETE! Vākya has been removed." -ForegroundColor Green
Write-Host "============================================================`n" -ForegroundColor Cyan
