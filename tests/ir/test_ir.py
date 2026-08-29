"""Unit tests for Vākya Intermediate Representation (IR) generation."""

import unittest
from vakya.lexer.lexer import Lexer
from vakya.parser.parser import Parser
from vakya.ir import IRBuilder, IRPrinter, IRConst, IRBinOp, IRCall, IRReturn


class TestIRGeneration(unittest.TestCase):
    def build_ir(self, code: str):
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens, source_code=code).parse()
        builder = IRBuilder("test.vakya")
        return builder.build(ast)

    def test_ir_basic_arithmetic(self):
        code = "chara x = 10 + 20"
        module = self.build_ir(code)
        output = IRPrinter.print_module(module)
        self.assertIn("const 10 : sankhya", output)
        self.assertIn("const 20 : sankhya", output)
        self.assertIn("add", output)
        self.assertIn("store x", output)

    def test_ir_function_definition(self):
        code = """
        karya add(a: sankhya, b: sankhya) -> sankhya {
            pratyavartaya a + b
        }
        """
        module = self.build_ir(code)
        self.assertIn("add", module.functions)
        output = IRPrinter.print_module(module)
        self.assertIn("define @add(%p_a, %p_b)", output)
        self.assertIn("ret", output)

    def test_ir_if_else_branches(self):
        code = """
        chara x = 42
        yadi x > 50 {
            vada("gt")
        } anyatha {
            vada("le")
        }
        """
        module = self.build_ir(code)
        output = IRPrinter.print_module(module)
        self.assertIn("br ", output)
        self.assertIn("then_", output)
        self.assertIn("else_", output)
        self.assertIn("endif_", output)

    def test_ir_while_loop(self):
        code = """
        chara i = 0
        yavat i < 10 {
            i += 1
        }
        """
        module = self.build_ir(code)
        output = IRPrinter.print_module(module)
        self.assertIn("loop_start_", output)
        self.assertIn("loop_body_", output)
        self.assertIn("loop_end_", output)
        self.assertIn("jump loop_start_", output)


if __name__ == "__main__":
    unittest.main()
