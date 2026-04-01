"""Interactive home editor overlay for placement and decoration workflows."""

import pygame
import random

from ui_animation import UI_CLOSE_DUR, UI_OPEN_DUR, ease_out_cubic

from home_items import HOME_ITEMS
from home_system import (
    ensure_player_home_state,
    get_unlocked_tiles,
    find_placed_item,
    move_item,
    rotate_item,
    recolor_item,
    set_item_skin_texture,
    store_item,
    retrieve_stored_item,
    sell_item,
)


BG = (10, 10, 10)
C_PARCHMENT = (238, 220, 178)
C_PARCHMENT_L = (248, 234, 196)
C_INK = (38, 22, 6)
C_INK_MID = (80, 50, 18)
C_INK_LIGHT = (130, 98, 50)
C_HEADER = (128, 30, 20)
C_LEATHER = (72, 38, 12)
C_COVER = (88, 50, 18)
C_SPINE_LINE = (52, 26, 8)
C_SELECT_BG = (210, 180, 118)
C_DIVIDER = (175, 152, 108)

INK = C_INK
MUTED = C_INK_MID
ACCENT = (160, 92, 36)
WARN = (160, 80, 50)
GOOD = (94, 122, 64)
GRID_LOCKED = (214, 194, 150)
GRID_OPEN = (238, 218, 175)
GRID_LINE = (145, 114, 69)


def _safe_int(value, fallback=0):
    try:
        return int(value)
    except Exception:
        return fallback


def _hex_to_rgb(hex_color, fallback=(180, 180, 180)):
    text = str(hex_color or "").strip()
    if text.startswith("#") and len(text) == 7:
        try:
            return (int(text[1:3], 16), int(text[3:5], 16), int(text[5:7], 16))
        except ValueError:
            return fallback
    return fallback


def _font_pick(size, bold=False):
    for name in ("Palatino Linotype", "Book Antiqua", "Georgia", "Times New Roman"):
        path = pygame.font.match_font(name, bold=bold)
        if path:
            return pygame.font.Font(path, max(6, size))
    return pygame.font.Font(None, max(8, size + 4))


