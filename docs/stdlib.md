# Vākya Standard Library Reference

The **Vākya Standard Library** (`std/`) provides foundational modules for mathematics, text manipulation, I/O, and time operations.

---

## 1. Importing Modules (`aayat`)

Standard library modules are loaded into the global namespace via `aayat`:

```vakya
aayat math
aayat string
```

Exported functions and constants are accessed via dot notation (`module.member`).

---

## 2. Standard Modules

### `math` — Mathematics & Arithmetic Functions
```vakya
aayat math
```

| Member | Signature | Description |
| :--- | :--- | :--- |
| `math.PI` | `dashamika` | Mathematical constant \(\pi \approx 3.141592653589793\) |
| `math.E` | `dashamika` | Euler's number \(e \approx 2.718281828459045\) |
| `math.varga(x)` | `(sankhya \| dashamika) -> number` | Returns the square of `x` (\(x^2\)) |
| `math.ghatamula(x)` | `(sankhya \| dashamika) -> number` | Returns the square root of `x` (\(\sqrt{x}\)) |
| `math.paramamana(x)`| `(sankhya \| dashamika) -> number` | Returns the absolute value (\(\|x\|\)) |
| `math.adhah(x)` | `(dashamika) -> sankhya` | Returns the floor of float `x` |
| `math.upari(x)` | `(dashamika) -> sankhya` | Returns the ceiling of float `x` |
| `math.adhikam(a, b)`| `(number, number) -> number` | Returns the maximum of `a` and `b` |
| `math.nyunam(a, b)` | `(number, number) -> number` | Returns the minimum of `a` and `b` |

**Example**:
```vakya
aayat math

chara r = 7
chara circle_area = math.PI * math.varga(r)
vada("Circle Area:", circle_area)
```

---

### `string` — String & Text Utilities
```vakya
aayat string
```

| Member | Signature | Description |
| :--- | :--- | :--- |
| `string.bada(s)` | `(shabda) -> shabda` | Returns uppercase string |
| `string.chhota(s)` | `(shabda) -> shabda` | Returns lowercase string |
| `string.trim(s)` | `(shabda) -> shabda` | Strips leading and trailing whitespace |
| `string.lamba(s)` | `(shabda) -> sankhya` | Returns the character count of `s` |

**Example**:
```vakya
aayat string

chara greeting = "  namaste  "
vada(string.bada(string.trim(greeting))) // "NAMASTE"
```

---

### `io` — Input & Output Operations
```vakya
aayat io
```

| Member | Signature | Description |
| :--- | :--- | :--- |
| `io.likha(s)` | `(shabda) -> shunya` | Writes string to standard output without trailing newline |
| `io.vada(*args)` | `(*args) -> shunya` | Writes formatted values with trailing newline |
| `io.puchha(p?)` | `(shabda?) -> shabda` | Reads a line of input from standard input |

---

### `time` — Date & Clock Operations
```vakya
aayat time
```

| Member | Signature | Description |
| :--- | :--- | :--- |
| `time.samaya()` | `() -> dashamika` | Returns current UNIX timestamp in seconds |
| `time.sthirata(ms)`| `(sankhya) -> shunya` | Pauses execution for `ms` milliseconds |

---

## 3. Standard Library Location & Resolution

The standard library is resolved in the following priority:
1. Bundled PyInstaller standalone environment (`sys._MEIPASS/std`)
2. Explicit environment variable: `$env:VAKYA_HOME/std`
3. Repository standard directory (`<repo_root>/std`)
4. System installation directory (`%LOCALAPPDATA%/Programs/Vakya/std` on Windows or `/usr/local/share/vakya/std` on Linux)
