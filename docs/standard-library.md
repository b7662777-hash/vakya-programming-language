# Vākya Standard Library Architecture

Vākya follows the philosophy of keeping the core language small and orthogonal, while providing a rich, modular standard library.

---

## 1. Core Built-in Functions (Available in Global Scope)

| Function | Signature | Description |
| :--- | :--- | :--- |
| `vada(*args)` | `vada(*args) -> shunya` | Prints formatted values to standard output followed by a newline. |
| `puchha(prompt?)`| `puchha(prompt?: shabda) -> shabda` | Reads a line of text from standard input. |
| `lamba(obj)` | `lamba(suchi \| naksha \| shabda) -> sankhya` | Returns the length of a string or collection. |
| `prakaar(val)` | `prakaar(val: any) -> shabda` | Returns runtime type name. |
| `suchi_jodo(l, item)`| `suchi_jodo(suchi, any) -> suchi` | Appends item to list. |
| `suchi_hatao(l, idx?)`| `suchi_hatao(suchi, sankhya?) -> any`| Removes item at index or end. |
| `shabda_bada(s)` | `shabda_bada(shabda) -> shabda` | Converts string to uppercase. |
| `shabda_chhota(s)`| `shabda_chhota(shabda) -> shabda` | Converts string to lowercase. |
| `shabda_trim(s)` | `shabda_trim(shabda) -> shabda` | Trims leading/trailing whitespace. |

---

## 2. Future Standard Library Modules (`std/`)

- `std.math`: Trigonometric, logarithmic, and mathematical constants.
- `std.fs`: Filesystem file reading, writing, path manipulation.
- `std.net`: TCP/UDP sockets, HTTP client & server.
- `std.json`: JSON serialization and deserialization.
- `std.time`: Timers, monotonic clocks, formatting dates.
