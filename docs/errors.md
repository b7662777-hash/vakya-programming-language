# Vākya Diagnostic & Error System

Vākya prioritizes developer ergonomics by providing structured diagnostics with precise source code locations, ASCII art line gutters, caret indicators (`^^^^`), and contextual help suggestions.

## Diagnostic Format

```text
Error [E102]: Undefined variable 'naam'

  --> hello.vakya:4:9

   3 | karya main() {
   4 |     vada(naam)
     |          ^^^^
   5 | }

Help: Declare the variable using 'chara' or 'dhruva' before using it.
```

## Standard Error Code Catalog

### Lexical Errors (E001 – E099)
- `[E001]`: Invalid Character — Unrecognized symbol in source.
- `[E002]`: Unterminated String — Missing closing quotation mark (`"`).
- `[E003]`: Unterminated Comment — Missing closing block comment delimiter (`*/`).
- `[E004]`: Invalid Escape Sequence — Unsupported character escape sequence.
- `[E005]`: Invalid Number Literal — Malformed numeric literal.

### Identifier & Scope Errors (E101 – E199)
- `[E101]`: Undefined Variable — Accessing an undeclared identifier.
- `[E102]`: Undefined Function — Calling an undeclared function.
- `[E103]`: Cannot Reassign Constant — Mutation attempt on `dhruva` binding.
- `[E104]`: Duplicate Declaration — Variable already declared in current scope.
- `[E105]`: Invalid Assignment Target — Target of assignment is not a variable or index.

### Parser & Syntax Errors (E201 – E299)
- `[E201]`: Unexpected Token — Token does not match grammatical grammar rule.
- `[E202]`: Expected Token — Missing expected delimiter, keyword, or identifier.
- `[E203]`: Expected Expression — Expected expression term.
- `[E204]`: Invalid Parameter Declaration — Malformed function parameter.
- `[E205]`: Invalid Loop Syntax — Malformed `pratyekam` or `yavat` loop structure.
- `[E206]`: Loop Control Outside Loop — `virama` or `agaccha` outside loop.
- `[E207]`: Return Outside Function — `pratyavartaya` outside function.

### Runtime Errors (E301 – E399)
- `[E301]`: Division by Zero — Divisor evaluated to zero.
- `[E302]`: Index Out of Bounds — List or string index outside valid range.
- `[E303]`: Key Not Found in Map — Accessing nonexistent key in `naksha`.
- `[E304]`: Recursion Limit Exceeded — Unbounded recursion depth.
- `[E305]`: Value Not Callable — Invocation attempt on non-function.
- `[E306]`: Runtime Type Error — Invalid operation on runtime value.
- `[E307]`: Unknown Property Access — Unsupported member access.

### Type Checking Errors (E401 – E499)
- `[E401]`: Type Mismatch — Incompatible types in variable assignment or initialization.
- `[E402]`: Argument Type Mismatch — Calling function with incompatible argument type.
- `[E403]`: Return Type Mismatch — Function return value does not match annotated return type.
- `[E404]`: Incompatible Operand Types — Binary operator applied to incompatible types.
- `[E405]`: Incompatible Unary Operand Type — Unary operator applied to invalid operand.
- `[E406]`: Argument Count Mismatch — Incorrect number of arguments in function call.
- `[E407]`: Type Not Indexable — Indexing attempted on non-collection type.
