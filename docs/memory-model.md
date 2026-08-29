# Vākya Memory Model & Resource Management

## 1. Abstract Memory Architecture

Vākya native compilation manages system memory through a deterministic **Ownership & Lexical Borrowing** model (*Swamitva*) without a garbage collector:

```text
┌─────────────────────────────────────────────────────────────┐
│                      STACK MEMORY                           │
│  - Call Frames (CallFrame)                                  │
│  - Primitives (sankhya: int64_t, dashamika: double, bool)   │
│  - Fat pointers to Heap Buffers (ptr, len, cap)             │
│  - Lexical Borrow References (Loan IDs, Place trackers)     │
└──────────────────────────────┬──────────────────────────────┘
                               │ Allocates / Owns
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                      HEAP MEMORY                            │
│  - Dynamic Arrays (VakyaList: items, length, capacity)      │
│  - Associative Maps (VakyaMap: hash buckets, key/val slots) │
│  - Dynamic Strings (VakyaString: data, length)              │
│  - Closures with captured upvalues (VMClosure / env env_t)  │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Copy Semantics vs Move Semantics

### 2.1 Copy Types (Stack-Only)
Types that are small and trivial to duplicate bitwise implement **Copy Semantics**:
- `sankhya` (64-bit signed integer)
- `dashamika` (64-bit IEEE 754 float)
- `boolean` (`satya` / `asatya`)
- `shunya` (null unit)

When copied (`chara b = a`), the source variable `a` remains valid and active.

### 2.2 Move Types (Heap-Backed)
Types managing heap allocations implement **Move Semantics**:
- `suchi` (dynamic array)
- `naksha` (associative map)
- `shabda` (dynamically allocated string)

When assigned (`chara b = a`), ownership of the resource is transferred to `b`. Variable `a` enters the `MOVED` state and subsequent access is rejected at compile time with **`Error [E501]`**.

---

## 3. Lexical Borrowing Rules

| Borrow Type | Keyword / Syntax | Permissions | Concurrency |
| :--- | :--- | :--- | :--- |
| **Shared Borrow** | `pashya x` | Read-only | Multiple shared loans allowed simultaneously |
| **Exclusive Borrow**| `chara x` | Read/Write | Exactly ONE active loan; no other loans permitted |

```vakya
// Shared borrows (pashya)
chara data = [10, 20, 30]
chara r1 = pashya data
chara r2 = pashya data // OK: Multiple shared readers

// Exclusive borrow conflict (E502)
// chara m = chara data // Error [E502]: Cannot borrow as mutable while shared borrows active
```

---

## 4. Deterministic Destruction (*Moksha*)

When an owning binding exits its lexical scope (`_exit_scope` / closing `}`):
1. Any active loans associated with the scope depth are dismissed.
2. The owned heap memory buffer is freed via `vakya_list_free`, `vakya_string_free`, or custom deallocators.
3. No lingering references or dangling pointers can outlive the stack frame (**`Error [E504]`**).
