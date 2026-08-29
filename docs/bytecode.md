# Vākya Bytecode & Instruction Set Specification (V2)

## 1. Chunk & Constant Pool Structure

A `Chunk` represents a compiled unit of bytecode instructions and its associated metadata:

- **`constants`**: Pool of deduplicated literal values (integers, floats, strings, nested function chunks).
- **`instructions`**: Linear array of `Instruction` records `(opcode, operand, span)`.
- **`param_names`**: Parameter names for function invocations.
- **`num_locals`**: Number of local stack slots required by the function.
- **`upvalues`**: List of captured enclosing bindings `(is_local: bool, index: int, name: str)`.

---

## 2. OpCode Reference Table

| Opcode | Operand | Description |
| :--- | :--- | :--- |
| `CONSTANT` | `index: int` | Push constant pool value at `index` onto stack. |
| `NULL` | None | Push `shunya` (None) onto stack. |
| `TRUE` | None | Push `satya` (True) onto stack. |
| `FALSE` | None | Push `asatya` (False) onto stack. |
| `POP` | None | Pop top value from stack. |
| `DUP` | None | Duplicate top value on stack. |
| `LOAD_LOCAL` | `slot: int` | Push local variable from slot `slot`. |
| `STORE_LOCAL`| `slot: int` | Pop value from stack and store into local slot `slot`. |
| `LOAD_GLOBAL`| `name: str` | Push global variable `name` onto stack. |
| `STORE_GLOBAL`| `name: str`| Pop value from stack and store into global `name`. |
| `LOAD_UPVALUE`| `index: int`| Push captured upvalue at `index` onto stack. |
| `STORE_UPVALUE`| `index: int`| Pop value from stack and store into captured upvalue. |
| `ADD` | None | Pop `b`, pop `a`, push `a + b` (numbers or string concatenation). |
| `SUBTRACT` | None | Pop `b`, pop `a`, push `a - b`. |
| `MULTIPLY` | None | Pop `b`, pop `a`, push `a * b` (numbers or string repetition). |
| `DIVIDE` | None | Pop `b`, pop `a`, push `a / b` (raises E301 on zero). |
| `MODULO` | None | Pop `b`, pop `a`, push `a % b` (raises E301 on zero). |
| `POWER` | None | Pop `b`, pop `a`, push `a ** b` (right-associative). |
| `NEGATE` | None | Pop `a`, push `-a`. |
| `NOT` | None | Pop `a`, push `not is_truthy(a)`. |
| `EQUAL` | None | Pop `b`, pop `a`, push `a == b` (strict boolean typing). |
| `NOT_EQUAL` | None | Pop `b`, pop `a`, push `a != b` (strict boolean typing). |
| `LESS` | None | Pop `b`, pop `a`, push `a < b`. |
| `LESS_EQUAL`| None | Pop `b`, pop `a`, push `a <= b`. |
| `GREATER` | None | Pop `b`, pop `a`, push `a > b`. |
| `GREATER_EQUAL`| None | Pop `b`, pop `a`, push `a >= b`. |
| `JUMP` | `target: int` | Unconditional jump to instruction index `target`. |
| `JUMP_IF_FALSE`| `target: int` | Pop condition; if falsy, jump to `target`. |
| `JUMP_IF_TRUE`| `target: int` | Pop condition; if truthy, jump to `target`. |
| `JUMP_IF_FALSE_OR_POP`| `target: int` | Peek condition; if falsy jump, else pop. |
| `JUMP_IF_TRUE_OR_POP`| `target: int` | Peek condition; if truthy jump, else pop. |
| `BUILD_LIST` | `count: int` | Pop `count` items and push new `suchi` list. |
| `BUILD_MAP` | `pair_count: int` | Pop `2 * pair_count` items and push new `naksha` map. |
| `INDEX` | None | Pop `idx`, pop `target`, push `target[idx]`. |
| `SET_INDEX` | None | Pop `val`, pop `idx`, pop `target`, set `target[idx] = val`. |
| `GET_MEMBER`| `name: str` | Pop `target`, push property `target.name` (e.g. `.length`). |
| `MAKE_CLOSURE`| `const_idx: int`| Instantiate `VMClosure` with captured upvalues from constant chunk. |
| `CALL` | `argc: int` | Pop `argc` arguments, pop callee, invoke function closure. |
| `CALL_BUILTIN`| `(name, argc)` | Optimized invocation of native builtin function. |
| `RETURN` | None | Pop return value, tear down CallFrame, push return value to caller. |
| `HALT` | None | Terminate top-level program execution and return final result. |

---

## 3. Disassembly Example

```text
=== Bytecode Disassembly: <main> (params=0, locals=1, upvalues=0) ===
Constants:
  [00] <Chunk: fibonacci>
  [01] 'Recursive Fibonacci of 7:'
  [02] 7
Instructions:
    3: 0000  MAKE_CLOSURE       0 (<Chunk: fibonacci>)
    | 0001  STORE_GLOBAL       fibonacci
   13: 0002  CONSTANT           1 ('Recursive Fibonacci of 7:')
    | 0003  CALL_BUILTIN       vada (args: 1)
    | 0004  POP
   14: 0005  LOAD_GLOBAL        fibonacci
    | 0006  CONSTANT           2 (7)
    | 0007  CALL               1
    | 0008  CALL_BUILTIN       vada (args: 1)
    | 0009  POP
    | 0010  NULL
    | 0011  HALT
```
