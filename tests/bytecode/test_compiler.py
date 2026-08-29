"""Unit tests for the Vākya Bytecode Compiler."""

import unittest
from vakya.lexer.lexer import Lexer
from vakya.parser.parser import Parser
from vakya.typechecker.checker import TypeChecker
from vakya.bytecode.compiler import BytecodeCompiler
from vakya.bytecode.opcodes import OpCode
from vakya.bytecode.chunk import Chunk


def compile_src(code: str) -> Chunk:
    tokens = Lexer(code).tokenize()
    ast = Parser(tokens, source_code=code).parse()
    TypeChecker(source_code=code).check(ast)
    return BytecodeCompiler(source_code=code).compile(ast)


class TestBytecodeCompiler(unittest.TestCase):
    def test_compile_literals(self):
        chunk = compile_src("chara a = 42\nchara b = 3.14\nchara s = \"Namaste\"\nchara t = satya\nchara f = asatya\nchara n = shunya")
        opcodes = [instr.opcode for instr in chunk.instructions]
        self.assertIn(OpCode.CONSTANT, opcodes)
        self.assertIn(OpCode.TRUE, opcodes)
        self.assertIn(OpCode.FALSE, opcodes)
        self.assertIn(OpCode.NULL, opcodes)
        self.assertEqual(chunk.constants[0], 42)
        self.assertEqual(chunk.constants[1], 3.14)
        self.assertEqual(chunk.constants[2], "Namaste")

    def test_compile_binary_arithmetic(self):
        chunk = compile_src("chara x = 10 + 20 * 3")
        opcodes = [instr.opcode for instr in chunk.instructions]
        self.assertIn(OpCode.ADD, opcodes)
        self.assertIn(OpCode.MULTIPLY, opcodes)
        # Verify 20 * 3 is multiplied before adding 10
        mult_idx = opcodes.index(OpCode.MULTIPLY)
        add_idx = opcodes.index(OpCode.ADD)
        self.assertLess(mult_idx, add_idx)

    def test_compile_short_circuit_and_or(self):
        chunk = compile_src("chara res = satya va asatya evam satya")
        opcodes = [instr.opcode for instr in chunk.instructions]
        self.assertIn(OpCode.JUMP_IF_TRUE_OR_POP, opcodes)
        self.assertIn(OpCode.JUMP_IF_FALSE_OR_POP, opcodes)

    def test_compile_unary_negate_and_not(self):
        chunk = compile_src("chara a = -10\nchara b = na satya")
        opcodes = [instr.opcode for instr in chunk.instructions]
        self.assertIn(OpCode.NEGATE, opcodes)
        self.assertIn(OpCode.NOT, opcodes)

    def test_compile_if_else_jumps(self):
        code = """
        chara x = 10
        yadi x > 5 {
            vada("Greater")
        } anyatha {
            vada("Smaller")
        }
        """
        chunk = compile_src(code)
        opcodes = [instr.opcode for instr in chunk.instructions]
        self.assertIn(OpCode.JUMP_IF_FALSE, opcodes)
        self.assertIn(OpCode.JUMP, opcodes)

    def test_compile_while_loop_jumps(self):
        code = """
        chara i = 0
        yavat i < 5 {
            i += 1
            yadi i == 2 { agaccha }
            yadi i == 4 { virama }
        }
        """
        chunk = compile_src(code)
        opcodes = [instr.opcode for instr in chunk.instructions]
        self.assertIn(OpCode.JUMP_IF_FALSE, opcodes)
        self.assertIn(OpCode.JUMP, opcodes)

    def test_compile_for_each_loop(self):
        code = """
        chara items = [1, 2, 3]
        pratyekam item madhye items {
            vada(item)
        }
        """
        chunk = compile_src(code)
        opcodes = [instr.opcode for instr in chunk.instructions]
        self.assertIn(OpCode.BUILD_LIST, opcodes)
        self.assertIn(OpCode.INDEX, opcodes)
        self.assertIn(OpCode.JUMP_IF_FALSE, opcodes)

    def test_compile_collections(self):
        code = """
        chara l = [10, 20]
        chara m = {"a": 1, "b": 2}
        chara item = l[0]
        chara len_l = l.length
        """
        chunk = compile_src(code)
        opcodes = [instr.opcode for instr in chunk.instructions]
        self.assertIn(OpCode.BUILD_LIST, opcodes)
        self.assertIn(OpCode.BUILD_MAP, opcodes)
        self.assertIn(OpCode.INDEX, opcodes)
        self.assertIn(OpCode.GET_MEMBER, opcodes)

    def test_compile_function_and_closure(self):
        code = """
        karya outer(x: sankhya) {
            karya inner(y: sankhya) -> sankhya {
                pratyavartaya x + y
            }
            pratyavartaya inner
        }
        """
        chunk = compile_src(code)
        opcodes = [instr.opcode for instr in chunk.instructions]
        self.assertIn(OpCode.MAKE_CLOSURE, opcodes)
        self.assertIn(OpCode.STORE_GLOBAL, opcodes)

        # Check nested chunk
        fn_chunk = chunk.constants[0]
        self.assertIsInstance(fn_chunk, Chunk)
        self.assertEqual(fn_chunk.name, "outer")
        self.assertEqual(fn_chunk.param_names, ["x"])

        # Check inner chunk inside outer chunk
        inner_chunk = fn_chunk.constants[0]
        self.assertIsInstance(inner_chunk, Chunk)
        self.assertEqual(inner_chunk.name, "inner")
        self.assertEqual(inner_chunk.param_names, ["y"])
        self.assertEqual(len(inner_chunk.upvalues), 1)  # captures 'x'

    def test_disassembly_output(self):
        code = "chara x = 10\nvada(x)"
        chunk = compile_src(code)
        disasm = chunk.disassemble()
        self.assertIn("=== Bytecode Disassembly:", disasm)
        self.assertIn("CONSTANT", disasm)
        self.assertIn("STORE_GLOBAL", disasm)
        self.assertIn("CALL_BUILTIN", disasm)


if __name__ == "__main__":
    unittest.main()
