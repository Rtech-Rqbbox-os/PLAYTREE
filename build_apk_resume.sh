#!/bin/bash
cd /home/playtree_build
export PATH=$PATH:/root/.local/bin
export PIP_BREAK_SYSTEM_PACKAGES=1
export BUILDOZER_WARN_ON_ROOT=0
echo "y" | buildozer android debug 2>&1 | grep -E "(BUILD|ERROR|SUCCESS|apk|COMPLETE|Failed|Your application)" | tail -20
mkdir -p "/mnt/c/Users/RhysC/Downloads/PLAYTREE PC/playtree/bin"
cp /home/playtree_build/bin/*.apk "/mnt/c/Users/RhysC/Downloads/PLAYTREE PC/playtree/bin/" 2>/dev/null
echo "=== RESULT ==="
ls -la "/mnt/c/Users/RhysC/Downloads/PLAYTREE PC/playtree/bin/"*.apk 2>/dev/null || echo "No APK yet"
