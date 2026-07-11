import pygame
import math
import sys

IS_MOBILE = sys.platform in ("android", "ios") or hasattr(sys, "getandroidapilevel")

class VirtualJoystick:
    def __init__(self, x, y, radius=60):
        self.base_x = x
        self.base_y = y
        self.radius = radius
        self.knob_x = x
        self.knob_y = y
        self.active = False
        self.finger_id = None
        self.dx = 0.0
        self.dy = 0.0

    def handle_event(self, event):
        if event.type == pygame.FINGERDOWN:
            fx = event.x * pygame.display.get_surface().get_width()
            fy = event.y * pygame.display.get_surface().get_height()
            dist = math.hypot(fx - self.base_x, fy - self.base_y)
            if dist < self.radius * 1.5:
                self.active = True
                self.finger_id = event.finger_id
                self._update(fx, fy)
                return True
        elif event.type == pygame.FINGERUP:
            if event.finger_id == self.finger_id:
                self.active = False
                self.finger_id = None
                self.knob_x = self.base_x
                self.knob_y = self.base_y
                self.dx = 0.0
                self.dy = 0.0
                return True
        elif event.type == pygame.FINGERMOTION:
            if event.finger_id == self.finger_id:
                fx = event.x * pygame.display.get_surface().get_width()
                fy = event.y * pygame.display.get_surface().get_height()
                self._update(fx, fy)
                return True
        return False

    def _update(self, fx, fy):
        dx = fx - self.base_x
        dy = fy - self.base_y
        dist = math.hypot(dx, dy)
        if dist > self.radius:
            dx = dx / dist * self.radius
            dy = dy / dist * self.radius
            dist = self.radius
        self.knob_x = self.base_x + dx
        self.knob_y = self.base_y + dy
        self.dx = dx / self.radius if self.radius > 0 else 0
        self.dy = dy / self.radius if self.radius > 0 else 0

    def draw(self, surface):
        alpha_surface = pygame.Surface((self.radius * 2 + 20, self.radius * 2 + 20), pygame.SRCALPHA)
        cx = self.radius + 10
        cy = self.radius + 10
        pygame.draw.circle(alpha_surface, (80, 255, 120, 40), (cx, cy), self.radius)
        pygame.draw.circle(alpha_surface, (80, 255, 120, 80), (cx, cy), self.radius, 2)
        knob_dx = self.knob_x - self.base_x
        knob_dy = self.knob_y - self.base_y
        pygame.draw.circle(alpha_surface, (80, 255, 120, 150), (int(cx + knob_dx), int(cy + knob_dy)), 22)
        pygame.draw.circle(alpha_surface, (80, 255, 120, 200), (int(cx + knob_dx), int(cy + knob_dy)), 22, 2)
        surface.blit(alpha_surface, (self.base_x - cx, self.base_y - cy))


class TouchButton:
    def __init__(self, x, y, radius, label, color=(80, 255, 120)):
        self.x = x
        self.y = y
        self.radius = radius
        self.label = label
        self.color = color
        self.pressed = False
        self.finger_id = None
        self.press_time = 0
        self._was_pressed = False
        self._cooldown = 0

    def handle_event(self, event):
        if event.type == pygame.FINGERDOWN:
            fx = event.x * pygame.display.get_surface().get_width()
            fy = event.y * pygame.display.get_surface().get_height()
            dist = math.hypot(fx - self.x, fy - self.y)
            if dist < self.radius * 1.3:
                self.pressed = True
                self.finger_id = event.finger_id
                self.press_time = pygame.time.get_ticks()
                return True
        elif event.type == pygame.FINGERUP:
            if event.finger_id == self.finger_id:
                self.pressed = False
                self.finger_id = None
                return True
        return False

    def just_pressed(self):
        now = self.pressed
        was = self._was_pressed
        self._was_pressed = now
        return now and not was

    def is_pressed(self):
        return self.pressed

    def draw(self, surface):
        alpha_surface = pygame.Surface((self.radius * 2 + 4, self.radius * 2 + 4), pygame.SRCALPHA)
        cx = self.radius + 2
        cy = self.radius + 2
        bg_alpha = 100 if self.pressed else 50
        border_alpha = 200 if self.pressed else 100
        bg_color = (*self.color[:3], bg_alpha)
        border_color = (*self.color[:3], border_alpha)
        pygame.draw.circle(alpha_surface, bg_color, (cx, cy), self.radius)
        pygame.draw.circle(alpha_surface, border_color, (cx, cy), self.radius, 2)
        font = pygame.font.Font(None, 24)
        txt = font.render(self.label, True, self.color)
        txt_rect = txt.get_rect(center=(cx, cy))
        alpha_surface.blit(txt, txt_rect)
        surface.blit(alpha_surface, (self.x - cx, self.y - cy))


