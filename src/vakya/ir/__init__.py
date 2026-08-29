"""Vākya Intermediate Representation (IR) module."""

from .instructions import (
    IRInstruction,
    IRConst,
    IRLoad,
    IRStore,
    IRBinOp,
    IRUnaryOp,
    IRJump,
    IRBranch,
    IRLabel,
    IRCall,
    IRReturn,
    IRAllocList,
    IRAllocMap,
    IRGetIndex,
    IRSetIndex,
)
from .builder import IRBuilder, IRFunction, IRModule
from .printer import IRPrinter

__all__ = [
    "IRInstruction",
    "IRConst",
    "IRLoad",
    "IRStore",
    "IRBinOp",
    "IRUnaryOp",
    "IRJump",
    "IRBranch",
    "IRLabel",
    "IRCall",
    "IRReturn",
    "IRAllocList",
    "IRAllocMap",
    "IRGetIndex",
    "IRSetIndex",
    "IRBuilder",
    "IRFunction",
    "IRModule",
    "IRPrinter",
]
