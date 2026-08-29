# Vākya — Windows Distribution & Installer Engineering Report

## Executive Summary

A standalone, self-contained Windows x86-64 distribution and installer has been engineered and validated for the **Vākya Programming Language (v0.1.0)**.

The end user does not need to install Python, configure environment variables, clone repositories, or install dependencies.

---

## 1. Release Metadata & Integrity Verification

| Metric | Value |
| :--- | :--- |
| **Language Version** | `0.1.0` |
| **Target Architecture** | Windows x86-64 (AMD64) |
| **Build Host OS** | Windows 11 (10.0.26200-SP0) |
| **Python Runtime** | 3.13.15 (Bundled Standalone in binary) |
| **Packaging Engine** | PyInstaller 6.22.2 + Inno Setup 6 / PowerShell Installer |
| **Binary Output** | `dist/Vakya/bin/vakya.exe` (10.1 MB) |
| **Portable ZIP Archive**| `dist/Vakya-v0.1.0-Windows-x64.zip` (10.0 MB) |
| **Binary SHA-256** | `FBE57BEC996AF337FC47AA1A7351EB8E152ABC15E24BFE9915690C2C2B3C6548` |
| **ZIP Archive SHA-256** | `8325F9DF77BA58FA7C50B2CB961521C3D6588ACF25CD1871B58E0F8D976461CF` |

---

## 2. End-User Requirements Matrix

| Requirement | End-User Needed? | Verification Note |
| :--- | :--- | :--- |
| **Python** | **NO** | Binary bundles its own isolated CPython runtime. |
| **pip / packages** | **NO** | All compiler, VM, typechecker, and borrow-checker packages are self-contained. |
| **Git / Repository** | **NO** | Standard library and runtime headers are packaged inside the installation directory. |
| **Internet Access** | **NO** | Zero runtime external network requests. |
| **Administrator Rights** | **NO** | Installs to `%LOCALAPPDATA%\Vakya` with per-user PATH registration. |

---

## 3. Package Layout Structure

```text
Vakya/
├── bin/
│   └── vakya.exe               # Standalone self-contained executable (10.1 MB)
├── std/                        # Standard Library modules
│   ├── core.vakya
│   ├── math.vakya
│   ├── strings.vakya
│   ├── collections.vakya
│   ├── io.vakya
│   └── time.vakya
├── runtime/                    # Standalone Native C99 headers
│   ├── vakya_runtime.h
│   ├── memory.h
│   ├── strings.h
│   ├── collections.h
│   ├── io.h
│   └── panic.h
├── docs/                       # Complete language documentation
├── examples/                   # 14 Canonical runnable examples
├── install.ps1                 # Standalone PowerShell 1-click installer
├── uninstall.ps1               # Clean uninstaller script
└── README.md                   # Project overview
```

---

## 4. User Experience & CLI Verification

### A. Direct Shorthand Execution
```powershell
# Shorthand execution
vakya hello.vakya

# Equivalent explicit command
vakya run hello.vakya
```

### B. Self-Diagnostics (`vakya doctor`)
```powershell
vakya doctor
```
```text
============================================================
VĀKYA SYSTEM DIAGNOSTIC (DOCTOR)
============================================================
Vākya Version:      v0.1.0
Operating System:   Windows 11 (AMD64)
Python Runtime:     3.13.15 (Bundled Standalone)
Vākya Installation: C:\Users\<User>\AppData\Local\Temp\...
Standard Library:   OK (6 modules found)
Native Runtime:     OK (Headers found)
Default Engine:     Bytecode VM (IntEnum Flat Dispatch)
Fallback Engine:    Reference AST Interpreter
Host C Compiler:    Available / C source emission active
LLVM Toolchain:     LLVM IR generator active
============================================================
```

### C. Environment Resolution (`vakya env`)
```powershell
vakya env
```
```text
VAKYA_VERSION=0.1.0
VAKYA_HOME=...
VAKYA_STDLIB=.../std
VAKYA_RUNTIME=.../runtime
VAKYA_FROZEN=true
```

---

## 5. Automated Smoke Testing in Isolated Directory

Executed via `scripts/build_windows.ps1` from an isolated temporary directory:
1. `vakya --version` -> Passed (`Vākya v0.1.0`)
2. `vakya doctor` -> Passed (All subsystem checks OK)
3. `vakya smoke_calc.vakya` (50 * 25) -> Passed (`1250`)
4. `vakya smoke_fact.vakya` (factorial 5) -> Passed (`120`)

---

## 6. Installation & Uninstallation Validation

1. **Installation**: Running `powershell -ExecutionPolicy Bypass -File .\install.ps1` copies all files to `%LOCALAPPDATA%\Vakya`, appends `%LOCALAPPDATA%\Vakya\bin` to User `PATH`, registers `.vakya` file association in `HKCU:\Software\Classes`, and verifies execution.
2. **Uninstallation**: Running `powershell -ExecutionPolicy Bypass -File .\uninstall.ps1` cleanly strips the PATH entry, removes registry keys, and deletes the installation directory without touching user code files.
