# Vākya Canonical Examples Index

This directory contains the official canonical examples for the **Vākya Programming Language**.

---

## 📋 Examples Catalog

| File | Title / Concept | Features Demonstrated | Run Command |
| :--- | :--- | :--- | :--- |
| [`01_hello.vakya`](01_hello.vakya) | Hello World | Basic printing (`vada`) | `vakya run examples/01_hello.vakya` |
| [`02_name.vakya`](02_name.vakya) | Interactive Name Input | Input (`puchha`), String concatenation (`+`) | `vakya run examples/02_name.vakya` |
| [`03_calculator.vakya`](03_calculator.vakya) | Arithmetic Operations | Arithmetic operators (`+`, `-`, `*`, `/`, `**`, `%`) | `vakya run examples/03_calculator.vakya` |
| [`04_conditions.vakya`](04_conditions.vakya) | Control Flow | Conditionals (`yadi`, `anyatha`, `tarhi`) | `vakya run examples/04_conditions.vakya` |
| [`05_loops.vakya`](05_loops.vakya) | Loops & Iteration | `yavat` (while), `pratyekam` (for-each), `virama`, `agaccha` | `vakya run examples/05_loops.vakya` |
| [`06_functions.vakya`](06_functions.vakya) | Functions | Function declarations (`karya`), return (`pratyavartaya`) | `vakya run examples/06_functions.vakya` |
| [`07_recursion.vakya`](07_recursion.vakya) | Recursion | Recursive function calls and base conditions | `vakya run examples/07_recursion.vakya` |
| [`08_arrays.vakya`](08_arrays.vakya) | Arrays & Lists (`suchi`) | List indexing, iteration, and built-ins (`suchi_jodo`, `lamba`) | `vakya run examples/08_arrays.vakya` |
| [`09_maps.vakya`](09_maps.vakya) | Hash Maps (`naksha`) | Key-value dictionary lookups and assignments | `vakya run examples/09_maps.vakya` |
| [`10_strings.vakya`](10_strings.vakya) | String Manipulation | Text trimming, casing (`shabda_bada`, `shabda_chhota`) | `vakya run examples/10_strings.vakya` |
| [`11_closures.vakya`](11_closures.vakya) | Closures & Higher-Order | Lexical upvalues and function returning functions | `vakya run examples/11_closures.vakya` |
| [`12_fibonacci.vakya`](12_fibonacci.vakya) | Fibonacci Sequence | Recursive mathematical algorithm | `vakya run examples/12_fibonacci.vakya` |
| [`13_factorial.vakya`](13_factorial.vakya) | Factorial Calculation | Recursive product computation | `vakya run examples/13_factorial.vakya` |
| [`14_project.vakya`](14_project.vakya) | Comprehensive Project | End-to-end integration combining functions, collections, modules | `vakya run examples/14_project.vakya` |

---

## 🏃 Running Examples

Execute any example using the `vakya run` command:
```bash
vakya run examples/01_hello.vakya
```

Or test equivalence across execution engines:
```bash
vakya run examples/13_factorial.vakya --engine=vm
vakya run examples/13_factorial.vakya --engine=interpreter
```
