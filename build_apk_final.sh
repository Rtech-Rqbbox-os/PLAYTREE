#!/bin/bash
set -e
SRCDIR="/mnt/c/Users/RhysC/Downloads/PLAYTREE PC/playtree"
BUILDDIR="/home/playtree_build"

rm -rf "$BUILDDIR"
mkdir -p "$BUILDDIR"
cd "$SRCDIR"

# Copy only what's needed (skip .buildozer, build, dist, __pycache__)
rsync -a --exclude='.buildozer' --exclude='build' --exclude='dist' --exclude='__pycache__' --exclude='bin' --exclude='*.apk' --exclude='*.exe' --exclude='*.msix' "$SRCDIR/" "$BUILDDIR/"

cd "$BUILDDIR"
export PATH=$PATH:/root/.local/bin
export PIP_BREAK_SYSTEM_PACKAGES=1
export BUILDOZER_WARN_ON_ROOT=0

echo "=== Starting buildozer ==="
echo "y" | buildozer android debug 2>&1

echo "=== Copying APK ==="
mkdir -p "$SRCDIR/bin"
cp "$BUILDDIR/bin/"*.apk "$SRCDIR/bin/" 2>/dev/null || echo "No APK found in bin/"
ls -la "$SRCDIR/bin/"*.apk 2>/dev/null || echo "APK not found"
echo "=== COMPLETE ==="
