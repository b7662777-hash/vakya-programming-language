# Vākya Diagnostic Error Codes Catalog

This document is the authoritative reference for all compiler, typechecker, and runtime error codes in the **Vākya Programming Language**.

---

## 1. Master Error Code Index

| Code | Title | Phase | Description & Fix |
| :--- | :--- | :--- | :--- |
| **`E001`** | Invalid character | Lexer | Character unrecognized by the lexer. Remove or replace it. |
| **`E002`** | Unterminated string literal | Lexer | String literal is missing a closing double quote (`"`). |
| **`E003`** | Unterminated multi-line comment | Lexer | Multi-line comment missing `*/` closing delimiter. |
| **`E004`** | Invalid escape sequence | Lexer | Unrecognized escape sequence inside a string literal. |
| **`E005`** | Invalid number literal | Lexer | Malformed integer or decimal format (e.g. `123abc`). |
| **`E101`** | Undefined variable | Type/Runtime | Identifier used without prior declaration via `chara` or `dhruva`. |
| **`E102`** | Undefined function | Type/Runtime | Function invoked without prior definition via `karya`. |
| **`E103`** | Cannot reassign constant | Type/Runtime | Attempted reassignment of an immutable `dhruva` constant. |
| **`E104`** | Variable already declared | Type/Runtime | Variable redeclared within the exact same lexical scope. |
| **`E105`** | Invalid assignment target | Parser | Left-hand side of `=` is not a valid assignable L-value. |
| **`E201`** | Unexpected token | Parser | Token encountered where another syntax was expected. |
| **`E202`** | Expected token | Parser | Missing required punctuation (e.g., closing `}`, `)`, `]`). |
| **`E203`** | Expected expression | Parser | Expression expected but not provided. |
| **`E204`** | Invalid parameter declaration | Parser | Parameter is not a valid identifier or has invalid syntax. |
| **`E205`** | Invalid loop syntax | Parser | Malformed `yavat` condition or `pratyekam ... madhye` statement. |
| **`E206`** | Loop control outside loop | Parser | `virama` or `agaccha` used outside a loop block. |
| **`E207`** | Return outside function | Parser | `pratyavartaya` used outside a function body. |
| **`E301`** | Division by zero | Runtime/VM | Division (`/`) or modulo (`%`) divisor evaluated to `0`. |
| **`E302`** | Index out of bounds | Runtime/VM | Collection index is outside valid range `[0, length - 1]`. |
| **`E303`** | Key not found in map | Runtime/VM | Attempted access to non-existent key in a `naksha` (map). |
| **`E304`** | Recursion limit exceeded | Runtime/VM | Call stack recursion limit reached without terminating base case. |
| **`E305`** | Value is not callable | Runtime/VM | Attempted to invoke a non-function value with `()`. |
| **`E306`** | Invalid runtime operation | Runtime/VM | Operation applied to incompatible runtime types. |
| **`E307`** | Unknown property access | Runtime/VM | Attempted access to unsupported member (e.g. `.length` on number). |
| **`E401`** | Type mismatch | Type Checker | Initializer or assigned value doesn't match variable type. |
| **`E402`** | Argument type mismatch | Type Checker | Function argument does not match parameter type annotation. |
| **`E403`** | Return type mismatch | Type Checker | Return expression doesn't match annotated function return type. |
| **`E404`** | Incompatible operand types | Type Checker | Binary operator cannot be applied to operand types. |
| **`E405`** | Incompatible unary operand | Type Checker | Unary operator (e.g. `-`) cannot be applied to operand type. |
| **`E406`** | Incorrect number of arguments | Type/Runtime | Function called with more or fewer arguments than expected. |
| **`E407`** | Type is not indexable | Type/Runtime | Indexing (`[]`) applied to non-collection type. |
| **`E501`** | Use of moved value | Borrow Checker | Variable accessed after its ownership was transferred. |
| **`E502`** | Mutable borrow conflict | Borrow Checker | Attempted mutable borrow while shared immutable borrows are active. |
| **`E503`** | Multiple mutable borrows | Borrow Checker | Attempted to create more than one exclusive mutable borrow. |
| **`E504`** | Dangling local reference | Borrow Checker | Returning reference to local variable allocated on stack frame. |
| **`E505`** | Mutation while borrowed | Borrow Checker | Resource mutated or reassigned while actively borrowed. |

---

## 2. Diagnostic Format Example

When an error is reported, Vākya emits a formatted diagnostic with line numbers, code snippets, caret highlights, and actionable help:

```text
Error [E103]: Cannot reassign constant 'max_users'

  --> app.vakya:5:1

 4 | dhruva max_users: sankhya = 100
 5 | max_users = 200
   | ^^^^^^^^^
 6 | vada(max_users)

Help: Constants declared with 'dhruva' are immutable. Use 'chara' for mutable variables.
```
