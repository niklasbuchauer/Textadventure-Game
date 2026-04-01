"""
Adventure World Editor — Pygame + pygame_gui
=============================================
Standalone tool for creating and editing world.json files.
Launch:  python world_editor.py
"""

import json
import os
import sys

import pygame
import pygame_gui
from pygame_gui.elements import (
    UIButton, UIDropDownMenu, UILabel, UIPanel, UISelectionList,
    UITextBox, UITextEntryLine, UIWindow,
)

WORLD_FILE = os.path.join(os.path.dirname(__file__), "world.json")
THEME_FILE = os.path.join(os.path.dirname(__file__), "pygame_theme.json")

WIDTH, HEIGHT = 1200, 800
FPS = 60
BG = (24, 24, 28)


# =====================================================================
# ANIMATION HELPERS
# =====================================================================

def _ease_out_cubic(t):
    """Ease-out cubic easing function."""
    t = max(0.0, min(1.0, t))
    return 1.0 - (1.0 - t) ** 3


# =====================================================================
# TINY MODAL HELPERS (message / confirm / input)
# =====================================================================

class _ModalBase:
    """Base for small modal dialog overlays with popup animation."""
    
    OPEN_DUR = 0.25  # seconds to fully open
    CLOSE_DUR = 0.15  # seconds to fully close
    
    def __init__(self, manager, title, w=380, h=160):
        sw, sh = pygame.display.get_surface().get_size()
        self.window = UIWindow(
            rect=pygame.Rect((sw - w) // 2, (sh - h) // 2, w, h),
            manager=manager, window_display_title=title,
        )
        self.manager = manager
        self.result = None
        self.done = False
        
        # Animation state
        self._anim = 0.0  # 0 = fully closed, 1 = fully open
        self._closing = False
        self._orig_rect = self.window.rect.copy()
        
        # Initial state - appear from center scaled down
        self.window.visible = True

    def update(self, dt):
        """Update animation state. Call from main loop."""
        if self._closing:
            self._anim = max(0.0, self._anim - dt / self.CLOSE_DUR)
            if self._anim <= 0.0:
                self.kill()
        else:
            self._anim = min(1.0, self._anim + dt / self.OPEN_DUR)
        
        # Apply animation scale and position
        ease = _ease_out_cubic(self._anim)
        scale = 0.8 + (ease * 0.2)  # Scale from 80% to 100%
        
        # Update window position and size with animation
        orig_w, orig_h = self._orig_rect.width, self._orig_rect.height
        new_w = int(orig_w * scale)
        new_h = int(orig_h * scale)
        new_x = self._orig_rect.x + (orig_w - new_w) // 2
        new_y = self._orig_rect.y + (orig_h - new_h) // 2
        
        self.window.rect = pygame.Rect(new_x, new_y, new_w, new_h)
        
        # Fade opacity
        alpha = int(255 * ease)
        self.window.ui_container.visual_depth = alpha / 255.0  # Some containers support this

    def close(self):
        """Trigger closing animation."""
        self._closing = True

    def kill(self):
        if self.window and self.window.alive():
            self.window.kill()


class MsgBox(_ModalBase):
    def __init__(self, manager, title, text):
        super().__init__(manager, title, 400, 150)
        UITextBox(
            html_text=text, relative_rect=pygame.Rect(10, 4, 370, 60),
            manager=manager, container=self.window,
        )
        self._ok = UIButton(
            relative_rect=pygame.Rect(150, 70, 80, 30),
            text="OK", manager=manager, container=self.window,
        )

    def handle_event(self, ev):
        if ev.type == pygame_gui.UI_BUTTON_PRESSED and ev.ui_element == self._ok:
            self.done = True
            self.close()


class ConfirmBox(_ModalBase):
    def __init__(self, manager, title, text):
        super().__init__(manager, title, 400, 150)
        UITextBox(
            html_text=text, relative_rect=pygame.Rect(10, 4, 370, 60),
            manager=manager, container=self.window,
        )
        self._yes = UIButton(
            relative_rect=pygame.Rect(100, 70, 80, 30),
            text="Yes", manager=manager, container=self.window,
        )
        self._no = UIButton(
            relative_rect=pygame.Rect(200, 70, 80, 30),
            text="No", manager=manager, container=self.window,
        )

    def handle_event(self, ev):
        if ev.type == pygame_gui.UI_BUTTON_PRESSED:
            if ev.ui_element == self._yes:
                self.result = True
                self.done = True
                self.close()
            elif ev.ui_element == self._no:
                self.result = False
                self.done = True
                self.close()


class InputBox(_ModalBase):
    def __init__(self, manager, title, prompt, initial=""):
        super().__init__(manager, title, 400, 160)
        UILabel(
            relative_rect=pygame.Rect(10, 4, 370, 24),
            text=prompt, manager=manager, container=self.window,
        )
        self._entry = UITextEntryLine(
            relative_rect=pygame.Rect(10, 32, 370, 28),
            manager=manager, container=self.window,
        )
        if initial:
            self._entry.set_text(initial)
        self._ok = UIButton(
            relative_rect=pygame.Rect(100, 70, 80, 30),
            text="OK", manager=manager, container=self.window,
        )
        self._cancel = UIButton(
            relative_rect=pygame.Rect(200, 70, 80, 30),
            text="Cancel", manager=manager, container=self.window,
        )

    def handle_event(self, ev):
        if ev.type == pygame_gui.UI_BUTTON_PRESSED:
            if ev.ui_element == self._ok:
                self.result = self._entry.get_text()
                self.done = True
                self.close()
            elif ev.ui_element == self._cancel:
                self.result = None
                self.done = True
                self.close()
        if ev.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
            if ev.ui_element == self._entry:
                self.result = self._entry.get_text()
                self.done = True
                self.close()


# =====================================================================
# WORLD EDITOR
# =====================================================================

class WorldEditor:
    """Standalone Pygame world editor."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Adventure World Editor")

        theme = THEME_FILE if os.path.exists(THEME_FILE) else None
        self.manager = pygame_gui.UIManager((WIDTH, HEIGHT), theme)
        self.clock = pygame.time.Clock()

        # Data model
        self.world = {"start_room": None, "rooms": {}}
        self.world_data = self.world
        self.current_room = None
        self.world_path = WORLD_FILE
        self.active_tab = "rooms"  # "rooms" or "commands"

        # Modal stack
        self._modal = None
        self._modal_callback = None

        # Build UI
        self._build_tabs()
        self._build_room_tab()
        self._build_cmd_tab()

        # Load or blank
        if os.path.exists(self.world_path):
            if not self._load_world(self.world_path):
                self._create_blank()
        else:
            self._create_blank()

        self._refresh_room_list()
        self._show_tab("rooms")

    # ── tabs ──

    def _build_tabs(self):
        self._tab_rooms_btn = UIButton(
            relative_rect=pygame.Rect(10, 6, 140, 28),
            text="Room Editor", manager=self.manager,
        )
        self._tab_cmds_btn = UIButton(
            relative_rect=pygame.Rect(155, 6, 160, 28),
            text="Commands & Stats", manager=self.manager,
        )

    def _show_tab(self, name):
        self.active_tab = name
        for el in self._room_tab_elements:
            el.visible = (name == "rooms")
            if name == "rooms":
                el.show()
            else:
                el.hide()
        for el in self._cmd_tab_elements:
            el.visible = (name == "commands")
            if name == "commands":
                el.show()
            else:
                el.hide()

    # ── room tab ──

    def _build_room_tab(self):
        self._room_tab_elements = []
        m = self.manager
        y0 = 40
        lw = 260  # left panel width

        # Left panel
        self._room_list_label = UILabel(
            relative_rect=pygame.Rect(10, y0, lw, 22), text="Rooms", manager=m)
        self._room_list = UISelectionList(
            relative_rect=pygame.Rect(10, y0 + 24, lw, 340),
            item_list=[], manager=m, allow_multi_select=False,
        )
        self._start_label = UILabel(
            relative_rect=pygame.Rect(10, y0 + 368, lw, 22),
            text="Start: None", manager=m,
        )

        btn_y = y0 + 394
        bw = 76
        self._btn_add_room = UIButton(pygame.Rect(10, btn_y, bw, 26), "Add", m)
        self._btn_rename_room = UIButton(pygame.Rect(10 + bw + 4, btn_y, bw, 26), "Rename", m)
        self._btn_delete_room = UIButton(pygame.Rect(10 + 2 * (bw + 4), btn_y, bw, 26), "Delete", m)
        self._btn_set_start = UIButton(pygame.Rect(10, btn_y + 30, lw, 26), "Set as Start Room", m)

        self._path_label = UILabel(pygame.Rect(10, btn_y + 62, lw, 20), f"File: {os.path.basename(self.world_path)}", m)
        self._btn_load = UIButton(pygame.Rect(10, btn_y + 84, lw // 2 - 2, 26), "Load...", m)
        self._btn_save = UIButton(pygame.Rect(10 + lw // 2 + 2, btn_y + 84, lw // 2 - 2, 26), "Save", m)

        self._room_tab_elements += [
            self._room_list_label, self._room_list, self._start_label,
            self._btn_add_room, self._btn_rename_room, self._btn_delete_room,
            self._btn_set_start, self._path_label, self._btn_load, self._btn_save,
        ]

        # Right panel
        rx = lw + 20
        rw = WIDTH - rx - 10

        self._name_label = UILabel(pygame.Rect(rx, y0, 100, 22), "Room Name:", m)
        self._name_entry = UITextEntryLine(pygame.Rect(rx + 100, y0, rw - 100, 26), m)
        self._name_hint = UILabel(pygame.Rect(rx, y0 + 28, rw, 18), "(Use Rename to change room key)", m)

        self._desc_label = UILabel(pygame.Rect(rx, y0 + 50, 100, 22), "Description:", m)
        self._desc_entry = UITextEntryLine(pygame.Rect(rx, y0 + 72, rw, 28), m)

        # Exits section
        ey = y0 + 108
        self._exits_label = UILabel(pygame.Rect(rx, ey, 200, 22), "Exits (direction -> room):", m)
        self._exits_list = UISelectionList(pygame.Rect(rx, ey + 24, rw, 80), [], m, allow_multi_select=False)
        self._exit_dir_entry = UITextEntryLine(pygame.Rect(rx, ey + 108, 120, 26), m, placeholder_text="direction")
        room_names = sorted(self.world.get("rooms", {}).keys())
        self._exit_target_dd = UIDropDownMenu(
            options_list=room_names if room_names else ["(none)"],
            starting_option=room_names[0] if room_names else "(none)",
            relative_rect=pygame.Rect(rx + 126, ey + 108, 200, 26), manager=m,
        )
        self._btn_add_exit = UIButton(pygame.Rect(rx + 336, ey + 108, 80, 26), "Add Exit", m)
        self._btn_rem_exit = UIButton(pygame.Rect(rx + 420, ey + 108, 100, 26), "Remove Exit", m)

        # Items section
        iy = ey + 142
        self._items_label = UILabel(pygame.Rect(rx, iy, 100, 22), "Items:", m)
        self._items_list = UISelectionList(pygame.Rect(rx, iy + 24, rw, 80), [], m, allow_multi_select=False)
        self._item_entry = UITextEntryLine(pygame.Rect(rx, iy + 108, 250, 26), m, placeholder_text="item name")
        self._item_count_entry = UITextEntryLine(pygame.Rect(rx + 256, iy + 108, 50, 26), m, placeholder_text="qty")
        self._item_count_entry.set_text("1")
        self._btn_add_item = UIButton(pygame.Rect(rx + 312, iy + 108, 60, 26), "Add", m)
        self._btn_rem_item = UIButton(pygame.Rect(rx + 376, iy + 108, 80, 26), "Remove", m)

        # Actions section
        ay = iy + 142
        self._actions_label = UILabel(pygame.Rect(rx, ay, 200, 22), "Actions (command -> response):", m)
        self._actions_list = UISelectionList(pygame.Rect(rx, ay + 24, rw, 90), [], m, allow_multi_select=False)
        self._act_cmd_entry = UITextEntryLine(pygame.Rect(rx, ay + 118, 150, 26), m, placeholder_text="command")
        self._act_resp_entry = UITextEntryLine(pygame.Rect(rx + 156, ay + 118, 250, 26), m, placeholder_text="response text")
        self._act_effects_entry = UITextEntryLine(pygame.Rect(rx, ay + 148, 200, 26), m, placeholder_text='effects JSON')
        self._act_conds_entry = UITextEntryLine(pygame.Rect(rx + 206, ay + 148, 200, 26), m, placeholder_text='conditions JSON')
        self._btn_add_action = UIButton(pygame.Rect(rx + 414, ay + 118, 100, 26), "Add/Update", m)
        self._btn_rem_action = UIButton(pygame.Rect(rx + 414, ay + 148, 100, 26), "Remove", m)

        # Bottom
        by = ay + 182
        self._btn_save_room = UIButton(pygame.Rect(rx, by, 100, 28), "Save Room", m)
        self._btn_preview = UIButton(pygame.Rect(rx + 110, by, 110, 28), "Preview Room", m)

        self._preview_box = UITextBox(
            html_text="", relative_rect=pygame.Rect(rx, by + 34, rw, 90), manager=m,
        )

        self._room_tab_elements += [
            self._name_label, self._name_entry, self._name_hint,
            self._desc_label, self._desc_entry,
            self._exits_label, self._exits_list, self._exit_dir_entry,
            self._exit_target_dd, self._btn_add_exit, self._btn_rem_exit,
            self._items_label, self._items_list, self._item_entry,
            self._item_count_entry, self._btn_add_item, self._btn_rem_item,
            self._actions_label, self._actions_list, self._act_cmd_entry,
            self._act_resp_entry, self._act_effects_entry, self._act_conds_entry,
            self._btn_add_action, self._btn_rem_action,
            self._btn_save_room, self._btn_preview, self._preview_box,
        ]

    # ── commands & stats tab ──

    def _build_cmd_tab(self):
        self._cmd_tab_elements = []
        m = self.manager
        y0 = 40
        lw = 260  # left

        self._gcmd_label = UILabel(pygame.Rect(10, y0, lw, 22), "Global Commands", m)
        self._gcmd_list = UISelectionList(pygame.Rect(10, y0 + 24, lw, 300), [], m, allow_multi_select=False)
        btn_y = y0 + 330
        self._btn_gcmd_add = UIButton(pygame.Rect(10, btn_y, 80, 26), "Add", m)
        self._btn_gcmd_edit = UIButton(pygame.Rect(94, btn_y, 80, 26), "Edit", m)
        self._btn_gcmd_del = UIButton(pygame.Rect(178, btn_y, 80, 26), "Delete", m)

        self._cmd_tab_elements += [
            self._gcmd_label, self._gcmd_list,
            self._btn_gcmd_add, self._btn_gcmd_edit, self._btn_gcmd_del,
        ]

        # Right: command editor
        rx = lw + 20
        rw = WIDTH - rx - 10

        fields = [
            ("Command:", "_gcmd_name_entry"),
            ("Response Text:", "_gcmd_text_entry"),
            ("Inv Add (comma):", "_gcmd_inv_add_entry"),
            ("Inv Remove (comma):", "_gcmd_inv_rem_entry"),
            ("State JSON:", "_gcmd_state_entry"),
            ("Stats JSON:", "_gcmd_stats_entry"),
        ]
        cy = y0
        for label_text, attr in fields:
            lbl = UILabel(pygame.Rect(rx, cy, 160, 22), label_text, m)
            entry = UITextEntryLine(pygame.Rect(rx + 164, cy, rw - 164, 26), m)
            setattr(self, attr, entry)
            self._cmd_tab_elements.append(lbl)
            self._cmd_tab_elements.append(entry)
            cy += 30

        self._btn_gcmd_save = UIButton(pygame.Rect(rx, cy + 4, 120, 28), "Save Command", m)
        self._cmd_tab_elements.append(self._btn_gcmd_save)

        # Default stats
        cy += 40
        self._stats_label = UILabel(pygame.Rect(rx, cy, 200, 22), "Default Stats", m)
        self._stats_list = UISelectionList(pygame.Rect(rx, cy + 24, rw, 120), [], m, allow_multi_select=False)
        self._stat_name_entry = UITextEntryLine(pygame.Rect(rx, cy + 148, 150, 26), m, placeholder_text="stat name")
        self._stat_value_entry = UITextEntryLine(pygame.Rect(rx + 156, cy + 148, 100, 26), m, placeholder_text="value")
        self._btn_stat_add = UIButton(pygame.Rect(rx + 262, cy + 148, 80, 26), "Add/Set", m)
        self._btn_stat_rem = UIButton(pygame.Rect(rx + 346, cy + 148, 80, 26), "Remove", m)

        self._cmd_tab_elements += [
            self._stats_label, self._stats_list,
            self._stat_name_entry, self._stat_value_entry,
            self._btn_stat_add, self._btn_stat_rem,
        ]

        # Inventory preview
        cy += 184
        self._inv_label = UILabel(pygame.Rect(rx, cy, 200, 22), "World Items (aggregate)", m)
        self._world_items_list = UISelectionList(pygame.Rect(rx, cy + 24, rw // 2 - 4, 120), [], m, allow_multi_select=False)
        self._pinv_label = UILabel(pygame.Rect(rx + rw // 2 + 4, cy, 200, 22), "Player Start Inventory", m)
        self._player_start_list = UISelectionList(pygame.Rect(rx + rw // 2 + 4, cy + 24, rw // 2 - 4, 120), [], m, allow_multi_select=False)

        psy = cy + 148
        self._ps_entry = UITextEntryLine(pygame.Rect(rx + rw // 2 + 4, psy, 160, 26), m, placeholder_text="item")
        self._ps_count_entry = UITextEntryLine(pygame.Rect(rx + rw // 2 + 168, psy, 50, 26), m, placeholder_text="qty")
        self._ps_count_entry.set_text("1")
        self._btn_ps_add = UIButton(pygame.Rect(rx + rw // 2 + 224, psy, 80, 26), "Add", m)
        self._btn_ps_rem = UIButton(pygame.Rect(rx + rw // 2 + 308, psy, 80, 26), "Remove", m)

        self._cmd_tab_elements += [
            self._inv_label, self._world_items_list,
            self._pinv_label, self._player_start_list,
            self._ps_entry, self._ps_count_entry,
            self._btn_ps_add, self._btn_ps_rem,
        ]

    # ── data operations ──

    def _load_world(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            self._show_msg("Error", f"Failed to load: {e}")
            return False

        start = data.get("start_room") or data.get("start")
        rooms = data.get("rooms", {})
        if not isinstance(rooms, dict):
            self._show_msg("Error", "'rooms' must be a JSON object.")
            return False

        nrooms = {}
        for name, r in rooms.items():
            if not isinstance(r, dict):
                continue
            desc = r.get("description", "")
            exits = r.get("exits", {}) or {}
            raw_items = r.get("items", []) or []
            # items may be dict {item: count} or list
            if isinstance(raw_items, dict):
                items = []
                for it, cnt in raw_items.items():
                    try:
                        cnt = int(cnt)
                    except Exception:
                        cnt = 1
                    items.extend([str(it)] * max(cnt, 1))
            else:
                items = [str(it) for it in raw_items if it is not None]
            actions = r.get("actions", {}) or {}
            nactions = {}
            for cmd, val in actions.items():
                if isinstance(val, str):
                    nactions[cmd] = {"response": val}
                elif isinstance(val, dict):
                    nactions[cmd] = val
            nrooms[name] = {"description": desc, "exits": dict(exits), "items": items, "actions": nactions}

        self.world = {
            "start_room": start, "rooms": nrooms,
            "global_commands": {}, "default_stats": {},
            "item_worth": {}, "default_inventory": {},
        }
        if isinstance(data.get("global_commands"), dict):
            for k, v in data["global_commands"].items():
                if isinstance(v, str):
                    self.world["global_commands"][k] = {"text": v, "effects": {}}
                else:
                    self.world["global_commands"][k] = v
        if isinstance(data.get("default_stats"), dict):
            self.world["default_stats"] = dict(data["default_stats"])
        if isinstance(data.get("item_worth"), dict):
            w = {}
            for k, v in data["item_worth"].items():
                try:
                    w[str(k)] = int(v)
                except Exception:
                    w[str(k)] = 0
            self.world["item_worth"] = w
        raw_def_inv = data.get("default_inventory", {})
        if isinstance(raw_def_inv, dict):
            ninv = {}
            for k, v in raw_def_inv.items():
                try:
                    ninv[str(k)] = int(v)
                except Exception:
                    ninv[str(k)] = 1
            self.world["default_inventory"] = ninv
        elif isinstance(raw_def_inv, list):
            agg = {}
            for it in raw_def_inv:
                if it is None:
                    continue
                agg[str(it)] = agg.get(str(it), 0) + 1
            self.world["default_inventory"] = agg
        else:
            self.world["default_inventory"] = {}

        if not self.world["start_room"] and nrooms:
            self.world["start_room"] = next(iter(nrooms))
        self.world_path = path
        self.current_room = None
        self.world_data = self.world
        self._refresh_room_list()
        if self.world["start_room"]:
            self.current_room = self.world["start_room"]
            self._load_room_to_editor(self.current_room)
        self._refresh_inventory_views()
        self._refresh_global_commands()
        self._refresh_stats_list()
        return True

    def _save_world(self, path=None):
        path = path or self.world_path
        if not isinstance(self.world.get("rooms"), dict):
            self._show_msg("Error", "World has no rooms.")
            return False
        for name, data in self.world["rooms"].items():
            for d, targ in data.get("exits", {}).items():
                if targ not in self.world["rooms"]:
                    self._show_msg("Error", f"Exit target '{targ}' in '{name}' does not exist.")
                    return False

        out = {"start_room": self.world.get("start_room"), "rooms": {}}
        for name, data in self.world["rooms"].items():
            raw_items = data.get("items", []) or []
            item_counts = {}
            for it in raw_items:
                if it is None:
                    continue
                item_counts[str(it)] = item_counts.get(str(it), 0) + 1
            out["rooms"][name] = {
                "description": data.get("description", ""),
                "exits": data.get("exits", {}),
                "items": item_counts,
                "actions": data.get("actions", {}),
            }
        if self.world.get("global_commands"):
            out["global_commands"] = self.world["global_commands"]
        if self.world.get("default_stats"):
            out["default_stats"] = self.world["default_stats"]
        if self.world.get("item_worth"):
            out["item_worth"] = {str(k): int(v) for k, v in self.world["item_worth"].items()}
        def_inv = self.world.get("default_inventory", {}) or {}
        ninv = {}
        if isinstance(def_inv, dict):
            for k, v in def_inv.items():
                try:
                    ninv[str(k)] = int(v)
                except Exception:
                    ninv[str(k)] = 1
        out["default_inventory"] = ninv

        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(out, f, indent=2, ensure_ascii=False)
            self.world_path = path
            self.world_data = self.world
            return True
        except Exception as e:
            self._show_msg("Error", f"Failed to save: {e}")
            return False

    def _create_blank(self):
        self.world = {
            "start_room": "Village",
            "rooms": {"Village": {"description": "A peaceful village.", "exits": {}, "items": [], "actions": {}}},
            "global_commands": {}, "default_stats": {}, "default_inventory": {},
        }
        self.world_data = self.world
        self.current_room = "Village"
        self._refresh_room_list()
        self._load_room_to_editor("Village")

    # ── refresh helpers ──

    def _refresh_room_list(self):
        items = []
        for name in sorted(self.world.get("rooms", {}).keys()):
            label = f"{name} (start)" if self.world.get("start_room") == name else name
            items.append(label)
        self._room_list.set_item_list(items)
        start = self.world.get("start_room") or "None"
        self._start_label.set_text(f"Start: {start}")
        self._path_label.set_text(f"File: {os.path.basename(self.world_path)}")
        # refresh exit target dropdown
        room_names = sorted(self.world.get("rooms", {}).keys())
        if not room_names:
            room_names = ["(none)"]
        try:
            self._exit_target_dd.kill()
        except Exception:
            pass
        # Recreate dropdown with current room list
        ey = 40 + 108
        rx = 280
        self._exit_target_dd = UIDropDownMenu(
            options_list=room_names,
            starting_option=room_names[0],
            relative_rect=pygame.Rect(rx + 126, ey + 108, 200, 26),
            manager=self.manager,
        )
        if self.active_tab != "rooms":
            self._exit_target_dd.hide()
        # update the tracked elements list
        for i, el in enumerate(self._room_tab_elements):
            if el is None:
                continue
            # can't easily swap, but the dropdown is managed separately

    def _refresh_global_commands(self):
        items = sorted(self.world.get("global_commands", {}).keys())
        self._gcmd_list.set_item_list(items)

    def _refresh_stats_list(self):
        items = [f"{k} = {v}" for k, v in sorted(self.world.get("default_stats", {}).items())]
        self._stats_list.set_item_list(items)

    def _refresh_inventory_views(self):
        world_items = set()
        for rdata in self.world.get("rooms", {}).values():
            for it in rdata.get("items", []):
                world_items.add(it)
        self._world_items_list.set_item_list(sorted(world_items))
        self.world.setdefault("default_inventory", {})
        ps_items = []
        for it, cnt in sorted(self.world.get("default_inventory", {}).items(), key=lambda x: x[0].lower()):
            ps_items.append(f"{it} | {cnt}")
        self._player_start_list.set_item_list(ps_items)

    def _load_room_to_editor(self, name):
        if not name or name not in self.world.get("rooms", {}):
            return
        data = self.world["rooms"][name]
        self._name_entry.set_text(name)
        self._desc_entry.set_text(data.get("description", ""))

        exits_items = [f"{d} -> {t}" for d, t in data.get("exits", {}).items()]
        self._exits_list.set_item_list(exits_items)

        counts = {}
        for it in data.get("items", []):
            counts[it] = counts.get(it, 0) + 1
        items_display = []
        for it, cnt in sorted(counts.items(), key=lambda x: x[0].lower()):
            items_display.append(f"{it} | {cnt}" if cnt > 1 else it)
        self._items_list.set_item_list(items_display)

        actions_display = []
        for cmd, act in data.get("actions", {}).items():
            if isinstance(act, dict):
                text = act.get("text") or act.get("response", "")
                logic = " [logic]" if act.get("effects") or act.get("conditions") else ""
                actions_display.append(f"{cmd} -> {text}{logic}")
            else:
                actions_display.append(f"{cmd} -> {str(act)}")
        self._actions_list.set_item_list(actions_display)

    # ── modal helpers ──

    def _show_msg(self, title, text):
        self._modal = MsgBox(self.manager, title, text)

    def _show_confirm(self, title, text, callback):
        self._modal = ConfirmBox(self.manager, title, text)
        self._modal_callback = callback

    def _show_input(self, title, prompt, callback, initial=""):
        self._modal = InputBox(self.manager, title, prompt, initial)
        self._modal_callback = callback

    def _check_modal(self):
        if self._modal and self._modal.done:
            cb = self._modal_callback
            result = self._modal.result
            self._modal = None
            self._modal_callback = None
            if cb:
                cb(result)

    # ── room CRUD ──

    def _add_room(self):
        def cb(name):
            if not name or not name.strip():
                return
            name = name.strip()
            if name in self.world.get("rooms", {}):
                self._show_msg("Error", "Room already exists.")
                return
            self.world.setdefault("rooms", {})[name] = {"description": "", "exits": {}, "items": [], "actions": {}}
            self.current_room = name
            self._refresh_room_list()
            self._load_room_to_editor(name)
            self._save_world()
        self._show_input("Add Room", "Room name:", cb)

    def _rename_room(self):
        if not self.current_room:
            self._show_msg("Warning", "Select a room first.")
            return
        def cb(new_name):
            if not new_name or not new_name.strip() or new_name.strip() == self.current_room:
                return
            new_name = new_name.strip()
            if new_name in self.world.get("rooms", {}):
                self._show_msg("Error", "A room with that name already exists.")
                return
            data = self.world["rooms"].pop(self.current_room)
            self.world["rooms"][new_name] = data
            for r, rd in self.world["rooms"].items():
                for d, targ in list(rd.get("exits", {}).items()):
                    if targ == self.current_room:
                        rd["exits"][d] = new_name
            if self.world.get("start_room") == self.current_room:
                self.world["start_room"] = new_name
            self.current_room = new_name
            self._refresh_room_list()
            self._load_room_to_editor(new_name)
            self._save_world()
        self._show_input("Rename Room", "New name:", cb, self.current_room)

    def _delete_room(self):
        if not self.current_room:
            self._show_msg("Warning", "Select a room first.")
            return
        def cb(yes):
            if not yes:
                return
            self.world["rooms"].pop(self.current_room, None)
            for r, rd in self.world["rooms"].items():
                for d, targ in list(rd.get("exits", {}).items()):
                    if targ == self.current_room:
                        rd["exits"].pop(d, None)
            if self.world.get("start_room") == self.current_room:
                self.world["start_room"] = next(iter(self.world["rooms"]), None)
            self.current_room = None
            self._refresh_room_list()
            self._save_world()
        self._show_confirm("Delete", f"Delete room '{self.current_room}'?", cb)

    def _set_start_room(self):
        if not self.current_room:
            return
        self.world["start_room"] = self.current_room
        self._refresh_room_list()
        self._save_world()

    # ── exit CRUD ──

    def _add_exit(self):
        if not self.current_room:
            return
        dirn = self._exit_dir_entry.get_text().strip()
        target = self._exit_target_dd.selected_option[0] if hasattr(self._exit_target_dd, 'selected_option') else ""
        if isinstance(target, tuple):
            target = target[0]
        if not dirn or not target or target == "(none)":
            return
        room = self.world["rooms"].setdefault(self.current_room, {})
        room.setdefault("exits", {})[dirn] = target
        self._load_room_to_editor(self.current_room)
        self._save_world()

    def _remove_exit(self):
        if not self.current_room:
            return
        sel = self._exits_list.get_single_selection()
        if not sel:
            return
        if "->" in sel:
            dirn = sel.split("->", 1)[0].strip()
            self.world["rooms"][self.current_room].get("exits", {}).pop(dirn, None)
        self._load_room_to_editor(self.current_room)
        self._save_world()

    # ── item CRUD ──

    def _add_item(self):
        if not self.current_room:
            return
        name = self._item_entry.get_text().strip()
        if not name:
            return
        try:
            cnt = int(self._item_count_entry.get_text().strip())
        except Exception:
            cnt = 1
        if cnt <= 0:
            cnt = 1
        items = self.world["rooms"][self.current_room].setdefault("items", [])
        for _ in range(cnt):
            items.append(name)
        self._item_entry.set_text("")
        self._item_count_entry.set_text("1")
        self._load_room_to_editor(self.current_room)
        self._refresh_inventory_views()

    def _remove_item(self):
        if not self.current_room:
            return
        sel = self._items_list.get_single_selection()
        if not sel:
            return
        item_name = sel.split(" | ")[0].strip()
        room_items = self.world["rooms"][self.current_room].get("items", [])
        if item_name in room_items:
            room_items.remove(item_name)
        self._load_room_to_editor(self.current_room)
        self._refresh_inventory_views()

    # ── action CRUD ──

    def _add_action(self):
        if not self.current_room:
            return
        cmd = self._act_cmd_entry.get_text().strip()
        if not cmd:
            self._show_msg("Error", "Action command required.")
            return
        resp = self._act_resp_entry.get_text().strip()
        try:
            effects = json.loads(self._act_effects_entry.get_text()) if self._act_effects_entry.get_text().strip() else {}
        except Exception as e:
            self._show_msg("Error", f"Invalid effects JSON: {e}")
            return
        try:
            conds = json.loads(self._act_conds_entry.get_text()) if self._act_conds_entry.get_text().strip() else {}
        except Exception as e:
            self._show_msg("Error", f"Invalid conditions JSON: {e}")
            return
        obj = {"text": resp}
        if effects:
            obj["effects"] = effects
        if conds:
            obj["conditions"] = conds
        self.world["rooms"].setdefault(self.current_room, {}).setdefault("actions", {})[cmd] = obj
        self._load_room_to_editor(self.current_room)
        self._save_world()

    def _remove_action(self):
        if not self.current_room:
            return
        sel = self._actions_list.get_single_selection()
        if not sel:
            return
        cmd = sel.split("->", 1)[0].strip() if "->" in sel else sel.strip()
        self.world["rooms"].setdefault(self.current_room, {}).get("actions", {}).pop(cmd, None)
        self._load_room_to_editor(self.current_room)
        self._save_world()

    def _on_action_select(self):
        if not self.current_room:
            return
        sel = self._actions_list.get_single_selection()
        if not sel:
            return
        cmd = sel.split("->", 1)[0].strip() if "->" in sel else sel.strip()
        act = self.world["rooms"].get(self.current_room, {}).get("actions", {}).get(cmd, {})
        self._act_cmd_entry.set_text(cmd)
        self._act_resp_entry.set_text(act.get("text") or act.get("response", ""))
        self._act_effects_entry.set_text(json.dumps(act.get("effects", {})) if act.get("effects") else "")
        self._act_conds_entry.set_text(json.dumps(act.get("conditions", {})) if act.get("conditions") else "")

    # ── global commands ──

    def _gcmd_clear(self):
        for entry in (self._gcmd_name_entry, self._gcmd_text_entry,
                      self._gcmd_inv_add_entry, self._gcmd_inv_rem_entry,
                      self._gcmd_state_entry, self._gcmd_stats_entry):
            entry.set_text("")

    def _gcmd_edit(self):
        sel = self._gcmd_list.get_single_selection()
        if not sel:
            return
        cmd = self.world.get("global_commands", {}).get(sel, {})
        self._gcmd_name_entry.set_text(sel)
        self._gcmd_text_entry.set_text(cmd.get("text") or cmd.get("response", ""))
        effects = cmd.get("effects", {})
        self._gcmd_inv_add_entry.set_text(",".join(effects.get("inventory_add", [])))
        self._gcmd_inv_rem_entry.set_text(",".join(effects.get("inventory_remove", [])))
        self._gcmd_state_entry.set_text(json.dumps(effects.get("state", {})))
        self._gcmd_stats_entry.set_text(json.dumps(effects.get("stats", {})))

    def _gcmd_delete(self):
        sel = self._gcmd_list.get_single_selection()
        if not sel:
            return
        def cb(yes):
            if not yes:
                return
            self.world.get("global_commands", {}).pop(sel, None)
            self._refresh_global_commands()
        self._show_confirm("Delete", f"Delete global command '{sel}'?", cb)

    def _gcmd_save(self):
        name = self._gcmd_name_entry.get_text().strip()
        if not name:
            self._show_msg("Error", "Command name required.")
            return
        text = self._gcmd_text_entry.get_text().strip()
        inv_add = [s.strip() for s in self._gcmd_inv_add_entry.get_text().split(",") if s.strip()]
        inv_rem = [s.strip() for s in self._gcmd_inv_rem_entry.get_text().split(",") if s.strip()]
        try:
            state = json.loads(self._gcmd_state_entry.get_text()) if self._gcmd_state_entry.get_text().strip() else {}
        except Exception as e:
            self._show_msg("Error", f"Invalid state JSON: {e}")
            return
        stats_raw = self._gcmd_stats_entry.get_text().strip()
        stats = {}
        if stats_raw:
            try:
                if stats_raw.startswith("{") and stats_raw.endswith("}"):
                    stats = json.loads(stats_raw)
                else:
                    for part in stats_raw.split(","):
                        if ":" in part:
                            k, v = part.split(":", 1)
                            stats[k.strip()] = v.strip()
            except Exception as e:
                self._show_msg("Error", f"Invalid stats: {e}")
                return
        obj = {"text": text, "effects": {"inventory_add": inv_add, "inventory_remove": inv_rem, "state": state, "stats": stats}}
        self.world.setdefault("global_commands", {})[name] = obj
        self._refresh_global_commands()

    # ── stats ──

    def _stat_add(self):
        k = self._stat_name_entry.get_text().strip()
        if not k:
            return
        v = self._stat_value_entry.get_text().strip()
        try:
            vnum = int(v)
        except Exception:
            try:
                vnum = float(v)
            except Exception:
                vnum = v
        self.world.setdefault("default_stats", {})[k] = vnum
        self._refresh_stats_list()

    def _stat_remove(self):
        sel = self._stats_list.get_single_selection()
        if not sel:
            return
        k = sel.split("=", 1)[0].strip()
        self.world.get("default_stats", {}).pop(k, None)
        self._refresh_stats_list()

    # ── player start inventory ──

    def _ps_add(self):
        name = self._ps_entry.get_text().strip()
        if not name:
            sel = self._world_items_list.get_single_selection()
            if sel:
                name = sel
        if not name:
            return
        try:
            count = int(self._ps_count_entry.get_text().strip())
        except Exception:
            count = 1
        if count <= 0:
            count = 1
        self.world.setdefault("default_inventory", {})
        self.world["default_inventory"][name] = self.world["default_inventory"].get(name, 0) + count
        self._ps_entry.set_text("")
        self._ps_count_entry.set_text("1")
        self._refresh_inventory_views()

    def _ps_remove(self):
        sel = self._player_start_list.get_single_selection()
        if not sel:
            return
        name = sel.split(" | ", 1)[0].strip() if " | " in sel else sel.strip()
        self.world.setdefault("default_inventory", {})
        self.world["default_inventory"].pop(name, None)
        self._refresh_inventory_views()

    # ── save / preview room ──

    def _save_room(self):
        name = self._name_entry.get_text().strip()
        if not name:
            self._show_msg("Error", "Room name required.")
            return
        self.world.setdefault("rooms", {})
        if self.current_room and name != self.current_room:
            if name in self.world["rooms"]:
                self._show_msg("Error", "A room with that name already exists.")
                return
            data = self.world["rooms"].pop(self.current_room)
            self.world["rooms"][name] = data
            for r, rd in self.world["rooms"].items():
                for d, targ in list(rd.get("exits", {}).items()):
                    if targ == self.current_room:
                        rd["exits"][d] = name
            if self.world.get("start_room") == self.current_room:
                self.world["start_room"] = name
            self.current_room = name

        room = self.world["rooms"].setdefault(name, {"description": "", "exits": {}, "items": [], "actions": {}})
        room["description"] = self._desc_entry.get_text().strip()
        ok = self._save_world()
        if ok:
            self._show_msg("Saved", f"Room '{name}' saved.")
        self._refresh_room_list()
        self._load_room_to_editor(name)

    def _preview_room(self):
        name = self._name_entry.get_text().strip() or "&lt;unnamed&gt;"
        desc = self._desc_entry.get_text().strip()
        lines = [f"<b>{name}</b>", desc]
        # items from current editor state
        items = []
        for rdata in [self.world["rooms"].get(self.current_room, {})]:
            counts = {}
            for it in rdata.get("items", []):
                counts[it] = counts.get(it, 0) + 1
            for it, cnt in sorted(counts.items()):
                items.append(f"{it} x{cnt}" if cnt > 1 else it)
        if items:
            lines.append(f"You see: {', '.join(items)}")
        exits = list(self.world["rooms"].get(self.current_room, {}).get("exits", {}).keys())
        if exits:
            lines.append(f"Exits: {', '.join(exits)}")
        self._preview_box.set_text("<br>".join(lines))

    # ── event handling ──

    def handle_event(self, event):
        if self._modal:
            self._modal.handle_event(event)
            self._check_modal()
            return

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            ui = event.ui_element
            # Tab switching
            if ui == self._tab_rooms_btn:
                self._show_tab("rooms")
            elif ui == self._tab_cmds_btn:
                self._show_tab("commands")
            # Room tab buttons
            elif ui == self._btn_add_room:
                self._add_room()
            elif ui == self._btn_rename_room:
                self._rename_room()
            elif ui == self._btn_delete_room:
                self._delete_room()
            elif ui == self._btn_set_start:
                self._set_start_room()
            elif ui == self._btn_load:
                self._show_input("Load World", "File path:", self._on_load_path, self.world_path)
            elif ui == self._btn_save:
                if self._save_world():
                    self._show_msg("Saved", "World saved successfully!")
            elif ui == self._btn_add_exit:
                self._add_exit()
            elif ui == self._btn_rem_exit:
                self._remove_exit()
            elif ui == self._btn_add_item:
                self._add_item()
            elif ui == self._btn_rem_item:
                self._remove_item()
            elif ui == self._btn_add_action:
                self._add_action()
            elif ui == self._btn_rem_action:
                self._remove_action()
            elif ui == self._btn_save_room:
                self._save_room()
            elif ui == self._btn_preview:
                self._preview_room()
            # Commands tab
            elif ui == self._btn_gcmd_add:
                self._gcmd_clear()
            elif ui == self._btn_gcmd_edit:
                self._gcmd_edit()
            elif ui == self._btn_gcmd_del:
                self._gcmd_delete()
            elif ui == self._btn_gcmd_save:
                self._gcmd_save()
            elif ui == self._btn_stat_add:
                self._stat_add()
            elif ui == self._btn_stat_rem:
                self._stat_remove()
            elif ui == self._btn_ps_add:
                self._ps_add()
            elif ui == self._btn_ps_rem:
                self._ps_remove()

        elif event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
            ui = event.ui_element
            if ui == self._room_list:
                text = event.text
                name = text.split(" (start)")[0]
                self.current_room = name
                self._load_room_to_editor(name)
            elif ui == self._actions_list:
                self._on_action_select()

    def _on_load_path(self, path):
        if not path:
            return
        path = path.strip()
        if not os.path.exists(path):
            self._show_msg("Error", f"File not found: {path}")
            return
        if self._load_world(path):
            self._show_msg("Loaded", f"World loaded from {os.path.basename(path)}")

    # ── main loop ──

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                self.manager.process_events(event)
                self.handle_event(event)

            self.manager.update(dt)
            
            # Update modal animation
            if self._modal:
                self._modal.update(dt)

            self.screen.fill(BG)
            self.manager.draw_ui(self.screen)
            pygame.display.flip()

        pygame.quit()


def main():
    editor = WorldEditor()
    editor.run()


if __name__ == "__main__":
    main()
