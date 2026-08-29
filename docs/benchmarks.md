# Vākya Benchmark & Performance Methodology

This document outlines the performance characteristics, benchmarking methodology, and empirical execution timings across Vākya execution targets.

---

## 1. Benchmarking Environment

- **Architecture**: x86-64 (Intel / AMD)
- **Host Runtime**: Python 3.12+ (CPython)
- **C Compiler (Native)**: GCC 13+ / MSVC 19+
- **Timing Harness**: High-resolution performance timer (`time.perf_counter`) with warm-up iterations and average execution timings over 10 repeated runs.

---

## 2. Workloads & Empirical Timings

| Workload Description | Iterations / Workload | AST Interpreter | Bytecode VM | VM vs Interpreter Speedup |
| :--- | :--- | :--- | :--- | :--- |
| **Arithmetic Loop** | 100,000 increments in `yavat` | 0.056s | 0.018s | **~3.1x faster** |
| **Recursive Fibonacci** | `fib(20)` recursive call tree | 0.099s | 0.038s | **~2.6x faster** |
| **Function Dispatch** | 50,000 function invocations | 0.043s | 0.015s | **~2.8x faster** |
| **Standard Library Math** | 10,000 `math.varga` & `math.PI` operations | 0.032s | 0.012s | **~2.6x faster** |

---

## 3. Running Benchmarks

To execute the baseline performance benchmarks:

```bash
python benchmarks/bench_baseline.py
```

To run detailed instruction profiling on the Bytecode VM:

```bash
python benchmarks/profile_vm.py
```
