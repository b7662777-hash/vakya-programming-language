# Loops and Iteration in Vākya

Vākya provides `yavat` for condition-controlled loops and `pratyekam ... madhye` for collection iteration.

---

## 1. While Loops (`yavat`)

`yavat` (यावत्, meaning *as long as* or *while*) repeatedly executes a block as long as its condition is truthy:

```vakya
chara count = 1
yavat count <= 5 {
    vada("Count:", count)
    count += 1
}
```

---

## 2. Loop Control (`virama` & `agaccha`)

- `virama` (विराम, *break*): Immediately exits the loop.
- `agaccha` (आगच्छ, *continue*): Skips the rest of the current iteration.

```vakya
chara i = 0
yavat i < 10 {
    i += 1
    yadi i == 3 {
        agaccha // Skip 3
    }
    yadi i == 7 {
        virama  // Stop at 7
    }
    vada(i)
}
```

---

## 3. For-Each Loops (`pratyekam ... madhye`)

`pratyekam` (प्रत्येकम्, *each*) and `madhye` (मध्ये, *within*) iterate over lists, maps, and strings:

### Iterating Lists
```vakya
chara warriors = ["Goku", "Vegeta", "Gohan"]
pratyekam w madhye warriors {
    vada("Warrior:", w)
}
```

### Iterating Map Keys
```vakya
chara scores = {"math": 95, "physics": 90}
pratyekam subject madhye scores {
    vada(subject, "->", scores[subject])
}
```
