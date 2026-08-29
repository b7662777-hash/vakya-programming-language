# Vākya VM Memory Architecture & Runtime Model

## 1. Overview

The **Vākya Bytecode Virtual Machine (V2)** uses a stack-based execution model with discrete call frames, local variable slot arrays, heap-allocated reference types, and `UpvalueCell` wrappers for lexical closures.

```
┌─────────────────────────────────────────────────────────────┐
│                     VĀKYA VM RUNTIME                        │
│                                                             │
│  ┌───────────────────────┐       ┌───────────────────────┐  │
│  │     VALUE STACK       │       │      CALL STACK       │  │
│  │   [Operand Buffer]    │       │     [CallFrames]      │  │
│  │   - Constants         │       │   - Frame 0 (top)     │  │
│  │   - Temp results      │       │   - Frame 1 (caller)  │  │
│  │   - Limit: 4096       │       │   - Limit: 200 depth  │  │
│  └───────────────────────┘       └───────────────────────┘  │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                      HEAP OBJECTS                     │  │
│  │   - suchi (Lists)           - naksha (Hash Maps)      │  │
│  │   - shabda (Strings)        - UpvalueCell (Closures)  │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Value Stack (`ValueStack`)

- **Role**: Operands for arithmetic, logic, comparison, function arguments, and return values are pushed and popped from a continuous array.
- **Protection**: The stack enforces a configurable `max_stack_size` (default: 4096 elements). Exceeding this boundary raises `Error [E304]: Value stack overflow` rather than causing an uncontrolled host crash.

---

## 3. Call Frames (`CallFrame`)

Every function invocation pushes a new `CallFrame` onto the VM call stack:
- **`chunk`**: The bytecode container being executed.
- **`ip`**: Instruction Pointer offset within the chunk.
- **`locals`**: Pre-allocated array of local variable slots for $O(1)$ variable reads and writes (`LOAD_LOCAL`, `STORE_LOCAL`).
- **`open_upvalues`**: Registry of active captured local slots.

### Call Depth Limit
The call stack depth is bounded by `max_call_depth` (default: 200). If recursive functions exceed this threshold without reaching a base condition, the VM halts execution and emits:
```text
Error [E304]: Maximum recursion depth exceeded
```

---

## 4. Upvalues and Lexical Closures (`UpvalueCell` & `VMClosure`)

Vākya implements lexical closures through upvalue cells:
1. **Open Upvalues**: While an outer function's frame is active on the call stack, captured variables point to shared `UpvalueCell` objects registered in `frame.open_upvalues`.
2. **Mutations**: Multiple inner closures capturing the same outer variable share the identical `UpvalueCell`. Mutations performed inside one closure (`STORE_UPVALUE`) are immediately observable in all other closures.
3. **Escaped Closures**: When the outer function returns and its `CallFrame` is popped, the `UpvalueCell` persists in memory for as long as any inner closure references it.

---

## 5. Heap Reference Types

- **`suchi` (Lists)**: Dynamic array references. Modifying elements (`INDEX_SET`, `suchi_jodo`, `suchi_hatao`) mutates the underlying list in place.
- **`naksha` (Maps)**: Key-value associative hash tables indexed by string keys.
- **`shabda` (Strings)**: UTF-8 encoded text sequences.
