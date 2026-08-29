# Vākya Virtual Machine Architecture (V2)

## Overview

Vākya V2 introduces a custom stack-based **Bytecode Virtual Machine (VM)** designed for efficient, predictable execution of Vākya programs.

```
Source (.vakya)
      │
      ▼
    Lexer
      │
      ▼
    Parser ──► AST
      │
      ▼
 TypeChecker ──► Validated AST
      │
      ▼
BytecodeCompiler ──► Chunk (Bytecode & Constants)
      │
      ▼
VirtualMachine (Value Stack, Call Frames, Upvalues)
```

---

## 1. Core VM Subsystems

### A. Value Stack (`ValueStack`)
- Stores operands, intermediate computation results, and function arguments.
- Protected against stack overflow with configurable stack limits (default 4096).
- Supports $O(1)$ push, pop, and index inspection.

### B. Call Frames (`CallFrame`)
- Each function call allocates an isolated `CallFrame`.
- A `CallFrame` encapsulates:
  - `chunk`: The compiled function `Chunk`.
  - `closure`: The associated `VMClosure` enclosing instance.
  - `ip`: Instruction pointer pointing to current bytecode offset.
  - `locals`: $O(1)$ array of local variable slots.
  - `open_upvalues`: Open upvalues captured by nested inner closures.

### C. Lexical Scoping & Closures (`VMClosure` & `UpvalueCell`)
- Closures capture outer lexical variables using `UpvalueCell` objects.
- When an inner function references an enclosing local, the compiler assigns an upvalue descriptor `(is_local, slot_index)`.
- Multiple closures referencing the same enclosing variable share the identical `UpvalueCell`, allowing synchronized mutable state across closures.

### D. Global Symbol Table & Builtins
- Top-level variables and functions are stored in the VM's global dictionary.
- Native standard builtins (`vada`, `puchha`, `lamba`, `prakaar`, `suchi_jodo`, `suchi_hatao`, `shabda_bada`, `shabda_chhota`, `shabda_trim`) are pre-populated and accessible globally or via `CALL_BUILTIN` bytecode optimizations.

---

## 2. CLI Execution & Inspection

### Run with Bytecode VM (Default)
```bash
vakya run program.vakya
# or explicitly
vakya run program.vakya --engine=vm
```

### Run with Reference AST Interpreter
```bash
vakya run program.vakya --engine=interpreter
```

### Execution Instruction Tracing
```bash
vakya run program.vakya --trace
```

### Disassemble Bytecode to Assembly
```bash
vakya disasm program.vakya
```

---

## 3. Error Handling and Diagnostics

All runtime VM exceptions map back to source lines and columns using the `Span` metadata attached to each bytecode instruction:

- `E301`: Division or Modulo by zero
- `E302`: Index out of bounds (suchi / shabda)
- `E303`: Key not found in map (naksha)
- `E304`: Recursion / stack depth limit exceeded
- `E305`: Non-callable value invocation
- `E306`: Runtime type mismatch
- `E307`: Invalid property or member access
- `E406`: Function argument count mismatch
