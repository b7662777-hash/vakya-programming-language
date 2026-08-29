# Vākya Subsystem Implementation Status Matrix (V3.1 Audit)

Every major subsystem of the Vākya programming language is classified below according to strict empirical verification:

| Classification | Meaning |
| :--- | :--- |
| **`IMPLEMENTED + TESTED`** | Fully implemented in source code with dedicated automated test coverage passing 100%. |
| **`IMPLEMENTED`** | Implemented in source code, basic tests present, awaiting exhaustive edge-case coverage. |
| **`PROTOTYPE`** | Working functional prototype; executes key scenarios but has architectural simplifications. |
| **`PARTIAL`** | Some components written, but cannot yet run end-to-end autonomously. |
| **`DESIGN ONLY`** | Formal design specification exists in documentation; no runtime code written yet. |
| **`DOCUMENTATION ONLY`** | High-level conceptual notes without formal technical specification or code. |
| **`NOT IMPLEMENTED`** | Planned feature with neither specification nor code. |

---

## Master Subsystem Status Table

| Subsystem | Status | Path / Implementation | Test Coverage |
| :--- | :--- | :--- | :--- |
| **Lexer** | `IMPLEMENTED + TESTED` | `src/vakya/lexer/lexer.py` | 100% (Keywords, spans, strings, comments) |
| **Parser** | `IMPLEMENTED + TESTED` | `src/vakya/parser/parser.py` | 100% (Recursive-descent, operator precedence) |
| **AST** | `IMPLEMENTED + TESTED` | `src/vakya/ast/nodes.py` | 100% (21 Dataclass nodes with source spans) |
| **Type Checker** | `IMPLEMENTED + TESTED` | `src/vakya/typechecker/checker.py` | 100% (Static inference, annotations, scopes) |
| **Borrow Checker** | `IMPLEMENTED + TESTED` | `src/vakya/typechecker/borrow_checker.py` | 100% (Move semantics `E501`, borrow conflicts `E502-E505`) |
| **AST Interpreter** | `IMPLEMENTED + TESTED` | `src/vakya/interpreter/interpreter.py` | 100% (Reference tree-walking execution engine) |
| **Bytecode Compiler** | `IMPLEMENTED + TESTED` | `src/vakya/bytecode/compiler.py` | 100% (Opcodes, constant pool, jump patching) |
| **Bytecode VM** | `IMPLEMENTED + TESTED` | `src/vakya/vm/vm.py` | 100% (Flat integer opcode dispatch, call frames) |
| **Linear IR** | `IMPLEMENTED + TESTED` | `src/vakya/ir/` | 100% (3-address virtual registers, CFG builder) |
| **Native C Backend** | `IMPLEMENTED + TESTED` | `src/vakya/native/c_emitter.py` | 100% (ANSI C99 emitter + host CC compiler driver) |
| **LLVM Backend** | `PARTIAL` / `PROTOTYPE` | `src/vakya/native/llvm_backend.py` | Text LLVM IR generator prototype |
| **Cranelift Backend** | `DESIGN ONLY` | `docs/native-backend-decision.md` | Architecture evaluated; code deferred to V4 |
| **Native Runtime** | `IMPLEMENTED + TESTED` | `runtime/` (`memory`, `strings`, `collections`, `io`, `panic`) | Standalone C runtime headers with memory tracking |
| **Ownership (*Swamitva*)** | `IMPLEMENTED + TESTED` | `src/vakya/typechecker/borrow_checker.py` | Affine move semantics on heap types |
| **Lexical Borrowing** | `IMPLEMENTED + TESTED` | `src/vakya/typechecker/borrow_checker.py` | Shared `pashya` vs unique `chara` loans |
| **Standard Library** | `IMPLEMENTED + TESTED` | `std/` (`core`, `math`, `strings`, `collections`, `io`, `time`) | 6 Pure Vākya stdlib modules |
| **Module Loader** | `IMPLEMENTED + TESTED` | `src/vakya/modules/loader.py` | Relative imports, cycle detection, caching |
| **CLI** | `IMPLEMENTED + TESTED` | `src/vakya/cli.py` | `run`, `build`, `new`, `check`, `fmt`, `repl`, `test` |
| **Formatter** | `IMPLEMENTED + TESTED` | `src/vakya/formatter/formatter.py` | AST-based idempotent code formatting |
| **REPL** | `IMPLEMENTED + TESTED` | `src/vakya/repl/repl.py` | Interactive shell with persistent environment |
| **Diagnostics System** | `IMPLEMENTED + TESTED` | `src/vakya/errors/` | ANSI formatted spans with code catalog `E001-E505` |
| **Three-Engine Differential** | `IMPLEMENTED + TESTED` | `tests/differential/` | Interpreter == VM == Native emission verified |
| **LSP / Language Server** | `NOT IMPLEMENTED` | Planned | Deferred post-native compiler baseline |
| **Interactive Debugger** | `NOT IMPLEMENTED` | Planned | Source mapping foundations laid |
| **Native Profiler** | `NOT IMPLEMENTED` | Planned | Standard Python/C profilers used currently |
| **WebAssembly Target** | `DESIGN ONLY` | `docs/native-backend-decision.md` | IR designed for WASM lowering |
| **Package Manager** | `PARTIAL` | `vakya.toml` scaffolding in CLI | Remote package registry not yet built |
| **Concurrency / Tasks** | `DESIGN ONLY` | `docs/concurrency.md` | Shared-nothing message passing designed |
| **Security Capabilities** | `DESIGN ONLY` | `docs/security-model.md` | Explicit permission capabilities designed |

---

## Showcase Applications Status

1. **01 Name Program** (`showcase/01_name_program/`): `IMPLEMENTED + TESTED` — Pure Vākya application.
2. **02 Calculator** (`showcase/02_calculator/`): `IMPLEMENTED + TESTED` — Pure Vākya application.
3. **03 Mini Browser** (`showcase/03_browser/`): `PROTOTYPE` — Vākya core logic with Python host bridge for rendering.
