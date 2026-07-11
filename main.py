#!/usr/bin/env python3
"""
PLAYTREE — Chapter 0 : Season 0
A stylized multiplayer fantasy adventure game.
"""

import pygame
import sys
import os

if getattr(sys, 'frozen', False):
    _base = sys._MEIPASS
    os.chdir(os.path.dirname(sys.executable))
else:
    _base = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, _base)

from config import WIDTH, HEIGHT, TITLE, FPS, BLACK
from src.game import Game

def is_mobile():
    if sys.platform in ("android", "ios"):
        return True
    if hasattr(sys, "getandroidapilevel"):
        return True
    return False

def main():
    pygame.init()
    pygame.font.init()
    pygame.joystick.init()

    import os
    version_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "version.json")
    if not os.path.exists(version_path):
        try:
            import json
            with open(version_path, "w") as f:
                json.dump({"version": "1.0.0", "build_time": 1750000000}, f)
        except Exception:
            pass

    saved_settings = None
    try:
        from src.save_system import load_settings
        saved_settings = load_settings()
    except Exception:
        pass

    is_fullscreen = True
    if saved_settings and "fullscreen" in saved_settings:
        is_fullscreen = saved_settings["fullscreen"]

    # Always create the display window
    if is_mobile():
        try:
            info = pygame.display.Info()
            monitor_w, monitor_h = info.current_w, info.current_h
        except Exception:
            monitor_w, monitor_h = 1200, 800
        flags = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
        try:
            display = pygame.display.set_mode((monitor_w, monitor_h), flags)
        except Exception:
            display = pygame.display.set_mode((WIDTH, HEIGHT))
    elif is_fullscreen:
        try:
            info = pygame.display.Info()
            monitor_w, monitor_h = info.current_w, info.current_h
        except Exception:
            monitor_w, monitor_h = 1920, 1080
        flags = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
        try:
            display = pygame.display.set_mode((monitor_w, monitor_h), flags)
        except Exception:
            display = pygame.display.set_mode((WIDTH, HEIGHT))
    else:
        flags = pygame.HWSURFACE | pygame.DOUBLEBUF
        display = pygame.display.set_mode((WIDTH, HEIGHT), flags)

    pygame.display.set_caption(TITLE)
    pygame.mouse.set_visible(not is_mobile())

    # Render surface is always the game's logical size
    render_surface = pygame.Surface((WIDTH, HEIGHT))

    try:
        icon = pygame.Surface((32, 32))
        icon.fill((10, 30, 15))
        pygame.draw.circle(icon, (80, 180, 60), (16, 16), 12)
        pygame.draw.circle(icon, (100, 255, 120), (16, 12), 8)
        pygame.display.set_icon(icon)
    except:
        pass

    clock = pygame.time.Clock()
    game = Game(render_surface)
    running = True

    while running:
        dt = clock.tick(FPS) / 1000.0
        dt = min(dt, 0.05)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                is_fullscreen = not is_fullscreen
                try:
                    info = pygame.display.Info()
                    monitor_w, monitor_h = info.current_w, info.current_h
                except Exception:
                    monitor_w, monitor_h = 1920, 1080
                if is_fullscreen:
                    flags = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
                    try:
                        display = pygame.display.set_mode((monitor_w, monitor_h), flags)
                    except Exception:
                        display = pygame.display.set_mode((WIDTH, HEIGHT))
                else:
                    flags = pygame.HWSURFACE | pygame.DOUBLEBUF
                    display = pygame.display.set_mode((WIDTH, HEIGHT), flags)

        game.handle_events(events)
        game.update(dt)
        game.draw()

        # Scale render surface to fill display
        dw, dh = display.get_size()
        if dw != WIDTH or dh != HEIGHT:
            scaled = pygame.transform.smoothscale(render_surface, (dw, dh))
            display.blit(scaled, (0, 0))
        pygame.display.flip()

        if not game.running:
            running = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
