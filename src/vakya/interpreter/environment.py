"""Lexical environment for Vākya runtime execution."""

from typing import Any, Dict, Optional, Set
from ..ast.nodes import Span
from ..errors import (
    NameError,
    ConstantError,
    E101_UNDEFINED_VARIABLE,
    E103_CONSTANT_REASSIGNMENT,
)


class Environment:
    """Manages variable bindings with lexical scoping."""

    def __init__(self, parent: Optional["Environment"] = None):
        self.parent = parent
        self.values: Dict[str, Any] = {}
        self.constants: Set[str] = set()

    def define(self, name: str, value: Any, is_constant: bool = False) -> None:
        """Bind a variable or constant in the local scope."""
        self.values[name] = value
        if is_constant:
            self.constants.add(name)

    def assign(
        self,
        name: str,
        value: Any,
        span: Optional[Span] = None,
        source_code: str = "",
        filename: str = "<anonymous>",
    ) -> None:
        """Assign a new value to an existing variable in the closest enclosing scope."""
        if name in self.values:
            if name in self.constants:
                raise ConstantError.from_info(
                    E103_CONSTANT_REASSIGNMENT,
                    f"Cannot reassign constant '{name}' declared with 'dhruva'",
                    filename=filename,
                    line=span.line if span else 1,
                    column=span.column if span else 1,
                    length=span.length if span else len(name),
                    source_code=source_code,
                    help_text="Variables declared with 'dhruva' cannot be modified. Use 'chara' for mutable variables.",
                )
            self.values[name] = value
            return

        if self.parent is not None:
            self.parent.assign(name, value, span=span, source_code=source_code, filename=filename)
            return

        raise NameError.from_info(
            E101_UNDEFINED_VARIABLE,
            f"Undefined variable '{name}'",
            filename=filename,
            line=span.line if span else 1,
            column=span.column if span else 1,
            length=span.length if span else len(name),
            source_code=source_code,
            help_text=f"Declare variable '{name}' using 'chara' before assigning to it.",
        )

    def get(
        self,
        name: str,
        span: Optional[Span] = None,
        source_code: str = "",
        filename: str = "<anonymous>",
    ) -> Any:
        """Retrieve the value of an identifier from the current or parent scopes."""
        if name in self.values:
            return self.values[name]

        if self.parent is not None:
            return self.parent.get(name, span=span, source_code=source_code, filename=filename)

        raise NameError.from_info(
            E101_UNDEFINED_VARIABLE,
            f"Undefined variable '{name}'",
            filename=filename,
            line=span.line if span else 1,
            column=span.column if span else 1,
            length=span.length if span else len(name),
            source_code=source_code,
            help_text=f"Declare '{name}' using 'chara' or 'dhruva' before using it.",
        )

    def exists(self, name: str) -> bool:
        """Check if a variable exists in the scope hierarchy."""
        if name in self.values:
            return True
        if self.parent is not None:
            return self.parent.exists(name)
        return False
