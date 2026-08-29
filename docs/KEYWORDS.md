# Vākya Keyword Reference

This document is the authoritative registry of all Romanized Sanskrit keywords in the **Vākya Programming Language** (v0.1.0).

---

## Keyword Catalog

| Keyword | Devanagari | English Meaning | Category | Example Syntax | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `chara` | चर | Variable (Mutable) | Declaration | `chara count = 0` | IMPLEMENTED |
| `dhruva` | ध्रुव | Constant (Immutable) | Declaration | `dhruva PI = 3.14159` | IMPLEMENTED |
| `karya` | कार्य | Function / Action | Function | `karya add(a, b) { ... }` | IMPLEMENTED |
| `pratyavartaya` | प्रत्यावर्तय | Return | Function | `pratyavartaya a + b` | IMPLEMENTED |
| `yadi` | यदि | If | Control Flow | `yadi x > 0 { ... }` | IMPLEMENTED |
| `anyatha` | अन्यथा | Else / Otherwise | Control Flow | `anyatha { ... }` | IMPLEMENTED |
| `tarhi` | तर्हि | Then | Control Flow | `yadi x tarhi { ... }` | IMPLEMENTED |
| `yavat` | यावत् | While / As long as | Loops | `yavat i < 10 { ... }` | IMPLEMENTED |
| `pratyekam` | प्रत्येकम् | For-each / Every | Loops | `pratyekam x madhye list { ... }` | IMPLEMENTED |
| `madhye` | मध्ये | In / Among | Loops | `pratyekam item madhye items` | IMPLEMENTED |
| `virama` | विराम | Break / Stop | Control Flow | `yadi i == 5 { virama }` | IMPLEMENTED |
| `agaccha` | आगच्छ | Continue / Next | Control Flow | `yadi i == 2 { agaccha }` | IMPLEMENTED |
| `satya` | सत्य | True | Literal | `chara active = satya` | IMPLEMENTED |
| `asatya` | असत्य | False | Literal | `chara done = asatya` | IMPLEMENTED |
| `shunya` | शून्य | Null / Void / Zero | Literal | `chara val = shunya` | IMPLEMENTED |
| `aayat` | आयात | Import / Bring in | Modules | `aayat math` | IMPLEMENTED |
| `evam` | एवम् | Logical AND (`&&`) | Operator | `yadi a > 0 evam b > 0` | IMPLEMENTED |
| `va` | वा | Logical OR (`\|\|`) | Operator | `yadi a > 0 va b > 0` | IMPLEMENTED |
| `na` | न | Logical NOT (`!`) | Operator | `yadi na is_empty` | IMPLEMENTED |
| `antah` | अन्तः | Private / Internal | Visibility | `antah chara secret = 1` | PARSED |
| `sarvajan` | सर्वजन | Public / Exported | Visibility | `sarvajan karya api() {}` | PARSED |

---

## Type Keywords

| Type Keyword | Devanagari | Type Concept | Example Annotation |
| :--- | :--- | :--- | :--- |
| `sankhya` | संख्या | 64-bit Integer | `chara age: sankhya = 25` |
| `dashamika` | दाशमिक | Double Precision Float | `chara rate: dashamika = 4.5` |
| `shabda` | शब्द | Text String | `chara name: shabda = "Goku"` |
| `boolean` | — | Boolean (`satya`/`asatya`) | `chara flag: boolean = satya` |
| `suchi` | सूची | Dynamic List / Array | `chara nums: suchi = [1, 2]` |
| `naksha` | नक्शा | Key-Value Map / Dict | `chara map: naksha = {"k": 1}` |
| `shunya` | शून्य | Null / Void | `karya log() -> shunya` |
