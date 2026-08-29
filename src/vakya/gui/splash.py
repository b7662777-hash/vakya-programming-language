"""High-Speed Professional Loading / Splash Screen for Vākya."""

import os
import sys
import time
import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional

from vakya.paths import get_stdlib_path, get_docs_path, get_examples_path, get_icon_path
from .theme import Theme, Colors


class SplashScreen:
    """Displays a modern loading screen with real initialization progress."""

    def __init__(self, root: tk.Tk, on_complete: Callable[[], None], theme: Theme):
        self.root = root
        self.on_complete = on_complete
        self.theme = theme

        # Create frameless splash top-level
        self.splash = tk.Toplevel(root)
        self.splash.overrideredirect(True)
        self.splash.attributes("-topmost", True)
        self.splash.configure(bg=self.theme.border)

        # Dimensions & Centering
        width = 460
        height = 280
        screen_w = self.splash.winfo_screenwidth()
        screen_h = self.splash.winfo_screenheight()
        x = (screen_w - width) // 2
        y = (screen_h - height) // 2
        self.splash.geometry(f"{width}x{height}+{x}+{y}")

        self._build_ui()
        self.root.after(20, self._run_initialization)

    def _build_ui(self):
        # Inner main card with padding
        card = tk.Frame(self.splash, bg=self.theme.card, bd=0)
        card.pack(fill="both", expand=True, padx=2, pady=2)

        # Header Title
        title_lbl = tk.Label(
            card,
            text="VĀKYA",
            font=("Segoe UI", 26, "bold"),
            bg=self.theme.card,
            fg=self.theme.accent,
        )
        title_lbl.pack(pady=(35, 2))

        # Subtitle
        sub_lbl = tk.Label(
            card,
            text="Romanized Sanskrit Programming Language",
            font=("Segoe UI", 11),
            bg=self.theme.card,
            fg=self.theme.text_muted,
        )
        sub_lbl.pack(pady=(0, 25))

        # Status Label
        self.status_lbl = tk.Label(
            card,
            text="Initializing environment...",
            font=("Segoe UI", 9),
            bg=self.theme.card,
            fg=self.theme.text_dim,
        )
        self.status_lbl.pack(pady=(0, 8))

        # Progress bar
        self.progress = ttk.Progressbar(
            card,
            orient="horizontal",
            length=340,
            mode="determinate",
            style="Horizontal.TProgressbar",
        )
        self.progress.pack(pady=(0, 15))

        # Version & Ready status
        footer_lbl = tk.Label(
            card,
            text="v0.1.0 • Standalone Architecture",
            font=("Segoe UI", 8),
            bg=self.theme.card,
            fg=self.theme.text_dim,
        )
        footer_lbl.pack(side="bottom", pady=12)

    def _run_initialization(self):
        """Execute real initialization steps sequentially without artificial delays."""
        steps = [
            (25, "Indexing standard library modules...", self._init_stdlib),
            (55, "Initializing Bytecode Virtual Machine...", self._init_vm),
            (80, "Verifying documentation and examples...", self._init_resources),
            (100, "Ready!", lambda: None),
        ]

        for percent, message, action in steps:
            self.status_lbl.config(text=message)
            self.progress["value"] = percent
            self.splash.update()
            try:
                action()
            except Exception:
                pass
            # Very tiny pause to ensure smooth visual rendering
            self.splash.update_idletasks()

        # Close splash and launch main application
        self.root.after(60, self._finish)

    def _init_stdlib(self):
        get_stdlib_path()

    def _init_vm(self):
        from vakya.vm.vm import VirtualMachine
        from vakya.bytecode.compiler import BytecodeCompiler

    def _init_resources(self):
        get_docs_path()
        get_examples_path()

    def _finish(self):
        self.splash.destroy()
        self.on_complete()
