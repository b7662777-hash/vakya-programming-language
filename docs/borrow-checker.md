# Vākya Borrow Checker & Memory Ownership Soundness Specification

## 1. Abstract State Machine & Data Model

The Vākya Borrow Checker (`src/vakya/typechecker/borrow_checker.py`) statically guarantees memory safety and data-race freedom at compile time without a runtime garbage collector.

```text
┌─────────────────────────────────────────────────────────────┐
│                 VARIABLE OWNERSHIP LIFECYCLE                │
│                                                             │
│       ┌───────────────┐     Declaration (chara/dhruva)      │
│       │ UNINITIALIZED ├───────────────────────┐             │
│       └───────────────┘                       ▼             │
│                              Assignment ┌───────────┐       │
│                      ┌─────────────────►│   OWNED   │       │
│                      │                  └─────┬─────┘       │
│                      │                        │             │
│                      │                        │ Move        │
│                      │                        ▼             │
│                      │                  ┌───────────┐       │
│                      └──────────────────┤   MOVED   │       │
│                                         └───────────┘       │
│                                               │ Read/Use    │
│                                               ▼             │
│                                       [Error E501 Trap]     │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Formal Invariants

1. **Affine Move Discipline**: Heap-backed values (`suchi`, `naksha`, `shabda`) have exactly one unique owner (*Swami*). Assignment transfers ownership; the source transitions to `MOVED` and cannot be accessed (`E501`).
2. **Copy Exemption**: Primitives (`sankhya`, `dashamika`, `boolean`, `shunya`) implement bitwise duplication and are exempt from move invalidation.
3. **Aliasing XOR Mutability**: At any lexical program point, a resource may have:
   - Arbitrarily many active shared immutable loans (`pashya`), **OR**
   - At most one active exclusive mutable loan (`chara`).
4. **Lexical Lifetime Confinement**: No loan may outlive the lexical scope depth of its underlying resource (`E504`).
5. **No Mutation While Borrowed**: Mutating or transferring an owned resource while an active loan is open is rejected (`E505`).

---

## 3. Compiler Data Structures

```python
class OwnershipKind(Enum):
    COPY = auto()   # sankhya, dashamika, boolean, shunya
    MOVE = auto()   # suchi, naksha, shabda, custom heap structures

@dataclass
class MoveRecord:
    is_moved: bool = False
    moved_at: Optional[Span] = None
    moved_to: Optional[str] = None

@dataclass
class Loan:
    id: int
    place_name: str
    is_mutable: bool
    borrowed_at: Optional[Span] = None
    scope_depth: int = 0
```

---

## 4. Compile-Time Diagnostic Error Catalog

| Code | Diagnostic Title | Rule Violation |
| :--- | :--- | :--- |
| **`E501`** | `Use of moved value` | Reading or passing a variable whose ownership was previously transferred. |
| **`E502`** | `Cannot borrow as mutable while shared borrows active` | Attempting exclusive borrow while active shared readers exist. |
| **`E503`** | `Multiple mutable borrows` | Attempting to create more than one simultaneous mutable loan. |
| **`E504`** | `Returning reference to local variable` | Escaping a reference to stack-allocated memory. |
| **`E505`** | `Mutation of target while borrowed` | Modifying or moving a resource with active loans. |
