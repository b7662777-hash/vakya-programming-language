# Vākya Windows Distribution & Installation Guide

This document describes the complete Windows packaging, installer, and standalone deployment system for the Vākya Programming Language.

---

## 1. Distribution Artifacts

The Vākya Windows release produces two primary artifacts:

1. **`vakya.exe` (Single-File Standalone Portable Binary)**:
   - Location: `dist/vakya.exe` (also aliased as `dist/Vakya.exe`)
   - Fully self-contained portable executable.
   - Requires zero external dependencies (no Python, pip, or Git).
   - Bundles the CLI, Bytecode Virtual Machine, Tree-Walking Interpreter, Standard Library, Offline Documentation, Canonical Examples, and Graphical Desktop Launcher.

2. **`Vakya-v0.1.0-Windows-x64.zip` (Portable Package)**:
   - Full distribution containing `bin/vakya.exe`, `std/`, `runtime/`, `docs/`, `examples/`, `resources/`, `README.md`, `install.ps1`, and `uninstall.ps1`.

3. **`Vakya-Setup-x64.exe` (Inno Setup Installer)**:
   - Full native Windows wizard installer with Start Menu shortcuts and `.vakya` file association.

---

## 2. Installation Methods

### Method 1: Portable Single-File Executable (Zero-Install)
Download `vakya.exe`, place it in any folder, and run:
- Double-click `vakya.exe` to launch the **Vākya GUI Launcher**.
- Run `vakya.exe <file.vakya>` from PowerShell or CMD to execute programs directly.

### Method 2: One-Click PowerShell Installer
Extract `Vakya-v0.1.0-Windows-x64.zip` and run:
```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1
```
This will:
- Install Vākya into `%LOCALAPPDATA%\Programs\Vakya`.
- Add `bin` to the User `PATH` environment variable.
- Create a Start Menu shortcut (`Start Menu -> Vakya`) with the custom Vākya application icon.
- Associate `.vakya` file extensions in the Windows Registry.

### Method 3: Clean Uninstallation
Run:
```powershell
powershell -ExecutionPolicy Bypass -File .\uninstall.ps1
```
This cleanly removes all installed files, registry associations, and PATH entries.

---

## 3. Windows Subsystem & Terminal Behavior

When launching from terminal:
```powershell
vakya hello.vakya
```
Stdout and stderr stream directly to the terminal with exit code 0.

When double-clicking `vakya.exe` in Windows Explorer:
The transient console window is hidden immediately (<1ms) and the Graphical Desktop Launcher opens.
