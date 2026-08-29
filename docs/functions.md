# Functions and Closures in Vākya

Functions in Vākya are declared with `karya` (कार्य, meaning *action/function*) and return values with `pratyavartaya` (प्रत्यावर्तय, meaning *return*).

---

## 1. Defining Functions

```vakya
karya yog(a: sankhya, b: sankhya) -> sankhya {
    pratyavartaya a + b
}

chara result = yog(10, 20)
vada(result) // Prints: 30
```

---

## 2. Top-Level Function Hoisting

Top-level functions are automatically hoisted during compilation. You can call a function before its lexical declaration in the source file, enabling seamless mutual recursion:

```vakya
karya is_even(n: sankhya) -> boolean {
    yadi n == 0 { pratyavartaya satya }
    pratyavartaya is_odd(n - 1)
}

karya is_odd(n: sankhya) -> boolean {
    yadi n == 0 { pratyavartaya asatya }
    pratyavartaya is_even(n - 1)
}
```

---

## 3. First-Class Functions & Lexical Closures

Functions can capture variables from their enclosing lexical scopes:

```vakya
karya make_counter(start: sankhya) {
    chara count = start
    karya increment() -> sankhya {
        count += 1
        pratyavartaya count
    }
    pratyavartaya increment
}

chara c1 = make_counter(0)
vada(c1()) // Prints: 1
vada(c1()) // Prints: 2
```
