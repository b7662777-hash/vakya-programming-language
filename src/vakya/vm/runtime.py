"""Runtime value representations and built-in functions for the Vākya Virtual Machine."""

import sys
import json
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, TextIO
from vakya.bytecode.chunk import Chunk
from vakya.errors import (
    RuntimeError,
    IndexError,
    ArgumentError,
    TypeError,
    E301_DIVISION_BY_ZERO,
    E302_INDEX_OUT_OF_BOUNDS,
    E303_KEY_NOT_FOUND,
    E306_RUNTIME_TYPE_ERROR,
    E406_ARGUMENT_COUNT_MISMATCH,
)


@dataclass
class UpvalueCell:
    value: Any = None


@dataclass
class VMClosure:
    chunk: Chunk
    upvalues: List[UpvalueCell] = field(default_factory=list)

    @property
    def name(self) -> str:
        return self.chunk.name

    def __str__(self) -> str:
        return f"<karya {self.name}>"

    def __repr__(self) -> str:
        return f"<VMClosure {self.name} params={len(self.chunk.param_names)} upvals={len(self.upvalues)}>"


@dataclass
class VMBuiltin:
    name: str
    func: Callable[..., Any]

    def __str__(self) -> str:
        return f"<karya (builtin) {self.name}>"

    def __repr__(self) -> str:
        return f"<VMBuiltin {self.name}>"


def is_truthy(val: Any) -> bool:
    """Vākya truthiness rules."""
    if val is None or val is False:
        return False
    if val == 0 or val == 0.0 or val == "":
        return False
    if isinstance(val, (list, dict)) and len(val) == 0:
        return False
    return True


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
    if isinstance(val, (VMClosure, VMBuiltin, Chunk)):
        return "karya"
    return "ajnata"


def vakya_str(val: Any) -> str:
    """Convert a runtime value to its Vākya string representation for output."""
    if val is None:
        return "shunya"
    if isinstance(val, bool):
        return "satya" if val else "asatya"
    if isinstance(val, float):
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
    if isinstance(val, (VMClosure, VMBuiltin)):
        return f"<karya {val.name}>"
    return str(val)


def vakya_repr(val: Any) -> str:
    """Convert a runtime value to its literal/inspection representation."""
    if isinstance(val, str):
        escaped = val.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\t", "\\t")
        return f'"{escaped}"'
    return vakya_str(val)


def create_vm_builtins(stdout: Optional[TextIO] = None, stdin: Optional[TextIO] = None) -> Dict[str, VMBuiltin]:
    out_stream = stdout if stdout is not None else sys.stdout
    in_stream = stdin if stdin is not None else sys.stdin

    def builtin_vada(*args: Any) -> None:
        formatted = " ".join(vakya_str(arg) for arg in args)
        print(formatted, file=out_stream)
        return None

    def builtin_puchha(prompt: Any = "") -> str:
        if prompt != "":
            out_stream.write(vakya_str(prompt))
            out_stream.flush()
        line = in_stream.readline()
        if line.endswith("\n"):
            line = line[:-1]
        if line.endswith("\r"):
            line = line[:-1]
        return line

    def builtin_lamba(obj: Any) -> int:
        if isinstance(obj, (list, dict, str)):
            return len(obj)
        raise TypeError.from_info(
            E306_RUNTIME_TYPE_ERROR,
            f"lamba() expects suchi, naksha, or shabda, found '{vakya_typeof(obj)}'",
        )

    def builtin_prakaar(obj: Any) -> str:
        return vakya_typeof(obj)

    def builtin_suchi_jodo(lst: Any, item: Any) -> Any:
        if not isinstance(lst, list):
            raise TypeError.from_info(
                E306_RUNTIME_TYPE_ERROR,
                f"suchi_jodo() expects a suchi as first argument, found '{vakya_typeof(lst)}'",
            )
        lst.append(item)
        return lst

    def builtin_suchi_hatao(lst: Any, index: Any = None) -> Any:
        if not isinstance(lst, list):
            raise TypeError.from_info(
                E306_RUNTIME_TYPE_ERROR,
                f"suchi_hatao() expects a suchi as first argument, found '{vakya_typeof(lst)}'",
            )
        if len(lst) == 0:
            raise IndexError.from_info(
                E302_INDEX_OUT_OF_BOUNDS,
                "Cannot remove item from empty list",
            )
        if index is None:
            return lst.pop()
        if not isinstance(index, int) or isinstance(index, bool):
            raise TypeError.from_info(
                E306_RUNTIME_TYPE_ERROR,
                f"suchi_hatao() index must be sankhya, found '{vakya_typeof(index)}'",
            )
        if index < 0 or index >= len(lst):
            raise IndexError.from_info(
                E302_INDEX_OUT_OF_BOUNDS,
                f"Index {index} out of bounds for list of length {len(lst)}",
            )
        return lst.pop(index)

    def builtin_shabda_bada(s: Any) -> str:
        if not isinstance(s, str):
            raise TypeError.from_info(
                E306_RUNTIME_TYPE_ERROR,
                f"shabda_bada() expects shabda, found '{vakya_typeof(s)}'",
            )
        return s.upper()

    def builtin_shabda_chhota(s: Any) -> str:
        if not isinstance(s, str):
            raise TypeError.from_info(
                E306_RUNTIME_TYPE_ERROR,
                f"shabda_chhota() expects shabda, found '{vakya_typeof(s)}'",
            )
        return s.lower()

    def builtin_shabda_trim(s: Any) -> str:
        if not isinstance(s, str):
            raise TypeError.from_info(
                E306_RUNTIME_TYPE_ERROR,
                f"shabda_trim() expects shabda, found '{vakya_typeof(s)}'",
            )
        return s.strip()

    def builtin_vakya_iter(obj: Any) -> Any:
        if isinstance(obj, dict):
            return list(obj.keys())
        if isinstance(obj, list):
            return obj
        if isinstance(obj, str):
            return list(obj)
        return obj

    return {
        "vada": VMBuiltin("vada", builtin_vada),
        "puchha": VMBuiltin("puchha", builtin_puchha),
        "lamba": VMBuiltin("lamba", builtin_lamba),
        "prakaar": VMBuiltin("prakaar", builtin_prakaar),
        "suchi_jodo": VMBuiltin("suchi_jodo", builtin_suchi_jodo),
        "suchi_hatao": VMBuiltin("suchi_hatao", builtin_suchi_hatao),
        "shabda_bada": VMBuiltin("shabda_bada", builtin_shabda_bada),
        "shabda_chhota": VMBuiltin("shabda_chhota", builtin_shabda_chhota),
        "shabda_trim": VMBuiltin("shabda_trim", builtin_shabda_trim),
        "__vakya_iter": VMBuiltin("__vakya_iter", builtin_vakya_iter),
    }
