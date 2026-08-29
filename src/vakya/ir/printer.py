"""Vākya IR Disassembler / Formatter."""

from .builder import IRModule, IRFunction


class IRPrinter:
    """Formats an IRModule or IRFunction into readable linear IR disassembly."""

    @classmethod
    def print_module(cls, module: IRModule) -> str:
        lines = [f"; === VAKYA IR MODULE: {module.name} ===", ""]

        # Functions
        for fn_name, fn in module.functions.items():
            lines.extend(cls._format_function(fn))
            lines.append("")

        # Top-level entry
        lines.extend(cls._format_function(module.top_level))
        return "\n".join(lines)

    @classmethod
    def _format_function(cls, fn: IRFunction) -> list:
        params_str = ", ".join(f"%p_{p}" for p in fn.params)
        lines = [f"define @{fn.name}({params_str}) {{"]
        for instr in fn.instructions:
            if hasattr(instr, "name") and instr.__class__.__name__ == "IRLabel":
                lines.append(f"{instr.name}:")
            else:
                lines.append(f"    {str(instr)}")
        lines.append("}")
        return lines
