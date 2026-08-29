"""CallFrame representation for the Vākya Virtual Machine."""

from typing import Any, Dict, List, Optional
from vakya.bytecode.chunk import Chunk
from .runtime import VMClosure, UpvalueCell


class CallFrame:
    """Execution call frame storing chunk, IP, and pre-allocated local variable array."""
    __slots__ = ("chunk", "closure", "ip", "stack_base", "locals", "open_upvalues")

    def __init__(
        self,
        chunk: Chunk,
        closure: Optional[VMClosure] = None,
        ip: int = 0,
        stack_base: int = 0,
        locals: Optional[List[Any]] = None,
        open_upvalues: Optional[Dict[int, UpvalueCell]] = None,
    ):
        self.chunk = chunk
        self.closure = closure
        self.ip = ip
        self.stack_base = stack_base
        if locals is not None:
            self.locals = locals
        else:
            self.locals = [None] * chunk.num_locals
        self.open_upvalues = open_upvalues if open_upvalues is not None else {}

    def get_local(self, slot: int) -> Any:
        if self.open_upvalues and slot in self.open_upvalues:
            return self.open_upvalues[slot].value
        if slot < len(self.locals):
            return self.locals[slot]
        return None

    def set_local(self, slot: int, val: Any) -> None:
        if slot >= len(self.locals):
            self.locals.extend([None] * (slot - len(self.locals) + 1))
        self.locals[slot] = val
        if self.open_upvalues and slot in self.open_upvalues:
            self.open_upvalues[slot].value = val

    def capture_upvalue(self, slot: int) -> UpvalueCell:
        if slot not in self.open_upvalues:
            val = self.locals[slot] if slot < len(self.locals) else None
            self.open_upvalues[slot] = UpvalueCell(value=val)
        return self.open_upvalues[slot]
