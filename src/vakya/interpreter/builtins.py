"""Standard built-in functions for Vākya runtime."""

import sys
from typing import Any, Callable, Dict, TextIO
from ..errors import (
    RuntimeError,
    IndexError,
    ArgumentError,
    E302_INDEX_OUT_OF_BOUNDS,
    E306_RUNTIME_TYPE_ERROR,
    E406_ARGUMENT_COUNT_MISMATCH,
)
from .values import VakyaBuiltin, vakya_str, vakya_typeof


def create_builtins(
    stdout: TextIO = sys.stdout,
    stdin: TextIO = sys.stdin,
) -> Dict[str, VakyaBuiltin]:
    """Create a dictionary of standard built-in functions bound to I/O streams."""

    def builtin_vada(*args: Any) -> Any:
        output = " ".join(vakya_str(arg) for arg in args)
        stdout.write(output + "\n")
        stdout.flush()
        return None

    def builtin_puchha(prompt: Any = "") -> str:
        if prompt != "":
            stdout.write(vakya_str(prompt))
            stdout.flush()
        line = stdin.readline()
        if line.endswith("\n"):
            line = line[:-1]
        if line.endswith("\r"):
            line = line[:-1]
        return line

    def builtin_lamba(val: Any) -> int:
        if isinstance(val, (str, list, dict)):
            return len(val)
        raise RuntimeError.from_info(
            E306_RUNTIME_TYPE_ERROR,
            f"Cannot determine length of type '{vakya_typeof(val)}'",
            help_text="'lamba' expects a string (shabda), list (suchi), or map (naksha).",
        )

    def builtin_prakaar(val: Any) -> str:
        return vakya_typeof(val)

    def builtin_suchi_jodo(lst: Any, val: Any) -> Any:
        if not isinstance(lst, list):
            raise RuntimeError.from_info(
                E306_RUNTIME_TYPE_ERROR,
                f"'suchi_jodo' expects a list (suchi) as first argument, found '{vakya_typeof(lst)}'",
            )
        lst.append(val)
        return None

    def builtin_suchi_hatao(lst: Any, index: Any) -> Any:
        if not isinstance(lst, list):
            raise RuntimeError.from_info(
                E306_RUNTIME_TYPE_ERROR,
                f"'suchi_hatao' expects a list (suchi) as first argument, found '{vakya_typeof(lst)}'",
            )
        if not isinstance(index, int):
            raise RuntimeError.from_info(
                E306_RUNTIME_TYPE_ERROR,
                f"List index must be an integer (sankhya), found '{vakya_typeof(index)}'",
            )
        if index < 0 or index >= len(lst):
            raise IndexError.from_info(
                E302_INDEX_OUT_OF_BOUNDS,
                f"Index {index} is out of bounds for list of length {len(lst)}",
                help_text=f"Valid index range is [0, {max(0, len(lst) - 1)}].",
            )
        return lst.pop(index)

    def builtin_shabda_bada(text: Any) -> str:
        if not isinstance(text, str):
            raise RuntimeError.from_info(
                E306_RUNTIME_TYPE_ERROR,
                f"'shabda_bada' expects a string (shabda), found '{vakya_typeof(text)}'",
            )
        return text.upper()

    def builtin_shabda_chhota(text: Any) -> str:
        if not isinstance(text, str):
            raise RuntimeError.from_info(
                E306_RUNTIME_TYPE_ERROR,
                f"'shabda_chhota' expects a string (shabda), found '{vakya_typeof(text)}'",
            )
        return text.lower()

    def builtin_shabda_trim(text: Any) -> str:
        if not isinstance(text, str):
            raise RuntimeError.from_info(
                E306_RUNTIME_TYPE_ERROR,
                f"'shabda_trim' expects a string (shabda), found '{vakya_typeof(text)}'",
            )
        return text.strip()

    builtins_map: Dict[str, Callable[..., Any]] = {
        "vada": builtin_vada,
        "puchha": builtin_puchha,
        "lamba": builtin_lamba,
        "prakaar": builtin_prakaar,
        "suchi_jodo": builtin_suchi_jodo,
        "suchi_hatao": builtin_suchi_hatao,
        "shabda_bada": builtin_shabda_bada,
        "shabda_chhota": builtin_shabda_chhota,
        "shabda_trim": builtin_shabda_trim,
    }

    return {name: VakyaBuiltin(name, func) for name, func in builtins_map.items()}
