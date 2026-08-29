"""Bytecode Chunk / CodeObject container and disassembler for Vākya."""

from dataclasses import dataclass, field
from typing import Any, List, Optional, Tuple
from vakya.ast.nodes import Span
from .opcodes import OpCode
from .instructions import Instruction


@dataclass
class Chunk:
    name: str = "<main>"
    instructions: List[Instruction] = field(default_factory=list)
    constants: List[Any] = field(default_factory=list)
    param_names: List[str] = field(default_factory=list)
    num_locals: int = 0
    upvalues: List[Tuple[bool, int, str]] = field(default_factory=list)  # (is_local, index, name)
    filename: str = "<unknown>"
    source_code: str = ""
    code_ops: List[int] = field(default_factory=list)
    code_args: List[Any] = field(default_factory=list)
    code_spans: List[Optional[Span]] = field(default_factory=list)

    def add_instruction(self, opcode: OpCode, operand: Any = None, span: Optional[Span] = None) -> int:
        idx = len(self.instructions)
        self.instructions.append(Instruction(opcode, operand, span))
        self.code_ops.append(int(opcode))
        self.code_args.append(operand)
        self.code_spans.append(span)
        return idx

    def add_constant(self, value: Any) -> int:
        for i, c in enumerate(self.constants):
            if type(c) is type(value) and c == value:
                return i
        idx = len(self.constants)
        self.constants.append(value)
        return idx

    def disassemble(self) -> str:
        lines = []
        header = f"=== Bytecode Disassembly: {self.name} (params={len(self.param_names)}, locals={self.num_locals}, upvalues={len(self.upvalues)}) ==="
        lines.append(header)

        if self.constants:
            lines.append("Constants:")
            for i, c in enumerate(self.constants):
                if isinstance(c, Chunk):
                    lines.append(f"  [{i:02d}] <Chunk: {c.name}>")
                else:
                    lines.append(f"  [{i:02d}] {c!r}")
            lines.append("Instructions:")

        last_line: Optional[int] = None
        for offset, instr in enumerate(self.instructions):
            line_str = "    |"
            if instr.span and instr.span.line != last_line:
                last_line = instr.span.line
                line_str = f"{last_line:5d}:"

            op_name = instr.opcode.name.ljust(18)
            operand_str = ""

            if instr.opcode == OpCode.CONSTANT:
                const_idx = instr.operand
                const_val = self.constants[const_idx] if 0 <= const_idx < len(self.constants) else "?"
                if isinstance(const_val, Chunk):
                    operand_str = f"{const_idx} (<Chunk: {const_val.name}>)"
                else:
                    operand_str = f"{const_idx} ({const_val!r})"
            elif instr.opcode in (OpCode.JUMP, OpCode.JUMP_IF_FALSE, OpCode.JUMP_IF_TRUE, OpCode.JUMP_IF_FALSE_OR_POP, OpCode.JUMP_IF_TRUE_OR_POP):
                operand_str = f"-> {instr.operand:04d}"
            elif instr.opcode == OpCode.MAKE_CLOSURE:
                const_idx = instr.operand
                const_val = self.constants[const_idx] if 0 <= const_idx < len(self.constants) else "?"
                chunk_name = const_val.name if isinstance(const_val, Chunk) else "?"
                operand_str = f"{const_idx} (<Chunk: {chunk_name}>)"
            elif instr.opcode == OpCode.CALL_BUILTIN:
                name, argc = instr.operand
                operand_str = f"{name} (args: {argc})"
            elif instr.operand is not None:
                operand_str = str(instr.operand)

            lines.append(f"{line_str} {offset:04d}  {op_name} {operand_str}".rstrip())

        # Disassemble nested chunk constants
        for c in self.constants:
            if isinstance(c, Chunk):
                lines.append("")
                lines.append(c.disassemble())

        return "\n".join(lines)
