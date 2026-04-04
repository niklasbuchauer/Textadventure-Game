"""Intro-matched quit outro overlay with save progress for pygame shutdown."""

import math
import random

import pygame

from ui_animation import clamp01, ease_in_out_cubic


BG = (0x08, 0x0A, 0x08)


def _hex(h):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


class QuitOutroOverlay:
    """Full-screen outro that mirrors title style and blocks until done."""

    def __init__(self, width, height, duration=1.5):
        self.width = int(width)
        self.height = int(height)
        self.duration = max(0.8, float(duration))

        self.done = False
        self.elapsed = 0.0
        self.save_started = False
        self.save_finished = False
        self.save_error = None

        self._bar_progress = 0.0
        self._post_save_timer = 0.0

        self._font_title = pygame.font.SysFont("Georgia", 58, bold=True)
        self._font_sub = pygame.font.SysFont("Georgia", 24, italic=True)
        self._font_sep = pygame.font.SysFont("Courier New", 11)
        self._font_tag = pygame.font.SysFont("Courier New", 12)
        self._font_status = pygame.font.SysFont("Courier New", 12, bold=True)
        self._font_pct = pygame.font.SysFont("Courier New", 10)

        self._bg_surf = None
        self._rebuild_bg()

        mote_palettes = [
            [(0x2A, 0xB8, 0xA0), (0x40, 0xD0, 0xB0), (0x30, 0xC8, 0xA8)],
            [(0x90, 0x60, 0xD0), (0xB0, 0x80, 0xE0), (0x70, 0x40, 0xC0)],
            [(0xC0, 0xD8, 0xC0), (0xA8, 0xC8, 0xA8), (0xE0, 0xF0, 0xE0)],
            [(0x48, 0x80, 0xA0), (0x60, 0xA0, 0xC0), (0x30, 0x60, 0xA0)],
        ]
        self.motes = []
        for _ in range(72):
            palette = random.choice(mote_palettes)
            self.motes.append({
                "x": float(random.randint(0, self.width)),
                "y": float(random.randint(0, self.height)),
                "sz": random.choice([1, 1, 2, 2, 3]),
                "speed": random.uniform(0.35, 1.05),
                "drift": random.uniform(-0.22, 0.22),
                "wobble": random.uniform(0.0, math.pi * 2.0),
                "col": random.choice(palette),
                "palette": palette,
            })

    def _rebuild_bg(self):
        w, h = self.width, self.height
        surf = pygame.Surface((w, h))
        surf.fill(BG)
        cx, cy = w // 2, h // 2

        for r, col in [(210, _hex("#0E140F")), (175, _hex("#0D130E")),
                       (140, _hex("#0C120E")), (105, _hex("#0D130E")),
                       (70, _hex("#101812"))]:
            pygame.draw.circle(surf, col, (cx, cy), r, 1)

        pygame.draw.line(surf, _hex("#0F1610"), (cx - 205, cy), (cx + 205, cy), 1)
        pygame.draw.line(surf, _hex("#0F1610"), (cx, cy - 205), (cx, cy + 205), 1)

        d = 148
        for dx, dy in [(d, d), (-d, d), (d, -d), (-d, -d)]:
            pygame.draw.line(surf, _hex("#121A10"), (cx, cy), (cx + dx // 3, cy + dy // 3), 1)

        pygame.draw.rect(surf, _hex("#2C3020"), (22, 22, w - 44, h - 44), 4)
        pygame.draw.rect(surf, _hex("#22281A"), (46, 46, w - 92, h - 92), 2)
        pygame.draw.rect(surf, _hex("#2A3022"), (52, 52, w - 104, h - 104), 1)

        self._bg_surf = surf

    def on_resize(self, width, height):
        self.width = int(width)
        self.height = int(height)
        self._rebuild_bg()

    def should_start_save(self):
        return (not self.save_started) and (self.elapsed >= self.duration)

    def mark_save_started(self):
        self.save_started = True

    def mark_save_finished(self, error=None):
        self.save_finished = True
        self.save_error = error
        self._bar_progress = max(self._bar_progress, 0.95 if error is None else 0.90)

    def update(self, dt):
        if self.done:
            return

        self.elapsed += max(0.0, float(dt))

        for m in self.motes:
            m["y"] += m["speed"]
            m["wobble"] += 0.038
            m["x"] += m["drift"] + math.sin(m["wobble"]) * 0.38
            if m["y"] > self.height + 4:
                m["y"] = -4.0
                m["x"] = float(random.randint(0, self.width))
                m["drift"] = random.uniform(-0.2, 0.2)
                m["wobble"] = random.uniform(0.0, math.pi * 2.0)
                m["col"] = random.choice(m["palette"])

        timed_t = clamp01(self.elapsed / self.duration)
        timed_progress = 0.92 * ease_in_out_cubic(timed_t)
        self._bar_progress = max(self._bar_progress, timed_progress)

        if self.save_finished:
            self._post_save_timer += dt
            self._bar_progress = min(1.0, self._bar_progress + dt * 1.6)
            if self._bar_progress >= 0.999 and self._post_save_timer >= 0.18:
                self.done = True

    def render(self, surface):
        if self.done:
            return

        if self._bg_surf:
            surface.blit(self._bg_surf, (0, 0))

        for m in self.motes:
            x = int(m["x"])
            y = int(m["y"])
            sz = m["sz"]
            if sz <= 1:
                if 0 <= x < self.width and 0 <= y < self.height:
                    surface.set_at((x, y), m["col"])
            else:
                pygame.draw.rect(surface, m["col"], (x, y, sz, sz))

        veil = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        fade_t = clamp01(self.elapsed / self.duration)
        veil.fill((6, 8, 6, int(40 + 165 * fade_t)))
        surface.blit(veil, (0, 0))

        cx = self.width // 2
        cy = self.height // 2

        shadow_col = _hex("#1A2414")
        title_col = _hex("#C8C090")
        sub_col = _hex("#7AAA6A")
        sep_col = _hex("#2A6050")
        tag_col = _hex("#7A7858")
        status_col = _hex("#50C8A8") if self.save_error is None else _hex("#D9A37D")

        s = self._font_title.render("ESTORIA'S", True, shadow_col)
        surface.blit(s, s.get_rect(center=(cx + 3, cy - 126)))
        t = self._font_title.render("ESTORIA'S", True, title_col)
        surface.blit(t, t.get_rect(center=(cx, cy - 130)))
        su = self._font_sub.render("C H R O N I C L E S", True, sub_col)
        surface.blit(su, su.get_rect(center=(cx, cy - 52)))
        sp = self._font_sep.render("- * - * - * - * - * - * - * -", True, sep_col)
        surface.blit(sp, sp.get_rect(center=(cx, cy - 14)))

        goodbye = self._font_tag.render("Securing your journey in the chronicles...", True, tag_col)
        surface.blit(goodbye, goodbye.get_rect(center=(cx, cy + 28)))

        if not self.save_started:
            status = "Preparing final records..."
        elif not self.save_finished:
            status = "Saving world state..."
        elif self.save_error is None:
            status = "Save complete. Closing the chronicle..."
        else:
            status = "Save encountered an issue. Closing safely..."

        st = self._font_status.render(status, True, status_col)
        surface.blit(st, st.get_rect(center=(cx, cy + 88)))

        bar_w = max(260, min(540, int(self.width * 0.44)))
        bar_h = 14
        bx = cx - bar_w // 2
        by = cy + 124

        pygame.draw.rect(surface, _hex("#1C241C"), (bx, by, bar_w, bar_h), border_radius=3)
        fill_w = int(bar_w * clamp01(self._bar_progress))
        if fill_w > 0:
            pygame.draw.rect(surface, _hex("#50C8A8"), (bx, by, fill_w, bar_h), border_radius=3)
        pygame.draw.rect(surface, _hex("#3A6050"), (bx, by, bar_w, bar_h), 1, border_radius=3)

        pct = int(round(clamp01(self._bar_progress) * 100.0))
        pct_text = self._font_pct.render(f"{pct}%", True, _hex("#A7D8C8"))
        surface.blit(pct_text, pct_text.get_rect(center=(cx, by + 24)))