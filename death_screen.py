"""
death_screen.py  –  5-second death overlay (Pygame)

Displays a red skull ASCII art, "YOU HAVE FALLEN" text, and a countdown
before auto-dismissing and showing the respawn text.
"""

import pygame

BG = (0x0a, 0x0a, 0x0a)
RED = (0xcc, 0x00, 0x00)
GREY = (0x88, 0x88, 0x88)
DIM = (0x55, 0x55, 0x55)

SKULL = [
    "  ░░░░░░░░░░░░░░░░░░░░░  ",
    " ░░  ██████████████  ░░ ",
    "░░  ██  ██    ██  ██  ░░",
    "░░  ██████    ██████  ░░",
    "░░    ████████████    ░░",
    "░░  ████  ████  ████  ░░",
    " ░░  ██████  ██████  ░░ ",
    "  ░░░░░░░░░░░░░░░░░░░  ",
]


class DeathOverlay:
    """
    Covers the game window for 5 seconds, then sets ``self.done = True``.

    When done, the caller reads ``self.respawn_text`` and appends it.
    """

    def __init__(self, width, height, respawn_text):
        self.width  = width
        self.height = height
        self.respawn_text = respawn_text
        self.done   = False

        self._timer     = 0.0
        self._remaining = 5

        # Pre-render fonts
        self._font_skull = pygame.font.SysFont("Courier New", 13)
        self._font_title = pygame.font.SysFont("Courier New", 28, bold=True)
        self._font_sub   = pygame.font.SysFont("Courier New", 13, italic=True)
        self._font_cd    = pygame.font.SysFont("Courier New", 11)

    def update(self, dt):
        if self.done:
            return
        self._timer += dt
        self._remaining = max(0, 5 - int(self._timer))
        if self._timer >= 5.0:
            self.done = True

    def render(self, surface):
        if self.done:
            return

        # Full-screen dark overlay
        ov = pygame.Surface((self.width, self.height))
        ov.fill(BG)
        ov.set_alpha(230)
        surface.blit(ov, (0, 0))

        cx = self.width // 2
        cy = self.height // 2

        # Skull ASCII rows
        total_h = len(SKULL) * 18
        start_y = cy - total_h // 2 - 60
        for i, line in enumerate(SKULL):
            r = self._font_skull.render(line, True, RED)
            surface.blit(r, r.get_rect(center=(cx, start_y + i * 18)))

        # Title
        t = self._font_title.render("YOU HAVE FALLEN", True, RED)
        surface.blit(t, t.get_rect(center=(cx, cy + 30)))

        # Subtitle
        s = self._font_sub.render("Your journey continues...", True, GREY)
        surface.blit(s, s.get_rect(center=(cx, cy + 70)))

        # Countdown
        cd = self._font_cd.render(
            f"Respawning in {self._remaining}...", True, DIM)
        surface.blit(cd, cd.get_rect(center=(cx, cy + 100)))
