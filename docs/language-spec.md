# Vākya Language Specification (v0.1.0)

**Status**: Authoritative Formal Specification  
**Canonical Name**: Vākya (वाक्य — *Sentence / Statement*)  
**Source Script**: Roman / Latin Characters (ASCII + UTF-8 string literals)  

---

## 1. Introduction & Design Principles

Vākya is a general-purpose programming language combining **modern systems language ergonomics** with **Romanized Sanskrit vocabulary**.

### Core Tenets
1. **Explicit Identity**: Keywords are drawn from Sanskrit linguistic foundations and written in Latin script for universal keyboard accessibility.
2. **Predictable Semantics**: Strict typing, deterministic operator precedence, and lexical scoping.
3. **Compile-Time Memory Safety (Swamitva)**: Static ownership tracking and borrow checking eliminating data races and use-after-move bugs without garbage collection pauses.
4. **Dual Execution Architecture**: Reference tree-walking AST interpreter and high-performance Bytecode Virtual Machine (VM).
5. **Actionable Diagnostics**: Machine-readable error codes (`E100`–`E505`), contextual line snippets, ASCII carats, and actionable remediation hints.

---

## 2. Lexical Structure

### 2.1 Encodings & Files
- Source files are plain UTF-8 encoded text with the `.vakya` file extension.
- Whitespace includes spaces (`U+0020`), tabs (`U+0009`), carriage returns (`U+000D`), and newlines (`U+000A`). Outside of strings, whitespace separates tokens but is otherwise insignificant.

### 2.2 Comments
```vakya
// Single-line comment to end of line
/* Multi-line
   comment block */
```

### 2.3 Identifiers
- Must begin with `[a-zA-Z_]` followed by `[a-zA-Z0-9_]*`.
- Reserved keywords cannot be used as user-defined identifiers.

### 2.4 Literals
- **Integer (`sankhya`)**: E.g. `0`, `42`, `-17`.
- **Float (`dashamika`)**: E.g. `3.14159`, `0.5`, `10.0`.
- **String (`shabda`)**: UTF-8 enclosed in double quotes `"..."` supporting `\n`, `\t`, `\r`, `\"`, `\\`.
- **Boolean**: `satya` (true), `asatya` (false).
- **Null**: `shunya` (null / void).

---

## 3. Type System

Static types are verified at compile time with support for local type inference.

| Type Identifier | Description | Representation |
| :--- | :--- | :--- |
| `sankhya` | 64-bit signed integer | Integer value |
| `dashamika` | IEEE-754 double precision float | Floating-point value |
| `shabda` | UTF-8 encoded text string | Unicode string |
| `boolean` | Logical truth value (`satya`/`asatya`) | Strict boolean |
| `suchi` | Ordered dynamic array | Dynamic list |
| `naksha` | Key-value dictionary | String-keyed dictionary |
| `shunya` | Null value | Null / None |

---

## 4. Declarations & Variables

### 4.1 Mutable Variables (`chara`)
```vakya
chara count: sankhya = 0
count = count + 1
```

### 4.2 Immutable Constants (`dhruva`)
```vakya
dhruva MAX_BUFFER = 1024
// MAX_BUFFER = 2048 // Error: Cannot reassign constant
```

---

## 5. Swamitva Memory Safety & Ownership

Vākya uses the **Swamitva Ownership Model**:
1. **Single Ownership**: Every non-primitive value has exactly one owner variable.
2. **Move Semantics**: Passing or reassigning a non-primitive value transfers ownership. Accessing a moved value causes error `E501`.
3. **Borrowing**:
   - **Shared Borrows (`&T`)**: Multiple immutable borrows are permitted.
   - **Mutable Borrows (`&mut T`)**: Strictly exclusive. Cannot coexist with other shared or mutable borrows (`E502`, `E503`).
4. **No Dangling References**: References cannot outlive the referenced owner (`E504`).
5. **Mutation Invariant**: Values cannot be modified while borrowed (`E505`).

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
    yadi i == 2 { agaccha } // continue
    yadi i == 4 { virama }  // break
    vada(i)
}
```

### 6.3 For-Each Loops (`pratyekam ... madhye`)
```vakya
chara items = ["apple", "banana", "cherry"]
pratyekam item madhye items {
    vada(item)
}
```

---

## 7. Functions & Closures

Functions are declared with `karya` and support recursion, first-class passing, and lexical closures:

```vakya
karya factorial(n: sankhya) -> sankhya {
    yadi n <= 1 {
        pratyavartaya 1
    }
    pratyavartaya n * factorial(n - 1)
}

vada(factorial(10)) // 3628800
```

---

## 8. Module System (`aayat`)

Modules are loaded via `aayat`:
```vakya
aayat math

chara radius = 5
chara area = math.PI * math.varga(radius)
vada("Area:", area)
```

---

## 9. Built-in Functions

| Function | Signature | Description |
| :--- | :--- | :--- |
| `vada(...)` | `vada(*args) -> shunya` | Prints formatted values to standard output followed by a newline. |
| `puchha(prompt?)`| `puchha(prompt?: shabda) -> shabda` | Displays prompt and reads a line from stdin. |
| `lamba(obj)` | `lamba(suchi \| naksha \| shabda) -> sankhya` | Returns length of string or element count of collection. |
| `prakaar(val)` | `prakaar(val: any) -> shabda` | Returns runtime type name string (`"sankhya"`, `"shabda"`). |
| `suchi_jodo(l, v)`| `suchi_jodo(suchi, any) -> suchi` | Appends value `v` to list `l`. |
| `suchi_hatao(l, i?)`| `suchi_hatao(suchi, sankhya?) -> any` | Removes and returns element at index `i`. |
| `shabda_bada(s)`| `shabda_bada(shabda) -> shabda` | Converts string to uppercase. |
| `shabda_chhota(s)`| `shabda_chhota(shabda) -> shabda` | Converts string to lowercase. |
| `shabda_trim(s)`| `shabda_trim(shabda) -> shabda` | Strips leading and trailing whitespace. |
