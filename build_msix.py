"""
PLAYTREE Microsoft Store (MSIX) Build Script

Prerequisites:
  1. Run build_exe.py first to create dist/PLAYTREE.exe
  2. Install MSIX Packaging Tool: winget install Microsoft.MSIXPackagingTool
  3. Or use Visual Studio's Windows Application Packaging Project

Usage:
    python build_msix.py

Output:
    msix/PLAYTREE.msix
"""

import os
import sys
import shutil
import subprocess
import glob


def build():
    print("=" * 50)
    print("  PLAYTREE Microsoft Store Build")
    print("=" * 50)

    exe_path = os.path.join("dist", "PLAYTREE.exe")
    if not os.path.exists(exe_path):
        print("\n[ERROR] dist/PLAYTREE.exe not found!")
        print("Run 'python build_exe.py' first.")
        return False

    msix_dir = "msix"
    staging_dir = os.path.join(msix_dir, "_staging")
    out_dir = os.path.join(msix_dir, "out")

    print("\n[1/5] Cleaning previous build...")
    for d in [staging_dir, out_dir]:
        if os.path.exists(d):
            shutil.rmtree(d, ignore_errors=True)
    os.makedirs(staging_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)

    print("[2/5] Copying exe and assets to staging...")
    shutil.copy2(exe_path, staging_dir)
    for f in glob.glob(os.path.join(msix_dir, "assets", "*")):
        dest = os.path.join(staging_dir, "assets")
        os.makedirs(dest, exist_ok=True)
        shutil.copy2(f, dest)
    shutil.copy2(os.path.join(msix_dir, "Package.appxmanifest"), staging_dir)

    print("[3/5] Checking for MSIX tools...")
    makeappx = shutil.which("makeappx")
    if not makeappx:
        common = r"C:\Program Files (x86)\Windows Kits\10\bin"
        if os.path.exists(common):
            versions = sorted(os.listdir(common), reverse=True)
            for v in versions:
                p = os.path.join(common, v, "x64", "makeappx.exe")
                if os.path.exists(p):
                    makeappx = p
                    break

    if makeappx:
        print(f"[4/5] Packaging with makeappx: {makeappx}")
        msix_path = os.path.join(out_dir, "PLAYTREE.msix")
        cmd = [makeappx, "pack", "/d", staging_dir, "/p", msix_path, "/o"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"\n[DONE] MSIX created: {msix_path}")
            print(f"       Size: {os.path.getsize(msix_path) / (1024*1024):.1f} MB")
        else:
            print(f"\n[ERROR] makeappx failed:\n{result.stderr}")
            return False
    else:
        print("[4/5] makeappx not found. Creating instructions instead...")
        create_instructions(staging_dir, out_dir)

    print("[5/5] Build complete!")
    print("\n" + "=" * 50)
    print("  NEXT STEPS FOR MICROSOFT STORE SUBMISSION")
    print("=" * 50)
    print(f"""
  1. Go to https://partner.microsoft.com/dashboard
  2. Sign in with your Microsoft account
  3. Click 'New product' > 'App'
  4. Reserve app name: RQBBoxGameStudios.PLAYTREE
  5. Upload the MSIX from: {out_dir}/
  6. Fill in Store listing (see store_listing.md)
  7. Submit for review (usually 1-3 days)
""")
    return True


def create_instructions(staging_dir, out_dir):
    instructions = f"""
PLAYTREE MSIX Packaging Instructions
=====================================

The makeappx tool was not found on this system.
You can package using one of these methods:

METHOD 1: Windows SDK (Recommended)
------------------------------------
1. Install Windows SDK from:
   https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/

2. Open Command Prompt as Administrator and run:
   makeappx pack /d "{os.path.abspath(staging_dir)}" /p "{os.path.abspath(out_dir)}\\PLAYTREE.msix" /o

METHOD 2: MSIX Packaging Tool (GUI)
------------------------------------
1. Install 'MSIX Packaging Tool' from Microsoft Store
2. Open the tool
3. Select 'Application package' > 'Create package'
4. Browse to: {os.path.abspath(staging_dir)}
5. Follow the wizard to create the .msix

METHOD 3: Visual Studio
-----------------------
1. Create a 'Windows Application Packaging Project'
2. Add the PLAYTREE.exe as an application reference
3. Build the project to generate the .msix

Staging directory contents:
{os.listdir(staging_dir)}
"""
    path = os.path.join(out_dir, "PACKAGING_INSTRUCTIONS.txt")
    with open(path, "w") as f:
        f.write(instructions)
    print(f"    Instructions saved to: {path}")


if __name__ == "__main__":
    build()
