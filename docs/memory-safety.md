# Swamitva (स्वामित्व) — Compile-Time Memory Safety

**Swamitva** is Vākya's compile-time ownership and borrow checking system. It guarantees memory safety, prevents data races, and eliminates dangling pointers without requiring a runtime garbage collector.

---

## 1. Core Principles

1. **Every Resource Has Exactly One Owner**: Each value on the heap or non-primitive object is bound to a single variable at any given time.
2. **Move Semantics by Default**: When a non-primitive value is assigned to another variable or passed to a function, ownership is transferred (*moved*). The original variable becomes invalid.
3. **Borrowing Invariants**:
   - You may have any number of active **shared borrows** (`&T`).
   - You may have at most **one exclusive mutable borrow** (`&mut T`).
   - Shared and mutable borrows cannot coexist simultaneously.
4. **References Must Always Be Valid**: A borrow cannot outlive the lifetime of its referenced owner.

---

## 2. Compile-Time Diagnostics (E501–E505)

### E501: Use After Move
Attempting to read or pass a variable whose ownership has already been transferred to another binding:

```vakya
chara list_a = [1, 2, 3]
chara list_b = list_a       // Ownership moved to list_b
vada(list_a)                 // Error [E501]: Use of moved value 'list_a'
```

**Remediation**: Use a borrow (`&list_a`) or access the new owner `list_b`.

---

### E502: Mutable Borrow Conflict
Attempting to create a mutable borrow while active shared borrows exist:

```vakya
chara data = {"key": "value"}
chara ref1 = &data           // Shared borrow
chara ref2 = &mut data       // Error [E502]: Cannot borrow 'data' as mutable because it is already borrowed as immutable
vada(ref1)
```

**Remediation**: Ensure immutable borrows have expired before creating an exclusive mutable borrow.

---

### E503: Multiple Mutable Borrows
Attempting to create more than one active mutable borrow to the same resource:

```vakya
chara buffer = [10, 20]
chara m1 = &mut buffer
chara m2 = &mut buffer       // Error [E503]: Cannot borrow 'buffer' as mutable more than once at a time
```

**Remediation**: Limit mutable access to one active alias at a time.

---

### E504: Dangling Reference
Attempting to return or retain a reference to a local variable that goes out of scope:

```vakya
karya get_dangling() {
    chara local_val = [1, 2, 3]
    pratyavartaya &local_val // Error [E504]: Cannot return reference to local variable 'local_val'
}
```

**Remediation**: Return the owned value directly (`pratyavartaya local_val`) instead of a reference.

---

### E505: Mutation While Borrowed
Attempting to mutate a variable directly while active borrows exist:

```vakya
chara numbers = [1, 2, 3]
chara r = &numbers           // Shared borrow active
numbers = [4, 5, 6]          // Error [E505]: Cannot assign to 'numbers' because it is currently borrowed
vada(r)
```

**Remediation**: Perform mutations only after all references to the value have completed their usage.

---

## 3. Running the Swamitva Borrow Checker

To check a Vākya source file without executing:
```bash
vakya check my_program.vakya
```

Machine-readable JSON output for IDEs and CI:
```bash
vakya check my_program.vakya --format=json
```
