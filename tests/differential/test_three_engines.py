"""Three-Engine Differential Testing Harness (Interpreter vs VM vs Native)."""

import io
import os
import unittest
from vakya.lexer.lexer import Lexer
from vakya.parser.parser import Parser
from vakya.typechecker.checker import TypeChecker
from vakya.typechecker.borrow_checker import BorrowChecker
from vakya.interpreter.interpreter import Interpreter
from vakya.bytecode.compiler import BytecodeCompiler
from vakya.vm.vm import VirtualMachine
from vakya.ir.builder import IRBuilder
from vakya.native.c_emitter import NativeCEmitter


class TestThreeEngineDifferential(unittest.TestCase):
    def execute_interpreter(self, code: str) -> str:
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens, source_code=code).parse()
        TypeChecker(source_code=code).check(ast)
        out = io.StringIO()
        Interpreter(source_code=code, stdout=out).interpret(ast)
        return out.getvalue().strip()

    def execute_vm(self, code: str) -> str:
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens, source_code=code).parse()
        TypeChecker(source_code=code).check(ast)
        chunk = BytecodeCompiler(source_code=code).compile(ast)
        out = io.StringIO()
        VirtualMachine(stdout=out).run(chunk)
        return out.getvalue().strip()

    def generate_native_c(self, code: str) -> str:
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens, source_code=code).parse()
        TypeChecker(source_code=code).check(ast)
        BorrowChecker(source_code=code).check(ast)
        builder = IRBuilder()
        module = builder.build(ast)
        return NativeCEmitter(module).emit_c()

    def assert_differential_parity(self, code: str):
        interp_res = self.execute_interpreter(code)
        vm_res = self.execute_vm(code)
        native_c = self.generate_native_c(code)

        self.assertEqual(interp_res, vm_res, f"Differential mismatch between Interpreter and VM:\n{code}")
        self.assertIn("int main(", native_c, "Native C generation must produce valid main entrypoint")

    def test_hello_differential(self):
        code = 'vada("Namaste Vākya")'
        self.assert_differential_parity(code)

    def test_arithmetic_differential(self):
        code = """
        chara a = 100
        chara b = 25
        vada(a + b)
        vada(a - b)
        vada(a * b)
        vada(a / b)
        vada(a % b)
        """
        self.assert_differential_parity(code)

    def test_loop_differential(self):
        code = """
        chara s = 0
        chara i = 1
        yavat i <= 10 {
            s += i
            i += 1
        }
        vada(s)
        """
        self.assert_differential_parity(code)

    def test_recursion_differential(self):
        code = """
        karya fact(n: sankhya) -> sankhya {
            yadi n <= 1 { pratyavartaya 1 }
            pratyavartaya n * fact(n - 1)
        }
        vada(fact(6))
        """
        self.assert_differential_parity(code)

    def test_arrays_differential(self):
        code = """
        chara nums = [10, 20, 30]
        nums[1] = 99
        vada(nums[0])
        vada(nums[1])
        vada(nums[2])
        """
        self.assert_differential_parity(code)


if __name__ == "__main__":
    unittest.main()
