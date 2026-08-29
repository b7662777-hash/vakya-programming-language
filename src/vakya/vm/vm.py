"""High-Performance Bytecode Virtual Machine for the Vākya Programming Language."""

import os
import sys
from typing import Any, Dict, List, Optional, TextIO
from vakya.bytecode.chunk import Chunk
from vakya.bytecode.opcodes import OpCode
from vakya.bytecode.instructions import Instruction
from vakya.modules.loader import ModuleLoader
from .runtime import (
    VMClosure,
    VMBuiltin,
    UpvalueCell,
    is_truthy,
    vakya_str,
    vakya_typeof,
    create_vm_builtins,
)
from .frames import CallFrame
from .stack import ValueStack
from vakya.errors import (
    VakyaError,
    RuntimeError,
    IndexError,
    NameError,
    TypeError,
    ArgumentError,
    E101_UNDEFINED_VARIABLE,
    E102_UNDEFINED_FUNCTION,
    E301_DIVISION_BY_ZERO,
    E302_INDEX_OUT_OF_BOUNDS,
    E303_KEY_NOT_FOUND,
    E304_RECURSION_LIMIT,
    E305_NOT_CALLABLE,
    E306_RUNTIME_TYPE_ERROR,
    E307_INVALID_PROPERTY,
    E406_ARGUMENT_COUNT_MISMATCH,
    E407_NOT_INDEXABLE,
)

# Pre-extracted integer constants for high-speed dispatch
OP_CONSTANT = 1
OP_NULL = 2
OP_TRUE = 3
OP_FALSE = 4
OP_POP = 5
OP_DUP = 6
OP_LOAD_LOCAL = 7
OP_STORE_LOCAL = 8
OP_LOAD_GLOBAL = 9
OP_STORE_GLOBAL = 10
OP_LOAD_UPVALUE = 11
OP_STORE_UPVALUE = 12
OP_ADD = 13
OP_SUBTRACT = 14
OP_MULTIPLY = 15
OP_DIVIDE = 16
OP_MODULO = 17
OP_POWER = 18
OP_NEGATE = 19
OP_NOT = 20
OP_EQUAL = 21
OP_NOT_EQUAL = 22
OP_LESS = 23
OP_LESS_EQUAL = 24
OP_GREATER = 25
OP_GREATER_EQUAL = 26
OP_JUMP = 27
OP_JUMP_IF_FALSE = 28
OP_JUMP_IF_TRUE = 29
OP_JUMP_IF_FALSE_OR_POP = 30
OP_JUMP_IF_TRUE_OR_POP = 31
OP_MAKE_CLOSURE = 32
OP_CALL = 33
OP_CALL_BUILTIN = 34
OP_RETURN = 35
OP_BUILD_LIST = 36
OP_BUILD_MAP = 37
OP_INDEX = 38
OP_SET_INDEX = 39
OP_GET_MEMBER = 40
OP_HALT = 41
OP_IMPORT_MODULE = 42


