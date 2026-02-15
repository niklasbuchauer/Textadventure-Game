"""
Live Map Window — Graphical Canvas-based map with drawn circles.

Automatically switches between overworld and dungeon floor maps based on
the player's current room.  Dungeon rooms are detected by their ID prefix
(dungeon_{seed}_floor{N}_room{M}) or fixed dungeon pattern ({prefix}_f{N}_{name}).
"""

import tkinter as tk


class LiveMapWindow:
    """Graphical map window using Canvas with circles, connections, and fog-of-war."""

    # ── colour palette ──────────────────────────────────────────────
    COLORS = {
        "bg":                 "#0a0a0a",
        "grid":               "#1a1a1a",
        "connection":         "#444444",
        "connection_visited": "#007700",
        "text":               "#cccccc",
        "text_dim":           "#555555",
        # room fills / outlines
        "current_fill":       "#ffff00",
        "current_outline":    "#ffaa00",
        "visited_fill":       "#003300",
        "visited_outline":    "#00ff00",
        "unexplored_fill":    "#1a1a1a",
        "unexplored_outline": "#555555",
        "entrance_fill":      "#003355",
        "entrance_outline":   "#00ffff",
        "stairs_fill":        "#330033",
        "stairs_outline":     "#ff00ff",
        "treasure_fill":      "#332200",
        "treasure_outline":   "#ffd700",
        "dungeon_entrance_fill":    "#331111",
        "dungeon_entrance_outline":  "#ff4444",
        # UI chrome
        "header_fg":          "#00ccff",
        "stats_bg":           "#111111",
        "zoom_btn_bg":        "#222222",
        "zoom_btn_fg":        "#cccccc",
    }

    # ── region colour themes (fill, outline) for visited rooms ──────
    REGION_COLORS = {
        "forest":    ("#0a2e0a", "#22aa22"),   # green
        "swamp":     ("#1a0a2e", "#9944cc"),   # purple
        "mountain":  ("#1a1a2e", "#8888cc"),   # slate blue
        "village":   ("#2e2210", "#ccaa55"),   # tan/gold
        "river":     ("#0a1a2e", "#4488cc"),   # blue
        "graveyard": ("#2e0a0a", "#aa4444"),   # dark red
        "ruins":     ("#2e1a0a", "#cc8844"),   # amber
        "building":  ("#1a1a2e", "#6688bb"),   # muted blue
        "default":   ("#003300", "#00ff00"),   # original green
    }

    ROOM_RADIUS = 24
    MIN_SPACING = 90   # minimum pixels between room centres
    ZOOM_MIN = 0.4
    ZOOM_MAX = 2.5
    ZOOM_STEP = 0.15

    # ── construction ────────────────────────────────────────────────
    def __init__(self, parent, rooms_data, game_engine=None):
        """
        Args:
            parent:      root tkinter widget (used as Toplevel parent)
            rooms_data:  dict  room_id -> Room object  (engine.rooms)
            game_engine: GameEngine instance (for dungeon data access)
        """
        self.parent = parent
        self.rooms_data = rooms_data          # live reference to engine.rooms
        self.game_engine = game_engine
        self.window = None
        self.canvas = None
        self.map_display = None               # alias kept for compatibility
        self.header_var = None
        self.stats_var = None
        self.current_location = None
        self.visited_rooms: set = set()
        self.reveal_all = False
        self._resize_after_id = None          # debounce handle
        self._zoom = 1.0                      # zoom level
        self._pan_x = 0.0                     # pan offset in pixels
        self._pan_y = 0.0
        self._drag_start = None               # for click-drag panning

    # ── window lifecycle ────────────────────────────────────────────
    def create_window(self, x_offset=200, y_offset=100):
        """Create / raise the map Toplevel."""
        if self.window and self.window.winfo_exists():
            self.window.lift()
            return

        self.window = tk.Toplevel(self.parent)
        self.window.title("Live Map")
        self.window.geometry("900x700")
        self.window.configure(bg=self.COLORS["bg"])
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)

        # ── header label ────────────────────────────────────────────
        self.header_var = tk.StringVar(value="MAP")
        header = tk.Label(
            self.window,
            textvariable=self.header_var,
            font=("Consolas", 14, "bold"),
            fg=self.COLORS["header_fg"],
            bg=self.COLORS["bg"],
            anchor="center",
        )
        header.pack(fill=tk.X, padx=5, pady=(5, 2))

        # ── toolbar frame (zoom controls) ──────────────────────────
        toolbar = tk.Frame(self.window, bg=self.COLORS["bg"])
        toolbar.pack(fill=tk.X, padx=5, pady=(0, 2))

        btn_opts = dict(
            font=("Consolas", 12, "bold"),
            fg=self.COLORS["zoom_btn_fg"],
            bg=self.COLORS["zoom_btn_bg"],
            activebackground="#333333",
            activeforeground="#ffffff",
            bd=0, padx=8, pady=1,
            cursor="hand2",
        )
        tk.Button(toolbar, text="\u2212", command=self._zoom_out, **btn_opts).pack(side=tk.LEFT, padx=(0, 2))
        self._zoom_label = tk.Label(toolbar, text="100%", font=("Consolas", 10),
                                    fg=self.COLORS["text"], bg=self.COLORS["bg"], width=5)
        self._zoom_label.pack(side=tk.LEFT)
        tk.Button(toolbar, text="+", command=self._zoom_in, **btn_opts).pack(side=tk.LEFT, padx=(2, 8))
        tk.Button(toolbar, text="\u2302", command=self._reset_view, **btn_opts).pack(side=tk.LEFT, padx=(0, 2))

        # right-side: region indicator
        self._region_label = tk.Label(toolbar, text="", font=("Consolas", 9),
                                      fg=self.COLORS["text_dim"], bg=self.COLORS["bg"])
        self._region_label.pack(side=tk.RIGHT, padx=5)

        # ── canvas ──────────────────────────────────────────────────
        self.canvas = tk.Canvas(
            self.window,
            bg=self.COLORS["bg"],
            highlightthickness=0,
            cursor="arrow",
        )
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=2)
        self.map_display = self.canvas          # alias for API compat

        # ── stats bar ───────────────────────────────────────────────
        self.stats_var = tk.StringVar(value="")
        stats = tk.Label(
            self.window,
            textvariable=self.stats_var,
            font=("Consolas", 10),
            fg=self.COLORS["text"],
            bg=self.COLORS["stats_bg"],
            anchor="w",
        )
        stats.pack(fill=tk.X, padx=5, pady=(2, 5))

        # redraw on resize (debounced)
        self.canvas.bind("<Configure>", self._on_resize)

        # zoom with mouse wheel
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)

        # pan with click-drag
        self.canvas.bind("<ButtonPress-1>", self._on_drag_start)
        self.canvas.bind("<B1-Motion>", self._on_drag_move)
        self.canvas.bind("<ButtonRelease-1>", self._on_drag_end)

        self.redraw_map()

    def close_window(self):
        """Destroy the window and clean up references."""
        if self.window and self.window.winfo_exists():
            self.window.destroy()
        self.window = None
        self.canvas = None
        self.map_display = None

    def is_open(self):
        return self.window is not None and self.window.winfo_exists()

    # ── public API ──────────────────────────────────────────────────
    def update_location(self, current_room_id, visited_rooms):
        """Called by engine when the player moves."""
        self.current_location = current_room_id
        self.visited_rooms = set(visited_rooms)
        if self.is_open():
            self.redraw_map()

    def toggle_reveal(self):
        """Toggle debug reveal (show all rooms ignoring fog)."""
        self.reveal_all = not self.reveal_all
        if self.is_open():
            self.redraw_map()
        return self.reveal_all

    # ── zoom / pan controls ─────────────────────────────────────────
    def _zoom_in(self):
        self._zoom = min(self.ZOOM_MAX, self._zoom + self.ZOOM_STEP)
        self._update_zoom_label()
        self.redraw_map()

    def _zoom_out(self):
        self._zoom = max(self.ZOOM_MIN, self._zoom - self.ZOOM_STEP)
        self._update_zoom_label()
        self.redraw_map()

    def _reset_view(self):
        self._zoom = 1.0
        self._pan_x = 0.0
        self._pan_y = 0.0
        self._update_zoom_label()
        self.redraw_map()

    def _update_zoom_label(self):
        if hasattr(self, '_zoom_label') and self._zoom_label:
            self._zoom_label.config(text=f"{int(self._zoom * 100)}%")

    def _on_mousewheel(self, event):
        if event.delta > 0:
            self._zoom_in()
        else:
            self._zoom_out()

    def _on_drag_start(self, event):
        self._drag_start = (event.x, event.y)
        self.canvas.config(cursor="fleur")

    def _on_drag_move(self, event):
        if self._drag_start:
            dx = event.x - self._drag_start[0]
            dy = event.y - self._drag_start[1]
            self._pan_x += dx
            self._pan_y += dy
            self._drag_start = (event.x, event.y)
            self.redraw_map()

    def _on_drag_end(self, _event=None):
        self._drag_start = None
        if self.canvas:
            self.canvas.config(cursor="arrow")

    # ── rendering entry-point ───────────────────────────────────────
    def redraw_map(self):
        """Decide which map to render and paint it."""
        if not self.canvas:
            return

        self.canvas.delete("all")

        if self._player_in_dungeon():
            self._render_dungeon_map()
        else:
            self._render_overworld_map()

    # ── internal resize handler (debounced) ─────────────────────────
    def _on_resize(self, _event=None):
        if self._resize_after_id:
            self.canvas.after_cancel(self._resize_after_id)
        self._resize_after_id = self.canvas.after(80, self.redraw_map)

    # ── coordinate layout ──────────────────────────────────────────
    def _compute_layout(self, coord_map, canvas_w, canvas_h, margin=70):
        """
        Map room grid-coords to pixel positions centred on the canvas.
        Applies zoom and pan offsets.

        Returns ({room_id: (px, py)}, spacing).
        """
        if not coord_map:
            return {}, 0

        xs = [p[0] for p in coord_map]
        ys = [p[1] for p in coord_map]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        range_x = max_x - min_x
        range_y = max_y - min_y

        usable_w = canvas_w - 2 * margin
        usable_h = canvas_h - 2 * margin - 80       # reserve space for legend

        spacing_x = (usable_w / range_x) if range_x > 0 else 200
        spacing_y = (usable_h / range_y) if range_y > 0 else 200

        base_spacing = max(self.MIN_SPACING, min(spacing_x, spacing_y, 200))
        spacing = base_spacing * self._zoom

        cx = canvas_w / 2 + self._pan_x
        cy = (canvas_h - 80) / 2 + self._pan_y
        mid_x = (min_x + max_x) / 2
        mid_y = (min_y + max_y) / 2

        positions = {}
        for (gx, gy), rid in coord_map.items():
            px = cx + (gx - mid_x) * spacing
            py = cy - (gy - mid_y) * spacing         # canvas-y is flipped
            positions[rid] = (px, py)

        return positions, spacing

    # ── drawing helpers ─────────────────────────────────────────────
    def _draw_grid(self, positions, spacing):
        """Draw faint dashed grid lines through room positions."""
        if not positions or spacing <= 0:
            return

        pxs = [p[0] for p in positions.values()]
        pys = [p[1] for p in positions.values()]
        pad = spacing * 0.6

        x_vals = sorted(set(round(p[0]) for p in positions.values()))
        y_vals = sorted(set(round(p[1]) for p in positions.values()))

        y_lo, y_hi = min(pys) - pad, max(pys) + pad
        x_lo, x_hi = min(pxs) - pad, max(pxs) + pad

        for x in x_vals:
            self.canvas.create_line(x, y_lo, x, y_hi,
                                    fill=self.COLORS["grid"], width=1, dash=(2, 6))
        for y in y_vals:
            self.canvas.create_line(x_lo, y, x_hi, y,
                                    fill=self.COLORS["grid"], width=1, dash=(2, 6))

    def _draw_connections(self, positions, rooms, visited):
        """Draw lines between rooms that share an exit."""
        drawn: set = set()
        for rid, rdata in rooms.items():
            if rid not in positions:
                continue
            # at least one end must be visible
            if rid not in visited and not self.reveal_all:
                continue

            x1, y1 = positions[rid]
            for _dir, target in rdata.get("exits", {}).items():
                target_id = target.get("target", "") if isinstance(target, dict) else target
                if target_id not in positions:
                    continue
                pair = tuple(sorted([rid, target_id]))
                if pair in drawn:
                    continue
                drawn.add(pair)

                x2, y2 = positions[target_id]
                both = rid in visited and target_id in visited
                color = self.COLORS["connection_visited"] if both else self.COLORS["connection"]
                width = 2 if both else 1
                self.canvas.create_line(x1, y1, x2, y2, fill=color, width=width)

    def _get_room_style(self, tag, room_id=""):
        """Return (fill, outline, label_color) for a room-type tag."""
        styles = {
            "current":    (self.COLORS["current_fill"],     self.COLORS["current_outline"],    "#000000"),
            "visited":    (self.COLORS["visited_fill"],      self.COLORS["visited_outline"],    self.COLORS["visited_outline"]),
            "unexplored": (self.COLORS["unexplored_fill"],   self.COLORS["unexplored_outline"], self.COLORS["text_dim"]),
            "entrance":   (self.COLORS["entrance_fill"],     self.COLORS["entrance_outline"],   self.COLORS["entrance_outline"]),
            "stairs":     (self.COLORS["stairs_fill"],       self.COLORS["stairs_outline"],     self.COLORS["stairs_outline"]),
            "treasure":   (self.COLORS["treasure_fill"],     self.COLORS["treasure_outline"],   self.COLORS["treasure_outline"]),
            "dungeon_entrance": (self.COLORS["dungeon_entrance_fill"], self.COLORS["dungeon_entrance_outline"], self.COLORS["dungeon_entrance_outline"]),
        }

        # For visited rooms, apply region-based coloring
        if tag == "visited" and room_id:
            region = self._detect_region(room_id)
            if region in self.REGION_COLORS:
                fill, outline = self.REGION_COLORS[region]
                return (fill, outline, outline)

        return styles.get(tag, styles["unexplored"])

    @staticmethod
    def _detect_region(room_id):
        """Determine which region a room belongs to based on its ID."""
        rid = room_id.lower()
        if any(kw in rid for kw in ("forest", "grove", "clearing", "mossy", "woodland",
                                     "hermit", "deep_forest", "ancient_grove")):
            return "forest"
        if any(kw in rid for kw in ("swamp", "witch", "marsh", "foggy")):
            return "swamp"
        if any(kw in rid for kw in ("mountain", "highland", "peak", "foothills")):
            return "mountain"
        if any(kw in rid for kw in ("village", "tavern", "shop", "blacksmith",
                                     "chapel", "farmland")):
            return "village"
        if any(kw in rid for kw in ("river", "bank", "beach", "dock", "lake",
                                     "tidal", "fishing", "old_dock")):
            return "river"
        if any(kw in rid for kw in ("grave", "crypt", "battlefield")):
            return "graveyard"
        if any(kw in rid for kw in ("ruins", "library", "watchtower", "crossroads",
                                     "sunken")):
            return "ruins"
        return "default"

    @staticmethod
    def _room_shape(room_data):
        """Determine shape type based on location_type: 'circle', 'square', 'diamond'."""
        loc_type = (room_data.get("location_type") or "wilderness").lower()
        if loc_type == "building":
            return "square"
        if loc_type == "settlement":
            return "diamond"
        return "circle"

    def _draw_rooms(self, positions, rooms, visited):
        """Draw shaped rooms with region colouring and labels."""
        r = int(self.ROOM_RADIUS * self._zoom)
        r = max(8, min(r, 40))  # clamp radius

        for rid, (px, py) in positions.items():
            rdata = rooms.get(rid, {})
            is_visible = rid in visited or self.reveal_all

            tag = self._room_tag(rid, rdata, self.current_location, visited) if is_visible else "unexplored"
            fill, outline, label_color = self._get_room_style(tag, rid)
            shape = self._room_shape(rdata) if is_visible else "circle"

            # glow ring for current room
            if tag == "current":
                self.canvas.create_oval(
                    px - r - 7, py - r - 7, px + r + 7, py + r + 7,
                    outline=self.COLORS["current_outline"], width=2, dash=(3, 3),
                )

            # draw room shape
            if shape == "square":
                self.canvas.create_rectangle(
                    px - r, py - r, px + r, py + r,
                    fill=fill, outline=outline, width=2,
                )
            elif shape == "diamond":
                self.canvas.create_polygon(
                    px, py - r,       # top
                    px + r, py,       # right
                    px, py + r,       # bottom
                    px - r, py,       # left
                    fill=fill, outline=outline, width=2,
                )
            else:  # circle
                self.canvas.create_oval(
                    px - r, py - r, px + r, py + r,
                    fill=fill, outline=outline, width=2,
                )

            # icon / marker inside the shape
            icon_size = max(8, int(14 * self._zoom))
            if tag == "current":
                self.canvas.create_text(px, py, text="\u2605",
                                        fill="#000000", font=("Consolas", icon_size, "bold"))
            elif tag == "dungeon_entrance" and is_visible:
                self.canvas.create_text(px, py, text="\u2620",
                                        fill=self.COLORS["dungeon_entrance_outline"],
                                        font=("Consolas", icon_size, "bold"))
            elif tag == "stairs" and is_visible:
                self.canvas.create_text(px, py, text="\u2193",
                                        fill=self.COLORS["stairs_outline"],
                                        font=("Consolas", icon_size, "bold"))
            elif not is_visible:
                self.canvas.create_text(px, py, text="?",
                                        fill=self.COLORS["text_dim"],
                                        font=("Consolas", icon_size, "bold"))

            # name label below shape
            if is_visible and self._zoom >= 0.6:
                name = rdata.get("name", "???")
                max_chars = max(6, int(16 * self._zoom))
                if len(name) > max_chars:
                    name = name[:max_chars - 2] + ".."
                font_size = max(7, int(9 * self._zoom))
                self.canvas.create_text(px, py + r + int(14 * self._zoom), text=name,
                                        fill=label_color, font=("Consolas", font_size),
                                        anchor="center")

    def _draw_legend(self, canvas_h):
        """Draw colour legend along the bottom of the canvas."""
        canvas_w = self.canvas.winfo_width()
        y = canvas_h - 25

        items = [
            ("\u2605 You",  self.COLORS["current_fill"],    self.COLORS["current_outline"],  "circle"),
            ("\u2620 Dungeon", self.COLORS["dungeon_entrance_fill"], self.COLORS["dungeon_entrance_outline"], "circle"),
            ("Forest",  self.REGION_COLORS["forest"][0],  self.REGION_COLORS["forest"][1],   "circle"),
            ("Village", self.REGION_COLORS["village"][0], self.REGION_COLORS["village"][1],  "diamond"),
            ("Mountain", self.REGION_COLORS["mountain"][0], self.REGION_COLORS["mountain"][1], "circle"),
            ("Swamp",   self.REGION_COLORS["swamp"][0],   self.REGION_COLORS["swamp"][1],    "circle"),
            ("Building", self.REGION_COLORS["building"][0], self.REGION_COLORS["building"][1], "square"),
            ("Unknown", self.COLORS["unexplored_fill"],   self.COLORS["unexplored_outline"], "circle"),
        ]

        # separator
        self.canvas.create_line(20, y - 18, canvas_w - 20, y - 18,
                                fill=self.COLORS["grid"], width=1)

        total_w = len(items) * 95
        sx = (canvas_w - total_w) / 2

        for i, (label, fill, outline, shape) in enumerate(items):
            x = sx + i * 95
            if shape == "square":
                self.canvas.create_rectangle(x, y - 6, x + 12, y + 6,
                                             fill=fill, outline=outline, width=1)
            elif shape == "diamond":
                self.canvas.create_polygon(
                    x + 6, y - 6, x + 12, y, x + 6, y + 6, x, y,
                    fill=fill, outline=outline, width=1)
            else:
                self.canvas.create_oval(x, y - 6, x + 12, y + 6,
                                        fill=fill, outline=outline, width=1)
            self.canvas.create_text(x + 18, y, text=label,
                                    fill=self.COLORS["text"], font=("Consolas", 8),
                                    anchor="w")

    # ── dungeon renderer ────────────────────────────────────────────
    def _render_dungeon_map(self):
        floor_num = self._current_floor_number()
        total_floors = self._get_dungeon_total_floors()
        rooms = self._get_dungeon_floor_rooms(floor_num)

        visited = set(self.visited_rooms) if not self.reveal_all else set(rooms.keys())

        if self.header_var:
            self.header_var.set(
                f"\u2694 DUNGEON MAP \u2014 FLOOR {floor_num} / {total_floors} \u2694"
            )

        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
        if canvas_w < 20 or canvas_h < 20:
            return

        if not rooms:
            self.canvas.create_text(
                canvas_w / 2, canvas_h / 2,
                text="No dungeon rooms on this floor.",
                fill=self.COLORS["text_dim"], font=("Consolas", 12),
            )
            return

        coord_map = {}
        for rid, rdata in rooms.items():
            c = rdata.get("coordinates", [0, 0])
            coord_map[(c[0], c[1])] = rid

        positions, spacing = self._compute_layout(coord_map, canvas_w, canvas_h)

        self._draw_grid(positions, spacing)
        self._draw_connections(positions, rooms, visited)
        self._draw_rooms(positions, rooms, visited)
        self._draw_legend(canvas_h)

        # stats bar
        total = len(rooms)
        found = len([r for r in rooms if r in visited])
        cur_name = rooms.get(self.current_location, {}).get("name", "Unknown")
        fog = "\U0001f513 Reveal ON" if self.reveal_all else "\U0001f512 Fog of War"
        if self.stats_var:
            self.stats_var.set(
                f"  Location: {cur_name}  |  "
                f"Floor {floor_num} Discovered: {found}/{total}  |  {fog}"
            )

    # ── overworld renderer ──────────────────────────────────────────
    def _render_overworld_map(self):
        rooms: dict = {}
        # Collect set of fixed dungeon room IDs to exclude from overworld
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

        visited = set(self.visited_rooms) if not self.reveal_all else set(rooms.keys())

        if self.header_var:
            self.header_var.set("\U0001f5fa OVERWORLD MAP \U0001f5fa")

        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
        if canvas_w < 20 or canvas_h < 20:
            return

        if not rooms:
            self.canvas.create_text(
                canvas_w / 2, canvas_h / 2,
                text="No rooms found.",
                fill=self.COLORS["text_dim"], font=("Consolas", 12),
            )
            return

        coord_map = {}
        for rid, rdata in rooms.items():
            c = rdata["coordinates"]
            coord_map[(c[0], c[1])] = rid

        positions, spacing = self._compute_layout(coord_map, canvas_w, canvas_h)

        self._draw_grid(positions, spacing)
        self._draw_connections(positions, rooms, visited)
        self._draw_rooms(positions, rooms, visited)
        self._draw_legend(canvas_h)

        # stats bar
        total = len(rooms)
        found = len([r for r in rooms if r in visited])
        cur_name = rooms.get(self.current_location, {}).get("name", "Unknown")
        fog = "\U0001f513 Reveal ON" if self.reveal_all else "\U0001f512 Fog of War"
        if self.stats_var:
            self.stats_var.set(
                f"  Location: {cur_name}  |  "
                f"Discovered: {found}/{total}  |  {fog}"
            )

        # update region label
        if hasattr(self, '_region_label') and self._region_label and self.current_location:
            region = self._detect_region(self.current_location).title()
            self._region_label.config(text=f"Region: {region}")

    # ── helpers (preserved from text-based version) ─────────────────
    def _player_in_dungeon(self) -> bool:
        """Check if player is actually inside a dungeon (not just at an entrance).
        Entrance rooms like 'dungeon_forest_entrance' are overworld rooms,
        not dungeon rooms. Actual dungeon rooms contain '_floor' in the ID."""
        if not self.current_location:
            return False
        # Must have '_floor' in the ID (e.g., dungeon_12345_floor1_room2)
        if "_floor" in self.current_location and self.current_location.startswith("dungeon_"):
            return True
        # Also check if the engine has an active dungeon instance and the player is inside it
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
        # Standard procedural dungeon format: dungeon_{seed}_floor{N}_room{M}
        for part in self.current_location.split("_"):
            if part.startswith("floor"):
                try:
                    return int(part[5:])
                except ValueError:
                    pass
        # Fixed dungeon format: {prefix}_f{N}_{room_name} (e.g. sc_f1_entrance)
        import re
        m = re.search(r'_f(\d+)_', self.current_location)
        if m:
            return int(m.group(1))
        return 1

    def _get_dungeon_floor_rooms(self, floor_num: int) -> dict:
        """Return {room_id: raw_room_dict} for the requested floor."""
        # Prefer the raw dungeon data (has full exit type info for stairs detection)
        if self.game_engine and self.game_engine.current_dungeon_instance:
            di = self.game_engine.current_dungeon_instance
            if di.dungeon_data:
                # Try both int and string keys (fixed dungeons use string keys from JSON)
                floor_data = (di.dungeon_data.get("floors", {}).get(floor_num, {})
                              or di.dungeon_data.get("floors", {}).get(str(floor_num), {}))
                rooms = floor_data.get("rooms", {})
                if rooms:
                    return rooms

        # Fallback: scan engine.rooms for registered Room objects on this floor
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
        """Classify a room for colour tagging."""
        if room_id == current_room:
            return "current"

        name_lower = (room_data.get("name") or "").lower()
        exits = room_data.get("exits", {})

        # dungeon entrance detector (rooms with time_gated_dungeon or fixed_dungeon exits)
        for direction, edata in exits.items():
            if isinstance(edata, dict) and edata.get("type") in ("time_gated_dungeon", "fixed_dungeon"):
                return "dungeon_entrance"

        # stairs detector
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
