# Control Flow Statements in Vākya

Vākya provides structured branching and loop control mechanisms.

---

## 1. Branching (`yadi` / `anyatha`)
```vakya
yadi condition1 {
    // block 1
} anyatha yadi condition2 {
    // block 2
} anyatha {
    // fallback block
}
```

---

## 2. Iteration (`yavat` and `pratyekam ... madhye`)

### `yavat` (While Loop)
```vakya
chara count = 0
yavat count < 10 {
    count += 1
}
```

### `pratyekam ... madhye` (Collection Loop)
Iterates over lists, strings, and map keys:
```vakya
chara colors = ["Rakta", "Pita", "Nila"]
pratyekam c madhye colors {
    vada(c)
}
```

---

## 3. Loop Termination & Flow Control

- **`virama`**: Immediately exits the loop.
- **`agaccha`**: Skips the rest of the current iteration.

```vakya
chara i = 0
yavat i < 10 {
    i += 1
    yadi i % 2 == 0 { agaccha }
    yadi i > 7 { virama }
    vada(i)
}
```
