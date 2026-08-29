# Vākya Native Backend Decision Matrix

## 1. Objective

To select the permanent native code generation backends for **Vākya V3+** based on measured engineering requirements: compilation latency, optimization quality, portability, debugging support, and static linking simplicity.

---

## 2. Technical Evaluation

| Criterion | LLVM Backend | Cranelift Backend | Native C Backend |
| :--- | :--- | :--- | :--- |
| **Optimization Depth** | ★★★★★ (O3, Vectorization, LTO) | ★★★☆☆ (Basic optimizations) | ★★★★☆ (Delegates to host CC) |
| **Compilation Latency** | ★★☆☆☆ (Heavyweight LLVM passes) | ★★★★★ (Extremely fast JIT/AOT) | ★★★☆☆ (Medium) |
| **Cross-Platform Targets** | x86-64, ARM64, RISC-V, WASM | x86-64, AArch64, RISC-V, WASM | Any platform with standard C compiler |
| **Debug Info (DWARF/PDB)**| Native first-class DWARF/CodeView | Growing DWARF support | Host debugger integration (GDB/LLDB/MSVC) |
| **Binary Self-Containment**| Standalone static binary (`.exe`/ELF) | Standalone static binary | Standalone static binary |
| **Dependency Weight** | Heavy (LLVM C-API / llvmlite) | Lightweight Rust crate | Minimal zero-dependency runtime header |

---

## 3. Decision & Multi-Backend Architecture

Vākya adopts a tiered native backend strategy:
1. **Tier 1 (Default AOT Release)**: **LLVM / Native Backend** for maximum runtime execution speed, loop vectorization, and static binary linking.
2. **Tier 2 (Fast Interactive Dev / JIT)**: **Cranelift** for lightning-fast compilation turnarounds and WASM compilation.
3. **Tier 3 (Reference & Bootstrap Backend)**: **Portable Native C (`--backend=c`)** providing a transparent, auditable bootstrap bridge and maximum cross-platform portability.
