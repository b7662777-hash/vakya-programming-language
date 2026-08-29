"""Deterministic source code formatter for Vākya."""

from typing import Any, List, Optional
from ..ast.nodes import (
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
from ..lexer.lexer import Lexer
from ..parser.parser import Parser


class Formatter:
    """Formats Vākya source code into canonical style."""

    def __init__(self, indent_size: int = 4):
        self.indent_size = indent_size
        self.indent_level = 0

    def _indent(self) -> str:
        return " " * (self.indent_level * self.indent_size)

    def format_source(self, source: str, filename: str = "<anonymous>") -> str:
        lexer = Lexer(source, filename=filename)
        tokens = lexer.tokenize()
        parser = Parser(tokens, source_code=source, filename=filename)
        ast = parser.parse()
        return self.format_program(ast)

    def format_program(self, program: Program) -> str:
        lines: List[str] = []
        for i, stmt in enumerate(program.statements):
            formatted_stmt = self.format_statement(stmt)
            lines.append(formatted_stmt)
            # Add an extra blank line between top-level function declarations and other statements
            if isinstance(stmt, FunctionDecl) and i < len(program.statements) - 1:
                lines.append("")
        return "\n".join(lines) + "\n"

    def format_statement(self, stmt: Statement) -> str:
        if isinstance(stmt, VarDecl):
            kw = "dhruva" if stmt.is_constant else "chara"
            type_str = f": {stmt.type_annotation}" if stmt.type_annotation else ""
            init_str = f" = {self.format_expression(stmt.initializer)}" if stmt.initializer is not None else ""
            return f"{self._indent()}{kw} {stmt.name}{type_str}{init_str}"

        if isinstance(stmt, FunctionDecl):
            params_str = ", ".join(self.format_param(p) for p in stmt.params)
            ret_str = f" -> {stmt.return_type}" if stmt.return_type else ""
            header = f"{self._indent()}karya {stmt.name}({params_str}){ret_str} {{"
            body_str = self.format_block_body(stmt.body)
            footer = f"{self._indent()}}}"
            return f"{header}\n{body_str}\n{footer}" if body_str else f"{header}\n{footer}"

        if isinstance(stmt, Assignment):
            target_str = self.format_expression(stmt.target)
            val_str = self.format_expression(stmt.value)
            return f"{self._indent()}{target_str} {stmt.operator} {val_str}"

        if isinstance(stmt, IfStatement):
            cond_str = self.format_expression(stmt.condition)
            result = f"{self._indent()}yadi {cond_str} {{"
            then_body = self.format_block_body(stmt.then_block)
            if then_body:
                result += f"\n{then_body}"

            for elif_cond, elif_block in stmt.else_if_branches:
                elif_cond_str = self.format_expression(elif_cond)
                result += f"\n{self._indent()}}} anyatha yadi {elif_cond_str} {{"
                elif_body = self.format_block_body(elif_block)
                if elif_body:
                    result += f"\n{elif_body}"

            if stmt.else_block:
                result += f"\n{self._indent()}}} anyatha {{"
                else_body = self.format_block_body(stmt.else_block)
                if else_body:
                    result += f"\n{else_body}"

            result += f"\n{self._indent()}}}"
            return result

        if isinstance(stmt, WhileStatement):
            cond_str = self.format_expression(stmt.condition)
            result = f"{self._indent()}yavat {cond_str} {{"
            body_str = self.format_block_body(stmt.body)
            if body_str:
                result += f"\n{body_str}"
            result += f"\n{self._indent()}}}"
            return result

        if isinstance(stmt, ForEachStatement):
            iter_str = self.format_expression(stmt.iterable)
            result = f"{self._indent()}pratyekam {stmt.variable} madhye {iter_str} {{"
            body_str = self.format_block_body(stmt.body)
            if body_str:
                result += f"\n{body_str}"
            result += f"\n{self._indent()}}}"
            return result

        if isinstance(stmt, BreakStatement):
            return f"{self._indent()}virama"

        if isinstance(stmt, ContinueStatement):
            return f"{self._indent()}agaccha"

        if isinstance(stmt, ReturnStatement):
            val_str = f" {self.format_expression(stmt.value)}" if stmt.value is not None else ""
            return f"{self._indent()}pratyavartaya{val_str}"

        if isinstance(stmt, Block):
            result = f"{self._indent()}{{"
            body_str = self.format_block_body(stmt)
            if body_str:
                result += f"\n{body_str}"
            result += f"\n{self._indent()}}}"
            return result

        if isinstance(stmt, ExpressionStatement):
            return f"{self._indent()}{self.format_expression(stmt.expression)}"

        return ""

    def format_param(self, param: Param) -> str:
        if param.type_annotation:
            return f"{param.name}: {param.type_annotation}"
        return param.name

    def format_block_body(self, block: Block) -> str:
        self.indent_level += 1
        lines = [self.format_statement(s) for s in block.statements]
        self.indent_level -= 1
        return "\n".join(lines)

    def format_expression(self, expr: Optional[Expression]) -> str:
        if expr is None:
            return ""

        if isinstance(expr, Literal):
            if expr.literal_type == "shabda":
                escaped = str(expr.value).replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\t", "\\t")
                return f'"{escaped}"'
            elif expr.literal_type == "boolean":
                return "satya" if expr.value else "asatya"
            elif expr.literal_type == "shunya":
                return "shunya"
            elif expr.literal_type == "dashamika":
                val = float(expr.value)
                return f"{int(val)}.0" if val.is_integer() else str(val)
            return str(expr.value)

        if isinstance(expr, Identifier):
            return expr.name

        if isinstance(expr, BinaryExpr):
            left_str = self._format_sub_expr(expr.left, expr, is_left=True)
            right_str = self._format_sub_expr(expr.right, expr, is_left=False)
            return f"{left_str} {expr.operator} {right_str}"

        if isinstance(expr, UnaryExpr):
            op_str = f"{expr.operator} " if expr.operator == "na" else expr.operator
            operand_str = self._format_sub_expr(expr.operand, expr, is_left=False)
            return f"{op_str}{operand_str}"

        if isinstance(expr, ListLiteral):
            elements_str = ", ".join(self.format_expression(e) for e in expr.elements)
            return f"[{elements_str}]"

        if isinstance(expr, MapLiteral):
            pairs_str = ", ".join(f"{self.format_expression(k)}: {self.format_expression(v)}" for k, v in expr.pairs)
            return f"{{{pairs_str}}}"

        if isinstance(expr, IndexExpr):
            tgt_str = self.format_expression(expr.target)
            idx_str = self.format_expression(expr.index)
            return f"{tgt_str}[{idx_str}]"

        if isinstance(expr, MemberExpr):
            tgt_str = self.format_expression(expr.target)
            return f"{tgt_str}.{expr.member}"

        if isinstance(expr, CallExpr):
            callee_str = self.format_expression(expr.callee)
            args_str = ", ".join(self.format_expression(a) for a in expr.arguments)
            return f"{callee_str}({args_str})"

        return str(expr)

    def _get_precedence(self, expr: Expression) -> int:
        if isinstance(expr, BinaryExpr):
            op = expr.operator
            if op == "va":
                return 1
            if op == "evam":
                return 2
            if op in ("==", "!="):
                return 4
            if op in ("<", "<=", ">", ">="):
                return 5
            if op in ("+", "-"):
                return 6
            if op in ("*", "/", "%"):
                return 7
            if op == "**":
                return 9
        if isinstance(expr, UnaryExpr):
            if expr.operator == "na":
                return 3
            return 8
        if isinstance(expr, (CallExpr, IndexExpr, MemberExpr)):
            return 10
        return 11  # Literals, identifiers, lists, maps

    def _format_sub_expr(self, sub_expr: Expression, parent_expr: Expression, is_left: bool) -> str:
        parent_prec = self._get_precedence(parent_expr)
        sub_prec = self._get_precedence(sub_expr)

        needs_parens = sub_prec < parent_prec
        # For non-associative or right-associative power
        if isinstance(parent_expr, BinaryExpr) and isinstance(sub_expr, BinaryExpr):
            if parent_expr.operator == "**" and is_left and sub_expr.operator == "**":
                needs_parens = True

        formatted = self.format_expression(sub_expr)
        if needs_parens:
            return f"({formatted})"
        return formatted
