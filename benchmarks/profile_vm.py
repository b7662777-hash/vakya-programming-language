"""Profile VM bottlenecks using cProfile and pstats."""

import cProfile
import pstats
import io
from vakya.lexer.lexer import Lexer
from vakya.parser.parser import Parser
from vakya.typechecker.checker import TypeChecker
from vakya.bytecode.compiler import BytecodeCompiler
from vakya.vm.vm import VirtualMachine

# While loop workload (20,000 iterations)
loop_code = """
chara i = 0
chara s = 0
yavat i < 20000 {
    s += i
    i += 1
}
"""

tokens = Lexer(loop_code).tokenize()
ast = Parser(tokens, source_code=loop_code).parse()
TypeChecker(source_code=loop_code).check(ast)
chunk = BytecodeCompiler().compile(ast)

pr = cProfile.Profile()
pr.enable()

vm = VirtualMachine()
vm.run(chunk)

pr.disable()

s = io.StringIO()
ps = pstats.Stats(pr, stream=s).sort_stats('tottime')
ps.print_stats(25)
print("=== CPROFILE FOR WHILE LOOP (20,000 ITERS) ===")
print(s.getvalue())
