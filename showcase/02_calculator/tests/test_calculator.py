"""Unit tests for Showcase Project 02 (Calculator Engine)."""

import io
import os
import unittest
from vakya.lexer.lexer import Lexer
from vakya.parser.parser import Parser
from vakya.typechecker.checker import TypeChecker
from vakya.bytecode.compiler import BytecodeCompiler
from vakya.vm.vm import VirtualMachine
from vakya.interpreter.interpreter import Interpreter


class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.script_path = os.path.join(os.path.dirname(__file__), "..", "vakya", "calculator.vakya")
        with open(self.script_path, "r", encoding="utf-8") as f:
            self.source_code = f.read()

    def run_vakya_code(self, code: str, engine: str = "vm") -> str:
        tokens = Lexer(code, filename="calculator_test.vakya").tokenize()
        ast = Parser(tokens, source_code=code, filename="calculator_test.vakya").parse()
        TypeChecker(source_code=code, filename="calculator_test.vakya").check(ast)

        stdout_stream = io.StringIO()
        if engine == "vm":
            chunk = BytecodeCompiler(source_code=code, filename="calculator_test.vakya").compile(ast)
            vm = VirtualMachine(stdout=stdout_stream)
            vm.run(chunk)
        else:
            interpreter = Interpreter(source_code=code, filename="calculator_test.vakya", stdout=stdout_stream)
            interpreter.interpret(ast)

        return stdout_stream.getvalue().strip()

    def test_calculator_operations_vm(self):
        code = self.source_code + '\nvada(ganana(100.0, 25.0, "+"))\nvada(ganana(100.0, 25.0, "-"))\nvada(ganana(10.0, 5.0, "*"))\nvada(ganana(100.0, 4.0, "/"))\nvada(ganana(2.0, 4.0, "**"))'
        out = self.run_vakya_code(code, engine="vm")
        self.assertIn("125.0", out)
        self.assertIn("75.0", out)
        self.assertIn("50.0", out)
        self.assertIn("25.0", out)
        self.assertIn("16.0", out)

    def test_calculator_operations_interpreter(self):
        code = self.source_code + '\nvada(ganana(50.0, 50.0, "+"))'
        out = self.run_vakya_code(code, engine="interpreter")
        self.assertIn("100.0", out)

    def test_calculator_division_by_zero(self):
        code = self.source_code + '\nchara res = ganana(42.0, 0.0, "/")\nvada("Zero result:", res)'
        out = self.run_vakya_code(code, engine="vm")
        self.assertIn("Dosha: Shunya se bhaga sambhava nahi hai", out)
        self.assertIn("Zero result: shunya", out)

    def test_calculator_modulo_by_zero(self):
        code = self.source_code + '\nchara res = ganana(42.0, 0.0, "%")\nvada("Modulo zero:", res)'
        out = self.run_vakya_code(code, engine="vm")
        self.assertIn("Dosha: Shunya se modulo sambhava nahi hai", out)
        self.assertIn("Modulo zero: shunya", out)


if __name__ == "__main__":
    unittest.main()
