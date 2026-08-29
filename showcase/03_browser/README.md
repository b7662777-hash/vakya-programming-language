# Project 03 — Vākya Mini Browser

## Overview

The **Vākya Mini Browser** is the systems & application showcase project for Vākya. It demonstrates:
- How core algorithmic tasks (URL parsing, stateful navigation history, recursive DOM trees) are implemented in valid, pure Vākya code.
- How host engine runtimes coordinate with Vākya data models to load, parse, inspect, and render web pages.
- A functional educational browser shell complete with an address bar, navigation controls (`Back`, `Forward`, `Reload`), a DOM tree inspector, and raw HTML viewer.

---

## Directory Structure

```text
showcase/03_browser/
├── README.md               # Showcase overview & guide
├── architecture.md         # Detailed architectural specification
├── vakya/
│   └── browser.vakya       # [Vākya] URL parsing, history stack, and DOM models
├── browser/
│   ├── __init__.py
│   ├── http_client.py      # [Host Runtime] HTTP/HTTPS network client
│   └── engine.py           # [Browser Engine] HTML parser & layout engine
├── ui/
│   ├── index.html          # [UI] Browser window shell
│   ├── style.css           # [UI] Styling & dark theme
│   └── app.js              # [UI] Client controller
├── examples/
│   ├── sample.html         # Well-formed HTML document
│   └── malformed.html      # Resilient parsing test page
└── tests/
    ├── __init__.py
    └── test_browser.py     # Automated browser test suite
```

---

## How to Run

### 1. Run Vākya Core Logic
```bash
vakya run showcase/03_browser/vakya/browser.vakya
```

### 2. Launch the Web Browser UI
Open `showcase/03_browser/ui/index.html` in your web browser.

You can enter any live URL (such as `https://example.com`) or choose one of the built-in presets (`Sample Page`, `Malformed HTML Test`, `Vākya Features`) to inspect the rendered page, live DOM tree structure, and raw source.

---

## Running the Automated Test Suite

```bash
python -m unittest showcase/03_browser/tests/test_browser.py
```
