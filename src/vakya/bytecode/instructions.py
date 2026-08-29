"""Bytecode instruction representation for Vākya."""

from dataclasses import dataclass
from typing import Any, Optional
from vakya.ast.nodes import Span
from .opcodes import OpCode


@dataclass
class Instruction:
    opcode: OpCode
    operand: Any = None
    span: Optional[Span] = None

    def __str__(self) -> str:
        if self.operand is not None:
            return f"{self.opcode.name} {self.operand}"
        return self.opcode.name
