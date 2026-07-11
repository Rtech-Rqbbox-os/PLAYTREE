import pygame
import math
import random
from config import *
from src.particles import ParticleSystem, StarField, GlowEffect
from src.ui import Button, xbox_icons

class MainMenu:
    def __init__(self, screen, has_save=False):
        self.screen = screen
        self.particles = ParticleSystem()
        self.stars = StarField(150)
        self.time = 0
        self.tree_sway = 0
        self.islands = self._create_islands()
        self.selected = 0
        self.hovered = -1
        self.menu_items = ["New Game", "Continue", "Locker", "Store", "Daily Rewards", "Leaderboards", "Update Log", "Settings", "Quit"]
        self.has_save = has_save
        self.transition_alpha = 0
        self.transitioning = False
        self.transition_target = None
        self.font_big = pygame.font.Font(None, 100)
        self.font_sub = pygame.font.Font(None, 36)
        self.font_menu = pygame.font.Font(None, 32)
        self.font_tiny = pygame.font.Font(None, 16)
        self.menu_rects = []
        self.audio = None
        self.prev_selected = -1
        self.music_started = False

        self.glow_orbs = [(random.randint(0, WIDTH), random.randint(0, HEIGHT),
                          random.uniform(0.5, 2), random.uniform(0, 6.28)) for _ in range(20)]

    def _create_islands(self):
        islands = []
        for i in range(5):
            x = random.randint(100, WIDTH - 100)
            y = random.randint(100, HEIGHT - 200)
            w = random.randint(60, 120)
            h = random.randint(20, 40)
            speed = random.uniform(0.1, 0.3)
            phase = random.uniform(0, 6.28)
            islands.append({"x": x, "y": y, "w": w, "h": h, "speed": speed, "phase": phase, "base_x": x})
        return islands

    def _update_menu_rects(self):
        menu_start_y = 380
        self.menu_rects = []
        for i, item in enumerate(self.menu_items):
            y = menu_start_y + i * 28
            f = self.font_menu
            txt = f"> {item} <" if self.selected == i else item
            surf = f.render(txt, True, (255, 255, 255))
            rect = surf.get_rect(center=(WIDTH // 2, y))
            rect = rect.inflate(40, 10)
            self.menu_rects.append(rect)

    def _get_item_at(self, pos):
        self._update_menu_rects()
        for i, rect in enumerate(self.menu_rects):
            if rect.collidepoint(pos):
                return i
        return -1

    def _activate_item(self, index):
        if index < 0 or index >= len(self.menu_items):
            return None
        item = self.menu_items[index]
        if item == "New Game":
            return "character_create"
        elif item == "Continue":
            if self.has_save:
                return "continue"
            return None
        elif item == "Locker":
            if self.has_save:
                return "locker"
            return None
        elif item == "Store":
            if self.has_save:
                return "store"
            return None
        elif item == "Daily Rewards":
            return "daily_rewards"
        elif item == "Leaderboards":
            return "leaderboards"
        elif item == "Update Log":
            return "update_log"
        elif item == "Settings":
            return "settings"
        elif item == "Quit":
            return "quit"
        return None

    def update(self, dt):
        self.time += dt
        self.tree_sway = math.sin(self.time * 0.3) * 0.05
        self.particles.update()

        self.particles.fountain(WIDTH // 2 + random.randint(-30, 30), HEIGHT // 2 + 100,
                               (80, 255, 120), 0.5, 2, 40, 3)
        self.particles.fountain(WIDTH // 2 + random.randint(-20, 20), HEIGHT // 2 + 120,
                               (255, 215, 0), 0.3, 1.5, 30, 2)

        for island in self.islands:
            island["x"] = island["base_x"] + math.sin(self.time * island["speed"] + island["phase"]) * 30
            island["y"] += math.sin(self.time * island["speed"] * 0.5 + island["phase"]) * 0.03

        self.glow_orbs = [(o[0] + math.sin(self.time * 0.5 + o[3]) * 0.3,
                          o[1] - 0.2, o[2], o[3]) for o in self.glow_orbs]
        self.glow_orbs = [(o[0] if o[0] > 0 and o[0] < WIDTH else random.randint(100, WIDTH-100),
                          o[1] if o[1] > 0 else HEIGHT + 20,
                          o[2], o[3]) for o in self.glow_orbs]

        self._update_menu_rects()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.selected = (self.selected - 1) % len(self.menu_items)
                if self.audio:
                    self.audio.play("menu_hover")
                return None
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected = (self.selected + 1) % len(self.menu_items)
                if self.audio:
                    self.audio.play("menu_hover")
                return None
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                if self.audio:
                    self.audio.play("menu_confirm")
                return self._activate_item(self.selected)
            elif event.key == pygame.K_ESCAPE:
                if self.audio:
                    self.audio.play("menu_select")
                return "quit"

        elif event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0:  # A
                if self.audio:
                    self.audio.play("menu_confirm")
                return self._activate_item(self.selected)
            elif event.button == 1:  # B
                if self.audio:
                    self.audio.play("menu_select")
                return "quit"
            elif event.button == 11:  # D-pad up
                self.selected = (self.selected - 1) % len(self.menu_items)
                if self.audio:
                    self.audio.play("menu_hover")
                return None
            elif event.button == 12:  # D-pad down
                self.selected = (self.selected + 1) % len(self.menu_items)
                if self.audio:
                    self.audio.play("menu_hover")
                return None
            elif event.button == 7:  # RT
                self.selected = (self.selected + 1) % len(self.menu_items)
                if self.audio:
                    self.audio.play("menu_hover")
                return None
            elif event.button == 6:  # LT
                self.selected = (self.selected - 1) % len(self.menu_items)
                if self.audio:
                    self.audio.play("menu_hover")
                return None

        elif event.type == pygame.JOYHATMOTION:
            if event.value[1] == 1:
                self.selected = (self.selected - 1) % len(self.menu_items)
                if self.audio:
                    self.audio.play("menu_hover")
            elif event.value[1] == -1:
                self.selected = (self.selected + 1) % len(self.menu_items)
                if self.audio:
                    self.audio.play("menu_hover")

        elif event.type == pygame.MOUSEMOTION:
            old = self.hovered
            self.hovered = self._get_item_at(event.pos)
            if self.hovered >= 0:
                self.selected = self.hovered
                if self.hovered != old and self.audio:
                    self.audio.play("menu_hover")
            return None

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            idx = self._get_item_at(event.pos)
            if idx >= 0:
                if self.audio:
                    self.audio.play("menu_confirm")
                return self._activate_item(idx)
            if hasattr(self, 'signin_rect') and self.signin_rect.collidepoint(event.pos):
                if self.audio:
                    self.audio.play("menu_confirm")
                return "signin"
            if hasattr(self, 'signup_rect') and self.signup_rect.collidepoint(event.pos):
                if self.audio:
                    self.audio.play("menu_confirm")
                return "signup"

        return None

    def draw(self):
        sky_top = (5, 5, 30)
        sky_bot = (20, 40, 60)
        GlowEffect.gradient_rect(self.screen, sky_top, sky_bot, (0, 0, WIDTH, HEIGHT))

        self.stars.draw(self.screen, self.time)

        for island in self.islands:
            self._draw_island(island, 0.6)

        for ox, oy, sz, _ in self.glow_orbs:
            glow = pygame.Surface((int(sz*20), int(sz*20)), pygame.SRCALPHA)
            pygame.draw.circle(glow, (*GREEN_GLOW[:3], int(15 + math.sin(self.time + ox)*5)),
                             (int(sz*10), int(sz*10)), int(sz*10))
            self.screen.blit(glow, (int(ox - sz*10), int(oy - sz*10)))

        ground_rect = (0, HEIGHT - 120, WIDTH, 120)
        GlowEffect.gradient_rect(self.screen, (10, 30, 15), (5, 15, 8), ground_rect)

        for i in range(WIDTH // 4):
            gx = i * 4
            gy = HEIGHT - 90 + math.sin(i * 0.5 + self.time * 0.5) * 5
            pygame.draw.line(self.screen, (20, 60, 25), (gx, gy), (gx, gy + 8), 1)

        self._draw_world_tree()

        for island in self.islands[2:4]:
            self._draw_island(island, 1.0)

        self.particles.draw(self.screen)

        # Title
        title_text = "PLAYTREE"
        title_y = 80
        for i in range(5, 0, -1):
            alpha = 30 // i
            glow_surf = self.font_big.render(title_text, True, (*GREEN_GLOW[:3], alpha))
            for dx, dy in [(i*2, i*2), (-i*2, i*2), (i*2, -i*2), (-i*2, -i*2)]:
                self.screen.blit(glow_surf, (WIDTH//2 - glow_surf.get_width()//2 + dx, title_y + dy))
        main_title = self.font_big.render(title_text, True, (255, 245, 220))
        self.screen.blit(main_title, (WIDTH//2 - main_title.get_width()//2, title_y))

        if self.time % 4 < 3:
            sub = self.font_sub.render(f"{CHAPTER}  \u2022  {SEASON}", True, GOLD)
            sub_rect = sub.get_rect(center=(WIDTH//2, title_y + 80))
            self.screen.blit(sub, sub_rect)

        tag = self.font_tiny.render("Awaken. Rebuild. Restore Balance.", True, (150, 200, 160))
        tag_rect = tag.get_rect(center=(WIDTH//2, title_y + 115))
        self.screen.blit(tag, tag_rect)

        menu_start_y = 380
        for i, item in enumerate(self.menu_items):
            y = menu_start_y + i * 28
            is_sel = i == self.selected
            is_hov = i == self.hovered
            active = is_sel or is_hov
            is_disabled = (item in ("Continue", "Locker", "Store")) and not self.has_save
            if is_disabled:
                color = (80, 80, 80)
            else:
                color = GOLD if active else (180, 200, 180)
            pulse = math.sin(self.time * 3) * 0.1 + 1 if active else 1
            fs = int(self.font_menu.get_height() * pulse)
            f = pygame.font.Font(None, fs)
            txt = f"> {item} <" if active else item
            if is_disabled:
                txt = f"{item} (No Save)"
            surf = f.render(txt, True, color)

            # Hover/selected glow background
            if active:
                bg_rect = surf.get_rect(center=(WIDTH // 2, y))
                bg_rect = bg_rect.inflate(60, 14)
                bg_surf = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
                glow_alpha = int(40 + math.sin(self.time * 2) * 20)
                pygame.draw.rect(bg_surf, (*GREEN_GLOW[:3], glow_alpha), bg_surf.get_rect(), border_radius=8)
                pygame.draw.rect(bg_surf, (*GREEN_GLOW[:3], glow_alpha + 20), bg_surf.get_rect(), border_radius=8, width=1)
                self.screen.blit(bg_surf, bg_rect)

                for r in range(2, 0, -1):
                    gs = f.render(txt, True, (*GREEN_GLOW[:3], 40 // max(1, r)))
                    self.screen.blit(gs, (WIDTH//2 - surf.get_width()//2 + r*3, y+r*3))
                    self.screen.blit(gs, (WIDTH//2 - surf.get_width()//2 - r*3, y-r*3))

            self.screen.blit(surf, (WIDTH//2 - surf.get_width()//2, y))

        # Sign In / Sign Up links at bottom
        link_f = pygame.font.Font(None, 18)
        link_y = HEIGHT - 48
        signin_txt = "Sign In"
        signup_txt = "Sign Up"
        signin_s = link_f.render(signin_txt, True, (100, 180, 100))
        signup_s = link_f.render(signup_txt, True, (100, 150, 200))
        gap = 30
        total_w = signin_s.get_width() + gap + signup_s.get_width()
        sx = WIDTH // 2 - total_w // 2
        self.screen.blit(signin_s, (sx, link_y))
        self.screen.blit(signup_s, (sx + signin_s.get_width() + gap, link_y))
        self.signin_rect = pygame.Rect(sx, link_y - 2, signin_s.get_width(), signin_s.get_height() + 4)
        self.signup_rect = pygame.Rect(sx + signin_s.get_width() + gap, link_y - 2, signup_s.get_width(), signup_s.get_height() + 4)

        ver = self.font_tiny.render(f"v{VERSION} — {CHAPTER} : {SEASON}", True, (80, 100, 80))
        self.screen.blit(ver, (20, HEIGHT - 20))
        copyr = self.font_tiny.render("RQBBOX GAME STUDIOS  •  RHYSTECH  •  PLAYTREE GAMES  •  2026", True, (60, 80, 60))
        self.screen.blit(copyr, (WIDTH//2 - copyr.get_width()//2, HEIGHT - 20))

        ctrl_connected = False
        try:
            ctrl_connected = pygame.joystick.get_count() > 0
        except Exception:
            pass
        if ctrl_connected:
            xbox_icons.draw_menu_prompt(self.screen, [("A", "ENTER", "Select"), ("B", "ESC", "Quit")], HEIGHT - 38)

    def _draw_world_tree(self):
        cx, cy = WIDTH // 2, HEIGHT // 2 - 20

        # Main trunk
        trunk_color = (60, 40, 30)
        trunk_rect = pygame.Rect(cx - 15, cy - 40, 30, 100)
        pygame.draw.rect(self.screen, trunk_color, trunk_rect)

        # Trunk glow
        glow = pygame.Surface((50, 120), pygame.SRCALPHA)
        pygame.draw.rect(glow, (*GREEN_GLOW[:3], 30), (10, 10, 30, 100), border_radius=10)
        self.screen.blit(glow, (cx - 25, cy - 50))

        # Branches
        branches = [(-30, -20, 40, 6), (30, -10, 35, 5), (-20, 10, 30, 5), (25, 20, 25, 4)]
        for bx, by, bw, bh in branches:
            pygame.draw.line(self.screen, trunk_color, (cx + bx, cy + by), (cx + bx - bw, cy + by - 15), bh)

        # Canopy - layered circles with glow
        canopy_colors = [(40, 120, 50), (50, 150, 60), (60, 180, 70), (80, 200, 90)]
        for i, (cc, radius) in enumerate(zip(canopy_colors, [70, 55, 40, 25])):
            sway = self.tree_sway * (radius * 0.5)
            py = cy - 30 - (70 - radius) * 0.6
            glow_r = radius + 15
            glow_s = pygame.Surface((glow_r*2, glow_r*2), pygame.SRCALPHA)
            g_alpha = int(60 - i * 10 + math.sin(self.time * 0.5 + i) * 10)
            pygame.draw.circle(glow_s, (*GREEN_GLOW[:3], g_alpha), (glow_r, glow_r), glow_r)
            self.screen.blit(glow_s, (int(cx + sway - glow_r), int(py - glow_r)))
            pygame.draw.circle(self.screen, cc, (int(cx + sway), int(py)), radius)

        # Energy particles around tree
        for i in range(8):
            a = self.time * 0.5 + i * 0.785
            r = 50 + math.sin(self.time + i) * 10
            px = cx + math.cos(a) * r
            py = cy - 30 + math.sin(a) * 20
            sz = 3 + math.sin(self.time * 2 + i) * 1
            alpha = int(100 + math.sin(self.time * 3 + i) * 50)
            p_glow = pygame.Surface((int(sz*6), int(sz*6)), pygame.SRCALPHA)
            pygame.draw.circle(p_glow, (*GOLD[:3], alpha//3), (int(sz*3), int(sz*3)), int(sz*3))
            self.screen.blit(p_glow, (int(px - sz*3), int(py - sz*3)))
            pygame.draw.circle(self.screen, (*GOLD[:3], alpha), (int(px), int(py)), sz)

        # Roots
        for i in range(3):
            angle = math.pi * (0.4 + i * 0.3)
            rx = cx + math.cos(angle) * 20
            ry = cy + 50
            for j in range(8):
                prev_x, prev_y = rx, ry
                rx += math.cos(angle + math.sin(j * 0.5) * 0.5) * 8
                ry += 5 + math.sin(j) * 3
                pygame.draw.line(self.screen, trunk_color, (int(prev_x), int(prev_y)), (int(rx), int(ry)), 3)
                if j % 2 == 0:
                    little = pygame.Surface((6, 6), pygame.SRCALPHA)
                    pygame.draw.circle(little, (*GREEN_GLOW[:3], 40), (3, 3), 3)
                    self.screen.blit(little, (int(rx) - 3, int(ry) - 3))

    def _draw_island(self, island, scale):
        x, y, w, h = island["x"], island["y"], int(island["w"] * scale), int(island["h"] * scale)
        # Island body
        island_surf = pygame.Surface((w + 10, h + 10), pygame.SRCALPHA)
        pygame.draw.ellipse(island_surf, (40, 60, 35, 180), (5, 5, w, h))
        pygame.draw.ellipse(island_surf, (60, 90, 50, 100), (5, 5, w, h), 2)
        self.screen.blit(island_surf, (x - w//2, y - h//2))

        # Grass tufts
        for i in range(w // 8):
            gx = x - w//2 + i * 8
            gy = y - h//4
            pygame.draw.line(self.screen, (40, 100, 40), (gx, gy), (gx, gy - 4), 1)

        # Small tree on island
        if scale > 0.5 and random.random() > 0.3:
            tx = x + random.randint(-w//3, w//3)
            ty = y - h//4
            pygame.draw.rect(self.screen, (60, 40, 20), (tx - 1, ty - 2, 3, 6))
            pygame.draw.circle(self.screen, (30, 80, 40), (tx, ty - 5), 5)
