"""Native compilation pipeline for Vākya."""

import os
import shutil
import subprocess
from typing import Optional, Tuple
from vakya.lexer.lexer import Lexer
from vakya.parser.parser import Parser
from vakya.typechecker.checker import TypeChecker
from vakya.typechecker.borrow_checker import BorrowChecker
from vakya.ir.builder import IRBuilder
from .c_emitter import NativeCEmitter
from .llvm_backend import LLVMEmitter


class NativeCompiler:
    """Orchestrates source -> AST -> Type/Borrow Checking -> IR -> Backend -> Binary."""

    def __init__(self, filename: str = "<anonymous>", backend: str = "c"):
        self.filename = filename
        self.backend = backend  # "c" or "llvm"

    def compile_ir(self, source_code: str):
        tokens = Lexer(source_code, filename=self.filename).tokenize()
        ast = Parser(tokens, filename=self.filename, source_code=source_code).parse()
        TypeChecker(filename=self.filename, source_code=source_code).check(ast)
        BorrowChecker(filename=self.filename, source_code=source_code).check(ast)

        builder = IRBuilder(filename=self.filename)
        return builder.build(ast)

    def compile_to_c(self, source_code: str) -> str:
        ir_module = self.compile_ir(source_code)
        emitter = NativeCEmitter(ir_module)
        return emitter.emit_c()

    def compile_to_llvm(self, source_code: str) -> str:
        ir_module = self.compile_ir(source_code)
        emitter = LLVMEmitter(ir_module)
        return emitter.emit_llvm_ir()

    def build_executable(self, source_code: str, output_path: str) -> Tuple[bool, str]:
        if self.backend == "llvm":
            llvm_code = self.compile_to_llvm(source_code)
            ll_file = f"{output_path}.ll"
            with open(ll_file, "w", encoding="utf-8") as f:
                f.write(llvm_code)

            clang = shutil.which("clang")
            if not clang:
                return False, f"LLVM IR generated at '{ll_file}'. Host 'clang' compiler not found on PATH."

            try:
                cmd = [clang, "-O3", ll_file, "-o", output_path]
                res = subprocess.run(cmd, capture_output=True, text=True)
                if res.returncode != 0:
                    return False, f"Clang LLVM compilation failed:\n{res.stderr}"
                return True, f"Native binary compiled via LLVM: '{output_path}'"
            except Exception as e:
                return False, f"Failed to invoke clang: {e}"

        # Default C backend
        c_code = self.compile_to_c(source_code)
        c_file = f"{output_path}.c"

        with open(c_file, "w", encoding="utf-8") as f:
            f.write(c_code)

        cc = shutil.which("gcc") or shutil.which("clang") or shutil.which("cl") or shutil.which("tcc")
        if not cc:
            return False, f"C source generated at '{c_file}'. No host C compiler (gcc/clang/cl) found to generate executable."

        try:
            if "cl" in os.path.basename(cc).lower():
                cmd = [cc, c_file, f"/Fe:{output_path}"]
            else:
                cmd = [cc, "-O3", c_file, "-o", output_path]

            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode != 0:
                return False, f"C compilation failed:\n{res.stderr}"
            return True, f"Native binary compiled successfully: '{output_path}'"
        except Exception as e:
            return False, f"Failed to invoke C compiler: {e}"
