# Vākya Operator Reference

This document defines the operator precedence, associativity, operand requirements, and evaluation semantics in the **Vākya Programming Language**.

---

## 1. Precedence Hierarchy

Operators are listed from highest precedence (binds tightest) to lowest precedence:

| Level | Operators | Description | Associativity | Operand Types | Result Type | Example |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **8** | `.` | Member access | Left-to-right | `naksha \| module`, `shabda` | Attribute value | `math.PI` |
| | `[]` | Index access | Left-to-right | `suchi \| naksha \| shabda`, `sankhya \| shabda` | Element | `items[0]` |
| | `()` | Function call | Left-to-right | `karya`, `(args...)` | Return type | `add(1, 2)` |
| **7** | `-` | Unary negation | Right-to-left | `sankhya \| dashamika` | Same numeric | `-count` |
| | `na` | Logical NOT | Right-to-left | `boolean` | `boolean` | `na is_ready` |
| **6** | `**` | Exponentiation | Right-to-left | `sankhya \| dashamika` | Numeric | `2 ** 3` (8) |
| **5** | `*` | Multiplication | Left-to-right | `sankhya \| dashamika` | Numeric | `6 * 7` (42) |
| | `/` | Division | Left-to-right | `sankhya \| dashamika` | Numeric (check div by 0) | `10 / 2` (5) |
| | `%` | Modulo | Left-to-right | `sankhya` | `sankhya` | `10 % 3` (1) |
| **4** | `+` | Addition / Concat | Left-to-right | `sankhya \| dashamika` OR `shabda + shabda` | Numeric / `shabda` | `"A" + "B"` |
| | `-` | Subtraction | Left-to-right | `sankhya \| dashamika` | Numeric | `10 - 4` (6) |
| **3** | `<` | Less than | Non-associative | `sankhya \| dashamika \| shabda` | `boolean` | `x < 10` |
| | `<=` | Less or equal | Non-associative | `sankhya \| dashamika \| shabda` | `boolean` | `x <= 10` |
| | `>` | Greater than | Non-associative | `sankhya \| dashamika \| shabda` | `boolean` | `x > 10` |
| | `>=` | Greater or equal | Non-associative | `sankhya \| dashamika \| shabda` | `boolean` | `x >= 10` |
| **2** | `==` | Equality | Non-associative | Any, Any (Type checked) | `boolean` | `x == 10` |
| | `!=` | Inequality | Non-associative | Any, Any (Type checked) | `boolean` | `x != 10` |
| **1** | `evam` | Logical AND | Left-to-right | `boolean`, `boolean` | `boolean` | `a > 0 evam b > 0` |
| | `va` | Logical OR | Left-to-right | `boolean`, `boolean` | `boolean` | `a > 0 va b > 0` |

---

## 2. Compound Assignment Operators

Compound assignment statements modify a mutable variable in-place:
- `+=` : Add and assign (`x += 5`)
- `-=` : Subtract and assign (`x -= 5`)
- `*=` : Multiply and assign (`x *= 5`)
- `/=` : Divide and assign (`x /= 5`)

---

## 3. Strict Type Rules & Evaluation Semantics

1. **No Implicit Type Coercion**:
   - In Vākya, integers and booleans do not cross-coerce. `satya == 1` evaluates strictly to `asatya` (or causes a static type warning if strict mode is enabled).
2. **Short-Circuit Evaluation**:
   - `evam` (AND): If the left operand evaluates to `asatya`, the right operand is not evaluated.
   - `va` (OR): If the left operand evaluates to `satya`, the right operand is not evaluated.
3. **String Concatenation**:
   - The `+` operator concatenates two strings: `"Namaste " + "Vākya"`. Combining a number and a string requires explicit conversion or separate arguments in `vada(a, b)`.
