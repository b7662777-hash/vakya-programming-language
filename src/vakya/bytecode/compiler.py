"""Bytecode Compiler for the Vākya Programming Language.

Translates a validated Vākya AST into executable Bytecode Chunks with
local variable resolution, closure upvalues, and jump patching.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Set

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
from .opcodes import OpCode
from .instructions import Instruction
from .chunk import Chunk

BUILTIN_NAMES = {
    "vada",
    "puchha",
    "lamba",
    "prakaar",
    "suchi_jodo",
    "suchi_hatao",
    "shabda_bada",
    "shabda_chhota",
    "shabda_trim",
    "__vakya_iter",
}


@dataclass
class Local:
    name: str
    depth: int
    is_captured: bool = False


@dataclass
class Upvalue:
    index: int
    is_local: bool
    name: str


@dataclass
class LoopInfo:
    start_offset: int
    continue_offset: int
    break_jumps: List[int] = field(default_factory=list)


class FunctionCompiler:
    def __init__(self, name: str, enclosing: Optional["FunctionCompiler"] = None, filename: str = "<unknown>", source_code: str = ""):
        self.name = name
        self.enclosing = enclosing
        self.filename = filename
        self.source_code = source_code
        self.chunk = Chunk(name=name, filename=filename, source_code=source_code)
        self.locals: List[Local] = []
        self.upvalues: List[Upvalue] = []
        self.scope_depth: int = 0
        self.loop_stack: List[LoopInfo] = []

    def enter_scope(self) -> None:
        self.scope_depth += 1

    def exit_scope(self, span: Optional[Span] = None) -> None:
        self.scope_depth -= 1
        # Pop locals that went out of scope
        while self.locals and self.locals[-1].depth > self.scope_depth:
            # We can leave the slot or pop
            self.locals.pop()

    def add_local(self, name: str) -> int:
        local = Local(name=name, depth=self.scope_depth)
        slot = len(self.locals)
        self.locals.append(local)
        if len(self.locals) > self.chunk.num_locals:
            self.chunk.num_locals = len(self.locals)
        return slot

    def resolve_local(self, name: str) -> int:
        for i in range(len(self.locals) - 1, -1, -1):
            if self.locals[i].name == name:
                return i
        return -1

    def resolve_upvalue(self, name: str) -> int:
        if self.enclosing is None:
            return -1

        # Check local in enclosing function
        local_idx = self.enclosing.resolve_local(name)
        if local_idx != -1:
            self.enclosing.locals[local_idx].is_captured = True
            return self._add_upvalue(index=local_idx, is_local=True, name=name)

        # Check upvalue in enclosing function
        upval_idx = self.enclosing.resolve_upvalue(name)
        if upval_idx != -1:
            return self._add_upvalue(index=upval_idx, is_local=False, name=name)

        return -1

    def _add_upvalue(self, index: int, is_local: bool, name: str) -> int:
        for i, upval in enumerate(self.upvalues):
            if upval.index == index and upval.is_local == is_local:
                return i
        idx = len(self.upvalues)
        self.upvalues.append(Upvalue(index=index, is_local=is_local, name=name))
        self.chunk.upvalues.append((is_local, index, name))
        return idx

    def emit(self, opcode: OpCode, operand: Any = None, span: Optional[Span] = None) -> int:
        return self.chunk.add_instruction(opcode, operand, span)

    def emit_constant(self, value: Any, span: Optional[Span] = None) -> int:
        const_idx = self.chunk.add_constant(value)
        return self.emit(OpCode.CONSTANT, const_idx, span)

    def emit_jump(self, opcode: OpCode, span: Optional[Span] = None) -> int:
        return self.emit(opcode, 0xFFFF, span)

    def patch_jump(self, jump_offset: int) -> None:
        target = len(self.chunk.instructions)
        self.chunk.instructions[jump_offset].operand = target
        if jump_offset < len(self.chunk.code_args):
            self.chunk.code_args[jump_offset] = target


class BytecodeCompiler:
    def __init__(self, filename: str = "<unknown>", source_code: str = "", optimize: bool = False):
        self.filename = filename
        self.source_code = source_code
        self.optimize = optimize
        self.current: FunctionCompiler = FunctionCompiler("<main>", None, filename, source_code)
        self.builtin_names: Set[str] = BUILTIN_NAMES

    def compile(self, program: Program) -> Chunk:
        """Compile a Program AST into a top-level Chunk."""
        # Pass 1: Hoist top-level functions
        for stmt in program.statements:
            if isinstance(stmt, FunctionDecl):
                self._compile_function_decl(stmt, is_top_level=True)

        # Pass 2: Compile remaining statements
        for stmt in program.statements:
            if not isinstance(stmt, FunctionDecl):
                self._compile_statement(stmt)

        # Main chunk returns NULL and HALTs
        self.current.emit(OpCode.NULL)
        self.current.emit(OpCode.HALT)
        return self.current.chunk

    # Statement Compilers
    def _compile_statement(self, stmt: Statement) -> None:
        if isinstance(stmt, VarDecl):
            self._compile_var_decl(stmt)
        elif isinstance(stmt, Assignment):
            self._compile_assignment(stmt)
        elif isinstance(stmt, FunctionDecl):
            self._compile_function_decl(stmt, is_top_level=False)
        elif isinstance(stmt, IfStatement):
            self._compile_if(stmt)
        elif isinstance(stmt, WhileStatement):
            self._compile_while(stmt)
        elif isinstance(stmt, ForEachStatement):
            self._compile_for_each(stmt)
        elif isinstance(stmt, BreakStatement):
            self._compile_break(stmt)
        elif isinstance(stmt, ContinueStatement):
            self._compile_continue(stmt)
        elif isinstance(stmt, ReturnStatement):
            self._compile_return(stmt)
        elif isinstance(stmt, ImportStatement):
            self._compile_import(stmt)
        elif isinstance(stmt, Block):
            self._compile_block(stmt)
        elif isinstance(stmt, ExpressionStatement):
            self._compile_expression(stmt.expression)
            self.current.emit(OpCode.POP, span=stmt.span)

    def _compile_import(self, stmt: ImportStatement) -> None:
        name = stmt.alias if stmt.alias else stmt.module_name
        self.current.emit(OpCode.IMPORT_MODULE, (stmt.module_name, name), span=stmt.span)

    def _compile_var_decl(self, decl: VarDecl) -> None:
        if decl.initializer is not None:
            self._compile_expression(decl.initializer)
        else:
            self.current.emit(OpCode.NULL, span=decl.span)

        if self.current.scope_depth > 0:
            # Local variable
            slot = self.current.add_local(decl.name)
            self.current.emit(OpCode.STORE_LOCAL, slot, span=decl.span)
        else:
            # Global variable
            self.current.emit(OpCode.STORE_GLOBAL, decl.name, span=decl.span)

    def _compile_assignment(self, assign: Assignment) -> None:
        op = assign.operator  # '=', '+=', '-=', '*=', '/='

        if isinstance(assign.target, Identifier):
            name = assign.target.name
            local_slot = self.current.resolve_local(name)
            upval_idx = -1
            if local_slot == -1:
                upval_idx = self.current.resolve_upvalue(name)

            if op == "=":
                self._compile_expression(assign.value)
            else:
                # Compound assignment: load target first
                if local_slot != -1:
                    self.current.emit(OpCode.LOAD_LOCAL, local_slot, span=assign.target.span)
                elif upval_idx != -1:
                    self.current.emit(OpCode.LOAD_UPVALUE, upval_idx, span=assign.target.span)
                else:
                    self.current.emit(OpCode.LOAD_GLOBAL, name, span=assign.target.span)

                self._compile_expression(assign.value)

                if op == "+=":
                    self.current.emit(OpCode.ADD, span=assign.span)
                elif op == "-=":
                    self.current.emit(OpCode.SUBTRACT, span=assign.span)
                elif op == "*=":
                    self.current.emit(OpCode.MULTIPLY, span=assign.span)
                elif op == "/=":
                    self.current.emit(OpCode.DIVIDE, span=assign.span)

            # Store back
            if local_slot != -1:
                self.current.emit(OpCode.STORE_LOCAL, local_slot, span=assign.span)
            elif upval_idx != -1:
                self.current.emit(OpCode.STORE_UPVALUE, upval_idx, span=assign.span)
            else:
                self.current.emit(OpCode.STORE_GLOBAL, name, span=assign.span)

        elif isinstance(assign.target, IndexExpr):
            # Target array/map indexing: target[index] = value
            self._compile_expression(assign.target.target)
            self._compile_expression(assign.target.index)

            if op == "=":
                self._compile_expression(assign.value)
            else:
                # Compound index assign: arr[idx] += val
                # Duplicate target & index: we need target[index]
                self._compile_expression(assign.target.target)
                self._compile_expression(assign.target.index)
                self.current.emit(OpCode.INDEX, span=assign.target.span)
                self._compile_expression(assign.value)
                if op == "+=":
                    self.current.emit(OpCode.ADD, span=assign.span)
                elif op == "-=":
                    self.current.emit(OpCode.SUBTRACT, span=assign.span)
                elif op == "*=":
                    self.current.emit(OpCode.MULTIPLY, span=assign.span)
                elif op == "/=":
                    self.current.emit(OpCode.DIVIDE, span=assign.span)

            self.current.emit(OpCode.SET_INDEX, span=assign.span)

    def _compile_function_decl(self, fn: FunctionDecl, is_top_level: bool = False) -> None:
        fn_compiler = FunctionCompiler(fn.name, enclosing=self.current, filename=self.filename, source_code=self.source_code)
        fn_compiler.chunk.param_names = [p.name for p in fn.params]

        # Function compiler scope
        fn_compiler.enter_scope()
        # Add parameters as locals
        for p in fn.params:
            fn_compiler.add_local(p.name)

        old_compiler = self.current
        self.current = fn_compiler

        # Compile body
        for stmt in fn.body.statements:
            self._compile_statement(stmt)

        # Implicit return NULL if execution reaches end of function
        self.current.emit(OpCode.NULL, span=fn.span)
        self.current.emit(OpCode.RETURN, span=fn.span)

        self.current.exit_scope()
        compiled_chunk = self.current.chunk
        self.current = old_compiler

        # Add function chunk as constant in enclosing compiler
        const_idx = self.current.chunk.add_constant(compiled_chunk)
        self.current.emit(OpCode.MAKE_CLOSURE, const_idx, span=fn.span)

        if self.current.scope_depth > 0 and not is_top_level:
            slot = self.current.add_local(fn.name)
            self.current.emit(OpCode.STORE_LOCAL, slot, span=fn.span)
        else:
            self.current.emit(OpCode.STORE_GLOBAL, fn.name, span=fn.span)

    def _compile_if(self, stmt: IfStatement) -> None:
        # Compile condition
        self._compile_expression(stmt.condition)
        else_jump = self.current.emit_jump(OpCode.JUMP_IF_FALSE, span=stmt.span)

        # Then branch
        self._compile_block(stmt.then_block)
        exit_jumps = [self.current.emit_jump(OpCode.JUMP, span=stmt.span)]

        self.current.patch_jump(else_jump)

        # Else-if branches
        for cond, blk in stmt.else_if_branches:
            self._compile_expression(cond)
            next_else_jump = self.current.emit_jump(OpCode.JUMP_IF_FALSE, span=stmt.span)
            self._compile_block(blk)
            exit_jumps.append(self.current.emit_jump(OpCode.JUMP, span=stmt.span))
            self.current.patch_jump(next_else_jump)

        # Else branch
        if stmt.else_block:
            self._compile_block(stmt.else_block)

        for j in exit_jumps:
            self.current.patch_jump(j)

    def _compile_while(self, stmt: WhileStatement) -> None:
        loop_start = len(self.current.chunk.instructions)
        self._compile_expression(stmt.condition)
        exit_jump = self.current.emit_jump(OpCode.JUMP_IF_FALSE, span=stmt.span)

        loop_info = LoopInfo(start_offset=loop_start, continue_offset=loop_start)
        self.current.loop_stack.append(loop_info)

        self._compile_block(stmt.body)

        # Jump back to condition
        self.current.emit(OpCode.JUMP, loop_start, span=stmt.span)
        self.current.patch_jump(exit_jump)

        # Patch break jumps
        for bj in loop_info.break_jumps:
            self.current.patch_jump(bj)

        self.current.loop_stack.pop()

    def _compile_for_each(self, stmt: ForEachStatement) -> None:
        """
        Compile for-each loop into bytecode:
        Hidden locals:
          __iter  (slot i)
          __idx   (slot i+1)
          __len   (slot i+2)
          __is_map(slot i+3)
        """
        self.current.enter_scope()

        # Evaluate iterable and normalize collection to iterable items
        self._compile_expression(stmt.iterable)
        self.current.emit(OpCode.CALL_BUILTIN, ("__vakya_iter", 1), span=stmt.span)
        iter_slot = self.current.add_local(f"__iter_{stmt.variable}")
        self.current.emit(OpCode.STORE_LOCAL, iter_slot, span=stmt.span)

        # Initialize index = 0
        self.current.emit_constant(0, span=stmt.span)
        idx_slot = self.current.add_local(f"__idx_{stmt.variable}")
        self.current.emit(OpCode.STORE_LOCAL, idx_slot, span=stmt.span)

        # Get length: lamba(__iter)
        self.current.emit(OpCode.LOAD_LOCAL, iter_slot, span=stmt.span)
        self.current.emit(OpCode.CALL_BUILTIN, ("lamba", 1), span=stmt.span)
        len_slot = self.current.add_local(f"__len_{stmt.variable}")
        self.current.emit(OpCode.STORE_LOCAL, len_slot, span=stmt.span)

        # User variable slot
        var_slot = self.current.add_local(stmt.variable)

        loop_start = len(self.current.chunk.instructions)
        # Condition: __idx < __len
        self.current.emit(OpCode.LOAD_LOCAL, idx_slot, span=stmt.span)
        self.current.emit(OpCode.LOAD_LOCAL, len_slot, span=stmt.span)
        self.current.emit(OpCode.LESS, span=stmt.span)
        exit_jump = self.current.emit_jump(OpCode.JUMP_IF_FALSE, span=stmt.span)

        # Fetch element: __iter[__idx] (for map, prakaar check or map iterator)
        # Builtin helper or index:
        self.current.emit(OpCode.LOAD_LOCAL, iter_slot, span=stmt.span)
        self.current.emit(OpCode.LOAD_LOCAL, idx_slot, span=stmt.span)
        self.current.emit(OpCode.INDEX, span=stmt.span)
        self.current.emit(OpCode.STORE_LOCAL, var_slot, span=stmt.span)

        continue_target = len(self.current.chunk.instructions)
        loop_info = LoopInfo(start_offset=loop_start, continue_offset=continue_target)
        self.current.loop_stack.append(loop_info)

        # Compile body
        for s in stmt.body.statements:
            self._compile_statement(s)

        # Increment index: __idx += 1
        incr_target = len(self.current.chunk.instructions)
        loop_info.continue_offset = incr_target
        self.current.emit(OpCode.LOAD_LOCAL, idx_slot, span=stmt.span)
        self.current.emit_constant(1, span=stmt.span)
        self.current.emit(OpCode.ADD, span=stmt.span)
        self.current.emit(OpCode.STORE_LOCAL, idx_slot, span=stmt.span)

        # Loop back
        self.current.emit(OpCode.JUMP, loop_start, span=stmt.span)
        self.current.patch_jump(exit_jump)

        for bj in loop_info.break_jumps:
            self.current.patch_jump(bj)

        self.current.loop_stack.pop()
        self.current.exit_scope(span=stmt.span)

    def _compile_break(self, stmt: BreakStatement) -> None:
        if not self.current.loop_stack:
            return
        jump = self.current.emit_jump(OpCode.JUMP, span=stmt.span)
        self.current.loop_stack[-1].break_jumps.append(jump)

    def _compile_continue(self, stmt: ContinueStatement) -> None:
        if not self.current.loop_stack:
            return
        target = self.current.loop_stack[-1].continue_offset
        self.current.emit(OpCode.JUMP, target, span=stmt.span)

    def _compile_return(self, stmt: ReturnStatement) -> None:
        if stmt.value is not None:
            self._compile_expression(stmt.value)
        else:
            self.current.emit(OpCode.NULL, span=stmt.span)
        self.current.emit(OpCode.RETURN, span=stmt.span)

    def _compile_block(self, block: Block) -> None:
        self.current.enter_scope()
        for s in block.statements:
            self._compile_statement(s)
        self.current.exit_scope(span=block.span)

    # Expression Compilers
    def _compile_expression(self, expr: Expression) -> None:
        if isinstance(expr, Literal):
            self._compile_literal(expr)
        elif isinstance(expr, Identifier):
            self._compile_identifier(expr)
        elif isinstance(expr, BinaryExpr):
            self._compile_binary(expr)
        elif isinstance(expr, UnaryExpr):
            self._compile_unary(expr)
        elif isinstance(expr, ListLiteral):
            self._compile_list(expr)
        elif isinstance(expr, MapLiteral):
            self._compile_map(expr)
        elif isinstance(expr, IndexExpr):
            self._compile_index(expr)
        elif isinstance(expr, MemberExpr):
            self._compile_member(expr)
        elif isinstance(expr, CallExpr):
            self._compile_call(expr)

    def _compile_literal(self, lit: Literal) -> None:
        if lit.literal_type == "sankhya" or lit.literal_type == "dashamika" or lit.literal_type == "shabda":
            self.current.emit_constant(lit.value, span=lit.span)
        elif lit.literal_type == "boolean":
            if lit.value is True:
                self.current.emit(OpCode.TRUE, span=lit.span)
            else:
                self.current.emit(OpCode.FALSE, span=lit.span)
        elif lit.literal_type == "shunya":
            self.current.emit(OpCode.NULL, span=lit.span)

    def _compile_identifier(self, ident: Identifier) -> None:
        name = ident.name
        local_slot = self.current.resolve_local(name)
        if local_slot != -1:
            self.current.emit(OpCode.LOAD_LOCAL, local_slot, span=ident.span)
            return

        upval_idx = self.current.resolve_upvalue(name)
        if upval_idx != -1:
            self.current.emit(OpCode.LOAD_UPVALUE, upval_idx, span=ident.span)
            return

        self.current.emit(OpCode.LOAD_GLOBAL, name, span=ident.span)

    def _try_fold_binary(self, expr: BinaryExpr) -> Optional[Any]:
        if not (isinstance(expr.left, Literal) and isinstance(expr.right, Literal)):
            return None
        l = expr.left.value
        r = expr.right.value
        op = expr.operator
        try:
            if op == "+":
                if (type(l) is int and type(r) is int) or (isinstance(l, (int, float)) and isinstance(r, (int, float)) and type(l) is not bool and type(r) is not bool):
                    return l + r
                if isinstance(l, str) or isinstance(r, str):
                    return str(l) + str(r)
            elif op == "-":
                if (type(l) is int or type(l) is float) and (type(r) is int or type(r) is float) and type(l) is not bool and type(r) is not bool:
                    return l - r
            elif op == "*":
                if (type(l) is int or type(l) is float) and (type(r) is int or type(r) is float) and type(l) is not bool and type(r) is not bool:
                    return l * r
                if isinstance(l, str) and type(r) is int and type(r) is not bool:
                    return l * r
            elif op == "/" and r != 0:
                if type(l) is int and type(r) is int and type(l) is not bool and type(r) is not bool and l % r == 0:
                    return l // r
                if (type(l) is int or type(l) is float) and (type(r) is int or type(r) is float) and type(l) is not bool and type(r) is not bool:
                    return l / r
            elif op == "%" and r != 0:
                if (type(l) is int or type(l) is float) and (type(r) is int or type(r) is float) and type(l) is not bool and type(r) is not bool:
                    return l % r
            elif op == "**":
                if (type(l) is int or type(l) is float) and (type(r) is int or type(r) is float) and type(l) is not bool and type(r) is not bool:
                    res = l ** r
                    return int(res) if type(l) is int and type(r) is int and r >= 0 else res
            elif op == "==":
                if (type(l) is bool and type(r) is not bool) or (type(r) is bool and type(l) is not bool):
                    return False
                return l == r
            elif op == "!=":
                if (type(l) is bool and type(r) is not bool) or (type(r) is bool and type(l) is not bool):
                    return True
                return l != r
            elif op == "<" and (type(l) is int or type(l) is float) and (type(r) is int or type(r) is float) and type(l) is not bool and type(r) is not bool:
                return l < r
            elif op == "<=" and (type(l) is int or type(l) is float) and (type(r) is int or type(r) is float) and type(l) is not bool and type(r) is not bool:
                return l <= r
            elif op == ">" and (type(l) is int or type(l) is float) and (type(r) is int or type(r) is float) and type(l) is not bool and type(r) is not bool:
                return l > r
            elif op == ">=" and (type(l) is int or type(l) is float) and (type(r) is int or type(r) is float) and type(l) is not bool and type(r) is not bool:
                return l >= r
        except Exception:
            return None
        return None

    def _compile_binary(self, expr: BinaryExpr) -> None:
        if self.optimize:
            folded = self._try_fold_binary(expr)
            if folded is not None:
                if folded is True:
                    self.current.emit(OpCode.TRUE, span=expr.span)
                elif folded is False:
                    self.current.emit(OpCode.FALSE, span=expr.span)
                elif folded is None:
                    self.current.emit(OpCode.NULL, span=expr.span)
                else:
                    self.current.emit_constant(folded, span=expr.span)
                return

        op = expr.operator

        # Short-circuit logical operators
        if op == "va":
            self._compile_expression(expr.left)
            jump = self.current.emit_jump(OpCode.JUMP_IF_TRUE_OR_POP, span=expr.span)
            self._compile_expression(expr.right)
            self.current.patch_jump(jump)
            return

        if op == "evam":
            self._compile_expression(expr.left)
            jump = self.current.emit_jump(OpCode.JUMP_IF_FALSE_OR_POP, span=expr.span)
            self._compile_expression(expr.right)
            self.current.patch_jump(jump)
            return

        self._compile_expression(expr.left)
        self._compile_expression(expr.right)

        if op == "+":
            self.current.emit(OpCode.ADD, span=expr.span)
        elif op == "-":
            self.current.emit(OpCode.SUBTRACT, span=expr.span)
        elif op == "*":
            self.current.emit(OpCode.MULTIPLY, span=expr.span)
        elif op == "/":
            self.current.emit(OpCode.DIVIDE, span=expr.span)
        elif op == "%":
            self.current.emit(OpCode.MODULO, span=expr.span)
        elif op == "**":
            self.current.emit(OpCode.POWER, span=expr.span)
        elif op == "==":
            self.current.emit(OpCode.EQUAL, span=expr.span)
        elif op == "!=":
            self.current.emit(OpCode.NOT_EQUAL, span=expr.span)
        elif op == "<":
            self.current.emit(OpCode.LESS, span=expr.span)
        elif op == "<=":
            self.current.emit(OpCode.LESS_EQUAL, span=expr.span)
        elif op == ">":
            self.current.emit(OpCode.GREATER, span=expr.span)
        elif op == ">=":
            self.current.emit(OpCode.GREATER_EQUAL, span=expr.span)

    def _compile_unary(self, expr: UnaryExpr) -> None:
        if self.optimize and isinstance(expr.operand, Literal):
            val = expr.operand.value
            if expr.operator == "-" and (type(val) is int or type(val) is float) and type(val) is not bool:
                self.current.emit_constant(-val, span=expr.span)
                return
            elif expr.operator == "na":
                if val is True:
                    self.current.emit(OpCode.FALSE, span=expr.span)
                    return
                elif val is False:
                    self.current.emit(OpCode.TRUE, span=expr.span)
                    return

        self._compile_expression(expr.operand)
        if expr.operator == "-":
            self.current.emit(OpCode.NEGATE, span=expr.span)
        elif expr.operator == "na":
            self.current.emit(OpCode.NOT, span=expr.span)
        elif expr.operator == "+":
            pass  # unary plus is no-op

    def _compile_list(self, expr: ListLiteral) -> None:
        for el in expr.elements:
            self._compile_expression(el)
        self.current.emit(OpCode.BUILD_LIST, len(expr.elements), span=expr.span)

    def _compile_map(self, expr: MapLiteral) -> None:
        for k, v in expr.pairs:
            self._compile_expression(k)
            self._compile_expression(v)
        self.current.emit(OpCode.BUILD_MAP, len(expr.pairs), span=expr.span)

    def _compile_index(self, expr: IndexExpr) -> None:
        self._compile_expression(expr.target)
        self._compile_expression(expr.index)
        self.current.emit(OpCode.INDEX, span=expr.span)

    def _compile_member(self, expr: MemberExpr) -> None:
        self._compile_expression(expr.target)
        self.current.emit(OpCode.GET_MEMBER, expr.member, span=expr.span)

    def _compile_call(self, call: CallExpr) -> None:
        # Check direct builtin call optimization
        if isinstance(call.callee, Identifier) and call.callee.name in self.builtin_names:
            for arg in call.arguments:
                self._compile_expression(arg)
            self.current.emit(OpCode.CALL_BUILTIN, (call.callee.name, len(call.arguments)), span=call.span)
            return

        # General function call
        self._compile_expression(call.callee)
        for arg in call.arguments:
            self._compile_expression(arg)
        self.current.emit(OpCode.CALL, len(call.arguments), span=call.span)
