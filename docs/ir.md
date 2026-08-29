# Vākya Intermediate Representation (IR) Specification

## 1. Overview & Principles

Vākya Linear IR (`src/vakya/ir/`) is a target-independent, 3-address virtual-register intermediate representation. It forms the clean abstraction boundary separating the validated frontend AST from execution backends (Bytecode Compiler, Native C Emitter, LLVM Emitter).

```text
               AST (Abstract Syntax Tree)
                           │
             Type & Borrow Checker Verification
                           │
                     IR Lowering (IRBuilder)
                           │
                           ▼
                    Vākya Linear IR
               ┌───────────┴───────────┐
               ▼                       ▼
      Bytecode Compiler         Native Backend (C / LLVM)
               │                       │
      Bytecode VM Execution    Native Machine Binary
```

---

## 2. Virtual Register Model

* **Virtual Registers**: Unlimited pseudo-registers `%t0`, `%t1`, `%t2`, ... allocated sequentially during expression lowering.
* **Variable References**: Named variable slots `%var_name` mapped directly to stack locations or memory cells.
* **Basic Blocks & Labels**: Linear instruction streams demarcated by explicit jump targets (`label_entry`, `loop_start_0`, `else_1`).

---

## 3. Instruction Set Architecture

| Instruction | Format | Description |
| :--- | :--- | :--- |
| **`IRConst`** | `%dest = const <type> <val>` | Load constant literal into virtual register. |
| **`IRLoad`** | `%dest = load <var>` | Load variable value into virtual register. |
| **`IRStore`** | `store <var>, %src` | Write register value into variable slot. |
| **`IRBinOp`** | `%dest = <op> %left, %right` | Binary arithmetic/comparison (`add`, `sub`, `mul`, `div`, `mod`, `pow`, `eq`, `ne`, `lt`, `le`, `gt`, `ge`). |
| **`IRUnaryOp`**| `%dest = <op> %src` | Unary negation (`neg`) or logical inversion (`not`). |
| **`IRLabel`** | `<name>:` | Declares a branch/jump target label. |
| **`IRJump`** | `jump <target>` | Unconditional control flow transfer. |
| **`IRBranch`** | `br %cond, <true_lbl>, <false_lbl>` | Conditional two-way branch. |
| **`IRCall`** | `[%dest =] call <fn>(%arg1, ...)` | Function call invocation. |
| **`IRReturn`** | `ret [%val]` | Return control (and optional value) to caller. |
| **`IRAllocList`**| `%dest = alloc_list [%e0, ...]` | Allocate heap dynamic array. |
| **`IRGetIndex`**| `%dest = get_index %tgt, %idx` | Read element at index. |
| **`IRSetIndex`**| `set_index %tgt, %idx, %val` | Write element at index. |

---

## 4. Lowering Example

```vakya
karya yog(a: sankhya, b: sankhya) -> sankhya {
    pratyavartaya a + b
}
```

Lowers to Linear IR:

```text
function yog(a, b):
    %t1 = load a
    %t2 = load b
    %t3 = add %t1, %t2
    ret %t3
```
