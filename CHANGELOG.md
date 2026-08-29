# Changelog

All notable changes to the **Vākya Programming Language** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.0] - 2026-08-29

### Added
- **Core Language Syntax**: Full Romanized Sanskrit syntax (`chara`, `dhruva`, `karya`, `yadi`, `anyatha`, `yavat`, `pratyekam`, `ganana`, `pratyavartaya`, `aayat`).
- **Lexical Analyzer & Parser**: Handwritten lexer and recursive-descent parser with comprehensive AST representations.
- **Static Type System**: Bidirectional type checker and type inference supporting `sankhya`, `dashamika`, `shabda`, `boolean`, `suchi`, `naksha`, and `shunya`.
- **Swamitva Ownership & Borrow Checker**: Compile-time memory safety system detecting use-after-move (`E501`), mutable borrow conflicts (`E502`), multiple mutable borrows (`E503`), dangling references (`E504`), and mutation while borrowed (`E505`).
- **High-Speed Bytecode VM**: Flat integer opcode virtual machine with specialized dispatch, call frame pooling, and integer arithmetic acceleration.
- **Reference AST Interpreter**: Tree-walking AST interpreter for differential verification and specification compliance.
- **Intermediate Representation (IR)**: Linear 3-address SSA-like intermediate representation.
- **Native C-Emitter Backend**: AOT compilation emitting standalone C code targeting GCC, Clang, or MSVC.
- **Standard Library**: Initial standard library modules (`std/math.vakya`, `std/string.vakya`, `std/io.vakya`, `std/time.vakya`).
- **Module System**: Module loader and `aayat` import statement with member property access (`math.PI`, `math.varga`).
- **Diagnostic Engine**: Machine-readable JSON and ANSI-highlighted diagnostics with source snippets and remediation tips.
- **Developer Tooling**:
  - `vakya run`: Multi-engine code execution (`--engine=vm` or `--engine=interpreter`).
  - `vakya check`: Static type and borrow checking.
  - `vakya fmt`: Source code formatter with in-place write and CI check modes.
  - `vakya repl`: Interactive REPL with command history.
  - `vakya disasm`: Bytecode instruction disassembler.
  - `vakya doctor`: System and environment diagnostic health inspection.
  - `vakya new`: Project scaffolding tool.
- **Dual-Mode Desktop GUI Launcher**: Graphical desktop interface with loading screen, dashboard hub, code editor, REPL, canonical example explorer, offline doc reader, and settings.
- **Windows Packaging & Installer**: Single-file portable `vakya.exe`, portable `.zip`, and one-click installer scripts.
- **Automated Test Matrix**: 448 automated unit, conformance, differential, borrow, and CLI regression tests.

### Known Limitations
- Native compilation is currently supported via the C-emitter backend; LLVM and Cranelift JIT/AOT backends are in active architecture/prototype phases.
- Networking sockets and async event loop runtime are currently host-assisted in showcase applications.
