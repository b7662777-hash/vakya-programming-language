"""Tree-walking interpreter for Vākya AST."""

import os
import sys
from typing import Any, List, Optional, TextIO
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
    ImportStatement,
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
    RuntimeError,
    IndexError,
    ArgumentError,
    ConstantError,
    NameError,
    E301_DIVISION_BY_ZERO,
    E302_INDEX_OUT_OF_BOUNDS,
    E303_KEY_NOT_FOUND,
    E304_RECURSION_LIMIT,
    E305_NOT_CALLABLE,
    E306_RUNTIME_TYPE_ERROR,
    E307_INVALID_PROPERTY,
    E406_ARGUMENT_COUNT_MISMATCH,
)
from ..modules.loader import ModuleLoader
from .values import (
    VakyaFunction,
    VakyaBuiltin,
    is_truthy,
    vakya_str,
    vakya_typeof,
)
from .environment import Environment
from .builtins import create_builtins


class ReturnSignal(Exception):
    """Internal control flow exception for function return."""

    def __init__(self, value: Any, span: Span):
        self.value = value
        self.span = span


class BreakSignal(Exception):
    """Internal control flow exception for loop break."""

    def __init__(self, span: Span):
        self.span = span


class ContinueSignal(Exception):
    """Internal control flow exception for loop continue."""

    def __init__(self, span: Span):
        self.span = span


