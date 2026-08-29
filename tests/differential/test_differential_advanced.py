"""Advanced differential tests asserting 100% semantic equivalence between AST Interpreter and Bytecode VM."""

import io
import unittest
from vakya.lexer.lexer import Lexer
from vakya.parser.parser import Parser
from vakya.typechecker.checker import TypeChecker
from vakya.interpreter.interpreter import Interpreter
from vakya.bytecode.compiler import BytecodeCompiler
from vakya.vm.vm import VirtualMachine


def run_interpreter(code: str) -> str:
    tokens = Lexer(code).tokenize()
    ast = Parser(tokens, source_code=code).parse()
    TypeChecker(source_code=code).check(ast)
    out = io.StringIO()
    interp = Interpreter(source_code=code, stdout=out)
    interp.interpret(ast)
    return out.getvalue().strip()


def run_vm(code: str) -> str:
    tokens = Lexer(code).tokenize()
    ast = Parser(tokens, source_code=code).parse()
    TypeChecker(source_code=code).check(ast)
    chunk = BytecodeCompiler(source_code=code).compile(ast)
    out = io.StringIO()
    vm = VirtualMachine(stdout=out)
    vm.run(chunk)
    return out.getvalue().strip()


class TestDifferentialAdvanced(unittest.TestCase):
    def assert_diff(self, code: str, desc: str = ""):
        interp_res = run_interpreter(code)
        vm_res = run_vm(code)
        self.assertEqual(interp_res, vm_res, f"Differential divergence in '{desc}':\nInterpreter:\n{interp_res}\nVM:\n{vm_res}")

    def test_diff_nested_while_loops(self):
        code = """
        chara i = 0
        chara total = 0
        yavat i < 4 {
            chara j = 0
            yavat j < 3 {
                total += i * 10 + j
                j += 1
            }
            i += 1
        }
        vada("Total:", total)
        """
        self.assert_diff(code, "nested while loops")

    def test_diff_break_in_nested_loops(self):
        code = """
        chara i = 0
        yavat i < 5 {
            chara j = 0
            yavat j < 5 {
                yadi j == 2 {
                    virama
                }
                vada(i, j)
                j += 1
            }
            i += 1
        }
        """
        self.assert_diff(code, "break in nested loops")

    def test_diff_continue_in_nested_loops(self):
        code = """
        chara i = 0
        yavat i < 3 {
            chara j = 0
            yavat j < 3 {
                j += 1
                yadi j == 2 {
                    agaccha
                }
                vada(i, j)
            }
            i += 1
        }
        """
        self.assert_diff(code, "continue in nested loops")

    def test_diff_matrix_multiplication(self):
        code = """
        chara matrix = [[1, 2], [3, 4]]
        chara sum = 0
        pratyekam row madhye matrix {
            pratyekam cell madhye row {
                sum += cell
            }
        }
        vada("Matrix sum:", sum)
        """
        self.assert_diff(code, "matrix sum")

    def test_diff_map_aggregation(self):
        code = """
        chara scores = {"math": 95, "physics": 90, "chemistry": 85}
        chara total = 0
        pratyekam subject madhye scores {
            total += scores[subject]
        }
        vada("Total score:", total)
        """
        self.assert_diff(code, "map aggregation")

    def test_diff_higher_order_map_filter(self):
        code = """
        karya my_map(fn, list) {
            chara result = []
            pratyekam item madhye list {
                suchi_jodo(result, fn(item))
            }
            pratyavartaya result
        }

        karya square(x: sankhya) -> sankhya {
            pratyavartaya x * x
        }

        chara nums = [1, 2, 3, 4, 5]
        chara squared = my_map(square, nums)
        vada(squared)
        """
        self.assert_diff(code, "higher order map")

    def test_diff_higher_order_filter(self):
        code = """
        karya my_filter(pred, list) {
            chara result = []
            pratyekam item madhye list {
                yadi pred(item) {
                    suchi_jodo(result, item)
                }
            }
            pratyavartaya result
        }

        karya is_gt_two(x: sankhya) -> boolean {
            pratyavartaya x > 2
        }

        chara nums = [1, 2, 3, 4, 5]
        vada(my_filter(is_gt_two, nums))
        """
        self.assert_diff(code, "higher order filter")

    def test_diff_closure_shared_environment(self):
        code = """
        karya bank_account(initial_balance) {
            chara balance = initial_balance

            karya deposit(amt) {
                balance += amt
                pratyavartaya balance
            }

            karya withdraw(amt) {
                balance -= amt
                pratyavartaya balance
            }

            pratyavartaya {"deposit": deposit, "withdraw": withdraw}
        }

        chara acc = bank_account(100)
        chara dep = acc["deposit"]
        chara withdr = acc["withdraw"]

        vada(dep(50))
        vada(withdr(30))
        vada(dep(20))
        """
        self.assert_diff(code, "closure shared state")

    def test_diff_fibonacci_iterative(self):
        code = """
        karya fib_iter(n: sankhya) -> sankhya {
            yadi n <= 0 { pratyavartaya 0 }
            yadi n == 1 { pratyavartaya 1 }
            chara a = 0
            chara b = 1
            chara i = 2
            yavat i <= n {
                chara temp = a + b
                a = b
                b = temp
                i += 1
            }
            pratyavartaya b
        }
        vada(fib_iter(10))
        vada(fib_iter(15))
        """
        self.assert_diff(code, "fibonacci iterative")

    def test_diff_compound_assignment_chains(self):
        code = """
        chara x = 10
        x += 5
        x -= 2
        x *= 3
        x /= 2
        vada("Final x:", x)
        """
        self.assert_diff(code, "compound assignments")

    def test_diff_nested_if_else_branches(self):
        code = """
        chara a = 15
        chara b = 25
        yadi a > 10 {
            yadi b > 20 {
                vada("Both high")
            } anyatha {
                vada("A high, B low")
            }
        } anyatha {
            vada("A low")
        }
        """
        self.assert_diff(code, "nested if-else")

    def test_diff_string_manipulation_pipeline(self):
        code = """
        chara raw = "   krishna   "
        chara cleaned = shabda_trim(raw)
        chara upper = shabda_bada(cleaned)
        vada("Cleaned:", cleaned)
        vada("Upper:", upper)
        vada("Length:", upper.length)
        """
        self.assert_diff(code, "string pipeline")

    def test_diff_list_stack_operations(self):
        code = """
        chara stack = []
        suchi_jodo(stack, "first")
        suchi_jodo(stack, "second")
        suchi_jodo(stack, "third")
        vada(suchi_hatao(stack, 0))
        vada(suchi_hatao(stack, 0))
        vada(stack)
        """
        self.assert_diff(code, "stack operations")


if __name__ == "__main__":
    unittest.main()
