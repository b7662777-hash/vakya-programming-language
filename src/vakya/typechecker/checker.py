"""Static type checker and semantic analyzer for Vākya."""

from typing import Dict, List, Optional, Tuple
from ..ast.nodes import (
    Span,
    ASTNode,
    Program,
    Statement,
    Expression,
    Block,
    VarDecl,
    Assignment,
    IfStatement,
    WhileStatement,
    ForEachStatement,
    BreakStatement,
    ContinueStatement,
    ReturnStatement,
    FunctionDecl,
    Param,
    ExpressionStatement,
    BinaryExpr,
    UnaryExpr,
    Literal,
    Identifier,
    ListLiteral,
    MapLiteral,
    IndexExpr,
    MemberExpr,
    CallExpr,
)
from ..errors import (
    TypeError,
    NameError,
    ConstantError,
    ArgumentError,
    ParseError,
    E101_UNDEFINED_VARIABLE,
    E102_UNDEFINED_FUNCTION,
    E103_CONSTANT_REASSIGNMENT,
    E104_DUPLICATE_DECLARATION,
    E105_INVALID_ASSIGNMENT_TARGET,
    E206_INVALID_BREAK_CONTINUE,
    E207_INVALID_RETURN,
    E401_TYPE_MISMATCH,
    E402_ARGUMENT_TYPE_MISMATCH,
    E403_RETURN_TYPE_MISMATCH,
    E404_OPERATOR_TYPE_MISMATCH,
    E405_UNARY_TYPE_MISMATCH,
    E406_ARGUMENT_COUNT_MISMATCH,
    E407_NOT_INDEXABLE,
)
from .types import (
    VakyaType,
    FunctionType,
    TYPE_SANKHYA,
    TYPE_DASHAMIKA,
    TYPE_SHABDA,
    TYPE_BOOLEAN,
    TYPE_SUCHI,
    TYPE_NAKSHA,
    TYPE_SHUNYA,
    TYPE_UNKNOWN,
    lookup_type,
)


class Symbol:
    def __init__(self, name: str, var_type: VakyaType, is_constant: bool, span: Span):
        self.name = name
        self.type = var_type
        self.is_constant = is_constant
        self.span = span


class TypeEnvironment:
    """Scoped symbol table for type checking."""

    def __init__(self, parent: Optional["TypeEnvironment"] = None):
        self.parent = parent
        self.symbols: Dict[str, Symbol] = {}

    def define(self, name: str, var_type: VakyaType, is_constant: bool, span: Span) -> None:
        self.symbols[name] = Symbol(name, var_type, is_constant, span)

    def lookup(self, name: str) -> Optional[Symbol]:
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.lookup(name)
        return None

    def lookup_current(self, name: str) -> Optional[Symbol]:
        return self.symbols.get(name)