class Interpreter:
    """Evaluates a Vākya AST with tree-walking execution."""

    def __init__(
        self,
        source_code: str = "",
        filename: str = "<anonymous>",
        stdout: TextIO = sys.stdout,
        stdin: TextIO = sys.stdin,
        max_call_depth: int = 150,
    ):
        self.source_code = source_code
        self.filename = filename
        self.stdout = stdout
        self.stdin = stdin
        self.max_call_depth = max_call_depth
        self.call_depth = 0

        # Global environment with standard library builtins
        self.global_env = Environment()
        self.current_env = self.global_env
        self.module_loader = ModuleLoader()
        self._load_builtins()

    def _load_builtins(self) -> None:
        builtins = create_builtins(stdout=self.stdout, stdin=self.stdin)
        for name, builtin in builtins.items():
            self.global_env.define(name, builtin, is_constant=True)

    def interpret(self, program: Program) -> Any:
        """Execute the entire program AST."""
        last_result: Any = None
        try:
            # Pass 1: Pre-register top-level function declarations for mutual recursion / forward calls
            for stmt in program.statements:
                if isinstance(stmt, FunctionDecl):
                    self._exec_function_decl(stmt)

            # Pass 2: Execute statements
            for stmt in program.statements:
                last_result = self._execute(stmt)
            return last_result
        except RecursionError:
            raise RuntimeError.from_info(
                E304_RECURSION_LIMIT,
                "Maximum call stack recursion limit reached",
                filename=self.filename,
                source_code=self.source_code,
                help_text="Check for unbounded recursion or missing base condition in your function.",
            )

    def _execute(self, stmt: Statement) -> Any:
        if isinstance(stmt, VarDecl):
            return self._exec_var_decl(stmt)
        elif isinstance(stmt, FunctionDecl):
            return self._exec_function_decl(stmt)
        elif isinstance(stmt, ImportStatement):
            return self._exec_import(stmt)
        elif isinstance(stmt, Assignment):
            return self._exec_assignment(stmt)
        elif isinstance(stmt, IfStatement):
            return self._exec_if(stmt)
        elif isinstance(stmt, WhileStatement):
            return self._exec_while(stmt)
        elif isinstance(stmt, ForEachStatement):
            return self._exec_for_each(stmt)
        elif isinstance(stmt, BreakStatement):
            raise BreakSignal(stmt.span)
        elif isinstance(stmt, ContinueStatement):
            raise ContinueSignal(stmt.span)
        elif isinstance(stmt, ReturnStatement):
            val = self._evaluate(stmt.value) if stmt.value is not None else None
            raise ReturnSignal(val, stmt.span)
        elif isinstance(stmt, Block):
            return self._exec_block(stmt, Environment(self.current_env))
        elif isinstance(stmt, ExpressionStatement):
            return self._evaluate(stmt.expression)
        return None

    def _exec_import(self, stmt: ImportStatement) -> Any:
        base_dir = os.path.dirname(self.filename) if self.filename and self.filename != "<anonymous>" else None
        symbols = self.module_loader.load_module(stmt.module_name, base_dir=base_dir)
        name = stmt.alias if stmt.alias else stmt.module_name
        self.current_env.define(name, symbols, is_constant=True)
        return symbols

    def _exec_var_decl(self, decl: VarDecl) -> Any:
        val = self._evaluate(decl.initializer) if decl.initializer is not None else None
        if decl.type_annotation == "dashamika" and isinstance(val, int) and not isinstance(val, bool):
            val = float(val)
        self.current_env.define(decl.name, val, is_constant=decl.is_constant)
        return val

    def _exec_function_decl(self, decl: FunctionDecl) -> Any:
        fn_obj = VakyaFunction(
            name=decl.name,
            params=decl.params,
            body=decl.body,
            closure=self.current_env,
            return_type=decl.return_type,
            span=decl.span,
        )
        self.current_env.define(decl.name, fn_obj, is_constant=True)
        return fn_obj

    def _exec_assignment(self, assign: Assignment) -> Any:
        val = self._evaluate(assign.value)

        if isinstance(assign.target, Identifier):
            name = assign.target.name
            if assign.operator == "=":
                final_val = val
            else:
                curr_val = self.current_env.get(name, span=assign.target.span, source_code=self.source_code, filename=self.filename)
                final_val = self._apply_compound_op(assign.operator, curr_val, val, assign.span)

            self.current_env.assign(name, final_val, span=assign.span, source_code=self.source_code, filename=self.filename)
            return final_val

        elif isinstance(assign.target, IndexExpr):
            target_obj = self._evaluate(assign.target.target)
            index_val = self._evaluate(assign.target.index)

            if isinstance(target_obj, list):
                if not isinstance(index_val, int):
                    raise RuntimeError.from_info(
                        E306_RUNTIME_TYPE_ERROR,
                        f"List index must be an integer, found '{vakya_typeof(index_val)}'",
                        filename=self.filename,
                        line=assign.target.index.span.line,
                        column=assign.target.index.span.column,
                        length=assign.target.index.span.length,
                        source_code=self.source_code,
                    )
                if index_val < 0 or index_val >= len(target_obj):
                    raise IndexError.from_info(
                        E302_INDEX_OUT_OF_BOUNDS,
                        f"List index {index_val} out of bounds (size {len(target_obj)})",
                        filename=self.filename,
                        line=assign.target.index.span.line,
                        column=assign.target.index.span.column,
                        length=assign.target.index.span.length,
                        source_code=self.source_code,
                    )
                if assign.operator == "=":
                    target_obj[index_val] = val
                else:
                    curr_val = target_obj[index_val]
                    target_obj[index_val] = self._apply_compound_op(assign.operator, curr_val, val, assign.span)
                return target_obj[index_val]

            elif isinstance(target_obj, dict):
                key = index_val
                if assign.operator == "=":
                    target_obj[key] = val
                else:
                    curr_val = target_obj.get(key)
                    if curr_val is None:
                        raise RuntimeError.from_info(
                            E303_KEY_NOT_FOUND,
                            f"Key {vakya_str(key)} not found in map",
                            filename=self.filename,
                            line=assign.target.index.span.line,
                            column=assign.target.index.span.column,
                            length=assign.target.index.span.length,
                            source_code=self.source_code,
                        )
                    target_obj[key] = self._apply_compound_op(assign.operator, curr_val, val, assign.span)
                return target_obj[key]

            else:
                raise RuntimeError.from_info(
                    E306_RUNTIME_TYPE_ERROR,
                    f"Cannot assign by index to object of type '{vakya_typeof(target_obj)}'",
                    filename=self.filename,
                    line=assign.target.span.line,
                    column=assign.target.span.column,
                    length=assign.target.span.length,
                    source_code=self.source_code,
                )

        raise RuntimeError.from_info(
            E306_RUNTIME_TYPE_ERROR,
            "Invalid assignment target",
            filename=self.filename,
            line=assign.span.line,
            column=assign.span.column,
            length=assign.span.length,
            source_code=self.source_code,
        )

    def _apply_compound_op(self, op: str, left: Any, right: Any, span: Span) -> Any:
        if op == "+=":
            if isinstance(left, str) or isinstance(right, str):
                return vakya_str(left) + vakya_str(right)
            return left + right
        elif op == "-=":
            return left - right
        elif op == "*=":
            return left * right
        elif op == "/=":
            if right == 0:
                raise RuntimeError.from_info(
                    E301_DIVISION_BY_ZERO,
                    "Division by zero in compound assignment '/='",
                    filename=self.filename,
                    line=span.line,
                    column=span.column,
                    length=span.length,
                    source_code=self.source_code,
                )
            res = left / right
            return int(res) if isinstance(left, int) and isinstance(right, int) and left % right == 0 else res
        return right

    def _exec_if(self, stmt: IfStatement) -> Any:
        cond_val = self._evaluate(stmt.condition)
        if is_truthy(cond_val):
            return self._exec_block(stmt.then_block, Environment(self.current_env))

        for elif_cond, elif_block in stmt.else_if_branches:
            if is_truthy(self._evaluate(elif_cond)):
                return self._exec_block(elif_block, Environment(self.current_env))

        if stmt.else_block:
            return self._exec_block(stmt.else_block, Environment(self.current_env))

        return None

    def _exec_while(self, stmt: WhileStatement) -> Any:
        last_val = None
        while is_truthy(self._evaluate(stmt.condition)):
            try:
                last_val = self._exec_block(stmt.body, Environment(self.current_env))
            except BreakSignal:
                break
            except ContinueSignal:
                continue
        return last_val

    def _exec_for_each(self, stmt: ForEachStatement) -> Any:
        iterable_val = self._evaluate(stmt.iterable)
        if not isinstance(iterable_val, (list, str, dict)):
            raise RuntimeError.from_info(
                E306_RUNTIME_TYPE_ERROR,
                f"Cannot iterate over type '{vakya_typeof(iterable_val)}' with 'pratyekam'",
                filename=self.filename,
                line=stmt.iterable.span.line,
                column=stmt.iterable.span.column,
                length=stmt.iterable.span.length,
                source_code=self.source_code,
            )

        items = list(iterable_val.keys()) if isinstance(iterable_val, dict) else list(iterable_val)
        last_val = None

        for item in items:
            loop_env = Environment(self.current_env)
            loop_env.define(stmt.variable, item, is_constant=False)
            try:
                last_val = self._exec_block(stmt.body, loop_env)
            except BreakSignal:
                break
            except ContinueSignal:
                continue

        return last_val

    def _exec_block(self, block: Block, env: Environment) -> Any:
        old_env = self.current_env
        self.current_env = env
        last_val = None
        try:
            for s in block.statements:
                last_val = self._execute(s)
            return last_val
        finally:
            self.current_env = old_env

    # Expression Evaluation
    def _evaluate(self, expr: Expression) -> Any:
        if isinstance(expr, Literal):
            return expr.value

        if isinstance(expr, Identifier):
            return self.current_env.get(expr.name, span=expr.span, source_code=self.source_code, filename=self.filename)

        if isinstance(expr, BinaryExpr):
            return self._eval_binary(expr)

        if isinstance(expr, UnaryExpr):
            return self._eval_unary(expr)

        if isinstance(expr, ListLiteral):
            return [self._evaluate(el) for el in expr.elements]

        if isinstance(expr, MapLiteral):
            result_map = {}
            for k, v in expr.pairs:
                key_val = self._evaluate(k)
                val_val = self._evaluate(v)
                result_map[key_val] = val_val
            return result_map

        if isinstance(expr, IndexExpr):
            target = self._evaluate(expr.target)
            index = self._evaluate(expr.index)

            if isinstance(target, list):
                if not isinstance(index, int):
                    raise RuntimeError.from_info(
                        E306_RUNTIME_TYPE_ERROR,
                        f"List index must be an integer, found '{vakya_typeof(index)}'",
                        filename=self.filename,
                        line=expr.index.span.line,
                        column=expr.index.span.column,
                        length=expr.index.span.length,
                        source_code=self.source_code,
                    )
                if index < 0 or index >= len(target):
                    raise IndexError.from_info(
                        E302_INDEX_OUT_OF_BOUNDS,
                        f"List index {index} out of range for list of length {len(target)}",
                        filename=self.filename,
                        line=expr.index.span.line,
                        column=expr.index.span.column,
                        length=expr.index.span.length,
                        source_code=self.source_code,
                        help_text=f"Valid index range is [0, {max(0, len(target) - 1)}].",
                    )
                return target[index]

            elif isinstance(target, str):
                if not isinstance(index, int):
                    raise RuntimeError.from_info(
                        E306_RUNTIME_TYPE_ERROR,
                        f"String index must be an integer, found '{vakya_typeof(index)}'",
                        filename=self.filename,
                        line=expr.index.span.line,
                        column=expr.index.span.column,
                        length=expr.index.span.length,
                        source_code=self.source_code,
                    )
                if index < 0 or index >= len(target):
                    raise IndexError.from_info(
                        E302_INDEX_OUT_OF_BOUNDS,
                        f"String index {index} out of range for string of length {len(target)}",
                        filename=self.filename,
                        line=expr.index.span.line,
                        column=expr.index.span.column,
                        length=expr.index.span.length,
                        source_code=self.source_code,
                    )
                return target[index]

            elif isinstance(target, dict):
                if index not in target:
                    raise RuntimeError.from_info(
                        E303_KEY_NOT_FOUND,
                        f"Key {vakya_str(index)} not found in map",
                        filename=self.filename,
                        line=expr.index.span.line,
                        column=expr.index.span.column,
                        length=expr.index.span.length,
                        source_code=self.source_code,
                    )
                return target[index]

            raise RuntimeError.from_info(
                E306_RUNTIME_TYPE_ERROR,
                f"Type '{vakya_typeof(target)}' is not indexable",
                filename=self.filename,
                line=expr.target.span.line,
                column=expr.target.span.column,
                length=expr.target.span.length,
                source_code=self.source_code,
            )

        if isinstance(expr, MemberExpr):
            target = self._evaluate(expr.target)
            if expr.member == "length":
                if isinstance(target, (str, list, dict)):
                    return len(target)
                raise RuntimeError.from_info(
                    E307_INVALID_PROPERTY,
                    f"Property 'length' is not supported on type '{vakya_typeof(target)}'",
                    filename=self.filename,
                    line=expr.span.line,
                    column=expr.span.column,
                    length=expr.span.length,
                    source_code=self.source_code,
                )
            if isinstance(target, dict) and expr.member in target:
                return target[expr.member]

            raise RuntimeError.from_info(
                E307_INVALID_PROPERTY,
                f"Unknown property '{expr.member}' on object of type '{vakya_typeof(target)}'",
                filename=self.filename,
                line=expr.span.line,
                column=expr.span.column,
                length=expr.span.length,
                source_code=self.source_code,
            )

        if isinstance(expr, CallExpr):
            return self._eval_call(expr)

        return None

    def _eval_binary(self, expr: BinaryExpr) -> Any:
        op = expr.operator

        # Logical short-circuit operators
        if op == "va":
            left_val = self._evaluate(expr.left)
            if is_truthy(left_val):
                return True
            right_val = self._evaluate(expr.right)
            return is_truthy(right_val)

        if op == "evam":
            left_val = self._evaluate(expr.left)
            if not is_truthy(left_val):
                return False
            right_val = self._evaluate(expr.right)
            return is_truthy(right_val)

        left = self._evaluate(expr.left)
        right = self._evaluate(expr.right)

        if op == "+":
            if isinstance(left, str) or isinstance(right, str):
                return vakya_str(left) + vakya_str(right)
            if isinstance(left, (int, float)) and not isinstance(left, bool) and isinstance(right, (int, float)) and not isinstance(right, bool):
                return left + right
            raise RuntimeError.from_info(
                E306_RUNTIME_TYPE_ERROR,
                f"Cannot add types '{vakya_typeof(left)}' and '{vakya_typeof(right)}'",
                filename=self.filename,
                line=expr.span.line,
                column=expr.span.column,
                length=expr.span.length,
                source_code=self.source_code,
            )

        if op == "-":
            if isinstance(left, (int, float)) and not isinstance(left, bool) and isinstance(right, (int, float)) and not isinstance(right, bool):
                return left - right
            raise RuntimeError.from_info(
                E306_RUNTIME_TYPE_ERROR,
                f"Cannot subtract types '{vakya_typeof(left)}' and '{vakya_typeof(right)}'",
                filename=self.filename,
                line=expr.span.line,
                column=expr.span.column,
                length=expr.span.length,
                source_code=self.source_code,
            )

        if op == "*":
            if isinstance(left, (int, float)) and not isinstance(left, bool) and isinstance(right, (int, float)) and not isinstance(right, bool):
                return left * right
            if isinstance(left, str) and isinstance(right, int) and not isinstance(right, bool):
                return left * right
            if isinstance(right, str) and isinstance(left, int) and not isinstance(left, bool):
                return right * left
            raise RuntimeError.from_info(
                E306_RUNTIME_TYPE_ERROR,
                f"Cannot multiply types '{vakya_typeof(left)}' and '{vakya_typeof(right)}'",
                filename=self.filename,
                line=expr.span.line,
                column=expr.span.column,
                length=expr.span.length,
                source_code=self.source_code,
            )

        if op == "/":
            if not (isinstance(left, (int, float)) and not isinstance(left, bool) and isinstance(right, (int, float)) and not isinstance(right, bool)):
                raise RuntimeError.from_info(
                    E306_RUNTIME_TYPE_ERROR,
                    f"Cannot divide types '{vakya_typeof(left)}' and '{vakya_typeof(right)}'",
                    filename=self.filename,
                    line=expr.span.line,
                    column=expr.span.column,
                    length=expr.span.length,
                    source_code=self.source_code,
                )
            if right == 0:
                raise RuntimeError.from_info(
                    E301_DIVISION_BY_ZERO,
                    "Division by zero",
                    filename=self.filename,
                    line=expr.span.line,
                    column=expr.span.column,
                    length=expr.span.length,
                    source_code=self.source_code,
                )
            res = left / right
            # Return int if whole integer division
            if isinstance(left, int) and isinstance(right, int) and left % right == 0:
                return int(res)
            return res

        if op == "%":
            if not (isinstance(left, (int, float)) and not isinstance(left, bool) and isinstance(right, (int, float)) and not isinstance(right, bool)):
                raise RuntimeError.from_info(
                    E306_RUNTIME_TYPE_ERROR,
                    f"Cannot calculate modulo of types '{vakya_typeof(left)}' and '{vakya_typeof(right)}'",
                    filename=self.filename,
                    line=expr.span.line,
                    column=expr.span.column,
                    length=expr.span.length,
                    source_code=self.source_code,
                )
            if right == 0:
                raise RuntimeError.from_info(
                    E301_DIVISION_BY_ZERO,
                    "Modulo by zero",
                    filename=self.filename,
                    line=expr.span.line,
                    column=expr.span.column,
                    length=expr.span.length,
                    source_code=self.source_code,
                )
            return left % right

        if op == "**":
            if not (isinstance(left, (int, float)) and not isinstance(left, bool) and isinstance(right, (int, float)) and not isinstance(right, bool)):
                raise RuntimeError.from_info(
                    E306_RUNTIME_TYPE_ERROR,
                    f"Cannot calculate power of types '{vakya_typeof(left)}' and '{vakya_typeof(right)}'",
                    filename=self.filename,
                    line=expr.span.line,
                    column=expr.span.column,
                    length=expr.span.length,
                    source_code=self.source_code,
                )
            return left ** right

        if op == "==":
            if isinstance(left, bool) != isinstance(right, bool):
                return False
            return left == right

        if op == "!=":
            if isinstance(left, bool) != isinstance(right, bool):
                return True
            return left != right

        if op in ("<", "<=", ">", ">="):
            is_left_num = isinstance(left, (int, float)) and not isinstance(left, bool)
            is_right_num = isinstance(right, (int, float)) and not isinstance(right, bool)
            if is_left_num and is_right_num:
                if op == "<":
                    return left < right
                if op == "<=":
                    return left <= right
                if op == ">":
                    return left > right
                if op == ">=":
                    return left >= right
            elif isinstance(left, str) and isinstance(right, str):
                if op == "<":
                    return left < right
                if op == "<=":
                    return left <= right
                if op == ">":
                    return left > right
                if op == ">=":
                    return left >= right
            else:
                raise RuntimeError.from_info(
                    E306_RUNTIME_TYPE_ERROR,
                    f"Cannot compare types '{vakya_typeof(left)}' and '{vakya_typeof(right)}' with '{op}'",
                    filename=self.filename,
                    line=expr.span.line,
                    column=expr.span.column,
                    length=expr.span.length,
                    source_code=self.source_code,
                )

        raise RuntimeError.from_info(
            E306_RUNTIME_TYPE_ERROR,
            f"Unsupported binary operator '{op}'",
            filename=self.filename,
            line=expr.span.line,
            column=expr.span.column,
            length=expr.span.length,
            source_code=self.source_code,
        )

    def _eval_unary(self, expr: UnaryExpr) -> Any:
        val = self._evaluate(expr.operand)
        if expr.operator == "-":
            if isinstance(val, (int, float)) and not isinstance(val, bool):
                return -val
            raise RuntimeError.from_info(
                E306_RUNTIME_TYPE_ERROR,
                f"Unary '-' cannot be applied to type '{vakya_typeof(val)}'",
                filename=self.filename,
                line=expr.span.line,
                column=expr.span.column,
                length=expr.span.length,
                source_code=self.source_code,
            )
        if expr.operator == "+":
            if isinstance(val, (int, float)) and not isinstance(val, bool):
                return +val
            raise RuntimeError.from_info(
                E306_RUNTIME_TYPE_ERROR,
                f"Unary '+' cannot be applied to type '{vakya_typeof(val)}'",
                filename=self.filename,
                line=expr.span.line,
                column=expr.span.column,
                length=expr.span.length,
                source_code=self.source_code,
            )
        if expr.operator == "na":
            return not is_truthy(val)
        raise RuntimeError.from_info(
            E306_RUNTIME_TYPE_ERROR,
            f"Unsupported unary operator '{expr.operator}'",
            filename=self.filename,
            line=expr.span.line,
            column=expr.span.column,
            length=expr.span.length,
            source_code=self.source_code,
        )

    def _eval_call(self, expr: CallExpr) -> Any:
        callee = self._evaluate(expr.callee)
        arg_values = [self._evaluate(arg) for arg in expr.arguments]

        if isinstance(callee, VakyaBuiltin):
            try:
                return callee.func(*arg_values)
            except VakyaError:
                raise
            except Exception as ex:
                raise RuntimeError.from_info(
                    E306_RUNTIME_TYPE_ERROR,
                    f"Error executing built-in '{callee.name}': {ex}",
                    filename=self.filename,
                    line=expr.span.line,
                    column=expr.span.column,
                    length=expr.span.length,
                    source_code=self.source_code,
                )

        if isinstance(callee, VakyaFunction):
            if self.call_depth >= self.max_call_depth:
                raise RuntimeError.from_info(
                    E304_RECURSION_LIMIT,
                    f"Call stack limit ({self.max_call_depth}) reached in function '{callee.name}'",
                    filename=self.filename,
                    line=expr.span.line,
                    column=expr.span.column,
                    length=expr.span.length,
                    source_code=self.source_code,
                    help_text="Check for unbounded recursion or missing base condition in your function.",
                )

            if len(arg_values) != len(callee.params):
                raise ArgumentError.from_info(
                    E406_ARGUMENT_COUNT_MISMATCH,
                    f"Function '{callee.name}' expects {len(callee.params)} argument(s), but received {len(arg_values)}",
                    filename=self.filename,
                    line=expr.span.line,
                    column=expr.span.column,
                    length=expr.span.length,
                    source_code=self.source_code,
                )

            fn_env = Environment(callee.closure)
            for param, arg_val in zip(callee.params, arg_values):
                fn_env.define(param.name, arg_val, is_constant=False)

            self.call_depth += 1
            try:
                self._exec_block(callee.body, fn_env)
                return None  # default return shunya
            except ReturnSignal as ret:
                return ret.value
            finally:
                self.call_depth -= 1

        if callable(callee):
            try:
                return callee(*arg_values)
            except VakyaError:
                raise
            except Exception as ex:
                raise RuntimeError.from_info(
                    E306_RUNTIME_TYPE_ERROR,
                    f"Error invoking function: {ex}",
                    filename=self.filename,
                    line=expr.span.line,
                    column=expr.span.column,
                    length=expr.span.length,
                    source_code=self.source_code,
                )

        raise RuntimeError.from_info(
            E305_NOT_CALLABLE,
            f"Value of type '{vakya_typeof(callee)}' is not callable",
            filename=self.filename,
            line=expr.callee.span.line,
            column=expr.callee.span.column,
            length=expr.callee.span.length,
            source_code=self.source_code,
            help_text="Only functions ('karya') can be invoked with '()'.",
        )
