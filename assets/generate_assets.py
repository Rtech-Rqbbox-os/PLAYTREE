"""Generate banners, logos, and icons for RQBBOX / PLAYTREE - Fast version"""
import struct, zlib, os, math

def make_png(w, h, pixels):
    def chunk(t, d):
        c = t + d
        return struct.pack(">I", len(d)) + c + struct.pack(">I", zlib.crc32(c) & 0xffffffff)
    raw = b""
    for y in range(h):
        raw += b"\x00"
        for x in range(w):
            r, g, b, a = pixels[y * w + x]
            raw += struct.pack("BBBB", r, g, b, a)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))

def fill(pixels, w, h, color):
    for i in range(w * h):
        pixels[i] = (*color, 255)

def rect(pixels, w, h, rx, ry, rw, rh, color):
    for dy in range(rh):
        for dx in range(rw):
            px, py = rx+dx, ry+dy
            if 0 <= px < w and 0 <= py < h:
                pixels[py*w+px] = (*color, 255)

def circle(p, w, h, cx, cy, r, col):
    for dy in range(-r, r+1):
        for dx in range(-r, r+1):
            if dx*dx+dy*dy <= r*r:
                px, py = cx+dx, cy+dy
                if 0 <= px < w and 0 <= py < h:
                    p[py*w+px] = (*col, 255)

def vgrad(pixels, w, h, c1, c2):
    for y in range(h):
        t = y / max(1, h-1)
        c = tuple(int(c1[i]+(c2[i]-c1[i])*t) for i in range(3))
        for x in range(w):
            pixels[y*w+x] = (*c, 255)

def gen_banner():
    W, H = 400, 200
    p = [(0,0,0,0)] * (W*H)
    vgrad(p, W, H, (5,5,30), (15,35,50))
    # ground
    for y in range(H-25, H):
        t = (y-(H-25))/25
        c = tuple(int((15,40,20)[i]*(1-t)+(5,15,8)[i]*t) for i in range(3))
        for x in range(W): p[y*W+x] = (*c, 255)
    # tree
    cx = W//2
    rect(p, W, H, cx-4, H//2-15, 8, 35, (60,40,30))
    for oy, rad, col in [(0,28,(40,140,60)),(-8,20,(60,180,70)),(-15,12,(80,220,90))]:
        circle(p, W, H, cx, H//2-15+oy, rad, col)
    # gold dots
    for i in range(8):
        a = math.radians(i*45)
        gx = int(cx+math.cos(a)*38)
        gy = int(H//2-15+math.sin(a)*28)
        circle(p, W, H, gx, gy, 2, (255,215,0))
    # border
    rect(p, W, H, 0, 0, W, 2, (100,255,150))
    rect(p, W, H, 0, H-2, W, 2, (100,255,150))
    rect(p, W, H, 0, 0, 2, H, (100,255,150))
    rect(p, W, H, W-2, 0, 2, H, (100,255,150))
    # title area
    rect(p, W, H, 20, 10, W-40, 22, (10,20,15))
    rect(p, W, H, 20, 10, W-40, 22, (100,255,150))
    # "P" block letter
    rect(p, W, H, 30, 14, 4, 14, (255,245,220))
    rect(p, W, H, 34, 14, 6, 4, (255,245,220))
    rect(p, W, H, 34, 18, 6, 4, (255,245,220))
    rect(p, W, H, 38, 18, 4, 4, (255,245,220))
    # bottom
    rect(p, W, H, 50, H-18, W-100, 1, (60,120,70))
    return make_png(W, H, p)

def gen_icon(sz):
    p = [(0,0,0,0)] * (sz*sz)
    circle(p, sz, sz, sz//2, sz//2, sz//2-2, (10,30,15))
    for r in range(sz//2-2, sz//2-15, -1):
        t = (sz//2-2-r)/13
        g = int(60+t*40)
        circle(p, sz, sz, sz//2, sz//2, r, (10+int(t*20), g, 15+int(t*20)))
    cx = sz//2
    rect(p, sz, sz, cx-3, sz//2-10, 6, 20, (60,40,30))
    for oy, rad, col in [(0,18,(40,140,60)),(-6,12,(60,180,70)),(-10,7,(80,220,90))]:
        circle(p, sz, sz, cx, sz//2-10+oy, rad, col)
    for i in range(8):
        a = math.radians(i*45)
        gx = int(cx+math.cos(a)*22)
        gy = int(sz//2-10+math.sin(a)*16)
        circle(p, sz, sz, gx, gy, 2, (255,215,0))
    return make_png(sz, sz, p)

def gen_presplash():
    W, H = 256, 160
    p = [(0,0,0,0)] * (W*H)
    vgrad(p, W, H, (5,10,20), (10,20,30))
    rect(p, W, H, W//2-80, H//2-20, 160, 30, (10,20,15))
    rect(p, W, H, W//2-80, H//2-20, 160, 30, (100,255,150))
    rect(p, W, H, W//2-60, H//2+20, 120, 6, (30,50,35))
    rect(p, W, H, W//2-60, H//2+20, 40, 6, (80,255,120))
    return make_png(W, H, p)

if __name__ == "__main__":
    d = os.path.dirname(os.path.abspath(__file__))
    for name, func, args in [
        ("banner.png", gen_banner, []),
        ("icon.png", gen_icon, [512]),
        ("icon192.png", gen_icon, [192]),
        ("icon128.png", gen_icon, [128]),
        ("icon48.png", gen_icon, [48]),
        ("icon32.png", gen_icon, [32]),
        ("presplash.png", gen_presplash, []),
    ]:
        print(f"Generating {name}...")
        with open(os.path.join(d, name), "wb") as f:
            f.write(func(*args))
        sz = os.path.getsize(os.path.join(d, name))
        print(f"  Done ({sz} bytes)")
    print("All assets generated!")
