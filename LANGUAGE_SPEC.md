# VĀKYA LANGUAGE SPECIFICATION (v2.0-alpha)

**Status**: Authoritative Formal Specification  
**Canonical Name**: Vākya (वाक्य — *Sentence / Statement*)  
**Source Script**: Roman / Latin Characters (ASCII + UTF-8 string literals)  

---

## 1. Introduction & Design Principles

Vākya is a general-purpose programming language that pairs **modern programming language structure** with **Romanized Sanskrit vocabulary**.

### Key Principles
1. **Explicit Identity**: Keywords are drawn from Sanskrit concepts and written in standard Latin script for universal keyboard accessibility.
2. **Predictable Semantics**: Strict typing, deterministic operator precedence, and isolated lexical scoping.
3. **Dual Execution Architecture**: Verified against a reference AST interpreter and powered by a stack-based Bytecode Virtual Machine (VM).
4. **Actionable Diagnostics**: Structured error reports with error codes (`E001`–`E407`), line/column positions, source snippets, and caret indicators.

---

## 2. Lexical Grammar

### 2.1 Character Set & Encodings
- Source code files must be UTF-8 encoded plain text with standard `.vakya` file extension.
- Whitespace consists of spaces (`U+0020`), horizontal tabs (`U+0009`), carriage returns (`U+000D`), and newlines (`U+000A`). Whitespace separates tokens but is otherwise ignored outside string literals.

### 2.2 Comments
- **Single-line comments**: Begin with `//` and extend to the end of the line.
- **Multi-line comments**: Enclosed in `/*` and `*/` (nesting is not supported).

```vakya
// Single line comment
/* Multi-line
   comment block */
```

### 2.3 Identifiers
Identifiers name variables, constants, and functions.
- Must begin with a Latin letter (`a`–`z`, `A`–`Z`) or an underscore `_`.
- Subsequent characters may include letters, digits (`0`–`9`), or underscores `_`.
- Reserved keywords cannot be used as user-defined variable or function identifiers.

### 2.4 Numeric Literals
- **Integers (`sankhya`)**: Sequences of one or more decimal digits (`0`–`9`). E.g., `0`, `42`, `1000`.
- **Floating-point (`dashamika`)**: Digits with a mandatory decimal point followed by one or more fractional digits. E.g., `3.14159`, `0.5`, `10.0`.

### 2.5 String Literals (`shabda`)
- Enclosed in double quotes `"..."`.
- Supports standard escape sequences:
  - `\"` : Double quotation mark
  - `\\` : Backslash
  - `\n` : Line feed
  - `\t` : Horizontal tab
  - `\r` : Carriage return

### 2.6 Boolean & Null Literals
- `satya` : Boolean true
- `asatya` : Boolean false
- `shunya` : Null / absence of value

---

## 3. Type System

Vākya features static type checking with local type inference.

### 3.1 Primitive Types
| Type Identifier | Description | Runtime Representation |
| :--- | :--- | :--- |
| `sankhya` | 64-bit signed integer | Integer numeric value |
| `dashamika` | IEEE-754 double precision float | Floating-point value |
| `shabda` | UTF-8 encoded text string | Unicode string |
| `boolean` | Logical truth value (`satya`/`asatya`) | Strict boolean |
| `suchi` | Ordered dynamic array list | Heterogeneous dynamic array |
| `naksha` | Key-value dictionary / hash map | String-keyed dictionary |
| `shunya` | Null value | Null / None |

### 3.2 Type Annotations & Inference
Variable declarations may specify an explicit type or omit it for automatic inference:

```vakya
chara x: sankhya = 10     // Explicit type annotation
chara y = 20              // Inferred as sankhya
dhruva pi = 3.14159       // Inferred as dashamika
```

---

## 4. Declarations & Bindings

### 4.1 Variables (`chara`)
Mutable variables are declared using `chara`:

```vakya
chara score = 50
score = score + 10        // Allowed
```

### 4.2 Constants (`dhruva`)
Immutable constants are declared using `dhruva` and must have an initializer:

```vakya
dhruva max_limit = 100
// max_limit = 200        // Compile-time error [E203]
```

---

## 5. Operators & Precedence

Vākya uses a strict 8-level precedence hierarchy.

