# Vākya Error Catalog

The **Vākya Error System** produces standard, machine-readable diagnostic codes with contextual source line highlights, column positions, and actionable remediation hints.

---

## 1. Error Categories & Code Ranges

| Category | Range | Subsystem |
| :--- | :--- | :--- |
| **Lexical Errors** | `E001`–`E099` | Lexer (tokenization, numbers, strings) |
| **Syntax & Grammar** | `E101`–`E199` | Parser (structure, delimiters, grammar rules) |
| **Runtime Exceptions**| `E301`–`E399` | Virtual Machine & Interpreter execution |
| **Type Checking** | `E401`–`E499` | Static Type Checker (inference, mismatches) |
| **Swamitva Ownership**| `E501`–`E599` | Swamitva Borrow Checker (moves, borrows) |

---

## 2. Complete Error Registry

### Lexical Errors (`E001`–`E099`)
- **`E001: Invalid Character`** — Source contains a character not recognized by the lexer.
- **`E002: Unterminated String`** — String literal missing closing quotation mark `"`.
- **`E003: Invalid Number Format`** — Malformed integer or float (e.g. multiple decimal points).

### Syntax Errors (`E101`–`E199`)
- **`E101: Unexpected Token`** — Token encountered where another was expected.
- **`E102: Expected Token`** — Specific delimiter or keyword missing (e.g. missing `}` or `)`).
- **`E103: Expected Expression`** — Expression expected following an operator or clause.
- **`E104: Invalid Parameter List`** — Malformed parameter list in function declaration.
- **`E105: Invalid Assignment Target`** — Attempted assignment to a literal or expression.
- **`E106: Invalid Loop Syntax`** — Loop declaration missing target condition or collection.

### Runtime Errors (`E301`–`E399`)
- **`E301: Division by Zero`** — Integer or floating-point division by `0`.
- **`E302: Index Out of Bounds`** — Collection access index outside `[0, length - 1]`.
- **`E303: Key Not Found`** — Accessing nonexistent key in a map without default fallback.
- **`E304: Recursion Limit Exceeded`** — Call stack depth exceeded configured recursion limit.
- **`E305: Not Callable`** — Attempting to call a non-function value.
- **`E306: Runtime Type Error`** — Dynamic operation on incompatible types.
- **`E307: Invalid Property`** — Accessing nonexistent attribute on a module or object.

### Type Errors (`E401`–`E499`)
- **`E401: Type Mismatch`** — Incompatible types in variable assignment or initialization.
- **`E402: Argument Type Mismatch`** — Function argument does not match parameter type.
- **`E403: Return Type Mismatch`** — Function return value violates declared signature.
- **`E404: Operator Type Mismatch`** — Binary operator applied to incompatible operand types.
- **`E405: Unary Type Mismatch`** — Unary operator applied to invalid operand type.
- **`E406: Argument Count Mismatch`** — Wrong number of arguments provided in function call.
- **`E407: Unindexable Target`** — Index operator `[]` used on a non-indexable type.

### Swamitva Memory Safety Errors (`E501`–`E599`)
- **`E501: Use After Move`** — Reading or using a value whose ownership has been transferred.
- **`E502: Mutable Borrow Conflict`** — Attempting mutable borrow while shared borrows exist.
- **`E503: Multiple Mutable Borrows`** — Attempting more than one active mutable borrow.
- **`E504: Dangling Reference`** — Returning reference to a local value that goes out of scope.
- **`E505: Mutation While Borrowed`** — Mutating a value while active references exist.

---

## 3. Machine-Readable Diagnostic Format

When `vakya check` is run with `--format=json`, diagnostics are formatted as JSON:

```json
{
  "status": "error",
  "file": "example.vakya",
  "error": {
    "code": "E401",
    "message": "Type mismatch: Cannot assign value of type 'shabda' to variable 'x' of type 'sankhya'",
    "line": 1,
    "column": 20,
    "length": 12,
    "help": "Expected type 'sankhya', but found 'shabda'."
  }
}
```