class TouchControls:
    def __init__(self, screen_w=1280, screen_h=720):
        self.screen_w = screen_w
        self.screen_h = screen_h
        margin = 30
        btn_r = 28
        spacing = 70

        self.joystick = VirtualJoystick(margin + 70, screen_h - margin - 70, radius=55)

        attack_x = screen_w - margin - 50
        attack_y = screen_h - margin - 160
        self.attack_btn = TouchButton(attack_x, attack_y, btn_r, "ATK", (255, 80, 80))

        dodge_x = screen_w - margin - 50 - spacing
        dodge_y = screen_h - margin - 100
        self.dodge_btn = TouchButton(dodge_x, dodge_y, btn_r, "DGE", (80, 180, 255))

        special_x = screen_w - margin - 50
        special_y = screen_h - margin - 80
        self.special_btn = TouchButton(special_x, special_y, btn_r, "SPL", (255, 200, 50))

        interact_x = screen_w - margin - 50 - spacing
        interact_y = screen_h - margin - 170
        self.interact_btn = TouchButton(interact_x, interact_y, btn_r * 0.8, "ACT", (100, 255, 180))

        potion_x = screen_w - margin - 50 - spacing * 2
        potion_y = screen_h - margin - 130
        self.potion_btn = TouchButton(potion_x, potion_y, btn_r * 0.7, "POT", (60, 200, 60))

        inv_x = margin + 70
        inv_y = margin + 70
        self.inventory_btn = TouchButton(inv_x, inv_y, btn_r * 0.8, "INV", (200, 180, 100))

        craft_x = margin + 70 + spacing
        craft_y = margin + 70
        self.craft_btn = TouchButton(craft_x, craft_y, btn_r * 0.8, "CRF", (180, 140, 80))

        mount_x = margin + 70
        mount_y = margin + 70 + spacing
        self.mount_btn = TouchButton(mount_x, mount_y, btn_r * 0.7, "MNT", (150, 200, 255))

        self.all_buttons = [self.attack_btn, self.dodge_btn, self.special_btn,
                           self.interact_btn, self.potion_btn, self.inventory_btn,
                           self.craft_btn, self.mount_btn]

        self.menu_btn = TouchButton(screen_w // 2, margin + 30, btn_r * 0.7, "|||", (200, 200, 200))

        self.enabled = IS_MOBILE

    def handle_event(self, event):
        if not self.enabled:
            return False
        if self.joystick.handle_event(event):
            return True
        if self.menu_btn.handle_event(event):
            return True
        for btn in self.all_buttons:
            if btn.handle_event(event):
                return True
        return False

    def draw(self, surface):
        if not self.enabled:
            return
        self.joystick.draw(surface)
        self.menu_btn.draw(surface)
        for btn in self.all_buttons:
            btn.draw(surface)

    def get_movement(self):
        return self.joystick.dx, self.joystick.dy


def detect_mobile():
    if sys.platform in ("android", "ios"):
        return True
    if hasattr(sys, "getandroidapilevel"):
        return True
    try:
        import os
        if os.path.exists("/system/build.prop"):
            return True
    except Exception:
        pass
    return False
