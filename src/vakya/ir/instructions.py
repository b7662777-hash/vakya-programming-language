"""Instruction definitions for the Vākya Intermediate Representation (IR)."""

from dataclasses import dataclass, field
from typing import Any, List, Optional, Tuple
from vakya.ast.nodes import Span


@dataclass(kw_only=True)
class IRInstruction:
    """Base class for all IR instructions."""
    span: Optional[Span] = None


@dataclass(kw_only=True)
class IRConst(IRInstruction):
    dest: str
    value: Any
    val_type: str

    def __str__(self) -> str:
        return f"{self.dest} = const {self.value!r} : {self.val_type}"


@dataclass(kw_only=True)
class IRLoad(IRInstruction):
    dest: str
    var_name: str

    def __str__(self) -> str:
        return f"{self.dest} = load {self.var_name}"


@dataclass(kw_only=True)
class IRStore(IRInstruction):
    var_name: str
    src: str

    def __str__(self) -> str:
        return f"store {self.var_name}, {self.src}"


@dataclass(kw_only=True)
class IRBinOp(IRInstruction):
    dest: str
    op: str
    left: str
    right: str

    def __str__(self) -> str:
        return f"{self.dest} = {self.op} {self.left}, {self.right}"


@dataclass(kw_only=True)
class IRUnaryOp(IRInstruction):
    dest: str
    op: str
    src: str

    def __str__(self) -> str:
        return f"{self.dest} = {self.op} {self.src}"


@dataclass(kw_only=True)
class IRLabel(IRInstruction):
    name: str

    def __str__(self) -> str:
        return f"{self.name}:"


@dataclass(kw_only=True)
class IRJump(IRInstruction):
    target: str

    def __str__(self) -> str:
        return f"jump {self.target}"


@dataclass(kw_only=True)
class IRBranch(IRInstruction):
    cond: str
    true_target: str
    false_target: str

    def __str__(self) -> str:
        return f"br {self.cond}, {self.true_target}, {self.false_target}"


@dataclass(kw_only=True)
class IRCall(IRInstruction):
    dest: Optional[str] = None
    callee: str
    args: List[str] = field(default_factory=list)

    def __str__(self) -> str:
        args_str = ", ".join(self.args)
        if self.dest:
            return f"{self.dest} = call @{self.callee}({args_str})"
        return f"call @{self.callee}({args_str})"


@dataclass(kw_only=True)
class IRReturn(IRInstruction):
    val: Optional[str] = None

    def __str__(self) -> str:
        return f"ret {self.val if self.val else 'void'}"


@dataclass(kw_only=True)
class IRAllocList(IRInstruction):
    dest: str
    elements: List[str] = field(default_factory=list)

    def __str__(self) -> str:
        return f"{self.dest} = alloc_list [{', '.join(self.elements)}]"


@dataclass(kw_only=True)
class IRAllocMap(IRInstruction):
    dest: str
    pairs: List[Tuple[str, str]] = field(default_factory=list)

    def __str__(self) -> str:
        pairs_str = ", ".join(f"{k}: {v}" for k, v in self.pairs)
        return f"{self.dest} = alloc_map {{{pairs_str}}}"


@dataclass(kw_only=True)
class IRGetIndex(IRInstruction):
    dest: str
    target: str
    index: str

    def __str__(self) -> str:
        return f"{self.dest} = get_index {self.target}[{self.index}]"


@dataclass(kw_only=True)
class IRSetIndex(IRInstruction):
    target: str
    index: str
    val: str

    def __str__(self) -> str:
        return f"set_index {self.target}[{self.index}] = {self.val}"
