"""Main application window and view coordinator for Vākya GUI Launcher."""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional

from vakya.gui.theme import Theme, enable_high_dpi
from vakya.gui.state import AppState
from vakya.gui.splash import SplashScreen
from vakya.gui.views.dashboard import DashboardView
from vakya.gui.views.editor import EditorView
from vakya.gui.views.repl_view import ReplView
from vakya.gui.views.examples_view import ExamplesView
from vakya.gui.views.docs_view import DocsView
from vakya.gui.views.doctor_view import DoctorView
from vakya.gui.views.project_modal import ProjectModal
from vakya.gui.views.settings_view import SettingsView
from vakya.paths import get_icon_path


class VakyaApplication:
    """Main graphical launcher window for the Vākya Programming Language."""

    def __init__(self, initial_file: Optional[str] = None):
        enable_high_dpi()

        self.root = tk.Tk()
        self.root.title("VĀKYA — Romanized Sanskrit Programming Language")
        self.root.withdraw()  # Hidden until splash completes

        self.state = AppState()
        self.theme = Theme(mode=self.state.theme_mode)
        self.style = ttk.Style(self.root)
        self.theme.apply_to_ttk(self.style)

        # Set Window Dimensions & Centering
        width = 980
        height = 660
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = (screen_w - width) // 2
        y = (screen_h - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.minsize(800, 520)
        self.root.configure(bg=self.theme.bg)

        # Set App Icon
        icon_path = get_icon_path()
        if icon_path:
            try:
                if icon_path.endswith(".ico"):
                    self.root.iconbitmap(icon_path)
                elif icon_path.endswith(".png"):
                    icon_img = tk.PhotoImage(file=icon_path)
                    self.root.iconphoto(True, icon_img)
            except Exception:
                pass

        self.initial_file = initial_file
        self.current_view: Optional[tk.Widget] = None

        # Container for dynamic view switching
        self.container = tk.Frame(self.root, bg=self.theme.bg)
        self.container.pack(fill="both", expand=True)

        # Launch splash screen
        self.splash = SplashScreen(self.root, on_complete=self._on_splash_done, theme=self.theme)

    def _on_splash_done(self):
        """Called when splash finishes initializing."""
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

        if self.initial_file and os.path.exists(self.initial_file):
            self.show_editor(self.initial_file)
        else:
            self.show_dashboard()

    def show_dashboard(self):
        self._switch_view(
            DashboardView(
                parent=self.container,
                theme=self.theme,
                state=self.state,
                on_open_file=self.show_editor,
                on_new_project=self._open_new_project_modal,
                on_open_repl=self.show_repl,
                on_open_examples=self.show_examples,
                on_open_docs=self.show_docs,
                on_open_doctor=self.show_doctor,
                on_open_settings=self.show_settings,
            )
        )

    def show_editor(self, file_path: str):
        self.state.add_recent_file(file_path)
        self._switch_view(
            EditorView(
                parent=self.container,
                theme=self.theme,
                state=self.state,
                file_path=file_path,
                on_back=self.show_dashboard,
            )
        )

    def show_repl(self):
        self._switch_view(
            ReplView(
                parent=self.container,
                theme=self.theme,
                state=self.state,
                on_back=self.show_dashboard,
            )
        )

    def show_examples(self):
        self._switch_view(
            ExamplesView(
                parent=self.container,
                theme=self.theme,
                state=self.state,
                on_back=self.show_dashboard,
                on_open_in_editor=self.show_editor,
            )
        )

    def show_docs(self):
        self._switch_view(
            DocsView(
                parent=self.container,
                theme=self.theme,
                state=self.state,
                on_back=self.show_dashboard,
            )
        )

    def show_doctor(self):
        self._switch_view(
            DoctorView(
                parent=self.container,
                theme=self.theme,
                state=self.state,
                on_back=self.show_dashboard,
            )
        )

    def show_settings(self):
        self._switch_view(
            SettingsView(
                parent=self.container,
                theme=self.theme,
                state=self.state,
                on_back=self.show_dashboard,
                on_settings_saved=self._on_theme_or_settings_updated,
            )
        )

    def _open_new_project_modal(self):
        ProjectModal(
            parent=self.root,
            theme=self.theme,
            state=self.state,
            on_created=self.show_editor,
        )

    def _on_theme_or_settings_updated(self):
        self.theme = Theme(mode=self.state.theme_mode)
        self.theme.apply_to_ttk(self.style)
        self.root.configure(bg=self.theme.bg)
        self.container.configure(bg=self.theme.bg)
        self.show_dashboard()

    def _switch_view(self, new_view: tk.Widget):
        if self.current_view:
            self.current_view.destroy()
        self.current_view = new_view
        self.current_view.pack(fill="both", expand=True)

    def run(self):
        self.root.mainloop()


def launch_gui(initial_file: Optional[str] = None):
    """Entry point for launching the Vākya graphical desktop application."""
    app = VakyaApplication(initial_file=initial_file)
    app.run()