class HomeEditorOverlay:
    OPEN_DUR = UI_OPEN_DUR
    CLOSE_DUR = UI_CLOSE_DUR

    COLOR_PRESETS = [None, "#d46a6a", "#6ad49a", "#6aa8d4", "#d4b66a", "#c17ad4"]
    SKIN_PRESETS = ["default", "oak", "stone", "iron", "arcane"]
    TEXTURE_PRESETS = ["default", "matte", "polished", "rough", "ornate"]

    def __init__(self, gui):
        self.gui = gui
        self._alive = True
        self._closing = False
        self._anim = 0.0
        self._font_cache = {}

        self.selected_inventory_item = None
        self.selected_stored_item = None
        self.selected_tile = None
        self.selected_placed_query = None

        self.palette_scroll = 0
        self.storage_scroll = 0
        self.message = "Click inventory item, then click a tile to place."
        self.message_color = INK

        self.dragging_item_query = None
        self.drag_start_tile = None
        self.hover_tile = None

        self._inventory_rows = []
        self._storage_rows = []
        self._grid_cells = []
        self._action_buttons = {}

        self._close_rect = pygame.Rect(0, 0, 1, 1)
        self._book_rect = pygame.Rect(0, 0, 1, 1)
        self._panel_cache_size = (0, 0)
        self._panel_cache_surface = None

    def is_open(self):
        return self._alive

    def close(self):
        if not self._closing:
            self._closing = True

    def _f(self, size, bold=False):
        key = (size, bold)
        if key not in self._font_cache:
            self._font_cache[key] = _font_pick(size, bold=bold)
        return self._font_cache[key]

    def _player(self):
        return getattr(self.gui.engine, "player", None)

    def _home_owned(self):
        player = self._player()
        return bool(player and player.state.get("home_owned"))

    def _home_data(self):
        player = self._player()
        if not player:
            return {}
        ensure_player_home_state(player)
        return player.state.get("home_data", {})

    def _inventory_home_items(self):
        player = self._player()
        inv = getattr(player, "inventory", {}) if player else {}
        rows = []
        for item_id, qty in sorted(inv.items()):
            if qty <= 0:
                continue
            if item_id in HOME_ITEMS:
                rows.append((item_id, qty, HOME_ITEMS[item_id]))
        return rows

    def _stored_items(self):
        return self._home_data().get("stored_items", [])

    def _placed_lookup(self):
        home_data = self._home_data()
        lookup = {}
        for placed in home_data.get("placed_items", []):
            lookup[(placed.get("x"), placed.get("y"))] = placed
        return lookup

    def _set_message(self, text, color=INK):
        self.message = text
        self.message_color = color

    def _apply_place(self, tile):
        if not self.selected_inventory_item:
            self._set_message("Select an inventory home item first.", WARN)
            return
        player = self._player()
        item_id = self.selected_inventory_item
        qty = player.inventory.get(item_id, 0) if player else 0
        if qty <= 0:
            self.selected_inventory_item = None
            self._set_message("That item is out of stock. Select another item.", WARN)
            return
        x, y = tile
        ok, msg = self.gui.engine.place_item_in_home(item_id, x, y)
        if not ok:
            self._set_message(msg, WARN)
            return

        if player and player.inventory.get(item_id, 0) > 0:
            player.inventory[item_id] -= 1
            if player.inventory[item_id] <= 0:
                player.inventory.pop(item_id, None)
                self.selected_inventory_item = None
        if hasattr(self.gui.engine, "_inventory_changed"):
            self.gui.engine._inventory_changed = True
        self._set_message(msg, GOOD)

    def _apply_remove(self):
        if not self.selected_placed_query:
            self._set_message("Select a placed item on the grid first.", WARN)
            return
        ok, item_id, msg = self.gui.engine.remove_item_from_home(self.selected_placed_query)
        if not ok:
            self._set_message(msg, WARN)
            return

        player = self._player()
        if player:
            inv = player.inventory
            inv[item_id] = inv.get(item_id, 0) + 1
        if hasattr(self.gui.engine, "_inventory_changed"):
            self.gui.engine._inventory_changed = True
        self._set_message(msg, GOOD)

    def _apply_rotate(self):
        if not self.selected_placed_query:
            self._set_message("Select a placed item first.", WARN)
            return
        ok, msg = rotate_item(self._home_data(), self.selected_placed_query, step=90)
        self._set_message(msg, GOOD if ok else WARN)

    def _apply_store(self):
        if not self.selected_placed_query:
            self._set_message("Select a placed item first.", WARN)
            return
        ok, _, msg = store_item(self._home_data(), self.selected_placed_query)
        if ok and hasattr(self.gui.engine, "refresh_home_room_description"):
            self.gui.engine.refresh_home_room_description()
        self._set_message(msg, GOOD if ok else WARN)

    def _apply_retrieve(self):
        if not self.selected_stored_item:
            self._set_message("Select a stored item first.", WARN)
            return
        tile = self.selected_tile
        if tile is None:
            self._set_message("Select a destination tile first.", WARN)
            return
        ok, msg = retrieve_stored_item(self._home_data(), self.selected_stored_item, x=tile[0], y=tile[1])
        if ok and hasattr(self.gui.engine, "refresh_home_room_description"):
            self.gui.engine.refresh_home_room_description()
        self._set_message(msg, GOOD if ok else WARN)

    def _apply_sell(self):
        if not self.selected_placed_query:
            self._set_message("Select a placed item first.", WARN)
            return
        ok, value, msg = sell_item(self._home_data(), self.selected_placed_query)
        if ok:
            player = self._player()
            if player:
                player.stats["gold"] = _safe_int(player.stats.get("gold", 0)) + value
            if hasattr(self.gui.engine, "refresh_home_room_description"):
                self.gui.engine.refresh_home_room_description()
        self._set_message(msg, GOOD if ok else WARN)

    def _apply_use(self):
        if not self.selected_placed_query:
            self._set_message("Select a placed item first.", WARN)
            return
        ok, msg = self.gui.engine.use_home_object(self.selected_placed_query)
        self._set_message(msg, GOOD if ok else WARN)

    def _cycle_recolor(self):
        if not self.selected_placed_query:
            self._set_message("Select a placed item first.", WARN)
            return
        _, placed = find_placed_item(self._home_data(), item_query=self.selected_placed_query)
        if not placed:
            self._set_message("That item no longer exists.", WARN)
            return
        current = placed.get("tint")
        idx = 0
        if current in self.COLOR_PRESETS:
            idx = self.COLOR_PRESETS.index(current)
        nxt = self.COLOR_PRESETS[(idx + 1) % len(self.COLOR_PRESETS)]
        ok, msg = recolor_item(self._home_data(), self.selected_placed_query, nxt)
        self._set_message(msg, GOOD if ok else WARN)

    def _cycle_skin(self):
        if not self.selected_placed_query:
            self._set_message("Select a placed item first.", WARN)
            return
        _, placed = find_placed_item(self._home_data(), item_query=self.selected_placed_query)
        if not placed:
            self._set_message("That item no longer exists.", WARN)
            return
        current = placed.get("skin", "default")
        idx = self.SKIN_PRESETS.index(current) if current in self.SKIN_PRESETS else 0
        nxt = self.SKIN_PRESETS[(idx + 1) % len(self.SKIN_PRESETS)]
        ok, msg = set_item_skin_texture(self._home_data(), self.selected_placed_query, skin=nxt)
        self._set_message(msg, GOOD if ok else WARN)

    def _cycle_texture(self):
        if not self.selected_placed_query:
            self._set_message("Select a placed item first.", WARN)
            return
        _, placed = find_placed_item(self._home_data(), item_query=self.selected_placed_query)
        if not placed:
            self._set_message("That item no longer exists.", WARN)
            return
        current = placed.get("texture", "default")
        idx = self.TEXTURE_PRESETS.index(current) if current in self.TEXTURE_PRESETS else 0
        nxt = self.TEXTURE_PRESETS[(idx + 1) % len(self.TEXTURE_PRESETS)]
        ok, msg = set_item_skin_texture(self._home_data(), self.selected_placed_query, texture=nxt)
        self._set_message(msg, GOOD if ok else WARN)

    def _handle_action(self, action):
        if action == "remove":
            self._apply_remove()
        elif action == "rotate":
            self._apply_rotate()
        elif action == "store":
            self._apply_store()
        elif action == "retrieve":
            self._apply_retrieve()
        elif action == "sell":
            self._apply_sell()
        elif action == "use":
            self._apply_use()
        elif action == "recolor":
            self._cycle_recolor()
        elif action == "skin":
            self._cycle_skin()
        elif action == "texture":
            self._cycle_texture()

    def handle_event(self, event):
        if not self._home_owned():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.close()
                return True
            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.KEYDOWN):
                self._set_message("Buy a home deed first, then reopen the Home Editor.", WARN)
                return True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.close()
                return True
            if event.key == pygame.K_DELETE:
                self._apply_remove()
                return True
            if event.key == pygame.K_r:
                self._apply_rotate()
                return True
            if event.key == pygame.K_s:
                self._apply_store()
                return True
            if event.key == pygame.K_u:
                self._apply_use()
                return True
            if event.key == pygame.K_c:
                self._cycle_recolor()
                return True
            if event.key == pygame.K_k:
                self._cycle_skin()
                return True
            if event.key == pygame.K_t:
                self._cycle_texture()
                return True
            if event.key == pygame.K_e:
                self._apply_sell()
                return True

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            if self._close_rect.collidepoint(pos):
                self.close()
                return True

            for rect, item_id in self._inventory_rows:
                if rect.collidepoint(pos):
                    self.selected_inventory_item = item_id
                    self.selected_stored_item = None
                    self._set_message(f"Selected inventory item: {item_id}")
                    return True

            for rect, item_id in self._storage_rows:
                if rect.collidepoint(pos):
                    self.selected_stored_item = item_id
                    self._set_message(f"Selected stored item: {item_id}")
                    return True

            for action, rect in self._action_buttons.items():
                if rect.collidepoint(pos):
                    self._handle_action(action)
                    return True

            for rect, tile in self._grid_cells:
                if rect.collidepoint(pos):
                    self.selected_tile = tile
                    lookup = self._placed_lookup()
                    placed = lookup.get(tile)
                    if placed:
                        self.selected_placed_query = placed.get("item_id")
                        self.dragging_item_query = placed.get("item_id")
                        self.drag_start_tile = tile
                        self._set_message(f"Selected placed item: {self.selected_placed_query}")
                    else:
                        self.selected_placed_query = None
                        self._apply_place(tile)
                    return True

        if event.type == pygame.MOUSEMOTION:
            pos = event.pos
            self.hover_tile = None
            for rect, tile in self._grid_cells:
                if rect.collidepoint(pos):
                    self.hover_tile = tile
                    break

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.dragging_item_query:
            target_tile = None
            for rect, tile in self._grid_cells:
                if rect.collidepoint(event.pos):
                    target_tile = tile
                    break
            if target_tile and target_tile != self.drag_start_tile:
                ok, msg = move_item(self._home_data(), self.dragging_item_query, target_tile[0], target_tile[1])
                self._set_message(msg, GOOD if ok else WARN)
            self.dragging_item_query = None
            self.drag_start_tile = None
            return True

        return False

    def update(self, dt):
        speed = dt / self.OPEN_DUR if not self._closing else dt / self.CLOSE_DUR
        if self._closing:
            self._anim -= speed
            if self._anim <= 0.0:
                self._alive = False
        else:
            self._anim = min(1.0, self._anim + speed)

    def _build_panel_base(self, bw, bh):
        panel = pygame.Surface((bw, bh), pygame.SRCALPHA)
        mid_x = bw // 2
        pygame.draw.rect(panel, C_PARCHMENT, pygame.Rect(0, 0, mid_x + 2, bh), border_radius=8)
        pygame.draw.rect(panel, C_PARCHMENT_L, pygame.Rect(mid_x - 2, 0, bw - (mid_x - 2), bh), border_radius=8)

        rng = random.Random(5192)
        spots = pygame.Surface((bw, bh), pygame.SRCALPHA)
        for _ in range(118):
            sx = rng.randint(6, max(7, bw - 6))
            sy = rng.randint(6, max(7, bh - 6))
            rr = rng.randint(2, 6)
            aa = rng.randint(8, 24)
            pygame.draw.circle(spots, (96, 64, 24, aa), (sx, sy), rr)
        panel.blit(spots, (0, 0))

        pygame.draw.rect(panel, C_LEATHER, pygame.Rect(mid_x - 11, 0, 22, bh))
        pygame.draw.rect(panel, C_COVER, pygame.Rect(mid_x - 4, 0, 4, bh))
        for i in range(1, 7):
            ly = int(bh * i / 7)
            pygame.draw.rect(panel, C_SPINE_LINE, pygame.Rect(mid_x - 11, ly - 2, 22, 4), border_radius=1)

        pygame.draw.rect(panel, C_COVER, panel.get_rect(), 3, border_radius=8)
        pygame.draw.line(panel, C_DIVIDER, (0, 60), (bw, 60), 1)
        pygame.draw.line(panel, C_DIVIDER, (0, bh - 46), (bw, bh - 46), 1)
        return panel

    def _draw_text(self, surf, text, x, y, size=16, color=INK, bold=False):
        fs = self._f(size, bold=bold)
        surf.blit(fs.render(str(text), True, color), (x, y))

    def draw(self, surface):
        if self._anim <= 0.0:
            return

        eased = ease_out_cubic(self._anim)
        w, h = surface.get_size()
        dim = pygame.Surface((w, h), pygame.SRCALPHA)
        dim.fill((*BG, int(170 * eased)))
        surface.blit(dim, (0, 0))

        scale = 0.92 + (0.08 * eased)
        bw = int(w * 0.92 * scale)
        bh = int(h * 0.88 * scale)
        bx = (w - bw) // 2
        by = (h - bh) // 2
        self._book_rect = pygame.Rect(bx, by, bw, bh)

        shadow = pygame.Surface((bw + 28, bh + 28), pygame.SRCALPHA)
        pygame.draw.rect(shadow, (0, 0, 0, 82), pygame.Rect(14, 14, bw, bh), border_radius=10)
        surface.blit(shadow, (bx - 14, by - 14))

        if self._panel_cache_surface is None or self._panel_cache_size != (bw, bh):
            self._panel_cache_surface = self._build_panel_base(bw, bh)
            self._panel_cache_size = (bw, bh)
        panel = self._panel_cache_surface.copy()

        left_w = int(bw * 0.30)
        center_w = int(bw * 0.40)
        right_w = bw - left_w - center_w - 24

        left_x = 12
        center_x = left_x + left_w + 8
        right_x = center_x + center_w + 8

        self._draw_text(panel, "HOME EDITOR", 16, 14, size=27, color=C_HEADER, bold=True)
        self._draw_text(panel, "Place | rotate | move | return | store home | sell | use | recolor | skin | texture", 16, 42, size=14, color=C_INK_MID)

        if not self._home_owned():
            self._draw_text(panel, "Home ownership required. Use 'buy home deed' first.", 16, 64, size=14, color=WARN)

        self._close_rect = pygame.Rect(bx + bw - 46, by + 12, 34, 30)
        close_col = (158, 92, 56) if self._close_rect.collidepoint(pygame.mouse.get_pos()) else (142, 82, 49)
        pygame.draw.rect(surface, close_col, self._close_rect, border_radius=5)
        pygame.draw.rect(surface, C_COVER, self._close_rect, 1, border_radius=5)
        self._draw_text(surface, "X", self._close_rect.x + 11, self._close_rect.y + 4, size=17, color=(246, 228, 188), bold=True)

        # Left panel: inventory + storage
        left_panel = pygame.Rect(left_x, 72, left_w, bh - 132)
        pygame.draw.rect(panel, (230, 212, 170), left_panel, border_radius=6)
        pygame.draw.rect(panel, C_INK_LIGHT, left_panel, 1, border_radius=6)
        self._draw_text(panel, "Inventory Home Items", left_x + 8, 80, size=16, color=C_HEADER, bold=True)
        pygame.draw.line(panel, C_DIVIDER, (left_x + 8, 101), (left_x + left_w - 8, 101), 1)

        self._inventory_rows = []
        inv_rows = self._inventory_home_items()
        y = 106
        row_h = 22
        for item_id, qty, data in inv_rows[:18]:
            rect = pygame.Rect(left_x + 8, y, left_w - 16, row_h)
            selected = self.selected_inventory_item == item_id
            fill = C_SELECT_BG if selected else (236, 222, 188)
            border = C_INK_MID if selected else C_DIVIDER
            pygame.draw.rect(panel, fill, rect, border_radius=4)
            pygame.draw.rect(panel, border, rect, 1, border_radius=4)
            self._draw_text(panel, f"{item_id} x{qty}", rect.x + 6, rect.y + 3, size=14, color=C_INK)
            self._inventory_rows.append((pygame.Rect(bx + rect.x, by + rect.y, rect.w, rect.h), item_id))
            y += row_h + 4

        self._draw_text(panel, "Stored", left_x + 8, bh - 186, size=16, color=C_HEADER, bold=True)
        pygame.draw.line(panel, C_DIVIDER, (left_x + 8, bh - 166), (left_x + left_w - 8, bh - 166), 1)
        self._storage_rows = []
        sy = bh - 160
        for entry in self._stored_items()[:6]:
            item_id = entry.get("item_id", "unknown")
            rect = pygame.Rect(left_x + 8, sy, left_w - 16, row_h)
            selected = self.selected_stored_item == item_id
            fill = (204, 190, 150) if selected else (229, 214, 180)
            border = C_INK_MID if selected else C_DIVIDER
            pygame.draw.rect(panel, fill, rect, border_radius=4)
            pygame.draw.rect(panel, border, rect, 1, border_radius=4)
            self._draw_text(panel, item_id, rect.x + 6, rect.y + 3, size=14, color=C_INK)
            self._storage_rows.append((pygame.Rect(bx + rect.x, by + rect.y, rect.w, rect.h), item_id))
            sy += row_h + 4

        # Center panel: grid
        grid_rect = pygame.Rect(center_x, 72, center_w, bh - 132)
        pygame.draw.rect(panel, (232, 216, 176), grid_rect, border_radius=6)
        pygame.draw.rect(panel, C_INK_LIGHT, grid_rect, 1, border_radius=6)
        self._draw_text(panel, "Layout Grid", center_x + 8, 80, size=16, color=C_HEADER, bold=True)
        pygame.draw.line(panel, C_DIVIDER, (center_x + 8, 101), (center_x + center_w - 8, 101), 1)

        unlocked = set(get_unlocked_tiles(self._home_data()))
        lookup = self._placed_lookup()

        tile_size = 28
        start_x = center_x + 10
        start_y = 108
        self._grid_cells = []

        if unlocked:
            max_x = max(x for x, _ in unlocked)
            max_y = max(y for _, y in unlocked)
        else:
            max_x = 7
            max_y = 5

        for gy in range(max_y + 1):
            for gx in range(max_x + 1):
                r = pygame.Rect(start_x + gx * tile_size, start_y + gy * tile_size, tile_size - 2, tile_size - 2)
                tile = (gx, gy)
                if tile in unlocked:
                    fill = GRID_OPEN
                    if tile == self.hover_tile:
                        fill = (222, 198, 146)
                else:
                    fill = GRID_LOCKED
                pygame.draw.rect(panel, fill, r)
                pygame.draw.rect(panel, GRID_LINE, r, 1)
                self._grid_cells.append((pygame.Rect(bx + r.x, by + r.y, r.w, r.h), tile))

                if tile in lookup:
                    placed = lookup[tile]
                    item_id = placed.get("item_id")
                    icon = (HOME_ITEMS.get(item_id, {}) or {}).get("map_icon", "#")
                    tint = placed.get("tint")
                    icon_color = _hex_to_rgb(tint, _hex_to_rgb((HOME_ITEMS.get(item_id, {}) or {}).get("map_color", "#cccccc")))
                    self._draw_text(panel, icon, r.x + 7, r.y + 3, size=16, color=icon_color, bold=True)
                    if self.selected_placed_query == item_id:
                        pygame.draw.rect(panel, ACCENT, r, 2)

        # Right panel: details + actions
        right_panel = pygame.Rect(right_x, 72, right_w, bh - 132)
        pygame.draw.rect(panel, (234, 219, 180), right_panel, border_radius=6)
        pygame.draw.rect(panel, C_INK_LIGHT, right_panel, 1, border_radius=6)
        self._draw_text(panel, "Selected", right_x + 8, 80, size=16, color=C_HEADER, bold=True)
        pygame.draw.line(panel, C_DIVIDER, (right_x + 8, 101), (right_x + right_w - 8, 101), 1)

        details_y = 106
        selected_item_id = self.selected_placed_query
        if selected_item_id:
            _, selected_placed = find_placed_item(self._home_data(), item_query=selected_item_id)
        else:
            selected_placed = None

        if selected_placed:
            data = HOME_ITEMS.get(selected_item_id, {})
            self._draw_text(panel, selected_item_id, right_x + 8, details_y, size=14, color=C_INK)
            details_y += 20
            self._draw_text(panel, f"rotation: {selected_placed.get('rotation', 0)}", right_x + 8, details_y, size=13, color=C_INK_MID)
            details_y += 18
            self._draw_text(panel, f"skin: {selected_placed.get('skin', 'default')}", right_x + 8, details_y, size=13, color=C_INK_MID)
            details_y += 18
            self._draw_text(panel, f"texture: {selected_placed.get('texture', 'default')}", right_x + 8, details_y, size=13, color=C_INK_MID)
            details_y += 18
            self._draw_text(panel, f"action: {data.get('use_action', 'none')}", right_x + 8, details_y, size=13, color=C_INK_MID)
        else:
            self._draw_text(panel, "No placed item selected", right_x + 8, details_y, size=14, color=C_INK_MID)

        actions = [
            ("rotate", "Rotate"),
            ("remove", "Return to Inv"),
            ("store", "Store (Home)"),
            ("retrieve", "Retrieve"),
            ("sell", "Sell"),
            ("use", "Interact/Use"),
            ("recolor", "Recolor"),
            ("skin", "Skin"),
            ("texture", "Texture"),
        ]
        self._action_buttons = {}
        ay = 220
        for action, label in actions:
            rect = pygame.Rect(right_x + 8, ay, right_w - 16, 24)
            hover = rect.collidepoint((pygame.mouse.get_pos()[0] - bx, pygame.mouse.get_pos()[1] - by))
            fill = (198, 176, 131) if hover else (208, 186, 141)
            pygame.draw.rect(panel, fill, rect, border_radius=4)
            pygame.draw.rect(panel, C_INK_MID, rect, 1, border_radius=4)
            self._draw_text(panel, label, rect.x + 8, rect.y + 4, size=13, color=C_INK)
            self._action_buttons[action] = pygame.Rect(bx + rect.x, by + rect.y, rect.w, rect.h)
            ay += 28

        # Footer
        self._draw_text(panel, self.message, 14, bh - 33, size=14, color=self.message_color)
        self._draw_text(panel, "Shortcuts: R rotate | Del return-to-inv | S store-home | E sell | U use | C recolor | K skin | T texture", 14, bh - 18, size=12, color=C_INK_LIGHT)

        surface.blit(panel, (bx, by))
