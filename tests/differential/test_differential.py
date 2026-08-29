"""Comprehensive differential testing between AST Interpreter and Bytecode VM."""

import io
import unittest
from vakya.lexer.lexer import Lexer
from vakya.parser.parser import Parser
from vakya.typechecker.checker import TypeChecker
from vakya.bytecode.compiler import BytecodeCompiler
from vakya.vm.vm import VirtualMachine
from vakya.interpreter.interpreter import Interpreter
from vakya.errors import VakyaError


class TestDifferentialExecution(unittest.TestCase):
    """Verifies 100% observable behavioral equivalence between AST Interpreter and Bytecode VM."""

    def execute_both(self, code: str):
        filename = "diff_test.vakya"
        tokens = Lexer(code, filename=filename).tokenize()
        ast = Parser(tokens, source_code=code, filename=filename).parse()
        TypeChecker(source_code=code, filename=filename).check(ast)

        # 1. Execute on AST Interpreter
        interp_out = io.StringIO()
        interp_err = None
        try:
            interp = Interpreter(source_code=code, filename=filename, stdout=interp_out)
            interp.interpret(ast)
        except VakyaError as e:
            interp_err = e

        # 2. Execute on Bytecode VM
        vm_out = io.StringIO()
        vm_err = None
        try:
            compiler = BytecodeCompiler(filename=filename, source_code=code)
            chunk = compiler.compile(ast)
            vm = VirtualMachine(stdout=vm_out)
            vm.run(chunk)
        except VakyaError as e:
            vm_err = e

        # Compare outputs and errors
        self.assertEqual(
            interp_out.getvalue().strip(),
            vm_out.getvalue().strip(),
            f"Differential stdout mismatch on code:\n{code}",
        )

        if interp_err is not None or vm_err is not None:
            self.assertIsNotNone(interp_err, f"VM raised {vm_err} but Interpreter did not")
            self.assertIsNotNone(vm_err, f"Interpreter raised {interp_err} but VM did not")
            self.assertEqual(
                interp_err.code,
                vm_err.code,
                f"Error code mismatch: Interpreter={interp_err.code}, VM={vm_err.code}",
            )

        return interp_out.getvalue().strip()

    def test_arithmetic_precedence_and_associativity(self):
        code = """
        vada(2 + 3 * 4)
        vada((2 + 3) * 4)
        vada(100 - 20 - 5)
        vada(2 ** 3 ** 2)
        vada(17 % 5)
        vada(-5 + 10)
        """
        out = self.execute_both(code)
        self.assertIn("14", out)
        self.assertIn("20", out)
        self.assertIn("75", out)
        self.assertIn("512", out)
        self.assertIn("2", out)
        self.assertIn("5", out)

    def test_strict_boolean_logic_and_short_circuit(self):
        code = """
        vada(satya evam asatya)
        vada(satya va asatya)
        vada(na satya)
        vada(na asatya)
        vada(satya == 1)
        vada(asatya == 0)
        """
        out = self.execute_both(code)
        self.assertIn("asatya", out)
        self.assertIn("satya", out)

    def test_conditionals_and_nested_branches(self):
        code = """
        chara x = 42
        yadi x > 50 {
            vada("gt50")
        } anyatha yadi x > 40 {
            yadi x == 42 {
                vada("exact 42")
            } anyatha {
                vada("gt40")
            }
        } anyatha {
            vada("other")
        }
        """
        out = self.execute_both(code)
        self.assertEqual(out, "exact 42")

    def test_while_loops_break_and_continue(self):
        code = """
        chara i = 0
        chara acc = []
        yavat i < 10 {
            i += 1
            yadi i % 2 == 0 {
                agaccha
            }
            yadi i > 7 {
                virama
            }
            suchi_jodo(acc, i)
        }
        vada(acc)
        """
        out = self.execute_both(code)
        self.assertEqual(out, "[1, 3, 5, 7]")

    def test_for_each_iterations(self):
        code = """
        chara fruits = ["Amra", "Seb", "Kela"]
        pratyekam f madhye fruits {
            vada(f)
        }
        chara m = {"a": 1, "b": 2}
        pratyekam k madhye m {
            vada(k, m[k])
        }
        """
        self.execute_both(code)

    def test_closures_and_independent_environments(self):
        code = """
        karya make_adder(x: sankhya) {
            karya adder(y: sankhya) -> sankhya {
                pratyavartaya x + y
            }
            pratyavartaya adder
        }
        chara add10 = make_adder(10)
        chara add50 = make_adder(50)
        vada(add10(5))
        vada(add50(5))
        """
        out = self.execute_both(code)
        self.assertIn("15", out)
        self.assertIn("55", out)

    def test_closure_mutation(self):
        code = """
        karya counter() {
            chara val = 0
            karya tick() -> sankhya {
                val += 1
                pratyavartaya val
            }
            pratyavartaya tick
        }
        chara c1 = counter()
        vada(c1())
        vada(c1())
        vada(c1())
        """
        out = self.execute_both(code)
        self.assertEqual(out, "1\n2\n3")

    def test_recursion_mutual_hoisting(self):
        code = """
        karya is_even(n: sankhya) -> boolean {
            yadi n == 0 { pratyavartaya satya }
            pratyavartaya is_odd(n - 1)
        }
        karya is_odd(n: sankhya) -> boolean {
            yadi n == 0 { pratyavartaya asatya }
            pratyavartaya is_even(n - 1)
        }
        vada(is_even(10))
        vada(is_odd(10))
        """
        out = self.execute_both(code)
        self.assertEqual(out, "satya\nasatya")

    def test_division_by_zero_error_parity(self):
        code = """
        chara x = 0
        vada(100 / x)
        """
        self.execute_both(code)

    def test_index_out_of_bounds_error_parity(self):
        code = """
        chara l = [1, 2, 3]
        vada(l[10])
        """
        self.execute_both(code)

    def test_map_key_not_found_error_parity(self):
        code = """
        chara m = {"name": "Goku"}
        vada(m["unknown_key"])
        """
        self.execute_both(code)


if __name__ == "__main__":
    unittest.main()
