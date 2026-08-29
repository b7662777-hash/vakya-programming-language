"""Abstract Syntax Tree (AST) node definitions for Vākya."""

from dataclasses import dataclass, field
from typing import Any, List, Optional, Tuple


@dataclass(frozen=True)
class Span:
    """Source code location range."""

    line: int
    column: int
    end_line: int
    end_column: int
    filename: str = "<anonymous>"

    @property
    def length(self) -> int:
        if self.line == self.end_line:
            return max(1, self.end_column - self.column)
        return 1

    @classmethod
    def from_token(cls, token: Any) -> "Span":
        return cls(
            line=token.line,
            column=token.column,
            end_line=token.line,
            end_column=token.column + token.length,
            filename=token.filename,
        )

    @classmethod
    def between(cls, start: "Span", end: "Span") -> "Span":
        return cls(
            line=start.line,
            column=start.column,
            end_line=end.end_line,
            end_column=end.end_column,
            filename=start.filename,
        )


@dataclass
class ASTNode:
    """Base class for all AST nodes."""

    span: Span


# Expressions
@dataclass
class Expression(ASTNode):
    """Base class for expressions."""


@dataclass
class Literal(Expression):
    value: Any
    literal_type: str  # "sankhya", "dashamika", "shabda", "boolean", "shunya"


@dataclass
class Identifier(Expression):
    name: str


@dataclass
class BinaryExpr(Expression):
    left: Expression
    operator: str
    right: Expression


@dataclass
class UnaryExpr(Expression):
    operator: str
    operand: Expression


@dataclass
class ListLiteral(Expression):
    elements: List[Expression]


@dataclass
class MapLiteral(Expression):
    pairs: List[Tuple[Expression, Expression]]


@dataclass
class IndexExpr(Expression):
    target: Expression
    index: Expression


@dataclass
class MemberExpr(Expression):
    target: Expression
    member: str


@dataclass
class CallExpr(Expression):
    callee: Expression
    arguments: List[Expression]


# Statements
@dataclass
class Statement(ASTNode):
    """Base class for statements."""


@dataclass
class ExpressionStatement(Statement):
    expression: Expression


@dataclass
class VarDecl(Statement):
    name: str
    type_annotation: Optional[str]
    initializer: Optional[Expression]
    is_constant: bool


@dataclass
class Assignment(Statement):
    target: Expression  # Identifier, IndexExpr, or MemberExpr
    operator: str       # "=", "+=", "-=", "*=", "/="
    value: Expression


@dataclass
class Block(Statement):
    statements: List[Statement]


@dataclass
class IfStatement(Statement):
    condition: Expression
    then_block: Block
    else_if_branches: List[Tuple[Expression, Block]]
    else_block: Optional[Block]


@dataclass
class WhileStatement(Statement):
    condition: Expression
    body: Block


@dataclass
class ForEachStatement(Statement):
    variable: str
    iterable: Expression
    body: Block


@dataclass
class BreakStatement(Statement):
    pass


@dataclass
class ContinueStatement(Statement):
    pass


@dataclass
class ReturnStatement(Statement):
    value: Optional[Expression]


@dataclass
class Param(ASTNode):
    name: str
    type_annotation: Optional[str]


@dataclass
class FunctionDecl(Statement):
    name: str
    params: List[Param]
    return_type: Optional[str]
    body: Block


@dataclass
class ImportStatement(Statement):
    module_name: str
    alias: Optional[str] = None


@dataclass
class Program(ASTNode):
    statements: List[Statement]
