# Concurrency & Async Operations in Vākya (Roadmap V3)

> **Status**: Design Specification for Future Roadmap Releases.

Vākya's concurrency model aims for high-performance, structured concurrency without data races.

---

## 1. Core Principles

1. **Structured Tasks**: Coroutines and asynchronous tasks must have clear lifecycles bounded by parent scopes.
2. **Channel-Based Communication**: Threads and tasks share state by communicating through channels, rather than shared mutable memory.
3. **No Uncontrolled Threads**: The runtime manages an adaptive thread pool to scale across CPU cores.

---

## 2. Future Syntax Concept

```vakya
// PROPOSED FUTURE VĀKYA CONCURRENCY CONCEPT
karya fetch_data(id: sankhya) {
    // async task
}

chara task1 = prayasa fetch_data(1)
chara task2 = prayasa fetch_data(2)

chara result1 = pratiksha task1
chara result2 = pratiksha task2
```
