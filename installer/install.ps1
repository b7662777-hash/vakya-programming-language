# Vākya Programming Language — Windows Standalone Installer
param(
    [string]$InstallDir = "$env:LOCALAPPDATA\Programs\Vakya",
    [switch]$NoPathUpdate = $false,
    [switch]$AssociateExtension = $true,
    [switch]$CreateDesktopShortcut = $false
)

$ErrorActionPreference = "Stop"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "     VĀKYA PROGRAMMING LANGUAGE — WINDOWS INSTALLER         " -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$sourceDir = Join-Path $scriptDir "..\dist\Vakya"

if (-not (Test-Path $sourceDir)) {
    # Fallback to current script directory if bundled together
    $sourceDir = $scriptDir
}

Write-Host "`n[1/5] Installing Vākya to: $InstallDir ..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $InstallDir "bin") | Out-Null

# Copy binaries, resources, stdlib, runtime, docs, and examples
Copy-Item -Recurse -Force (Join-Path $sourceDir "bin\*") (Join-Path $InstallDir "bin")
if (Test-Path (Join-Path $sourceDir "resources")) {
    Copy-Item -Recurse -Force (Join-Path $sourceDir "resources") $InstallDir
}
Copy-Item -Recurse -Force (Join-Path $sourceDir "std") $InstallDir
Copy-Item -Recurse -Force (Join-Path $sourceDir "runtime") $InstallDir
Copy-Item -Recurse -Force (Join-Path $sourceDir "docs") $InstallDir
Copy-Item -Recurse -Force (Join-Path $sourceDir "examples") $InstallDir
if (Test-Path (Join-Path $sourceDir "README.md")) {
    Copy-Item -Force (Join-Path $sourceDir "README.md") $InstallDir
}

# Copy uninstaller
Copy-Item -Force (Join-Path $scriptDir "uninstall.ps1") $InstallDir

Write-Host "[2/5] Configuring Environment & User PATH ..." -ForegroundColor Yellow
$binDir = Join-Path $InstallDir "bin"
$vakyaExe = Join-Path $binDir "vakya.exe"
$icoPath = Join-Path $InstallDir "resources\vakya.ico"

if (-not $NoPathUpdate) {
    $userPath = [Environment]::GetEnvironmentVariable("Path", [EnvironmentVariableTarget]::User)
    if ($userPath -notlike "*$binDir*") {
        $newPath = if ($userPath) { "$userPath;$binDir" } else { $binDir }
        [Environment]::SetEnvironmentVariable("Path", $newPath, [EnvironmentVariableTarget]::User)
        $env:Path += ";$binDir"
        Write-Host "      Added '$binDir' to User PATH." -ForegroundColor Green
    } else {
        Write-Host "      '$binDir' is already present in User PATH." -ForegroundColor Gray
    }
}

Write-Host "[3/5] Creating Start Menu & Shortcuts ..." -ForegroundColor Yellow
try {
    $wshShell = New-Object -ComObject WScript.Shell
    
    # Start Menu Shortcut
    $startMenuDir = Join-Path $env:APPDATA "Microsoft\Windows\Start Menu\Programs\Vakya"
    New-Item -ItemType Directory -Force -Path $startMenuDir | Out-Null
    
    $shortcutPath = Join-Path $startMenuDir "Vakya.lnk"
    $shortcut = $wshShell.CreateShortcut($shortcutPath)
    $shortcut.TargetPath = $vakyaExe
    $shortcut.WorkingDirectory = $InstallDir
    $shortcut.Description = "Vakya Programming Language Launcher"
    if (Test-Path $icoPath) {
        $shortcut.IconLocation = "$icoPath, 0"
    }
    $shortcut.Save()
    Write-Host "      Created Start Menu shortcut: $shortcutPath" -ForegroundColor Green

    # Optional Desktop Shortcut
    if ($CreateDesktopShortcut) {
        $desktopDir = [Environment]::GetFolderPath("Desktop")
        $deskShortcutPath = Join-Path $desktopDir "Vakya.lnk"
        $deskShortcut = $wshShell.CreateShortcut($deskShortcutPath)
        $deskShortcut.TargetPath = $vakyaExe
        $deskShortcut.WorkingDirectory = $InstallDir
        $deskShortcut.Description = "Vakya Programming Language"
        if (Test-Path $icoPath) {
            $deskShortcut.IconLocation = "$icoPath, 0"
        }
        $deskShortcut.Save()
        Write-Host "      Created Desktop shortcut: $deskShortcutPath" -ForegroundColor Green
    }
} catch {
    Write-Host "      Shortcut creation warning: $($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host "[4/5] Registering File Association (.vakya) ..." -ForegroundColor Yellow
if ($AssociateExtension) {
    try {
        New-Item -Path "HKCU:\Software\Classes\.vakya" -Value "VakyaSourceFile" -Force | Out-Null
        New-Item -Path "HKCU:\Software\Classes\VakyaSourceFile" -Value "Vākya Source File" -Force | Out-Null
        if (Test-Path $icoPath) {
            New-Item -Path "HKCU:\Software\Classes\VakyaSourceFile\DefaultIcon" -Value "$icoPath,0" -Force | Out-Null
        }
        New-Item -Path "HKCU:\Software\Classes\VakyaSourceFile\shell\open\command" -Value "`"$vakyaExe`" `"%1`"" -Force | Out-Null
        New-Item -Path "HKCU:\Software\Classes\VakyaSourceFile\shell\edit\command" -Value "`"$vakyaExe`" --gui `"%1`"" -Force | Out-Null
        Write-Host "      Associated .vakya files with vakya.exe." -ForegroundColor Green
    } catch {
        Write-Host "      File association warning: $($_.Exception.Message)" -ForegroundColor Yellow
    }
}

Write-Host "[5/5] Verifying Installation ..." -ForegroundColor Yellow
if (Test-Path $vakyaExe) {
    $versionOutput = (& $vakyaExe --version) -join "`n"
    Write-Host "      $versionOutput" -ForegroundColor Green
} else {
    Write-Error "Failed to locate $vakyaExe after installation."
}

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "  INSTALLATION COMPLETE!" -ForegroundColor Green
Write-Host "  Launch GUI:     Start Menu -> Vakya  (or double-click vakya.exe)" -ForegroundColor White
Write-Host "  Launch CLI:     Open terminal and run 'vakya <file.vakya>'" -ForegroundColor White
Write-Host "============================================================`n" -ForegroundColor Cyan
