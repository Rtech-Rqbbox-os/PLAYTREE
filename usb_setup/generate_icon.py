#!/usr/bin/env python3
"""Generate PLAYTREE .ico icon file"""
import struct
import zlib

def create_png(width, height, pixels):
    def chunk(chunk_type, data):
        c = chunk_type + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xffffffff)

    raw = b""
    for y in range(height):
        raw += b"\x00"
        for x in range(width):
            r, g, b, a = pixels[y * width + x]
            raw += bytes([r, g, b, a])

    ihdr = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", ihdr)
        + chunk(b"IDAT", zlib.compress(raw))
        + chunk(b"IEND", b"")
    )

def generate_icon():
    SIZE = 64
    pixels = [(0, 0, 0, 0)] * (SIZE * SIZE)

    def set_pixel(x, y, r, g, b, a=255):
        if 0 <= x < SIZE and 0 <= y < SIZE:
            pixels[y * SIZE + x] = (r, g, b, a)

    def fill_circle(cx, cy, radius, r, g, b, a=255):
        for y in range(cy - radius, cy + radius + 1):
            for x in range(cx - radius, cx + radius + 1):
                if (x - cx) ** 2 + (y - cy) ** 2 <= radius ** 2:
                    set_pixel(x, y, r, g, b, a)

    # Dark background
    for y in range(SIZE):
        for x in range(SIZE):
            set_pixel(x, y, 10, 30, 15, 255)

    # Tree trunk
    for y in range(38, 55):
        for x in range(30, 34):
            set_pixel(x, y, 80, 50, 30, 255)

    # Tree canopy layers
    fill_circle(32, 28, 14, 40, 120, 50, 255)
    fill_circle(32, 24, 10, 50, 150, 60, 255)
    fill_circle(32, 22, 6, 60, 180, 70, 255)

    # Glow center
    fill_circle(32, 20, 3, 100, 255, 120, 200)

    # Energy particles
    fill_circle(28, 18, 1, 255, 215, 0, 200)
    fill_circle(36, 22, 1, 255, 215, 0, 200)
    fill_circle(32, 16, 1, 255, 215, 0, 180)
    fill_circle(26, 24, 1, 80, 255, 120, 160)
    fill_circle(38, 18, 1, 80, 255, 120, 160)

    return pixels

def main():
    pixels = generate_icon()
    png_data = create_png(64, 64, pixels)

    # Create ICO file (single 64x64 image)
    # ICO format: header + entry + PNG data
    num_images = 1
    header = struct.pack("<HHH", 0, 1, num_images)  # reserved, type=ico, count
    entry = struct.pack("<BBBBHHII",
        64,    # width
        64,    # height
        0,     # colors (0 = >8bpp)
        0,     # reserved
        1,     # color planes
        32,    # bits per pixel
        len(png_data),  # size of image data
        6 + 16  # offset (header + 1 entry)
    )

    ico_data = header + entry + png_data

    ico_path = "playtree.ico"
    with open(ico_path, "wb") as f:
        f.write(ico_data)
    print(f"Created {ico_path} ({len(ico_data)} bytes)")

    # Also save as PNG for reference
    with open("playtree_icon.png", "wb") as f:
        f.write(png_data)
    print(f"Created playtree_icon.png ({len(png_data)} bytes)")

if __name__ == "__main__":
    main()
