"""
Live Map Window — Pygame graphical map with drawn shapes.

Automatically switches between overworld and dungeon floor maps based on
the player's current room.  Renders circles/squares/diamonds on a Surface
displayed inside a pygame_gui UIWindow via UIImage.
"""

import re
import math
import random
import pygame
import pygame_gui
from pygame_gui.elements import (
    UIButton, UILabel, UIWindow, UIImage,
)
from font_support import load_font, wrap_font_with_symbol_fallback

from ui_animation import UI_OPEN_DUR, ease_out_cubic

try:
    from home_system import is_home_room, get_unlocked_tiles
    from home_items import get_home_item
    from home_assets import blit_home_item_sprite
    HOME_MAP_AVAILABLE = True
except Exception:
    HOME_MAP_AVAILABLE = False


class LiveMapWindow:
    """Graphical map window using pygame drawing + UIWindow overlay."""

    # ── colour palette ──────────────────────────────────────────────
    # ── medieval parchment colour palette ───────────────────────────
    COLORS = {
        # backgrounds
        "bg":                 "#2e2618",   # dungeon: dark stone
        "ocean":              "#b8cfd8",   # aged sea — pale blue-grey
        "ocean_deep":         "#8aaebb",   # deeper ocean
        "ocean_lines":        "#9bbac6",   # cartouche grid lines on sea
        "land":               "#e2c988",   # warm aged parchment cream
        "land_inner":         "#ead8a0",   # inner land lighter
        "land_shadow":        "#c4aa6c",   # land edge vignette
        "grid":               "#c8b480",
        # roads / connections
        "connection":         "#c8b490",   # unvisited trail — faint dust
        "connection_border":  "#6e4820",   # road border ink
        "connection_visited": "#7a4e1c",   # worn dirt road
        "connection_vis_hi":  "#a87030",   # road highlight
        # text
        "text":               "#2c1804",   # iron-gall ink
        "text_dim":           "#9a8060",   # fog label
        "text_label_bg":      "#ecddb0",   # label parchment backing
        # player marker
        "current_fill":       "#be1818",   # heraldic red
        "current_outline":    "#7a0c0c",   # dark red outline
        "current_glow":       "#e06028",   # warm pulse
        # visited
        "visited_fill":       "#d8c48c",
        "visited_outline":    "#7a5828",
        # fog of war
        "unexplored_fill":    "#ccb87c",
        "unexplored_dot":     "#b8a46a",
        # special tags
        "entrance_fill":      "#cad8b8",
        "entrance_outline":   "#4e7830",
        "stairs_fill":        "#d4cce0",
        "stairs_outline":     "#6850a0",
        "treasure_fill":      "#f0e090",
        "treasure_outline":   "#a07818",
        "dungeon_entrance_fill":    "#c0a888",
        "dungeon_entrance_outline": "#6e2010",
        # UI
        "header_fg":          "#5a2e08",
        "stats_bg":           "#f0e4c0",
        "boat_line":          "#3a6888",
        "boat_line_hi":       "#7aaac8",
        # decoration
        "ink":                "#2c1804",
        "ink_mid":            "#7a5028",
        "border_outer":       "#7a5028",
        "border_inner":       "#a87838",
        "compass_fg":         "#5c2e08",
        "compass_bg":         "#ecddb0",
        "dungeon_wall":       "#3a3028",
        "dungeon_stone":      "#484038",
    }

    # ── region colour themes (fill, ink-outline) — parchment naturalistic ──
    REGION_COLORS = {
        "forest":     ("#a0bf7c", "#3c6018"),
        "swamp":      ("#90a882", "#305038"),
        "mountain":   ("#c0b4a0", "#706050"),
        "village":    ("#d8c484", "#886018"),
        "river":      ("#98c0d0", "#2e6888"),
        "graveyard":  ("#b0a8a0", "#505050"),
        "ruins":      ("#c8b888", "#786028"),
        "building":   ("#c0c0cc", "#486080"),
        "desert":     ("#e0c87c", "#987020"),
        "tundra":     ("#c8d8e4", "#5888a4"),
        "coast":      ("#90bcd0", "#286882"),
        "castle":     ("#c0b0c8", "#604890"),
        "dock":       ("#98b8cc", "#2c5878"),
        "sunstone":   ("#e4d07c", "#a07818"),
        "emerald":    ("#84c898", "#186838"),
        "stormbreak": ("#98a8c4", "#284890"),
        "cinderforge":("#d09078", "#882810"),
        "dreadmist":  ("#a898b8", "#503870"),
        "wyrmscale":  ("#c8b084", "#806018"),
        "abyssal":    ("#8888b0", "#282870"),
        "default":    ("#c8b888", "#786038"),
    }

    ROOM_RADIUS = 14
    MIN_SPACING = 80
    ZOOM_MIN = 0.05
    ZOOM_MAX = 0.69
    ZOOM_STEP = 0.15
    OPEN_DUR = UI_OPEN_DUR

    # ── construction ────────────────────────────────────────────────
    def __init__(self, app, rooms_data, game_engine=None):
        """
        Args:
            app:         GameApp instance (has .manager, .width, .height, .screen)
            rooms_data:  dict  room_id -> Room object  (engine.rooms)
            game_engine: GameEngine instance (for dungeon data access)
        """
        self.app = app
        self.manager = app.manager
        self._font_profile = getattr(app, "font_profile", {}) or {}
        self.rooms_data = rooms_data
        self.game_engine = game_engine

        self.window = None
        self._map_image = None          # UIImage element for map surface
        self._map_surface = None        # pygame.Surface we draw on
        self._header_label = None
        self._stats_label = None
        self._zoom_label = None
        self._region_label = None

        self.current_location = None
        self.visited_rooms: set = set()
        self.reveal_all = False

        self._zoom = self.ZOOM_MAX
        self._pan_x = 0.0
        self._pan_y = 0.0
        self._drag_start = None
        self._resize_drag = None   # {'edges':(l,r,b), 'sm':(x,y), 'sr': Rect}
        self._last_map_size = (0, 0)

        # caches
        self._cached_overworld_rooms = None
        self._cached_room_count = 0
        self._region_cache: dict = {}
        self._needs_redraw = True
        self._font_cache: dict = {}         # keyed by int size
        self._text_surf_cache: dict = {}    # keyed by (text, color_tuple, size)
        self._hex_pts_cache: dict = {}      # radius -> list of (dx,dy) offsets for dungeon hexagon

        # Clickable room hit map + selection
        self._hit_positions: dict = {}
        self._hit_rooms: dict = {}
        self._hit_visible: set = set()
        self._hit_radius: float = self.ROOM_RADIUS
        self._selected_room_id: str | None = None

        # Island-cluster cache: avoids O(n^2) proximity recomputation each frame.
        # Keyed on (spacing, frozenset(room_ids)); invalidated when zoom or rooms change.
        self._island_cache_kv = None        # ((spacing, frozenset), [frozenset, ...])
        # Actual screen-px spacing from last _compute_layout — used for cluster threshold
        self._last_layout_spacing = 0.0
        # Pre-computed wave jitter offsets — built once, reused every frame (~27x speedup)
        self._wave_jitter_table = None      # list of (gx_idx, gy_idx, jx_off, jy_off)
        # Map centre cache for routing curves
        self._layout_cx = 0.0
        self._layout_cy = 0.0
        self._layout_mid_x = 0.0
        self._layout_mid_y = 0.0
        self._layout_spacing = 0.0
        self._main_island_obstacle = None

        self._home_ids: set[str] = set()
        self._cached_unlocked_islands: set[str] = set()

        # Pre-compute RGB colour tuples once so _c() / _hex_to_rgb() are O(1)
        self._rgb_colors = {k: self._hex_to_rgb(v) for k, v in self.COLORS.items()}
        self._rgb_region = {k: (self._hex_to_rgb(v[0]), self._hex_to_rgb(v[1]))
                            for k, v in self.REGION_COLORS.items()}

        # fonts (initialised lazily)
        self._font_label = None
        self._font_icon = None
        self._font_legend = None
        self._font_header = None
        self._open_started_ms = 0
        self._open_t = 1.0

    def _init_fonts(self):
        if self._font_label is not None:
            return
        def _best(size):
            return wrap_font_with_symbol_fallback(
                load_font(self._font_profile, size)
            )
        self._font_label  = _best(9)
        self._font_icon   = _best(14)
        self._font_legend = _best(8)
        self._font_header = _best(13)

    # ── window lifecycle ────────────────────────────────────────────
    def create_window(self, x_offset=200, y_offset=100):
        """Create / raise the map UIWindow."""
        if self.window and self.window.alive():
            return

        self._init_fonts()

        W, H = self.app.width, self.app.height
        ww, wh = 900, 700
        self.window = UIWindow(
            rect=pygame.Rect((W - ww) // 2, (H - wh) // 2, ww, wh),
            manager=self.manager,
            window_display_title="Live Map",
            resizable=True,
        )
        iw = ww - 60

        # Header label
        self._header_label = UILabel(
            relative_rect=pygame.Rect(10, 4, iw - 20, 22),
            text="MAP", manager=self.manager, container=self.window,
        )

        # Toolbar row
        btn_w = 30
        y_tb = 28
        self._btn_zoom_out = UIButton(
            relative_rect=pygame.Rect(10, y_tb, btn_w, 24),
            text="\u2212", manager=self.manager, container=self.window,
        )
        self._zoom_label = UILabel(
            relative_rect=pygame.Rect(42, y_tb, 50, 24),
            text="100%", manager=self.manager, container=self.window,
        )
        self._btn_zoom_in = UIButton(
            relative_rect=pygame.Rect(94, y_tb, btn_w, 24),
            text="+", manager=self.manager, container=self.window,
        )
        self._btn_reset = UIButton(
            relative_rect=pygame.Rect(130, y_tb, btn_w, 24),
            text="\u2302", manager=self.manager, container=self.window,
        )
        self._region_label = UILabel(
            relative_rect=pygame.Rect(iw - 200, y_tb, 200, 24),
            text="", manager=self.manager, container=self.window,
        )

        # Map image area — UIImage is hidden; we blit _map_surface directly
        # each frame via render_direct() to avoid the costly pygame_gui composite.
        map_y = 56
        map_h = wh - 130 - map_y
        map_w = iw
        self._map_rect_local = pygame.Rect(10, map_y, map_w, map_h)
        self._map_surface = pygame.Surface((map_w, map_h))
        _placeholder = pygame.Surface((1, 1), pygame.SRCALPHA)
        self._map_image = UIImage(
            relative_rect=self._map_rect_local,
            image_surface=_placeholder,
            manager=self.manager, container=self.window,
        )
        self._map_image.hide()  # pygame_gui skips it during draw_ui → zero composite cost

        # Stats bar
        self._stats_label = UILabel(
            relative_rect=pygame.Rect(10, wh - 130 + 4, iw, 22),
            text="", manager=self.manager, container=self.window,
        )

        self._open_started_ms = pygame.time.get_ticks()
        self._open_t = 0.0

        self._needs_redraw = True
        self.redraw_map()

    def close_window(self):
        if self.window and self.window.alive():
            self.window.kill()
        self.window = None
        self._map_image = None
        self._map_surface = None

    def is_open(self):
        return self.window is not None and self.window.alive()

    def render_direct(self, screen: pygame.Surface):
        """Blit the map surface directly to the game screen (called from render_overlay).
        This bypasses pygame_gui's compositing pipeline for the large map texture."""
        if not self.is_open() or not self._map_surface:
            return
        if not self._map_image or not self._map_image.alive():
            return
        rect = self._map_image.get_abs_rect()
        if self._open_t >= 0.999:
            screen.blit(self._map_surface, rect.topleft)
            return

        eased = ease_out_cubic(self._open_t)
        scale = 0.90 + (0.10 * eased)
        tw = max(2, int(rect.width * scale))
        th = max(2, int(rect.height * scale))
        tx = rect.x + (rect.width - tw) // 2
        ty = rect.y + (rect.height - th) // 2

        scaled = pygame.transform.smoothscale(self._map_surface, (tw, th))
        if eased < 0.999:
            scaled = scaled.copy()
            scaled.set_alpha(int(255 * eased))
        screen.blit(scaled, (tx, ty))

    def _tick_open_animation(self):
        if not self.is_open() or self._open_t >= 1.0:
            return
        elapsed = (pygame.time.get_ticks() - self._open_started_ms) / 1000.0
        self._open_t = min(1.0, elapsed / self.OPEN_DUR)

    def tick(self):
        """Called once per game-frame to perform any deferred redraw."""
        self._tick_open_animation()
        if self.is_open() and self._needs_redraw:
            self.redraw_map()

    # ── public API ──────────────────────────────────────────────────
    def update_location(self, current_room_id, visited_rooms):
        self.current_location = current_room_id
        self.visited_rooms = set(visited_rooms)
        if self.is_open():
            self._needs_redraw = True
            self.redraw_map()

    def toggle_reveal(self):
        self.reveal_all = not self.reveal_all
        if self.is_open():
            self._needs_redraw = True
            self.redraw_map()
        return self.reveal_all

    # ── event handling ──────────────────────────────────────────────
    def handle_event(self, event):
        if not self.is_open():
            return

        # ── Window-edge resize (left / right / bottom, 14 px hit zone) ──────
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            edges = self._check_resize_edges(pygame.mouse.get_pos())
            if edges:
                self._resize_drag = {
                    'edges': edges,
                    'sm': pygame.mouse.get_pos(),
                    'sr': pygame.Rect(self.window.get_abs_rect()),
                }
                return

        if event.type == pygame.MOUSEMOTION and self._resize_drag:
            self._apply_resize_drag(pygame.mouse.get_pos())
            return

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self._resize_drag:
            self._resize_drag = None
            self._needs_redraw = True
            self.redraw_map()
            return

        # Zoom buttons
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self._btn_zoom_in:
                self._zoom_in()
            elif event.ui_element == self._btn_zoom_out:
                self._zoom_out()
            elif event.ui_element == self._btn_reset:
                self._reset_view()
            return

        # Mouse wheel zoom over map area — zooms toward cursor position
        if event.type == pygame.MOUSEWHEEL:
            if self._is_mouse_over_map():
                if event.y > 0:
                    self._apply_zoom_at(1.20, pygame.mouse.get_pos())
                elif event.y < 0:
                    self._apply_zoom_at(1.0 / 1.20, pygame.mouse.get_pos())
            return

        # Click-drag pan
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._is_mouse_over_map():
                self._drag_start = pygame.mouse.get_pos()
            return

        if event.type == pygame.MOUSEMOTION:
            if self._drag_start:
                mx, my = pygame.mouse.get_pos()
                dx = mx - self._drag_start[0]
                dy = my - self._drag_start[1]
                self._pan_x += dx
                self._pan_y += dy
                self._drag_start = (mx, my)
                self._needs_redraw = True
                # redraw is deferred to tick() — do NOT call redraw_map() here
                # as MOUSEMOTION fires hundreds of times per second during drag
            return

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self._drag_start:
                start = self._drag_start
                self._drag_start = None
                dist = math.hypot(pygame.mouse.get_pos()[0] - start[0],
                                  pygame.mouse.get_pos()[1] - start[1])
                if self._is_mouse_over_map() and dist <= 6:
                    self._handle_map_click(pygame.mouse.get_pos())
                else:
                    self._needs_redraw = True
                    self.redraw_map()
            return

    def _is_mouse_over_map(self):
        """Check if mouse is currently over the map image area."""
        if not self._map_image or not self._map_image.alive():
            return False
        mx, my = pygame.mouse.get_pos()
        return self._map_image.get_abs_rect().collidepoint(mx, my)

    _RESIZE_HIT = 14  # pixels from window edge that count as resize zone

    def _check_resize_edges(self, pos):
        """Return (left, right, bottom) booleans if pos hits a resize edge, else None.
        The title-bar top is intentionally excluded to avoid conflicting with
        pygame_gui's built-in window drag."""
        mx, my = pos
        wr = self.window.get_abs_rect()
        h = self._RESIZE_HIT
        near_left   = wr.left   <= mx <= wr.left   + h
        near_right  = wr.right  - h <= mx <= wr.right
        near_bottom = wr.bottom - h <= my <= wr.bottom
        if near_left or near_right or near_bottom:
            return (near_left, near_right, near_bottom)
        return None

    def _apply_resize_drag(self, pos):
        """Resize the window based on accumulated drag delta from the start pos."""
        mx, my = pos
        smx, smy = self._resize_drag['sm']
        sr = self._resize_drag['sr']
        l, r, b = self._resize_drag['edges']
        dx = mx - smx
        dy = my - smy
        new_w = sr.width
        new_h = sr.height
        new_x = sr.x
        if l:
            new_w = max(400, sr.width - dx)
            new_x = sr.right - new_w   # anchor right edge
        if r:
            new_w = max(400, sr.width + dx)
        if b:
            new_h = max(300, sr.height + dy)
        self.window.set_dimensions((new_w, new_h))
        if l:
            self.window.set_relative_position((new_x, sr.y))
        self._needs_redraw = True

    def _handle_map_click(self, abs_pos):
        """Select the nearest visible room under the cursor and toggle its label."""
        if not self._map_image or not self._map_image.alive():
            return
        if not self._hit_positions:
            return

        rect = self._map_image.get_abs_rect()
        lx = abs_pos[0] - rect.x
        ly = abs_pos[1] - rect.y

        hit_radius = max(10, self._hit_radius + 6)
        best = None  # (rid, dist)
        for rid, (px, py) in self._hit_positions.items():
            if rid not in self._hit_rooms:
                continue
            is_visible = self.reveal_all or rid in self._hit_visible or rid == self.current_location
            if not is_visible:
                continue
            dist = math.hypot(lx - px, ly - py)
            if dist <= hit_radius and (best is None or dist < best[1]):
                best = (rid, dist)

        new_sel = best[0] if best else None
        if new_sel == self._selected_room_id:
            self._selected_room_id = None
        else:
            self._selected_room_id = new_sel

        self._needs_redraw = True
        self.redraw_map()

    # ── zoom / pan controls ─────────────────────────────────────────
    def _zoom_in(self):
        old_z = self._zoom
        new_z = min(self.ZOOM_MAX, old_z + self.ZOOM_STEP)
        ratio = new_z / old_z if old_z else 1.0
        self._pan_x *= ratio
        self._pan_y *= ratio
        self._zoom = new_z
        self._update_zoom_label()
        self._needs_redraw = True
        self.redraw_map()

    def _zoom_out(self):
        old_z = self._zoom
        new_z = max(self.ZOOM_MIN, old_z - self.ZOOM_STEP)
        ratio = new_z / old_z if old_z else 1.0
        self._pan_x *= ratio
        self._pan_y *= ratio
        self._zoom = new_z
        self._update_zoom_label()
        self._needs_redraw = True
        self.redraw_map()

    def _apply_zoom_at(self, factor, cursor_abs_pos):
        """Zoom by factor, keeping the map point under cursor_abs_pos stationary."""
        if not self._map_image or not self._map_image.alive():
            return
        rect = self._map_image.get_abs_rect()
        mcx = cursor_abs_pos[0] - rect.x
        mcy = cursor_abs_pos[1] - rect.y
        sw, sh = rect.width, rect.height
        old_z = self._zoom
        new_z = max(self.ZOOM_MIN, min(self.ZOOM_MAX, old_z * factor))
        ratio = new_z / old_z
        # Offset of cursor from the layout centre (in screen pixels)
        ox = mcx - (sw / 2 + self._pan_x)
        oy = mcy - ((sh - 60) / 2 + self._pan_y)
        # Shift pan so the world point under the cursor stays fixed
        self._pan_x = mcx - sw / 2 - ox * ratio
        self._pan_y = mcy - (sh - 60) / 2 - oy * ratio
        self._zoom = new_z
        self._update_zoom_label()
        self._needs_redraw = True
        self.redraw_map()

    def _reset_view(self):
        self._zoom = self.ZOOM_MAX
        self._pan_x = 0.0
        self._pan_y = 0.0
        self._update_zoom_label()
        self._needs_redraw = True
        self.redraw_map()

    def _update_zoom_label(self):
        if self._zoom_label:
            self._zoom_label.set_text(f"{int(self._zoom * 100)}%")

    # ── hit map helpers for click-to-label ────────────────────────
    def _clear_hitmap(self):
        self._hit_positions = {}
        self._hit_rooms = {}
        self._hit_visible = set()
        self._hit_radius = self.ROOM_RADIUS

    def _remember_hitmap(self, positions, rooms, visible_set, radius):
        self._hit_positions = dict(positions) if positions else {}
        self._hit_rooms = rooms or {}
        vis = set(visible_set or [])
        if self.current_location:
            vis.add(self.current_location)
        self._hit_visible = vis
        self._hit_radius = radius

    # ── rendering entry-point ───────────────────────────────────────
    def redraw_map(self):
        if not self.is_open() or not self._map_surface:
            return

        # Check if UIWindow was resized — recreate map surface if needed
        container = self.window.get_container()
        cr = container.get_rect()
        iw = cr.width - 20
        map_h = cr.height - self._map_rect_local.y - 80
        map_w = iw
        if map_w < 20 or map_h < 20:
            return

        if (map_w, map_h) != self._last_map_size:
            self._last_map_size = (map_w, map_h)
            self._map_surface = pygame.Surface((map_w, map_h))
            self._map_rect_local.width = map_w
            self._map_rect_local.height = map_h
            self._map_image.set_dimensions((map_w, map_h))
            self._needs_redraw = True

        if not self._needs_redraw:
            return
        self._needs_redraw = False

        if self._player_in_dungeon():
            self._render_dungeon_map()
        elif self._player_in_home():
            self._render_home_map()
        else:
            self._render_overworld_map()
        # Surface is consumed by render_direct() each frame — no set_image() needed

    # ── coordinate layout ──────────────────────────────────────────
    def _compute_layout(self, coord_map, sw, sh, margin=70):
        if not coord_map:
            return {}, 0

        xs = [p[0] for p in coord_map]
        ys = [p[1] for p in coord_map]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        range_x = max_x - min_x
        range_y = max_y - min_y

        usable_w = sw - 2 * margin
        usable_h = sh - 2 * margin - 60

        spacing_x = (usable_w / range_x) if range_x > 0 else 200
        spacing_y = (usable_h / range_y) if range_y > 0 else 200

        base_spacing = max(self.MIN_SPACING, min(spacing_x, spacing_y, 200))
        spacing = base_spacing * self._zoom
        self._last_layout_spacing = spacing  # stored for island clustering threshold

        cx = sw / 2 + self._pan_x
        cy = (sh - 60) / 2 + self._pan_y
        mid_x = (min_x + max_x) / 2
        mid_y = (min_y + max_y) / 2

        # Store for world↔screen transforms used by island drawing
        self._layout_cx      = cx
        self._layout_cy      = cy
        self._layout_mid_x   = mid_x
        self._layout_mid_y   = mid_y
        self._layout_spacing = spacing

        positions = {}
        for (gx, gy), rid in coord_map.items():
            px = cx + (gx - mid_x) * spacing
            py = cy - (gy - mid_y) * spacing
            positions[rid] = (px, py)

        return positions, spacing

    def _boat_control_point(self, x1, y1, x2, y2):
        """Choose a control point that bends the sea route around the main landmass."""
        cx = getattr(self, "_layout_cx", 0.0)
        cy = getattr(self, "_layout_cy", 0.0)
        mx = (x1 + x2) / 2.0
        my = (y1 + y2) / 2.0

        dx = x2 - x1
        dy = y2 - y1
        dist = max(1.0, math.hypot(dx, dy))
        px = -dy / dist
        py = dx / dist

        # Push away from the land centroid (layout centre) so the curve skirts islands
        to_center = (cx - mx, cy - my)
        if px * to_center[0] + py * to_center[1] > 0:
            px, py = -px, -py

        offset = min(220.0, max(80.0, dist * 0.45))
        ctrl = [mx + px * offset, my + py * offset]

        # If a main-island obstacle exists, push the control point further outward to clear it
        obs = self._main_island_obstacle
        if obs:
            ocx, ocy, orad = obs
            vx = ctrl[0] - ocx
            vy = ctrl[1] - ocy
            d = math.hypot(vx, vy)
            min_clear = orad * 1.08
            if d < min_clear:
                scale = (min_clear + 40.0) / max(d, 1.0)
                ctrl[0] = ocx + vx * scale
                ctrl[1] = ocy + vy * scale

        return tuple(ctrl)

    def _pos_for_room(self, rid, positions, rooms):
        """Return screen position for rid, deriving from coordinates if missing."""
        if rid in positions:
            return positions[rid]
        rdata = rooms.get(rid) if isinstance(rooms, dict) else None
        if not rdata or "coordinates" not in rdata:
            return None
        if self._is_home_room_id(rid, rdata):
            return None
        cx, cy = rdata.get("coordinates", [0, 0])
        return self._world_to_screen(cx, cy)


    def _world_to_screen(self, wx, wy):
        """Convert a world-space (grid) coordinate to screen pixels."""
        s  = getattr(self, '_layout_spacing', self._last_layout_spacing)
        cx = getattr(self, '_layout_cx', 0)
        cy = getattr(self, '_layout_cy', 0)
        mx = getattr(self, '_layout_mid_x', 0)
        my = getattr(self, '_layout_mid_y', 0)
        return (cx + (wx - mx) * s,
                cy - (wy - my) * s)

    # ── drawing helpers ─────────────────────────────────────────────
    @staticmethod
    def _hex_to_rgb(hex_color):
        h = hex_color.lstrip("#")
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

    def _c(self, key):
        """Return cached RGB tuple for named colour."""
        return self._rgb_colors[key]

    @staticmethod
    def _safe_xy(value, default=(0.0, 0.0)):
        """Return a numeric (x, y) tuple from potentially malformed coordinate data."""
        if isinstance(value, (list, tuple)) and len(value) >= 2:
            try:
                return (float(value[0]), float(value[1]))
            except Exception:
                return default
        return default

    def _normalize_coordinates(self, value):
        x, y = self._safe_xy(value)
        return [x, y]

    def _get_font(self, size: int) -> pygame.font.Font:
        """Return a cached medieval-style font at *size*."""
        f = self._font_cache.get(size)
        if f is None:
            f = wrap_font_with_symbol_fallback(
                load_font(self._font_profile, size)
            )
            self._font_cache[size] = f
        return f

    def _render_text(self, text: str, color: tuple, size: int) -> pygame.Surface:
        """Return a cached text surface — avoids font.render() per room per frame."""
        key = (text, color, size)
        s = self._text_surf_cache.get(key)
        if s is None:
            s = self._get_font(size).render(text, True, color)
            self._text_surf_cache[key] = s
            # Bound cache size
            if len(self._text_surf_cache) > 2000:
                self._text_surf_cache.clear()
        return s

    def _is_home_room_id(self, rid, room_obj=None) -> bool:
        if not rid:
            return False
        if rid in self._home_ids:
            return True
        try:
            if HOME_MAP_AVAILABLE and is_home_room(rid):
                self._home_ids.add(rid)
                return True
        except Exception:
            pass
        if isinstance(room_obj, dict) and room_obj.get("location_type") == "home":
            self._home_ids.add(rid)
            return True
        if rid == "player_home":
            self._home_ids.add(rid)
            return True
        return False

    def _is_island_unlocked(self, island_id: str) -> bool:
        if not island_id:
            return False
        if island_id in self._cached_unlocked_islands:
            return True
        ge = self.game_engine
        try:
            player = getattr(ge, "player", None) if ge else None
            unlocked = getattr(player, "unlocked_islands", None)
            if unlocked and island_id in unlocked:
                self._cached_unlocked_islands.add(island_id)
                return True
        except Exception:
            pass
        return False

    def _find_island_components(self, positions, world_positions=None):
        """Split positions into island clusters by SPATIAL proximity.
        When world_positions is provided (grid-coordinate space), clustering is
        done in world-space with a fixed threshold so islands never merge or split
        as the player zooms.  The screen-space positions dict is still used for
        the returned position dicts (for drawing).
        Returns list of position-dicts, largest component first.
        The grouping is cached so repeated calls are O(n) on a cache hit."""
        rids = list(positions.keys())
        if not rids:
            return []
        if len(rids) == 1:
            return [{rids[0]: positions[rids[0]]}]

        # Use a zoom-independent cache key when world_positions are available
        if world_positions:
            cache_key = frozenset(rids)
        else:
            cache_key = (round(self._last_layout_spacing, 1), frozenset(rids))

        if self._island_cache_kv is not None and self._island_cache_kv[0] == cache_key:
            # Fast O(n) path: rebuild position dicts from the cached room-ID groups
            result = [
                {rid: positions[rid] for rid in g if rid in positions}
                for g in self._island_cache_kv[1]
            ]
            result = [c for c in result if c]
            result.sort(key=lambda c: -len(c))
            return result

        # O(n^2) Union-Find proximity clustering
        if world_positions:
            # Cluster in world-space (grid units) — zoom-independent.
            # Rooms within 2.5 grid steps merge into the same island.
            threshold = 2.5
            cluster_src = world_positions
        elif self._last_layout_spacing > 0:
            threshold = max(120, self._last_layout_spacing * 1.8)
            cluster_src = positions
        else:
            threshold = max(120, self.MIN_SPACING * self._zoom * 1.8)
            cluster_src = positions

        parent = {r: r for r in rids}

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a, b):
            parent[find(a)] = find(b)

        for i, rid_a in enumerate(rids):
            ax, ay = cluster_src[rid_a]
            for rid_b in rids[i + 1:]:
                bx, by = cluster_src[rid_b]
                if math.hypot(ax - bx, ay - by) < threshold:
                    union(rid_a, rid_b)

        clusters: dict = {}
        for r in rids:
            root = find(r)
            clusters.setdefault(root, {})[r] = positions[r]

        result = list(clusters.values())
        result.sort(key=lambda c: -len(c))
        # Cache the group structure (room IDs only, not positions)
        self._island_cache_kv = (cache_key, [frozenset(c.keys()) for c in result])
        return result

    def _draw_single_island(self, surf, screen_positions, world_positions=None, rng_seed=42, num_spots=60):
        """Paint one bumpy coastline island polygon.
        When world_positions are supplied the hull is built and expanded in
        world-space (grid units) then transformed to screen-space — so the
        island shape is completely stable across zoom levels."""
        if not screen_positions:
            return

        def _convex_hull(points):
            pts = sorted(set(points))
            if len(pts) <= 1:
                return pts
            def cross(o, a, b):
                return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
            lower, upper = [], []
            for p in pts:
                while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
                    lower.pop()
                lower.append(p)
            for p in reversed(pts):
                while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
                    upper.pop()
                upper.append(p)
            return lower[:-1] + upper[:-1]

        if world_positions and len(world_positions) >= 1:
            # ── World-space path (zoom-stable) ─────────────────────
            wpts = list(world_positions.values())
            wxs = [p[0] for p in wpts]
            wys = [p[1] for p in wpts]
            wcx = (min(wxs) + max(wxs)) / 2
            wcy = (min(wys) + max(wys)) / 2

            hull_w = _convex_hull([(x, y) for x, y in wpts])
            if len(hull_w) < 3:
                r = max(2.0, (max(wxs) - min(wxs) + max(wys) - min(wys)) / 2 + 2.0)
                hull_w = [(wcx + math.cos(2*math.pi*i/12)*r,
                           wcy + math.sin(2*math.pi*i/12)*r) for i in range(12)]

            # Expand each hull vertex outward from centroid by WORLD_PAD grid units
            WORLD_PAD = 2.5
            expanded_w = []
            for hx, hy in hull_w:
                dx, dy = hx - wcx, hy - wcy
                d = max(0.001, math.hypot(dx, dy))
                expanded_w.append((hx + dx/d * WORLD_PAD,
                                   hy + dy/d * WORLD_PAD))

            # Subdivide, transform to screen, add tiny outward jitter
            rng = random.Random(rng_seed)
            n = len(expanded_w)
            SUBDIV = max(3, 80 // max(1, n))
            pts_outer = []
            scx, scy = self._world_to_screen(wcx, wcy)
            for i, (ax, ay) in enumerate(expanded_w):
                bx, by = expanded_w[(i + 1) % n]
                for k in range(SUBDIV):
                    t = k / SUBDIV
                    wx_ = ax + (bx - ax) * t
                    wy_ = ay + (by - ay) * t
                    sx, sy = self._world_to_screen(wx_, wy_)
                    ddx, ddy = sx - scx, sy - scy
                    dd = max(1, math.hypot(ddx, ddy))
                    j = rng.uniform(0, 12)
                    pts_outer.append((int(sx + ddx/dd * j),
                                      int(sy + ddy/dd * j)))
            cx, cy = scx, scy

        else:
            # ── Screen-space fallback ───────────────────────────────
            spts = list(screen_positions.values())
            xs = [p[0] for p in spts]
            ys = [p[1] for p in spts]
            cx = (min(xs) + max(xs)) / 2
            cy = (min(ys) + max(ys)) / 2

            hull_s = _convex_hull([(int(x), int(y)) for x, y in spts])
            if len(hull_s) < 3:
                hull_s = [(int(cx + math.cos(2*math.pi*i/12)*80),
                           int(cy + math.sin(2*math.pi*i/12)*80)) for i in range(12)]

            PAD = max(80, self._last_layout_spacing * 1.2)
            expanded_s = []
            for hx, hy in hull_s:
                dx, dy = hx - cx, hy - cy
                d = max(0.001, math.hypot(dx, dy))
                expanded_s.append((hx + dx/d * PAD, hy + dy/d * PAD))

            rng = random.Random(rng_seed)
            n = len(expanded_s)
            SUBDIV = max(3, 80 // max(1, n))
            pts_outer = []
            for i, (ax, ay) in enumerate(expanded_s):
                bx, by = expanded_s[(i + 1) % n]
                for k in range(SUBDIV):
                    t = k / SUBDIV
                    mx_ = ax + (bx - ax) * t
                    my_ = ay + (by - ay) * t
                    ddx, ddy = mx_ - cx, my_ - cy
                    dd = max(1, math.hypot(ddx, ddy))
                    j = rng.uniform(0, 12)
                    pts_outer.append((int(mx_ + ddx/dd * j),
                                      int(my_ + ddy/dd * j)))

        if len(pts_outer) < 3:
            return

        shadow_col = self._rgb_colors["land_shadow"]
        for shrink in (18, 10, 4):
            pts_s = []
            for px, py in pts_outer:
                dx, dy = px - cx, py - cy
                dist = max(1, math.hypot(dx, dy))
                pts_s.append((int(cx + dx * (1 - shrink / dist)),
                               int(cy + dy * (1 - shrink / dist))))
            pygame.draw.polygon(surf, shadow_col, pts_s)

        land_outer = self._rgb_colors["land"]
        land_inner = self._rgb_colors["land_inner"]
        pygame.draw.polygon(surf, land_outer, pts_outer)

        pts_inner = []
        for px, py in pts_outer:
            dx, dy = px - cx, py - cy
            dist = max(1, math.hypot(dx, dy))
            pts_inner.append((int(cx + dx * (1 - 20 / dist)),
                               int(cy + dy * (1 - 20 / dist))))
        pygame.draw.polygon(surf, land_inner, pts_inner)

        contour_col = self._rgb_colors["land_shadow"]
        for shrink_f in (0.72, 0.52, 0.34):
            pts_c = [(int(cx + (px - cx) * shrink_f), int(cy + (py - cy) * shrink_f))
                     for px, py in pts_outer]
            if len(pts_c) >= 3:
                pygame.draw.lines(surf, contour_col, True, pts_c, 1)

        bx_all = [p[0] for p in pts_outer]
        by_all = [p[1] for p in pts_outer]
        rw = (max(bx_all) - min(bx_all)) / 2
        rh = (max(by_all) - min(by_all)) / 2
        rng2 = random.Random(rng_seed + 57)
        land_inner_rgb = self._rgb_colors["land_inner"]
        for _ in range(num_spots):
            angle = rng2.uniform(0, 2 * math.pi)
            dist_f = rng2.uniform(0.0, 0.80)
            sx2 = int(cx + math.cos(angle) * rw * dist_f)
            sy2 = int(cy + math.sin(angle) * rh * dist_f)
            r2 = rng2.randint(1, 3)
            alpha = rng2.randint(4, 16)
            spot_col = tuple(max(0, c - alpha) for c in land_inner_rgb)
            pygame.draw.circle(surf, spot_col, (sx2, sy2), r2)

    def _draw_land_mass(self, surf, positions, rooms=None):
        """Draw one bumpy island per spatial cluster of rooms."""
        if not positions:
            return
        # Build world-space positions for zoom-independent clustering + hull
        world_pos = {}
        if rooms:
            for rid in positions:
                if rid in rooms:
                    c = rooms[rid].get("coordinates", [0, 0])
                    world_pos[rid] = self._safe_xy(c)
        world_pos = world_pos if len(world_pos) == len(positions) else None
        components = self._find_island_components(positions, world_pos)
        if not components:
            self._main_island_obstacle = None
            return
        # Cache main island obstacle for boat routing (largest component extent)
        main = components[0]
        xs_m = [p[0] for p in main.values()]
        ys_m = [p[1] for p in main.values()]
        if xs_m and ys_m:
            cx_m = (min(xs_m) + max(xs_m)) / 2.0
            cy_m = (min(ys_m) + max(ys_m)) / 2.0
            rx_m = (max(xs_m) - min(xs_m)) / 2.0
            ry_m = (max(ys_m) - min(ys_m)) / 2.0
            rad_m = max(rx_m, ry_m) * 1.15 + 40.0
            self._main_island_obstacle = (cx_m, cy_m, rad_m)
        else:
            self._main_island_obstacle = None
        total = sum(len(c) for c in components)
        largest = len(components[0])
        min_size = max(5, int(largest * 0.06))
        for i, comp_pos in enumerate(components):
            if len(comp_pos) < min_size:
                continue
            comp_world = ({rid: world_pos[rid] for rid in comp_pos if rid in world_pos}
                          if world_pos else None)
            spots = max(20, int(60 * len(comp_pos) // max(1, total)))
            self._draw_single_island(surf, comp_pos, comp_world,
                                     rng_seed=42 + i * 17, num_spots=spots)

    def _draw_grid(self, surf, positions, spacing):
        pass  # Removed: dashed-grid drawing iterated O(rooms²) tiny segments — major perf cost

    @staticmethod
    def _draw_dashed_line(surf, color, start, end, dash=4, gap=4, width=1):
        """Draw a dashed line on a surface."""
        x1, y1 = start
        x2, y2 = end
        dx = x2 - x1
        dy = y2 - y1
        dist = max(1, int((dx*dx + dy*dy) ** 0.5))
        step = dash + gap
        for i in range(0, dist, step):
            t0 = i / dist
            t1 = min((i + dash) / dist, 1.0)
            sx = int(x1 + dx * t0)
            sy = int(y1 + dy * t0)
            ex = int(x1 + dx * t1)
            ey = int(y1 + dy * t1)
            pygame.draw.line(surf, color, (sx, sy), (ex, ey), width)

    @staticmethod
    def _draw_dashed_curve(surf, color, p0, p1, p2, dash=4, gap=4, width=1, samples=28):
        """Draw a dashed quadratic Bezier curve p0->p2 with control p1."""

        def bez(t):
            u = 1 - t
            x = u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0]
            y = u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1]
            return x, y

        pts = [bez(i / samples) for i in range(samples + 1)]
        drawing = True
        remaining = dash
        for i in range(len(pts) - 1):
            ax, ay = pts[i]
            bx, by = pts[i + 1]
            dx = bx - ax
            dy = by - ay
            seg_len = math.hypot(dx, dy)
            if seg_len == 0:
                continue
            seg_pos = 0.0
            while seg_pos < seg_len:
                step = min(remaining, seg_len - seg_pos)
                t0 = seg_pos / seg_len
                t1 = (seg_pos + step) / seg_len
                sx = ax + dx * t0
                sy = ay + dy * t0
                ex = ax + dx * t1
                ey = ay + dy * t1
                if drawing:
                    pygame.draw.line(surf, color,
                                     (int(sx), int(sy)), (int(ex), int(ey)), width)
                seg_pos += step
                remaining -= step
                if remaining <= 0:
                    drawing = not drawing
                    remaining = dash if drawing else gap

    @staticmethod
    def _quad_point(p0, p1, p2, t: float):
        """Return a point on a quadratic Bezier at param t."""
        u = 1 - t
        x = u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0]
        y = u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1]
        return x, y

    def _draw_connections(self, surf, positions, rooms, visited, sw, sh):
        drawn = set()
        boat_routes = []
        unvisited_routes = []
        visited_routes = []
        margin = 60

        for rid, rdata in rooms.items():
            if rid not in positions:
                pos1 = self._pos_for_room(rid, positions, rooms)
                if not pos1:
                    continue
            else:
                pos1 = positions[rid]
            x1, y1 = pos1
            exits = rdata.get("exits", {})
            if not hasattr(exits, 'items'):
                continue

            for _dir, target in exits.items():
                target_id = target.get("target", "") if isinstance(target, dict) else target
                if target_id not in positions:
                    pos2 = self._pos_for_room(target_id, positions, rooms)
                    if not pos2:
                        continue
                else:
                    pos2 = positions[target_id]
                pair = tuple(sorted([rid, target_id]))
                if pair in drawn:
                    continue
                drawn.add(pair)

                x2, y2 = pos2
                # Viewport culling
                if (max(x1, x2) < -margin or min(x1, x2) > sw + margin or
                        max(y1, y2) < -margin or min(y1, y2) > sh + margin):
                    continue

                if isinstance(target, dict) and target.get("type") == "boat_travel":
                    island_id = target.get("island_id") or ""
                    if island_id and not self.reveal_all and not self._is_island_unlocked(island_id):
                        continue
                    boat_routes.append((x1, y1, x2, y2))
                    continue

                both = rid in visited and target_id in visited
                if both:
                    visited_routes.append((x1, y1, x2, y2))
                else:
                    unvisited_routes.append((x1, y1, x2, y2))

        # Unvisited: single faint dotted trail
        trail_col = self._rgb_colors["connection"]
        for x1, y1, x2, y2 in unvisited_routes:
            self._draw_dashed_line(surf, trail_col,
                                   (int(x1), int(y1)), (int(x2), int(y2)),
                                   dash=5, gap=4, width=1)

        # Visited: hand-drawn wobbled ink road — dark border + warm fill
        road_border = self._rgb_colors["connection_border"]
        road_col    = self._rgb_colors["connection_visited"]
        road_hi     = self._rgb_colors["connection_vis_hi"]
        rng = random.Random(12345)
        for x1, y1, x2, y2 in visited_routes:
            # Break into 4 sub-segments with seeded jitter for a quill-stroke look
            dx = x2 - x1
            dy = y2 - y1
            dist = max(1, math.hypot(dx, dy))
            # perpendicular unit vector
            nx = -dy / dist
            ny =  dx / dist
            segs = 4
            pts = [(x1, y1)]
            for k in range(1, segs):
                t = k / segs
                mx_ = x1 + dx * t + nx * rng.uniform(-2.0, 2.0)
                my_ = y1 + dy * t + ny * rng.uniform(-2.0, 2.0)
                pts.append((int(mx_), int(my_)))
            pts.append((x2, y2))
            # Border pass (wider, darker)
            for i in range(len(pts) - 1):
                pygame.draw.line(surf, road_border, pts[i], pts[i+1], 4)
            # Road fill
            for i in range(len(pts) - 1):
                pygame.draw.line(surf, road_col, pts[i], pts[i+1], 2)

        # Boat sea-routes: dashed with small wave marks
        boat_col = self._rgb_colors["boat_line"]
        boat_hi  = self._rgb_colors["boat_line_hi"]
        for x1, y1, x2, y2 in boat_routes:
            ctrl = self._boat_control_point(x1, y1, x2, y2)
            self._draw_dashed_curve(surf, boat_col,
                                    (int(x1), int(y1)), ctrl, (int(x2), int(y2)),
                                    dash=12, gap=6, width=3, samples=36)
            self._draw_dashed_curve(surf, boat_hi,
                                    (int(x1), int(y1)), ctrl, (int(x2), int(y2)),
                                    dash=12, gap=6, width=1, samples=36)
            # Small "~" wave ticks along the curve (quarter, mid, three-quarter)
            for t_wave in (0.25, 0.5, 0.75):
                wx, wy = self._quad_point((x1, y1), ctrl, (x2, y2), t_wave)
                wx = int(wx)
                wy = int(wy)
                for dxw in (-5, 0, 5):
                    pygame.draw.arc(surf, boat_hi,
                                    (wx + dxw - 3, wy - 3, 6, 6),
                                    0, math.pi, 1)

    def _get_room_style(self, tag, room_id=""):
        styles = {
            "current":    (self._c("current_fill"),          self._c("current_outline"),          self._c("text")),
            "visited":    (self._c("visited_fill"),           self._c("visited_outline"),           self._c("text")),
            "unexplored": (self._c("unexplored_fill"),        self._c("unexplored_dot"),            self._c("text_dim")),
            "entrance":   (self._c("entrance_fill"),          self._c("entrance_outline"),          self._c("entrance_outline")),
            "stairs":     (self._c("stairs_fill"),            self._c("stairs_outline"),            self._c("stairs_outline")),
            "treasure":   (self._c("treasure_fill"),          self._c("treasure_outline"),          self._c("treasure_outline")),
            "dungeon_entrance": (self._c("dungeon_entrance_fill"), self._c("dungeon_entrance_outline"), self._c("dungeon_entrance_outline")),
        }

        if tag == "visited" and room_id:
            region = self._detect_region_cached(room_id)
            if region in self._rgb_region:
                fill, outline = self._rgb_region[region]
                return (fill, outline, self._c("text"))

        return styles.get(tag, styles["unexplored"])

    def _detect_region_cached(self, room_id):
        cached = self._region_cache.get(room_id)
        if cached is not None:
            return cached
        result = self._detect_region(room_id)
        self._region_cache[room_id] = result
        return result

    @staticmethod
    def _detect_region(room_id):
        rid = room_id.lower()
        if rid.startswith("sunstone_"):  return "sunstone"
        if rid.startswith("emerald_"):   return "emerald"
        if rid.startswith("stormbreak_"):return "stormbreak"
        if rid.startswith("cinder_"):    return "cinderforge"
        if rid.startswith("dreadmist_"): return "dreadmist"
        if rid.startswith("wyrm_"):      return "wyrmscale"
        if rid.startswith("abyssal_"):   return "abyssal"
        if any(kw in rid for kw in ("grand_harbor", "harbor_north_dock", "harbor_east_dock",
                                     "harbor_west_dock", "harbor_south_pier", "harbor_warehouse",
                                     "harbor_watchtower", "harbor_master", "harbor_tavern",
                                     "harbor_inn", "harbor_shop")):
            return "dock"
        if any(kw in rid for kw in ("castle", "royal", "kingshold", "throne")):
            return "castle"
        if any(kw in rid for kw in ("desert", "dunes", "oasis", "sand", "pyramid",
                                     "scorpion", "mesa", "canyon", "caravan", "nomad",
                                     "djinn", "cactus", "vulture", "salt_flat")):
            return "desert"
        if any(kw in rid for kw in ("frozen", "tundra", "ice", "frost", "glacier",
                                     "polar", "blizzard", "mammoth", "aurora", "snow")):
            return "tundra"
        if any(kw in rid for kw in ("port", "harbor", "pier", "lighthouse", "coastal",
                                     "shipwreck", "reef", "coral", "kelp", "mermaid",
                                     "whale", "pelican", "shrimp", "smuggler")):
            return "coast"
        if any(kw in rid for kw in ("forest", "grove", "clearing", "mossy", "woodland",
                                     "hermit", "deep_forest", "ancient_grove", "thicket",
                                     "logging", "fairy", "ravine", "wolf", "bear",
                                     "spider", "fallen", "hollow_tree", "hunter", "orchard",
                                     "twilight", "mushroom", "berry", "fox")):
            return "forest"
        if any(kw in rid for kw in ("swamp", "witch", "marsh", "foggy", "bog",
                                     "crocodile", "leech", "cypress", "frog", "drowned",
                                     "lily", "corpse_grove", "quicksand")):
            return "swamp"
        if any(kw in rid for kw in ("mountain", "highland", "peak", "foothills",
                                     "cliff", "pass", "avalanche", "goat", "eagle",
                                     "mining", "dwarf", "waterfall", "stream", "hot_spring")):
            return "mountain"
        if any(kw in rid for kw in ("village", "tavern", "shop", "blacksmith",
                                     "chapel", "farmland", "stable", "inn", "guild",
                                     "apothecary", "baker", "market", "notice", "well",
                                     "training", "garden", "pasture", "shepherd", "mill",
                                     "covered_bridge", "ferry")):
            return "village"
        if any(kw in rid for kw in ("river", "bank", "beach", "dock", "lake",
                                     "tidal", "fishing", "old_dock", "tide_pool",
                                     "sandy_beach", "sea_cave", "pond")):
            return "river"
        if any(kw in rid for kw in ("grave", "crypt", "battlefield", "cemetery",
                                     "haunted", "cursed", "tomb", "raven")):
            return "graveyard"
        if any(kw in rid for kw in ("ruins", "library", "watchtower", "crossroads",
                                     "sunken", "collapsed", "standing_stones", "shrine",
                                     "temple", "obelisk", "meteor", "dragon_bones")):
            return "ruins"
        return "default"

    @staticmethod
    def _room_shape(room_data):
        loc_type = (room_data.get("location_type") or "wilderness").lower()
        if loc_type == "building":   return "square"
        if loc_type in ("settlement", "dock"): return "diamond"
        if loc_type in ("mountain", "highland"): return "triangle"
        return "circle"

    @staticmethod
    def _terrain_symbol(tag, room_data):
        """Return a small Unicode terrain glyph for the given tag/region."""
        if tag == "current":          return "\u2605"  # ★
        if tag == "dungeon_entrance":  return "\u2620"  # ☠
        if tag == "stairs":            return "\u21d3"  # ⇓
        if tag == "treasure":          return "\u25c6"  # ◆
        if tag == "entrance":          return "\u25b7"  # ▷
        loc = (room_data.get("location_type") or "").lower()
        if loc == "building":   return "\u2302"  # ⌂
        if loc in ("settlement", "dock"): return "\u25a0"  # ■
        return ""

    def _draw_terrain_marker(self, surf, ipx, ipy, r, fill, outline, tag, room_data):
        """Draw a medieval cartographic icon for each room type."""
        loc_type = (room_data.get("location_type") or "wilderness").lower() if room_data else ""
        region   = self._detect_region_cached(room_data.get("_rid", "")) if room_data else "default"
        ink  = self._rgb_colors["ink"]
        ink2 = self._rgb_colors["ink_mid"]

        # ── CURRENT PLAYER: 8-pointed heraldic star ─────────────────
        if tag == "current":
            glow = self._rgb_colors["current_glow"]
            # outer glow rings
            for gr in (r + 10, r + 6):
                pygame.draw.circle(surf, glow, (ipx, ipy), gr, 1)
            # 8-pointed star: 4 long + 4 short diamond points
            star_pts = []
            for i in range(8):
                angle = math.radians(i * 45 - 90)
                rad = r if (i % 2 == 0) else r * 0.48
                star_pts.append((int(ipx + math.cos(angle) * rad),
                                 int(ipy + math.sin(angle) * rad)))
            pygame.draw.polygon(surf, fill, star_pts)
            pygame.draw.polygon(surf, outline, star_pts, 1)
            # white center dot
            pygame.draw.circle(surf, (255, 250, 240), (ipx, ipy), max(2, r // 4))
            return

        # ── DUNGEON ENTRANCE: dark arch (rectangle + semicircle top) ─
        if tag == "dungeon_entrance":
            hw = max(5, r - 2)
            hh = max(6, int(r * 1.1))
            arch_rect = pygame.Rect(ipx - hw, ipy - hh // 2, hw * 2, hh)
            # body
            pygame.draw.rect(surf, fill, arch_rect, border_radius=hw)
            pygame.draw.rect(surf, outline, arch_rect, 2, border_radius=hw)
            # skull glyph inside (simplistic: two dots + horizontal line)
            ey = ipy - r // 5
            for ex in (-r // 3, r // 3):
                pygame.draw.circle(surf, outline, (ipx + ex, ey), max(1, r // 6))
            pygame.draw.line(surf, outline,
                             (ipx - r // 3, ipy + r // 5), (ipx + r // 3, ipy + r // 5), 1)
            return

        # ── STAIRS: downward pointing pennant ────────────────────────
        if tag == "stairs":
            pts = [(ipx - r + 2, ipy - r + 2), (ipx + r - 2, ipy - r + 2),
                   (ipx, ipy + r - 2)]
            pygame.draw.polygon(surf, fill, pts)
            pygame.draw.polygon(surf, outline, pts, 2)
            return

        # ── TREASURE: small octagon in gold ──────────────────────────
        if tag == "treasure":
            oct_pts = [(int(ipx + r * math.cos(math.radians(a * 45 - 22.5))),
                        int(ipy + r * math.sin(math.radians(a * 45 - 22.5))))
                       for a in range(8)]
            pygame.draw.polygon(surf, fill, oct_pts)
            pygame.draw.polygon(surf, outline, oct_pts, 2)
            # cross inside
            pygame.draw.line(surf, outline, (ipx - r + 3, ipy), (ipx + r - 3, ipy), 1)
            pygame.draw.line(surf, outline, (ipx, ipy - r + 3), (ipx, ipy + r - 3), 1)
            return

        # ── ENTRANCE: arrow pointing right (gateway) ─────────────────
        if tag == "entrance":
            pts = [(ipx - r + 2, ipy - r // 2), (ipx + r // 2, ipy - r // 2),
                   (ipx + r - 2, ipy), (ipx + r // 2, ipy + r // 2),
                   (ipx - r + 2, ipy + r // 2)]
            pygame.draw.polygon(surf, fill, pts)
            pygame.draw.polygon(surf, outline, pts, 2)
            return

        # ── MOUNTAIN: layered peaks ───────────────────────────────────
        if region in ("mountain",) or loc_type in ("mountain", "highland"):
            # back peak (slightly offset for depth)
            back_pts = [(ipx - r + 2, ipy + r - 2),
                        (ipx + r // 3, ipy - r + 4),
                        (ipx + r + 2, ipy + r - 2)]
            pygame.draw.polygon(surf, ink2, back_pts)
            # front peak
            front_pts = [(ipx - r - 2, ipy + r - 2),
                         (ipx - r // 4, ipy - r + 2),
                         (ipx + r // 2, ipy + r - 2)]
            pygame.draw.polygon(surf, fill, front_pts)
            pygame.draw.polygon(surf, outline, front_pts, 1)
            # snow cap on front peak
            cap_y = ipy - r + 2 + int((r * 2 - 4) * 0.28)
            cap_pts = [(ipx - r // 4, ipy - r + 2),
                       (ipx - r // 4 + int(r * 0.3), cap_y),
                       (ipx - r // 4 - int(r * 0.12), cap_y)]
            pygame.draw.polygon(surf, (240, 240, 235), cap_pts)
            return

        # ── FOREST: canopy circle on trunk ───────────────────────────
        if region in ("forest",) or loc_type in ("forest",):
            trunk_h = max(3, r // 2)
            trunk_w = max(2, r // 3)
            # trunk
            pygame.draw.rect(surf, ink2,
                             (ipx - trunk_w // 2, ipy + r - trunk_h - 2, trunk_w, trunk_h))
            # canopy (two overlapping circles for layered crown look)
            cr = max(4, r - 2)
            pygame.draw.circle(surf, fill, (ipx, ipy - r // 6), cr)
            pygame.draw.circle(surf, outline, (ipx, ipy - r // 6), cr, 1)
            return

        # ── CASTLE: tower with crenellations ─────────────────────────
        if region in ("castle",) or loc_type in ("castle", "keep"):
            tw = max(6, r - 2)
            th = max(8, int(r * 1.2))
            bx_ = ipx - tw
            by_ = ipy - th // 2
            pygame.draw.rect(surf, fill, (bx_, by_, tw * 2, th))
            pygame.draw.rect(surf, outline, (bx_, by_, tw * 2, th), 1)
            # crenellations (3 merlons)
            merlon_w = max(3, tw * 2 // 5)
            merlon_h = max(2, th // 4)
            for mi in range(3):
                mx_ = bx_ + mi * (tw * 2 - merlon_w) // 2
                pygame.draw.rect(surf, fill, (mx_, by_ - merlon_h, merlon_w, merlon_h))
                pygame.draw.rect(surf, outline, (mx_, by_ - merlon_h, merlon_w, merlon_h), 1)
            return

        # ── VILLAGE / SETTLEMENT: house silhouette ────────────────────
        if region in ("village",) or loc_type in ("settlement", "village"):
            hw = max(5, r - 1)
            wall_h = max(5, int(r * 0.8))
            wx = ipx - hw
            wy = ipy - wall_h // 2
            # walls
            pygame.draw.rect(surf, fill, (wx, wy, hw * 2, wall_h))
            pygame.draw.rect(surf, outline, (wx, wy, hw * 2, wall_h), 1)
            # roof (triangle)
            roof_pts = [(wx - 1, wy), (ipx + hw + 1, wy),
                        (ipx, wy - max(4, int(r * 0.7)))]
            pygame.draw.polygon(surf, ink2, roof_pts)
            pygame.draw.polygon(surf, outline, roof_pts, 1)
            return

        # ── DOCK / PORT: anchor shape ─────────────────────────────────
        if region in ("dock", "coast") or loc_type in ("dock", "port"):
            # vertical staff
            pygame.draw.line(surf, fill, (ipx, ipy - r), (ipx, ipy + r), 2)
            # crossbar
            pygame.draw.line(surf, fill, (ipx - r // 2, ipy - r // 2),
                             (ipx + r // 2, ipy - r // 2), 2)
            # anchor ring at top
            pygame.draw.circle(surf, fill, (ipx, ipy - r), max(2, r // 4), 1)
            # flukes at bottom
            pygame.draw.line(surf, fill, (ipx, ipy + r),
                             (ipx - r // 2, ipy + r // 2), 2)
            pygame.draw.line(surf, fill, (ipx, ipy + r),
                             (ipx + r // 2, ipy + r // 2), 2)
            pygame.draw.circle(surf, outline, (ipx, ipy), r + 1, 1)
            return

        # ── BUILDING / SETTLEMENT (generic square): upright square ───
        if loc_type == "building":
            hw = max(5, r - 2)
            rect = pygame.Rect(ipx - hw, ipy - hw, hw * 2, hw * 2)
            pygame.draw.rect(surf, fill, rect, border_radius=1)
            pygame.draw.rect(surf, outline, rect, 2, border_radius=1)
            return

        # ── DEFAULT: filled circle — region coloured ──────────────────
        pygame.draw.circle(surf, fill, (ipx, ipy), r)
        if tag != "unexplored":
            pygame.draw.circle(surf, outline, (ipx, ipy), r, 1)

    def _draw_rooms(self, surf, positions, rooms, visited, sw, sh):
        r = int(self.ROOM_RADIUS * self._zoom)
        r = max(6, min(r, 32))
        margin = r + 40

        # Remember latest hit map so clicks can pick the right room marker
        self._remember_hitmap(positions, rooms, visited, r)

        show_labels = False  # keep map clean; labels are shown on click
        max_chars   = max(8, int(18 * self._zoom)) if show_labels else 0
        font_size   = max(7, int(9 * self._zoom)) if show_labels else 9
        label_offset = r + int(10 * self._zoom) if show_labels else 0
        icon_size = max(7, int(11 * self._zoom))
        small_dot_r = max(3, int(4 * self._zoom))

        for rid, (px, py) in positions.items():
            ipx, ipy = int(px), int(py)
            if ipx < -margin or ipx > sw + margin or ipy < -margin or ipy > sh + margin:
                continue

            rdata = rooms.get(rid, {})
            if isinstance(rdata, dict):
                rdata["_rid"] = rid   # stash id for region lookup in marker
            is_visible = rid in visited or self.reveal_all

            if not is_visible:
                # Fog-of-war: tiny × cross in dim ink
                dot_col = self._c("unexplored_dot")
                cr = max(2, small_dot_r - 1)
                pygame.draw.line(surf, dot_col, (ipx - cr, ipy - cr), (ipx + cr, ipy + cr), 1)
                pygame.draw.line(surf, dot_col, (ipx + cr, ipy - cr), (ipx - cr, ipy + cr), 1)
                continue

            tag = self._room_tag(rid, rdata, self.current_location, visited)
            fill, outline, label_color = self._get_room_style(tag, rid)

            self._draw_terrain_marker(surf, ipx, ipy, r, fill, outline, tag, rdata)

            # Icon symbol above the marker (only for special tags)
            sym = self._terrain_symbol(tag, rdata)
            if sym:
                sym_size = icon_size + (4 if tag == "current" else 0)
                txt = self._render_text(sym,
                                        (0, 0, 0) if tag == "current" else outline,
                                        sym_size)
                surf.blit(txt, (ipx - txt.get_width() // 2, ipy - txt.get_height() // 2))

            # Name label below marker — parchment-toned backing
            if show_labels:
                name = (rdata.get("name", "???") if isinstance(rdata, dict)
                        else (getattr(rdata, "name", None) or "???"))
                if len(name) > max_chars:
                    name = name[:max_chars - 2] + ".."
                lbl_col = self._c("text") if tag != "unexplored" else self._c("text_dim")
                lbl = self._render_text(name, lbl_col, font_size)
                lx = ipx - lbl.get_width() // 2
                ly = ipy + label_offset + 2
                pad = 2
                box = pygame.Rect(lx - pad, ly - 1, lbl.get_width() + pad * 2, lbl.get_height() + 1)
                pygame.draw.rect(surf, self._c("text_label_bg"), box)
                pygame.draw.rect(surf, self._c("ink_mid"), box, 1)
                surf.blit(lbl, (lx, ly))

            # Overlay a large, always-legible label for the selected room
            self._draw_selected_label(surf, positions, rooms)

    def _draw_selected_label(self, surf, positions, rooms):
        sel = self._selected_room_id
        if not sel or sel not in positions or sel not in rooms:
            return

        px, py = positions[sel]
        rdata = rooms.get(sel, {})
        name = (rdata.get("name", "???") if isinstance(rdata, dict)
                else (getattr(rdata, "name", None) or "???"))

        txt = self._render_text(name, self._c("text"), 17)
        pad = 6
        w = txt.get_width() + pad * 2
        h = txt.get_height() + pad * 2

        sw, sh = surf.get_size()
        offset = max(22, self._hit_radius + 8)
        # Prefer placing to the right; fall back to the left if near the edge.
        bx = int(px + offset)
        place_left = False
        if bx + w + 12 > sw:
            bx = int(px - offset - w)
            place_left = True
        bx = max(8, min(bx, sw - w - 8))

        by = int(py - h // 2)
        by = max(8, min(by, sh - h - 8))

        rect = pygame.Rect(bx, by, w, h)
        bg = self._c("text_label_bg")
        bord = self._c("border_inner")
        ink = self._c("ink_mid")

        # Draw connector first so the label sits on top of it
        anchor_x = rect.right if place_left else rect.left
        anchor_y = rect.y + rect.height // 2
        pygame.draw.line(surf, ink, (int(px), int(py)), (anchor_x, anchor_y), 2)

        pygame.draw.rect(surf, bg, rect, border_radius=4)
        pygame.draw.rect(surf, bord, rect, 2, border_radius=4)
        surf.blit(txt, (rect.x + pad, rect.y + pad))

        # Pointer from label edge toward the room marker
        if place_left:
            tri = [(rect.right, anchor_y), (rect.right + 12, anchor_y - 7), (rect.right + 12, anchor_y + 7)]
        else:
            tri = [(rect.left, anchor_y), (rect.left - 12, anchor_y - 7), (rect.left - 12, anchor_y + 7)]
        pygame.draw.polygon(surf, bg, tri)
        pygame.draw.polygon(surf, bord, tri, 1)

    def _draw_legend(self, surf, sh):
        """Draw a parchment scroll legend box in the bottom-right corner."""
        sw = surf.get_width()
        ink  = self._rgb_colors["ink"]
        ink2 = self._rgb_colors["ink_mid"]
        bg   = self._rgb_colors["text_label_bg"]
        bord = self._rgb_colors["border_inner"]

        items_col1 = [
            ("You \u2605",       self._c("current_fill"),  self._c("current_outline"),  "star"),
            ("Dungeon",    self._c("dungeon_entrance_fill"), self._c("dungeon_entrance_outline"), "arch"),
            ("Village",    *self._rgb_region["village"],   "house"),
            ("Forest",     *self._rgb_region["forest"],    "tree"),
            ("Mountain",   *self._rgb_region["mountain"],  "peak"),
            ("Castle",     *self._rgb_region["castle"],    "castle"),
        ]
        items_col2 = [
            ("Swamp",      *self._rgb_region["swamp"],     "circle"),
            ("Desert",     *self._rgb_region["desert"],    "circle"),
            ("Coast",      *self._rgb_region["coast"],     "circle"),
            ("Ruins",      *self._rgb_region["ruins"],     "circle"),
            ("Tundra",     *self._rgb_region["tundra"],    "circle"),
            ("Sea route",  self._rgb_colors["boat_line"],  self._rgb_colors["boat_line_hi"], "dash"),
        ]

        ITEM_H  = 16
        COL_W   = 88
        PAD     = 8
        rows    = max(len(items_col1), len(items_col2))
        BOX_W   = COL_W * 2 + PAD * 2
        BOX_H   = rows * ITEM_H + PAD + 18   # +18 for header
        BX      = sw - BOX_W - 10
        BY      = sh - BOX_H - 10

        # Box background
        pygame.draw.rect(surf, bg,   (BX, BY, BOX_W, BOX_H), border_radius=4)
        pygame.draw.rect(surf, bord, (BX, BY, BOX_W, BOX_H), 2, border_radius=4)

        # Header
        hdr = self._font_legend.render("\u2014  L E G E N D  \u2014", True, ink)
        surf.blit(hdr, (BX + (BOX_W - hdr.get_width()) // 2, BY + 4))
        pygame.draw.line(surf, ink2, (BX + PAD, BY + 16), (BX + BOX_W - PAD, BY + 16), 1)

        # Items
        for col_idx, items in enumerate((items_col1, items_col2)):
            cx = BX + PAD + col_idx * COL_W
            cy = BY + 20
            for label, fill, outline, shape in items:
                self._draw_legend_item(surf, cx, cy + ITEM_H // 2, label, fill, outline, shape)
                cy += ITEM_H

    def _draw_legend_item(self, surf, x, y, label, fill, outline, shape):
        """Draw one legend entry with a mini icon + label."""
        ink = self._rgb_colors["ink"]
        ICON_R = 5
        ix, iy = x + ICON_R + 1, y

        if shape == "star":
            pts = [(int(ix + ICON_R * math.cos(math.radians(i * 45 - 90))),
                    int(iy + ICON_R * (1 if i % 2 == 0 else 0.46) * math.sin(math.radians(i * 45 - 90))))
                   for i in range(8)]
            # fix: recompute properly
            pts = []
            for i in range(8):
                ang = math.radians(i * 45 - 90)
                rad = ICON_R if (i % 2 == 0) else ICON_R * 0.46
                pts.append((int(ix + math.cos(ang) * rad), int(iy + math.sin(ang) * rad)))
            pygame.draw.polygon(surf, fill, pts)
            pygame.draw.polygon(surf, outline, pts, 1)
        elif shape == "arch":
            pygame.draw.rect(surf, fill,    (ix - ICON_R, iy - ICON_R, ICON_R * 2, ICON_R * 2), border_radius=ICON_R)
            pygame.draw.rect(surf, outline, (ix - ICON_R, iy - ICON_R, ICON_R * 2, ICON_R * 2), 1, border_radius=ICON_R)
        elif shape == "house":
            hw = ICON_R
            pygame.draw.rect(surf, fill,    (ix - hw, iy - 2,     hw * 2, ICON_R + 2))
            pygame.draw.rect(surf, outline, (ix - hw, iy - 2,     hw * 2, ICON_R + 2), 1)
            roof_pts = [(ix - hw - 1, iy - 2), (ix + hw + 1, iy - 2), (ix, iy - ICON_R - 2)]
            pygame.draw.polygon(surf, outline, roof_pts, 1)
        elif shape == "tree":
            pygame.draw.circle(surf, fill,    (ix, iy - 2), ICON_R)
            pygame.draw.circle(surf, outline, (ix, iy - 2), ICON_R, 1)
            pygame.draw.line(surf, outline,   (ix, iy + ICON_R - 2), (ix, iy + ICON_R + 1), 1)
        elif shape == "peak":
            p = [(ix - ICON_R, iy + ICON_R - 1), (ix, iy - ICON_R),
                 (ix + ICON_R, iy + ICON_R - 1)]
            pygame.draw.polygon(surf, fill,    p)
            pygame.draw.polygon(surf, outline, p, 1)
        elif shape == "castle":
            pygame.draw.rect(surf, fill,    (ix - ICON_R, iy - 3, ICON_R * 2, ICON_R + 3))
            pygame.draw.rect(surf, outline, (ix - ICON_R, iy - 3, ICON_R * 2, ICON_R + 3), 1)
            for mi in range(3):
                mx_ = ix - ICON_R + mi * ICON_R - 1
                pygame.draw.rect(surf, fill,    (mx_, iy - 3 - 3, 4, 3))
                pygame.draw.rect(surf, outline, (mx_, iy - 3 - 3, 4, 3), 1)
        elif shape == "dash":
            for di in range(3):
                pygame.draw.line(surf, fill,
                                 (ix - ICON_R + di * 4, iy),
                                 (ix - ICON_R + di * 4 + 2, iy), 2)
        elif shape == "square":
            pygame.draw.rect(surf, fill,    (ix - ICON_R, iy - ICON_R, ICON_R * 2, ICON_R * 2))
            pygame.draw.rect(surf, outline, (ix - ICON_R, iy - ICON_R, ICON_R * 2, ICON_R * 2), 1)
        else:  # circle
            pygame.draw.circle(surf, fill,    (ix, iy), ICON_R)
            pygame.draw.circle(surf, outline, (ix, iy), ICON_R, 1)

        txt = self._font_legend.render(label, True, ink)
        surf.blit(txt, (x + ICON_R * 2 + 4, y - txt.get_height() // 2))

    # ── decorative helpers ──────────────────────────────────────────

    def _draw_sea_waves(self, surf, positions, rooms=None):
        """Scatter hand-drawn ~ wave marks in the ocean, avoiding all island polygons."""
        if not positions:
            return
        sw, sh = surf.get_size()
        xs = [p[0] for p in positions.values()]
        ys = [p[1] for p in positions.values()]
        if not xs:
            return

        # Build world-space positions for zoom-independent clustering
        world_pos = {}
        if rooms:
            for rid in positions:
                if rid in rooms:
                    c = rooms[rid].get("coordinates", [0, 0])
                    world_pos[rid] = self._safe_xy(c)
        world_pos = world_pos if len(world_pos) == len(positions) else None

        # Build per-island exclusion ellipses from the same spatial clusters
        components = self._find_island_components(positions, world_pos)
        island_ellipses = []
        for comp in components:
            cxs = [p[0] for p in comp.values()]
            cys = [p[1] for p in comp.values()]
            if not cxs:
                continue
            icx = (min(cxs) + max(cxs)) / 2
            icy = (min(cys) + max(cys)) / 2
            # match exactly the rw/rh used in _draw_single_island, × max jitter (1.18)
            irw = max(70, (max(cxs) - min(cxs)) / 2 + 75) * 1.18
            irh = max(70, (max(cys) - min(cys)) / 2 + 75) * 1.18 * 0.78
            island_ellipses.append((icx, icy, irw, irh))

        # Anchor wave grid to the overall bounding-box centre so waves pan with land
        cx = (min(xs) + max(xs)) / 2
        cy = (min(ys) + max(ys)) / 2

        wave_col = self._rgb_colors["ocean_deep"]
        step = 52
        # Build the jitter offset table once — creating 425 random.Random() objects per
        # bake costs ~5 ms; pre-computing reduces sea-wave bake overhead to < 0.2 ms.
        if self._wave_jitter_table is None:
            tbl = []
            for gy_idx in range(-8, 9):
                for gx_idx in range(-12, 13):
                    cell_rng = random.Random(gx_idx * 997 + gy_idx * 31)
                    tbl.append((gx_idx, gy_idx,
                                cell_rng.randint(-18, 18),
                                cell_rng.randint(-14, 14)))
            self._wave_jitter_table = tbl

        for gx_idx, gy_idx, jx_off, jy_off in self._wave_jitter_table:
            jx = int(cx + gx_idx * step + jx_off)
            jy = int(cy + gy_idx * step + jy_off)
            # Skip if inside any island ellipse
            in_land = any(
                ((jx - icx) / max(1, irw)) ** 2
                + ((jy - icy) / max(1, irh)) ** 2 < 1.0
                for icx, icy, irw, irh in island_ellipses
            )
            if in_land:
                continue
            if jx < 4 or jy < 4 or jx > sw - 4 or jy > sh - 4:
                continue
            for wk in range(2):
                ox = jx + wk * 7
                try:
                    pygame.draw.arc(surf, wave_col,
                                    (ox - 3, jy - 2, 6, 4), 0, math.pi, 1)
                except Exception:
                    pass

    def _draw_compass_rose(self, surf, sw, sh):
        """Draw a medieval compass rose in the bottom-left corner."""
        SIZE  = 52
        cx    = 18 + SIZE // 2
        cy    = sh - 18 - SIZE // 2
        fg    = self._rgb_colors["compass_fg"]
        bg    = self._rgb_colors["compass_bg"]
        bord  = self._rgb_colors["border_inner"]

        # Background circle
        pygame.draw.circle(surf, bg,   (cx, cy), SIZE // 2)
        pygame.draw.circle(surf, bord, (cx, cy), SIZE // 2, 1)

        # 4 cardinal spear-points (N/S long, E/W shorter)
        lengths = {"N": SIZE // 2 - 3, "S": SIZE // 2 - 3,
                   "E": SIZE // 2 - 8, "W": SIZE // 2 - 8}
        half_w = {"N": 5, "S": 5, "E": 4, "W": 4}
        directions = {
            "N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0),
        }
        for name, (dx, dy) in directions.items():
            tip  = (cx + dx * lengths[name], cy + dy * lengths[name])
            perp = (-dy, dx)
            hw   = half_w[name]
            base_l = (cx + perp[0] * hw, cy + perp[1] * hw)
            base_r = (cx - perp[0] * hw, cy - perp[1] * hw)
            # front half (bright)
            pygame.draw.polygon(surf, fg,   [tip, base_l, base_r])
            pygame.draw.polygon(surf, bord, [tip, base_l, base_r], 1)

        # 4 diagonal small points
        diag_len = SIZE // 2 - 12
        for ang in (45, 135, 225, 315):
            rad = math.radians(ang)
            tip = (cx + int(math.cos(rad) * diag_len),
                   cy + int(math.sin(rad) * diag_len))
            perp_ang = rad + math.pi / 2
            hw = 3
            base_l = (cx + int(math.cos(perp_ang) * hw),
                      cy + int(math.sin(perp_ang) * hw))
            base_r = (cx - int(math.cos(perp_ang) * hw),
                      cy - int(math.sin(perp_ang) * hw))
            pygame.draw.polygon(surf, fg,   [tip, base_l, base_r])

        # Center dot
        pygame.draw.circle(surf, bg,   (cx, cy), 5)
        pygame.draw.circle(surf, bord, (cx, cy), 5, 1)
        pygame.draw.circle(surf, fg,   (cx, cy), 2)

        # Cardinal letters
        font = self._font_legend
        for letter, (dx, dy) in [("N", (0, -1)), ("S", (0, 1)),
                                   ("E", (1, 0)),  ("W", (-1, 0))]:
            lsurf = font.render(letter, True, fg)
            off   = SIZE // 2 + 3
            lx    = cx + dx * off - lsurf.get_width() // 2
            ly    = cy + dy * off - lsurf.get_height() // 2
            surf.blit(lsurf, (lx, ly))

    def _draw_map_border(self, surf, sw, sh):
        """Draw a decorative double-line frame with corner ornaments."""
        outer_col  = self._rgb_colors["border_outer"]
        inner_col  = self._rgb_colors["border_inner"]
        # outer frame
        pygame.draw.rect(surf, outer_col, (2, 2, sw - 4, sh - 4), 3)
        # inner frame (4 px gap)
        pygame.draw.rect(surf, inner_col, (8, 8, sw - 16, sh - 16), 1)
        # Corner ornament squares
        for ox, oy in ((2, 2), (sw - 12, 2), (2, sh - 12), (sw - 12, sh - 12)):
            pygame.draw.rect(surf, outer_col, (ox, oy, 10, 10))
            pygame.draw.rect(surf, inner_col, (ox + 2, oy + 2, 6, 6))

    # ── dungeon renderer ────────────────────────────────────────────
    def _render_dungeon_map(self):
        surf = self._map_surface
        sw, sh = surf.get_size()
        # Dark stone background
        surf.fill(self._rgb_colors["bg"])

        # Stone-block texture: seeded small rects slightly lighter than bg
        rng = random.Random(314)
        stone_col = self._rgb_colors["dungeon_stone"]
        for _ in range(180):
            bx = rng.randint(0, sw - 8)
            by = rng.randint(0, sh - 8)
            bw = rng.randint(4, 9)
            bh = rng.randint(3, 7)
            pygame.draw.rect(surf, stone_col, (bx, by, bw, bh))

        floor_num = self._current_floor_number()
        total_floors = self._get_dungeon_total_floors()
        rooms = self._get_dungeon_floor_rooms(floor_num)

        visited = set(self.visited_rooms) if not self.reveal_all else set(rooms.keys())

        self._clear_hitmap()

        if self._header_label:
            self._header_label.set_text(
                f"\u2694  DUNGEON  \u2014  FLOOR {floor_num} / {total_floors}  \u2694"
            )

        if not rooms:
            txt = self._font_header.render("No dungeon rooms on this floor.", True,
                                           self._rgb_colors["ink_mid"])
            surf.blit(txt, (sw//2 - txt.get_width()//2, sh//2 - txt.get_height()//2))
            self._draw_map_border(surf, sw, sh)
            return

        coord_map = {}
        for rid, rdata in rooms.items():
            c = rdata.get("coordinates", [0, 0]) if isinstance(rdata, dict) else [0, 0]
            x, y = self._safe_xy(c)
            coord_map[(x, y)] = rid

        positions, spacing = self._compute_layout(coord_map, sw, sh)

        self._draw_land_mass(surf, positions, rooms)
        self._draw_grid(surf, positions, spacing)
        self._draw_connections(surf, positions, rooms, visited, sw, sh)
        self._draw_rooms(surf, positions, rooms, visited, sw, sh)
        self._draw_legend(surf, sh)
        self._draw_map_border(surf, sw, sh)

        total = len(rooms)
        found = sum(1 for r in rooms if r in visited)
        cur_name = rooms.get(self.current_location, {}).get("name", "Unknown")
        fog = "\U0001f513 Reveal ON" if self.reveal_all else "\U0001f512 Fog of War"
        if self._stats_label:
            self._stats_label.set_text(
                f"Location: {cur_name}  |  Floor {floor_num} Discovered: {found}/{total}  |  {fog}"
            )

    # ── overworld renderer ──────────────────────────────────────────
    def _build_overworld_rooms(self):
        cur_count = len(self.rooms_data)
        if self._cached_overworld_rooms is not None and self._cached_room_count == cur_count:
            return self._cached_overworld_rooms

        rooms = {}
        fixed_ids = set()
        if self.game_engine and hasattr(self.game_engine, 'fixed_dungeon_room_ids'):
            fixed_ids = self.game_engine.fixed_dungeon_room_ids
        for rid, room_obj in self.rooms_data.items():
            if rid.startswith("dungeon_") and "_floor" in rid:
                continue
            if rid in fixed_ids:
                continue
            if self._is_home_room_id(rid, room_obj):
                continue

            raw_coords = getattr(room_obj, "coordinates", None)
            if raw_coords is None and isinstance(room_obj, dict):
                raw_coords = room_obj.get("coordinates", [0, 0])

            raw_exits = getattr(room_obj, "exits", None)
            if raw_exits is None and isinstance(room_obj, dict):
                raw_exits = room_obj.get("exits", {})
            if not isinstance(raw_exits, dict):
                raw_exits = {}

            rooms[rid] = {
                "name": getattr(room_obj, "name", None)
                        or (room_obj.get("name", "???") if isinstance(room_obj, dict) else "???"),
                "coordinates": self._normalize_coordinates(raw_coords),
                "location_type": getattr(room_obj, "location_type", None)
                                 or (room_obj.get("location_type", "wilderness") if isinstance(room_obj, dict) else "wilderness"),
                "exits": raw_exits,
            }
        self._cached_overworld_rooms = rooms
        self._cached_room_count = cur_count
        return rooms

    def _render_overworld_map(self):
        surf = self._map_surface
        sw, sh = surf.get_size()

        rooms = self._build_overworld_rooms()
        visited = set(self.visited_rooms) if not self.reveal_all else set(rooms.keys())

        self._clear_hitmap()

        if self._header_label:
            self._header_label.set_text("\u2014  OVERWORLD MAP  \u2014")

        if not rooms:
            surf.fill(self._rgb_colors["ocean"])
            txt = self._font_header.render("No rooms found.", True,
                                           self._rgb_colors["ink_mid"])
            surf.blit(txt, (sw//2 - txt.get_width()//2, sh//2 - txt.get_height()//2))
            self._draw_map_border(surf, sw, sh)
            return

        coord_map = {}
        for rid, rdata in rooms.items():
            x, y = self._safe_xy(rdata.get("coordinates", [0, 0]))
            coord_map[(x, y)] = rid

        # ── Background: ocean, grid, island, waves (drawn directly every frame) ──
        # A surface-bake cache was tried but always crashes or clips at high zoom
        # because the bake surface must be sized to hold the full island polygon
        # which grows enormous at ZOOM_MAX with a large world.  Drawing directly
        # is fast enough (~1.6 ms) thanks to the wave-jitter table (built once)
        # and the island-cluster cache (O(n) on cache hit, O(n²) on zoom change).
        positions, spacing = self._compute_layout(coord_map, sw, sh)

        # Reset island obstacle; _draw_land_mass will cache it for boat routing
        self._main_island_obstacle = None

        surf.fill(self._rgb_colors["ocean"])
        grid_col = self._rgb_colors["ocean_lines"]
        for gx_px in range(0, sw, 32):
            pygame.draw.line(surf, grid_col, (gx_px, 0), (gx_px, sh), 1)
        for gy_px in range(0, sh, 32):
            pygame.draw.line(surf, grid_col, (0, gy_px), (sw, gy_px), 1)
        self._draw_sea_waves(surf, positions, rooms)
        self._draw_land_mass(surf, positions, rooms)

        # Dynamic layers — fast (~1 ms total)
        self._draw_connections(surf, positions, rooms, visited, sw, sh)
        self._draw_rooms(surf, positions, rooms, visited, sw, sh)
        # Fixed UI elements (screen-space, not panned)
        self._draw_compass_rose(surf, sw, sh)
        self._draw_legend(surf, sh)
        self._draw_map_border(surf, sw, sh)

        total = len(rooms)
        found = sum(1 for r in rooms if r in visited)
        cur_name = rooms.get(self.current_location, {}).get("name", "Unknown")
        fog = "\U0001f513 Reveal ON" if self.reveal_all else "\U0001f512 Fog of War"
        if self._stats_label:
            self._stats_label.set_text(
                f"Location: {cur_name}  |  Discovered: {found}/{total}  |  {fog}"
            )
        if self._region_label and self.current_location:
            region = self._detect_region_cached(self.current_location).title()
            self._region_label.set_text(f"Region: {region}")

    # ── helpers ─────────────────────────────────────────────────────
    def _player_in_home(self) -> bool:
        if not self.current_location:
            return False
        if HOME_MAP_AVAILABLE:
            try:
                return is_home_room(self.current_location)
            except Exception:
                return self.current_location == "player_home"
        return self.current_location == "player_home"

    def _render_home_map(self):
        surf = self._map_surface
        sw, sh = surf.get_size()

        self._clear_hitmap()

        bg = (92, 63, 39)
        floor = (120, 84, 56)
        wall = (58, 39, 24)
        section = (104, 74, 49)
        marker = (255, 220, 120)
        text_col = (245, 235, 210)

        surf.fill(bg)

        if self._header_label:
            self._header_label.set_text("- HOME MAP -")

        player = getattr(self.game_engine, "player", None)
        home_data = {}
        if player and isinstance(getattr(player, "state", {}), dict):
            home_data = player.state.get("home_data", {}) or {}

        if HOME_MAP_AVAILABLE and home_data:
            tiles = get_unlocked_tiles(home_data)
        else:
            tiles = [(x, y) for x in range(8) for y in range(6)]

        if not tiles:
            tiles = [(x, y) for x in range(8) for y in range(6)]

        xs = [t[0] for t in tiles]
        ys = [t[1] for t in tiles]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        grid_w = max_x - min_x + 1
        grid_h = max_y - min_y + 1
        tile_size = max(18, min(44, min((sw - 130) // max(1, grid_w), (sh - 150) // max(1, grid_h))))
        origin_x = (sw - grid_w * tile_size) // 2
        origin_y = (sh - grid_h * tile_size) // 2

        expansions = set(home_data.get("unlocked_expansions", [])) if isinstance(home_data, dict) else set()

        for tx, ty in tiles:
            sx = origin_x + (tx - min_x) * tile_size
            sy = origin_y + (ty - min_y) * tile_size
            color = section if (tx >= 8 or ty >= 6) else floor
            pygame.draw.rect(surf, color, (sx, sy, tile_size - 1, tile_size - 1))

        outer_x = origin_x - 4
        outer_y = origin_y - 4
        outer_w = grid_w * tile_size + 8
        outer_h = grid_h * tile_size + 8
        pygame.draw.rect(surf, wall, (outer_x, outer_y, outer_w, outer_h), 4)

        placed_items = []
        if isinstance(home_data, dict):
            placed_items = home_data.get("placed_items", []) or []

        label_font = self._get_font(10)

        for placed in placed_items:
            if not isinstance(placed, dict):
                continue
            item_id = placed.get("item_id", "")
            x = int(placed.get("x", 0))
            y = int(placed.get("y", 0))
            if (x, y) not in set(tiles):
                continue
            sx = origin_x + (x - min_x) * tile_size
            sy = origin_y + (y - min_y) * tile_size
            item_def = get_home_item(item_id) or {} if HOME_MAP_AVAILABLE else {}
            if not isinstance(item_def, dict):
                item_def = {}
            item_color = (225, 201, 150)
            if HOME_MAP_AVAILABLE:
                hex_col = item_def.get("map_color", "#d4b07a").lstrip("#")
                if len(hex_col) == 6:
                    item_color = tuple(int(hex_col[i:i+2], 16) for i in (0, 2, 4))

            inner = pygame.Rect(sx + 2, sy + 2, tile_size - 4, tile_size - 4)
            drew = False
            if HOME_MAP_AVAILABLE:
                drew = blit_home_item_sprite(surf, item_def, placed, inner)
            if not drew:
                pygame.draw.rect(surf, item_color, (sx + 3, sy + 3, tile_size - 6, tile_size - 6), border_radius=4)
                icon = item_def.get("map_icon", item_id[:1].upper() if item_id else "*")
                icon_surf = self._get_font(max(10, tile_size // 2)).render(str(icon), True, (30, 20, 10))
                surf.blit(icon_surf, (sx + (tile_size - icon_surf.get_width()) // 2, sy + (tile_size - icon_surf.get_height()) // 2))
            short_label = item_id.replace("_", " ")[:10]
            lbl = label_font.render(short_label, True, text_col)
            surf.blit(lbl, (sx + 2, sy + tile_size - 10))

        # Player marker sits at the center tile for the home map.
        px = origin_x + (grid_w * tile_size) // 2
        py = origin_y + (grid_h * tile_size) // 2
        pygame.draw.circle(surf, marker, (px, py), max(5, tile_size // 4))
        pygame.draw.circle(surf, (255, 255, 255), (px, py), max(2, tile_size // 8))

        bonuses = {}
        if player and isinstance(player.state, dict):
            bonuses = player.state.get("active_home_bonuses", {}) or {}

        legend_x = 12
        legend_y = sh - 92
        pygame.draw.rect(surf, (66, 47, 30), (legend_x, legend_y, 280, 76), border_radius=6)
        pygame.draw.rect(surf, (140, 110, 76), (legend_x, legend_y, 280, 76), 1, border_radius=6)
        legend_title = self._get_font(12).render("Active altar bonuses", True, text_col)
        surf.blit(legend_title, (legend_x + 8, legend_y + 6))
        if bonuses:
            yline = legend_y + 24
            for key, value in bonuses.items():
                line = self._get_font(10).render(f"{key}: {value}", True, text_col)
                surf.blit(line, (legend_x + 8, yline))
                yline += 14
        else:
            none_line = self._get_font(10).render("None", True, text_col)
            surf.blit(none_line, (legend_x + 8, legend_y + 28))

        fog = "Reveal ON" if self.reveal_all else "Fog of War"
        if self._stats_label:
            self._stats_label.set_text(
                f"Home tiles: {len(tiles)} | Placed: {len(placed_items)} | Expansions: {len(expansions)} | {fog}"
            )

        self._draw_map_border(surf, sw, sh)

    def _player_in_dungeon(self) -> bool:
        if not self.current_location:
            return False
        if "_floor" in self.current_location and self.current_location.startswith("dungeon_"):
            return True
        if self.game_engine and self.game_engine.current_dungeon_instance:
            di = self.game_engine.current_dungeon_instance
            dungeon_data = getattr(di, "dungeon_data", None)
            if isinstance(dungeon_data, dict):
                for _fnum, fdata in dungeon_data.get("floors", {}).items():
                    if self.current_location in (fdata.get("rooms", {}) if isinstance(fdata, dict) else {}):
                        return True
        return False

    def _current_floor_number(self) -> int:
        if not self.current_location:
            return 1
        for part in self.current_location.split("_"):
            if part.startswith("floor"):
                try:
                    return int(part[5:])
                except ValueError:
                    pass
        m = re.search(r'_f(\d+)_', self.current_location)
        if m:
            return int(m.group(1))
        return 1

    def _get_dungeon_floor_rooms(self, floor_num: int) -> dict:
        if self.game_engine and self.game_engine.current_dungeon_instance:
            di = self.game_engine.current_dungeon_instance
            dungeon_data = getattr(di, "dungeon_data", None)
            if isinstance(dungeon_data, dict):
                floor_data = (dungeon_data.get("floors", {}).get(floor_num, {})
                              or dungeon_data.get("floors", {}).get(str(floor_num), {}))
                rooms = floor_data.get("rooms", {}) if isinstance(floor_data, dict) else {}
                if rooms:
                    return rooms

        result = {}
        floor_tag = f"_floor{floor_num}_"
        for rid, room_obj in self.rooms_data.items():
            if rid.startswith("dungeon_") and floor_tag in rid:
                raw_coords = getattr(room_obj, "coordinates", None)
                if raw_coords is None and isinstance(room_obj, dict):
                    raw_coords = room_obj.get("coordinates", [0, 0])
                raw_exits = getattr(room_obj, "exits", None)
                if raw_exits is None and isinstance(room_obj, dict):
                    raw_exits = room_obj.get("exits", {})
                if not isinstance(raw_exits, dict):
                    raw_exits = {}
                result[rid] = {
                    "name": getattr(room_obj, "name", "???"),
                    "description": getattr(room_obj, "description", ""),
                    "exits": raw_exits,
                    "coordinates": self._normalize_coordinates(raw_coords),
                    "location_type": getattr(room_obj, "location_type", "dungeon"),
                }
        return result

    def _get_dungeon_total_floors(self) -> int:
        if self.game_engine and self.game_engine.current_dungeon_instance:
            di = self.game_engine.current_dungeon_instance
            dungeon_data = getattr(di, "dungeon_data", None)
            if isinstance(dungeon_data, dict):
                try:
                    return int(dungeon_data.get("num_floors", 1))
                except Exception:
                    return 1
        return 1

    @staticmethod
    def _room_tag(room_id, room_data, current_room, visited_rooms) -> str:
        if room_id == current_room:
            return "current"

        name_lower = (room_data.get("name") or "").lower()
        exits = room_data.get("exits", {})

        for direction, edata in exits.items():
            if isinstance(edata, dict) and edata.get("type") in ("time_gated_dungeon", "fixed_dungeon"):
                return "dungeon_entrance"

        for direction, edata in exits.items():
            if direction in ("down", "up"):
                return "stairs"
            if isinstance(edata, dict) and "stairs" in str(edata.get("type", "")):
                return "stairs"

        if "entrance" in name_lower:
            return "entrance"
        if any(kw in name_lower for kw in ("treasure", "vault", "treasury")):
            return "treasure"
        if room_id in visited_rooms:
            return "visited"
        return "unexplored"