| Level | Operators | Description | Associativity |
| :--- | :--- | :--- | :--- |
| **8 (Highest)** | `.` `[]` `()` | Member access, Indexing, Call | Left-to-right |
| **7** | Unary `-`, `na` | Unary negation, Logical NOT | Right-to-left |
| **6** | `**` | Exponentiation (Power) | **Right-to-left** |
| **5** | `*` `/` `%` | Multiplication, Division, Modulo | Left-to-right |
| **4** | `+` `-` | Addition, Subtraction | Left-to-right |
| **3** | `<` `<=` `>` `>=` | Relational comparisons | Non-associative |
| **2** | `==` `!=` | Equality / Inequality | Non-associative |
| **1 (Lowest)** | `evam` `va` | Logical AND, Logical OR | Left-to-right |

### 5.1 Strict Equality & Comparison Semantics
- In Vākya, boolean and integer values are distinct types. `satya == 1` evaluates strictly to `asatya`.
- Logical NOT (`na`) binds tighter than equality: `na 1 + 2 == 3` parses as `na ((1 + 2) == 3)` which evaluates to `asatya`.

---

## 6. Control Flow

### 6.1 Conditionals (`yadi` / `anyatha`)
```vakya
yadi score >= 90 {
    vada("Grade: A")
} anyatha yadi score >= 75 {
    vada("Grade: B")
} anyatha {
    vada("Grade: C")
}
```

### 6.2 While Loops (`yavat`)
```vakya
chara i = 0
yavat i < 5 {
    i += 1
    yadi i == 2 { agaccha } // Skip 2
    yadi i == 4 { virama }  // Exit loop at 4
    vada(i)
}
```

### 6.3 For-Each Loops (`pratyekam ... madhye`)
```vakya
chara warriors = ["Goku", "Vegeta", "Gohan"]
pratyekam w madhye warriors {
    vada("Warrior:", w)
}
```

---

## 7. Functions & Closures

### 7.1 Function Declarations (`karya`)
Functions are declared using `karya` with typed or untyped parameters:

```vakya
karya guna(a: sankhya, b: sankhya) -> sankhya {
    pratyavartaya a * b
}
```

Top-level functions are automatically hoisted during compilation to support mutual recursion and forward references without forward declarations.

### 7.2 First-Class Functions & Closures
Functions are first-class values and can be passed as arguments, returned from outer functions, and stored in collections:

```vakya
karya make_adder(x: sankhya) {
    karya adder(y: sankhya) -> sankhya {
        pratyavartaya x + y
    }
    pratyavartaya adder
}

chara add5 = make_adder(5)
vada(add5(10)) // Prints: 15
```

---

## 8. Built-in Functions

| Function | Signature | Description |
| :--- | :--- | :--- |
| `vada(...)` | `vada(*args) -> shunya` | Prints formatted values to standard output followed by a newline. |
| `puchha(prompt?)`| `puchha(prompt?: shabda) -> shabda` | Displays prompt and reads a line of input from stdin. |
| `lamba(obj)` | `lamba(suchi \| naksha \| shabda) -> sankhya` | Returns the length or element count of a collection or string. |
| `prakaar(val)` | `prakaar(val: any) -> shabda` | Returns the runtime type name string (`"sankhya"`, `"shabda"`, etc.). |
| `suchi_jodo(l, v)`| `suchi_jodo(suchi, any) -> suchi` | Appends value `v` to list `l` in-place and returns `l`. |
| `suchi_hatao(l, i?)`| `suchi_hatao(suchi, sankhya?) -> any` | Removes and returns element at index `i` (or the last item if omitted). |
| `shabda_bada(s)`| `shabda_bada(shabda) -> shabda` | Returns uppercase string. |
| `shabda_chhota(s)`| `shabda_chhota(shabda) -> shabda` | Returns lowercase string. |
| `shabda_trim(s)`| `shabda_trim(shabda) -> shabda` | Returns string with leading and trailing whitespace removed. |

---

## 9. Error Categories

- **`E001–E003`**: Lexical analysis errors (invalid character, unterminated string, malformed number).
- **`E101–E106`**: Syntax & Parser errors (unexpected token, missing delimiter, invalid assignment target).
- **`E201–E207`**: Static Type Checker errors (type mismatch, redeclaration, constant reassignment).
- **`E301–E307`**: Runtime execution errors (division by zero, index out of bounds, key not found, recursion limit).
- **`E401–E407`**: Semantic & argument errors (argument count mismatch, unindexable target).
