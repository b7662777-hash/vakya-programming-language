"""Tests for bytecode chunk structures, constant pool deduplication, and instruction properties."""

import unittest
from vakya.lexer.lexer import Lexer
from vakya.parser.parser import Parser
from vakya.typechecker.checker import TypeChecker
from vakya.bytecode.compiler import BytecodeCompiler
from vakya.bytecode.opcodes import OpCode
from vakya.bytecode.chunk import Chunk
from vakya.bytecode.instructions import Instruction


class TestBytecodeStructures(unittest.TestCase):
    def test_chunk_constant_deduplication(self):
        chunk = Chunk(name="test")
        c1 = chunk.add_constant(42)
        c2 = chunk.add_constant(42)
        c3 = chunk.add_constant("hello")
        c4 = chunk.add_constant("hello")
        self.assertEqual(c1, c2)
        self.assertEqual(c3, c4)
        self.assertEqual(len(chunk.constants), 2)

    def test_chunk_instruction_indexing(self):
        chunk = Chunk(name="test")
        i0 = chunk.add_instruction(OpCode.CONSTANT, 0)
        i1 = chunk.add_instruction(OpCode.STORE_GLOBAL, "x")
        i2 = chunk.add_instruction(OpCode.HALT)
        self.assertEqual(i0, 0)
        self.assertEqual(i1, 1)
        self.assertEqual(i2, 2)
        self.assertEqual(len(chunk.instructions), 3)

    def test_instruction_string_representation(self):
        instr1 = Instruction(OpCode.ADD)
        instr2 = Instruction(OpCode.STORE_GLOBAL, "x")
        self.assertEqual(str(instr1), "ADD")
        self.assertEqual(str(instr2), "STORE_GLOBAL x")

    def test_disassembler_formatting(self):
        chunk = Chunk(name="demo")
        chunk.add_constant(100)
        chunk.add_instruction(OpCode.CONSTANT, 0)
        chunk.add_instruction(OpCode.HALT)
        disasm = chunk.disassemble()
        self.assertIn("=== Bytecode Disassembly: demo", disasm)
        self.assertIn("CONSTANT", disasm)
        self.assertIn("HALT", disasm)

    def test_jump_target_within_bounds(self):
        code = """
        chara x = 10
        yadi x > 5 {
            vada("Big")
        } anyatha {
            vada("Small")
        }
        """
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens, source_code=code).parse()
        TypeChecker(source_code=code).check(ast)
        chunk = BytecodeCompiler(source_code=code).compile(ast)

        num_instructions = len(chunk.instructions)
        for offset, instr in enumerate(chunk.instructions):
            if instr.opcode in (OpCode.JUMP, OpCode.JUMP_IF_FALSE, OpCode.JUMP_IF_TRUE):
                target = instr.operand
                self.assertIsInstance(target, int)
                self.assertGreaterEqual(target, 0)
                self.assertLessEqual(target, num_instructions)

    def test_chunk_param_and_upvalue_metadata(self):
        chunk = Chunk(name="test_fn", param_names=["a", "b"], num_locals=3)
        self.assertEqual(len(chunk.param_names), 2)
        self.assertEqual(chunk.num_locals, 3)

    def test_chunk_empty_disassembly(self):
        chunk = Chunk(name="empty")
        disasm = chunk.disassemble()
        self.assertIn("=== Bytecode Disassembly: empty", disasm)

    def test_opcode_string_enum_values(self):
        for op in OpCode:
            self.assertEqual(str(op), op.name)

    def test_chunk_add_multiple_types_constants(self):
        chunk = Chunk(name="types")
        idx_int = chunk.add_constant(1)
        idx_float = chunk.add_constant(1.0)
        idx_str = chunk.add_constant("1")
        # Ensure separate constant pool slots for distinct types
        self.assertNotEqual(idx_int, idx_float)
        self.assertNotEqual(idx_int, idx_str)
        self.assertEqual(len(chunk.constants), 3)

    def test_instruction_with_span(self):
        from vakya.ast.nodes import Span
        span = Span(line=10, column=5, end_line=10, end_column=9, filename="")
        instr = Instruction(OpCode.ADD, span=span)
        self.assertEqual(instr.span.line, 10)
        self.assertEqual(instr.span.column, 5)


if __name__ == "__main__":
    unittest.main()
