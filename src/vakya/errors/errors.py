"""Vākya structured error classes and diagnostic formatting."""

from typing import Optional
from .codes import ErrorInfo


class VakyaError(Exception):
    """Base error class for all Vākya compiler and runtime errors."""

    def __init__(
        self,
        message: str,
        code: Optional[str] = None,
        filename: str = "<anonymous>",
        line: int = 1,
        column: int = 1,
        length: int = 1,
        source_code: Optional[str] = None,
        help_text: Optional[str] = None,
    ):
        super().__init__(message)
        self.message = message
        self.code = code or "E000"
        self.filename = filename
        self.line = line
        self.column = column
        self.length = max(1, length)
        self.source_code = source_code
        self.help_text = help_text

    @classmethod
    def from_info(
        cls,
        info: ErrorInfo,
        detail: str,
        filename: str = "<anonymous>",
        line: int = 1,
        column: int = 1,
        length: int = 1,
        source_code: Optional[str] = None,
        help_text: Optional[str] = None,
    ):
        if detail:
            if detail.lower().startswith(info.title.lower()):
                msg = detail
            else:
                msg = f"{info.title}: {detail}"
        else:
            msg = info.title
        help_str = help_text if help_text is not None else info.default_help
        return cls(
            message=msg,
            code=info.code,
            filename=filename,
            line=line,
            column=column,
            length=length,
            source_code=source_code,
            help_text=help_str,
        )

    def format_diagnostic(self, source_code: Optional[str] = None) -> str:
        """Render a formatted, user-friendly diagnostic message."""
        src = source_code if source_code is not None else self.source_code
        header = f"Error [{self.code}]: {self.message}"
        location_line = f"  --> {self.filename}:{self.line}:{self.column}"

        if not src:
            result = f"{header}\n\n{location_line}"
            if self.help_text:
                result += f"\n\nHelp: {self.help_text}"
            return result

        lines = src.splitlines()
        target_idx = self.line - 1

        # Gutter width calculation
        start_idx = max(0, target_idx - 1)
        end_idx = min(len(lines), target_idx + 2)
        max_lineno_len = len(str(end_idx))

        snippet_lines = []
        for i in range(start_idx, end_idx):
            lineno = i + 1
            gutter = str(lineno).rjust(max_lineno_len)
            line_str = lines[i] if i < len(lines) else ""
            snippet_lines.append(f" {gutter} | {line_str}")

            if i == target_idx:
                empty_gutter = " " * max_lineno_len
                col_offset = " " * (max(0, self.column - 1))
                carets = "^" * self.length
                snippet_lines.append(f" {empty_gutter} | {col_offset}{carets}")

        snippet = "\n".join(snippet_lines)
        result = f"{header}\n\n{location_line}\n\n{snippet}"

        if self.help_text:
            result += f"\n\nHelp: {self.help_text}"

        return result

    def __str__(self) -> str:
        return self.format_diagnostic()


class LexerError(VakyaError):
    """Errors encountered during lexical tokenization."""


class ParseError(VakyaError):
    """Errors encountered during syntax parsing."""


class TypeError(VakyaError):
    """Errors encountered during static type checking."""


class RuntimeError(VakyaError):
    """Errors encountered during program execution."""


class NameError(VakyaError):
    """Errors related to undeclared or duplicate identifiers."""


class ArgumentError(VakyaError):
    """Errors related to invalid function call arguments."""


class IndexError(VakyaError):
    """Errors related to list index or string index out of range."""


class ConstantError(VakyaError):
    """Errors related to reassignment or modification of constants."""
