# Vākya Graphical Desktop Application & Launcher

The **Vākya Graphical Desktop Application** provides a modern, professional desktop environment for developers using the Vākya programming language on Windows, macOS, and Linux.

---

## 1. Overview & Execution Modes

Vākya uses an intelligent **Dual-Mode Dispatch Architecture**:

```text
Double-Click vakya.exe (No Arguments) ───────────► Vākya GUI Launcher (Loading Screen + Dashboard)
Terminal: vakya hello.vakya ────────────────────► High-Speed CLI (Direct Terminal Output)
Terminal: vakya --gui [file.vakya] ─────────────► Vākya GUI File Editor & Runner
```

- **MODE A (Command-Line Interface)**: When invoked from PowerShell, CMD, or Windows Terminal with arguments (e.g. `vakya hello.vakya`, `vakya doctor`, `vakya repl`), the application executes strictly in terminal mode without spawning or flashing any GUI window.
- **MODE B (Graphical Launcher)**: When double-clicked from Windows Explorer, started from the Windows Start Menu, or executed without arguments, Vākya immediately hides any transient console and renders the rich graphical desktop interface.

---

## 2. GUI Features & Capabilities

### A. High-Speed Loading Screen (Splash)
- Centered, frameless window with Vākya Sanskrit typography and amber gold branding.
- Displays real-time initialization progress:
  - Standard library verification (`std/`)
  - Virtual machine & compiler structure initialization
  - Documentation and canonical examples indexing
  - User preferences loading
- Disappears dynamically once initialization is complete.

### B. Main Dashboard (Launcher Hub)
- **Status Badges**: Displays active engine (`Bytecode VM` / `AST Interpreter`) and runtime status.
- **Open Vākya File**: File dialog filtered to `*.vakya` with recent files history.
- **New Project**: Scaffolds a new project directory structure with `main.vakya`, `vakya.toml`, and `README.md`.
- **Interactive REPL**: Embedded rich evaluation console with history and multi-line support.
- **Canonical Examples**: Instant access to all 14 official examples with differential engine testing.
- **Documentation Reader**: Offline markdown guide viewer for all language features.
- **System Doctor**: Real-time diagnostic viewer matching `vakya doctor`.
- **Settings**: Configuration of runtime engine, theme (Dark / Light), and workspace path.

### C. File Runner & Editor View
- Built-in syntax viewer and editor.
- **▷ Run Program**: Executes the current source in the selected engine with millisecond timing.
- **🔍 Type Check**: Runs both Static Type Checker and Swamitva Borrow Checker.
- **🪄 Format**: Automatically formats code according to the official Vākya style specification.
- **🔬 Disassemble**: Views raw bytecode instructions and constant tables.
- **Output & Diagnostics Pane**: Clean error diagnostics without raw Python tracebacks.

---

## 3. Keyboard Shortcuts & Navigation

| Action | Shortcut / Trigger |
| :--- | :--- |
| **Run Code** | Click `▷ Run Program` |
| **Check Code** | Click `🔍 Type Check` |
| **Format Code** | Click `🪄 Format` |
| **Disassemble Bytecode** | Click `🔬 Disasm` |
| **REPL History Navigation** | `[Up Arrow]` / `[Down Arrow]` |
| **REPL Evaluate** | `[Enter]` |
| **Return to Dashboard** | Click `← Dashboard` |

---

## 4. Configuration & Preferences

Settings are persisted to `%APPDATA%\Vakya\gui_settings.json`:

```json
{
  "engine": "vm",
  "theme_mode": "dark",
  "default_workspace": "C:\\Users\\User\\Projects",
  "max_recursion": 200,
  "recent_files": [
    "C:\\Users\\User\\Projects\\hello.vakya"
  ]
}
```
