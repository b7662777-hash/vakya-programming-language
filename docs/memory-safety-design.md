# Vākya Memory Safety & Ownership Design (V3 Roadmap)

## 1. Safety Goals & Motivation

Modern systems programming requires memory safety without sacrificing deterministic throughput. Vākya avoids garbage collection pauses in native binaries by adopting a **compile-time ownership and reference borrowing model**.

### Primary Invariants
1. **No Use-After-Free**: Memory is never accessed after its lifetime has concluded.
2. **No Double-Free**: Every resource has exactly one deterministic deallocation point.
3. **No Dangling Pointers**: References cannot outlive the target memory to which they point.
4. **No Data Races**: Concurrent memory access guarantees either exclusive mutation or shared read-only aliasing.

---

## 2. Vākya Ownership Model (`Swamitva`)

```
┌─────────────────────────────────────────────────────────────┐
│                      SINGLE OWNER RULE                      │
│  Every resource is owned by a single binding.               │
│  When the binding scope exits, the resource is reclaimed.   │
└──────────────────────────────┬──────────────────────────────┘
                               │
                ┌──────────────┴──────────────┐
                ▼                             ▼
     IMMUTABLE BORROWS (Read)      MUTABLE BORROW (Exclusive)
     Multiple concurrent readers   Single exclusive writer
```

### 2.1 Scope-Based Reclamation (RAII)
```vakya
{
    chara buffer = [1, 2, 3, 4, 5]
    // buffer allocated on heap
    vada(buffer[0])
} // buffer automatically deallocated here at block exit
```

### 2.2 Move Semantics by Default
Assigning a non-primitive value transfers ownership:
```vakya
chara list_a = [10, 20, 30]
chara list_b = list_a // Ownership moved to list_b
// vada(list_a)       // Compile error: Use of moved value 'list_a'
```

---

## 3. Reference Borrowing Rules

To allow inspecting data without transferring ownership, functions can borrow references:

```vakya
// Read-only borrow
karya calculate_sum(items: suchi) -> sankhya {
    chara total = 0
    pratyekam x madhye items {
        total += x
    }
    pratyavartaya total
}

chara nums = [1, 2, 3, 4]
chara s = calculate_sum(nums) // Borrowed
vada("Sum:", s)
vada("Original:", nums)       // nums is still valid and owned here
```
