"""
Usage:
python setup.py build

This will build an executable and a small copy of python to be able to use the executable.
Requirements:

- cx_Freeze
- TCL/TK

"""

import sys, os
from cx_Freeze import setup, Executable

# Set this to python's install dir
pypath = r"D:\Program_Files\python_3.6"

os.environ['TCL_LIBRARY'] = pypath+r'\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = pypath+r'\tcl\tk8.6'

dlls = [
	pypath+r"\DLLs\tcl86t.dll",
	pypath+r"\DLLs\tk86t.dll"
]

base = "Win32GUI"

setup(  name = "JSON-G Viewer",
		version = "1.0",
		options = {"build_exe": {"include_files": dlls}},
		description = "View JSON-G files without converting!",
		executables = [Executable("jsong-viewer.py", base=base)])