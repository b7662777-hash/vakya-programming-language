"""Module loader and resolver for Vākya."""

import os
from typing import Any, Dict, List, Optional, Set
from vakya.lexer.lexer import Lexer
from vakya.parser.parser import Parser
from vakya.typechecker.checker import TypeChecker
from vakya.bytecode.compiler import BytecodeCompiler
from vakya.paths import get_default_search_paths
from vakya.errors import VakyaError, RuntimeError, E101_UNDEFINED_VARIABLE


class ModuleLoader:
    """Resolves and loads external .vakya modules and standard library components."""

    def __init__(self, search_paths: Optional[List[str]] = None):
        self.search_paths = list(search_paths) if search_paths else []
        for p in get_default_search_paths():
            if p not in self.search_paths:
                self.search_paths.append(p)

        self.loaded_modules: Dict[str, Dict[str, Any]] = {}
        self.loading_stack: Set[str] = set()

    def resolve_module_path(self, module_name: str, base_dir: Optional[str] = None) -> Optional[str]:
        """Resolve a module identifier (e.g. 'math' or './utils') to an absolute file path."""
        # Normalize name
        filename = module_name if module_name.endswith(".vakya") else f"{module_name}.vakya"

        # Check relative to base_dir
        if base_dir:
            candidate = os.path.abspath(os.path.join(base_dir, filename))
            if os.path.exists(candidate):
                return candidate

        # Check in search paths
        for path in self.search_paths:
            candidate = os.path.abspath(os.path.join(path, filename))
            if os.path.exists(candidate):
                return candidate

        return None

    def load_module(self, module_name: str, base_dir: Optional[str] = None) -> Dict[str, Any]:
        """Load and execute a module, returning its exported symbols dictionary."""
        abs_path = self.resolve_module_path(module_name, base_dir)
        if not abs_path:
            raise RuntimeError.from_info(
                E101_UNDEFINED_VARIABLE,
                f"Module '{module_name}' could not be resolved in search paths",
                help_text=f"Ensure '{module_name}.vakya' exists in the current directory or std/ folder.",
            )

        if abs_path in self.loaded_modules:
            return self.loaded_modules[abs_path]

        if abs_path in self.loading_stack:
            raise RuntimeError.from_info(
                E101_UNDEFINED_VARIABLE,
                f"Circular module dependency detected when loading '{abs_path}'",
                help_text="Refactor circular module imports to break dependency loops.",
            )

        self.loading_stack.add(abs_path)
        try:
            with open(abs_path, "r", encoding="utf-8") as f:
                source_code = f.read()

            filename = os.path.basename(abs_path)
            tokens = Lexer(source_code, filename=filename).tokenize()
            ast = Parser(tokens, source_code=source_code, filename=filename).parse()
            TypeChecker(source_code=source_code, filename=filename).check(ast)

            compiler = BytecodeCompiler(filename=filename, source_code=source_code)
            chunk = compiler.compile(ast)

            from vakya.vm.vm import VirtualMachine
            vm = VirtualMachine()
            vm.run(chunk)

            # Export global symbols from module VM execution
            exports = dict(vm.globals)
            self.loaded_modules[abs_path] = exports
            return exports

        finally:
            self.loading_stack.remove(abs_path)
