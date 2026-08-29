# Project 02 — Calculator with Web UI

## Overview

The **Calculator** showcase demonstrates how Vākya core computational logic can power user-facing interactive applications.

It features:
1. **Genuine Vākya Arithmetic Engine** (`vakya/calculator.vakya`):
   - Strongly typed arithmetic functions (`joda`, `ghatana`, `guna`, `bhaga`, `ghata`, `sheshaphala`).
   - Dynamic dispatch function (`ganana`).
   - Safe division by zero detection and error messaging.
2. **Modern Accessible UI** (`ui/`):
   - Responsive dark-theme design.
   - Complete keyboard shortcuts support (`0-9`, `+`, `-`, `*`, `/`, `%`, `^`, `Enter`, `Backspace`, `Escape`).
   - Decimal number entry, chained calculations, and explicit error state presentation.

---

## Architectural Separation & Current Language Boundaries

```
┌─────────────────────────────────────────────────────────┐
│ Host / Web UI Layer (HTML5 / CSS3 / JavaScript)         │
│  - Event loop, keyboard listeners, display rendering    │
└────────────────────────────┬────────────────────────────┘
                             │ (Semantic 1:1 Mapping)
┌────────────────────────────▼────────────────────────────┐
│ Vākya Computational Core (vakya/calculator.vakya)       │
│  - joda (Addition)        - bhaga (Division + Safe Zero)│
│  - ghatana (Subtraction)  - ghata (Power)               │
│  - guna (Multiplication)  - sheshaphala (Modulo)        │
└─────────────────────────────────────────────────────────┘
```

> **Note on Native GUI**:
> Vākya V1/V2 does not currently include a native windowing or OS GUI library (e.g., `ui.window()`). 
> Rather than inventing non-existent syntax, this showcase clearly demonstrates the separation of the computational layer (written in 100% valid Vākya) and the client interface, establishing the pattern for future Vākya WebAssembly and Native FFI bindings.

---

## How to Run

### 1. Run the Vākya Arithmetic Engine
```bash
vakya run showcase/02_calculator/vakya/calculator.vakya
```

### 2. Launch the Web UI
Simply open `showcase/02_calculator/ui/index.html` in any web browser.

---

## Running the Automated Test Suite

```bash
python -m unittest showcase/02_calculator/tests/test_calculator.py
```
