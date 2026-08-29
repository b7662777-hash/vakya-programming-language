# Vākya Language Tour

A quick walkthrough of all core language features in Vākya (वाक्य).

---

## 1. Variables & Constants
```vakya
chara score = 100        // Mutable variable
dhruva app_name = "Game" // Immutable constant
```

## 2. Types & Expressions
```vakya
chara age: sankhya = 16
chara pi: dashamika = 3.14159
chara is_active: boolean = satya
chara empty: shunya = shunya
```

## 3. Conditionals & Logic
```vakya
yadi age >= 18 {
    vada("Adult")
} anyatha yadi age >= 13 {
    vada("Teenager")
} anyatha {
    vada("Child")
}
```

## 4. Loops & Iteration
```vakya
// While loop
chara i = 0
yavat i < 5 {
    vada("Step:", i)
    i += 1
}

// For-each loop
chara names = ["Arjuna", "Bhima", "Nakula"]
pratyekam n madhye names {
    vada("Hero:", n)
}
```

## 5. Functions & Recursion
```vakya
karya factorial(n: sankhya) -> sankhya {
    yadi n <= 1 { pratyavartaya 1 }
    pratyavartaya n * factorial(n - 1)
}

vada("6! =", factorial(6)) // 720
```

## 6. Collections
```vakya
// Lists
chara items = [10, 20, 30]
suchi_jodo(items, 40)

// Maps
chara user = {"name": "Goku", "power": 9001}
user["status"] = "Super Saiyan"
```
