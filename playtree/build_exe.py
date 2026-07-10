"""
PLAYTREE Build Script for Windows (.exe)

Usage:
    python build_exe.py

Requirements:
    pip install pyinstaller
"""

import os
import sys
import shutil

def build():
    # Check for PyInstaller
    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller not found. Installing...")
        os.system("pip install pyinstaller")
        try:
            import PyInstaller
        except ImportError:
            print("Failed to install PyInstaller. Please run: pip install pyinstaller")
            return

    print("Building PLAYTREE executable...")

    # Clean previous builds
    for d in ['dist', 'build', '__pycache__']:
        if os.path.exists(d):
            shutil.rmtree(d, ignore_errors=True)

    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--name", "PLAYTREE",
        "--onefile",
        "--windowed",
        "--icon", "NONE",
        "--add-data", "src;src",
        "--hidden-import", "pygame",
        "--noconfirm",
        "main.py"
    ]

    os.system(" ".join(cmd))

    # Check result
    exe_path = os.path.join("dist", "PLAYTREE.exe")
    if os.path.exists(exe_path):
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print(f"\nSuccess! Executable created: {exe_path}")
        print(f"Size: {size_mb:.1f} MB")
    else:
        print("\nBuild may have failed. Check output above.")

if __name__ == "__main__":
    build()
