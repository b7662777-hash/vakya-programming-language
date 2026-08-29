"""Performance baseline benchmark suite comparing V1 AST Interpreter vs V2 Bytecode VM."""

import sys
import time
import io

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from vakya.lexer.lexer import Lexer
from vakya.parser.parser import Parser
from vakya.typechecker.checker import TypeChecker
from vakya.interpreter.interpreter import Interpreter
from vakya.bytecode.compiler import BytecodeCompiler
from vakya.vm.vm import VirtualMachine


def benchmark_frontend(iterations: int = 1000):
    sample_code = """
    dhruva pi = 3.14159
    chara message = "Namaste"
    karya add(a: sankhya, b: sankhya) -> sankhya {
        yadi a > b {
            pratyavartaya a + b * 2
        } anyatha {
            pratyavartaya b - a
        }
    }
    """
    # Lexer
    start = time.perf_counter()
    total_tokens = 0
    for _ in range(iterations):
        lexer = Lexer(sample_code)
        tokens = lexer.tokenize()
        total_tokens += len(tokens)
    lex_time = time.perf_counter() - start
    lex_rate = total_tokens / lex_time
    print(f"[FRONTEND] Lexer Throughput:  {lex_rate:,.0f} tokens/sec ({total_tokens} tokens in {lex_time:.3f}s)")

    # Parser
    tokens = Lexer(sample_code).tokenize()
    start = time.perf_counter()
    for _ in range(iterations):
        parser = Parser(tokens, source_code=sample_code)
        ast = parser.parse()
    parse_time = time.perf_counter() - start
    parse_rate = iterations / parse_time
    print(f"[FRONTEND] Parser Throughput: {parse_rate:,.0f} parses/sec ({iterations} parses in {parse_time:.3f}s)")

    # Compiler
    ast = Parser(tokens, source_code=sample_code).parse()
    start = time.perf_counter()
    for _ in range(iterations):
        compiler = BytecodeCompiler(source_code=sample_code)
        chunk = compiler.compile(ast)
    comp_time = time.perf_counter() - start
    comp_rate = iterations / comp_time
    print(f"[FRONTEND] Compiler Throughput: {comp_rate:,.0f} compiles/sec ({iterations} compiles in {comp_time:.3f}s)")


def run_benchmark_workload(name: str, code: str, run_interp: bool = True):
    tokens = Lexer(code).tokenize()
    ast = Parser(tokens, source_code=code).parse()
    TypeChecker(source_code=code).check(ast)
    chunk = BytecodeCompiler(source_code=code).compile(ast)

    # 1. AST Interpreter
    interp_time = 0.0
    if run_interp:
        interp = Interpreter(source_code=code)
        start = time.perf_counter()
        interp.interpret(ast)
        interp_time = time.perf_counter() - start

    # 2. Bytecode VM
    vm = VirtualMachine()
    start = time.perf_counter()
    vm.run(chunk)
    vm_time = time.perf_counter() - start

    speedup_str = f"{interp_time / vm_time:.2f}x" if vm_time > 0 and interp_time > 0 else "N/A"
    print(f"| {name:<32} | Interpreter: {interp_time:.4f}s | VM: {vm_time:.4f}s | Speedup: {speedup_str:<6} |")
    return interp_time, vm_time


def main():
    print("=" * 80)
    print("VĀKYA V2 — PERFORMANCE BENCHMARK SUITE (INTERPRETER vs BYTECODE VM)")
    print("=" * 80)

    benchmark_frontend()
    print("-" * 80)
    print(f"| {'Workload':<32} | {'Interpreter Time':<20} | {'VM Time':<12} | {'Relative Speedup':<16} |")
    print("-" * 80)

    # 1. While loop & arithmetic
    loop_code = """
    chara total = 0
    chara i = 0
    yavat i < 20000 {
        total += i * 2 + 1
        i += 1
    }
    """
    run_benchmark_workload("While Loop (20,000 iters)", loop_code)

    # 2. Function calls
    fn_code = """
    karya add_one(x) {
        pratyavartaya x + 1
    }
    chara res = 0
    chara i = 0
    yavat i < 10000 {
        res = add_one(res)
        i += 1
    }
    """
    run_benchmark_workload("Function Calls (10,000 calls)", fn_code)

    # 3. Recursive Fibonacci (n=20)
    fib_code = """
    karya fib(n: sankhya) -> sankhya {
        yadi n <= 0 { pratyavartaya 0 }
        yadi n == 1 { pratyavartaya 1 }
        pratyavartaya fib(n - 1) + fib(n - 2)
    }
    chara ans = fib(20)
    """
    run_benchmark_workload("Recursive Fibonacci (n=20)", fib_code)

    # 4. Recursive Factorial (n=12, repeated)
    fact_code = """
    karya fact(n: sankhya) -> sankhya {
        yadi n <= 1 { pratyavartaya 1 }
        pratyavartaya n * fact(n - 1)
    }
    chara i = 0
    yavat i < 2000 {
        chara ans = fact(12)
        i += 1
    }
    """
    run_benchmark_workload("Factorial (2,000 recursions)", fact_code)

    # 5. Array & Map collections
    coll_code = """
    chara l = []
    chara m = {}
    chara i = 0
    yavat i < 3000 {
        suchi_jodo(l, i)
        m[i] = i * 2
        i += 1
    }
    """
    run_benchmark_workload("Array & Map (3,000 elements)", coll_code)

    print("=" * 80)
    print("Benchmark completed.")
    print("=" * 80)


if __name__ == "__main__":
    main()
