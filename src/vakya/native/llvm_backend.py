"""Text LLVM IR Emitter for Vākya Intermediate Representation (IR)."""

from typing import Dict, List, Optional, Set
from vakya.ir.builder import IRModule, IRFunction
from vakya.ir.instructions import (
    IRInstruction,
    IRConst,
    IRLoad,
    IRStore,
    IRBinOp,
    IRUnaryOp,
    IRLabel,
    IRJump,
    IRBranch,
    IRCall,
    IRReturn,
    IRAllocList,
    IRAllocMap,
    IRGetIndex,
    IRSetIndex,
)


LLVM_HEADER = """; ModuleID = 'vakya_module'
source_filename = "vakya"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"

%VakyaList = type opaque

declare void @vada_int(i64)
declare void @vada_float(double)
declare void @vada_str(i8*)
declare void @vada_bool(i1)
declare %VakyaList* @vakya_list_new(i64)
declare void @vakya_list_push(%VakyaList*, i64)
declare i64 @vakya_list_get(%VakyaList*, i64)
declare void @vakya_list_set(%VakyaList*, i64, i64)
declare double @pow(double, double)

"""


class LLVMEmitter:
    """Translates Vākya IR into standard textual LLVM IR (.ll)."""

    def __init__(self, module: IRModule):
        self.module = module
        self.str_literals: List[str] = []

    def emit_llvm_ir(self) -> str:
        lines = [LLVM_HEADER]

        # String constants pool
        for idx, s in enumerate(self.str_literals):
            escaped = s.replace("\\", "\\5C").replace("\n", "\\0A").replace('"', '\\22')
            length = len(s.encode("utf-8")) + 1
            lines.append(f'@.str.{idx} = private unnamed_addr constant [{length} x i8] c"{escaped}\\00", align 1')
        if self.str_literals:
            lines.append("")

        # Function definitions
        for fn_name, fn in self.module.functions.items():
            lines.extend(self._emit_function(fn))
            lines.append("")

        # Main function
        lines.append("define i32 @main(i32 %argc, i8** %argv) {")
        lines.append("entry:")
        for line in self._emit_function_body(self.module.top_level):
            lines.append(f"    {line}")
        lines.append("    ret i32 0")
        lines.append("}")

        return "\n".join(lines)

    def _emit_function(self, fn: IRFunction) -> List[str]:
        params_sig = ", ".join(f"i64 %{p}" for p in fn.params) if fn.params else ""
        lines = [f"define i64 @{fn.name}({params_sig}) {{", "entry:"]
        for line in self._emit_function_body(fn):
            lines.append(f"    {line}")
        lines.append("}")
        return lines

    def _emit_function_body(self, fn: IRFunction) -> List[str]:
        body_lines: List[str] = []
        allocated_vars: Set[str] = set()

        for instr in fn.instructions:
            if isinstance(instr, IRConst):
                t = self._llvm_temp(instr.dest)
                if instr.val_type == "sankhya":
                    body_lines.append(f"{t} = add i64 0, {instr.value}")
                elif instr.val_type == "boolean":
                    val = "1" if instr.value else "0"
                    body_lines.append(f"{t} = add i1 0, {val}")
                else:
                    body_lines.append(f"{t} = add i64 0, 0")

            elif isinstance(instr, IRLoad):
                t = self._llvm_temp(instr.dest)
                v = self._llvm_var(instr.var_name)
                body_lines.append(f"{t} = load i64, i64* {v}")

            elif isinstance(instr, IRStore):
                v = self._llvm_var(instr.var_name)
                if instr.var_name not in allocated_vars:
                    allocated_vars.add(instr.var_name)
                    body_lines.insert(0, f"{v} = alloca i64, align 8")
                src = self._llvm_temp(instr.src)
                body_lines.append(f"store i64 {src}, i64* {v}")

            elif isinstance(instr, IRBinOp):
                t = self._llvm_temp(instr.dest)
                l = self._llvm_temp(instr.left)
                r = self._llvm_temp(instr.right)
                op_map = {
                    "add": "add nsw i64",
                    "sub": "sub nsw i64",
                    "mul": "mul nsw i64",
                    "div": "sdiv i64",
                    "mod": "srem i64",
                    "eq": "icmp eq i64",
                    "ne": "icmp ne i64",
                    "lt": "icmp slt i64",
                    "le": "icmp sle i64",
                    "gt": "icmp sgt i64",
                    "ge": "icmp sge i64",
                }
                llvm_op = op_map.get(instr.op, "add nsw i64")
                if llvm_op.startswith("icmp"):
                    cmp_temp = f"{t}_cmp"
                    body_lines.append(f"{cmp_temp} = {llvm_op} {l}, {r}")
                    body_lines.append(f"{t} = zext i1 {cmp_temp} to i64")
                else:
                    body_lines.append(f"{t} = {llvm_op} {l}, {r}")

            elif isinstance(instr, IRUnaryOp):
                t = self._llvm_temp(instr.dest)
                src = self._llvm_temp(instr.src)
                if instr.op == "neg":
                    body_lines.append(f"{t} = sub nsw i64 0, {src}")
                else:
                    body_lines.append(f"{t} = xor i64 {src}, 1")

            elif isinstance(instr, IRLabel):
                body_lines.append(f"{instr.name}:")

            elif isinstance(instr, IRJump):
                body_lines.append(f"br label %{instr.target}")

            elif isinstance(instr, IRBranch):
                c = self._llvm_temp(instr.cond)
                cond_i1 = f"{c}_i1"
                body_lines.append(f"{cond_i1} = trunc i64 {c} to i1")
                body_lines.append(f"br i1 {cond_i1}, label %{instr.true_target}, label %{instr.false_target}")

            elif isinstance(instr, IRCall):
                if instr.callee == "vada":
                    arg = self._llvm_temp(instr.args[0]) if instr.args else "0"
                    body_lines.append(f"call void @vada_int(i64 {arg})")
                else:
                    args_str = ", ".join(f"i64 {self._llvm_temp(a)}" for a in instr.args)
                    if instr.dest:
                        t = self._llvm_temp(instr.dest)
                        body_lines.append(f"{t} = call i64 @{instr.callee}({args_str})")
                    else:
                        body_lines.append(f"call i64 @{instr.callee}({args_str})")

            elif isinstance(instr, IRReturn):
                if instr.val:
                    body_lines.append(f"ret i64 {self._llvm_temp(instr.val)}")
                else:
                    body_lines.append("ret i64 0")

        return body_lines

    def _llvm_temp(self, name: str) -> str:
        if name.startswith("%"):
            return name
        return f"%{name}"

    def _llvm_var(self, name: str) -> str:
        return f"%var_{name}"
