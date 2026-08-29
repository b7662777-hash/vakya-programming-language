# Type System & Type Inference in Vākya

Vākya features static type checking with local type inference.

---

## 1. Primitive Types

| Type Identifier | Sanskrit Etymology | Description | Literals / Examples |
| :--- | :--- | :--- | :--- |
| `sankhya` | संख्या (Number) | 64-bit signed integer | `0`, `42`, `-10` |
| `dashamika` | दशमिक (Decimal) | Double precision float | `3.14`, `0.0`, `10.5` |
| `shabda` | शब्द (Word/Sound) | UTF-8 encoded text string | `"Namaste"`, `"Vākya"` |
| `boolean` | बूलियन (Truth) | Logical truth value | `satya` (true), `asatya` (false) |
| `suchi` | सूची (List/Index) | Dynamic array collection | `[1, 2, 3]`, `["a", "b"]` |
| `naksha` | नक्शा (Map/Chart) | Key-value hash map | `{"k1": 100, "k2": 200}` |
| `shunya` | शून्य (Void/Null) | Absence of a value | `shunya` |

---

## 2. Type Inference

When type annotations are omitted, Vākya's `TypeChecker` infers the type from the initializer expression:

```vakya
chara age = 25              // Inferred as sankhya
chara pi = 3.14             // Inferred as dashamika
chara title = "Vākya"       // Inferred as shabda
chara is_active = satya     // Inferred as boolean
```

Once a variable's type is established (either via explicit annotation or inference), assigning a value of an incompatible type causes a static type error (`[E401]`):

```vakya
chara count = 10
count = "ten" // Error [E401]: Type mismatch: cannot assign 'shabda' to variable of type 'sankhya'
```

---

## 3. Function Signatures

Function parameters and return types can be typed:

```vakya
karya bhaga(a: dashamika, b: dashamika) -> dashamika {
    pratyavartaya a / b
}
```
