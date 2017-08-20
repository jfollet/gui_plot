import cx_Freeze
import sys
import matplotlib

base = None
if sys.platform == 'win32':
    base = "Win32GUI"


executables = [cx_Freeze.Executable("gui_main.py", base=base, icon='icon.ico')]

cx_Freeze.setup(name = "Plot GUI", options = {"build_exe": {"packages": ["tkinter", "matplotlib"], "include_files":["icon.ico"]}},
                version = "0.01",
                description = "Plot GUI data",
                executables = executables)
