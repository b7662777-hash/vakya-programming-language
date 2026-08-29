# Vākya Type System & Inference

## Supported Primitive Types

| Type Name | Sanskrit Meaning | Description | Example Literals |
| :--- | :--- | :--- | :--- |
| `sankhya` | Number / Count | Integer number | `0`, `42`, `-10`, `1000000` |
| `dashamika` | Decimal | Floating-point number | `3.14`, `0.5`, `-12.75` |
| `shabda` | Word / Sound | String | `"Goku"`, `"Namaste\nWorld"` |
| `boolean` | Boolean truth value | Boolean | `satya` (true), `asatya` (false) |
| `suchi` | List / Index | Ordered array | `[1, 2, 3]`, `["a", "b"]` |
| `naksha` | Map / Chart | Key-value dictionary | `{"name": "Goku", "age": 16}` |
| `shunya` | Void / Zero | Null / Nil value | `shunya` |

## Type Annotations

Type annotations are optional on variable and constant declarations:

```vakya
chara age: sankhya = 16
dhruva pi: dashamika = 3.14159
chara name: shabda = "Goku"
chara active: boolean = satya
```

## Type Inference

When type annotations are omitted, Vākya's static analyzer infers the type from the initializer expression:

```vakya
chara age = 16       // Inferred as sankhya
chara pi = 3.14      // Inferred as dashamika
chara name = "Goku"  // Inferred as shabda
```

## Static Validation

The static typechecker detects type mismatches prior to program execution:

```vakya
chara x: sankhya = "hello"
// Type mismatch: Cannot assign shabda to variable x of type sankhya (Error [E401])
```
