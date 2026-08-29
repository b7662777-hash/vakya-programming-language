# String Operations in Vākya

Strings (`shabda`) represent UTF-8 encoded text literals enclosed in double quotes `"..."`.

---

## 1. String Concatenation & Repetition

```vakya
chara first = "Namaste"
chara second = "World"
chara greeting = first + ", " + second + "!"
vada(greeting) // Prints: Namaste, World!

// String repetition with an integer
chara mantra = "om " * 3
vada(mantra)   // Prints: om om om
```

---

## 2. String Indexing & Length

Strings can be indexed like arrays to access individual characters:

```vakya
chara word = "Vakya"
vada("First char:", word[0])       // Prints: V
vada("Length via property:", word.length) // Prints: 5
vada("Length via builtin:", lamba(word))  // Prints: 5
```

---

## 3. String Built-in Functions

| Builtin | Description | Example |
| :--- | :--- | :--- |
| `shabda_bada(s)` | Uppercase conversion | `shabda_bada("namaste")` → `"NAMASTE"` |
| `shabda_chhota(s)`| Lowercase conversion | `shabda_chhota("VAKYA")` → `"vakya"` |
| `shabda_trim(s)` | Strip leading/trailing whitespace | `shabda_trim("  hi  ")` → `"hi"` |
