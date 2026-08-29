# Vākya Type System

The **Vākya Type System** provides compile-time safety through static typing combined with ergonomic local type inference.

---

## 1. Type Hierarchy

```text
                       ┌─────────┐
                       │   Any   │
                       └────┬────┘
         ┌───────────────┼───────────────┬────────────────┐
         ▼               ▼               ▼                ▼
    ┌─────────┐    ┌───────────┐   ┌───────────┐    ┌──────────┐
    │ sankhya │    │ dashamika │   │  shabda   │    │ boolean  │
    └─────────┘    └───────────┘   └───────────┘    └──────────┘
         │               │               │                │
         └───────────────┼───────────────┴────────────────┘
                         ▼
        ┌────────────────────────────────┐
        │ Collections: suchi, naksha     │
        │ Function: (T1, T2) -> R        │
        │ Bottom: shunya (Null / Void)   │
        └────────────────────────────────┘
```

---

## 2. Primitive Types

| Type Identifier | Description | Valid Values | Example |
| :--- | :--- | :--- | :--- |
| `sankhya` | 64-bit signed integer | `... -2, -1, 0, 1, 2, 42 ...` | `chara x: sankhya = 100` |
| `dashamika` | IEEE-754 double float | `0.0, 3.14159, -0.001` | `chara pi: dashamika = 3.14` |
| `shabda` | UTF-8 encoded text string | `"hello", "वाक्य", ""` | `chara msg: shabda = "Namaste"` |
| `boolean` | Boolean truth value | `satya` (true), `asatya` (false)| `chara ok: boolean = satya` |
| `shunya` | Null / absence of value | `shunya` | `chara empty = shunya` |

---

## 3. Collection Types

### Lists (`suchi`)
Ordered, dynamic sequence of values:
```vakya
chara numbers: suchi = [1, 2, 3, 4, 5]
chara first = numbers[0]
numbers = suchi_jodo(numbers, 6)
```

### Maps (`naksha`)
Key-value associative mapping where keys are strings:
```vakya
chara user: naksha = {
    "name": "Arjuna",
    "score": 100
}
vada(user["name"]) // Arjuna
```

---

## 4. Local Type Inference

When an explicit type annotation is omitted, the Vākya Type Checker automatically infers the variable's type from its initializer:

```vakya
chara a = 42            // Inferred as sankhya
chara b = 3.14          // Inferred as dashamika
chara c = "Namaste"     // Inferred as shabda
chara d = satya         // Inferred as boolean
chara e = [1, 2, 3]     // Inferred as suchi
```

Once inferred, the variable's type is strictly enforced for all subsequent assignments:
```vakya
chara x = 10
// x = "cannot assign string" // Compile-time Error [E401]
```

---

## 5. Function Types & Signatures

Functions declare their parameter types and return type:
```vakya
karya area(width: sankhya, height: sankhya) -> sankhya {
    pratyavartaya width * height
}
```

If a return type is omitted, it is inferred from the returned expression or defaults to `shunya` if no value is returned.

---

## 6. Static Type Errors

| Code | Diagnostic Title | Cause |
| :--- | :--- | :--- |
| `E401` | Type Mismatch | Assigning a value of type `U` to a variable expecting type `T`. |
| `E402` | Argument Type Mismatch | Passing an argument of incompatible type to a typed function parameter. |
| `E403` | Return Type Mismatch | Returning an expression that contradicts the function's declared return type. |
| `E404` | Operator Type Mismatch | Using an operator with incompatible operand types (e.g. `10 * "text"`). |
| `E405` | Unary Type Mismatch | Applying unary operator to an invalid type (e.g. `na 42`). |
| `E406` | Argument Count Mismatch | Calling a function with too few or too many arguments. |
| `E407` | Unindexable Target | Indexing a value that is not a list, map, or string. |
