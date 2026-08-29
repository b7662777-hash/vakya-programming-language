# Vākya Memory Safety & Ownership Specification (V3.x Roadmap)

## 1. Principles of Vākya Memory Safety (`Swamitva`)

Vākya native compilation provides zero-cost deterministic memory safety without a tracing garbage collector by enforcing compile-time ownership, affine type rules, and lexical borrowing.

```
┌─────────────────────────────────────────────────────────────┐
│                   VĀKYA OWNERSHIP INVARIANTS                │
│                                                             │
│ 1. Every resource is owned by exactly ONE binding.          │
│ 2. When the owner goes out of scope, the memory is freed.   │
│ 3. You may have EITHER:                                     │
│      - Multiple shared read-only borrows (pashya), OR       │
│      - Exactly ONE exclusive mutable borrow (chara).        │
│ 4. References must ALWAYS be valid for their lifetime.      │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Formal Terminology

| Term | Sanskrit Concept | Definition |
| :--- | :--- | :--- |
| **Owner** | *Swami* | The unique variable binding responsible for the lifetime and deallocation of a resource. |
| **Move** | *Sthanantarana* | Transfer of ownership from one binding to another. The source binding becomes invalid. |
| **Borrow (Shared)** | *Pashya* | Temporary read-only aliased access to a resource without transferring ownership. |
| **Borrow (Exclusive)** | *Chara* | Temporary unique mutable access to a resource. No other reads or writes allowed concurrently. |
| **Lifetime** | *Aayushya* | The lexical scope during which a reference or binding is guaranteed valid. |
| **Reclamation** | *Moksha* | Deterministic deallocation of memory when an owning binding leaves scope (RAII). |

---

## 3. Ownership Invariants & Move Semantics

### Rule 1: Move on Assignment for Heap Types
Primitive types (`sankhya`, `dashamika`, `boolean`) implement copy semantics. Heap types (`suchi`, `naksha`, `shabda`) move ownership on assignment:

```vakya
chara list_a = [1, 2, 3]
chara list_b = list_a // Ownership MOVES to list_b

// Error [E501]: Use of moved value 'list_a'
// vada(list_a[0])
```

---

## 4. Borrowing & Aliasing Rules

### Rule 2: Multiple Shared Readers (`pashya`)
```vakya
karya count_elements(pashya items: suchi) -> sankhya {
    pratyavartaya lamba(items)
}

chara data = [10, 20, 30]
chara c1 = count_elements(data) // Borrow 1
chara c2 = count_elements(data) // Borrow 2 (Concurrent readers allowed)
vada("Original:", data)         // data still valid
```

### Rule 3: Exclusive Mutable Borrow (`chara`)
```vakya
karya append_zero(chara items: suchi) {
    suchi_jodo(items, 0)
}

chara data = [10, 20]
append_zero(data) // Exclusive borrow
vada(data)        // [10, 20, 0]
```

---

## 5. Diagnostic Error Catalog for Ownership Violations

### `E501`: Use of Moved Value
- **Trigger**: Attempting to read or pass a variable after its ownership has been transferred.
- **Example**:
  ```vakya
  chara a = [10, 20]
  chara b = a
  vada(a[0]) // Error [E501]: Value 'a' was moved into 'b' on line 2
  ```

### `E502`: Mutable Borrow While Shared Borrows Active
- **Trigger**: Attempting to create an exclusive mutable reference while shared read-only borrows are active.
- **Example**:
  ```vakya
  chara items = [1, 2, 3]
  chara ref1 = pashya items
  chara ref2 = chara items // Error [E502]: Cannot borrow 'items' as mutable while shared borrow 'ref1' is active
  ```

### `E503`: Multiple Concurrent Mutable Borrows
- **Trigger**: Creating two simultaneous mutable references to the same target.
- **Example**:
  ```vakya
  chara m1 = chara items
  chara m2 = chara items // Error [E503]: Cannot borrow 'items' as mutable more than once
  ```

### `E504`: Returning Reference to Local Stack Variable
- **Trigger**: A function attempting to return a reference whose lifetime concludes at function exit.
- **Example**:
  ```vakya
  karya get_ref() -> pashya suchi {
      chara local_buf = [1, 2]
      pratyavartaya pashya local_buf // Error [E504]: Cannot return reference to local variable 'local_buf'
  }
  ```

### `E505`: Mutation of Target While Borrowed
- **Trigger**: Modifying an owned resource while an active borrow exists.
- **Example**:
  ```vakya
  chara nums = [1, 2, 3]
  chara r = pashya nums
  suchi_jodo(nums, 4) // Error [E505]: Cannot mutate 'nums' while borrowed by 'r'
  vada(r)
  ```
