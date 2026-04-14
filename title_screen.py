"""
title_screen.py  –  Animated title screen for Estoria's Chronicles (Pygame)

Replicates the mossy stone medieval RPG title: runic circle, floating magic
motes, staggered text fade-in, and a "Press Any Key" prompt.
"""

import pygame
import math
import random
from font_support import load_font

# ── Colour palette ─────────────────────────────────────────────────────────
BG       = (0x08, 0x0a, 0x08)
BG_HEX   = "#080a08"

def _hex(h):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

def _lerp_col(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


class TitleScreen:
    """Full-screen animated title rendered directly to a Surface."""

    def __init__(self, app):
        self.app    = app
        self.width  = app.width
        self.height = app.height
        self.active = True
        self._font_profile = getattr(app, "font_profile", {}) or {}

        # Preload fonts (needed before _rebuild_bg)
        self._font_title  = load_font(self._font_profile, 64, bold=True)
        self._font_sub    = load_font(self._font_profile, 26, italic=True)
        self._font_sep    = load_font(self._font_profile, 11, mono=True)
        self._font_tag    = load_font(self._font_profile, 12, mono=True)
        self._font_prompt = load_font(self._font_profile, 13, bold=True, mono=True)
        self._font_ver    = load_font(self._font_profile, 9, mono=True)
        self._font_rune   = load_font(self._font_profile, 16, bold=True, mono=True)
        self._font_rune2  = load_font(self._font_profile, 22, mono=True)

        # Pre-render the static background once
        self._bg_surf = None
        self._rebuild_bg()

        # ── Floating magic motes ────────────────────────────────────────
        self.motes = []
        mote_palettes = [
            [(0x2a, 0xb8, 0xa0), (0x40, 0xd0, 0xb0), (0x30, 0xc8, 0xa8)],
            [(0x90, 0x60, 0xd0), (0xb0, 0x80, 0xe0), (0x70, 0x40, 0xc0)],
            [(0xc0, 0xd8, 0xc0), (0xa8, 0xc8, 0xa8), (0xe0, 0xf0, 0xe0)],
            [(0x48, 0x80, 0xa0), (0x60, 0xa0, 0xc0), (0x30, 0x60, 0xa0)],
        ]
        for _ in range(80):
            palette = random.choice(mote_palettes)
            self.motes.append({
                "x": float(random.randint(0, self.width)),
                "y": float(random.randint(0, self.height)),
                "sz": random.choice([1, 1, 1, 2, 2, 3]),
                "speed": random.uniform(0.25, 0.90),
                "drift": random.uniform(-0.35, 0.35),
                "wobble": random.uniform(0, math.pi * 2),
                "col": random.choice(palette),
                "palette": palette,
            })

        # ── Text fade-in state ──────────────────────────────────────────
        self._fade_step  = 0
        self._fade_done  = False
        self._fade_timer = 0.0

        # Target colours after fade completes
        self._title_col   = BG
        self._shadow_col  = BG
        self._sub_col     = BG
        self._sep_col     = BG
        self._tag_col     = BG
        self._prompt_col  = BG
        self._ver_col     = BG

        # Final (static) colours
        self._title_final  = _hex("#d8d0a0")
        self._shadow_final = _hex("#2a3020")
        self._sub_final    = _hex("#8ac07a")
        self._sep_final    = _hex("#2a6050")
        self._tag_final    = _hex("#7a7858")
        self._prompt_final = _hex("#50c8a8")
        self._ver_final    = _hex("#2a3820")

    # ── Static background (runic circle, borders, moss) ─────────────────

    def _rebuild_bg(self):
        w, h = self.width, self.height
        surf = pygame.Surface((w, h))
        surf.fill(BG)
        cx, cy = w // 2, h // 2

        # Runic circles
        for r, col in [(210, _hex("#101812")), (175, _hex("#0e160e")),
                        (140, _hex("#0c1410")), (105, _hex("#0e1610")),
                        (70,  _hex("#101812"))]:
            pygame.draw.circle(surf, col, (cx, cy), r, 1)

        # Cardinal cross lines
        pygame.draw.line(surf, _hex("#0f1610"), (cx - 205, cy), (cx + 205, cy), 1)
        pygame.draw.line(surf, _hex("#0f1610"), (cx, cy - 205), (cx, cy + 205), 1)

        # Diagonal rune marks
        d = 148
        for dx, dy in [(d, d), (-d, d), (d, -d), (-d, -d)]:
            pygame.draw.line(surf, _hex("#121a10"),
                             (cx, cy), (cx + dx // 3, cy + dy // 3), 1)

        # Stone borders
        pygame.draw.rect(surf, _hex("#2c3020"),
                         (22, 22, w - 44, h - 44), 4)
        # Stone block courses
        for y in range(26, 48, 7):
            pygame.draw.line(surf, _hex("#1a1e16"), (26, y), (w - 26, y), 1)
        for y in range(h - 47, h - 21, 7):
            pygame.draw.line(surf, _hex("#1a1e16"), (26, y), (w - 26, y), 1)

        pygame.draw.rect(surf, _hex("#22281a"),
                         (46, 46, w - 92, h - 92), 2)
        pygame.draw.rect(surf, _hex("#2a3022"),
                         (52, 52, w - 104, h - 104), 1)

        # Mossy corner fills
        for ox, oy in [(22, 22), (w - 22, 22), (22, h - 22), (w - 22, h - 22)]:
            pygame.draw.ellipse(surf, _hex("#182014"),
                                (ox - 9, oy - 9, 18, 18))
            pygame.draw.ellipse(surf, _hex("#22281a"),
                                (ox - 9, oy - 9, 18, 18), 1)

        # Corner rune ornaments
        for ox, oy in [(68, 68), (w - 68, 68), (68, h - 68), (w - 68, h - 68)]:
            r2 = self._font_rune2.render("o", True, _hex("#1e3028"))
            surf.blit(r2, r2.get_rect(center=(ox, oy)))
            r1 = self._font_rune.render("*", True, _hex("#3a8060"))
            surf.blit(r1, r1.get_rect(center=(ox, oy)))

        # Horizontal separator lines
        sep_y_top = cy - 110
        sep_y_bot = cy + 82
        for yy in [sep_y_top, sep_y_top + 4]:
            pygame.draw.line(surf, _hex("#283420"), (90, yy), (w - 90, yy), 1)
        for yy in [sep_y_bot, sep_y_bot + 4]:
            pygame.draw.line(surf, _hex("#283420"), (90, yy), (w - 90, yy), 1)

        # Separator end markers
        fnt = self._font_sep
        for sx in [90, w - 90]:
            r = fnt.render("-", True, _hex("#3a6050"))
            surf.blit(r, r.get_rect(center=(sx, sep_y_top + 2)))
            r = fnt.render("-", True, _hex("#3a6050"))
            surf.blit(r, r.get_rect(center=(sx, sep_y_bot + 2)))

        # Side moss streaks
        for _ in range(18):
            sx = random.choice([random.randint(24, 50),
                                random.randint(w - 50, w - 24)])
            sy = random.randint(60, h - 60)
            sl = random.randint(8, 28)
            col = random.choice([_hex("#1a2416"), _hex("#182014"), _hex("#1e2818")])
            pygame.draw.line(surf, col,
                             (sx, sy), (sx + random.randint(-4, 4), sy + sl), 1)

        self._bg_surf = surf

    # ── Event handling ──────────────────────────────────────────────────

    def handle_event(self, event):
        if not self.active:
            return
        if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
            self._continue()

    def _continue(self):
        self.active = False
        self.app.start_game()

    # ── Resize ──────────────────────────────────────────────────────────

    def on_resize(self, w, h):
        self.width  = w
        self.height = h
        self._rebuild_bg()
        # Reset mote positions
        for m in self.motes:
            m["x"] = float(random.randint(0, w))
            m["y"] = float(random.randint(0, h))

    # ── Per-frame update ────────────────────────────────────────────────

    def update(self, dt):
        if not self.active:
            return

        # Mote physics
        for m in self.motes:
            m["y"] -= m["speed"]
            m["wobble"] += 0.04
            m["x"] += m["drift"] + math.sin(m["wobble"]) * 0.5
            if m["y"] < -4:
                m["y"] = float(self.height) + 4
                m["x"] = float(random.randint(0, self.width))
                m["drift"] = random.uniform(-0.3, 0.3)
                m["wobble"] = random.uniform(0, math.pi * 2)
                m["col"] = random.choice(m["palette"])

        # Fade-in timer (step every 28 ms like tkinter version)
        if not self._fade_done:
            self._fade_timer += dt
            while self._fade_timer >= 0.028 and self._fade_step < 55:
                self._fade_timer -= 0.028
                self._fade_step += 1

            t = min(self._fade_step / 40.0, 1.0)

            def lp(target, offset=0.0, span=1.0):
                tt = min(max((t - offset) / span, 0.0), 1.0)
                return _lerp_col(BG, target, tt)

            self._shadow_col = lp(_hex("#1a2414"), 0.0, 0.5)
            self._title_col  = lp(_hex("#c8c090"), 0.0, 0.6)
            self._sub_col    = lp(_hex("#7aaa6a"), 0.2, 0.6)
            self._sep_col    = lp(_hex("#2a6050"), 0.35, 0.5)
            self._tag_col    = lp(_hex("#7a7858"), 0.45, 0.45)
            self._prompt_col = lp(_hex("#40a890"), 0.70, 0.30)
            self._ver_col    = lp(_hex("#2a3820"), 0.80, 0.20)

            if self._fade_step >= 55:
                self._fade_done = True
                self._title_col  = self._title_final
                self._shadow_col = self._shadow_final
                self._sub_col    = self._sub_final
                self._prompt_col = self._prompt_final

    # ── Render (called before pygame_gui draw_ui) ───────────────────────

    def render(self, surface):
        if not self.active:
            return

        # Blit static background
        if self._bg_surf:
            surface.blit(self._bg_surf, (0, 0))

        # Draw motes
        for m in self.motes:
            x, y, sz = int(m["x"]), int(m["y"]), m["sz"]
            if sz <= 1:
                surface.set_at((x, y), m["col"])
            else:
                pygame.draw.rect(surface, m["col"], (x, y, sz, sz))

    def render_overlay(self, surface):
        """Text drawn AFTER pygame_gui so it's always on top."""
        if not self.active:
            return

        cx = self.width // 2
        cy = self.height // 2

        # Shadow text
        s = self._font_title.render("ESTORIA'S", True, self._shadow_col)
        surface.blit(s, s.get_rect(center=(cx + 3, cy - 126)))

        # Main title
        t = self._font_title.render("ESTORIA'S", True, self._title_col)
        surface.blit(t, t.get_rect(center=(cx, cy - 130)))

        # Subtitle
        su = self._font_sub.render("C H R O N I C L E S", True, self._sub_col)
        surface.blit(su, su.get_rect(center=(cx, cy - 50)))

        # Separator
        sp = self._font_sep.render(
            "- * - * - * - * - * - * - * -", True, self._sep_col)
        surface.blit(sp, sp.get_rect(center=(cx, cy - 14)))

        # Taglines
        t1 = self._font_tag.render(
            "Discover ancient dungeons. Master powerful skills.",
            True, self._tag_col)
        surface.blit(t1, t1.get_rect(center=(cx, cy + 22)))
        t2 = self._font_tag.render(
            "Grow stronger. Uncover the world's secrets.",
            True, self._tag_col)
        surface.blit(t2, t2.get_rect(center=(cx, cy + 46)))

        # Prompt
        pr = self._font_prompt.render(
            "-  Press  ANY BUTTON  to  Begin  Your  Journey  -",
            True, self._prompt_col)
        surface.blit(pr, pr.get_rect(center=(cx, cy + 126)))

        # Version
        vr = self._font_ver.render("v1.0", True, self._ver_col)
        surface.blit(vr, vr.get_rect(center=(self.width - 65, self.height - 55)))

    # ── Cleanup ─────────────────────────────────────────────────────────

    def cleanup(self):
        self.active = False
        self._bg_surf = None
        self.motes.clear()
