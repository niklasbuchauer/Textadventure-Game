# dungeon_entrance_overlay.py  –  Dramatic dungeon entrance animation
#
# Full-screen double-door opening animation followed by camera movement into darkness.
# Professional visual effect for dungeon entry sequences.
#
# Public interface:
#   handle_event(event) -> bool
#   update(dt)
#   draw(surface)
#   is_open() -> bool
#   close()

import pygame
import math


class DungeonEntranceOverlay:
    """
    Dramatic dungeon entrance animation:
    1. Double doors (wooden with metal bands) swing open from center
    2. Camera moves forward into darkness with perspective and vignette
    3. Animation duration: 5 seconds total
    """

    TOTAL_DURATION = 3.5
    DOOR_OPEN_DURATION = 2.0  # Time for doors to fully open
    CAMERA_MOVE_DURATION = 3.0  # Time for camera to move into darkness

    # Color palette
    C_DOOR_WOOD = (101, 67, 33)      # Dark wood brown
    C_DOOR_EDGE = (70, 45, 20)       # Darker wood
    C_METAL = (180, 180, 190)        # Metal bands
    C_METAL_DARK = (90, 90, 100)     # Metal shadow
    C_METAL_LIGHT = (220, 220, 230)  # Metal highlight
    C_STONE = (120, 120, 120)        # Stone frame
    C_LOCK_GOLD = (200, 160, 50)     # Lock color
    C_SHADOW = (20, 20, 20)          # Deep shadow
    C_DARK = (5, 5, 10)              # Near-black

    def __init__(self, screen_w=1920, screen_h=1440):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self._alive = True
        self._elapsed = 0.0
        self._progress = 0.0  # 0..1 overall animation progress

    def handle_event(self, event):
        """Handle input events (can skip animation with spacebar/click)."""
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_ESCAPE):
                self.close()
                return True
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.close()
            return True
        return False

    def update(self, dt):
        """Update animation state."""
        if self._alive:
            self._elapsed += dt
            self._progress = min(1.0, self._elapsed / self.TOTAL_DURATION)
            if self._progress >= 1.0:
                self.close()

    def is_open(self):
        """Return True if overlay is still visible."""
        return self._alive

    def is_done(self):
        """Return True if animation is complete (for GUI integration)."""
        return not self._alive

    def close(self):
        """Close the overlay."""
        self._alive = False

    def draw(self, surface):
        """Render the full animation."""
        if not self._alive:
            return

        # Clear with black background
        surface.fill((0, 0, 0))

        # Phase 1: Door opening (0 to 2 seconds)
        door_phase = min(1.0, self._elapsed / self.DOOR_OPEN_DURATION)
        self._draw_doors(surface, door_phase)

        # Phase 2: Camera movement into darkness (overlays on door animation)
        if self._elapsed > 0.5:  # Start fade-in after doors begin opening
            camera_phase = max(0.0, (self._elapsed - 0.5) / self.CAMERA_MOVE_DURATION)
            self._draw_camera_movement(surface, camera_phase)

    # ── Door Drawing ──────────────────────────────────────────────────────────

    def _draw_doors(self, surface, phase):
        """
        Draw two wooden doors swinging open from center (hinged, not spinning).
        phase: 0.0 (closed) to 1.0 (fully open)
        """
        sw, sh = self.screen_w, self.screen_h
        cx, cy = sw // 2, sh // 2

        # Door dimensions
        door_w = int(sw // 2.5)   # Each door width
        door_h = int(sh * 0.95)   # Door height (95% of screen)

        # Easing: quadratic ease-out for dramatic motion
        eased_phase = 1.0 - (1.0 - phase) ** 2

        # Left door moves left, right door moves right (simple X translation)
        max_offset = int(door_w * 1.05)  # Move doors fully off-screen
        left_offset = int(eased_phase * max_offset)
        right_offset = int(eased_phase * max_offset)

        # Draw left door (moves left)
        left_x = cx - door_w - left_offset
        self._draw_single_door(surface, left_x, cy - door_h // 2, door_w, door_h, is_left=True)

        # Draw right door (moves right)
        right_x = cx + right_offset
        self._draw_single_door(surface, right_x, cy - door_h // 2, door_w, door_h, is_left=False)

    def _draw_single_door(self, surface, x, y, w, h, is_left):
        """
        Draw one ornate dungeon door (solid rectangle with details, no rotation).
        """
        x, y, w, h = int(x), int(y), int(w), int(h)

        # Door frame
        pygame.draw.rect(surface, self.C_DOOR_EDGE, (x, y, w, h), 8)

        # Fill door with wood color
        pygame.draw.rect(surface, self.C_DOOR_WOOD, (x + 8, y + 8, w - 16, h - 16))

        # Vertical wood plank divisions
        plank_width = w // 4
        for i in range(1, 4):
            px = x + i * plank_width
            pygame.draw.line(surface, self.C_DOOR_EDGE, (px, y + 8), (px, y + h - 8), 3)

        # Metal reinforcement bands (horizontal)
        band_height = 24
        band_positions = [y + h // 4, y + h // 2, y + 3 * h // 4]
        for by in band_positions:
            # Band base
            pygame.draw.rect(surface, self.C_METAL, (x + 20, by - band_height // 2, w - 40, band_height))
            # Band highlights for 3D effect
            pygame.draw.line(surface, self.C_METAL_LIGHT, (x + 20, by - band_height // 2),
                           (x + w - 20, by - band_height // 2), 3)
            # Band shadows
            pygame.draw.line(surface, self.C_METAL_DARK, (x + 20, by + band_height // 2),
                           (x + w - 20, by + band_height // 2), 3)

        # Ornate lock/handle in center
        lock_y = y + h // 2
        # Lock circle
        pygame.draw.circle(surface, self.C_LOCK_GOLD, (x + w // 2, lock_y), 16)
        pygame.draw.circle(surface, self.C_METAL_DARK, (x + w // 2, lock_y), 16, 3)
        # Lock keyhole
        pygame.draw.circle(surface, (20, 20, 20), (x + w // 2, lock_y), 6)

    # ── Camera Movement into Darkness ─────────────────────────────────────────

    def _draw_camera_movement(self, surface, phase):
        """
        Draw camera moving forward into darkness with elegant fade.
        phase: 0.0 (at door) to 1.0 (deep in dungeon)
        """
        sw, sh = self.screen_w, self.screen_h

        # Smooth easing for the fade
        eased = min(1.0, phase ** 0.8)

        # Progressive fade to black using alpha blending
        fade_alpha = max(0, min(255, int(200 * eased)))
        fade_overlay = pygame.Surface((sw, sh))
        fade_overlay.set_alpha(fade_alpha)
        fade_overlay.fill((0, 0, 0))
        surface.blit(fade_overlay, (0, 0))

        # Subtle vignette effect (darkening at edges)
        if eased < 1.3:
            vignette = pygame.Surface((sw, sh))
            vignette_strength = max(0, min(255, int(150 * eased)))
            vignette.set_alpha(vignette_strength)
            # Draw darkening circle at edges
            pygame.draw.circle(vignette, (0, 0, 0), (sw // 2, sh // 2), max(sw, sh) // 3)
            surface.blit(vignette, (0, 0))
            fade_amount = (phase - 0.7) / 0.3
            fade_surf = pygame.Surface((sw, sh))
            fade_surf.fill(self.C_DARK)
            fade_surf.set_alpha(int(255 * fade_amount * 0.9))
            surface.blit(fade_surf, (0, 0))


# ══════════════════════════════════════════════════════════════════════════════
#  USAGE EXAMPLE
# ══════════════════════════════════════════════════════════════════════════════
#
# In your engine or game state manager:
#
#   from dungeon_entrance_overlay import DungeonEntranceOverlay
#
#   # When dungeon is entered:
#   self.dungeon_entrance = DungeonEntranceOverlay(screen_w, screen_h)
#
#   # In your game loop update:
#   if self.dungeon_entrance and self.dungeon_entrance.is_open():
#       self.dungeon_entrance.update(dt)
#
#   # In your game loop event handling:
#   if self.dungeon_entrance and self.dungeon_entrance.is_open():
#       if self.dungeon_entrance.handle_event(event):
#           # Animation closed (either finished or skipped)
#           self.dungeon_entrance = None
#
#   # In your render/draw code:
#   if self.dungeon_entrance and self.dungeon_entrance.is_open():
#       self.dungeon_entrance.draw(surface)  # Draw last (on top)
