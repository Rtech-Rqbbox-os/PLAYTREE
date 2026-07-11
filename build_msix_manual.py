"""
Build PLAYTREE.msix manually — no Windows SDK required.
"""
import os
import shutil
import hashlib
import zlib
import struct


def sha256(data):
    return hashlib.sha256(data).digest()


def build_msix():
    staging = os.path.join("msix", "_staging")
    out_dir = os.path.join("msix", "out")
    exe_path = os.path.join("dist", "PLAYTREE.exe")
    msix_path = os.path.join(out_dir, "PLAYTREE.msix")

    if not os.path.exists(exe_path):
        print("ERROR: dist/PLAYTREE.exe not found. Run build_exe.py first.")
        return False

    os.makedirs(out_dir, exist_ok=True)
    if os.path.exists(staging):
        shutil.rmtree(staging, ignore_errors=True)
    os.makedirs(staging, exist_ok=True)

    print("[1/4] Staging files...")
    shutil.copy2(exe_path, staging)
    assets_dir = os.path.join(staging, "assets")
    os.makedirs(assets_dir, exist_ok=True)
    for f in os.listdir(os.path.join("msix", "assets")):
        shutil.copy2(os.path.join("msix", "assets", f), assets_dir)

    manifest_path = os.path.join(staging, "AppxManifest.xml")
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write(manifest_xml_content())

    print("[2/4] Collecting files...")
    file_entries = []
    for root, dirs, files in os.walk(staging):
        for fname in files:
            full = os.path.join(root, fname)
            rel = os.path.relpath(full, staging).replace("\\", "/")
            with open(full, "rb") as fh:
                data = fh.read()
            file_entries.append((rel, data))

    print("[3/4] Building MSIX package...")
    with open(msix_path, "wb") as out:
        offsets = {}
        for rel, data in file_entries:
            offsets[rel] = out.tell()
            name_bytes = rel.encode("utf-8")
            crc = zlib.crc32(data) & 0xFFFFFFFF
            lh = struct.pack(
                "<4sHHHHHIIIHH",
                b"PK\x03\x04",   # signature
                20,               # version needed
                0,                # flags
                0,                # method (stored)
                0,                # mod time
                0,                # mod date
                crc,              # crc32
                len(data),        # compressed size
                len(data),        # uncompressed size
                len(name_bytes),  # name length
                0,                # extra length
            )
            out.write(lh)
            out.write(name_bytes)
            out.write(data)

        cd_offset = out.tell()
        for rel, data in file_entries:
            name_bytes = rel.encode("utf-8")
            crc = zlib.crc32(data) & 0xFFFFFFFF
            cd = struct.pack(
                "<4sHHHHHHIIIHHHHHII",
                b"PK\x01\x02",       # signature
                20,                   # version made by
                20,                   # version needed
                0,                    # flags
                0,                    # method
                0,                    # mod time
                0,                    # mod date
                crc,                  # crc32
                len(data),            # compressed size
                len(data),            # uncompressed size
                len(name_bytes),      # name length
                0,                    # extra length
                0,                    # comment length
                0,                    # disk start
                0,                    # internal attrs
                0x20,                 # external attrs (archive)
                offsets[rel],         # local header offset
            )
            out.write(cd)
            out.write(name_bytes)

        cd_size = out.tell() - cd_offset

        eocd = struct.pack(
            "<4sHHHHIIH",
            b"PK\x05\x06",       # signature
            0,                    # disk number
            0,                    # disk with cd
            len(file_entries),    # entries on disk
            len(file_entries),    # total entries
            cd_size,              # cd size
            cd_offset,            # cd offset
            0,                    # comment length
        )
        out.write(eocd)

    size_mb = os.path.getsize(msix_path) / (1024 * 1024)
    print(f"[4/4] Done! Size: {size_mb:.1f} MB")
    print(f"      Output: {os.path.abspath(msix_path)}")
    return True


def manifest_xml_content():
    return (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<Package\n'
        '  xmlns="http://schemas.microsoft.com/appx/manifest/foundation/windows10"\n'
        '  xmlns:uap="http://schemas.microsoft.com/appx/manifest/uap/windows10"\n'
        '  xmlns:rescap="http://schemas.microsoft.com/appx/manifest/foundation/windows10/restrictedcapabilities"\n'
        '  IgnorableNamespaces="uap rescap">\n'
        '\n'
        '  <Identity\n'
        '    Name="RQBBoxGameStudios.PLAYTREE"\n'
        '    Publisher="CN=RQBBox Game Studios"\n'
        '    Version="1.0.0.0" />\n'
        '\n'
        '  <Properties>\n'
        '    <DisplayName>PLAYTREE</DisplayName>\n'
        '    <PublisherDisplayName>RQBBox Game Studios</PublisherDisplayName>\n'
        '    <Logo>assets\\storelogo.png</Logo>\n'
        '    <Description>A stylized multiplayer fantasy adventure game.</Description>\n'
        '  </Properties>\n'
        '\n'
        '  <Dependencies>\n'
        '    <TargetDeviceFamily Name="Windows.Desktop" MinVersion="10.0.17763.0" MaxVersionTested="10.0.22621.0" />\n'
        '  </Dependencies>\n'
        '\n'
        '  <Resources>\n'
        '    <Resource Language="en-US" />\n'
        '  </Resources>\n'
        '\n'
        '  <Applications>\n'
        '    <Application Id="PLAYTREE"\n'
        '      Executable="PLAYTREE.exe"\n'
        '      EntryPoint="Windows.FullTrustApplication">\n'
        '      <uap:VisualElements\n'
        '        DisplayName="PLAYTREE"\n'
        '        Description="A stylized multiplayer fantasy adventure game"\n'
        '        BackgroundColor="transparent"\n'
        '        Square150x150Logo="assets\\Square150x150Logo.png"\n'
        '        Square44x44Logo="assets\\Square44x44Logo.png">\n'
        '        <uap:DefaultTile Wide310x150Logo="assets\\Wide310x150Logo.png" />\n'
        '        <uap:SplashScreen Image="assets\\SplashScreen.png" />\n'
        '      </uap:VisualElements>\n'
        '    </Application>\n'
        '  </Applications>\n'
        '\n'
        '  <Capabilities>\n'
        '    <rescap:Capability Name="runFullTrust" />\n'
        '  </Capabilities>\n'
        '\n'
        '</Package>'
    )


if __name__ == "__main__":
    build_msix()
