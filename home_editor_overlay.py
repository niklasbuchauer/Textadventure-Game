"""Interactive home editor overlay for placement and decoration workflows."""

import pygame
import random
import time

from ui_animation import UI_CLOSE_DUR, UI_OPEN_DUR, ease_out_cubic

from home_items import HOME_ITEMS
from home_system import (
    ensure_player_home_state,
    HOME_ROOMS,
    get_active_room_id,
    set_active_room,
    get_unlocked_tiles,
    find_placed_item,
    move_item,
    store_item,
    retrieve_stored_item,
    sell_item,
    store_inventory_item,
    retrieve_inventory_item,
    set_spawn_room,
    plant_garden_crop,
    harvest_garden,
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
        self.dragging_inventory_item = None
        self.hover_tile = None

        self._inventory_rows = []
        self._player_inventory_rows = []
        self._home_inventory_rows = []
        self._storage_rows = []
        self._grid_cells = []
        self._action_buttons = {}
        self._room_tab_rows = []
        self._container_rows = []
        self._container_item_rows = []
        self._seed_rows = []
        self.selected_container_id = None
        self.selected_container_item = None
        self.selected_seed_item = None
        self.selected_player_inventory_item = None
        self.player_inventory_scroll = 0
        self.home_inventory_scroll = 0
        self._player_inventory_panel_rect = pygame.Rect(0, 0, 0, 0)
        self._home_inventory_panel_rect = pygame.Rect(0, 0, 0, 0)

        self._close_rect = pygame.Rect(0, 0, 1, 1)
        self._book_rect = pygame.Rect(0, 0, 1, 1)
        self._panel_cache_size = (0, 0)
        self._panel_cache_surface = None
        self._drag_ghost_cache = {}

    def is_open(self):
        return self._alive

    def is_drag_active(self):
        return bool(self.dragging_inventory_item or self.dragging_item_query)

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
        state = getattr(player, "state", {}) if player else {}
        if not isinstance(state, dict):
            return {}

        home_data = state.get("home_data")
        if not isinstance(home_data, dict):
            ensure_player_home_state(player)
            return player.state.get("home_data", {})

        # Only normalize if key structural fields are missing.
        required = ("unlocked_rooms", "placed_items", "containers", "garden_state")
        if any(key not in home_data for key in required):
            ensure_player_home_state(player)
            return player.state.get("home_data", {})
        return home_data

    def _inventory_home_items(self, inv=None):
        if inv is None:
            player = self._player()
            inv = getattr(player, "inventory", {}) if player else {}
        rows = []
        for item_id, qty in sorted(inv.items()):
            if qty <= 0:
                continue
            rows.append((item_id, qty, HOME_ITEMS.get(item_id, {})))
        return rows

    def _player_inventory_items(self, inv_rows=None):
        if inv_rows is None:
            inv_rows = self._inventory_home_items()
        rows = []
        for item_id, qty, data in inv_rows:
            if item_id in HOME_ITEMS:
                continue
            rows.append((item_id, qty, data))
        return rows

    def _home_inventory_items(self, inv_rows=None):
        if inv_rows is None:
            inv_rows = self._inventory_home_items()
        rows = []
        for item_id, qty, data in inv_rows:
            if item_id not in HOME_ITEMS:
                continue
            rows.append((item_id, qty, data))
        return rows

    def _room_name(self, room_id):
        return HOME_ROOMS.get(room_id, {}).get("name", room_id)

    def _item_allowed_rooms(self, item_id, data=None):
        item_def = data if isinstance(data, dict) else HOME_ITEMS.get(item_id, {})
        allowed = item_def.get("allowed_rooms", []) if isinstance(item_def, dict) else []
        rooms = []
        for room_id in allowed or []:
            room_key = str(room_id or "").strip().lower().replace(" ", "_")
            if room_key:
                rooms.append(room_key)
        return rooms

    def _item_placeable_in_active_room(self, item_id, data=None, active_room=None):
        allowed_rooms = self._item_allowed_rooms(item_id, data)
        if not allowed_rooms:
            return True
        room_id = active_room or self._active_room_id()
        return room_id in allowed_rooms

    def _item_room_tag(self, item_id, data=None):
        allowed_rooms = self._item_allowed_rooms(item_id, data)
        if not allowed_rooms:
            return None
        if len(allowed_rooms) == 1:
            return f"{self._room_name(allowed_rooms[0])} only"
        return f"{', '.join(self._room_name(room_id) for room_id in allowed_rooms)} only"

    def _inventory_row_height(self):
        return 22

    def _max_inventory_scroll(self, row_count, visible_height):
        content_height = max(0, row_count * (self._inventory_row_height() + 4) - 4)
        return max(0, content_height - visible_height)

    def _scroll_inventory(self, which, delta, row_count, visible_height):
        current = getattr(self, which)
        current -= int(delta) * 32
        current = max(0, min(current, self._max_inventory_scroll(row_count, visible_height)))
        setattr(self, which, current)

    def _panel_hovered(self, rect, pos):
        return isinstance(rect, pygame.Rect) and rect.width > 0 and rect.height > 0 and rect.collidepoint(pos)

    def _draw_inventory_section(self, panel, bx, by, section_rect, title, rows, scroll_attr, selection_attr, rect_attr, show_room_tags=False, subtitle=None, active_room=None):
        pygame.draw.rect(panel, (230, 212, 170), section_rect, border_radius=6)
        pygame.draw.rect(panel, C_INK_LIGHT, section_rect, 1, border_radius=6)
        self._draw_text(panel, title, section_rect.x + 8, section_rect.y + 8, size=16, color=C_HEADER, bold=True)
        if subtitle:
            self._draw_text(panel, subtitle, section_rect.x + 92, section_rect.y + 10, size=12, color=C_INK_MID)

        list_x = section_rect.x + 8
        list_y = section_rect.y + 34
        list_w = section_rect.width - 16
        list_h = section_rect.height - 42
        row_h = self._inventory_row_height()
        max_scroll = self._max_inventory_scroll(len(rows), list_h)
        scroll = min(max(0, getattr(self, scroll_attr)), max_scroll)
        setattr(self, scroll_attr, scroll)

        rects = []
        visible_top = list_y
        visible_bottom = list_y + list_h
        active_room_id = active_room if show_room_tags else None
        for row_idx, (item_id, qty, data) in enumerate(rows):
            y = list_y + row_idx * (row_h + 4) - scroll
            if y + row_h < visible_top or y > visible_bottom:
                continue

            rect = pygame.Rect(list_x, y, list_w, row_h)
            selected = getattr(self, selection_attr) == item_id
            allowed_here = True
            if show_room_tags:
                allowed_here = self._item_placeable_in_active_room(item_id, data, active_room=active_room_id)

            fill = C_SELECT_BG if selected else (236, 222, 188)
            if show_room_tags and not allowed_here:
                fill = (225, 206, 176)
            border = C_INK_MID if selected else (C_DIVIDER if (allowed_here or not show_room_tags) else WARN)
            pygame.draw.rect(panel, fill, rect, border_radius=4)
            pygame.draw.rect(panel, border, rect, 1, border_radius=4)

            row_color = C_INK if (allowed_here or not show_room_tags) else WARN
            self._draw_text(panel, f"{item_id} x{qty}", rect.x + 6, rect.y + 3, size=13, color=row_color)
            if show_room_tags:
                room_tag = self._item_room_tag(item_id, data)
                if room_tag:
                    self._draw_text(panel, room_tag, rect.x + 142, rect.y + 4, size=11, color=C_INK_MID if allowed_here else WARN)

            rects.append((pygame.Rect(bx + rect.x, by + rect.y, rect.w, rect.h), item_id))

        setattr(self, rect_attr, rects)

    def _active_room_id(self, home_data=None):
        return get_active_room_id(home_data if isinstance(home_data, dict) else self._home_data())

    def _current_drag_item_id(self):
        if self.dragging_inventory_item:
            return self.dragging_inventory_item
        if self.dragging_item_query:
            return self.dragging_item_query
        return None

    def _drag_ghost_surface(self, item_id):
        cached = self._drag_ghost_cache.get(item_id)
        if cached is not None:
            return cached

        item_data = HOME_ITEMS.get(item_id, {}) if isinstance(HOME_ITEMS.get(item_id, {}), dict) else {}
        icon = str(item_data.get("map_icon", "#"))[:1]
        icon_color = _hex_to_rgb(item_data.get("map_color", "#cccccc"))

        ghost = pygame.Surface((28, 28), pygame.SRCALPHA)
        pygame.draw.circle(ghost, (20, 12, 6, 190), (14, 14), 13)
        pygame.draw.circle(ghost, (230, 210, 170, 220), (14, 14), 12)
        pygame.draw.circle(ghost, (120, 90, 50, 220), (14, 14), 12, 1)
        icon_surf = self._f(16, bold=True).render(icon, True, icon_color)
        ghost.blit(icon_surf, (14 - icon_surf.get_width() // 2, 14 - icon_surf.get_height() // 2))
        self._drag_ghost_cache[item_id] = ghost
        return ghost

    def _stored_items(self, home_data=None):
        data = home_data if isinstance(home_data, dict) else self._home_data()
        return data.get("stored_items", [])

    def _placed_lookup(self, home_data=None, active_room=None):
        home_data = home_data if isinstance(home_data, dict) else self._home_data()
        active_room = active_room or self._active_room_id(home_data)
        lookup = {}
        for placed in home_data.get("placed_items", []):
            if str(placed.get("room_id", "foyer")).strip().lower() != active_room:
                continue
            lookup[(placed.get("x"), placed.get("y"))] = placed
        return lookup

    def _containers_in_active_room(self, home_data=None, active_room=None):
        home_data = home_data if isinstance(home_data, dict) else self._home_data()
        active_room = active_room or self._active_room_id(home_data)
        rows = []
        for container in home_data.get("containers", []):
            if str(container.get("room_id", "")).strip().lower() != active_room:
                continue
            items = container.get("items", {}) if isinstance(container.get("items", {}), dict) else {}
            used = sum(max(0, int(v)) for v in items.values())
            cap = max(0, int(container.get("capacity", 0) or 0))
            rows.append((container, used, cap))
        return rows

    def _garden_plot_rows(self, home_data=None):
        home_data = home_data if isinstance(home_data, dict) else self._home_data()
        garden = home_data.get("garden_state", {}) if isinstance(home_data.get("garden_state", {}), dict) else {}
        return list(garden.get("plots", []))

    def _set_message(self, text, color=INK):
        self.message = text
        self.message_color = color

    def _apply_place(self, tile):
        if not self.selected_inventory_item:
            self._set_message("Select an inventory home item first.", WARN)
            return
        player = self._player()
        item_id = self.selected_inventory_item
        if item_id not in HOME_ITEMS:
            self._set_message("That item is not a placeable home object.", WARN)
            return
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

    def _apply_store_container(self):
        if not self.selected_player_inventory_item:
            self._set_message("Select a backpack item to store.", WARN)
            return
        ok, msg = store_inventory_item(
            self._player(),
            self.selected_player_inventory_item,
            quantity=1,
            room_id=self._active_room_id(),
            container_id=self.selected_container_id,
        )
        if ok and hasattr(self.gui.engine, "_inventory_changed"):
            self.gui.engine._inventory_changed = True
        self._set_message(msg, GOOD if ok else WARN)

    def _apply_take_container(self):
        if not self.selected_container_item:
            self._set_message("Select a container item to retrieve.", WARN)
            return
        ok, msg = retrieve_inventory_item(
            self._player(),
            self.selected_container_item,
            quantity=1,
            room_id=self._active_room_id(),
            container_id=self.selected_container_id,
        )
        if ok and hasattr(self.gui.engine, "_inventory_changed"):
            self.gui.engine._inventory_changed = True
        self._set_message(msg, GOOD if ok else WARN)

    def _apply_plant_seed(self):
        if self._active_room_id() != "garden":
            self._set_message("Switch to the Garden Room first.", WARN)
            return
        if not self.selected_seed_item:
            self._set_message("Select a seed item to plant.", WARN)
            return
        ok, msg = plant_garden_crop(self._player(), self.selected_seed_item, quantity=1)
        if ok and hasattr(self.gui.engine, "_inventory_changed"):
            self.gui.engine._inventory_changed = True
        self._set_message(msg, GOOD if ok else WARN)

    def _apply_harvest(self):
        ok, msg = harvest_garden(self._player())
        if ok and hasattr(self.gui.engine, "_inventory_changed"):
            self.gui.engine._inventory_changed = True
        self._set_message(msg, GOOD if ok else WARN)

    def _apply_set_spawn(self):
        ok, msg = set_spawn_room(self._home_data(), self._active_room_id())
        self._set_message(msg, GOOD if ok else WARN)

    def _switch_room(self, room_id):
        ok, msg = set_active_room(self._home_data(), room_id)
        if ok:
            self.selected_tile = None
            self.selected_placed_query = None
            self.selected_inventory_item = None
            self.selected_player_inventory_item = None
            self.selected_container_item = None
            self.selected_container_id = None
            self.selected_seed_item = None
            if hasattr(self.gui.engine, "refresh_home_room_description"):
                self.gui.engine.refresh_home_room_description()
        self._set_message(msg, GOOD if ok else WARN)

    def _handle_action(self, action):
        if action == "remove":
            self._apply_remove()
        elif action == "store":
            self._apply_store()
        elif action == "retrieve":
            self._apply_retrieve()
        elif action == "sell":
            self._apply_sell()
        elif action == "use":
            self._apply_use()
        elif action == "container_store":
            self._apply_store_container()
        elif action == "container_take":
            self._apply_take_container()
        elif action == "plant_seed":
            self._apply_plant_seed()
        elif action == "harvest":
            self._apply_harvest()
        elif action == "set_spawn":
            self._apply_set_spawn()

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
            if event.key == pygame.K_s:
                self._apply_store()
                return True
            if event.key == pygame.K_u:
                self._apply_use()
                return True
            if event.key == pygame.K_e:
                self._apply_sell()
                return True

        if event.type == pygame.MOUSEWHEEL:
            pos = pygame.mouse.get_pos()
            if self._panel_hovered(self._player_inventory_panel_rect, pos):
                rows = self._player_inventory_items()
                visible_height = self._player_inventory_panel_rect.height - 34
                self._scroll_inventory("player_inventory_scroll", event.y, len(rows), visible_height)
                return True
            if self._panel_hovered(self._home_inventory_panel_rect, pos):
                rows = self._home_inventory_items()
                visible_height = self._home_inventory_panel_rect.height - 34
                self._scroll_inventory("home_inventory_scroll", event.y, len(rows), visible_height)
                return True

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            if self._close_rect.collidepoint(pos):
                self.close()
                return True

            for rect, room_id in self._room_tab_rows:
                if rect.collidepoint(pos):
                    self._switch_room(room_id)
                    return True

            for rect, item_id in self._player_inventory_rows:
                if rect.collidepoint(pos):
                    self.selected_player_inventory_item = item_id
                    self._set_message(f"Selected backpack item: {item_id}")
                    return True

            for rect, item_id in self._home_inventory_rows:
                if rect.collidepoint(pos):
                    self.selected_inventory_item = item_id
                    self.selected_player_inventory_item = None
                    self.selected_stored_item = None
                    self.dragging_inventory_item = item_id
                    allowed_rooms = self._item_allowed_rooms(item_id)
                    active_room = self._active_room_id()
                    if allowed_rooms and active_room not in allowed_rooms:
                        target_room = allowed_rooms[0]
                        self._switch_room(target_room)
                        self.selected_inventory_item = item_id
                        self.dragging_inventory_item = item_id
                        self._set_message(
                            f"Drag {item_id} onto the grid. Switched to {self._room_name(target_room)} for placement."
                        )
                    else:
                        self._set_message(f"Drag {item_id} onto the grid to place it.")
                    return True

            for rect, item_id in self._storage_rows:
                if rect.collidepoint(pos):
                    self.selected_stored_item = item_id
                    self._set_message(f"Selected stored item: {item_id}")
                    return True

            for rect, container_id in self._container_rows:
                if rect.collidepoint(pos):
                    self.selected_container_id = container_id
                    self.selected_container_item = None
                    self._set_message(f"Selected container: {container_id}")
                    return True

            for rect, item_id in self._container_item_rows:
                if rect.collidepoint(pos):
                    self.selected_container_item = item_id
                    self._set_message(f"Selected stored stack: {item_id}")
                    return True

            for rect, seed_id in self._seed_rows:
                if rect.collidepoint(pos):
                    self.selected_seed_item = seed_id
                    self._set_message(f"Selected seed: {seed_id}")
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
                        self._set_message("Drag a home placable item from the list onto this tile.", MUTED)
                    return True

        if event.type == pygame.MOUSEBUTTONDOWN and event.button in (4, 5):
            delta = 1 if event.button == 4 else -1
            pos = event.pos if hasattr(event, "pos") else pygame.mouse.get_pos()
            if self._panel_hovered(self._player_inventory_panel_rect, pos):
                rows = self._player_inventory_items()
                visible_height = self._player_inventory_panel_rect.height - 34
                self._scroll_inventory("player_inventory_scroll", delta, len(rows), visible_height)
                return True
            if self._panel_hovered(self._home_inventory_panel_rect, pos):
                rows = self._home_inventory_items()
                visible_height = self._home_inventory_panel_rect.height - 34
                self._scroll_inventory("home_inventory_scroll", delta, len(rows), visible_height)
                return True

        if event.type == pygame.MOUSEMOTION:
            pos = event.pos
            self.hover_tile = None
            for rect, tile in self._grid_cells:
                if rect.collidepoint(pos):
                    self.hover_tile = tile
                    break

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            target_tile = None
            for rect, tile in self._grid_cells:
                if rect.collidepoint(event.pos):
                    target_tile = tile
                    break

            if self.dragging_inventory_item:
                if target_tile is None and self.hover_tile is not None:
                    target_tile = self.hover_tile
                self.selected_inventory_item = self.dragging_inventory_item
                if target_tile is not None:
                    self._apply_place(target_tile)
                else:
                    self._set_message("Drop the item on a highlighted grid tile to place it.", MUTED)
                self.dragging_inventory_item = None
                return True

            if self.dragging_item_query:
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
        self._draw_text(panel, "Rooms | layout | containers | garden | bonuses", 16, 42, size=14, color=C_INK_MID)

        if not self._home_owned():
            self._draw_text(panel, "Home ownership required. Use 'buy home deed' first.", 16, 64, size=14, color=WARN)

        self._close_rect = pygame.Rect(bx + bw - 46, by + 12, 34, 30)
        close_col = (158, 92, 56) if self._close_rect.collidepoint(pygame.mouse.get_pos()) else (142, 82, 49)
        pygame.draw.rect(surface, close_col, self._close_rect, border_radius=5)
        pygame.draw.rect(surface, C_COVER, self._close_rect, 1, border_radius=5)
        self._draw_text(surface, "X", self._close_rect.x + 11, self._close_rect.y + 4, size=17, color=(246, 228, 188), bold=True)

        # Snapshot frequently used data once per frame.
        player = self._player()
        home_data = self._home_data()
        active_room = self._active_room_id(home_data)
        inv = getattr(player, "inventory", {}) if player else {}
        inv_rows = self._inventory_home_items(inv=inv)
        backpack_rows = self._player_inventory_items(inv_rows)
        home_rows = self._home_inventory_items(inv_rows)
        placed_lookup = self._placed_lookup(home_data, active_room)
        unlocked_tiles = set(get_unlocked_tiles(home_data))

        # Room tabs
        self._room_tab_rows = []
        tabs_y = 66
        tab_x = 16
        unlocked_rooms = set(home_data.get("unlocked_rooms", []))
        for room_id, info in HOME_ROOMS.items():
            label = info.get("name", room_id)
            tab_w = max(78, min(126, 26 + len(label) * 6))
            tab_rect = pygame.Rect(tab_x, tabs_y, tab_w, 22)
            is_active = room_id == active_room
            is_unlocked = room_id in unlocked_rooms
            fill = (214, 194, 150)
            if is_unlocked:
                fill = (208, 186, 141)
            if is_active:
                fill = C_SELECT_BG
            pygame.draw.rect(panel, fill, tab_rect, border_radius=4)
            pygame.draw.rect(panel, C_INK_MID, tab_rect, 1, border_radius=4)
            short = label if len(label) <= 12 else label[:11] + "…"
            suffix = "" if is_unlocked else " 🔒"
            self._draw_text(panel, f"{short}{suffix}", tab_rect.x + 5, tab_rect.y + 4, size=12, color=C_INK)
            self._room_tab_rows.append((pygame.Rect(bx + tab_rect.x, by + tab_rect.y, tab_rect.w, tab_rect.h), room_id))
            tab_x += tab_w + 6

        # Left panel: backpack inventory + home placables
        left_panel = pygame.Rect(left_x, 94, left_w, bh - 154)
        top_h = int(left_panel.height * 0.48)
        top_panel = pygame.Rect(left_panel.x, left_panel.y, left_panel.w, top_h)
        bottom_panel = pygame.Rect(left_panel.x, top_panel.bottom + 8, left_panel.w, left_panel.height - top_h - 8)
        self._player_inventory_panel_rect = pygame.Rect(bx + top_panel.x, by + top_panel.y, top_panel.w, top_panel.h)
        self._home_inventory_panel_rect = pygame.Rect(bx + bottom_panel.x, by + bottom_panel.y, bottom_panel.w, bottom_panel.h)

        self._player_inventory_rows = []
        self._home_inventory_rows = []
        self._storage_rows = []

        self._draw_inventory_section(panel, bx, by, top_panel, "Backpack", backpack_rows, "player_inventory_scroll", "selected_player_inventory_item", "_player_inventory_rows", subtitle="(scroll)")
        self._draw_inventory_section(panel, bx, by, bottom_panel, "Home Placables", home_rows, "home_inventory_scroll", "selected_inventory_item", "_home_inventory_rows", show_room_tags=True, subtitle="(scroll to browse room-locked items)", active_room=active_room)

        # Center panel: grid
        grid_rect = pygame.Rect(center_x, 94, center_w, bh - 154)
        pygame.draw.rect(panel, (232, 216, 176), grid_rect, border_radius=6)
        pygame.draw.rect(panel, C_INK_LIGHT, grid_rect, 1, border_radius=6)
        room_name = HOME_ROOMS.get(active_room, {}).get("name", active_room)
        self._draw_text(panel, f"Layout Grid: {room_name}", center_x + 8, 102, size=16, color=C_HEADER, bold=True)
        pygame.draw.line(panel, C_DIVIDER, (center_x + 8, 123), (center_x + center_w - 8, 123), 1)

        tile_size = 28
        start_x = center_x + 10
        start_y = 130
        self._grid_cells = []

        if unlocked_tiles:
            max_x = max(x for x, _ in unlocked_tiles)
            max_y = max(y for _, y in unlocked_tiles)
        else:
            max_x = 7
            max_y = 5

        for gy in range(max_y + 1):
            for gx in range(max_x + 1):
                r = pygame.Rect(start_x + gx * tile_size, start_y + gy * tile_size, tile_size - 2, tile_size - 2)
                tile = (gx, gy)
                if tile in unlocked_tiles:
                    fill = GRID_OPEN
                    if tile == self.hover_tile:
                        fill = (222, 198, 146)
                else:
                    fill = GRID_LOCKED
                pygame.draw.rect(panel, fill, r)
                pygame.draw.rect(panel, GRID_LINE, r, 1)
                self._grid_cells.append((pygame.Rect(bx + r.x, by + r.y, r.w, r.h), tile))

                if tile in placed_lookup:
                    placed = placed_lookup[tile]
                    item_id = placed.get("item_id")
                    icon = (HOME_ITEMS.get(item_id, {}) or {}).get("map_icon", "#")
                    icon_color = _hex_to_rgb((HOME_ITEMS.get(item_id, {}) or {}).get("map_color", "#cccccc"))
                    self._draw_text(panel, icon, r.x + 7, r.y + 3, size=16, color=icon_color, bold=True)
                    if self.selected_placed_query == item_id:
                        pygame.draw.rect(panel, ACCENT, r, 2)

        # Right panel: details + actions + containers + garden + bonuses
        right_panel = pygame.Rect(right_x, 94, right_w, bh - 154)
        pygame.draw.rect(panel, (234, 219, 180), right_panel, border_radius=6)
        pygame.draw.rect(panel, C_INK_LIGHT, right_panel, 1, border_radius=6)
        self._draw_text(panel, "Room Tools", right_x + 8, 102, size=16, color=C_HEADER, bold=True)
        pygame.draw.line(panel, C_DIVIDER, (right_x + 8, 123), (right_x + right_w - 8, 123), 1)

        details_y = 128
        selected_item_id = self.selected_placed_query
        if selected_item_id:
            _, selected_placed = find_placed_item(self._home_data(), item_query=selected_item_id)
        else:
            selected_placed = None

        if selected_placed:
            data = HOME_ITEMS.get(selected_item_id, {})
            self._draw_text(panel, selected_item_id, right_x + 8, details_y, size=14, color=C_INK)
            details_y += 20
            self._draw_text(panel, f"action: {data.get('use_action', 'none')}", right_x + 8, details_y, size=13, color=C_INK_MID)
        else:
            self._draw_text(panel, "No placed item selected", right_x + 8, details_y, size=14, color=C_INK_MID)

        actions = [
            ("remove", "Return to Inv"),
            ("store", "Store (Home)"),
            ("retrieve", "Retrieve"),
            ("sell", "Sell"),
            ("use", "Interact/Use"),
        ]
        self._action_buttons = {}
        ay = 174
        for action, label in actions:
            rect = pygame.Rect(right_x + 8, ay, right_w - 16, 24)
            hover = rect.collidepoint((pygame.mouse.get_pos()[0] - bx, pygame.mouse.get_pos()[1] - by))
            fill = (198, 176, 131) if hover else (208, 186, 141)
            pygame.draw.rect(panel, fill, rect, border_radius=4)
            pygame.draw.rect(panel, C_INK_MID, rect, 1, border_radius=4)
            self._draw_text(panel, label, rect.x + 8, rect.y + 4, size=13, color=C_INK)
            self._action_buttons[action] = pygame.Rect(bx + rect.x, by + rect.y, rect.w, rect.h)
            ay += 28

        # Containers
        self._draw_text(panel, "Containers", right_x + 8, ay + 4, size=14, color=C_HEADER, bold=True)
        ay += 22
        self._container_rows = []
        self._container_item_rows = []
        container_rows = self._containers_in_active_room(home_data, active_room)
        for container, used, cap in container_rows[:2]:
            cid = container.get("container_id", "container")
            rect = pygame.Rect(right_x + 8, ay, right_w - 16, 20)
            selected = self.selected_container_id == cid
            fill = C_SELECT_BG if selected else (227, 211, 174)
            pygame.draw.rect(panel, fill, rect, border_radius=4)
            pygame.draw.rect(panel, C_DIVIDER, rect, 1, border_radius=4)
            self._draw_text(panel, f"{container.get('name', cid)} {used}/{cap}", rect.x + 6, rect.y + 3, size=12, color=C_INK)
            self._container_rows.append((pygame.Rect(bx + rect.x, by + rect.y, rect.w, rect.h), cid))
            ay += 22
            if selected:
                items = container.get("items", {}) if isinstance(container.get("items", {}), dict) else {}
                for item_id, qty in sorted(items.items())[:3]:
                    srect = pygame.Rect(right_x + 14, ay, right_w - 28, 18)
                    sfill = (218, 202, 165) if self.selected_container_item == item_id else (232, 218, 184)
                    pygame.draw.rect(panel, sfill, srect, border_radius=3)
                    pygame.draw.rect(panel, C_DIVIDER, srect, 1, border_radius=3)
                    self._draw_text(panel, f"{item_id} x{qty}", srect.x + 5, srect.y + 2, size=11, color=C_INK)
                    self._container_item_rows.append((pygame.Rect(bx + srect.x, by + srect.y, srect.w, srect.h), item_id))
                    ay += 20

        for action, label in (("container_store", "Store Selected Item"), ("container_take", "Take Selected Stack")):
            rect = pygame.Rect(right_x + 8, ay, right_w - 16, 20)
            pygame.draw.rect(panel, (208, 186, 141), rect, border_radius=4)
            pygame.draw.rect(panel, C_INK_MID, rect, 1, border_radius=4)
            self._draw_text(panel, label, rect.x + 6, rect.y + 3, size=11, color=C_INK)
            self._action_buttons[action] = pygame.Rect(bx + rect.x, by + rect.y, rect.w, rect.h)
            ay += 22

        # Garden panel for garden room
        if active_room == "garden":
            self._draw_text(panel, "Garden", right_x + 8, ay + 2, size=14, color=C_HEADER, bold=True)
            ay += 20
            self._seed_rows = []
            seed_rows = [row for row in backpack_rows if row[0].endswith("_seed")]
            for item_id, qty, _ in seed_rows[:3]:
                srect = pygame.Rect(right_x + 8, ay, right_w - 16, 18)
                sfill = C_SELECT_BG if self.selected_seed_item == item_id else (232, 218, 184)
                pygame.draw.rect(panel, sfill, srect, border_radius=3)
                pygame.draw.rect(panel, C_DIVIDER, srect, 1, border_radius=3)
                self._draw_text(panel, f"{item_id} x{qty}", srect.x + 5, srect.y + 2, size=11, color=C_INK)
                self._seed_rows.append((pygame.Rect(bx + srect.x, by + srect.y, srect.w, srect.h), item_id))
                ay += 20

            plots = self._garden_plot_rows(home_data)
            if plots:
                for idx, plot in enumerate(plots[:3], start=1):
                    crop = plot.get("crop_id", "crop")
                    ready_at = int(plot.get("ready_at", 0) or 0)
                    ready_text = "ready" if ready_at <= int(time.time()) else "growing"
                    self._draw_text(panel, f"Plot {idx}: {crop} ({ready_text})", right_x + 8, ay, size=11, color=C_INK_MID)
                    ay += 14

            for action, label in (("plant_seed", "Plant Selected Seed"), ("harvest", "Harvest Ready Plots")):
                rect = pygame.Rect(right_x + 8, ay, right_w - 16, 20)
                pygame.draw.rect(panel, (208, 186, 141), rect, border_radius=4)
                pygame.draw.rect(panel, C_INK_MID, rect, 1, border_radius=4)
                self._draw_text(panel, label, rect.x + 6, rect.y + 3, size=11, color=C_INK)
                self._action_buttons[action] = pygame.Rect(bx + rect.x, by + rect.y, rect.w, rect.h)
                ay += 22
        else:
            self._seed_rows = []

        rect = pygame.Rect(right_x + 8, ay, right_w - 16, 20)
        pygame.draw.rect(panel, (208, 186, 141), rect, border_radius=4)
        pygame.draw.rect(panel, C_INK_MID, rect, 1, border_radius=4)
        self._draw_text(panel, "Set Spawn To This Room", rect.x + 6, rect.y + 3, size=11, color=C_INK)
        self._action_buttons["set_spawn"] = pygame.Rect(bx + rect.x, by + rect.y, rect.w, rect.h)
        ay += 24

        # Active home bonus status
        bonus = player.state.get("active_home_room_bonuses", {}) if player else {}
        bonus_y = min(bh - 118, ay + 4)
        self._draw_text(panel, "Active Bonus", right_x + 8, bonus_y, size=13, color=C_HEADER, bold=True)
        if isinstance(bonus, dict) and bonus:
            self._draw_text(panel, str(bonus.get("source", "home bonus")), right_x + 8, bonus_y + 14, size=11, color=C_INK)
            self._draw_text(panel, f"wins left: {int(bonus.get('wins_remaining', 0) or 0)}", right_x + 8, bonus_y + 28, size=11, color=C_INK_MID)
        else:
            self._draw_text(panel, "No active room bonus.", right_x + 8, bonus_y + 14, size=11, color=C_INK_MID)

        # Footer
        self._draw_text(panel, self.message, 14, bh - 33, size=14, color=self.message_color)
        self._draw_text(panel, "Shortcuts: Del return-to-inv | S store-home | E sell | U use", 14, bh - 18, size=12, color=C_INK_LIGHT)

        surface.blit(panel, (bx, by))

        drag_item_id = self._current_drag_item_id()
        if drag_item_id:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            ghost = self._drag_ghost_surface(drag_item_id)
            surface.blit(ghost, (mouse_x + 10, mouse_y + 8))
