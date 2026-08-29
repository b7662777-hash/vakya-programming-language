# Vākya V1 (वाक्य) — Romanized Sanskrit Programming Language

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)

> **Modern programming structure + Sanskrit vocabulary + extremely readable syntax.**

**Vākya** (वाक्य, meaning *statement* or *sentence* in Sanskrit) is a modern, statically checkable programming language designed with Sanskrit-inspired vocabulary and written in standard Latin/Roman characters for effortless typing on standard keyboards.

Vākya V1 is a complete, standalone interpreted language featuring an explicit handwritten lexer, recursive-descent parser, Abstract Syntax Tree (AST), static typechecker, tree-walking interpreter with lexical scoping, rich error reporting with source diagnostics, code formatter, interactive REPL, CLI tool, and comprehensive test suite.

---

## 🌟 Key Features

* **Sanskrit-Inspired Vocabulary**: Intuitive keywords (`chara`, `dhruva`, `karya`, `yadi`, `anyatha`, `yavat`, `pratyekam`, `pratyavartaya`, `vada`, `puchha`, etc.)
* **Romanized Syntax**: Standard ASCII characters with curly-brace blocks `{ ... }`
* **Static Type Checking & Inference**: Optional type annotations with automatic type inference
* **Rich Diagnostic Engine**: Formatted error reports with line numbers, error codes (`[E101]`-`[E402]`), and caret (`^^^^`) source indicators
* **Standard Built-in Functions**: `vada`, `puchha`, `lamba`, `prakaar`, `suchi_jodo`, `suchi_hatao`, `shabda_bada`, `shabda_chhota`, `shabda_trim`
* **Developer Tooling**: Built-in code formatter (`vakya fmt`), interactive REPL (`vakya repl`), type checker (`vakya check`), and test runner (`vakya test`)
* **Clean Architecture**: Clear separation of frontend (lexer, parser, AST, typechecker) and runtime (environment, values, interpreter), ready for future native compiler backends.

---

## 🚀 Quick Start

### Installation

Clone the repository and install locally:

```bash
git clone https://github.com/vakya-lang/vakya.git
cd vakya
pip install -e .
```

### Check Version

```bash
vakya version
```

### Run an Example

```bash
vakya run examples/hello.vakya
```

---

## 📜 Example Program

```vakya
// Factorial with type annotations
karya factorial(n: sankhya) -> sankhya {
    yadi n <= 1 {
        pratyavartaya 1
    }

    pratyavartaya n * factorial(n - 1)
}

chara result = factorial(5)

vada("Factorial of 5:")
vada(result)
```

**Output:**
```text
Factorial of 5:
120
```

---

## 🛠️ CLI Usage

```bash
# Execute a program
vakya run examples/calculator.vakya

# Typecheck without executing
vakya check examples/factorial.vakya

# Format source code
vakya fmt examples/hello.vakya --write

# Launch interactive REPL
vakya repl

# Run automated test suite
vakya test
```

---

## 📖 Keyword Reference Table

| Vākya Keyword | English Equivalent | Purpose |
| :--- | :--- | :--- |
| `chara` | `var` / `let` | Mutable variable declaration |
| `dhruva` | `const` | Immutable constant declaration |
| `karya` | `function` | Function definition |
| `pratyavartaya` | `return` | Return value from function |
| `yadi` | `if` | Conditional branch |
| `anyatha` | `else` | Alternative conditional branch |
| `tarhi` | `then` | Optional continuation keyword |
| `yavat` | `while` | While loop |
| `pratyekam` | `for each` | For-each loop |
| `madhye` | `in` / `within` | Iteration connector |
| `virama` | `break` | Terminate loop |
| `agaccha` | `continue` | Continue to next loop iteration |
| `satya` | `true` | Boolean true literal |
| `asatya` | `false` | Boolean false literal |
| `shunya` | `null` / `nil` | Null value literal |
| `vada` | `print` | Output to console |
| `puchha` | `input` | Prompt input from console |
| `evam` | `and` (`&&`) | Logical conjunction |
| `va` | `or` (`\|\|`) | Logical disjunction |
| `na` | `not` (`!`) | Logical negation |

---

## 📚 Documentation

Detailed documentation is available in the [`docs/`](docs/) directory:

- [Language Design & Architecture](docs/language.md)
- [Syntax & Grammar](docs/syntax.md)
- [Type System & Inference](docs/types.md)
- [Functions & Closures](docs/functions.md)
- [Diagnostic & Error System](docs/errors.md)
- [Vākya Roadmap](docs/roadmap.md)

---

## 🧪 Testing

Run the automated test suite with Python's built-in test runner or pytest:

```bash
pytest
# or
vakya test
```

---

## 📄 License

Vākya is licensed under the [MIT License](LICENSE).
