# -*- mode: python ; coding: utf-8 -*-

import os
import sys

block_cipher = None

repo_root = os.path.abspath(SPECPATH)

datas = [
    (os.path.join(repo_root, "std"), "std"),
    (os.path.join(repo_root, "runtime"), "runtime"),
    (os.path.join(repo_root, "docs"), "docs"),
    (os.path.join(repo_root, "examples"), "examples"),
    (os.path.join(repo_root, "resources"), "resources"),
]

hiddenimports = [
    "vakya",
    "vakya.lexer",
    "vakya.lexer.lexer",
    "vakya.lexer.tokens",
    "vakya.parser",
    "vakya.parser.parser",
    "vakya.ast",
    "vakya.ast.nodes",
    "vakya.typechecker",
    "vakya.typechecker.checker",
    "vakya.typechecker.borrow_checker",
    "vakya.typechecker.types",
    "vakya.interpreter",
    "vakya.interpreter.interpreter",
    "vakya.interpreter.environment",
    "vakya.bytecode",
    "vakya.bytecode.compiler",
    "vakya.bytecode.opcodes",
    "vakya.bytecode.chunk",
    "vakya.vm",
    "vakya.vm.vm",
    "vakya.vm.frames",
    "vakya.ir",
    "vakya.ir.builder",
    "vakya.ir.instructions",
    "vakya.native",
    "vakya.native.c_emitter",
    "vakya.native.llvm_backend",
    "vakya.native.compiler",
    "vakya.modules",
    "vakya.modules.loader",
    "vakya.formatter",
    "vakya.formatter.formatter",
    "vakya.repl",
    "vakya.repl.repl",
    "vakya.errors",
    "vakya.errors.codes",
    "vakya.errors.errors",
    "vakya.paths",
    "vakya.gui",
    "vakya.gui.app",
    "vakya.gui.theme",
    "vakya.gui.state",
    "vakya.gui.splash",
    "vakya.gui.views",
    "vakya.gui.views.dashboard",
    "vakya.gui.views.editor",
    "vakya.gui.views.repl_view",
    "vakya.gui.views.examples_view",
    "vakya.gui.views.docs_view",
    "vakya.gui.views.doctor_view",
    "vakya.gui.views.project_modal",
    "vakya.gui.views.settings_view",
    "tkinter",
    "tkinter.ttk",
    "tkinter.filedialog",
    "tkinter.messagebox",
    "tkinter.scrolledtext",
    "PIL",
    "PIL.Image",
    "PIL.ImageTk",
]

icon_file = os.path.join(repo_root, "resources", "vakya.ico")
if not os.path.exists(icon_file):
    icon_file = None

a = Analysis(
    [os.path.join(repo_root, "src", "vakya", "cli.py")],
    pathex=[os.path.join(repo_root, "src")],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="vakya",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    icon=icon_file,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
