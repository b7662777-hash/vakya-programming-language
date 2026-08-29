# Vākya Distribution & Packaging Architecture

## 1. Distribution Topology

```text
Vakya/
├── bin/
│   └── vakya.exe               # Standalone self-contained executable
├── std/                        # Standard Library (.vakya source modules)
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
├── examples/                   # Canonical runnable examples
├── install.ps1                 # Standalone PowerShell installer
├── uninstall.ps1               # Clean uninstaller script
└── README.md                   # Project overview
```

---

## 2. Resource Path Resolution Mechanics

Vākya resolves its dependencies using hierarchical discovery implemented in `src/vakya/paths.py`:

```text
1. Explicit Override:   VAKYA_HOME environment variable (if set)
2. PyInstaller Bundle:   sys._MEIPASS (temporary unpacked runtime directory)
3. Installed Layout:    <InstallDir>/bin/vakya.exe -> <InstallDir>/std and <InstallDir>/runtime
4. Development Mode:    Repository root fallback relative to source file
5. Working Directory:   ./std fallback
```

---

## 3. Build & Release Automation

The packaging pipeline is automated via `scripts/build_windows.ps1`:

1. **Verification Gate**: Executes `python -m unittest discover -s tests -p "test_*.py"`.
2. **Binary Compilation**: PyInstaller compiles `vakya.spec` into an optimized standalone binary embedding the Vākya compiler, VM, and standard library.
3. **Distribution Assembly**: Assembles `dist/Vakya/` with `bin/`, `std/`, `runtime/`, `docs/`, and `examples/`.
4. **Archive Generation**: Creates `dist/Vakya-v<version>-Windows-x64.zip`.
5. **Installer Generation**: Compiles `installer/vakya_installer.iss` using Inno Setup compiler (`iscc.exe`).
6. **Integrity Manifest**: Computes SHA-256 hashes and outputs `release-manifest.json`.
7. **Isolated Smoke Testing**: Executes the compiled binary from an isolated temporary directory to ensure zero host-path leaks.
