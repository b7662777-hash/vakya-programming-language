# Vākya Evolution Roadmap

## V1.0 (Current) — Foundations & Core Interpreted Language
- [x] Handwritten Lexer & Recursive-Descent Parser
- [x] AST Representation with exact source spans
- [x] Static Type Checker & Local Type Inference
- [x] Tree-Walking Interpreter with Lexical Scoping
- [x] Primitive Data Types (`sankhya`, `dashamika`, `shabda`, `boolean`, `suchi`, `naksha`, `shunya`)
- [x] Structured Diagnostics & Error System with Carets
- [x] Deterministic Code Formatter (`vakya fmt`)
- [x] Interactive REPL (`vakya repl`)
- [x] CLI Tool (`vakya run`, `vakya check`, `vakya fmt`, `vakya test`)
- [x] Comprehensive Automated Test Suite (>90% coverage)

---

## V1.1 — Ergonomics & Multilingual Alias Prototype
- [ ] Multilingual Token Alias Engine (Devanagari aliases: `chara` → `चर`, `karya` → `कार्य`, `vada` → `वद`)
- [ ] Extended Standard Library (math, string formatting, date/time)
- [ ] Language Server Protocol (LSP) prototype for VS Code syntax highlighting and diagnostics
- [ ] Rich doc-comment generator

---

## V2.0 Alpha (Current) — Bytecode Virtual Machine Architecture
- [x] Stack-based Bytecode Virtual Machine (`VirtualMachine`, `ValueStack`, `CallFrame`)
- [x] AST-to-Bytecode Compiler (`BytecodeCompiler`, `Chunk`, `Instruction`, `OpCode`)
- [x] Upvalue-based Lexical Closures & mutable environments
- [x] Bytecode Disassembler CLI (`vakya disasm <file.vakya>`)
- [x] Dual-engine execution support (`--engine=vm` (default), `--engine=interpreter`)
- [x] Execution tracing (`--trace`)
- [x] Differential Conformance Test Suite (>300 tests)
- [ ] Module system (`aayat`) and package manager
- [ ] Capability-based security model (`anumati filesystem.read`, `anumati network.connect`)
- [ ] Structured concurrency primitives

---

## V3 — Native Compiler & Memory Safety
- [ ] Native compiler backend via LLVM or Cranelift
- [ ] Compile directly to standalone native machine binaries (`.exe`, ELF, Mach-O)
- [ ] Memory safety system (ownership and borrow checking without garbage collection)
- [ ] Foreign Function Interface (FFI) with C / Rust
- [ ] Whole-program optimization and dead code elimination
