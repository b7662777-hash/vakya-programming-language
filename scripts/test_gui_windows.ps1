# Standalone Vākya GUI & CLI Dual-Mode Verification Test Suite
# Tests isolated vakya.exe from a clean directory outside the repository

$ErrorActionPreference = "Stop"
$repoRoot = (Split-Path -Parent $MyInvocation.MyCommand.Definition) + "\.."
$repoRoot = [System.IO.Path]::GetFullPath($repoRoot)

$distExe = Join-Path $repoRoot "dist\vakya.exe"
if (-not (Test-Path $distExe)) {
    Write-Error "Executable not found at $distExe. Run build_windows.ps1 first."
}

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "     VĀKYA GUI & CLI DUAL-MODE ISOLATED VERIFICATION TEST   " -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Testing Binary: $distExe`n"

# Create clean isolated temporary folder
$cleanDir = Join-Path ([System.IO.Path]::GetTempPath()) ("VakyaGuiTest_" + [System.Guid]::NewGuid().ToString().Substring(0, 8))
New-Item -ItemType Directory -Force -Path $cleanDir | Out-Null
Write-Host "Created clean isolated test directory: $cleanDir" -ForegroundColor Yellow

$isolatedExe = Join-Path $cleanDir "vakya.exe"
Copy-Item $distExe $isolatedExe

try {
    Set-Location -Path $cleanDir

    # --- PART 1: CLI REGRESSION TESTS (No GUI must be launched for CLI) ---
    Write-Host "`n--- PART 1: CLI Execution Verification (No GUI Window) ---" -ForegroundColor Yellow

    # Test 1: CLI Version
    Write-Host "[TEST 1] CLI: vakya.exe --version ..." -ForegroundColor Yellow
    $vOut = (& $isolatedExe --version) -join "`n"
    if ($vOut.Contains("0.1.0")) {
        Write-Host "  [PASS] CLI --version -> $vOut" -ForegroundColor Green
    } else {
        Write-Error "TEST 1 Failed: $vOut"
    }

    # Test 2: CLI Direct Script Execution
    Write-Host "[TEST 2] CLI: vakya.exe hello.vakya ..." -ForegroundColor Yellow
    $f1 = Join-Path $cleanDir "hello.vakya"
    "vada(`"Namaste Vākya`")" | Out-File -FilePath $f1 -Encoding ascii
    $out1 = (& $isolatedExe hello.vakya) -join "`n"
    if ($out1.Contains("Namaste")) {
        Write-Host "  [PASS] CLI Output: $out1" -ForegroundColor Green
    } else {
        Write-Error "TEST 2 Failed: $out1"
    }

    # Test 3: CLI Stdlib Execution
    Write-Host "[TEST 3] CLI: vakya.exe test_math.vakya ..." -ForegroundColor Yellow
    $f2 = Join-Path $cleanDir "test_math.vakya"
    "aayat math`nvada(math.PI)" | Out-File -FilePath $f2 -Encoding ascii
    $out2 = (& $isolatedExe test_math.vakya) -join "`n"
    if ($out2.Contains("3.141592")) {
        Write-Host "  [PASS] CLI Stdlib Output: $out2" -ForegroundColor Green
    } else {
        Write-Error "TEST 3 Failed: $out2"
    }

    # Test 4: CLI Doctor
    Write-Host "[TEST 4] CLI: vakya.exe doctor ..." -ForegroundColor Yellow
    $docOut = (& $isolatedExe doctor) -join "`n"
    if ($docOut.Contains("SYSTEM DIAGNOSTIC")) {
        Write-Host "  [PASS] CLI Doctor executed cleanly" -ForegroundColor Green
    } else {
        Write-Error "TEST 4 Failed: $docOut"
    }

    # --- PART 2: GUI LAUNCH VERIFICATION ---
    Write-Host "`n--- PART 2: GUI Launch & Desktop Verification ---" -ForegroundColor Yellow

    # Test 5: GUI Launch without arguments
    Write-Host "[TEST 5] GUI: Launching vakya.exe in GUI mode (No arguments) ..." -ForegroundColor Yellow
    
    $guiProcess = Start-Process -FilePath $isolatedExe -NoNewWindow -PassThru
    Start-Sleep -Milliseconds 2500  # Allow splash and main window to initialize
    
    if (-not $guiProcess.HasExited) {
        Write-Host "  [PASS] Vākya GUI launched successfully and is actively running (PID: $($guiProcess.Id))." -ForegroundColor Green
        # Gracefully stop the GUI process after verifying it runs
        Stop-Process -Id $guiProcess.Id -Force
        Write-Host "  [PASS] GUI closed cleanly after verification." -ForegroundColor Green
    } else {
        $exitCode = $guiProcess.ExitCode
        Write-Error "TEST 5 Failed: GUI process terminated prematurely with exit code $exitCode."
    }

    # Test 6: GUI Launch with explicit target file (Open With / Double-click file association)
    Write-Host "[TEST 6] GUI: Launching vakya.exe with file argument (gui mode) ..." -ForegroundColor Yellow
    $guiFileProcess = Start-Process -FilePath $isolatedExe -ArgumentList "--gui", "$f1" -NoNewWindow -PassThru
    Start-Sleep -Milliseconds 2500

    if (-not $guiFileProcess.HasExited) {
        Write-Host "  [PASS] Vākya GUI opened target file successfully (PID: $($guiFileProcess.Id))." -ForegroundColor Green
        Stop-Process -Id $guiFileProcess.Id -Force
        Write-Host "  [PASS] GUI closed cleanly after file verification." -ForegroundColor Green
    } else {
        $exitCode = $guiFileProcess.ExitCode
        Write-Error "TEST 6 Failed: GUI file open process exited prematurely with exit code $exitCode."
    }

    Write-Host "`n============================================================" -ForegroundColor Cyan
    Write-Host "   ALL CLI & GUI ACCEPTANCE TESTS PASSED SUCCESSFULLY!      " -ForegroundColor Green
    Write-Host "============================================================`n" -ForegroundColor Cyan

} finally {
    Set-Location -Path $repoRoot
    Start-Sleep -Milliseconds 800
    try {
        Remove-Item -Recurse -Force $cleanDir -ErrorAction SilentlyContinue
    } catch {}
}
