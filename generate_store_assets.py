#!/usr/bin/env python3
"""
Generate placeholder Store assets for PLAYTREE Microsoft Store submission.
Run this once to create the required logo images.
Uses pygame to generate PNGs — run from the playtree/ directory.
"""

import pygame
import os

pygame.init()

ASSETS_DIR = os.path.join("msix", "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

GREEN = (100, 255, 150)
GOLD = (255, 215, 0)
BG = (10, 10, 30)


def make_logo(size, filename):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    surf.fill((*BG, 255))

    cx, cy = size // 2, size // 2

    trunk_w = max(2, size // 20)
    trunk_h = size // 4
    pygame.draw.rect(surf, (60, 40, 30), (cx - trunk_w, cy, trunk_w * 2, trunk_h))

    r = size // 3
    for i, (color, radius) in enumerate([
        ((40, 120, 50), r),
        ((50, 150, 60), int(r * 0.78)),
        ((60, 180, 70), int(r * 0.56)),
        ((80, 200, 90), int(r * 0.35)),
    ]):
        pygame.draw.circle(surf, color, (cx, cy - size // 8), radius)

    glow = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(glow, (*GREEN, 40), (cx, cy - size // 8), r + 5)
    surf.blit(glow, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

    font_size = max(12, size // 6)
    font = pygame.font.Font(None, font_size)
    txt = font.render("PT", True, GOLD)
    surf.blit(txt, (cx - txt.get_width() // 2, cy + size // 4 + 4))

    path = os.path.join(ASSETS_DIR, filename)
    pygame.image.save(surf, path)
    print(f"Created {path} ({size}x{size})")


make_logo(150, "Square150x150Logo.png")
make_logo(44, "Square44x44Logo.png")
make_logo(50, "storelogo.png")

wide = pygame.Surface((310, 150), pygame.SRCALPHA)
wide.fill((*BG, 255))
cx, cy = 155, 60
r = 40
for color, radius in [
    ((40, 120, 50), r),
    ((50, 150, 60), int(r * 0.78)),
    ((60, 180, 70), int(r * 0.56)),
    ((80, 200, 90), int(r * 0.35)),
]:
    pygame.draw.circle(wide, color, (cx, cy), radius)
font = pygame.font.Font(None, 50)
txt = font.render("PLAYTREE", True, GOLD)
wide.blit(txt, (cx - txt.get_width() // 2, 100))
path = os.path.join(ASSETS_DIR, "Wide310x150Logo.png")
pygame.image.save(wide, path)
print(f"Created {path} (310x150)")

splash = pygame.Surface((620, 300), pygame.SRCALPHA)
splash.fill((*BG, 255))
cx, cy = 310, 120
r = 60
for color, radius in [
    ((40, 120, 50), r),
    ((50, 150, 60), int(r * 0.78)),
    ((60, 180, 70), int(r * 0.56)),
    ((80, 200, 90), int(r * 0.35)),
]:
    pygame.draw.circle(splash, color, (cx, cy), radius)
font = pygame.font.Font(None, 72)
txt = font.render("PLAYTREE", True, (255, 245, 220))
splash.blit(txt, (cx - txt.get_width() // 2, 200))
path = os.path.join(ASSETS_DIR, "SplashScreen.png")
pygame.image.save(splash, path)
print(f"Created {path} (620x300)")

print("\nAll Store assets generated. Replace with real artwork before submission.")
pygame.quit()
