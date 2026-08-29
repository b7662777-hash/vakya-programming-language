# Control Flow: Conditionals in Vākya

Vākya uses `yadi` (यदि, meaning *if*) and `anyatha` (अन्यथा, meaning *otherwise/else*) for conditional branching.

---

## 1. Syntax

```vakya
yadi <condition> {
    // Then block
} anyatha yadi <condition> {
    // Else-if block
} anyatha {
    // Else block
}
```

---

## 2. Example: Grade Calculator

```vakya
chara score = 85

yadi score >= 90 {
    vada("Grade: A")
} anyatha yadi score >= 80 {
    vada("Grade: B")
} anyatha yadi score >= 70 {
    vada("Grade: C")
} anyatha {
    vada("Grade: D")
}
```

---

## 3. Truthiness Rules

In Vākya, conditions are evaluated according to explicit truthiness semantics:
- Falsy values: `asatya`, `shunya`, `0`, `0.0`, `""`, `[]`, `{}`.
- Truthy values: `satya` and any non-zero, non-empty value.
