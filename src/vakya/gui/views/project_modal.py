"""Modal dialog for scaffolding a new Vākya project."""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Callable

from vakya.gui.theme import Theme, Colors
from vakya.gui.state import AppState
from vakya.cli import scaffold_project


class ProjectModal(tk.Toplevel):
    """Modal dialog for creating and scaffolding a new Vākya project."""

    def __init__(self, parent: tk.Widget, theme: Theme, state: AppState, on_created: Callable[[str], None]):
        super().__init__(parent)
        self.theme = theme
        self.state = state
        self.on_created = on_created

        self.title("Create New Vākya Project")
        self.configure(bg=self.theme.bg)
        self.resizable(False, False)

        width = 480
        height = 280
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        x = (screen_w - width) // 2
        y = (screen_h - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.transient(parent)
        self.grab_set()

        self._build_ui()

    def _build_ui(self):
        pad_frame = tk.Frame(self, bg=self.theme.bg)
        pad_frame.pack(fill="both", expand=True, padx=25, pady=20)

        # Title
        title = tk.Label(
            pad_frame,
            text="🚀  New Vākya Project",
            font=("Segoe UI", 13, "bold"),
            bg=self.theme.bg,
            fg=self.theme.accent,
        )
        title.pack(anchor="w", pady=(0, 15))

        # Project Name
        name_lbl = tk.Label(
            pad_frame,
            text="Project Name:",
            font=("Segoe UI", 9, "bold"),
            bg=self.theme.bg,
            fg=self.theme.text,
        )
        name_lbl.pack(anchor="w")

        self.name_entry = tk.Entry(
            pad_frame,
            font=("Segoe UI", 10),
            bg=self.theme.card,
            fg=self.theme.text,
            insertbackground=self.theme.accent,
            relief="flat",
        )
        self.name_entry.pack(fill="x", pady=(4, 12))
        self.name_entry.insert(0, "namaste_app")

        # Location
        loc_lbl = tk.Label(
            pad_frame,
            text="Parent Directory:",
            font=("Segoe UI", 9, "bold"),
            bg=self.theme.bg,
            fg=self.theme.text,
        )
        loc_lbl.pack(anchor="w")

        loc_frame = tk.Frame(pad_frame, bg=self.theme.bg)
        loc_frame.pack(fill="x", pady=(4, 20))

        self.loc_entry = tk.Entry(
            loc_frame,
            font=("Segoe UI", 9),
            bg=self.theme.card,
            fg=self.theme.text,
            insertbackground=self.theme.accent,
            relief="flat",
        )
        self.loc_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.loc_entry.insert(0, self.state.default_workspace)

        browse_btn = tk.Button(
            loc_frame,
            text="Browse...",
            font=("Segoe UI", 8),
            bg=self.theme.card,
            fg=self.theme.text,
            activebackground=self.theme.card_hover,
            relief="flat",
            padx=8,
            command=self._browse_dir,
        )
        browse_btn.pack(side="right")

        # Action buttons
        btn_box = tk.Frame(pad_frame, bg=self.theme.bg)
        btn_box.pack(fill="x", side="bottom")

        cancel_btn = tk.Button(
            btn_box,
            text="Cancel",
            font=("Segoe UI", 9),
            bg=self.theme.card,
            fg=self.theme.text,
            activebackground=self.theme.card_hover,
            relief="flat",
            padx=12,
            pady=4,
            command=self.destroy,
        )
        cancel_btn.pack(side="right", padx=(8, 0))

        create_btn = tk.Button(
            btn_box,
            text="Create Project",
            font=("Segoe UI", 9, "bold"),
            bg=self.theme.accent,
            fg="#11111B" if self.theme.mode == "dark" else "#FFFFFF",
            activebackground=self.theme.accent_hover,
            relief="flat",
            padx=14,
            pady=4,
            command=self._create,
        )
        create_btn.pack(side="right")

    def _browse_dir(self):
        d = filedialog.askdirectory(initialdir=self.loc_entry.get())
        if d:
            self.loc_entry.delete(0, tk.END)
            self.loc_entry.insert(0, d)

    def _create(self):
        name = self.name_entry.get().strip()
        target_dir = self.loc_entry.get().strip()

        if not name:
            messagebox.showerror("Error", "Please provide a valid project name.")
            return

        if not os.path.exists(target_dir):
            messagebox.showerror("Error", "Target directory does not exist.")
            return

        project_path = os.path.join(target_dir, name)
        if os.path.exists(project_path):
            messagebox.showerror("Error", f"Directory '{project_path}' already exists.")
            return

        try:
            cwd = os.getcwd()
            os.chdir(target_dir)
            try:
                scaffold_project(name)
            finally:
                os.chdir(cwd)

            main_file = os.path.join(project_path, "main.vakya")
            self.destroy()
            self.on_created(main_file)

        except Exception as ex:
            messagebox.showerror("Scaffolding Error", f"Failed to create project:\n{ex}")
