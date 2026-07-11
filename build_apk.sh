#!/bin/bash
# Copy project to a path without spaces, then build
SRCDIR="/mnt/c/Users/RhysC/Downloads/PLAYTREE PC/playtree"
BUILDDIR="/tmp/playtree_build"

rm -rf "$BUILDDIR"
cp -r "$SRCDIR" "$BUILDDIR"

cd "$BUILDDIR"
export PATH=$PATH:/root/.local/bin
export PIP_BREAK_SYSTEM_PACKAGES=1
export BUILDOZER_WARN_ON_ROOT=0

# Add storage-dir override in buildozer.spec
sed -i 's/^log_level = 2/log_level = 2\nstorage.dir = \/tmp\/playtree_build\/.buildozer/' buildozer.spec

echo "y" | buildozer -v android debug 2>&1

# Copy result back
cp "$BUILDDIR/bin/"*.apk "$SRCDIR/bin/" 2>/dev/null
echo "=== DONE ==="
ls -la "$SRCDIR/bin/"*.apk 2>/dev/null
