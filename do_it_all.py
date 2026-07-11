#!/usr/bin/env python3
"""
Generate Store assets from playtree.ico + rebuild MSIX — one shot.
"""
import pygame
import os
import struct
import shutil
import sys
import zlib

pygame.init()

ICO_PATH = "playtree.ico"
ASSETS_DIR = os.path.join("msix", "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

GOLD = (255, 215, 0)
GREEN_GLOW = (100, 255, 150)
BG = (10, 10, 30)


def extract_png_from_ico(path):
    with open(path, "rb") as f:
        data = f.read()
    _, _, count = struct.unpack_from("<HHH", data, 0)
    best_off, best_sz, best_w = 0, 0, 0
    for i in range(count):
        off = 6 + i * 16
        w = data[off] or 256
        sz = struct.unpack_from("<I", data, off + 8)[0]
        img_off = struct.unpack_from("<I", data, off + 12)[0]
        if w > best_w:
            best_w = w
            best_off = img_off
            best_sz = sz
    png_data = data[best_off:best_off + best_sz]
    tmp = os.path.join("msix", "_ico_tmp.png")
    with open(tmp, "wb") as f:
        f.write(png_data)
    surf = pygame.image.load(tmp)
    os.remove(tmp)
    return surf


def scale_to(surf, size):
    return pygame.transform.smoothscale(surf, (size, size))


print("[1/5] Loading playtree.ico...")
ico = extract_png_from_ico(ICO_PATH)
print(f"      {ico.get_width()}x{ico.get_height()} loaded")

print("[2/5] Generating Store assets...")

for name, sz in [("Square44x44Logo.png", 44), ("Square150x150Logo.png", 150), ("storelogo.png", 150)]:
    pygame.image.save(scale_to(ico, sz), os.path.join(ASSETS_DIR, name))
    print(f"      {name} ({sz}x{sz})")

wide = pygame.Surface((310, 150), pygame.SRCALPHA)
wide.fill((*BG, 255))
wide.blit(scale_to(ico, 100), (10, 25))
glow = pygame.Surface((310, 150), pygame.SRCALPHA)
pygame.draw.circle(glow, (*GREEN_GLOW, 25), (60, 75), 55)
wide.blit(glow, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
f48 = pygame.font.Font(None, 48)
wide.blit(f48.render("PLAYTREE", True, GOLD), (130, 40))
f24 = pygame.font.Font(None, 24)
wide.blit(f24.render("Awaken. Rebuild. Restore Balance.", True, (150, 200, 160)), (130, 90))
pygame.image.save(wide, os.path.join(ASSETS_DIR, "Wide310x150Logo.png"))
print("      Wide310x150Logo.png (310x150)")

splash = pygame.Surface((620, 300), pygame.SRCALPHA)
splash.fill((*BG, 255))
splash.blit(scale_to(ico, 120), (250, 20))
glow2 = pygame.Surface((620, 300), pygame.SRCALPHA)
pygame.draw.circle(glow2, (*GREEN_GLOW, 30), (310, 80), 70)
splash.blit(glow2, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
f72 = pygame.font.Font(None, 72)
splash.blit(f72.render("PLAYTREE", True, (255, 245, 220)), (310 - f72.render("PLAYTREE", True, (0,0,0)).get_width() // 2, 150))
f32 = pygame.font.Font(None, 32)
splash.blit(f32.render("Chapter 0  |  Season 0", True, (150, 200, 160)), (310 - f32.render("Chapter 0  |  Season 0", True, (0,0,0)).get_width() // 2, 220))
pygame.image.save(splash, os.path.join(ASSETS_DIR, "SplashScreen.png"))
print("      SplashScreen.png (620x300)")

pygame.quit()

print("[3/5] Staging files...")
staging = os.path.join("msix", "_staging")
out_dir = os.path.join("msix", "out")
exe_path = os.path.join("dist", "PLAYTREE.exe")

if not os.path.exists(exe_path):
    print("ERROR: dist/PLAYTREE.exe not found. Run build_exe.py first.")
    sys.exit(1)

if os.path.exists(staging):
    shutil.rmtree(staging)
os.makedirs(staging, exist_ok=True)
shutil.copy2(exe_path, staging)
assets_staging = os.path.join(staging, "assets")
os.makedirs(assets_staging, exist_ok=True)
for f in os.listdir(ASSETS_DIR):
    shutil.copy2(os.path.join(ASSETS_DIR, f), assets_staging)

with open(os.path.join(staging, "AppxManifest.xml"), "w", encoding="utf-8") as f:
    f.write("""<?xml version="1.0" encoding="utf-8"?>
<Package
  xmlns="http://schemas.microsoft.com/appx/manifest/foundation/windows10"
  xmlns:uap="http://schemas.microsoft.com/appx/manifest/uap/windows10"
  xmlns:rescap="http://schemas.microsoft.com/appx/manifest/foundation/windows10/restrictedcapabilities"
  IgnorableNamespaces="uap rescap">
  <Identity Name="RQBBoxGameStudios.PLAYTREE" Publisher="CN=RQBBoxGameStudios" Version="1.0.0.0" />
  <Properties>
    <DisplayName>PLAYTREE</DisplayName>
    <PublisherDisplayName>RQBBox Game Studios</PublisherDisplayName>
    <Logo>assets\\storelogo.png</Logo>
    <Description>A stylized multiplayer fantasy adventure game. Awaken. Rebuild. Restore Balance.</Description>
  </Properties>
  <Dependencies>
    <TargetDeviceFamily Name="Windows.Desktop" MinVersion="10.0.17763.0" MaxVersionTested="10.0.22621.0" />
  </Dependencies>
  <Resources><Resource Language="en-US" /></Resources>
  <Applications>
    <Application Id="PLAYTREE" Executable="PLAYTREE.exe" EntryPoint="Windows.FullTrustApplication">
      <uap:VisualElements DisplayName="PLAYTREE" Description="PLAYTREE - Fantasy Adventure"
        BackgroundColor="transparent" Square150x150Logo="assets\\Square150x150Logo.png" Square44x44Logo="assets\\Square44x44Logo.png">
        <uap:DefaultTile Wide310x150Logo="assets\\Wide310x150Logo.png" />
        <uap:SplashScreen Image="assets\\SplashScreen.png" />
      </uap:VisualElements>
    </Application>
  </Applications>
  <Capabilities><rescap:Capability Name="runFullTrust" /></Capabilities>
</Package>""")

print("[4/5] Building MSIX...")
file_entries = []
for root, dirs, files in os.walk(staging):
    for fname in files:
        full = os.path.join(root, fname)
        rel = os.path.relpath(full, staging).replace("\\", "/")
        with open(full, "rb") as fh:
            data = fh.read()
        file_entries.append((rel, data))

if os.path.exists(out_dir):
    shutil.rmtree(out_dir)
os.makedirs(out_dir)
msix_path = os.path.join(out_dir, "PLAYTREE.msix")

with open(msix_path, "wb") as out:
    offsets = {}
    for rel, data in file_entries:
        offsets[rel] = out.tell()
        nb = rel.encode("utf-8")
        crc = zlib.crc32(data) & 0xFFFFFFFF
        lh = struct.pack("<4sHHHHHIIIHH", b"PK\x03\x04", 20, 0, 0, 0, 0, crc, len(data), len(data), len(nb), 0)
        out.write(lh + nb + data)

    cd_offset = out.tell()
    for rel, data in file_entries:
        nb = rel.encode("utf-8")
        crc = zlib.crc32(data) & 0xFFFFFFFF
        cd = struct.pack("<4sHHHHHHIIIHHHHHII", b"PK\x01\x02", 20, 20, 0, 0, 0, 0, crc, len(data), len(data), len(nb), 0, 0, 0, 0, 0x20, offsets[rel])
        out.write(cd + nb)

    cd_size = out.tell() - cd_offset
    eocd = struct.pack("<4sHHHHIIH", b"PK\x05\x06", 0, 0, len(file_entries), len(file_entries), cd_size, cd_offset, 0)
    out.write(eocd)

size_mb = os.path.getsize(msix_path) / (1024 * 1024)
print(f"[5/5] DONE! PLAYTREE.msix = {size_mb:.1f} MB")
print(f"      {os.path.abspath(msix_path)}")
print()
print("Upload to: https://partner.microsoft.com/dashboard")
