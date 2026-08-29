"""Canonical Examples Browser for Vākya Launcher."""

import io
import os
import time
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Dict, List

from vakya.gui.theme import Theme, Colors
from vakya.gui.state import AppState
from vakya.paths import get_examples_path
from vakya.lexer.lexer import Lexer
from vakya.parser.parser import Parser
from vakya.typechecker.checker import TypeChecker
from vakya.typechecker.borrow_checker import BorrowChecker
from vakya.bytecode.compiler import BytecodeCompiler
from vakya.vm.vm import VirtualMachine
from vakya.interpreter.interpreter import Interpreter
from vakya.errors import VakyaError


class ExamplesView(tk.Frame):
    """Browser and runner for canonical Vākya examples."""

    def __init__(
        self,
        parent: tk.Widget,
        theme: Theme,
        state: AppState,
        on_back: Callable[[], None],
        on_open_in_editor: Callable[[str], None],
    ):
        super().__init__(parent, bg=theme.bg)
        self.theme = theme
        self.state = state
        self.on_back = on_back
        self.on_open_in_editor = on_open_in_editor

        self.examples_dir = get_examples_path()
        self.example_files: List[str] = []
        self.current_example_path: Optional[str] = None

        self._build_ui()
        self._load_examples_list()

    def _build_ui(self):
        # Toolbar
        toolbar = tk.Frame(self, bg=self.theme.surface, height=45)
        toolbar.pack(fill="x", side="top")

        back_btn = tk.Button(
            toolbar,
            text="← Dashboard",
            font=("Segoe UI", 9, "bold"),
            bg=self.theme.card,
            fg=self.theme.text,
            activebackground=self.theme.card_hover,
            relief="flat",
            padx=10,
            pady=4,
            command=self.on_back,
        )
        back_btn.pack(side="left", padx=(15, 10), pady=6)

        title = tk.Label(
            toolbar,
            text="💡  Canonical Vākya Examples",
            font=("Segoe UI", 11, "bold"),
            bg=self.theme.surface,
            fg=self.theme.accent,
        )
        title.pack(side="left", padx=5)

        # Right actions
        open_ed_btn = tk.Button(
            toolbar,
            text="Open in Editor",
            font=("Segoe UI", 9),
            bg=self.theme.card,
            fg=self.theme.text,
            activebackground=self.theme.card_hover,
            relief="flat",
            padx=10,
            pady=4,
            command=self._open_current_in_editor,
        )
        open_ed_btn.pack(side="right", padx=(5, 15), pady=6)

        diff_btn = tk.Button(
            toolbar,
            text="⚖ Differential Test (VM vs Interp)",
            font=("Segoe UI", 9),
            bg=self.theme.card,
            fg=self.theme.text,
            activebackground=self.theme.card_hover,
            relief="flat",
            padx=10,
            pady=4,
            command=self._diff_test,
        )
        diff_btn.pack(side="right", padx=5, pady=6)

        run_btn = tk.Button(
            toolbar,
            text="▷ Run Example",
            font=("Segoe UI", 9, "bold"),
            bg=self.theme.accent,
            fg="#11111B" if self.theme.mode == "dark" else "#FFFFFF",
            activebackground=self.theme.accent_hover,
            relief="flat",
            padx=12,
            pady=4,
            command=self._run_example,
        )
        run_btn.pack(side="right", padx=5, pady=6)

        # Main Split: List (Left) & Viewer (Right)
        paned = tk.PanedWindow(self, orient=tk.HORIZONTAL, bg=self.theme.border, bd=0, sashwidth=4)
        paned.pack(fill="both", expand=True, padx=10, pady=10)

        # Left Sidebar (Example list)
        list_frame = tk.Frame(paned, bg=self.theme.card, width=220)
        paned.add(list_frame, width=220)

        list_title = tk.Label(
            list_frame,
            text="OFFICIAL EXAMPLES",
            font=("Segoe UI", 8, "bold"),
            bg=self.theme.surface,
            fg=self.theme.text_dim,
            padx=10,
            pady=6,
        )
        list_title.pack(fill="x")

        self.listbox = tk.Listbox(
            list_frame,
            font=("Segoe UI", 9),
            bg=self.theme.card,
            fg=self.theme.text,
            selectbackground=self.theme.accent,
            selectforeground="#11111B" if self.theme.mode == "dark" else "#FFFFFF",
            relief="flat",
            bd=0,
            highlightthickness=0,
        )
        self.listbox.pack(fill="both", expand=True, padx=4, pady=4)
        self.listbox.bind("<<ListboxSelect>>", self._on_select_example)

        # Right Split: Code Viewer (top) and Output Console (bottom)
        right_paned = tk.PanedWindow(paned, orient=tk.VERTICAL, bg=self.theme.border, bd=0, sashwidth=4)
        paned.add(right_paned, width=650)

        # Code Viewer
        code_frame = tk.Frame(right_paned, bg=self.theme.code_bg)
        right_paned.add(code_frame, height=350)

        self.code_viewer = tk.Text(
            code_frame,
            font=("Consolas", 10),
            bg=self.theme.code_bg,
            fg=self.theme.text,
            relief="flat",
            padx=10,
            pady=8,
        )
        self.code_viewer.pack(fill="both", expand=True)

        # Output Console
        out_frame = tk.Frame(right_paned, bg=self.theme.card)
        right_paned.add(out_frame, height=200)

        out_lbl = tk.Label(
            out_frame,
            text="EXECUTION RESULT",
            font=("Segoe UI", 8, "bold"),
            bg=self.theme.surface,
            fg=self.theme.text_dim,
            padx=10,
            pady=4,
        )
        out_lbl.pack(fill="x")

        self.out_text = tk.Text(
            out_frame,
            font=("Consolas", 10),
            bg=self.theme.card,
            fg=self.theme.text,
            relief="flat",
            padx=10,
            pady=8,
            state="disabled",
        )
        self.out_text.pack(fill="both", expand=True)

    def _load_examples_list(self):
        if not os.path.exists(self.examples_dir):
            return
        files = sorted([f for f in os.listdir(self.examples_dir) if f.endswith(".vakya")])
        self.example_files = [os.path.join(self.examples_dir, f) for f in files]

        self.listbox.delete(0, tk.END)
        for f in files:
            clean_name = f.replace(".vakya", "").replace("_", " ").title()
            self.listbox.insert(tk.END, f"  {clean_name}")

        if self.example_files:
            self.listbox.selection_set(0)
            self._display_example(self.example_files[0])

    def _on_select_example(self, event):
        sel = self.listbox.curselection()
        if sel and sel[0] < len(self.example_files):
            self._display_example(self.example_files[sel[0]])

    def _display_example(self, file_path: str):
        self.current_example_path = file_path
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.code_viewer.delete("1.0", tk.END)
            self.code_viewer.insert("1.0", content)
            self._set_output(f"Selected: {os.path.basename(file_path)}\nClick '▷ Run Example' to execute.")
        except Exception as ex:
            self._set_output(f"Error reading example: {ex}")

    def _set_output(self, text: str):
        self.out_text.config(state="normal")
        self.out_text.delete("1.0", tk.END)
        self.out_text.insert("1.0", text)
        self.out_text.config(state="disabled")

    def _run_example(self):
        if not self.current_example_path:
            return
        source = self.code_viewer.get("1.0", tk.END)
        filename = os.path.basename(self.current_example_path)
        out_buf = io.StringIO()
        start_t = time.perf_counter()

        try:
            tokens = Lexer(source, filename=filename).tokenize()
            ast = Parser(tokens, source_code=source, filename=filename).parse()
            TypeChecker(source_code=source, filename=filename).check(ast)
            BorrowChecker(source_code=source, filename=filename).check(ast)

            compiler = BytecodeCompiler(filename=filename, source_code=source)
            chunk = compiler.compile(ast)
            vm = VirtualMachine(stdout=out_buf)
            vm.run(chunk)

            elapsed = (time.perf_counter() - start_t) * 1000
            self._set_output(f"=== Bytecode VM Execution ({elapsed:.2f}ms) ===\n{out_buf.getvalue()}")
        except VakyaError as ve:
            self._set_output(f"=== Error ===\n\n{ve.format_diagnostic()}")
        except Exception as ex:
            self._set_output(f"=== Error ===\n\n{ex}")

    def _diff_test(self):
        if not self.current_example_path:
            return
        source = self.code_viewer.get("1.0", tk.END)
        filename = os.path.basename(self.current_example_path)

        out_vm = io.StringIO()
        out_interp = io.StringIO()

        try:
            tokens = Lexer(source, filename=filename).tokenize()
            ast = Parser(tokens, source_code=source, filename=filename).parse()
            TypeChecker(source_code=source, filename=filename).check(ast)

            # VM execution
            t0 = time.perf_counter()
            chunk = BytecodeCompiler(filename=filename, source_code=source).compile(ast)
            vm = VirtualMachine(stdout=out_vm)
            vm.run(chunk)
            t_vm = (time.perf_counter() - t0) * 1000

            # Interpreter execution
            t1 = time.perf_counter()
            interp = Interpreter(source_code=source, filename=filename, stdout=out_interp)
            interp.interpret(ast)
            t_interp = (time.perf_counter() - t1) * 1000

            vm_val = out_vm.getvalue()
            int_val = out_interp.getvalue()
            matched = vm_val == int_val

            res = (
                f"=== Differential Engine Verification ===\n\n"
                f"Bytecode VM ({t_vm:.2f}ms):\n{vm_val}\n"
                f"AST Interpreter ({t_interp:.2f}ms):\n{int_val}\n"
                f"Differential Status: {'✓ PERFECT MATCH (100% Equivalence)' if matched else '✗ MISMATCH'}\n"
            )
            self._set_output(res)
        except Exception as ex:
            self._set_output(f"Differential test failed: {ex}")

    def _open_current_in_editor(self):
        if self.current_example_path:
            self.on_open_in_editor(self.current_example_path)
