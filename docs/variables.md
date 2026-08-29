# Variables and Constants in Vākya

Vākya distinguishes between mutable variable bindings (`chara`) and immutable constant bindings (`dhruva`).

---

## 1. Mutable Variables (`chara`)

`chara` (चर, meaning *movable* or *changeable*) declares a variable whose value can be reassigned during program execution.

```vakya
chara score = 50
score = score + 25
vada("Score:", score) // Prints: Score: 75
```

### Optional Type Annotations
You can explicitly declare the variable type or allow the compiler to infer it:

```vakya
chara count: sankhya = 0
chara rate: dashamika = 4.5
chara name: shabda = "Arjuna"
```

---

## 2. Immutable Constants (`dhruva`)

`dhruva` (ध्रुव, meaning *fixed* or *immutable*) declares an unmodifiable binding.

```vakya
dhruva pi: dashamika = 3.1415926535
dhruva app_name = "Vākya Engine"
```

### Immutability Enforcement
Attempting to reassign a constant results in a compile-time error (`[E103]`):

```vakya
dhruva max_connections = 100
max_connections = 200 // Error [E103]: Cannot reassign constant 'max_connections'
```

---

## 3. Lexical Scoping and Shadowing

Variables in Vākya are block-scoped using `{ ... }`. Inner scopes can access and modify outer variables, or shadow them locally:

```vakya
chara x = 10
{
    chara x = 20  // Shadows outer 'x' locally
    vada(x)       // Prints: 20
}
vada(x)           // Prints: 10
```
