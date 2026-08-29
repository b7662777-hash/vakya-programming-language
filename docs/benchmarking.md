# Benchmarking and Performance Profiling in Vākya

## 1. Running the Benchmark Suite

To measure frontend throughput and compare AST Interpreter vs Bytecode VM execution:

```bash
python benchmarks/bench_baseline.py
```

---

## 2. Baseline Measurements

### Frontend Throughput (Python 3.12 Reference Runtime)
* **Lexer**: ~650,000+ tokens / second
* **Parser**: ~9,500+ parses / second
* **Bytecode Compiler**: ~70,000+ AST-to-bytecode compiles / second

### Execution Analysis
* The AST Interpreter recurses directly within Python's native C function stack.
* The V2 Bytecode VM simulates a virtual stack and instruction loop within Python.
* As detailed in the [Native Compiler Roadmap](native-compiler.md), true 10x-50x native speedups will be unlocked in V3 via the Vākya Intermediate Representation (IR) and LLVM / Cranelift native code emission.
