# Vākya Native Compiler Architecture (V3 Roadmap)

## 1. Native Compilation Objective

The goal of the **Vākya Native Compiler (V3)** is to translate Vākya Intermediate Representation (IR) into standalone, optimized, native machine binaries without depending on a Python host runtime.

```
Vākya Source (.vakya)
         │
         ▼
    Type Checker
         │
         ▼
     Vākya IR
         │
    ┌────┴────────────────────────┐
    ▼                             ▼
LLVM Backend              Cranelift Backend
    │                             │
    ├─────────────┬───────────────┤
    ▼             ▼               ▼
 x86-64         ARM64          RISC-V / WASM
```

---

## 2. Backend Evaluation: LLVM vs Cranelift

| Metric | LLVM (Primary AOT) | Cranelift (Fast JIT / Dev) |
| :--- | :--- | :--- |
| **Optimization Depth** | Industry-leading (O3, vectorized, LTO) | Fast debug/dev code generation |
| **Compilation Latency**| Higher startup / compilation time | Extremely low compilation latency |
| **Target Architectures**| x86-64, ARM64, RISC-V, WebAssembly | x86-64, AArch64, RISC-V, WASM |
| **Tooling & Debugging** | DWARF / PDB debug symbols, lld linker | Native debug info support |
| **Recommendation** | **Default Release Binary Target** | **Default Fast Dev / JIT Target** |

---

## 3. Native Runtime Architecture & C ABI

1. **Primitive Representation**:
   - `sankhya`: 64-bit two's complement integer (`i64`)
   - `dashamika`: IEEE-754 double precision float (`f64`)
   - `boolean`: 1-byte boolean (`i1` / `i8`)
   - `shunya`: Null pointer / tag (`ptr null`)
2. **Collection Representation**:
   - Dynamic arrays (`suchi`): Contiguous memory pointer with capacity and length headers `(ptr, u64 len, u64 cap)`.
   - Hash maps (`naksha`): Open-addressing Robin Hood hash table.
3. **Foreign Function Interface (FFI)**:
   - Export standard C ABI calling conventions:
     ```vakya
     // PROPOSED FUTURE V3 FFI SPECIFICATION
     sarvajan karya add(a: sankhya, b: sankhya) -> sankhya {
         pratyavartaya a + b
     }
     ```
