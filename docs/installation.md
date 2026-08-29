# Vākya Windows Installation Guide

## 1. Overview

Vākya is distributed as a self-contained, standalone toolchain for Windows (x86-64).

**Key Features of the Windows Distribution:**
- **No Python Required**: The installer and standalone binary bundle the full compiler, Bytecode VM, AST interpreter, and runtime.
- **No Git or Repository Required**: Run programs from any folder on your machine.
- **Automatic Standard Library Discovery**: Modules in `std/` are resolved automatically relative to the installation directory.
- **Zero-Configuration PATH Setup**: Automatic user PATH registration.

---

## 2. Installation Options

### Option A: 1-Click Windows Setup (`Vakya-Setup.exe`)
1. Download `Vakya-0.1.0-Windows-x64-Setup.exe`.
2. Double-click the installer and follow the setup wizard.
3. Choose your preferences:
   - **Add to PATH** (Recommended: Enabled by default)
   - **Associate `.vakya` files** (Optional)
4. Click **Install**.

### Option B: PowerShell 1-Click Installer (`install.ps1`)
From the release folder or downloaded zip archive:
```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1
```
This automatically installs Vākya to `%LOCALAPPDATA%\Vakya` and updates your user PATH.

### Option C: Portable ZIP Archive (`Vakya-v0.1.0-Windows-x64.zip`)
1. Extract the zip archive to your preferred directory (e.g. `C:\Tools\Vakya` or `%LOCALAPPDATA%\Vakya`).
2. Add the `bin\` subfolder to your system or user `PATH` environment variable.

---

## 3. Verifying Installation

Open a fresh PowerShell or Command Prompt terminal and run:

```powershell
# 1. Verify version
vakya --version

# 2. Run system diagnostic
vakya doctor

# 3. Check environment resolution paths
vakya env
```

Expected diagnostic output:
```text
============================================================
VĀKYA SYSTEM DIAGNOSTIC (DOCTOR)
============================================================
Vākya Version:      v0.1.0
Operating System:   Windows 11 (AMD64)
Python Runtime:     3.13.15 (Bundled Standalone)
Vākya Installation: C:\Users\<Username>\AppData\Local\Vakya
Standard Library:   OK (6 modules found)
Native Runtime:     OK (Headers found)
Default Engine:     Bytecode VM (IntEnum Flat Dispatch)
Fallback Engine:    Reference AST Interpreter
============================================================
```

---

## 4. Running Your First Vākya Program

Create a new file called `hello.vakya`:

```vakya
// hello.vakya
chara message = "Namaste Vākya"
vada(message)
```

Run it directly from any directory:

```powershell
# Shorthand execution
vakya hello.vakya

# Explicit run command
vakya run hello.vakya
```

Output:
```text
Namaste Vākya
```

---

## 5. Available Commands

| Command | Usage | Description |
| :--- | :--- | :--- |
| `vakya <file.vakya>` | Direct Run | Executes a Vākya file directly. |
| `vakya run <file>` | Run File | Runs a file with optional `--engine=vm` or `--engine=interpreter`. |
| `vakya check <file>` | Static Check | Validates syntax and types without executing. |
| `vakya fmt <file> -w` | Formatter | Formats source code in place. |
| `vakya repl` | Interactive REPL | Starts the interactive Vākya shell. |
| `vakya doctor` | Diagnostics | System health and toolchain diagnostic report. |
| `vakya env` | Environment | Displays active resolution paths. |
| `vakya disasm <file>` | Disassembler | Disassembles bytecode instructions. |
| `vakya build <file>` | Native Compiler | Compiles file to native C99/LLVM IR executable. |

---

## 6. Uninstallation

### Via Windows Settings
- Open **Settings > Apps > Installed Apps**.
- Locate **Vākya Programming Language** and select **Uninstall**.

### Via PowerShell Uninstaller
```powershell
powershell -ExecutionPolicy Bypass -File "%LOCALAPPDATA%\Vakya\uninstall.ps1"
```
The uninstaller cleanly removes all Vākya binaries, standard library files, PATH entries, and file associations without touching your source files.
