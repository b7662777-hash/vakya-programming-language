# Vākya V3 Language Baseline & Specification Freeze

## 1. Specification Baseline Status

The language specification of **Vākya** is hereby frozen for the V3 Native Compiler implementation. No arbitrary syntax changes or keyword additions will be made during native code generation and memory safety engineering.

---

## 2. Core Grammar & Syntax Reference

### 2.1 Keyword Registry (33 Keywords)
| Keyword | Category | Role |
| :--- | :--- | :--- |
| `chara` | Declaration | Mutable variable declaration / mutable borrow |
| `dhruva` | Declaration | Immutable constant declaration |
| `karya` | Declaration | Function declaration |
| `pratyavartaya` | Control Flow | Return from function |
| `yadi` | Control Flow | If condition |
| `anyatha` | Control Flow | Else branch |
| `yavat` | Control Flow | While loop |
| `pratyekam` | Control Flow | For-each loop element binding |
| `madhye` | Control Flow | For-each collection specifier |
| `virama` | Control Flow | Break from loop |
| `agaccha` | Control Flow | Continue to next loop iteration |
| `pashya` | Memory Safety | Shared read-only borrow |
| `satya` | Literal | Boolean true |
| `asatya` | Literal | Boolean false |
| `shunya` | Literal | Null value |
| `evam` | Operator | Short-circuit logical AND |
| `va` | Operator | Short-circuit logical OR |
| `na` | Operator | Logical NOT |
| `sankhya` | Type | 64-bit integer |
| `dashamika` | Type | Double-precision float |
| `shabda` | Type | String text |
| `boolean` | Type | Boolean truth value |
| `suchi` | Type | Dynamic array / list |
| `naksha` | Type | Key-value associative map |

### 2.2 Operators & Precedence (8 Levels)
1. **Level 1 (Lowest)**: `evam`, `va`
2. **Level 2**: `==`, `!=`
3. **Level 3**: `<`, `<=`, `>`, `>=`
4. **Level 4**: `+`, `-`
5. **Level 5**: `*`, `/`, `%`
6. **Level 6**: `**` (Power, right-associative)
7. **Level 7**: `-` (unary negation), `na` (logical NOT)
8. **Level 8 (Highest)**: Calls `()`, Indexing `[]`, Member access `.`

---

## 3. Native Target Architecture

```text
Vākya Source (.vakya)
        │
    Frontend (Lexer, Parser, Type Checker)
        │
  Borrow Checker (Swamitva Ownership & Lifetimes)
        │
   Vākya Linear IR (SSA-ready 3-Address Virtual Registers)
        │
   ┌────┴───────────────────────────┐
   ▼                                ▼
Bytecode VM Backend          Native Backend (LLVM / Cranelift / Native C)
                                    │
                             Native Executable
```
