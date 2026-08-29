"""Conformance tests for variable and constant declarations in Vākya."""

import io
import unittest
from vakya.lexer.lexer import Lexer
from vakya.parser.parser import Parser
from vakya.typechecker.checker import TypeChecker
from vakya.interpreter.interpreter import Interpreter


def run_code(code: str) -> str:
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens, source_code=code)
    ast = parser.parse()
    checker = TypeChecker(source_code=code)
    checker.check(ast)
    out = io.StringIO()
    interpreter = Interpreter(source_code=code, stdout=out)
    interpreter.interpret(ast)
    return out.getvalue().strip()


class TestConformanceDeclarations(unittest.TestCase):
    def test_var_decl_unannotated_int(self):
        out = run_code("chara x = 42\nvada(x)")
        self.assertEqual(out, "42")

    def test_var_decl_unannotated_float(self):
        out = run_code("chara f = 3.14\nvada(f)")
        self.assertEqual(out, "3.14")

    def test_var_decl_unannotated_string(self):
        out = run_code('chara s = "Namaste"\nvada(s)')
        self.assertEqual(out, "Namaste")

    def test_var_decl_unannotated_bool(self):
        out = run_code("chara b = satya\nvada(b)")
        self.assertEqual(out, "satya")

    def test_var_decl_unannotated_null(self):
        out = run_code("chara n = shunya\nvada(n)")
        self.assertEqual(out, "shunya")

    def test_var_decl_annotated_sankhya(self):
        out = run_code("chara x: sankhya = 100\nvada(x)")
        self.assertEqual(out, "100")

    def test_var_decl_annotated_dashamika(self):
        out = run_code("chara d: dashamika = 2.5\nvada(d)")
        self.assertEqual(out, "2.5")

    def test_var_decl_annotated_shabda(self):
        out = run_code('chara s: shabda = "Goku"\nvada(s)')
        self.assertEqual(out, "Goku")

    def test_var_decl_annotated_boolean(self):
        out = run_code("chara b: boolean = asatya\nvada(b)")
        self.assertEqual(out, "asatya")

    def test_var_decl_annotated_suchi(self):
        out = run_code("chara l: suchi = [1, 2]\nvada(l)")
        self.assertEqual(out, "[1, 2]")

    def test_var_decl_annotated_naksha(self):
        out = run_code('chara m: naksha = {"a": 1}\nvada(m["a"])')
        self.assertEqual(out, "1")

    def test_const_decl(self):
        out = run_code("dhruva pi = 3.14159\nvada(pi)")
        self.assertEqual(out, "3.14159")

    def test_const_decl_annotated(self):
        out = run_code("dhruva max_val: sankhya = 1000\nvada(max_val)")
        self.assertEqual(out, "1000")

    def test_variable_reassignment(self):
        code = """
        chara x = 10
        x = 20
        vada(x)
        x = 30
        vada(x)
        """
        out = run_code(code)
        self.assertEqual(out, "20\n30")

    def test_compound_assignments(self):
        code = """
        chara a = 10
        a += 5
        vada(a)
        a -= 3
        vada(a)
        a *= 2
        vada(a)
        a /= 4
        vada(a)
        """
        out = run_code(code)
        self.assertEqual(out, "15\n12\n24\n6")

    def test_string_compound_assignment(self):
        code = """
        chara greeting = "Namaste"
        greeting += " World"
        vada(greeting)
        """
        out = run_code(code)
        self.assertEqual(out, "Namaste World")

    def test_shadowing_in_inner_block(self):
        code = """
        chara x = 1
        {
            chara x = 2
            vada(x)
        }
        vada(x)
        """
        out = run_code(code)
        self.assertEqual(out, "2\n1")

    def test_multiple_declarations_sequential(self):
        code = """
        chara a = 1
        chara b = 2
        chara c = 3
        vada(a + b + c)
        """
        out = run_code(code)
        self.assertEqual(out, "6")


if __name__ == "__main__":
    unittest.main()