class VirtualMachine:
    """Stack-based Virtual Machine with flat integer opcode dispatch and lightweight CallFrames."""

    def __init__(
        self,
        stdout: Optional[TextIO] = None,
        stdin: Optional[TextIO] = None,
        trace: bool = False,
        max_stack_size: int = 4096,
        max_call_depth: int = 200,
    ):
        self.stdout = stdout if stdout is not None else sys.stdout
        self.stdin = stdin if stdin is not None else sys.stdin
        self.trace = trace
        self.max_stack_size = max_stack_size
        self.max_call_depth = max_call_depth

        self.globals: Dict[str, Any] = {}
        self.module_loader = ModuleLoader()
        self.builtins: Dict[str, VMBuiltin] = create_vm_builtins(stdout=self.stdout, stdin=self.stdin)
        self.value_stack = ValueStack(max_size=max_stack_size)
        self.call_stack: List[CallFrame] = []

    def reset(self) -> None:
        self.value_stack.clear()
        self.call_stack.clear()
        self.globals.clear()

    def run(self, chunk: Chunk) -> Any:
        frame = CallFrame(chunk=chunk)
        self.call_stack = [frame]
        self.value_stack.clear()
        return self._run_frames()

    def _run_frames(self) -> Any:
        last_result: Any = None
        stack = self.value_stack.data
        stack_append = stack.append
        stack_pop = stack.pop
        call_stack = self.call_stack
        globals_dict = self.globals
        builtins_dict = self.builtins
        max_call_depth = self.max_call_depth
        trace = self.trace
        stdout = self.stdout

        while call_stack:
            frame = call_stack[-1]
            chunk = frame.chunk
            ops = chunk.code_ops
            args = chunk.code_args
            constants = chunk.constants
            num_ops = len(ops)

            while frame.ip < num_ops:
                ip = frame.ip
                op = ops[ip]
                arg = args[ip]
                frame.ip = ip + 1

                if trace:
                    stack_repr = [vakya_str(x) for x in stack]
                    op_name = OpCode(op).name if 1 <= op <= 41 else str(op)
                    print(f"[TRACE] IP={ip:04d} OP={op_name:<20} STACK={stack_repr}", file=stdout)

                try:
                    # 1. Constants & Literals
                    if op == OP_CONSTANT:
                        stack_append(constants[arg])

                    elif op == OP_NULL:
                        stack_append(None)

                    elif op == OP_TRUE:
                        stack_append(True)

                    elif op == OP_FALSE:
                        stack_append(False)

                    # 2. Local Variable Access
                    elif op == OP_LOAD_LOCAL:
                        if frame.open_upvalues and arg in frame.open_upvalues:
                            stack_append(frame.open_upvalues[arg].value)
                        else:
                            stack_append(frame.locals[arg])

                    elif op == OP_STORE_LOCAL:
                        val = stack_pop() if stack else None
                        if arg >= len(frame.locals):
                            frame.locals.extend([None] * (arg - len(frame.locals) + 1))
                        frame.locals[arg] = val
                        if frame.open_upvalues and arg in frame.open_upvalues:
                            frame.open_upvalues[arg].value = val

                    # 3. Global Variable Access
                    elif op == OP_LOAD_GLOBAL:
                        if arg in globals_dict:
                            stack_append(globals_dict[arg])
                        elif arg in builtins_dict:
                            stack_append(builtins_dict[arg])
                        else:
                            span = chunk.code_spans[ip]
                            raise NameError.from_info(
                                E101_UNDEFINED_VARIABLE,
                                f"Undefined variable or function '{arg}'",
                                filename=chunk.filename,
                                line=span.line if span else None,
                                column=span.column if span else None,
                                length=span.length if span else 1,
                                source_code=chunk.source_code,
                                help_text=f"Declare '{arg}' using 'chara' or 'karya' before using it.",
                            )

                    elif op == OP_STORE_GLOBAL:
                        globals_dict[arg] = stack_pop() if stack else None

                    # 4. Arithmetic Operations
                    elif op == OP_ADD:
                        b = stack_pop()
                        a = stack_pop()
                        if type(a) is int and type(b) is int:
                            stack_append(a + b)
                        elif type(a) is float and (type(b) is int or type(b) is float):
                            stack_append(a + b)
                        elif type(b) is float and type(a) is int:
                            stack_append(a + b)
                        elif isinstance(a, str) or isinstance(b, str):
                            stack_append(vakya_str(a) + vakya_str(b))
                        else:
                            span = chunk.code_spans[ip]
                            raise RuntimeError.from_info(
                                E306_RUNTIME_TYPE_ERROR,
                                f"Cannot add types '{vakya_typeof(a)}' and '{vakya_typeof(b)}'",
                                filename=chunk.filename,
                                line=span.line if span else None,
                                column=span.column if span else None,
                                length=span.length if span else 1,
                                source_code=chunk.source_code,
                            )

                    elif op == OP_SUBTRACT:
                        b = stack_pop()
                        a = stack_pop()
                        if type(a) is int and type(b) is int:
                            stack_append(a - b)
                        elif type(a) is float and (type(b) is int or type(b) is float):
                            stack_append(a - b)
                        elif type(b) is float and type(a) is int:
                            stack_append(a - b)
                        else:
                            span = chunk.code_spans[ip]
                            raise RuntimeError.from_info(
                                E306_RUNTIME_TYPE_ERROR,
                                f"Cannot subtract types '{vakya_typeof(a)}' and '{vakya_typeof(b)}'",
                                filename=chunk.filename,
                                line=span.line if span else None,
                                column=span.column if span else None,
                                length=span.length if span else 1,
                                source_code=chunk.source_code,
                            )

                    elif op == OP_MULTIPLY:
                        b = stack_pop()
                        a = stack_pop()
                        if type(a) is int and type(b) is int:
                            stack_append(a * b)
                        elif type(a) is float and (type(b) is int or type(b) is float):
                            stack_append(a * b)
                        elif type(b) is float and type(a) is int:
                            stack_append(a * b)
                        elif isinstance(a, str) and type(b) is int:
                            stack_append(a * b)
                        elif isinstance(b, str) and type(a) is int:
                            stack_append(b * a)
                        else:
                            span = chunk.code_spans[ip]
                            raise RuntimeError.from_info(
                                E306_RUNTIME_TYPE_ERROR,
                                f"Cannot multiply types '{vakya_typeof(a)}' and '{vakya_typeof(b)}'",
                                filename=chunk.filename,
                                line=span.line if span else None,
                                column=span.column if span else None,
                                length=span.length if span else 1,
                                source_code=chunk.source_code,
                            )

                    elif op == OP_DIVIDE:
                        b = stack_pop()
                        a = stack_pop()
                        if not ((type(a) is int or type(a) is float) and (type(b) is int or type(b) is float)):
                            span = chunk.code_spans[ip]
                            raise RuntimeError.from_info(
                                E306_RUNTIME_TYPE_ERROR,
                                f"Cannot divide types '{vakya_typeof(a)}' and '{vakya_typeof(b)}'",
                                filename=chunk.filename,
                                line=span.line if span else None,
                                column=span.column if span else None,
                                length=span.length if span else 1,
                                source_code=chunk.source_code,
                            )
                        if b == 0:
                            span = chunk.code_spans[ip]
                            raise RuntimeError.from_info(
                                E301_DIVISION_BY_ZERO,
                                "Division by zero",
                                filename=chunk.filename,
                                line=span.line if span else None,
                                column=span.column if span else None,
                                length=span.length if span else 1,
                                source_code=chunk.source_code,
                                help_text="Ensure the divisor is non-zero before dividing.",
                            )
                        if type(a) is int and type(b) is int and a % b == 0:
                            stack_append(a // b)
                        else:
                            stack_append(a / b)

                    elif op == OP_MODULO:
                        b = stack_pop()
                        a = stack_pop()
                        if not ((type(a) is int or type(a) is float) and (type(b) is int or type(b) is float)):
                            span = chunk.code_spans[ip]
                            raise RuntimeError.from_info(
                                E306_RUNTIME_TYPE_ERROR,
                                f"Cannot perform modulo on types '{vakya_typeof(a)}' and '{vakya_typeof(b)}'",
                                filename=chunk.filename,
                                line=span.line if span else None,
                                column=span.column if span else None,
                                length=span.length if span else 1,
                                source_code=chunk.source_code,
                            )
                        if b == 0:
                            span = chunk.code_spans[ip]
                            raise RuntimeError.from_info(
                                E301_DIVISION_BY_ZERO,
                                "Modulo by zero",
                                filename=chunk.filename,
                                line=span.line if span else None,
                                column=span.column if span else None,
                                length=span.length if span else 1,
                                source_code=chunk.source_code,
                                help_text="Ensure the divisor is non-zero before calculating modulo.",
                            )
                        stack_append(a % b)

                    elif op == OP_POWER:
                        b = stack_pop()
                        a = stack_pop()
                        if (type(a) is int or type(a) is float) and (type(b) is int or type(b) is float):
                            res = a ** b
                            if type(a) is int and type(b) is int and b >= 0:
                                stack_append(int(res))
                            else:
                                stack_append(res)
                        else:
                            span = chunk.code_spans[ip]
                            raise RuntimeError.from_info(
                                E306_RUNTIME_TYPE_ERROR,
                                f"Cannot raise type '{vakya_typeof(a)}' to power '{vakya_typeof(b)}'",
                                filename=chunk.filename,
                                line=span.line if span else None,
                                column=span.column if span else None,
                                length=span.length if span else 1,
                                source_code=chunk.source_code,
                            )

                    elif op == OP_NEGATE:
                        val = stack_pop()
                        if (type(val) is int or type(val) is float) and type(val) is not bool:
                            stack_append(-val)
                        else:
                            span = chunk.code_spans[ip]
                            raise RuntimeError.from_info(
                                E306_RUNTIME_TYPE_ERROR,
                                f"Cannot negate type '{vakya_typeof(val)}'",
                                filename=chunk.filename,
                                line=span.line if span else None,
                                column=span.column if span else None,
                                length=span.length if span else 1,
                                source_code=chunk.source_code,
                            )

                    elif op == OP_NOT:
                        val = stack_pop()
                        stack_append(not is_truthy(val))

                    # 5. Comparisons & Equality
                    elif op == OP_EQUAL:
                        b = stack_pop()
                        a = stack_pop()
                        if (type(a) is bool and type(b) is not bool) or (type(b) is bool and type(a) is not bool):
                            stack_append(False)
                        else:
                            stack_append(a == b)

                    elif op == OP_NOT_EQUAL:
                        b = stack_pop()
                        a = stack_pop()
                        if (type(a) is bool and type(b) is not bool) or (type(b) is bool and type(a) is not bool):
                            stack_append(True)
                        else:
                            stack_append(a != b)

                    elif op == OP_LESS:
                        b = stack_pop()
                        a = stack_pop()
                        stack_append(a < b)

                    elif op == OP_GREATER:
                        b = stack_pop()
                        a = stack_pop()
                        stack_append(a > b)

                    elif op == OP_LESS_EQUAL:
                        b = stack_pop()
                        a = stack_pop()
                        stack_append(a <= b)

                    elif op == OP_GREATER_EQUAL:
                        b = stack_pop()
                        a = stack_pop()
                        stack_append(a >= b)

                    # 6. Control Flow & Jumps
                    elif op == OP_JUMP:
                        frame.ip = arg

                    elif op == OP_JUMP_IF_FALSE:
                        val = stack_pop() if stack else None
                        if val is False or val is None or val == 0 or val == "":
                            frame.ip = arg
                        elif isinstance(val, (list, dict)) and len(val) == 0:
                            frame.ip = arg

                    elif op == OP_JUMP_IF_TRUE:
                        val = stack_pop() if stack else None
                        if val is True or (val and val != 0 and val != ""):
                            frame.ip = arg

                    elif op == OP_JUMP_IF_FALSE_OR_POP:
                        val = stack[-1] if stack else None
                        if not is_truthy(val):
                            frame.ip = arg
                        else:
                            stack_pop()

                    elif op == OP_JUMP_IF_TRUE_OR_POP:
                        val = stack[-1] if stack else None
                        if is_truthy(val):
                            frame.ip = arg
                        else:
                            stack_pop()

                    # 7. Stack Operations
                    elif op == OP_POP:
                        if stack:
                            stack_pop()

                    elif op == OP_DUP:
                        if stack:
                            stack_append(stack[-1])

                    # 8. Closures & Upvalues
                    elif op == OP_LOAD_UPVALUE:
                        if frame.closure and 0 <= arg < len(frame.closure.upvalues):
                            stack_append(frame.closure.upvalues[arg].value)
                        else:
                            stack_append(None)

                    elif op == OP_STORE_UPVALUE:
                        val = stack_pop() if stack else None
                        if frame.closure and 0 <= arg < len(frame.closure.upvalues):
                            frame.closure.upvalues[arg].value = val

                    elif op == OP_MAKE_CLOSURE:
                        fn_chunk = constants[arg]
                        upvalues = []
                        for is_local, index, _ in fn_chunk.upvalues:
                            if is_local:
                                cell = frame.capture_upvalue(index)
                            else:
                                cell = frame.closure.upvalues[index] if frame.closure else UpvalueCell(None)
                            upvalues.append(cell)
                        closure = VMClosure(chunk=fn_chunk, upvalues=upvalues)
                        stack_append(closure)

                    # 9. Function Calls
                    elif op == OP_CALL_BUILTIN:
                        name, argc = arg
                        args_list = [stack_pop() for _ in range(argc)]
                        args_list.reverse()

                        if name not in builtins_dict:
                            span = chunk.code_spans[ip]
                            raise NameError.from_info(
                                E102_UNDEFINED_FUNCTION,
                                f"Undefined builtin function '{name}'",
                                filename=chunk.filename,
                                line=span.line if span else None,
                                column=span.column if span else None,
                                length=span.length if span else 1,
                                source_code=chunk.source_code,
                            )
                        ret = builtins_dict[name].func(*args_list)
                        stack_append(ret)

                    elif op == OP_CALL:
                        argc = arg
                        args_list = [stack_pop() for _ in range(argc)]
                        args_list.reverse()
                        callee = stack_pop()

                        if isinstance(callee, VMBuiltin):
                            ret = callee.func(*args_list)
                            stack_append(ret)

                        elif callable(callee) and not isinstance(callee, VMClosure):
                            try:
                                ret = callee(*args_list)
                                stack_append(ret)
                            except VakyaError:
                                raise
                            except Exception as ex:
                                span = chunk.code_spans[ip]
                                raise RuntimeError.from_info(
                                    E306_RUNTIME_TYPE_ERROR,
                                    f"Error executing function: {ex}",
                                    filename=chunk.filename,
                                    line=span.line if span else None,
                                    column=span.column if span else None,
                                    length=span.length if span else 1,
                                    source_code=chunk.source_code,
                                )

                        elif isinstance(callee, VMClosure):
                            if len(call_stack) >= max_call_depth:
                                span = chunk.code_spans[ip]
                                raise RuntimeError.from_info(
                                    E304_RECURSION_LIMIT,
                                    "Maximum call stack recursion limit reached in Virtual Machine",
                                    filename=chunk.filename,
                                    line=span.line if span else None,
                                    column=span.column if span else None,
                                    length=span.length if span else 1,
                                    source_code=chunk.source_code,
                                    help_text="Check for unbounded recursion or missing base condition in your function.",
                                )

                            expected_argc = len(callee.chunk.param_names)
                            if argc != expected_argc:
                                span = chunk.code_spans[ip]
                                raise ArgumentError.from_info(
                                    E406_ARGUMENT_COUNT_MISMATCH,
                                    f"Function '{callee.name}' expects {expected_argc} argument(s), but received {argc}",
                                    filename=chunk.filename,
                                    line=span.line if span else None,
                                    column=span.column if span else None,
                                    length=span.length if span else 1,
                                    source_code=chunk.source_code,
                                )

                            new_frame = CallFrame(chunk=callee.chunk, closure=callee)
                            for i, a_val in enumerate(args_list):
                                new_frame.locals[i] = a_val
                            call_stack.append(new_frame)
                            break  # Switch to new top frame

                        else:
                            span = chunk.code_spans[ip]
                            raise RuntimeError.from_info(
                                E305_NOT_CALLABLE,
                                f"Value of type '{vakya_typeof(callee)}' is not callable",
                                filename=chunk.filename,
                                line=span.line if span else None,
                                column=span.column if span else None,
                                length=span.length if span else 1,
                                source_code=chunk.source_code,
                            )

                    elif op == OP_RETURN:
                        ret_val = stack_pop() if stack else None
                        call_stack.pop()
                        if call_stack:
                            stack_append(ret_val)
                            break  # Return to caller frame
                        else:
                            last_result = ret_val
                            return last_result

                    # 10. Collections & Indexing
                    elif op == OP_BUILD_LIST:
                        count = arg
                        elements = [stack_pop() for _ in range(count)]
                        elements.reverse()
                        stack_append(elements)

                    elif op == OP_BUILD_MAP:
                        count = arg
                        pairs = [(stack_pop(), stack_pop()) for _ in range(count)]
                        pairs.reverse()
                        map_dict = {str(k): v for v, k in pairs}
                        stack_append(map_dict)

                    elif op == OP_INDEX:
                        idx = stack_pop()
                        target = stack_pop()
                        if isinstance(target, list):
                            if type(idx) is not int or type(idx) is bool:
                                span = chunk.code_spans[ip]
                                raise IndexError.from_info(
                                    E302_INDEX_OUT_OF_BOUNDS,
                                    f"List index must be an integer, got '{vakya_typeof(idx)}'",
                                    filename=chunk.filename,
                                    line=span.line if span else None,
                                    column=span.column if span else None,
                                    length=span.length if span else 1,
                                    source_code=chunk.source_code,
                                )
                            if idx < 0 or idx >= len(target):
                                span = chunk.code_spans[ip]
                                raise IndexError.from_info(
                                    E302_INDEX_OUT_OF_BOUNDS,
                                    f"Index {idx} out of range for list of length {len(target)}",
                                    filename=chunk.filename,
                                    line=span.line if span else None,
                                    column=span.column if span else None,
                                    length=span.length if span else 1,
                                    source_code=chunk.source_code,
                                )
                            stack_append(target[idx])

                        elif isinstance(target, dict):
                            key_str = str(idx)
                            if key_str not in target:
                                span = chunk.code_spans[ip]
                                raise RuntimeError.from_info(
                                    E303_KEY_NOT_FOUND,
                                    f"Key '{key_str}' not found in map",
                                    filename=chunk.filename,
                                    line=span.line if span else None,
                                    column=span.column if span else None,
                                    length=span.length if span else 1,
                                    source_code=chunk.source_code,
                                )
                            stack_append(target[key_str])

                        elif isinstance(target, str):
                            if type(idx) is not int or type(idx) is bool:
                                span = chunk.code_spans[ip]
                                raise IndexError.from_info(
                                    E302_INDEX_OUT_OF_BOUNDS,
                                    f"String index must be an integer, got '{vakya_typeof(idx)}'",
                                    filename=chunk.filename,
                                    line=span.line if span else None,
                                    column=span.column if span else None,
                                    length=span.length if span else 1,
                                    source_code=chunk.source_code,
                                )
                            if idx < 0 or idx >= len(target):
                                span = chunk.code_spans[ip]
                                raise IndexError.from_info(
                                    E302_INDEX_OUT_OF_BOUNDS,
                                    f"Index {idx} out of range for string of length {len(target)}",
                                    filename=chunk.filename,
                                    line=span.line if span else None,
                                    column=span.column if span else None,
                                    length=span.length if span else 1,
                                    source_code=chunk.source_code,
                                )
                            stack_append(target[idx])
                        else:
                            span = chunk.code_spans[ip]
                            raise TypeError.from_info(
                                E407_NOT_INDEXABLE,
                                f"Type '{vakya_typeof(target)}' is not indexable",
                                filename=chunk.filename,
                                line=span.line if span else None,
                                column=span.column if span else None,
                                length=span.length if span else 1,
                                source_code=chunk.source_code,
                            )

                    elif op == OP_SET_INDEX:
                        val = stack_pop()
                        idx = stack_pop()
                        target = stack_pop()
                        if isinstance(target, list):
                            if type(idx) is not int or type(idx) is bool:
                                span = chunk.code_spans[ip]
                                raise IndexError.from_info(
                                    E302_INDEX_OUT_OF_BOUNDS,
                                    f"List index must be an integer, got '{vakya_typeof(idx)}'",
                                    filename=chunk.filename,
                                    line=span.line if span else None,
                                    column=span.column if span else None,
                                    length=span.length if span else 1,
                                    source_code=chunk.source_code,
                                )
                            if idx < 0 or idx >= len(target):
                                span = chunk.code_spans[ip]
                                raise IndexError.from_info(
                                    E302_INDEX_OUT_OF_BOUNDS,
                                    f"Index {idx} out of range for list of length {len(target)}",
                                    filename=chunk.filename,
                                    line=span.line if span else None,
                                    column=span.column if span else None,
                                    length=span.length if span else 1,
                                    source_code=chunk.source_code,
                                )
                            target[idx] = val

                        elif isinstance(target, dict):
                            target[str(idx)] = val
                        else:
                            span = chunk.code_spans[ip]
                            raise TypeError.from_info(
                                E407_NOT_INDEXABLE,
                                f"Type '{vakya_typeof(target)}' is not indexable for assignment",
                                filename=chunk.filename,
                                line=span.line if span else None,
                                column=span.column if span else None,
                                length=span.length if span else 1,
                                source_code=chunk.source_code,
                            )

                    elif op == OP_GET_MEMBER:
                        member_name = arg
                        target = stack_pop()
                        if member_name == "length":
                            if isinstance(target, (list, dict, str)):
                                stack_append(len(target))
                            else:
                                span = chunk.code_spans[ip]
                                raise RuntimeError.from_info(
                                    E307_INVALID_PROPERTY,
                                    f"Property '.length' is not supported on type '{vakya_typeof(target)}'",
                                    filename=chunk.filename,
                                    line=span.line if span else None,
                                    column=span.column if span else None,
                                    length=span.length if span else 1,
                                    source_code=chunk.source_code,
                                )
                        elif isinstance(target, dict) and member_name in target:
                            stack_append(target[member_name])
                        else:
                            span = chunk.code_spans[ip]
                            raise RuntimeError.from_info(
                                E307_INVALID_PROPERTY,
                                f"Unknown property '.{member_name}' on type '{vakya_typeof(target)}'",
                                filename=chunk.filename,
                                line=span.line if span else None,
                                column=span.column if span else None,
                                length=span.length if span else 1,
                                source_code=chunk.source_code,
                            )

                    elif op == OP_IMPORT_MODULE:
                        mod_name, bind_name = arg
                        base_dir = os.path.dirname(chunk.filename) if chunk.filename and chunk.filename != "<anonymous>" else None
                        symbols = self.module_loader.load_module(mod_name, base_dir=base_dir)
                        self.globals[bind_name] = symbols

                    elif op == OP_HALT:
                        last_result = stack_pop() if stack else None
                        call_stack.clear()
                        return last_result

                except VakyaError:
                    raise
                except RecursionError:
                    span = chunk.code_spans[ip]
                    raise RuntimeError.from_info(
                        E304_RECURSION_LIMIT,
                        "Maximum call stack recursion limit reached in Virtual Machine",
                        filename=chunk.filename,
                        line=span.line if span else None,
                        column=span.column if span else None,
                        length=span.length if span else 1,
                        source_code=chunk.source_code,
                        help_text="Check for unbounded recursion or missing base condition in your function.",
                    )

            if call_stack and call_stack[-1] is frame and frame.ip >= num_ops:
                call_stack.pop()

        return last_result
