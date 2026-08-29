# Standalone Windows x64 Verification Test Suite
# Tests isolated vakya.exe in a clean directory outside the repository

$ErrorActionPreference = "Stop"
$repoRoot = (Split-Path -Parent $MyInvocation.MyCommand.Definition) + "\.."
$repoRoot = [System.IO.Path]::GetFullPath($repoRoot)

$distExe = Join-Path $repoRoot "dist\vakya.exe"
if (-not (Test-Path $distExe)) {
    $distExe = Join-Path $repoRoot "dist\Vakya\bin\vakya.exe"
}

if (-not (Test-Path $distExe)) {
    Write-Error "Standalone binary not found at $distExe. Run build_windows.ps1 first."
}

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "   VĀKYA STANDALONE ISOLATED END-USER VERIFICATION TEST     " -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Testing Binary: $distExe`n"

# Create clean isolated temporary folder
$cleanDir = Join-Path ([System.IO.Path]::GetTempPath()) ("VakyaCleanTest_" + [System.Guid]::NewGuid().ToString().Substring(0, 8))
New-Item -ItemType Directory -Force -Path $cleanDir | Out-Null
Write-Host "Created clean isolated test directory: $cleanDir" -ForegroundColor Yellow

$isolatedExe = Join-Path $cleanDir "vakya.exe"
Copy-Item $distExe $isolatedExe

try {
    # Set location completely away from repository
    Set-Location -Path $cleanDir

    # TEST 0: --version and --help
    Write-Host "`n[TEST 0] Testing --version and --help ..." -ForegroundColor Yellow
    $vOut = & $isolatedExe --version
    if ($vOut -like "*0.1.0*") {
        Write-Host "  [PASS] --version -> $vOut" -ForegroundColor Green
    } else {
        Write-Error "TEST 0 Failed: Expected version containing 0.1.0, got '$vOut'"
    }

    # TEST 1: Hello World
    Write-Host "[TEST 1] Testing Hello World: vada(`"Namaste Vākya`") ..." -ForegroundColor Yellow
    $f1 = Join-Path $cleanDir "hello.vakya"
    "vada(`"Namaste Vākya`")" | Out-File -FilePath $f1 -Encoding ascii
    $out1 = & $isolatedExe hello.vakya
    if ($out1.Trim() -like "Namaste*") {
        Write-Host "  [PASS] Output: $out1" -ForegroundColor Green
    } else {
        Write-Error "TEST 1 Failed: Expected output starting with Namaste, got '$out1'"
    }

    # TEST 2: Arithmetic
    Write-Host "[TEST 2] Testing Arithmetic: chara a = 10; chara b = 20; vada(a + b) ..." -ForegroundColor Yellow
    $f2 = Join-Path $cleanDir "arithmetic.vakya"
    "chara a = 10`nchara b = 20`nvada(a + b)" | Out-File -FilePath $f2 -Encoding ascii
    $out2 = & $isolatedExe arithmetic.vakya
    if ($out2.Trim() -eq "30") {
        Write-Host "  [PASS] Output: $out2" -ForegroundColor Green
    } else {
        Write-Error "TEST 2 Failed: Expected '30', got '$out2'"
    }

    # TEST 3: Recursion (Factorial 10)
    Write-Host "[TEST 3] Testing Recursion: factorial(10) ..." -ForegroundColor Yellow
    $f3 = Join-Path $cleanDir "factorial.vakya"
    $code3 = @"
karya factorial(n: sankhya) -> sankhya {
    yadi n <= 1 {
        pratyavartaya 1
    }
    pratyavartaya n * factorial(n - 1)
}
vada(factorial(10))
"@
    $code3 | Out-File -FilePath $f3 -Encoding ascii
    $out3 = & $isolatedExe factorial.vakya
    if ($out3.Trim() -eq "3628800") {
        Write-Host "  [PASS] Output: $out3" -ForegroundColor Green
    } else {
        Write-Error "TEST 3 Failed: Expected '3628800', got '$out3'"
    }

    # TEST 4: Standard Library Import (aayat math)
    Write-Host "[TEST 4] Testing Standard Library: aayat math; vada(math.PI) ..." -ForegroundColor Yellow
    $f4 = Join-Path $cleanDir "test_math.vakya"
    "aayat math`nvada(math.PI)" | Out-File -FilePath $f4 -Encoding ascii
    $out4 = & $isolatedExe test_math.vakya
    if ($out4.Trim() -like "3.141592*") {
        Write-Host "  [PASS] Output: $out4" -ForegroundColor Green
    } else {
        Write-Error "TEST 4 Failed: Expected '3.141592...', got '$out4'"
    }

    # TEST 5: Arrays
    Write-Host "[TEST 5] Testing Collections: chara numbers = [1, 2, 3, 4]; vada(numbers) ..." -ForegroundColor Yellow
    $f5 = Join-Path $cleanDir "test_arrays.vakya"
    "chara numbers = [1, 2, 3, 4]`nvada(numbers)" | Out-File -FilePath $f5 -Encoding ascii
    $out5 = & $isolatedExe test_arrays.vakya
    if ($out5.Trim() -eq "[1, 2, 3, 4]") {
        Write-Host "  [PASS] Output: $out5" -ForegroundColor Green
    } else {
        Write-Error "TEST 5 Failed: Expected '[1, 2, 3, 4]', got '$out5'"
    }

    # TEST 6: Error Reporting (no tracebacks)
    Write-Host "[TEST 6] Testing Clean Diagnostic Error Reporting ..." -ForegroundColor Yellow
    $f6 = Join-Path $cleanDir "invalid.vakya"
    "chara x = `nvada(x" | Out-File -FilePath $f6 -Encoding ascii
    $errProcess = Start-Process -FilePath $isolatedExe -ArgumentList "invalid.vakya" -NoNewWindow -PassThru -Wait -RedirectStandardError (Join-Path $cleanDir "err.log") -RedirectStandardOutput (Join-Path $cleanDir "out.log")
    $errContent = (Get-Content (Join-Path $cleanDir "err.log") -Raw -ErrorAction SilentlyContinue) + (Get-Content (Join-Path $cleanDir "out.log") -Raw -ErrorAction SilentlyContinue)
    if ($errContent.Contains("Error [E") -and -not $errContent.Contains("Traceback (most recent call last)")) {
        Write-Host "  [PASS] Clean diagnostic displayed without Python traceback" -ForegroundColor Green
    } else {
        Write-Error "TEST 6 Failed: Output did not contain clean diagnostic or leaked traceback: `n$errContent"
    }

    # TEST 7: Doctor & Env
    Write-Host "[TEST 7] Testing 'doctor' and 'env' Subcommands ..." -ForegroundColor Yellow
    $docOut = (& $isolatedExe doctor) -join "`n"
    $envOut = (& $isolatedExe env) -join "`n"
    if ($docOut.Contains("SYSTEM DIAGNOSTIC") -and $envOut.Contains("VAKYA_VERSION=")) {
        Write-Host "  [PASS] Doctor & Env diagnostics executed cleanly" -ForegroundColor Green
    } else {
        Write-Error "TEST 7 Failed: doctor/env did not produce expected output. Got:`nDoctor:`n$docOut`nEnv:`n$envOut"
    }

    Write-Host "`n============================================================" -ForegroundColor Cyan
    Write-Host "  ALL 8 STANDALONE END-USER ACCEPTANCE TESTS PASSED!        " -ForegroundColor Green
    Write-Host "============================================================`n" -ForegroundColor Cyan

} finally {
    Set-Location -Path $repoRoot
    Remove-Item -Recurse -Force $cleanDir
}
