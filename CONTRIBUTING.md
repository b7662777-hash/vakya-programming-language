# Contributing to Vākya

Welcome, and thank you for your interest in contributing to **Vākya** (वाक्य) — the Romanized Sanskrit programming language!

---

## 1. Code of Conduct

All contributors are expected to adhere to our [Code of Conduct](CODE_OF_CONDUCT.md) in all community spaces and interactions.

---

## 2. Development Prerequisites

- **Python 3.12 or newer**
- **Git**
- *(Optional for native C compilation tests)*: GCC, Clang, or MSVC (`cl.exe`)

---

## 3. Developer Quick Start

Clone the repository and set up a development virtual environment:

### Linux / macOS
```bash
git clone https://github.com/vakya-lang/vakya.git
cd vakya
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e ".[dev]"
```

### Windows (PowerShell)
```powershell
git clone https://github.com/vakya-lang/vakya.git
cd vakya
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

Verify your installation:
```bash
vakya --version
vakya doctor
vakya test
```

---

## 4. Repository Structure

```text
vakya/
├── src/vakya/              # Core compiler, runtime, VM, CLI, and GUI
│   ├── lexer/              # Lexical analyzer and token definitions
│   ├── parser/             # Recursive-descent parser and AST nodes
│   ├── ast/                # AST node representations
│   ├── typechecker/        # Static type checker and Swamitva borrow checker
│   ├── bytecode/           # Bytecode instruction opcodes and compiler
│   ├── vm/                 # Flat-opcode bytecode virtual machine
│   ├── interpreter/        # Reference tree-walking AST interpreter
│   ├── ir/                 # Intermediate representation lowering
│   ├── native/             # Native C source emitter and compiler backend
│   ├── modules/            # Module resolution and loader
│   ├── formatter/          # Source code formatter (vakya fmt)
│   ├── repl/               # Interactive REPL
│   ├── errors/             # Error code catalog and diagnostic renderer
│   ├── gui/                # Desktop GUI Launcher and IDE views
│   └── cli.py              # Unified CLI / GUI dispatcher entrypoint
├── std/                    # Standard library modules (math, string, io, time)
├── runtime/                # Standalone native C runtime headers and primitives
├── examples/               # 14 canonical Vākya code examples
├── showcase/               # Showcase applications (CLI, Calculator, Browser)
├── tests/                  # 448 automated unit, conformance, and differential tests
├── benchmarks/             # Baseline performance measurement benchmarks
├── scripts/                # Build and distribution automation scripts
├── installer/              # Windows installer scripts
└── docs/                   # Authoritative language documentation and specifications
```

---

## 5. Running Tests

### Run Full Test Suite (448 Tests)
```bash
python -m unittest discover -s tests -p "test_*.py"
```
Or via the CLI:
```bash
vakya test
```

### Run Showcase Tests
```bash
python -m unittest discover -s showcase -p "test_*.py"
```

### Run Differential Verification (VM vs Interpreter)
```bash
python -m unittest discover -s tests/differential -p "test_*.py"
```

### Run Borrow Checker Tests
```bash
python -m unittest discover -s tests/borrow -p "test_*.py"
```

---

## 6. Language Conventions & Formatting

- **Keywords**: All keywords follow Romanized Sanskrit etymology defined in [`docs/keywords.md`](docs/keywords.md).
- **Diagnostics**: Errors must register standard error codes (`E100`–`E505`) and provide contextual source line highlights and actionable remediation hints.
- **Formatter**: Use `vakya fmt <file.vakya> --write` to format Vākya source code.

---

## 7. Pull Request Process

1. Fork the repository and create a new feature branch (`git checkout -b feature/my-feature`).
2. Implement your changes with corresponding unit tests in `tests/`.
3. Verify that all 448 tests pass cleanly.
4. Update any relevant documentation in `docs/`.
5. Submit a Pull Request describing your motivation and referencing any related issues.
