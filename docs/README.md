# Vākya Documentation Index

Welcome to the official documentation for the **Vākya Programming Language** (वाक्य).

---

## 📚 Documentation Table of Contents

### 1. Getting Started & Fundamentals
- [**Getting Started Guide**](getting-started.md) — Installation, environment setup, and your first program.
- [**Language Tour**](language-tour.md) — Quick introduction to Vākya syntax, features, and idioms.
- [**Language Specification**](language-spec.md) — Authoritative grammar and language specification.
- [**Formal Grammar (EBNF)**](grammar.ebnf) — Formal grammar in Extended Backus-Naur Form.
- [**Keywords Reference**](keywords.md) — Romanized Sanskrit keywords, Devanagari etymology, and usage.
- [**Operators Reference**](operators.md) — Operator precedence, associativity, and operand type rules.

### 2. Type System & Memory Safety
- [**Type System**](type-system.md) — Static type checking, inference, and type hierarchy.
- [**Memory Safety (Swamitva)**](memory-safety.md) — Compile-time ownership, move semantics, and borrow checking (`E501`–`E505`).
- [**Memory Model**](memory-model.md) — Stack vs heap allocation and value lifecycles.
- [**Error Catalog**](errors.md) — Standard compiler and runtime error codes with remediation examples.

### 3. Architecture & Compiler Internals
- [**System Architecture**](architecture.md) — High-level architecture and pipeline diagrams.
- [**Compiler Pipeline**](compiler.md) — Lexer, parser, AST lowering, intermediate representation (IR), and code emitters.
- [**Bytecode Virtual Machine**](bytecode.md) — Opcode instruction set and high-performance VM design.
- [**Native Compiler Backend**](native-compiler.md) — Standalone C code emitter and native execution runtime.
- [**Intermediate Representation (IR)**](ir.md) — Linear SSA-style IR.

### 4. Standard Library & Ecosystem
- [**Standard Library Reference**](stdlib.md) — Built-in modules (`math`, `string`, `io`, `time`).
- [**Module System**](modules.md) — `aayat` module resolution, paths, and cycle prevention.
- [**CLI Tooling Reference**](cli.md) — Complete guide to `vakya` command-line tools.
- [**Desktop GUI Launcher**](gui.md) — Graphical desktop launcher and IDE views.

### 5. Quality, Performance & Operations
- [**Testing & Quality Assurance**](testing.md) — 448-test test matrix, differential testing, and regression suites.
- [**Performance & Benchmarking**](benchmarks.md) — Empirical execution benchmarks and performance methodology.
- [**Windows Distribution**](windows-distribution.md) — Standalone binaries and Windows installer documentation.
- [**Release Engineering**](release-process.md) — Release automation and packaging process.
- [**Security Policy & Model**](security.md) — Sandboxing limits and responsible disclosure.
- [**GitHub Configuration**](github.md) — Suggested topics, description, and social preview assets.
