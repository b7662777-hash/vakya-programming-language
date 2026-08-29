"""Unit tests for Showcase Project 01 (Name Program)."""

import io
import os
import unittest
from vakya.lexer.lexer import Lexer
from vakya.parser.parser import Parser
from vakya.typechecker.checker import TypeChecker
from vakya.bytecode.compiler import BytecodeCompiler
from vakya.vm.vm import VirtualMachine
from vakya.interpreter.interpreter import Interpreter


class TestNameProgram(unittest.TestCase):
    def setUp(self):
        self.script_path = os.path.join(os.path.dirname(__file__), "..", "main.vakya")
        with open(self.script_path, "r", encoding="utf-8") as f:
            self.source_code = f.read()

    def run_program(self, input_text: str, engine: str = "vm") -> str:
        tokens = Lexer(self.source_code, filename="main.vakya").tokenize()
        ast = Parser(tokens, source_code=self.source_code, filename="main.vakya").parse()
        TypeChecker(source_code=self.source_code, filename="main.vakya").check(ast)

        stdin_stream = io.StringIO(input_text + "\n")
        stdout_stream = io.StringIO()

        if engine == "vm":
            chunk = BytecodeCompiler(source_code=self.source_code, filename="main.vakya").compile(ast)
            vm = VirtualMachine(stdout=stdout_stream, stdin=stdin_stream)
            vm.run(chunk)
        else:
            interpreter = Interpreter(source_code=self.source_code, filename="main.vakya", stdout=stdout_stream, stdin=stdin_stream)
            interpreter.interpret(ast)

        return stdout_stream.getvalue()

    def test_name_greeting_vm(self):
        output = self.run_program("Goku", engine="vm")
        self.assertIn("Tumhara naam kya hai?", output)
        self.assertIn("Namaste, Goku!", output)

    def test_name_greeting_interpreter(self):
        output = self.run_program("Arjuna", engine="interpreter")
        self.assertIn("Tumhara naam kya hai?", output)
        self.assertIn("Namaste, Arjuna!", output)

    def test_empty_name_default_mitra(self):
        output_vm = self.run_program("   ", engine="vm")
        self.assertIn("Namaste, Mitra!", output_vm)

        output_interp = self.run_program("", engine="interpreter")
        self.assertIn("Namaste, Mitra!", output_interp)


if __name__ == "__main__":
    unittest.main()
