"""Interactive REPL View for Vākya Launcher."""

import io
import tkinter as tk
from tkinter import ttk
from typing import Callable, List

from vakya.gui.theme import Theme, Colors
from vakya.gui.state import AppState
from vakya.lexer.lexer import Lexer
from vakya.parser.parser import Parser
from vakya.typechecker.checker import TypeChecker
from vakya.bytecode.compiler import BytecodeCompiler
from vakya.vm.vm import VirtualMachine
from vakya.errors import VakyaError


class ReplView(tk.Frame):
    """Interactive Graphical REPL for Vākya."""

    def __init__(self, parent: tk.Widget, theme: Theme, state: AppState, on_back: Callable[[], None]):
        super().__init__(parent, bg=theme.bg)
        self.theme = theme
        self.state = state
        self.on_back = on_back

        self.history: List[str] = []
        self.history_index = -1
        self.vm = VirtualMachine()

        self._build_ui()
        self._welcome()

    def _build_ui(self):
        # Header toolbar
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
            text="⚡  Vākya Interactive REPL",
            font=("Segoe UI", 11, "bold"),
            bg=self.theme.surface,
            fg=self.theme.accent,
        )
        title.pack(side="left", padx=5)

        clear_btn = tk.Button(
            toolbar,
            text="Clear Console",
            font=("Segoe UI", 9),
            bg=self.theme.card,
            fg=self.theme.text,
            activebackground=self.theme.card_hover,
            relief="flat",
            padx=10,
            pady=4,
            command=self._clear,
        )
        clear_btn.pack(side="right", padx=(5, 15), pady=6)

        # Output / Transcript Area
        self.transcript = tk.Text(
            self,
            font=("Consolas", 11),
            bg=self.theme.code_bg,
            fg=self.theme.text,
            relief="flat",
            padx=12,
            pady=12,
            state="disabled",
        )
        self.transcript.pack(fill="both", expand=True, padx=15, pady=(10, 5))

        # Input Prompt Bar
        input_frame = tk.Frame(self, bg=self.theme.card)
        input_frame.pack(fill="x", padx=15, pady=(0, 15))

        prompt_lbl = tk.Label(
            input_frame,
            text=">>>",
            font=("Consolas", 11, "bold"),
            bg=self.theme.card,
            fg=self.theme.accent,
            padx=8,
        )
        prompt_lbl.pack(side="left")

        self.input_entry = tk.Entry(
            input_frame,
            font=("Consolas", 11),
            bg=self.theme.card,
            fg=self.theme.text,
            insertbackground=self.theme.accent,
            relief="flat",
        )
        self.input_entry.pack(side="left", fill="x", expand=True, padx=(0, 10), pady=8)
        self.input_entry.bind("<Return>", lambda e: self._eval_line())
        self.input_entry.bind("<Up>", self._history_prev)
        self.input_entry.bind("<Down>", self._history_next)
        self.input_entry.focus_set()

    def _welcome(self):
        welcome_text = (
            "============================================================\n"
            "   VĀKYA INTERACTIVE REPL (v0.1.0)\n"
            "   Type Romanized Sanskrit code and press [Enter] to evaluate.\n"
            "   Examples: chara x = 10 * 5 | vada(\"Namaste\") | math.PI\n"
            "============================================================\n\n"
        )
        self._append_text(welcome_text)

    def _append_text(self, text: str):
        self.transcript.config(state="normal")
        self.transcript.insert(tk.END, text)
        self.transcript.see(tk.END)
        self.transcript.config(state="disabled")

    def _clear(self):
        self.transcript.config(state="normal")
        self.transcript.delete("1.0", tk.END)
        self.transcript.config(state="disabled")
        self._welcome()

    def _eval_line(self):
        line = self.input_entry.get().strip()
        if not line:
            return

        self.history.append(line)
        self.history_index = len(self.history)
        self.input_entry.delete(0, tk.END)

        self._append_text(f">>> {line}\n")

        out_buf = io.StringIO()
        self.vm.stdout = out_buf

        try:
            tokens = Lexer(line, filename="<repl>").tokenize()
            ast = Parser(tokens, source_code=line, filename="<repl>").parse()
            compiler = BytecodeCompiler(filename="<repl>", source_code=line)
            chunk = compiler.compile(ast)
            res = self.vm.run(chunk)

            out_text = out_buf.getvalue()
            if out_text:
                self._append_text(out_text)
            if res is not None:
                self._append_text(f"=> {res}\n")
        except VakyaError as ve:
            self._append_text(f"{ve.format_diagnostic()}\n")
        except Exception as ex:
            self._append_text(f"Error: {ex}\n")

    def _history_prev(self, event):
        if self.history and self.history_index > 0:
            self.history_index -= 1
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, self.history[self.history_index])
        return "break"

    def _history_next(self, event):
        if self.history and self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, self.history[self.history_index])
        elif self.history_index == len(self.history) - 1:
            self.history_index = len(self.history)
            self.input_entry.delete(0, tk.END)
        return "break"
