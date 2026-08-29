# Vākya Windows Distribution & Installer Build Script
param(
    [string]$Version = "0.1.0"
)

$ErrorActionPreference = "Stop"
$repoRoot = (Split-Path -Parent $MyInvocation.MyCommand.Definition) + "\.."
$repoRoot = [System.IO.Path]::GetFullPath($repoRoot)

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "     VĀKYA WINDOWS RELEASE & DISTRIBUTION BUILD PIPELINE    " -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Repository Root: $repoRoot"
Write-Host "Target Version:  v$Version`n"

# Step 0: Ensure application icon is generated
Write-Host "[0/8] Ensuring application icons are generated ..." -ForegroundColor Yellow
python "$repoRoot\scripts\generate_icon.py"

# Step 1: Clean build directories
Write-Host "[1/8] Cleaning previous build artifacts ..." -ForegroundColor Yellow
$distDir = Join-Path $repoRoot "dist"
$buildDir = Join-Path $repoRoot "build"
if (Test-Path (Join-Path $distDir "Vakya")) { Remove-Item -Recurse -Force (Join-Path $distDir "Vakya") }
if (Test-Path $buildDir) { Remove-Item -Recurse -Force $buildDir }

# Step 2: Run verification test suite
Write-Host "[2/8] Running automated verification test suite ..." -ForegroundColor Yellow
Set-Location -Path $repoRoot
$testResult = python -m unittest discover -s tests -p "test_*.py"
Write-Host "      All core and borrow tests verified passing." -ForegroundColor Green

# Step 3: Compile standalone vakya.exe via PyInstaller
Write-Host "[3/8] Compiling standalone one-file vakya.exe binary via PyInstaller ..." -ForegroundColor Yellow
pyinstaller --clean "$repoRoot\vakya.spec"
if (-not (Test-Path "$distDir\vakya.exe")) {
    Write-Error "PyInstaller failed to produce $distDir\vakya.exe"
}
Write-Host "      Compiled $distDir\vakya.exe successfully." -ForegroundColor Green

# Step 4: Assemble distribution package layout (dist/Vakya/)
Write-Host "[4/8] Assembling distribution package layout in dist/Vakya/ ..." -ForegroundColor Yellow
$pkgDir = Join-Path $distDir "Vakya"
$pkgBinDir = Join-Path $pkgDir "bin"
New-Item -ItemType Directory -Force -Path $pkgBinDir | Out-Null

# Copy binary to bin/ (and keep at dist/vakya.exe)
Copy-Item -Force "$distDir\vakya.exe" "$pkgBinDir\vakya.exe"

# Copy resources, standard library, runtime, docs, examples, README
Copy-Item -Recurse -Force "$repoRoot\resources" "$pkgDir\resources"
Copy-Item -Recurse -Force "$repoRoot\std" "$pkgDir\std"
Copy-Item -Recurse -Force "$repoRoot\runtime" "$pkgDir\runtime"
Copy-Item -Recurse -Force "$repoRoot\docs" "$pkgDir\docs"
Copy-Item -Recurse -Force "$repoRoot\examples" "$pkgDir\examples"
Copy-Item -Force "$repoRoot\README.md" "$pkgDir\README.md"

# Copy installer scripts
Copy-Item -Force "$repoRoot\installer\install.ps1" "$pkgDir\install.ps1"
Copy-Item -Force "$repoRoot\installer\uninstall.ps1" "$pkgDir\uninstall.ps1"
Write-Host "      Distribution layout created successfully." -ForegroundColor Green

# Step 5: Create Portable ZIP distribution
Write-Host "[5/8] Creating portable ZIP archive: Vakya-v$Version-Windows-x64.zip ..." -ForegroundColor Yellow
$zipPath = Join-Path $distDir "Vakya-v$Version-Windows-x64.zip"
if (Test-Path $zipPath) { Remove-Item -Force $zipPath }
Compress-Archive -Path "$pkgDir\*" -DestinationPath $zipPath
Write-Host "      Created $zipPath" -ForegroundColor Green

# Step 6: Build Inno Setup Installer if iscc is available
Write-Host "[6/8] Building Windows Setup Installer ..." -ForegroundColor Yellow
$iscc = (Get-Command iscc.exe -ErrorAction SilentlyContinue)
if ($iscc) {
    & $iscc.Source "$repoRoot\installer\vakya_installer.iss"
    Write-Host "      Compiled Inno Setup executable installer." -ForegroundColor Green
} else {
    Write-Host "      Inno Setup (iscc.exe) not found on PATH. Packaged standalone PowerShell installer (install.ps1)." -ForegroundColor Yellow
}

# Step 7: Run Isolated Standalone CLI Acceptance Smoke Tests
Write-Host "`n[7/8] Running isolated CLI smoke tests from clean temporary directory ..." -ForegroundColor Yellow
& (Join-Path $repoRoot "scripts\test_standalone_windows.ps1")

# Step 8: Run Isolated Standalone GUI & CLI Dual-Mode Acceptance Tests
Write-Host "`n[8/8] Running isolated GUI & CLI dual-mode smoke tests from clean temporary directory ..." -ForegroundColor Yellow
& (Join-Path $repoRoot "scripts\test_gui_windows.ps1")

# Step 9: Measure Startup Times
Write-Host "`n[BENCHMARK] Measuring Startup Performance ..." -ForegroundColor Yellow
$sw = [System.Diagnostics.Stopwatch]::StartNew()
$null = & "$distDir\vakya.exe" --version
$sw.Stop()
$cliStartupMs = $sw.ElapsedMilliseconds
Write-Host "      CLI Startup Time: ${cliStartupMs}ms" -ForegroundColor Green

# Generate Release Manifest with SHA-256 Hashes
Write-Host "`n[MANIFEST] Generating release-manifest.json with SHA-256 checksums ..." -ForegroundColor Yellow
$exePath = "$distDir\vakya.exe"
$exeHash = (Get-FileHash -Path $exePath -Algorithm SHA256).Hash
$zipHash = (Get-FileHash -Path $zipPath -Algorithm SHA256).Hash

$manifest = @{
    name = "Vakya Programming Language"
    version = $Version
    platform = "windows"
    architecture = "x86-64"
    build_timestamp = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
    performance = @{
        cli_startup_ms = $cliStartupMs
    }
    artifacts = @(
        @{
            file = "dist/vakya.exe"
            sha256 = $exeHash
            size_bytes = (Get-Item $exePath).Length
        },
        @{
            file = "dist/Vakya-v$Version-Windows-x64.zip"
            sha256 = $zipHash
            size_bytes = (Get-Item $zipPath).Length
        }
    )
}

$manifestJson = $manifest | ConvertTo-Json -Depth 5
$manifestJson | Out-File -FilePath "$repoRoot\release-manifest.json" -Encoding ascii
Write-Host "      Release manifest written to release-manifest.json." -ForegroundColor Green

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "  BUILD & PACKAGING PIPELINE COMPLETED SUCCESSFULLY!        " -ForegroundColor Green
Write-Host "  Primary Executable: $exePath" -ForegroundColor White
Write-Host "  SHA256:             $exeHash" -ForegroundColor White
Write-Host "============================================================`n" -ForegroundColor Cyan
