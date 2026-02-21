"""
travel_animation.py  –  ASCII sailing animation overlay (Pygame)

Shows a small ship moving across wave-lines, with day-labels,
then an "Anchor Dropped" frame, before auto-dismissing.
"""

import pygame

BG   = (0x0a, 0x0a, 0x14)
CYAN = (0x00, 0xcc, 0xff)
BLUE = (0x88, 0xdd, 0xff)
DIM  = (0x44, 0x66, 0x88)
LINE_COL = (0x1a, 0x3a, 0x5a)

WIDTH_CHARS  = 56

# Ship pieces
SAIL_TOP = "  |  "
SAIL_MID = " [-] "
HULL     = "\\_O_/"

WAVE_A = ("\u2248" * WIDTH_CHARS)[:WIDTH_CHARS]
WAVE_B = ("~ " * (WIDTH_CHARS // 2 + 1))[:WIDTH_CHARS]
WAVE_C = (" ~" * (WIDTH_CHARS // 2 + 1))[:WIDTH_CHARS]

POSITIONS = [1, 7, 13, 19, 25, 31, 37, 43, 49]
DAY_LABELS = [
    "Leaving port\u2026", "Day 1 at sea\u2026", "Day 2 at sea\u2026",
    "Day 3 at sea\u2026", "Day 4 at sea\u2026", "Day 5 at sea\u2026",
    "Day 6 at sea\u2026", "Nearing land\u2026", "Land ahoy!",
]
WAVE_CYCLE = [WAVE_A, WAVE_B, WAVE_C, WAVE_B]


class TravelOverlay:
    """
    Covers the game window with a sailing animation.

    When done, ``self.done`` is True and ``self.deferred_text`` holds
    the travel result text to be appended by the caller.
    """

    def __init__(self, width, height, island_name, deferred_text):
        self.width  = width
        self.height = height
        self.island_name   = island_name
        self.deferred_text = deferred_text
        self.done   = False

        # Build frames
        self._frames = []
        for i, pos in enumerate(POSITIONS):
            p = min(pos, WIDTH_CHARS - 5)
            l1 = " " * p + SAIL_TOP
            l2 = " " * p + SAIL_MID
            l3 = " " * p + HULL
            w1 = WAVE_CYCLE[i % 4]
            w2 = WAVE_CYCLE[(i + 1) % 4]
            w3 = WAVE_CYCLE[(i + 2) % 4]
            self._frames.append((
                [l1, l2, l3, w1, w2, w3],
                DAY_LABELS[i],
            ))

        # Arrival frame
        short = island_name[:24]
        arr_lines = [
            "",
            f"       \u2693  ANCHOR DROPPED  \u2693",
            "",
            "   " + "\u2550" * 36,
            f"       {short:^24}",
            "   " + "\u2550" * 36,
        ]
        self._frames.append((arr_lines, f"Arrived at {island_name}!"))

        self._frame_idx = 0
        self._timer     = 0.0
        self._interval  = 0.22       # 220 ms per frame
        self._hold      = 1.4        # 1.4 s on arrival

        # Fonts
        self._font_hdr    = pygame.font.SysFont("Consolas", 13, bold=True)
        self._font_body   = pygame.font.SysFont("Consolas", 11)
        self._font_status = pygame.font.SysFont("Consolas", 10)

    def update(self, dt):
        if self.done:
            return
        self._timer += dt

        last = len(self._frames) - 1
        if self._frame_idx < last:
            if self._timer >= self._interval:
                self._timer -= self._interval
                self._frame_idx += 1
        else:
            # Hold on arrival frame
            if self._timer >= self._hold:
                self.done = True

    def render(self, surface):
        if self.done:
            return

        # Overlay box in center
        bw, bh = 620, 310
        bx = (self.width  - bw) // 2
        by = (self.height - bh) // 2

        # Background
        pygame.draw.rect(surface, BG, (bx, by, bw, bh))
        pygame.draw.rect(surface, LINE_COL, (bx, by, bw, bh), 2)

        # Header
        hdr_text = (f"  \u26f5  SETTING SAIL  \u2192  "
                    f"{self.island_name.upper()}  \u2693 ")
        hdr_r = self._font_hdr.render(hdr_text, True, CYAN)
        surface.blit(hdr_r, hdr_r.get_rect(
            center=(bx + bw // 2, by + 24)))

        # Separator line
        pygame.draw.line(surface, LINE_COL,
                         (bx + 16, by + 44), (bx + bw - 16, by + 44), 1)

        # Frame lines
        lines, status = self._frames[self._frame_idx]
        y = by + 56
        for line in lines:
            r = self._font_body.render(line, True, BLUE)
            surface.blit(r, (bx + 20, y))
            y += 22

        # Bottom separator
        pygame.draw.line(surface, LINE_COL,
                         (bx + 16, by + bh - 50), (bx + bw - 16, by + bh - 50), 1)

        # Status label
        st = self._font_status.render(status, True, DIM)
        surface.blit(st, st.get_rect(center=(bx + bw // 2, by + bh - 28)))
