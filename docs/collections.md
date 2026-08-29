# Collections: Lists and Maps in Vākya

Vākya supports ordered lists (`suchi`) and key-value maps (`naksha`).

---

## 1. Lists (`suchi`)

Lists are heterogeneous, dynamically sized arrays created with bracket syntax `[...]`.

```vakya
chara numbers = [10, 20, 30, 40]
vada("First element:", numbers[0])
vada("Length via property:", numbers.length)
vada("Length via builtin:", lamba(numbers))
```

### Mutating Lists
```vakya
numbers[1] = 99              // Update index 1
suchi_jodo(numbers, 50)      // Append 50
chara removed = suchi_hatao(numbers, 0) // Remove first element
vada("Removed:", removed)
vada("Current list:", numbers)
```

---

## 2. Maps (`naksha`)

Maps are key-value associative dictionaries created with brace syntax `{...}`.

```vakya
chara user = {
    "name": "Goku",
    "power": 9001
}

user["role"] = "Warrior" // Add or update key
vada("User name:", user["name"])
vada("Map length:", user.length)
```

### Iterating Maps
```vakya
pratyekam key madhye user {
    vada(key, "->", user[key])
}
```
