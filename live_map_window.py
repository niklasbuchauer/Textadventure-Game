"""
Live Map Window — Pygame graphical map with drawn shapes.

Automatically switches between overworld and dungeon floor maps based on
the player's current room.  Renders circles/squares/diamonds on a Surface
displayed inside a pygame_gui UIWindow via UIImage.
"""

import re
import math
import pygame
import pygame_gui
from pygame_gui.elements import (
    UIButton, UILabel, UIWindow, UIImage,
)


class LiveMapWindow:
    """Graphical map window using pygame drawing + UIWindow overlay."""

    # ── colour palette ──────────────────────────────────────────────
    COLORS = {
        "bg":                 "#0e0c09",   # dungeon: dark stone
        "ocean":              "#0d1a26",   # deep sea
        "land":               "#1e1a10",   # dark parchment land base
        "grid":               "#1a1a1a",
        "connection":         "#2c2518",   # unvisited trail (barely visible)
        "connection_border":  "#1a1208",   # road shadow undercoat
        "connection_visited": "#7a5c28",   # travelled dirt road
        "connection_vis_hi":  "#a07838",   # road highlight
        "text":               "#d4b896",   # parchment ink
        "text_dim":           "#4a3e2e",   # dim parchment
        # room markers
        "current_fill":       "#f5c842",   # golden
        "current_outline":    "#ff9900",   # amber
        "current_glow":       "#ff6600",   # orange glow ring
        "visited_fill":       "#2a3a1e",
        "visited_outline":    "#5a8a3a",
        "unexplored_fill":    "#1e1a12",
        "unexplored_dot":     "#3a3028",
        "entrance_fill":      "#1a2e3e",
        "entrance_outline":   "#4499cc",
        "stairs_fill":        "#1e1030",
        "stairs_outline":     "#9955cc",
        "treasure_fill":      "#2e2208",
        "treasure_outline":   "#cc9922",
        "dungeon_entrance_fill":    "#2a0e0e",
        "dungeon_entrance_outline": "#cc3322",
        # UI
        "header_fg":          "#c8a050",
        "stats_bg":           "#0e0c09",
        "boat_line":          "#2255aa",
        "boat_line_hi":       "#4488dd",
    }

    # ── region colour themes (fill, accent) ──
    REGION_COLORS = {
        "forest":    ("#182e12", "#4a8a32"),
        "swamp":     ("#141824", "#6633aa"),
        "mountain":  ("#1a1e2a", "#6677aa"),
        "village":   ("#2e2410", "#c8973c"),
        "river":     ("#0e1e2e", "#3378aa"),
        "graveyard": ("#200c0c", "#884433"),
        "ruins":     ("#221808", "#aa7733"),
        "building":  ("#151828", "#556699"),
        "desert":    ("#2e2610", "#cc9933"),
        "tundra":    ("#141e2e", "#6699bb"),
        "coast":     ("#0e2030", "#3399aa"),
        "castle":    ("#201428", "#9966bb"),
        "dock":      ("#101428", "#4466aa"),
        "sunstone":  ("#2a2008", "#ddaa33"),
        "emerald":   ("#0c2e10", "#33bb44"),
        "stormbreak":("#101428", "#5566cc"),
        "cinderforge":("#2a1008", "#cc5522"),
        "dreadmist": ("#1e0818", "#884488"),
        "wyrmscale": ("#2a1c08", "#bb7722"),
        "abyssal":   ("#100828", "#6633bb"),
        "default":   ("#182410", "#4a7a34"),
    }

    ROOM_RADIUS = 14
    MIN_SPACING = 80
    ZOOM_MIN = 0.4
    ZOOM_MAX = 2.5
    ZOOM_STEP = 0.15

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

        self._zoom = 1.0
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
        self._hex_pts_cache: dict = {}      # radius → list of (dx,dy) offsets for dungeon hexagon

        # Pre-compute RGB colour tuples once so _c() / _hex_to_rgb() are O(1)
        self._rgb_colors = {k: self._hex_to_rgb(v) for k, v in self.COLORS.items()}
        self._rgb_region = {k: (self._hex_to_rgb(v[0]), self._hex_to_rgb(v[1]))
                            for k, v in self.REGION_COLORS.items()}

        # fonts (initialised lazily)
        self._font_label = None
        self._font_icon = None
        self._font_legend = None
        self._font_header = None

    def _init_fonts(self):
        if self._font_label is not None:
            return
        self._font_label = pygame.font.SysFont("consolas", 9)
        self._font_icon  = pygame.font.SysFont("consolas", 14)
        self._font_legend = pygame.font.SysFont("consolas", 8)
        self._font_header = pygame.font.SysFont("consolas", 12)

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
        screen.blit(self._map_surface, rect.topleft)

    def tick(self):
        """Called once per game-frame to perform any deferred redraw."""
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

        # Mouse wheel zoom over map area
        if event.type == pygame.MOUSEWHEEL:
            if self._is_mouse_over_map():
                if event.y > 0:
                    self._zoom_in()
                elif event.y < 0:
                    self._zoom_out()
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
                self._drag_start = None
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

    # ── zoom / pan controls ─────────────────────────────────────────
    def _zoom_in(self):
        self._zoom = min(self.ZOOM_MAX, self._zoom + self.ZOOM_STEP)
        self._update_zoom_label()
        self._needs_redraw = True
        self.redraw_map()

    def _zoom_out(self):
        self._zoom = max(self.ZOOM_MIN, self._zoom - self.ZOOM_STEP)
        self._update_zoom_label()
        self._needs_redraw = True
        self.redraw_map()

    def _reset_view(self):
        self._zoom = 1.0
        self._pan_x = 0.0
        self._pan_y = 0.0
        self._update_zoom_label()
        self._needs_redraw = True
        self.redraw_map()

    def _update_zoom_label(self):
        if self._zoom_label:
            self._zoom_label.set_text(f"{int(self._zoom * 100)}%")

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

        cx = sw / 2 + self._pan_x
        cy = (sh - 60) / 2 + self._pan_y
        mid_x = (min_x + max_x) / 2
        mid_y = (min_y + max_y) / 2

        positions = {}
        for (gx, gy), rid in coord_map.items():
            px = cx + (gx - mid_x) * spacing
            py = cy - (gy - mid_y) * spacing
            positions[rid] = (px, py)

        return positions, spacing

    # ── drawing helpers ─────────────────────────────────────────────
    @staticmethod
    def _hex_to_rgb(hex_color):
        h = hex_color.lstrip("#")
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

    def _c(self, key):
        """Return cached RGB tuple for named colour."""
        return self._rgb_colors[key]

    def _get_font(self, size: int) -> pygame.font.Font:
        """Return a cached SysFont at *size* — avoids repeated filesystem scans."""
        f = self._font_cache.get(size)
        if f is None:
            f = pygame.font.SysFont("consolas", size)
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

    def _draw_land_mass(self, surf, positions):
        """Paint a subtle parchment-land ellipse behind all known room positions.
        Draws directly onto surf (pygame clips to surface bounds automatically),
        so no intermediate surface is needed regardless of zoom level."""
        if not positions:
            return
        xs = [p[0] for p in positions.values()]
        ys = [p[1] for p in positions.values()]
        if not xs:
            return
        sw, sh = surf.get_size()
        cx = (min(xs) + max(xs)) / 2
        cy = (min(ys) + max(ys)) / 2
        # Cap radii to surface size — at high zoom rooms extend far off-screen,
        # but we only need to fill the visible area.
        rw = max(80, min((max(xs) - min(xs)) / 2 + 100, sw * 0.85))
        rh = max(80, min((max(ys) - min(ys)) / 2 + 100, sh * 0.85))

        land_col = self._rgb_colors["land"]
        steps = 5
        icx, icy = int(cx), int(cy)
        for i in range(steps, 0, -1):
            frac = i / steps
            ew = max(2, int(rw * 2 * frac))
            eh = max(2, int(rh * 2 * frac))
            brightness = int(frac * 30)
            col = tuple(min(255, land_col[v] + brightness) for v in range(3))
            pygame.draw.ellipse(surf, col, (icx - ew // 2, icy - eh // 2, ew, eh))

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

    def _draw_connections(self, surf, positions, rooms, visited, sw, sh):
        drawn = set()
        boat_routes = []
        unvisited_routes = []
        visited_routes = []
        margin = 60

        for rid, rdata in rooms.items():
            if rid not in positions:
                continue
            x1, y1 = positions[rid]
            exits = rdata.get("exits", {})
            if not hasattr(exits, 'items'):
                continue

            for _dir, target in exits.items():
                target_id = target.get("target", "") if isinstance(target, dict) else target
                if target_id not in positions:
                    continue
                pair = tuple(sorted([rid, target_id]))
                if pair in drawn:
                    continue
                drawn.add(pair)

                x2, y2 = positions[target_id]
                # Viewport culling
                if (max(x1, x2) < -margin or min(x1, x2) > sw + margin or
                        max(y1, y2) < -margin or min(y1, y2) > sh + margin):
                    continue

                if isinstance(target, dict) and target.get("type") == "boat_travel":
                    boat_routes.append((x1, y1, x2, y2))
                    continue

                both = rid in visited and target_id in visited
                if both:
                    visited_routes.append((x1, y1, x2, y2))
                else:
                    unvisited_routes.append((x1, y1, x2, y2))

        # Unvisited: single faint trail
        trail_col = self._rgb_colors["connection"]
        for x1, y1, x2, y2 in unvisited_routes:
            pygame.draw.line(surf, trail_col,
                             (int(x1), int(y1)), (int(x2), int(y2)), 1)

        # Visited: double-pass dirt road (dark border then warm road colour)
        road_border = self._rgb_colors["connection_border"]
        road_col    = self._rgb_colors["connection_visited"]
        road_hi     = self._rgb_colors["connection_vis_hi"]
        for x1, y1, x2, y2 in visited_routes:
            pygame.draw.line(surf, road_border,
                             (int(x1), int(y1)), (int(x2), int(y2)), 5)
            pygame.draw.line(surf, road_col,
                             (int(x1), int(y1)), (int(x2), int(y2)), 3)

        # Boat sea-routes: dashed blue
        boat_col = self._rgb_colors["boat_line"]
        boat_hi  = self._rgb_colors["boat_line_hi"]
        for x1, y1, x2, y2 in boat_routes:
            self._draw_dashed_line(surf, boat_col,
                                   (int(x1), int(y1)), (int(x2), int(y2)),
                                   dash=10, gap=5, width=3)
            self._draw_dashed_line(surf, boat_hi,
                                   (int(x1), int(y1)), (int(x2), int(y2)),
                                   dash=10, gap=5, width=1)

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
        """Draw a cartographic-style terrain marker instead of uniform node circles."""
        loc_type = (room_data.get("location_type") or "wilderness").lower() if room_data else ""

        if tag == "current":
            # Glowing golden compass-rose style: outer glow, main circle, inner dot
            glow = self._c("current_glow")
            for glow_r in (r + 9, r + 6):
                pygame.draw.circle(surf, glow, (ipx, ipy), glow_r, 1)
            pygame.draw.circle(surf, fill, (ipx, ipy), r)
            pygame.draw.circle(surf, outline, (ipx, ipy), r, 2)
            # Cross-hair lines inside
            hl = r - 4
            pygame.draw.line(surf, outline, (ipx - hl, ipy), (ipx + hl, ipy), 1)
            pygame.draw.line(surf, outline, (ipx, ipy - hl), (ipx, ipy + hl), 1)
            return

        if tag == "dungeon_entrance":
            # Dark hexagon with red accent — cache offset points by radius
            offsets = self._hex_pts_cache.get(r)
            if offsets is None:
                offsets = [(int(r * math.cos(math.radians(a * 60 - 30))),
                            int(r * math.sin(math.radians(a * 60 - 30))))
                           for a in range(6)]
                self._hex_pts_cache[r] = offsets
            pts = [(ipx + dx, ipy + dy) for dx, dy in offsets]
            pygame.draw.polygon(surf, fill, pts)
            pygame.draw.polygon(surf, outline, pts, 2)
            return

        if loc_type in ("settlement",):
            # Settlement: filled square rotated 45° (diamond)
            pts = [(ipx, ipy - r), (ipx + r, ipy), (ipx, ipy + r), (ipx - r, ipy)]
            pygame.draw.polygon(surf, fill, pts)
            pygame.draw.polygon(surf, outline, pts, 2)
            return

        if loc_type == "building":
            # Building: small upright square
            hw = max(6, r - 2)
            rect = pygame.Rect(ipx - hw, ipy - hw, hw * 2, hw * 2)
            pygame.draw.rect(surf, fill, rect, border_radius=1)
            pygame.draw.rect(surf, outline, rect, 2, border_radius=1)
            return

        # Default: flat circle with no thick node outline — just a terrain patch
        pygame.draw.circle(surf, fill, (ipx, ipy), r)
        if tag != "unexplored":
            pygame.draw.circle(surf, outline, (ipx, ipy), r, 1)

    def _draw_rooms(self, surf, positions, rooms, visited, sw, sh):
        r = int(self.ROOM_RADIUS * self._zoom)
        r = max(6, min(r, 32))
        margin = r + 40

        show_labels = self._zoom >= 0.65
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
                # Fog-of-war: tiny dark smudge, no label
                dot_col = self._c("unexplored_dot")
                pygame.draw.circle(surf, dot_col, (ipx, ipy), small_dot_r)
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

            # Name label below marker — solid dark backing rect (no SRCALPHA per room)
            if show_labels:
                name = (rdata.get("name", "???") if isinstance(rdata, dict)
                        else (getattr(rdata, "name", None) or "???"))
                if len(name) > max_chars:
                    name = name[:max_chars - 2] + ".."
                lbl = self._render_text(name, label_color, font_size)
                lx = ipx - lbl.get_width() // 2
                ly = ipy + label_offset
                pad = 2
                box = pygame.Rect(lx - pad, ly - 1, lbl.get_width() + pad * 2, lbl.get_height())
                pygame.draw.rect(surf, (8, 6, 4), box)  # solid near-black backing
                surf.blit(lbl, (lx, ly))

    def _draw_legend(self, surf, sh):
        sw = surf.get_width()
        y = sh - 25

        mainland_items = [
            ("\u2605 You",     self._c("current_fill"),  self._c("current_outline"),         "circle"),
            ("\u2620 Dungeon", self._c("dungeon_entrance_fill"), self._c("dungeon_entrance_outline"), "hex"),
            ("Forest",   *self._rgb_region["forest"],    "circle"),
            ("Village",  *self._rgb_region["village"],   "diamond"),
            ("Mountain", *self._rgb_region["mountain"],  "circle"),
            ("Swamp",    *self._rgb_region["swamp"],     "circle"),
            ("Desert",   *self._rgb_region["desert"],    "circle"),
            ("Tundra",   *self._rgb_region["tundra"],    "circle"),
            ("Coast",    *self._rgb_region["coast"],     "circle"),
            ("Castle",   *self._rgb_region["castle"],    "diamond"),
            ("Dock",     *self._rgb_region["dock"],      "square"),
        ]
        island_items = [
            ("Sunstone",  *self._rgb_region["sunstone"],    "circle"),
            ("Emerald",   *self._rgb_region["emerald"],     "circle"),
            ("Storm",     *self._rgb_region["stormbreak"],  "circle"),
            ("Cinder",    *self._rgb_region["cinderforge"], "circle"),
            ("Dread",     *self._rgb_region["dreadmist"],   "circle"),
            ("Wyrm",      *self._rgb_region["wyrmscale"],   "circle"),
            ("Abyssal",   *self._rgb_region["abyssal"],     "circle"),
            ("\u2693 Sea", self._rgb_colors["connection_border"], self._rgb_colors["boat_line_hi"], "circle"),
        ]

        # Separator line
        pygame.draw.line(surf, self._rgb_colors["connection_border"],
                         (20, y - 38), (sw - 20, y - 38), 1)

        y1 = y - 20
        total_w1 = len(mainland_items) * 80
        sx1 = (sw - total_w1) / 2
        for i, (label, fill, outline, shape) in enumerate(mainland_items):
            x = int(sx1 + i * 80)
            self._draw_legend_item(surf, x, y1, label, fill, outline, shape)

        y2 = y + 2
        total_w2 = len(island_items) * 80
        sx2 = (sw - total_w2) / 2
        for i, (label, fill, outline, shape) in enumerate(island_items):
            x = int(sx2 + i * 80)
            self._draw_legend_item(surf, x, y2, label, fill, outline, shape)

    def _draw_legend_item(self, surf, x, y, label, fill, outline, shape):
        if shape == "square":
            pygame.draw.rect(surf, fill, (x, y - 5, 11, 11))
            pygame.draw.rect(surf, outline, (x, y - 5, 11, 11), 1)
        elif shape == "diamond":
            pts = [(x+6, y-6), (x+12, y), (x+6, y+6), (x, y)]
            pygame.draw.polygon(surf, fill, pts)
            pygame.draw.polygon(surf, outline, pts, 1)
        elif shape == "hex":
            pts = [(x + 6 + int(6*math.cos(math.radians(a*60-30))),
                    y     + int(6*math.sin(math.radians(a*60-30)))) for a in range(6)]
            pygame.draw.polygon(surf, fill, pts)
            pygame.draw.polygon(surf, outline, pts, 1)
        else:
            pygame.draw.circle(surf, fill, (x + 6, y), 6)
            pygame.draw.circle(surf, outline, (x + 6, y), 6, 1)
        txt = self._font_legend.render(label, True, self._rgb_colors["text"])
        surf.blit(txt, (x + 18, y - txt.get_height() // 2))

    # ── dungeon renderer ────────────────────────────────────────────
    def _render_dungeon_map(self):
        surf = self._map_surface
        sw, sh = surf.get_size()
        surf.fill(self._rgb_colors["bg"])

        floor_num = self._current_floor_number()
        total_floors = self._get_dungeon_total_floors()
        rooms = self._get_dungeon_floor_rooms(floor_num)

        visited = set(self.visited_rooms) if not self.reveal_all else set(rooms.keys())

        if self._header_label:
            self._header_label.set_text(
                f"\u2694 DUNGEON MAP \u2014 FLOOR {floor_num} / {total_floors} \u2694"
            )

        if not rooms:
            txt = self._font_header.render("No dungeon rooms on this floor.", True,
                                           self._hex_to_rgb(self.COLORS["text_dim"]))
            surf.blit(txt, (sw//2 - txt.get_width()//2, sh//2 - txt.get_height()//2))
            return

        coord_map = {}
        for rid, rdata in rooms.items():
            c = rdata.get("coordinates", [0, 0])
            coord_map[(c[0], c[1])] = rid

        positions, spacing = self._compute_layout(coord_map, sw, sh)

        self._draw_land_mass(surf, positions)
        self._draw_grid(surf, positions, spacing)
        self._draw_connections(surf, positions, rooms, visited, sw, sh)
        self._draw_rooms(surf, positions, rooms, visited, sw, sh)
        self._draw_legend(surf, sh)

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
            rooms[rid] = {
                "name": getattr(room_obj, "name", None)
                        or (room_obj.get("name", "???") if isinstance(room_obj, dict) else "???"),
                "coordinates": getattr(room_obj, "coordinates", None)
                               or (room_obj.get("coordinates", [0, 0]) if isinstance(room_obj, dict) else [0, 0]),
                "location_type": getattr(room_obj, "location_type", None)
                                 or (room_obj.get("location_type", "wilderness") if isinstance(room_obj, dict) else "wilderness"),
                "exits": getattr(room_obj, "exits", None)
                         or (room_obj.get("exits", {}) if isinstance(room_obj, dict) else {}),
            }
        self._cached_overworld_rooms = rooms
        self._cached_room_count = cur_count
        return rooms

    def _render_overworld_map(self):
        surf = self._map_surface
        sw, sh = surf.get_size()
        surf.fill(self._rgb_colors["ocean"])

        rooms = self._build_overworld_rooms()
        visited = set(self.visited_rooms) if not self.reveal_all else set(rooms.keys())

        if self._header_label:
            self._header_label.set_text("\U0001f5fa OVERWORLD MAP \U0001f5fa")

        if not rooms:
            txt = self._font_header.render("No rooms found.", True,
                                           self._hex_to_rgb(self.COLORS["text_dim"]))
            surf.blit(txt, (sw//2 - txt.get_width()//2, sh//2 - txt.get_height()//2))
            return

        coord_map = {}
        for rid, rdata in rooms.items():
            c = rdata["coordinates"]
            coord_map[(c[0], c[1])] = rid

        positions, spacing = self._compute_layout(coord_map, sw, sh)

        self._draw_land_mass(surf, positions)
        self._draw_grid(surf, positions, spacing)
        self._draw_connections(surf, positions, rooms, visited, sw, sh)
        self._draw_rooms(surf, positions, rooms, visited, sw, sh)
        self._draw_legend(surf, sh)

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
    def _player_in_dungeon(self) -> bool:
        if not self.current_location:
            return False
        if "_floor" in self.current_location and self.current_location.startswith("dungeon_"):
            return True
        if self.game_engine and self.game_engine.current_dungeon_instance:
            di = self.game_engine.current_dungeon_instance
            if di.dungeon_data:
                for _fnum, fdata in di.dungeon_data.get("floors", {}).items():
                    if self.current_location in fdata.get("rooms", {}):
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
            if di.dungeon_data:
                floor_data = (di.dungeon_data.get("floors", {}).get(floor_num, {})
                              or di.dungeon_data.get("floors", {}).get(str(floor_num), {}))
                rooms = floor_data.get("rooms", {})
                if rooms:
                    return rooms

        result = {}
        floor_tag = f"_floor{floor_num}_"
        for rid, room_obj in self.rooms_data.items():
            if rid.startswith("dungeon_") and floor_tag in rid:
                result[rid] = {
                    "name": getattr(room_obj, "name", "???"),
                    "description": getattr(room_obj, "description", ""),
                    "exits": getattr(room_obj, "exits", {}),
                    "coordinates": getattr(room_obj, "coordinates", [0, 0]),
                    "location_type": getattr(room_obj, "location_type", "dungeon"),
                }
        return result

    def _get_dungeon_total_floors(self) -> int:
        if self.game_engine and self.game_engine.current_dungeon_instance:
            di = self.game_engine.current_dungeon_instance
            if di.dungeon_data:
                return di.dungeon_data.get("num_floors", 1)
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
