"""Value stack implementation for the Vākya Virtual Machine."""

from typing import Any, List
from vakya.errors import RuntimeError, E304_RECURSION_LIMIT


class ValueStack:
    def __init__(self, max_size: int = 4096):
        self.data: List[Any] = []
        self.max_size = max_size

    def push(self, val: Any) -> None:
        if len(self.data) >= self.max_size:
            raise RuntimeError.from_info(
                E304_RECURSION_LIMIT,
                f"Virtual Machine value stack overflow (limit {self.max_size})",
            )
        self.data.append(val)

    def pop(self) -> Any:
        if not self.data:
            return None
        return self.data.pop()

    def peek(self, distance: int = 0) -> Any:
        idx = len(self.data) - 1 - distance
        if idx < 0 or idx >= len(self.data):
            return None
        return self.data[idx]

    def get(self, index: int) -> Any:
        if 0 <= index < len(self.data):
            return self.data[index]
        return None

    def set(self, index: int, val: Any) -> None:
        if 0 <= index < len(self.data):
            self.data[index] = val

    def size(self) -> int:
        return len(self.data)

    def clear(self) -> None:
        self.data.clear()

    def __repr__(self) -> str:
        return f"ValueStack({self.data!r})"
