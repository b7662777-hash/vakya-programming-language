"""Unit tests for Vākya module loader and standard library modules."""

import unittest
from vakya.modules.loader import ModuleLoader
from vakya.errors import VakyaError


class TestModuleLoader(unittest.TestCase):
    def setUp(self):
        self.loader = ModuleLoader()

    def test_load_std_math_module(self):
        exports = self.loader.load_module("math")
        self.assertIn("PI", exports)
        self.assertAlmostEqual(exports["PI"], 3.141592653589793)
        self.assertIn("varga", exports)
        self.assertIn("ghana", exports)
        self.assertIn("parama_mana", exports)

    def test_load_std_strings_module(self):
        exports = self.loader.load_module("strings")
        self.assertIn("jodo_sarva", exports)
        self.assertIn("shabda_viparita", exports)

    def test_load_std_core_module(self):
        exports = self.loader.load_module("core")
        self.assertIn("nirdharaya", exports)
        self.assertIn("parivartana_shabda", exports)

    def test_load_std_collections_module(self):
        exports = self.loader.load_module("collections")
        self.assertIn("suchi_viparita", exports)
        self.assertIn("suchi_shodhaka", exports)
        self.assertIn("suchi_yog", exports)

    def test_load_std_io_module(self):
        exports = self.loader.load_module("io")
        self.assertIn("vada_pankti", exports)

    def test_load_std_time_module(self):
        exports = self.loader.load_module("time")
        self.assertIn("NIMESHA_SECOND", exports)
        self.assertIn("convert_minutes_to_seconds", exports)

    def test_module_not_found(self):
        with self.assertRaises(VakyaError):
            self.loader.load_module("nonexistent_module_xyz_123")

    def test_aayat_math_in_vm(self):
        from vakya.lexer.lexer import Lexer
        from vakya.parser.parser import Parser
        from vakya.typechecker.checker import TypeChecker
        from vakya.bytecode.compiler import BytecodeCompiler
        from vakya.vm.vm import VirtualMachine

        code = "aayat math\nchara p = math.PI"
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens).parse()
        TypeChecker().check(ast)
        chunk = BytecodeCompiler().compile(ast)
        vm = VirtualMachine()
        vm.run(chunk)
        self.assertAlmostEqual(vm.globals["p"], 3.141592653589793)

    def test_aayat_math_in_interpreter(self):
        from vakya.lexer.lexer import Lexer
        from vakya.parser.parser import Parser
        from vakya.typechecker.checker import TypeChecker
        from vakya.interpreter.interpreter import Interpreter

        code = "aayat math\nchara p = math.PI"
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens).parse()
        TypeChecker().check(ast)
        interp = Interpreter()
        interp.interpret(ast)
        self.assertAlmostEqual(interp.current_env.values["p"], 3.141592653589793)


if __name__ == "__main__":
    unittest.main()
