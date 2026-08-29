# Project 01 — Name Greeting Program

## Overview

The **Name Program** is the foundational showcase application for Vākya. It demonstrates:
- Standard terminal user input via `puchha()`
- Variable declarations with `chara`
- String manipulation and trimming via `shabda_trim()` and `lamba()`
- Function definitions with typed parameters (`karya abhivadana(naama: shabda) -> shabda`)
- Conditional branching with `yadi` and `anyatha`
- Standard output via `vada()`

---

## How to Run

From the root of the repository:

```bash
vakya run showcase/01_name_program/main.vakya
```

Or from within this directory:

```bash
cd showcase/01_name_program
vakya run main.vakya
```

---

## Program Behavior & Expected Output

When launched, the program prompts for your name:

```text
Tumhara naam kya hai? Goku
Namaste, Goku!
```

If you press Enter without typing a name:

```text
Tumhara naam kya hai? 
Namaste, Mitra!
```

---

## Vākya Language Concepts Demonstrated

| Syntax / Keyword | Category | Purpose |
| :--- | :--- | :--- |
| `karya` | Functions | Declares a typed function `abhivadana` |
| `chara` | Variables | Declares a mutable variable `naama` |
| `puchha(...)` | Builtin I/O | Prompts user and reads a line from stdin |
| `vada(...)` | Builtin I/O | Prints greeting message to stdout |
| `shabda_trim(...)` | Builtin String | Strips leading and trailing whitespace |
| `lamba(...)` | Builtin Utility | Returns the character length of a string |
| `yadi` / `anyatha` | Control Flow | Handles empty vs non-empty input |
| `+` | Operator | Concatenates strings |

---

## Running the Automated Test

```bash
python -m unittest showcase/01_name_program/tests/test_name.py
```
