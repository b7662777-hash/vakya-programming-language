"""Runtime values and formatting for Vākya."""

from dataclasses import dataclass
from typing import Any, Callable, List, Optional
from ..ast.nodes import Block, Param, Span


def vakya_typeof(val: Any) -> str:
    """Return the Vākya type name for a runtime value."""
    if val is None:
        return "shunya"
    if isinstance(val, bool):
        return "boolean"
    if isinstance(val, int):
        return "sankhya"
    if isinstance(val, float):
        return "dashamika"
    if isinstance(val, str):
        return "shabda"
    if isinstance(val, list):
        return "suchi"
    if isinstance(val, dict):
        return "naksha"
    if isinstance(val, (VakyaFunction, VakyaBuiltin)):
        return "karya"
    return "unknown"


def is_truthy(val: Any) -> bool:
    """Evaluate truthiness according to Vākya semantics."""
    if val is None or val is False:
        return False
    if val is True:
        return True
    if isinstance(val, (int, float)):
        return val != 0
    if isinstance(val, (str, list, dict)):
        return len(val) > 0
    return True


def vakya_str(val: Any) -> str:
    """Convert a runtime value to its Vākya string representation for output."""
    if val is None:
        return "shunya"
    if isinstance(val, bool):
        return "satya" if val else "asatya"
    if isinstance(val, float):
        # Format clean floats like 3.14 or 3.0
        if val.is_integer():
            return f"{int(val)}.0"
        return str(val)
    if isinstance(val, str):
        return val
    if isinstance(val, list):
        elements = ", ".join(vakya_repr(item) for item in val)
        return f"[{elements}]"
    if isinstance(val, dict):
        pairs = ", ".join(f"{vakya_repr(k)}: {vakya_repr(v)}" for k, v in val.items())
        return f"{{{pairs}}}"
    if isinstance(val, (VakyaFunction, VakyaBuiltin)):
        return f"<karya {val.name}>"
    return str(val)


def vakya_repr(val: Any) -> str:
    """Convert a runtime value to its literal/inspection representation."""
    if isinstance(val, str):
        escaped = val.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\t", "\\t")
        return f'"{escaped}"'
    return vakya_str(val)


@dataclass
class VakyaFunction:
    name: str
    params: List[Param]
    body: Block
    closure: Any  # Environment
    return_type: Optional[str] = None
    span: Optional[Span] = None


@dataclass
class VakyaBuiltin:
    name: str
    func: Callable[..., Any]
