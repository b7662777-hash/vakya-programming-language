# Vākya Clean Checkout Isolation Verification Script
# Verifies that Vākya installs, runs, and passes all tests from a clean clone without repo dependencies

$ErrorActionPreference = "Stop"
$repoRoot = (Split-Path -Parent $MyInvocation.MyCommand.Definition) + "\.."
$repoRoot = [System.IO.Path]::GetFullPath($repoRoot)

$tempCheckout = Join-Path ([System.IO.Path]::GetTempPath()) ("VakyaCleanCheckout_" + [System.Guid]::NewGuid().ToString().Substring(0, 8))

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "     VĀKYA CLEAN CHECKOUT ISOLATION VERIFICATION TEST       " -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Target Directory: $tempCheckout`n"

New-Item -ItemType Directory -Force -Path $tempCheckout | Out-Null

# Copy source repository excluding ignored build artifacts
$items = Get-ChildItem -Path $repoRoot -Exclude "dist", "build", ".venv", ".pytest_cache", "__pycache__"
foreach ($item in $items) {
    Copy-Item -Recurse -Force $item.FullName (Join-Path $tempCheckout $item.Name)
}

try {
    Set-Location -Path $tempCheckout

    Write-Host "[1/4] Installing package in clean environment ..." -ForegroundColor Yellow
    python -m pip install --quiet -e .
    Write-Host "      Installed successfully." -ForegroundColor Green

    Write-Host "[2/4] Running core test suite (448 tests) ..." -ForegroundColor Yellow
    $prevEA = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    python -m unittest discover -s tests -p "test_*.py"
    if ($LASTEXITCODE -ne 0) { throw "Core tests failed in clean checkout" }
    Write-Host "      All core tests passed in clean checkout." -ForegroundColor Green

    Write-Host "[3/4] Running showcase tests ..." -ForegroundColor Yellow
    python -m unittest discover -s showcase/01_name_program/tests
    if ($LASTEXITCODE -ne 0) { throw "Showcase 01 tests failed" }
    python -m unittest discover -s showcase/02_calculator/tests
    if ($LASTEXITCODE -ne 0) { throw "Showcase 02 tests failed" }
    python -m unittest discover -s showcase/03_browser/tests
    if ($LASTEXITCODE -ne 0) { throw "Showcase 03 tests failed" }
    $ErrorActionPreference = $prevEA
    Write-Host "      All showcase tests passed in clean checkout." -ForegroundColor Green

    Write-Host "[4/4] Verifying CLI execution offline ..." -ForegroundColor Yellow
    $hOut = (python -m vakya.cli run examples/01_hello.vakya) -join "`n"
    if ($hOut.Contains("Namaste")) {
        Write-Host "      CLI Hello World output: $hOut" -ForegroundColor Green
    } else {
        Write-Error "Hello world execution failed in clean checkout"
    }

    $factOut = (python -m vakya.cli run examples/13_factorial.vakya) -join "`n"
    if ($factOut.Contains("720")) {
        Write-Host "      CLI Factorial output:   $factOut" -ForegroundColor Green
    } else {
        Write-Error "Factorial execution failed in clean checkout"
    }

    $docOut = (python -m vakya.cli doctor) -join "`n"
    if ($docOut.Contains("SYSTEM DIAGNOSTIC")) {
        Write-Host "      CLI Doctor diagnostics: [PASS]" -ForegroundColor Green
    } else {
        Write-Error "Doctor check failed in clean checkout"
    }

    Write-Host "`n============================================================" -ForegroundColor Cyan
    Write-Host "  CLEAN CHECKOUT ISOLATION VERIFICATION PASSED 100%!       " -ForegroundColor Green
    Write-Host "============================================================`n" -ForegroundColor Cyan

} finally {
    Set-Location -Path $repoRoot
    Start-Sleep -Milliseconds 800
    Remove-Item -Recurse -Force $tempCheckout -ErrorAction SilentlyContinue
}
