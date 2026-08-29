# Vākya V2 Full Architecture & Subsystem Audit

This document presents a comprehensive audit of all 14 core subsystems in the Vākya codebase.

---

## Subsystem 1: Lexer (`src/vakya/lexer/`)
- **Purpose**: Tokenize UTF-8 Romanized Sanskrit source text into structured `Token` streams with source spans.
- **Inputs**: Raw string `source_code`, optional `filename`.
- **Outputs**: `List[Token]` (tokens containing `TokenType`, literal values, line numbers, column numbers, and length).
- **Dependencies**: `src/vakya/language/keywords.py`, `src/vakya/errors/`.
- **Performance**: High throughput: ~688,000+ tokens/sec.
- **Known Limitations**: Single-character lookahead; Unicode escape sequences not yet expanded beyond ASCII escapes.
- **Tests**: `tests/lexer/test_lexer.py` (52 tests).

---

## Subsystem 2: Parser (`src/vakya/parser/`)
- **Purpose**: Recursive-descent predictive parsing constructing an Abstract Syntax Tree (AST).
- **Inputs**: `List[Token]`.
- **Outputs**: `Program` AST node root.
- **Dependencies**: `src/vakya/ast/nodes.py`, `src/vakya/errors/`.
- **Performance**: ~9,800+ parses/sec.
- **Known Limitations**: Panic-mode recovery synchronizes on statement boundaries; does not perform full error correction.
- **Tests**: `tests/parser/test_parser.py` (50 tests).

---

## Subsystem 3: Abstract Syntax Tree (`src/vakya/ast/nodes.py`)
- **Purpose**: Typed dataclass hierarchy representing all 21 grammar constructs.
- **Inputs**: Constructed by Parser.
- **Outputs**: Consumed by TypeChecker, BytecodeCompiler, Interpreter, Formatter, and IRBuilder.
- **Dependencies**: None (pure data model).
- **Performance**: Zero-copy node representations.
- **Tests**: Validated through parser and compiler suites.

---

## Subsystem 4: Static Type Checker (`src/vakya/typechecker/`)
- **Purpose**: Pre-execution verification of variable scopes, type compatibility, immutability, and function signatures.
- **Inputs**: `Program` AST.
- **Outputs**: Type-annotated / validated AST (or raises `TypeError` / `NameError` / `ConstantError`).
- **Dependencies**: `src/vakya/ast/nodes.py`, `src/vakya/errors/`.
- **Performance**: Fast single-pass symbol table and expression inference.
- **Known Limitations**: Structural subtyping for maps is unconstrained at compile time.
- **Tests**: `tests/typechecker/test_typechecker.py` (22 tests).

---

## Subsystem 5: Bytecode Compiler (`src/vakya/bytecode/`)
- **Purpose**: Compiles validated AST into discrete `Chunk` bytecode containers with local variable slot resolution and upvalue capture descriptors.
- **Inputs**: `Program` AST.
- **Outputs**: `Chunk` containing `instructions`, `constants`, `num_locals`, and `upvalues`.
- **Dependencies**: `src/vakya/bytecode/opcodes.py`, `src/vakya/bytecode/instructions.py`.
- **Performance**: ~67,000+ AST-to-bytecode compiles/sec.
- **Known Bottlenecks**: Heavy instruction objects created per bytecode step; constant folding not yet active.
- **Tests**: `tests/vm/test_vm_instructions.py` (28 tests).

---

## Subsystem 6: Virtual Machine (`src/vakya/vm/`)
- **Purpose**: Stack-based execution engine with discrete call frames, pre-allocated local variable arrays, and lexical closures.
- **Inputs**: Compiled `Chunk`.
- **Outputs**: Return value, standard output side-effects.
- **Dependencies**: `src/vakya/bytecode/`, `src/vakya/vm/runtime.py`, `src/vakya/vm/frames.py`.
- **Performance**: Slower than AST interpreter due to object wrapper overhead in Python (0.34x–0.44x interpreter speed).
- **Target Bottlenecks**:
  1. Opcode enum dispatch inside `_run_frames()`.
  2. Object attribute lookups (`instr.opcode`, `instr.operand`, `instr.span`).
  3. Dynamic stack bounds checking per push/pop.
  4. CallFrame allocation per function call.
- **Tests**: `tests/vm/test_vm_core.py` (14 tests), `tests/differential/test_differential.py` (11 tests).

---

## Subsystem 7: Intermediate Representation (`src/vakya/ir/`)
- **Purpose**: Language-agnostic virtual-register 3-address IR bridging AST to multiple backends.
- **Inputs**: `Program` AST.
- **Outputs**: `IRModule` containing linear `IRInstruction` streams.
- **Dependencies**: `src/vakya/ast/nodes.py`.
- **Performance**: Fast linear generation; zero host recursion.
- **Tests**: `tests/ir/test_ir.py` (4 tests).

---

## Subsystem 8: Module Loader (`src/vakya/modules/`)
- **Purpose**: Resolves module file paths, detects circular imports, compiles modules into VM chunks, and extracts exports.
- **Inputs**: Module name / path.
- **Outputs**: Dictionary of exported global bindings.
- **Dependencies**: Lexer, Parser, TypeChecker, BytecodeCompiler, VM.
- **Tests**: `tests/modules/test_modules.py` (3 tests).

---

## Subsystem 9: Standard Library (`std/`)
- **Purpose**: Canonical pure Vākya modules for math, strings, collections, and I/O.
- **Inputs**: `.vakya` source files in `std/`.
- **Outputs**: High-level reusable utility functions (`varga`, `ghana`, `parama_mana`, `jodo_sarva`, `shabda_viparita`).
- **Tests**: Loaded and executed in module test suite.

---

## Subsystem 10: Command Line Interface (`src/vakya/cli.py`)
- **Purpose**: User-facing entry point for `run`, `check`, `disasm`, `fmt`, `errors`, `repl`, `test`, and `version`.
- **Outputs**: Text diagnostics, formatted source, or machine-readable JSON (`--format=json`).
- **Tests**: `tests/integration/test_cli.py`.

---

## Subsystem 11: Formatter (`src/vakya/formatter/`)
- **Purpose**: Canonical code formatting adhering to Vākya style guide with idempotency guarantee (`format(format(x)) == format(x)`).
- **Tests**: `tests/formatter/test_formatter.py`.

---

## Subsystem 12: REPL (`src/vakya/repl/`)
- **Purpose**: Interactive Read-Eval-Print Loop with multi-line block accumulation and persistent global state.
- **Tests**: `tests/integration/test_repl.py`.

---

## Subsystem 13: Error Diagnostics (`src/vakya/errors/`)
- **Purpose**: Catalog of structured errors (`E001`–`E407`) with source gutters, carets, error codes, and remediation advice.
- **Tests**: `tests/diagnostics/test_diagnostics.py`.

---

## Subsystem 14: Differential Testing Harness (`tests/differential/`)
- **Purpose**: Automated side-by-side verification asserting 100% identical outputs and error codes between AST Interpreter and Bytecode VM.
- **Tests**: `tests/differential/test_differential.py`.
