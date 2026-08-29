"""C99 Native Code Emitter for Vākya Intermediate Representation (IR)."""

import os
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


RUNTIME_EMBEDDED = """/* Embedded Vākya Native Runtime Header */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <math.h>

typedef int64_t vakya_int;
typedef double vakya_float;
typedef bool vakya_bool;

typedef struct {
    char* data;
    size_t length;
} VakyaString;

typedef struct {
    int64_t* items;
    size_t length;
    size_t capacity;
} VakyaList;

static inline void vakya_panic(const char* code, const char* msg) {
    fprintf(stderr, "\\nError [%s]: %s\\n\\n", code, msg);
    exit(1);
}

static inline void* vakya_alloc(size_t sz) {
    void* p = malloc(sz);
    if (!p && sz > 0) vakya_panic("E304", "Out of memory");
    return p;
}

static inline VakyaList* vakya_list_new(size_t cap) {
    VakyaList* l = (VakyaList*)vakya_alloc(sizeof(VakyaList));
    l->length = 0;
    l->capacity = cap > 4 ? cap : 4;
    l->items = (int64_t*)vakya_alloc(l->capacity * sizeof(int64_t));
    return l;
}

static inline void vakya_list_push(VakyaList* l, int64_t v) {
    if (l->length >= l->capacity) {
        l->capacity *= 2;
        l->items = (int64_t*)realloc(l->items, l->capacity * sizeof(int64_t));
    }
    l->items[l->length++] = v;
}

static inline int64_t vakya_list_get(const VakyaList* l, int64_t idx) {
    if (idx < 0 || (size_t)idx >= l->length) vakya_panic("E302", "List index out of bounds");
    return l->items[idx];
}

static inline void vakya_list_set(VakyaList* l, int64_t idx, int64_t v) {
    if (idx < 0 || (size_t)idx >= l->length) vakya_panic("E302", "List index out of bounds");
    l->items[idx] = v;
}

static inline void vada_int(int64_t x) { printf("%lld\\n", (long long)x); }
static inline void vada_float(double x) { printf("%g\\n", x); }
static inline void vada_str(const char* x) { printf("%s\\n", x ? x : "shunya"); }
static inline void vada_bool(bool x) { printf("%s\\n", x ? "satya" : "asatya"); }
static inline void vada_list(const VakyaList* l) {
    if (!l) { printf("[]\\n"); return; }
    printf("[");
    for (size_t i = 0; i < l->length; ++i) {
        if (i > 0) printf(", ");
        printf("%lld", (long long)l->items[i]);
    }
    printf("]\\n");
}

"""


