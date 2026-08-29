"""Comprehensive unit tests for every VM OpCode and runtime operation."""

import io
import unittest
from vakya.lexer.lexer import Lexer
from vakya.parser.parser import Parser
from vakya.typechecker.checker import TypeChecker
from vakya.bytecode.compiler import BytecodeCompiler
from vakya.bytecode.opcodes import OpCode
from vakya.bytecode.chunk import Chunk
from vakya.vm.vm import VirtualMachine
from vakya.vm.runtime import UpvalueCell, VMClosure
from vakya.errors import RuntimeError, IndexError, TypeError, NameError, ArgumentError


def run_code(code: str) -> str:
    tokens = Lexer(code).tokenize()
    ast = Parser(tokens, source_code=code).parse()
    TypeChecker(source_code=code).check(ast)
    chunk = BytecodeCompiler(source_code=code).compile(ast)
    out = io.StringIO()
    vm = VirtualMachine(stdout=out)
    vm.run(chunk)
    return out.getvalue().strip()


class TestVMInstructions(unittest.TestCase):
    # Literals
    def test_op_constant_int(self):
        self.assertEqual(run_code("vada(12345)"), "12345")

    def test_op_constant_float(self):
        self.assertEqual(run_code("vada(3.14159)"), "3.14159")

    def test_op_constant_string(self):
        self.assertEqual(run_code('vada("Vakya Bytecode VM")'), "Vakya Bytecode VM")

    def test_op_true_and_false(self):
        self.assertEqual(run_code("vada(satya, asatya)"), "satya asatya")

    def test_op_null(self):
        self.assertEqual(run_code("vada(shunya)"), "shunya")

    # Arithmetic
    def test_op_add_numbers(self):
        self.assertEqual(run_code("vada(15 + 25)"), "40")

    def test_op_add_strings(self):
        self.assertEqual(run_code('vada("Namaste " + "Duniya")'), "Namaste Duniya")

    def test_op_subtract(self):
        self.assertEqual(run_code("vada(100 - 35)"), "65")

    def test_op_multiply_numbers(self):
        self.assertEqual(run_code("vada(9 * 9)"), "81")

    def test_op_multiply_string_repeat(self):
        self.assertEqual(run_code('vada("om" * 3)'), "omomom")
        self.assertEqual(run_code('vada(3 * "om")'), "omomom")

    def test_op_divide_int_exact(self):
        self.assertEqual(run_code("vada(40 / 5)"), "8")

    def test_op_divide_float(self):
        self.assertEqual(run_code("vada(9 / 2)"), "4.5")

    def test_op_modulo(self):
        self.assertEqual(run_code("vada(29 % 7)"), "1")

    def test_op_power(self):
        self.assertEqual(run_code("vada(3 ** 4)"), "81")

    def test_op_negate(self):
        self.assertEqual(run_code("vada(-(-50))"), "50")

    def test_op_not(self):
        self.assertEqual(run_code("vada(na (10 == 20))"), "satya")

    # Comparisons
    def test_op_equal_numbers(self):
        self.assertEqual(run_code("vada(100 == 100)"), "satya")

    def test_op_not_equal_numbers(self):
        self.assertEqual(run_code("vada(100 != 200)"), "satya")

    def test_op_less_greater(self):
        self.assertEqual(run_code("vada(10 < 20, 20 > 10)"), "satya satya")

    def test_op_less_greater_equal(self):
        self.assertEqual(run_code("vada(10 <= 10, 20 >= 20)"), "satya satya")

    def test_op_compare_strings(self):
        self.assertEqual(run_code('vada("apple" < "banana")'), "satya")

    # Data Structures
    def test_op_build_list(self):
        self.assertEqual(run_code("vada([1, 2, 3, 4])"), "[1, 2, 3, 4]")

    def test_op_build_map(self):
        self.assertEqual(run_code('vada({"k1": "v1", "k2": "v2"})'), '{"k1": "v1", "k2": "v2"}')

    def test_op_index_list(self):
        self.assertEqual(run_code("chara l = [10, 20, 30]\nvada(l[2])"), "30")

    def test_op_set_index_list(self):
        self.assertEqual(run_code("chara l = [10, 20]\nl[0] = 99\nvada(l)"), "[99, 20]")

    def test_op_index_map(self):
        self.assertEqual(run_code('chara m = {"key": 77}\nvada(m["key"])'), "77")

    def test_op_set_index_map(self):
        self.assertEqual(run_code('chara m = {}\nm["hero"] = "Arjuna"\nvada(m["hero"])'), "Arjuna")

    def test_op_get_member_length(self):
        self.assertEqual(run_code('vada([1, 2].length, {"a": 1}.length, "abc".length)'), "2 1 3")

    # Builtins
    def test_op_call_builtin_lamba(self):
        self.assertEqual(run_code('vada(lamba("Hello"), lamba([1, 2, 3]))'), "5 3")

    def test_op_call_builtin_prakaar(self):
        self.assertEqual(run_code('vada(prakaar(10), prakaar("s"), prakaar(satya))'), "sankhya shabda boolean")

    def test_op_call_builtin_suchi_jodo_hatao(self):
        code = """
        chara l = [1]
        suchi_jodo(l, 2)
        suchi_jodo(l, 3)
        vada(l)
        vada(suchi_hatao(l, 0))
        vada(l)
        """
        self.assertEqual(run_code(code), "[1, 2, 3]\n1\n[2, 3]")

    def test_op_call_builtin_shabda_transforms(self):
        code = """
        vada(shabda_bada("namaste"))
        vada(shabda_chhota("VAKYA"))
        vada(shabda_trim("  clean  "))
        """
        self.assertEqual(run_code(code), "NAMASTE\nvakya\nclean")


if __name__ == "__main__":
    unittest.main()
