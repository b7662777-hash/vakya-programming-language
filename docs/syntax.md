# Vākya Syntax & Grammar Specification

## Comments

### Single-Line Comments
```vakya
// This is a single-line comment
```

### Multi-Line Comments
```vakya
/*
   This is a
   multi-line comment
*/
```

## Variables & Constants

### Mutable Variables (`chara`)
```vakya
chara score = 100
score = 150
```

### Immutable Constants (`dhruva`)
```vakya
dhruva pi = 3.14159
// pi = 3.0  <-- Produces Error [E103]
```

## Control Flow

### If / Else Conditions (`yadi` / `anyatha`)
```vakya
yadi score >= 90 {
    vada("Grade: A")
} anyatha yadi score >= 75 {
    vada("Grade: B")
} anyatha {
    vada("Grade: C")
}
```

### While Loops (`yavat`)
```vakya
chara count = 0
yavat count < 5 {
    vada("Count:", count)
    count += 1
}
```

### For-Each Loops (`pratyekam ... madhye`)
```vakya
chara items = ["apple", "banana", "mango"]
pratyekam item madhye items {
    vada("Item:", item)
}
```

### Loop Control (`virama` & `agaccha`)
- `virama`: Breaks out of the innermost loop.
- `agaccha`: Continues to the next iteration of the innermost loop.

## Operators & Precedence

| Precedence | Operators | Description |
| :--- | :--- | :--- |
| 1 (highest) | `()` `[]` `.` | Function call, indexing, member access |
| 2 | `**` | Exponentiation (right-associative) |
| 3 | `-` `+` | Unary negation, identity |
| 4 | `*` `/` `%` | Multiplication, division, modulo |
| 5 | `+` `-` | Addition, subtraction, string concatenation |
| 6 | `<` `<=` `>` `>=` | Relational comparisons |
| 7 | `==` `!=` | Equality comparisons |
| 8 | `na` | Logical NOT |
| 9 | `evam` | Logical AND |
| 10 | `va` | Logical OR |
| 11 (lowest) | `=` `+=` `-=` `*=` `/=` | Assignment and compound assignment |
