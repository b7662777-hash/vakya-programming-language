"""Unit tests for the Vākya Native Compiler Backend (C and LLVM)."""

import unittest
from vakya.native import NativeCompiler


class TestNativeCompiler(unittest.TestCase):
    def test_native_c_emission_basic(self):
        code = """
        karya yog(a: sankhya, b: sankhya) -> sankhya {
            pratyavartaya a + b
        }

        chara x = 10
        chara y = 20
        chara ans = yog(x, y)
        vada(ans)
        """
        compiler = NativeCompiler("test.vakya", backend="c")
        c_code = compiler.compile_to_c(code)

        self.assertIn("vakya_int yog(vakya_int a, vakya_int b)", c_code)
        self.assertIn("int main(int argc, char** argv)", c_code)
        self.assertIn("vada_int(", c_code)

    def test_native_c_emission_while_loop(self):
        code = """
        chara i = 0
        chara s = 0
        yavat i < 100 {
            s += i
            i += 1
        }
        vada(s)
        """
        compiler = NativeCompiler("test_loop.vakya", backend="c")
        c_code = compiler.compile_to_c(code)

        self.assertIn("goto loop_start_", c_code)
        self.assertIn("goto loop_body_", c_code)
        self.assertIn("vada_int(", c_code)

    def test_native_llvm_emission_basic(self):
        code = """
        karya guna(a: sankhya, b: sankhya) -> sankhya {
            pratyavartaya a * b
        }

        chara x = 5
        chara y = 6
        chara ans = guna(x, y)
        vada(ans)
        """
        compiler = NativeCompiler("test_llvm.vakya", backend="llvm")
        llvm_ir = compiler.compile_to_llvm(code)

        self.assertIn("define i64 @guna(i64 %a, i64 %b)", llvm_ir)
        self.assertIn("define i32 @main(i32 %argc, i8** %argv)", llvm_ir)
        self.assertIn("call void @vada_int(", llvm_ir)

    def test_native_llvm_emission_conditions(self):
        code = """
        chara x = 10
        yadi x > 5 {
            vada(1)
        } anyatha {
            vada(0)
        }
        """
        compiler = NativeCompiler("test_cond.vakya", backend="llvm")
        llvm_ir = compiler.compile_to_llvm(code)

        self.assertIn("icmp sgt i64", llvm_ir)
        self.assertIn("br i1", llvm_ir)


if __name__ == "__main__":
    unittest.main()
