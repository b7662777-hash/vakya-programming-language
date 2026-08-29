"""Unit tests for the Vākya Virtual Machine execution engine."""

import io
import unittest
from vakya.lexer.lexer import Lexer
from vakya.parser.parser import Parser
from vakya.typechecker.checker import TypeChecker
from vakya.bytecode.compiler import BytecodeCompiler
from vakya.vm.vm import VirtualMachine
from vakya.errors import RuntimeError, IndexError, TypeError, NameError


def run_vm(code: str) -> str:
    tokens = Lexer(code).tokenize()
    ast = Parser(tokens, source_code=code).parse()
    TypeChecker(source_code=code).check(ast)
    chunk = BytecodeCompiler(source_code=code).compile(ast)
    out = io.StringIO()
    vm = VirtualMachine(stdout=out)
    vm.run(chunk)
    return out.getvalue().strip()


class TestVMCore(unittest.TestCase):
    def test_vm_arithmetic_operations(self):
        self.assertEqual(run_vm("vada(10 + 20)"), "30")
        self.assertEqual(run_vm("vada(50 - 18)"), "32")
        self.assertEqual(run_vm("vada(6 * 7)"), "42")
        self.assertEqual(run_vm("vada(100 / 4)"), "25")
        self.assertEqual(run_vm("vada(7 / 2)"), "3.5")
        self.assertEqual(run_vm("vada(17 % 5)"), "2")
        self.assertEqual(run_vm("vada(2 ** 5)"), "32")
        self.assertEqual(run_vm("vada(2 ** 3 ** 2)"), "512")

    def test_vm_comparisons_and_equality(self):
        self.assertEqual(run_vm("vada(5 < 10)"), "satya")
        self.assertEqual(run_vm("vada(10 <= 10)"), "satya")
        self.assertEqual(run_vm("vada(10 > 5)"), "satya")
        self.assertEqual(run_vm("vada(10 >= 10)"), "satya")
        self.assertEqual(run_vm("vada(42 == 42)"), "satya")
        self.assertEqual(run_vm("vada(42 != 100)"), "satya")
        self.assertEqual(run_vm("vada(satya == 1)"), "asatya")
        self.assertEqual(run_vm("vada(asatya == 0)"), "asatya")

    def test_vm_boolean_logic(self):
        self.assertEqual(run_vm("vada(satya evam satya)"), "satya")
        self.assertEqual(run_vm("vada(satya evam asatya)"), "asatya")
        self.assertEqual(run_vm("vada(satya va asatya)"), "satya")
        self.assertEqual(run_vm("vada(asatya va asatya)"), "asatya")
        self.assertEqual(run_vm("vada(na satya)"), "asatya")
        self.assertEqual(run_vm("vada(na asatya)"), "satya")

    def test_vm_variables_and_scopes(self):
        code = """
        chara x = 10
        {
            chara x = 20
            vada(x)
        }
        vada(x)
        """
        self.assertEqual(run_vm(code), "20\n10")

    def test_vm_recursion_factorial(self):
        code = """
        karya fact(n: sankhya) -> sankhya {
            yadi n <= 1 { pratyavartaya 1 }
            pratyavartaya n * fact(n - 1)
        }
        vada(fact(6))
        """
        self.assertEqual(run_vm(code), "720")

    def test_vm_recursion_fibonacci(self):
        code = """
        karya fib(n: sankhya) -> sankhya {
            yadi n <= 0 { pratyavartaya 0 }
            yadi n == 1 { pratyavartaya 1 }
            pratyavartaya fib(n - 1) + fib(n - 2)
        }
        vada(fib(8))
        """
        self.assertEqual(run_vm(code), "21")

    def test_vm_closure_state_mutation(self):
        code = """
        karya make_counter() {
            chara count = 0
            karya inc() -> sankhya {
                count += 1
                pratyavartaya count
            }
            pratyavartaya inc
        }
        chara c1 = make_counter()
        vada(c1())
        vada(c1())
        vada(c1())
        """
        self.assertEqual(run_vm(code), "1\n2\n3")

    def test_vm_multiple_independent_closures(self):
        code = """
        karya make_counter(start: sankhya) {
            chara count = start
            karya inc(step: sankhya) -> sankhya {
                count += step
                pratyavartaya count
            }
            pratyavartaya inc
        }
        chara c1 = make_counter(100)
        chara c2 = make_counter(0)
        vada(c1(5))
        vada(c2(1))
        vada(c1(10))
        vada(c2(1))
        """
        self.assertEqual(run_vm(code), "105\n1\n115\n2")

    def test_vm_collections_list_and_map(self):
        code = """
        chara l = [10, 20, 30]
        l[1] = 99
        vada(l)
        vada(l[1])
        vada(l.length)

        chara m = {"name": "Goku", "power": 9001}
        m["power"] = 9002
        vada(m["power"])
        vada(m.length)
        """
        self.assertEqual(run_vm(code), "[10, 99, 30]\n99\n3\n9002\n2")

    def test_vm_call_depth_limit_e304(self):
        code = """
        karya inf() {
            pratyavartaya inf()
        }
        inf()
        """
        with self.assertRaises(RuntimeError) as ctx:
            run_vm(code)
        self.assertEqual(ctx.exception.code, "E304")

    def test_vm_division_by_zero_e301(self):
        code = "chara x = 10 / 0"
        with self.assertRaises(RuntimeError) as ctx:
            run_vm(code)
        self.assertEqual(ctx.exception.code, "E301")

    def test_vm_index_out_of_bounds_e302(self):
        code = "chara l = [1, 2]\nchara val = l[5]"
        with self.assertRaises(IndexError) as ctx:
            run_vm(code)
        self.assertEqual(ctx.exception.code, "E302")

    def test_vm_map_key_not_found_e303(self):
        code = 'chara m = {"a": 1}\nchara val = m["missing"]'
        with self.assertRaises(RuntimeError) as ctx:
            run_vm(code)
        self.assertEqual(ctx.exception.code, "E303")


if __name__ == "__main__":
    unittest.main()
