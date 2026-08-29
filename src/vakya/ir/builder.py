"""Vākya AST to Linear Intermediate Representation (IR) Builder."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
from vakya.ast.nodes import (
    Program,
    Statement,
    Expression,
    VarDecl,
    Assignment,
    FunctionDecl,
    IfStatement,
    WhileStatement,
    ForEachStatement,
    BreakStatement,
    ContinueStatement,
    ReturnStatement,
    Block,
    ExpressionStatement,
    Literal,
    Identifier,
    BinaryExpr,
    UnaryExpr,
    ListLiteral,
    MapLiteral,
    IndexExpr,
    MemberExpr,
    CallExpr,
)
from .instructions import (
    IRInstruction,
    IRConst,
    IRLoad,
    IRStore,
    IRBinOp,
    IRUnaryOp,
    IRLabel,
    IRJump,
    IRBranch,
    IRCall,
    IRReturn,
    IRAllocList,
    IRAllocMap,
    IRGetIndex,
    IRSetIndex,
)


@dataclass
class IRFunction:
    name: str
    params: List[str] = field(default_factory=list)
    instructions: List[IRInstruction] = field(default_factory=list)


@dataclass
class IRModule:
    name: str = "<main>"
    functions: Dict[str, IRFunction] = field(default_factory=dict)
    top_level: IRFunction = field(default_factory=lambda: IRFunction("<main>"))


class IRBuilder:
    """Builds linear language-agnostic Intermediate Representation from Vākya AST."""

    def __init__(self, filename: str = "<anonymous>"):
        self.filename = filename
        self.module = IRModule(name=filename)
        self.current_function = self.module.top_level
        self._temp_counter = 0
        self._label_counter = 0

    def new_temp(self) -> str:
        self._temp_counter += 1
        return f"%t{self._temp_counter}"

    def new_label(self, prefix: str = "L") -> str:
        self._label_counter += 1
        return f"{prefix}_{self._label_counter}"

    def emit(self, instr: IRInstruction) -> None:
        self.current_function.instructions.append(instr)

    def build(self, ast: Program) -> IRModule:
        for stmt in ast.statements:
            self._build_statement(stmt)
        return self.module

    def _build_statement(self, stmt: Statement) -> None:
        if isinstance(stmt, VarDecl):
            if stmt.initializer:
                val = self._build_expression(stmt.initializer)
            else:
                val = self.new_temp()
                self.emit(IRConst(dest=val, value=None, val_type="shunya", span=stmt.span))
            self.emit(IRStore(var_name=stmt.name, src=val, span=stmt.span))

        elif isinstance(stmt, Assignment):
            val = self._build_expression(stmt.value)
            if isinstance(stmt.target, Identifier):
                if stmt.operator == "=":
                    self.emit(IRStore(var_name=stmt.target.name, src=val, span=stmt.span))
                else:
                    curr = self.new_temp()
                    self.emit(IRLoad(dest=curr, var_name=stmt.target.name, span=stmt.span))
                    res = self.new_temp()
                    op_map = {"+=": "add", "-=": "sub", "*=": "mul", "/=": "div"}
                    self.emit(IRBinOp(dest=res, op=op_map.get(stmt.operator, "add"), left=curr, right=val, span=stmt.span))
                    self.emit(IRStore(var_name=stmt.target.name, src=res, span=stmt.span))
            elif isinstance(stmt.target, IndexExpr):
                tgt = self._build_expression(stmt.target.target)
                idx = self._build_expression(stmt.target.index)
                self.emit(IRSetIndex(target=tgt, index=idx, val=val, span=stmt.span))

        elif isinstance(stmt, ExpressionStatement):
            self._build_expression(stmt.expression)

        elif isinstance(stmt, FunctionDecl):
            fn_ir = IRFunction(name=stmt.name, params=[p.name for p in stmt.params])
            self.module.functions[stmt.name] = fn_ir
            old_fn = self.current_function
            self.current_function = fn_ir

            for s in stmt.body.statements:
                self._build_statement(s)

            self.emit(IRReturn(val=None, span=stmt.span))
            self.current_function = old_fn

        elif isinstance(stmt, ReturnStatement):
            if stmt.value:
                val = self._build_expression(stmt.value)
                self.emit(IRReturn(val=val, span=stmt.span))
            else:
                self.emit(IRReturn(val=None, span=stmt.span))

        elif isinstance(stmt, IfStatement):
            cond_val = self._build_expression(stmt.condition)
            then_lbl = self.new_label("then")
            else_lbl = self.new_label("else")
            end_lbl = self.new_label("endif")

            self.emit(IRBranch(cond=cond_val, true_target=then_lbl, false_target=else_lbl, span=stmt.span))

            # Then
            self.emit(IRLabel(name=then_lbl))
            for s in stmt.then_block.statements:
                self._build_statement(s)
            self.emit(IRJump(target=end_lbl, span=stmt.span))

            # Else
            self.emit(IRLabel(name=else_lbl))
            if stmt.else_block:
                for s in stmt.else_block.statements:
                    self._build_statement(s)
            self.emit(IRJump(target=end_lbl, span=stmt.span))

            self.emit(IRLabel(name=end_lbl))

        elif isinstance(stmt, WhileStatement):
            start_lbl = self.new_label("loop_start")
            body_lbl = self.new_label("loop_body")
            end_lbl = self.new_label("loop_end")

            self.emit(IRLabel(name=start_lbl))
            cond_val = self._build_expression(stmt.condition)
            self.emit(IRBranch(cond=cond_val, true_target=body_lbl, false_target=end_lbl, span=stmt.span))

            self.emit(IRLabel(name=body_lbl))
            for s in stmt.body.statements:
                self._build_statement(s)
            self.emit(IRJump(target=start_lbl, span=stmt.span))

            self.emit(IRLabel(name=end_lbl))

        elif isinstance(stmt, Block):
            for s in stmt.statements:
                self._build_statement(s)

    def _build_expression(self, expr: Expression) -> str:
        if isinstance(expr, Literal):
            tmp = self.new_temp()
            self.emit(IRConst(dest=tmp, value=expr.value, val_type=expr.literal_type, span=expr.span))
            return tmp

        elif isinstance(expr, Identifier):
            tmp = self.new_temp()
            self.emit(IRLoad(dest=tmp, var_name=expr.name, span=expr.span))
            return tmp

        elif isinstance(expr, BinaryExpr):
            l = self._build_expression(expr.left)
            r = self._build_expression(expr.right)
            tmp = self.new_temp()
            op_map = {
                "+": "add", "-": "sub", "*": "mul", "/": "div", "%": "mod", "**": "pow",
                "==": "eq", "!=": "ne", "<": "lt", "<=": "le", ">": "gt", ">=": "ge",
                "evam": "and", "va": "or"
            }
            self.emit(IRBinOp(dest=tmp, op=op_map.get(expr.operator, expr.operator), left=l, right=r, span=expr.span))
            return tmp

        elif isinstance(expr, UnaryExpr):
            src = self._build_expression(expr.operand)
            tmp = self.new_temp()
            op_map = {"-": "neg", "na": "not"}
            self.emit(IRUnaryOp(dest=tmp, op=op_map.get(expr.operator, expr.operator), src=src, span=expr.span))
            return tmp

        elif isinstance(expr, CallExpr):
            callee_name = expr.callee.name if isinstance(expr.callee, Identifier) else "closure"
            args = [self._build_expression(arg) for arg in expr.arguments]
            tmp = self.new_temp()
            self.emit(IRCall(dest=tmp, callee=callee_name, args=args, span=expr.span))
            return tmp

        elif isinstance(expr, ListLiteral):
            elements = [self._build_expression(e) for e in expr.elements]
            tmp = self.new_temp()
            self.emit(IRAllocList(dest=tmp, elements=elements, span=expr.span))
            return tmp

        elif isinstance(expr, MapLiteral):
            pairs = [(self._build_expression(k), self._build_expression(v)) for k, v in expr.pairs]
            tmp = self.new_temp()
            self.emit(IRAllocMap(dest=tmp, pairs=pairs, span=expr.span))
            return tmp

        elif isinstance(expr, IndexExpr):
            tgt = self._build_expression(expr.target)
            idx = self._build_expression(expr.index)
            tmp = self.new_temp()
            self.emit(IRGetIndex(dest=tmp, target=tgt, index=idx, span=expr.span))
            return tmp

        return self.new_temp()