class TypeChecker:
    """Performs static type checking and semantic validation on a Vākya AST."""

    def __init__(self, source_code: str = "", filename: str = "<anonymous>"):
        self.source_code = source_code
        self.filename = filename
        self.current_env = TypeEnvironment()
        self.loop_depth = 0
        self.current_function_return_type: Optional[VakyaType] = None
        self._init_builtins()

    def _init_builtins(self) -> None:
        # Define built-in functions
        dummy_span = Span(1, 1, 1, 1, self.filename)
        # vada: accepts any args, returns shunya
        self.current_env.define("vada", FunctionType([TYPE_UNKNOWN], TYPE_SHUNYA), True, dummy_span)
        # puchha: accepts optional prompt, returns shabda
        self.current_env.define("puchha", FunctionType([TYPE_SHABDA], TYPE_SHABDA), True, dummy_span)
        # lamba: length of sequence/map, returns sankhya
        self.current_env.define("lamba", FunctionType([TYPE_UNKNOWN], TYPE_SANKHYA), True, dummy_span)
        # prakaar: returns type name as shabda
        self.current_env.define("prakaar", FunctionType([TYPE_UNKNOWN], TYPE_SHABDA), True, dummy_span)
        # suchi_jodo: appends to list
        self.current_env.define("suchi_jodo", FunctionType([TYPE_SUCHI, TYPE_UNKNOWN], TYPE_SHUNYA), True, dummy_span)
        # suchi_hatao: removes index from list
        self.current_env.define("suchi_hatao", FunctionType([TYPE_SUCHI, TYPE_SANKHYA], TYPE_UNKNOWN), True, dummy_span)
        # shabda_bada: uppercase
        self.current_env.define("shabda_bada", FunctionType([TYPE_SHABDA], TYPE_SHABDA), True, dummy_span)
        # shabda_chhota: lowercase
        self.current_env.define("shabda_chhota", FunctionType([TYPE_SHABDA], TYPE_SHABDA), True, dummy_span)
        # shabda_trim: trim
        self.current_env.define("shabda_trim", FunctionType([TYPE_SHABDA], TYPE_SHABDA), True, dummy_span)

    def check(self, program: Program) -> None:
        # Pass 1: Register all top-level function signatures for forward references / mutual recursion
        for stmt in program.statements:
            if isinstance(stmt, FunctionDecl):
                self._register_function_signature(stmt)

        # Pass 2: Typecheck statements and bodies
        for stmt in program.statements:
            self._check_statement(stmt)

    def _register_function_signature(self, fn: FunctionDecl) -> None:
        param_types: List[VakyaType] = []
        for p in fn.params:
            p_type = lookup_type(p.type_annotation) if p.type_annotation else TYPE_UNKNOWN
            param_types.append(p_type)

        ret_type = lookup_type(fn.return_type) if fn.return_type else TYPE_UNKNOWN
        fn_type = FunctionType(param_types, ret_type)
        self.current_env.define(fn.name, fn_type, True, fn.span)

    def _check_statement(self, stmt: Statement) -> None:
        if isinstance(stmt, VarDecl):
            self._check_var_decl(stmt)
        elif isinstance(stmt, FunctionDecl):
            self._check_function_decl(stmt)
        elif isinstance(stmt, Assignment):
            self._check_assignment(stmt)
        elif isinstance(stmt, IfStatement):
            self._check_if(stmt)
        elif isinstance(stmt, WhileStatement):
            self._check_while(stmt)
        elif isinstance(stmt, ForEachStatement):
            self._check_for_each(stmt)
        elif isinstance(stmt, BreakStatement):
            if self.loop_depth == 0:
                raise ParseError.from_info(
                    E206_INVALID_BREAK_CONTINUE,
                    "'virama' (break) can only be used inside a loop",
                    filename=self.filename,
                    line=stmt.span.line,
                    column=stmt.span.column,
                    length=stmt.span.length,
                    source_code=self.source_code,
                )
        elif isinstance(stmt, ContinueStatement):
            if self.loop_depth == 0:
                raise ParseError.from_info(
                    E206_INVALID_BREAK_CONTINUE,
                    "'agaccha' (continue) can only be used inside a loop",
                    filename=self.filename,
                    line=stmt.span.line,
                    column=stmt.span.column,
                    length=stmt.span.length,
                    source_code=self.source_code,
                )
        elif isinstance(stmt, ReturnStatement):
            self._check_return(stmt)
        elif isinstance(stmt, Block):
            self._check_block(stmt)
        elif isinstance(stmt, ExpressionStatement):
            self._check_expression(stmt.expression)

    def _check_var_decl(self, decl: VarDecl) -> None:
        annotated_type = lookup_type(decl.type_annotation) if decl.type_annotation else None
        init_type = TYPE_SHUNYA

        if decl.initializer is not None:
            init_type = self._check_expression(decl.initializer)

        final_type = annotated_type if annotated_type is not None else init_type

        if annotated_type is not None and decl.initializer is not None:
            if not init_type.is_assignable_to(annotated_type):
                raise TypeError.from_info(
                    E401_TYPE_MISMATCH,
                    f"Cannot assign value of type '{init_type}' to variable '{decl.name}' of type '{annotated_type}'",
                    filename=self.filename,
                    line=decl.initializer.span.line,
                    column=decl.initializer.span.column,
                    length=decl.initializer.span.length,
                    source_code=self.source_code,
                    help_text=f"Expected type '{annotated_type}', but found '{init_type}'.",
                )

        self.current_env.define(decl.name, final_type, decl.is_constant, decl.span)

    def _check_assignment(self, assign: Assignment) -> None:
        val_type = self._check_expression(assign.value)

        if isinstance(assign.target, Identifier):
            sym = self.current_env.lookup(assign.target.name)
            if sym is None:
                raise NameError.from_info(
                    E101_UNDEFINED_VARIABLE,
                    f"Undefined variable '{assign.target.name}'",
                    filename=self.filename,
                    line=assign.target.span.line,
                    column=assign.target.span.column,
                    length=assign.target.span.length,
                    source_code=self.source_code,
                    help_text=f"Declare variable '{assign.target.name}' using 'chara' before assigning to it.",
                )

            if sym.is_constant:
                raise ConstantError.from_info(
                    E103_CONSTANT_REASSIGNMENT,
                    f"Cannot reassign constant '{assign.target.name}' declared with 'dhruva'",
                    filename=self.filename,
                    line=assign.span.line,
                    column=assign.span.column,
                    length=assign.span.length,
                    source_code=self.source_code,
                    help_text="Variables declared with 'dhruva' cannot be modified. Use 'chara' for mutable variables.",
                )

            if assign.operator == "=":
                if not val_type.is_assignable_to(sym.type):
                    raise TypeError.from_info(
                        E401_TYPE_MISMATCH,
                        f"Cannot assign {val_type} to variable {assign.target.name} of type {sym.type}",
                        filename=self.filename,
                        line=assign.value.span.line,
                        column=assign.value.span.column,
                        length=assign.value.span.length,
                        source_code=self.source_code,
                        help_text=f"Expected '{sym.type}', but received '{val_type}'.",
                    )
            else:
                # Compound assignment: +=, -=, *=, /=
                if assign.operator == "+=":
                    # Allow numeric addition or string concat
                    if sym.type in (TYPE_SANKHYA, TYPE_DASHAMIKA):
                        if val_type not in (TYPE_SANKHYA, TYPE_DASHAMIKA, TYPE_UNKNOWN):
                            raise TypeError.from_info(
                                E404_OPERATOR_TYPE_MISMATCH,
                                f"Cannot use '+=' with '{val_type}' on numeric variable '{assign.target.name}'",
                                filename=self.filename,
                                line=assign.value.span.line,
                                column=assign.value.span.column,
                                length=assign.value.span.length,
                                source_code=self.source_code,
                            )
                    elif sym.type == TYPE_SHABDA:
                        # Any value can be appended as string
                        pass
                else:
                    if sym.type not in (TYPE_SANKHYA, TYPE_DASHAMIKA, TYPE_UNKNOWN) or val_type not in (TYPE_SANKHYA, TYPE_DASHAMIKA, TYPE_UNKNOWN):
                        raise TypeError.from_info(
                            E404_OPERATOR_TYPE_MISMATCH,
                            f"Compound operator '{assign.operator}' requires numeric types",
                            filename=self.filename,
                            line=assign.span.line,
                            column=assign.span.column,
                            length=assign.span.length,
                            source_code=self.source_code,
                        )

        elif isinstance(assign.target, IndexExpr):
            tgt_type = self._check_expression(assign.target.target)
            idx_type = self._check_expression(assign.target.index)
            if tgt_type not in (TYPE_SUCHI, TYPE_NAKSHA, TYPE_UNKNOWN):
                raise TypeError.from_info(
                    E407_NOT_INDEXABLE,
                    f"Cannot assign by index to non-collection type '{tgt_type}'",
                    filename=self.filename,
                    line=assign.target.span.line,
                    column=assign.target.span.column,
                    length=assign.target.span.length,
                    source_code=self.source_code,
                )
            if tgt_type == TYPE_SUCHI and idx_type not in (TYPE_SANKHYA, TYPE_UNKNOWN):
                raise TypeError.from_info(
                    E401_TYPE_MISMATCH,
                    f"List index must be 'sankhya' (integer), found '{idx_type}'",
                    filename=self.filename,
                    line=assign.target.index.span.line,
                    column=assign.target.index.span.column,
                    length=assign.target.index.span.length,
                    source_code=self.source_code,
                )
        elif isinstance(assign.target, MemberExpr):
            self._check_expression(assign.target.target)

    def _check_function_decl(self, fn: FunctionDecl) -> None:
        param_types: List[VakyaType] = []
        for p in fn.params:
            p_type = lookup_type(p.type_annotation) if p.type_annotation else TYPE_UNKNOWN
            param_types.append(p_type)

        ret_type = lookup_type(fn.return_type) if fn.return_type else TYPE_UNKNOWN
        fn_type = FunctionType(param_types, ret_type)

        # Define function in current scope
        self.current_env.define(fn.name, fn_type, True, fn.span)

        # Enter function scope
        fn_env = TypeEnvironment(self.current_env)
        for p, pt in zip(fn.params, param_types):
            fn_env.define(p.name, pt, False, p.span)

        old_env = self.current_env
        old_ret_type = self.current_function_return_type
        self.current_env = fn_env
        self.current_function_return_type = ret_type

        try:
            for stmt in fn.body.statements:
                self._check_statement(stmt)
        finally:
            self.current_env = old_env
            self.current_function_return_type = old_ret_type

    def _check_if(self, stmt: IfStatement) -> None:
        self._check_expression(stmt.condition)
        self._check_block(stmt.then_block)
        for cond, blk in stmt.else_if_branches:
            self._check_expression(cond)
            self._check_block(blk)
        if stmt.else_block:
            self._check_block(stmt.else_block)

    def _check_while(self, stmt: WhileStatement) -> None:
        self._check_expression(stmt.condition)
        self.loop_depth += 1
        try:
            self._check_block(stmt.body)
        finally:
            self.loop_depth -= 1

    def _check_for_each(self, stmt: ForEachStatement) -> None:
        iter_type = self._check_expression(stmt.iterable)
        if iter_type not in (TYPE_SUCHI, TYPE_NAKSHA, TYPE_SHABDA, TYPE_UNKNOWN):
            raise TypeError.from_info(
                E404_OPERATOR_TYPE_MISMATCH,
                f"Cannot iterate over type '{iter_type}' with 'pratyekam'",
                filename=self.filename,
                line=stmt.iterable.span.line,
                column=stmt.iterable.span.column,
                length=stmt.iterable.span.length,
                source_code=self.source_code,
                help_text="pratyekam can only iterate over lists (suchi), maps (naksha), or strings (shabda).",
            )

        self.loop_depth += 1
        block_env = TypeEnvironment(self.current_env)
        block_env.define(stmt.variable, TYPE_UNKNOWN, False, stmt.span)
        old_env = self.current_env
        self.current_env = block_env
        try:
            for s in stmt.body.statements:
                self._check_statement(s)
        finally:
            self.current_env = old_env
            self.loop_depth -= 1

    def _check_block(self, block: Block) -> None:
        block_env = TypeEnvironment(self.current_env)
        old_env = self.current_env
        self.current_env = block_env
        try:
            for s in block.statements:
                self._check_statement(s)
        finally:
            self.current_env = old_env

    def _check_return(self, stmt: ReturnStatement) -> None:
        if self.current_function_return_type is None:
            raise ParseError.from_info(
                E207_INVALID_RETURN,
                "'pratyavartaya' (return) can only be used inside a function",
                filename=self.filename,
                line=stmt.span.line,
                column=stmt.span.column,
                length=stmt.span.length,
                source_code=self.source_code,
            )

        val_type = TYPE_SHUNYA
        if stmt.value is not None:
            val_type = self._check_expression(stmt.value)

        expected = self.current_function_return_type
        if expected != TYPE_UNKNOWN and not val_type.is_assignable_to(expected):
            raise TypeError.from_info(
                E403_RETURN_TYPE_MISMATCH,
                f"Function return type mismatch: expected '{expected}', returned '{val_type}'",
                filename=self.filename,
                line=stmt.span.line,
                column=stmt.span.column,
                length=stmt.span.length,
                source_code=self.source_code,
            )

    # Expression checking
    def _check_expression(self, expr: Expression) -> VakyaType:
        if isinstance(expr, Literal):
            return lookup_type(expr.literal_type)

        if isinstance(expr, Identifier):
            sym = self.current_env.lookup(expr.name)
            if sym is None:
                raise NameError.from_info(
                    E101_UNDEFINED_VARIABLE,
                    f"Undefined variable '{expr.name}'",
                    filename=self.filename,
                    line=expr.span.line,
                    column=expr.span.column,
                    length=expr.span.length,
                    source_code=self.source_code,
                    help_text=f"Declare '{expr.name}' using 'chara' or 'dhruva' before using it.",
                )
            return sym.type

        if isinstance(expr, BinaryExpr):
            left_type = self._check_expression(expr.left)
            right_type = self._check_expression(expr.right)
            op = expr.operator

            # Arithmetic
            if op in ("+", "-", "*", "/", "%", "**"):
                if op == "+":
                    if left_type == TYPE_SHABDA or right_type == TYPE_SHABDA:
                        return TYPE_SHABDA
                    if left_type in (TYPE_SANKHYA, TYPE_DASHAMIKA, TYPE_UNKNOWN) and right_type in (TYPE_SANKHYA, TYPE_DASHAMIKA, TYPE_UNKNOWN):
                        if left_type == TYPE_DASHAMIKA or right_type == TYPE_DASHAMIKA:
                            return TYPE_DASHAMIKA
                        return TYPE_SANKHYA
                    raise TypeError.from_info(
                        E404_OPERATOR_TYPE_MISMATCH,
                        f"Operator '+' cannot be applied to types '{left_type}' and '{right_type}'",
                        filename=self.filename,
                        line=expr.span.line,
                        column=expr.span.column,
                        length=expr.span.length,
                        source_code=self.source_code,
                    )
                else:
                    if op == "*" and ((left_type == TYPE_SHABDA and right_type in (TYPE_SANKHYA, TYPE_UNKNOWN)) or (right_type == TYPE_SHABDA and left_type in (TYPE_SANKHYA, TYPE_UNKNOWN))):
                        return TYPE_SHABDA
                    if left_type in (TYPE_SANKHYA, TYPE_DASHAMIKA, TYPE_UNKNOWN) and right_type in (TYPE_SANKHYA, TYPE_DASHAMIKA, TYPE_UNKNOWN):
                        if op == "/" or left_type == TYPE_DASHAMIKA or right_type == TYPE_DASHAMIKA:
                            return TYPE_DASHAMIKA
                        return TYPE_SANKHYA
                    raise TypeError.from_info(
                        E404_OPERATOR_TYPE_MISMATCH,
                        f"Operator '{op}' cannot be applied to types '{left_type}' and '{right_type}'",
                        filename=self.filename,
                        line=expr.span.line,
                        column=expr.span.column,
                        length=expr.span.length,
                        source_code=self.source_code,
                    )

            # Comparisons
            if op in ("<", "<=", ">", ">="):
                if left_type in (TYPE_SANKHYA, TYPE_DASHAMIKA, TYPE_UNKNOWN) and right_type in (TYPE_SANKHYA, TYPE_DASHAMIKA, TYPE_UNKNOWN):
                    return TYPE_BOOLEAN
                if left_type in (TYPE_SHABDA, TYPE_UNKNOWN) and right_type in (TYPE_SHABDA, TYPE_UNKNOWN):
                    return TYPE_BOOLEAN
                raise TypeError.from_info(
                    E404_OPERATOR_TYPE_MISMATCH,
                    f"Relational operator '{op}' cannot compare types '{left_type}' and '{right_type}'",
                    filename=self.filename,
                    line=expr.span.line,
                    column=expr.span.column,
                    length=expr.span.length,
                    source_code=self.source_code,
                )

            # Equality
            if op in ("==", "!="):
                return TYPE_BOOLEAN

            # Logical
            if op in ("evam", "va"):
                return TYPE_BOOLEAN

            return TYPE_UNKNOWN

        if isinstance(expr, UnaryExpr):
            op_type = self._check_expression(expr.operand)
            if expr.operator in ("-", "+"):
                if op_type in (TYPE_SANKHYA, TYPE_DASHAMIKA, TYPE_UNKNOWN):
                    return op_type
                raise TypeError.from_info(
                    E405_UNARY_TYPE_MISMATCH,
                    f"Unary operator '{expr.operator}' requires numeric type, found '{op_type}'",
                    filename=self.filename,
                    line=expr.span.line,
                    column=expr.span.column,
                    length=expr.span.length,
                    source_code=self.source_code,
                )
            elif expr.operator == "na":
                return TYPE_BOOLEAN
            return TYPE_UNKNOWN

        if isinstance(expr, ListLiteral):
            for el in expr.elements:
                self._check_expression(el)
            return TYPE_SUCHI

        if isinstance(expr, MapLiteral):
            for k, v in expr.pairs:
                self._check_expression(k)
                self._check_expression(v)
            return TYPE_NAKSHA

        if isinstance(expr, IndexExpr):
            tgt_t = self._check_expression(expr.target)
            idx_t = self._check_expression(expr.index)
            if tgt_t not in (TYPE_SUCHI, TYPE_NAKSHA, TYPE_SHABDA, TYPE_UNKNOWN):
                raise TypeError.from_info(
                    E407_NOT_INDEXABLE,
                    f"Type '{tgt_t}' is not indexable",
                    filename=self.filename,
                    line=expr.target.span.line,
                    column=expr.target.span.column,
                    length=expr.target.span.length,
                    source_code=self.source_code,
                )
            if tgt_t == TYPE_SHABDA:
                return TYPE_SHABDA
            return TYPE_UNKNOWN

        if isinstance(expr, MemberExpr):
            tgt_t = self._check_expression(expr.target)
            if expr.member == "length":
                return TYPE_SANKHYA
            return TYPE_UNKNOWN

        if isinstance(expr, CallExpr):
            return self._check_call(expr)

        return TYPE_UNKNOWN

    def _check_call(self, call: CallExpr) -> VakyaType:
        if isinstance(call.callee, Identifier):
            sym = self.current_env.lookup(call.callee.name)
            if sym is None:
                raise NameError.from_info(
                    E102_UNDEFINED_FUNCTION,
                    f"Undefined function '{call.callee.name}'",
                    filename=self.filename,
                    line=call.callee.span.line,
                    column=call.callee.span.column,
                    length=call.callee.span.length,
                    source_code=self.source_code,
                    help_text=f"Define the function '{call.callee.name}' using 'karya' before calling it.",
                )

            # Special case built-in vada (allows variable arguments)
            if call.callee.name == "vada":
                for arg in call.arguments:
                    self._check_expression(arg)
                return TYPE_SHUNYA

            if isinstance(sym.type, FunctionType):
                fn_type = sym.type
                # Check argument count
                if len(call.arguments) != len(fn_type.param_types):
                    raise ArgumentError.from_info(
                        E406_ARGUMENT_COUNT_MISMATCH,
                        f"Function '{call.callee.name}' expects {len(fn_type.param_types)} argument(s), but received {len(call.arguments)}",
                        filename=self.filename,
                        line=call.span.line,
                        column=call.span.column,
                        length=call.span.length,
                        source_code=self.source_code,
                    )

                for i, (arg, p_type) in enumerate(zip(call.arguments, fn_type.param_types)):
                    arg_type = self._check_expression(arg)
                    if p_type != TYPE_UNKNOWN and not arg_type.is_assignable_to(p_type):
                        raise TypeError.from_info(
                            E402_ARGUMENT_TYPE_MISMATCH,
                            f"Argument {i + 1} of '{call.callee.name}' expects type '{p_type}', but received '{arg_type}'",
                            filename=self.filename,
                            line=arg.span.line,
                            column=arg.span.column,
                            length=arg.span.length,
                            source_code=self.source_code,
                        )
                return fn_type.return_type
            else:
                for arg in call.arguments:
                    self._check_expression(arg)
                return TYPE_UNKNOWN
        else:
            self._check_expression(call.callee)
            for arg in call.arguments:
                self._check_expression(arg)
            return TYPE_UNKNOWN
