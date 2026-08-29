"""Vākya Compile-Time Borrow Checker & Memory Ownership (Swamitva) Analyzer."""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Set, Tuple

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
    ImportStatement,
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
    Span,
)
from vakya.errors import (
    BorrowError,
    E501_USE_AFTER_MOVE,
    E502_MUTABLE_BORROW_CONFLICT,
    E503_MULTIPLE_MUTABLE_BORROWS,
    E504_DANGLING_REFERENCE,
    E505_MUTATION_WHILE_BORROWED,
)


class OwnershipKind(Enum):
    COPY = auto()   # Primitives: sankhya, dashamika, boolean, shunya
    MOVE = auto()   # Heap types: suchi, naksha, shabda, custom resources


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


@dataclass
class VariableBinding:
    name: str
    kind: OwnershipKind
    scope_depth: int
    declared_at: Optional[Span] = None
    is_local_to_fn: bool = False


class BorrowChecker:
    """Enforces single-owner, affine move semantics, and lexical borrow lifetimes."""

    def __init__(self, filename: str = "<unknown>", source_code: str = ""):
        self.filename = filename
        self.source_code = source_code
        self.scope_depth: int = 0
        self.in_function: bool = False
        self._loan_counter: int = 0

        self.bindings: Dict[str, VariableBinding] = {}
        self.move_states: Dict[str, MoveRecord] = {}
        self.active_loans: List[Loan] = []
        self.scope_bindings_stack: List[List[str]] = []

    def check(self, program: Program) -> None:
        """Run borrow and ownership analysis on the validated AST."""
        self.scope_depth = 0
        self.bindings.clear()
        self.move_states.clear()
        self.active_loans.clear()
        self.scope_bindings_stack = [[]]

        for stmt in program.statements:
            self._check_statement(stmt)

    def _enter_scope(self) -> None:
        self.scope_depth += 1
        self.scope_bindings_stack.append([])

    def _exit_scope(self) -> None:
        # Drop all loans created in this scope
        self.active_loans = [l for l in self.active_loans if l.scope_depth < self.scope_depth]

        # Drop bindings created in this scope
        if self.scope_bindings_stack:
            vars_to_drop = self.scope_bindings_stack.pop()
            for v in vars_to_drop:
                self.bindings.pop(v, None)
                self.move_states.pop(v, None)

        self.scope_depth -= 1

    def _check_statement(self, stmt: Statement) -> None:
        if isinstance(stmt, VarDecl):
            kind = self._infer_ownership_kind(stmt.type_annotation, stmt.initializer)
            if stmt.initializer is not None:
                self._check_expression(stmt.initializer, is_move_context=(kind == OwnershipKind.MOVE))

            binding = VariableBinding(
                name=stmt.name,
                kind=kind,
                scope_depth=self.scope_depth,
                declared_at=stmt.span,
                is_local_to_fn=self.in_function,
            )
            self.bindings[stmt.name] = binding
            self.move_states[stmt.name] = MoveRecord(is_moved=False)
            if self.scope_bindings_stack:
                self.scope_bindings_stack[-1].append(stmt.name)

        elif isinstance(stmt, Assignment):
            if isinstance(stmt.target, Identifier):
                var_name = stmt.target.name
                # Check if target is currently borrowed
                for loan in self.active_loans:
                    if loan.place_name == var_name:
                        raise BorrowError.from_info(
                            E505_MUTATION_WHILE_BORROWED,
                            f"Cannot reassign or mutate '{var_name}' while actively borrowed",
                            filename=self.filename,
                            line=stmt.span.line if stmt.span else None,
                            column=stmt.span.column if stmt.span else None,
                            length=stmt.span.length if stmt.span else 1,
                            source_code=self.source_code,
                            help_text=f"End active borrows of '{var_name}' before reassigning.",
                        )

                # If reassigning a previously moved variable, it becomes active again
                if var_name in self.move_states:
                    self.move_states[var_name] = MoveRecord(is_moved=False)

                kind = self.bindings[var_name].kind if var_name in self.bindings else OwnershipKind.COPY
                self._check_expression(stmt.value, is_move_context=(kind == OwnershipKind.MOVE))

            elif isinstance(stmt.target, IndexExpr):
                # Target mutation
                if isinstance(stmt.target.target, Identifier):
                    var_name = stmt.target.target.name
                    for loan in self.active_loans:
                        if loan.place_name == var_name and not loan.is_mutable:
                            raise BorrowError.from_info(
                                E505_MUTATION_WHILE_BORROWED,
                                f"Cannot mutate collection '{var_name}' while shared immutable borrow is active",
                                filename=self.filename,
                                line=stmt.span.line if stmt.span else None,
                                column=stmt.span.column if stmt.span else None,
                                length=stmt.span.length if stmt.span else 1,
                                source_code=self.source_code,
                                help_text=f"End immutable borrows of '{var_name}' before modifying elements.",
                            )
                self._check_expression(stmt.target.target)
                self._check_expression(stmt.target.index)
                self._check_expression(stmt.value)

        elif isinstance(stmt, FunctionDecl):
            prev_in_fn = self.in_function
            self.in_function = True
            self._enter_scope()

            for param in stmt.params:
                p_kind = OwnershipKind.MOVE if param.type_annotation in ("suchi", "naksha", "shabda") else OwnershipKind.COPY
                self.bindings[param.name] = VariableBinding(
                    name=param.name,
                    kind=p_kind,
                    scope_depth=self.scope_depth,
                    declared_at=param.span,
                    is_local_to_fn=True,
                )
                self.move_states[param.name] = MoveRecord(is_moved=False)
                self.scope_bindings_stack[-1].append(param.name)

            for s in stmt.body.statements:
                self._check_statement(s)

            self._exit_scope()
            self.in_function = prev_in_fn

        elif isinstance(stmt, IfStatement):
            self._check_expression(stmt.condition)
            self._check_block(stmt.then_block)
            for cond, blk in stmt.else_if_branches:
                self._check_expression(cond)
                self._check_block(blk)
            if stmt.else_block:
                self._check_block(stmt.else_block)

        elif isinstance(stmt, WhileStatement):
            self._check_expression(stmt.condition)
            self._check_block(stmt.body)

        elif isinstance(stmt, ForEachStatement):
            self._check_expression(stmt.iterable)
            self._enter_scope()
            self.bindings[stmt.variable] = VariableBinding(
                name=stmt.variable,
                kind=OwnershipKind.COPY,
                scope_depth=self.scope_depth,
                declared_at=stmt.span,
                is_local_to_fn=self.in_function,
            )
            self.move_states[stmt.variable] = MoveRecord(is_moved=False)
            self.scope_bindings_stack[-1].append(stmt.variable)
            for s in stmt.body.statements:
                self._check_statement(s)
            self._exit_scope()

        elif isinstance(stmt, ReturnStatement):
            if stmt.value is not None:
                # Check for dangling reference to local variable
                if isinstance(stmt.value, Identifier):
                    var_name = stmt.value.name
                    if var_name in self.bindings and self.bindings[var_name].is_local_to_fn:
                        for loan in self.active_loans:
                            if loan.place_name == var_name:
                                raise BorrowError.from_info(
                                    E504_DANGLING_REFERENCE,
                                    f"Cannot return reference to local variable '{var_name}' allocated on function stack frame",
                                    filename=self.filename,
                                    line=stmt.span.line if stmt.span else None,
                                    column=stmt.span.column if stmt.span else None,
                                    length=stmt.span.length if stmt.span else 1,
                                    source_code=self.source_code,
                                    help_text=f"Return an owned value or allocate '{var_name}' in caller scope.",
                                )
                self._check_expression(stmt.value)

        elif isinstance(stmt, ImportStatement):
            name = stmt.alias if stmt.alias else stmt.module_name
            self.bindings[name] = VariableBinding(
                name=name,
                kind=OwnershipKind.COPY,
                scope_depth=self.scope_depth,
                declared_at=stmt.span,
                is_local_to_fn=self.in_function,
            )
            self.move_states[name] = MoveRecord(is_moved=False)
            self.scope_bindings_stack[-1].append(name)

        elif isinstance(stmt, Block):
            self._check_block(stmt)

        elif isinstance(stmt, ExpressionStatement):
            self._check_expression(stmt.expression)

    def _check_block(self, block: Block) -> None:
        self._enter_scope()
        for s in block.statements:
            self._check_statement(s)
        self._exit_scope()

    def _check_expression(self, expr: Expression, is_move_context: bool = False) -> None:
        if isinstance(expr, Identifier):
            name = expr.name
            # 1. Check if variable was moved
            if name in self.move_states and self.move_states[name].is_moved:
                moved_at = self.move_states[name].moved_at
                line_info = f" on line {moved_at.line}" if moved_at else ""
                raise BorrowError.from_info(
                    E501_USE_AFTER_MOVE,
                    f"Use of moved value '{name}'. Value was moved previously{line_info}",
                    filename=self.filename,
                    line=expr.span.line if expr.span else None,
                    column=expr.span.column if expr.span else None,
                    length=expr.span.length if expr.span else 1,
                    source_code=self.source_code,
                    help_text=f"Clone the value or avoid using '{name}' after transferring ownership.",
                )

            # 2. If used in a move context for heap types, mark as moved
            if is_move_context and name in self.bindings:
                if self.bindings[name].kind == OwnershipKind.MOVE:
                    # Verify no active borrows exist on name
                    for loan in self.active_loans:
                        if loan.place_name == name:
                            raise BorrowError.from_info(
                                E505_MUTATION_WHILE_BORROWED,
                                f"Cannot move '{name}' while actively borrowed",
                                filename=self.filename,
                                line=expr.span.line if expr.span else None,
                                column=expr.span.column if expr.span else None,
                                length=expr.span.length if expr.span else 1,
                                source_code=self.source_code,
                                help_text=f"End active borrows of '{name}' before moving.",
                            )
                    self.move_states[name] = MoveRecord(is_moved=True, moved_at=expr.span)

        elif isinstance(expr, BinaryExpr):
            self._check_expression(expr.left)
            self._check_expression(expr.right)

        elif isinstance(expr, UnaryExpr):
            self._check_expression(expr.operand)

        elif isinstance(expr, CallExpr):
            self._check_expression(expr.callee)
            for arg in expr.arguments:
                self._check_expression(arg)

        elif isinstance(expr, ListLiteral):
            for el in expr.elements:
                self._check_expression(el, is_move_context=True)

        elif isinstance(expr, MapLiteral):
            for k, v in expr.pairs:
                self._check_expression(k)
                self._check_expression(v, is_move_context=True)

        elif isinstance(expr, IndexExpr):
            self._check_expression(expr.target)
            self._check_expression(expr.index)

        elif isinstance(expr, MemberExpr):
            self._check_expression(expr.target)

    def _infer_ownership_kind(self, type_ann: Optional[str], initializer: Optional[Expression]) -> OwnershipKind:
        if type_ann in ("suchi", "naksha", "shabda"):
            return OwnershipKind.MOVE
        if type_ann in ("sankhya", "dashamika", "boolean", "shunya"):
            return OwnershipKind.COPY

        if isinstance(initializer, (ListLiteral, MapLiteral)):
            return OwnershipKind.MOVE
        if isinstance(initializer, Literal):
            if isinstance(initializer.value, str):
                return OwnershipKind.MOVE
            return OwnershipKind.COPY

        if isinstance(initializer, Identifier):
            if initializer.name in self.bindings:
                return self.bindings[initializer.name].kind

        return OwnershipKind.COPY
