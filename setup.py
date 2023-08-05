import sys
import os
from cx_Freeze import setup, Executable

# Dependencies that need to be excluded (if any)
excludes = []

# Include required Qt plugins (Assuming PyQt5)
pyqt_plugins_dir = os.path.join(os.path.dirname(sys.executable), 'Library', 'plugins', 'platforms')
include_files = [(pyqt_plugins_dir, 'platforms')]

# Include other necessary data files (if any)
include_files += [('R_SHEL.ico', 'R_SHEL.ico','LICENSE.txt')]  # Assuming R_SHEL.ico is in the same directory as setup.py

# Options for cx_Freeze
build_options = {
    'packages': ['numpy', 'cv2', 'scipy', 'matplotlib'],
    'includes': [],
    'excludes': excludes,
    'include_files': include_files,
}

# Executable
executables = [
    Executable(
        "R_SHEL_Analyzer.py",                 # Replace with the name of your main script
        base=None,                           # Use None for a console-based application or "Win32GUI" for a GUI application
        icon="R_SHEL.ico"                    # Icon file for the executable (if any)
    )
]

setup(
    name="R_SHEL Analyzer",
    version="1.0",
    author="Janmey Jay Panda",
    description="This application is intended to be used for Retro SHEL beam analysis",
    options={"build_exe": build_options},
    executables=executables
)