class NativeCEmitter:
    """Translates Vākya IR into optimized C99 source code."""

    def __init__(self, module: IRModule):
        self.module = module
        self.temp_types: Dict[str, str] = {}

    def emit_c(self) -> str:
        lines = [RUNTIME_EMBEDDED]

        # Function forward declarations
        for fn_name, fn in self.module.functions.items():
            params = ", ".join(f"vakya_int {p}" for p in fn.params) if fn.params else "void"
            lines.append(f"vakya_int {fn_name}({params});")
        lines.append("")

        # Function definitions
        for fn_name, fn in self.module.functions.items():
            lines.extend(self._emit_function(fn))
            lines.append("")

        # Main entrypoint
        lines.append("int main(int argc, char** argv) {")
        for line in self._emit_function_body(self.module.top_level):
            lines.append(f"    {line}")
        lines.append("    return 0;")
        lines.append("}")

        return "\n".join(lines)

    def _emit_function(self, fn: IRFunction) -> List[str]:
        params = ", ".join(f"vakya_int {p}" for p in fn.params) if fn.params else "void"
        lines = [f"vakya_int {fn.name}({params}) {{"]
        for line in self._emit_function_body(fn):
            lines.append(f"    {line}")
        lines.append("}")
        return lines

    def _emit_function_body(self, fn: IRFunction) -> List[str]:
        body_lines: List[str] = []
        declared_temps: Set[str] = set()
        declared_vars: Set[str] = set()

        for instr in fn.instructions:
            if isinstance(instr, IRConst):
                t_name = self._c_ident(instr.dest)
                if t_name not in declared_temps:
                    declared_temps.add(t_name)
                    if instr.val_type == "shabda":
                        body_lines.append(f'const char* {t_name} = "{instr.value}";')
                    elif instr.val_type == "dashamika":
                        body_lines.append(f"vakya_float {t_name} = {instr.value};")
                    elif instr.val_type == "boolean":
                        body_lines.append(f"vakya_bool {t_name} = {'true' if instr.value else 'false'};")
                    else:
                        body_lines.append(f"vakya_int {t_name} = {instr.value};")

            elif isinstance(instr, IRLoad):
                t_name = self._c_ident(instr.dest)
                v_name = self._c_ident(instr.var_name)
                if t_name not in declared_temps:
                    declared_temps.add(t_name)
                    body_lines.append(f"vakya_int {t_name} = {v_name};")
                else:
                    body_lines.append(f"{t_name} = {v_name};")

            elif isinstance(instr, IRStore):
                v_name = self._c_ident(instr.var_name)
                src = self._c_ident(instr.src)
                if v_name not in declared_vars:
                    declared_vars.add(v_name)
                    body_lines.append(f"vakya_int {v_name} = {src};")
                else:
                    body_lines.append(f"{v_name} = {src};")

            elif isinstance(instr, IRBinOp):
                t_name = self._c_ident(instr.dest)
                l = self._c_ident(instr.left)
                r = self._c_ident(instr.right)
                if instr.op == "pow":
                    if t_name not in declared_temps:
                        declared_temps.add(t_name)
                        body_lines.append(f"vakya_int {t_name} = (vakya_int)pow((double){l}, (double){r});")
                    else:
                        body_lines.append(f"{t_name} = (vakya_int)pow((double){l}, (double){r});")
                else:
                    op_map = {
                        "add": "+", "sub": "-", "mul": "*", "div": "/", "mod": "%",
                        "eq": "==", "ne": "!=", "lt": "<", "le": "<=", "gt": ">", "ge": ">=",
                        "and": "&&", "or": "||"
                    }
                    c_op = op_map.get(instr.op, "+")
                    if t_name not in declared_temps:
                        declared_temps.add(t_name)
                        body_lines.append(f"vakya_int {t_name} = {l} {c_op} {r};")
                    else:
                        body_lines.append(f"{t_name} = {l} {c_op} {r};")

            elif isinstance(instr, IRUnaryOp):
                t_name = self._c_ident(instr.dest)
                src = self._c_ident(instr.src)
                c_op = "-" if instr.op == "neg" else "!"
                if t_name not in declared_temps:
                    declared_temps.add(t_name)
                    body_lines.append(f"vakya_int {t_name} = {c_op}({src});")
                else:
                    body_lines.append(f"{t_name} = {c_op}({src});")

            elif isinstance(instr, IRLabel):
                body_lines.append(f"{instr.name}:")

            elif isinstance(instr, IRJump):
                body_lines.append(f"goto {instr.target};")

            elif isinstance(instr, IRBranch):
                c = self._c_ident(instr.cond)
                body_lines.append(f"if ({c}) goto {instr.true_target}; else goto {instr.false_target};")

            elif isinstance(instr, IRAllocList):
                t_name = self._c_ident(instr.dest)
                if t_name not in declared_temps:
                    declared_temps.add(t_name)
                    body_lines.append(f"VakyaList* {t_name} = vakya_list_new({len(instr.elements)});")
                else:
                    body_lines.append(f"{t_name} = vakya_list_new({len(instr.elements)});")
                for elem in instr.elements:
                    body_lines.append(f"vakya_list_push({t_name}, {self._c_ident(elem)});")

            elif isinstance(instr, IRGetIndex):
                t_name = self._c_ident(instr.dest)
                tgt = self._c_ident(instr.target)
                idx = self._c_ident(instr.index)
                if t_name not in declared_temps:
                    declared_temps.add(t_name)
                    body_lines.append(f"vakya_int {t_name} = vakya_list_get((VakyaList*){tgt}, {idx});")
                else:
                    body_lines.append(f"{t_name} = vakya_list_get((VakyaList*){tgt}, {idx});")

            elif isinstance(instr, IRSetIndex):
                tgt = self._c_ident(instr.target)
                idx = self._c_ident(instr.index)
                val = self._c_ident(instr.val)
                body_lines.append(f"vakya_list_set((VakyaList*){tgt}, {idx}, {val});")

            elif isinstance(instr, IRCall):
                args_str = ", ".join(self._c_ident(a) for a in instr.args)
                if instr.callee == "vada":
                    arg = self._c_ident(instr.args[0]) if instr.args else "0"
                    body_lines.append(f"vada_int({arg});")
                else:
                    if instr.dest:
                        t_name = self._c_ident(instr.dest)
                        if t_name not in declared_temps:
                            declared_temps.add(t_name)
                            body_lines.append(f"vakya_int {t_name} = {instr.callee}({args_str});")
                        else:
                            body_lines.append(f"{t_name} = {instr.callee}({args_str});")
                    else:
                        body_lines.append(f"{instr.callee}({args_str});")

            elif isinstance(instr, IRReturn):
                if instr.val:
                    body_lines.append(f"return {self._c_ident(instr.val)};")
                else:
                    body_lines.append("return 0;")

        return body_lines

    def _c_ident(self, name: str) -> str:
        if name.startswith("%"):
            return name[1:]
        return name
