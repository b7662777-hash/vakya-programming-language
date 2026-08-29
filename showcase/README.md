# Vākya Official Showcase Applications

Welcome to the official showcase suite for the **Vākya Programming Language**.

These three applications demonstrate the capabilities of Vākya today, establish clean architectural patterns for host integration, and illuminate the systems roadmap for future Vākya development.

---

## 📂 Showcase Projects Overview

```text
showcase/
├── 01_name_program/    # Project 01: Language fundamentals (I/O, strings, variables, functions)
├── 02_calculator/      # Project 02: Application logic and Web UI integration
└── 03_browser/         # Project 03: Systems architecture, URL parsing, DOM trees, and Mini Browser
```

---

### [Project 01 — Name Program](01_name_program/README.md)
* **Goal**: The simplest polished Vākya application.
* **Demonstrates**: Interactive terminal input (`puchha`), variable declarations (`chara`), string concatenation (`+`), string trimming (`shabda_trim`), and formatted output (`vada`).
* **Run**:
  ```bash
  vakya run showcase/01_name_program/main.vakya
  ```

---

### [Project 02 — Calculator with UI](02_calculator/README.md)
* **Goal**: Real interactive calculator application with a clean, responsive UI.
* **Demonstrates**: Vākya arithmetic computational layer (`joda`, `ghatana`, `guna`, `bhaga`, `ghata`, `sheshaphala`), safe division by zero error handling, and 1:1 semantic binding with a keyboard-accessible HTML5/CSS3/JavaScript UI.
* **Run**:
  ```bash
  vakya run showcase/02_calculator/vakya/calculator.vakya
  # Open showcase/02_calculator/ui/index.html in any browser
  ```

---

### [Project 03 — Vākya Mini Browser](03_browser/README.md)
* **Goal**: Systems & application showcase demonstrating document parsing, navigation state, and visual page layout.
* **Demonstrates**: Pure Vākya URL parsing (`parse_url`), stateful navigation history stack (`itihaasa_*`), recursive DOM node tree structures (`dom_node`), alongside a resilient host HTML parser, network HTTP client, and tabbed inspection shell (Rendered View, DOM Tree, Raw HTML, Architecture).
* **Run**:
  ```bash
  vakya run showcase/03_browser/vakya/browser.vakya
  # Open showcase/03_browser/ui/index.html in any browser
  ```

---

## 📊 Vākya Language Capability Matrix

| Language / System Capability | Vākya Current (V2 Alpha) | Showcase Application Layer | Future Roadmap Direction |
| :--- | :--- | :--- | :--- |
| **Variables & Constants** | ✅ Native (`chara`, `dhruva`) | Project 01, 02, 03 | Immutable references |
| **Functions & Closures** | ✅ Native (`karya`, `UpvalueCell`) | Project 01, 02, 03 | Tail call optimization |
| **Strings & Text Operations** | ✅ Native (`shabda_trim`, `lamba`) | Project 01, 03 | Unicode normalization |
| **Collections (List & Map)** | ✅ Native (`suchi`, `naksha`) | Project 02, 03 | Immutable Persistent Collections |
| **Control Flow & Loops** | ✅ Native (`yadi`, `yavat`, `pratyekam`)| Project 01, 02, 03 | Pattern matching (`anuroopa`) |
| **Bytecode Virtual Machine** | ✅ Native (`VirtualMachine`) | Project 01, 02, 03 | JIT / Register VM |
| **Graphical User Interface** | 🔄 Host / UI Layer | Project 02, 03 UI | Native Windowing Library / Canvas |
| **Network & HTTP Sockets** | 🔄 Host Network Layer | Project 03 (`http_client.py`) | Native `jalam` Module |
| **HTML Parsing Engine** | 🔄 Host Engine Layer | Project 03 (`engine.py`) | Native Parser Module |
| **Native AOT Compilation** | ⏳ Future (V3) | N/A | LLVM / Cranelift Backend |
| **Memory Safety & Borrowing** | ⏳ Future (V3) | N/A | Ownership Model |
| **Capability Security** | ⏳ Future (V3) | N/A | Sandbox Permissions (`anumati`) |

---

## 🧪 Automated Testing

To run all showcase test suites:

```bash
python -m unittest discover -s showcase -p "test_*.py"
```

To run the entire Vākya language regression test suite:

```bash
vakya test
```
