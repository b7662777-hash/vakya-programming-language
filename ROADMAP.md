# Vākya Language Roadmap

This document outlines the development direction, architecture milestones, and future roadmap for the **Vākya Programming Language**.

---

## 1. Completed Milestones

- [x] **V1 Language Core**: Romanized Sanskrit lexer, recursive-descent parser, AST representations, tree-walking interpreter, and static type checker.
- [x] **V2 Bytecode Virtual Machine**: Flat integer opcode VM, chunk compiler, call frame management, differential engine verification, and benchmark suite.
- [x] **V3 Compile-Time Memory Safety (Swamitva)**: Static ownership tracking, move semantics, affine types, shared/mutable borrow checking (`E501`–`E505`), and C-emitter native compilation.
- [x] **Standard Library & Modules**: `aayat` module system, member access, and built-in standard library foundation (`math`, `string`, `io`, `time`).
- [x] **Developer CLI & Diagnostics Tooling**: `vakya run`, `check`, `fmt`, `repl`, `disasm`, `doctor`, `new`, `errors`, and ANSI/JSON diagnostic reports.
- [x] **Dual-Mode Desktop GUI Launcher**: High-DPI desktop application with splash screen, dashboard hub, editor, REPL, offline docs, and examples explorer.
- [x] **Windows Packaging & Distribution**: Standalone single-file portable `vakya.exe`, release `.zip`, installer scripts, and Start Menu / file associations.
- [x] **Automated Test Suite**: 448 automated unit, conformance, differential, and regression tests.

---

## 2. In Progress (v0.2.0)

- [ ] **Cross-Platform Standalone Binaries**: Pre-compiled standalone native binaries for Linux (x64, ARM64) and macOS (ARM64 Apple Silicon, x64).
- [ ] **Standard Library Expansion**: Additional standard library modules (`std/json.vakya`, `std/os.vakya`, `std/path.vakya`).
- [ ] **Enhanced Bytecode Optimizations**: Constant folding pass, dead code elimination, and peephole jump chain flattening.

---

## 3. Planned (v0.3.0 - v0.5.0)

- [ ] **Direct LLVM IR & Cranelift Backend**: Native code generation without intermediate C compilation for ultra-fast native binaries.
- [ ] **Language Server Protocol (LSP)**: `vakya-lsp` providing diagnostics, hover information, autocomplete, and go-to-definition.
- [ ] **Official VS Code Extension**: Syntax highlighting, snippet library, and LSP integration.
- [ ] **Package Manager (`sutra`)**: Decentralized package dependency resolver and project manager.

---

## 4. Long-Term Vision (v1.0.0)

- [ ] **Native Concurrency Model (`sahakarya`)**: Structured concurrency, message-passing channels, and thread safety.
- [ ] **WebAssembly (`wasm32-unknown-unknown`) Target**: Direct browser compilation and execution.
- [ ] **Formal Language Specification & ABI Freeze**: 1.0 stability guarantees and backward compatibility policy.
