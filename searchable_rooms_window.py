"""
Searchable Rooms Window (Pygame)
================================
Browse every game room/area in a searchable, categorised overlay.
Uses pygame_gui UIWindow with UISelectionList + UITextBox.
"""

import pygame
import pygame_gui
from pygame_gui.elements import (
    UIButton, UILabel, UITextBox, UITextEntryLine,
    UIWindow, UISelectionList, UIPanel,
)
import textwrap
import html as html_module

# ── Colour palette ──────────────────────────────────────────────────────────
COLORS = {
    "header":       "#00ccff",
    "text":         "#cccccc",
    "dim":          "#666666",
    "bright":       "#ffffff",
    "detail_key":   "#00ccff",
    "detail_val":   "#cccccc",
    "exit_boat":    "#00ffcc",
    "exit_dir":     "#88aacc",
    "npc":          "#ffcc44",
    "item":         "#88ff88",
    "separator":    "#2a2a2a",
    "category":     "#ffaa00",
    "area_mainland":  "#88ccff",
    "area_sunstone":  "#ffdd88",
    "area_emerald":   "#44ff88",
    "area_stormbreak":"#88bbff",
    "area_cinderforge":"#ff8844",
    "area_dreadmist": "#cc88ff",
    "area_wyrmscale": "#ff4444",
    "area_abyssal":   "#cc44ff",
    "area_dungeon":   "#ff8844",
    "area_other":     "#888888",
}

# Ordered region list: (display_name, id_prefix_list, colour_key)
REGIONS = [
    ("MAINLAND",          ["port_haven", "blackwood", "harbor", "grand_", "bramble",
                           "swamp", "dark_tor", "hermit", "mine", "river", "cave",
                           "village", "town", "market", "tavern", "shrine", "forest",
                           "road", "crossroads", "gatehouse"],
                           "area_mainland"),
    ("SUNSTONE ATOLL",    ["sunstone"],   "area_sunstone"),
    ("EMERALD ISLE",      ["emerald"],    "area_emerald"),
    ("STORMBREAK REEF",   ["stormbreak"], "area_stormbreak"),
    ("CINDERFORGE ISLE",  ["cinder"],     "area_cinderforge"),
    ("DREADMIST ISLE",    ["dreadmist"],  "area_dreadmist"),
    ("WYRMSCALE ISLE",    ["wyrm"],       "area_wyrmscale"),
    ("THE ABYSSAL REACH", ["abyssal"],    "area_abyssal"),
    ("DUNGEONS",          ["dungeon_", "crystal_", "iron_hall", "shadow_", "sunken_",
                           "frozen_", "molten_", "tempest_", "verdant_", "void_",
                           "wyrms_", "halls_"],
                           "area_dungeon"),
    ("OTHER",             [],             "area_other"),
]
REGION_ORDER = [r[0] for r in REGIONS]


def _esc(t):
    """HTML-escape helper."""
    return html_module.escape(str(t))


def _region_for(room_id: str):
    rid = room_id.lower()
    for name, prefixes, colour in REGIONS[:-1]:
        for p in prefixes:
            if rid.startswith(p) or p in rid:
                return name, colour
    return REGIONS[-1][0], REGIONS[-1][2]


def _build_room_registry(engine):
    """Build dict { room_id -> RoomInfo } from engine.rooms."""
    registry = {}
    try:
        raw_rooms = engine.rooms
    except AttributeError:
        return registry

    for rid, rdata in raw_rooms.items():
        if hasattr(rdata, "name"):
            name        = rdata.name or rid
            description = getattr(rdata, "description", "")
            loc_type    = getattr(rdata, "location_type", "")
            exits       = dict(getattr(rdata, "exits", {}))
            npcs        = list(getattr(rdata, "npcs", []) or [])
            items       = getattr(rdata, "items", {})
            coordinates = getattr(rdata, "coordinates", None)
        else:
            name        = rdata.get("name", rid)
            description = rdata.get("description", "")
            loc_type    = rdata.get("location_type", "")
            exits       = dict(rdata.get("exits", {}))
            npcs        = list(rdata.get("npcs", []) or [])
            items       = rdata.get("items", {})
            coordinates = rdata.get("coordinates", None)

        region, colour = _region_for(rid)
        registry[rid] = {
            "name":        name,
            "id":          rid,
            "description": description,
            "loc_type":    loc_type,
            "exits":       exits,
            "npcs":        npcs,
            "items":       items,
            "coordinates": coordinates,
            "region":      region,
            "colour":      colour,
        }
    return registry


class SearchableRoomsWindow:
    """Searchable room browser overlay using pygame_gui."""

    def __init__(self, app, engine):
        self.app = app
        self.manager = app.manager
        self._engine = engine
        self._registry = {}
        self._filtered_ids = []
        self._last_query = ""

        W, H = app.width, app.height
        ww, wh = 1020, 680
        self.window = UIWindow(
            rect=pygame.Rect((W - ww) // 2, (H - wh) // 2, ww, wh),
            manager=self.manager,
            window_display_title="Room & Area Browser",
            resizable=True,
        )
        iw = ww - 60  # inner width accounting for UIWindow chrome

        # Search bar
        self._search = UITextEntryLine(
            relative_rect=pygame.Rect(10, 10, iw - 120, 28),
            manager=self.manager, container=self.window,
            placeholder_text="Search rooms...",
        )
        self._status = UILabel(
            relative_rect=pygame.Rect(iw - 100, 12, 100, 24),
            text="Loading...", manager=self.manager, container=self.window,
        )

        # Left list (40% width)
        lw = int(iw * 0.40)
        self._list = UISelectionList(
            relative_rect=pygame.Rect(10, 46, lw, wh - 130),
            item_list=[], manager=self.manager, container=self.window,
        )

        # Right detail panel
        self._detail = UITextBox(
            html_text='<font color="#666666">Click a room to see details.</font>',
            relative_rect=pygame.Rect(lw + 20, 46, iw - lw - 20, wh - 130),
            manager=self.manager, container=self.window,
        )

        # Load data
        self._load_registry()

    # ── public API ────────────────────────────────────────────────────────────
    def is_open(self):
        return self.window.alive()

    def handle_event(self, event):
        if not self.window.alive():
            return
        if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
            if event.ui_element == self._search:
                self._apply_filter(self._search.get_text().strip().lower())
        elif event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
            if event.ui_element == self._list:
                self._on_room_selected(event.text)

    # ── data loading ──────────────────────────────────────────────────────────
    def _load_registry(self):
        self._registry = _build_room_registry(self._engine)
        self._apply_filter("")

    # ── filtering ─────────────────────────────────────────────────────────────
    def _apply_filter(self, query):
        self._last_query = query

        if query:
            matches = {
                rid: d for rid, d in self._registry.items()
                if query in rid.lower() or query in d["name"].lower()
                   or query in d["region"].lower()
                   or query in (d["description"] or "").lower()
            }
        else:
            matches = self._registry

        # Group by region
        regions: dict[str, list] = {}
        for rid, d in matches.items():
            regions.setdefault(d["region"], []).append((rid, d))
        for reg in regions:
            regions[reg].sort(key=lambda x: x[1]["name"].lower())

        items_for_list = []
        self._filtered_ids = []
        total = 0

        for region_name in REGION_ORDER:
            room_items = regions.get(region_name)
            if not room_items:
                continue
            # Region header
            header_text = f"── {region_name} ({len(room_items)}) ──"
            items_for_list.append(header_text)
            self._filtered_ids.append(None)

            for rid, d in room_items:
                loc = d["loc_type"]
                tag = f"[{loc[:3].upper()}]" if loc else "[   ]"
                has_boat = any(
                    isinstance(v, dict) and v.get("type") == "boat_travel"
                    for v in d["exits"].values()
                )
                boat_icon = " ⛵" if has_boat else ""
                label = f"  {tag} {d['name']}{boat_icon}"
                items_for_list.append(label)
                self._filtered_ids.append(rid)
                total += 1

        self._list.set_item_list(items_for_list)
        self._status.set_text(f"{total} rooms")

        # Build direct text→room_id lookup for selection matching
        self._text_to_rid = {}
        for i, label in enumerate(items_for_list):
            rid = self._filtered_ids[i]
            if rid is not None:
                self._text_to_rid[label] = rid

    # ── selection ─────────────────────────────────────────────────────────────
    def _on_room_selected(self, text):
        rid = self._text_to_rid.get(text)
        if rid is None:
            return
        d = self._registry.get(rid)
        if d:
            self._show_detail(rid, d)

    def _list_label_for(self, rid):
        """Reconstruct the list label for a room_id (for matching)."""
        d = self._registry.get(rid)
        if not d:
            return ""
        loc = d["loc_type"]
        tag = f"[{loc[:3].upper()}]" if loc else "[   ]"
        has_boat = any(
            isinstance(v, dict) and v.get("type") == "boat_travel"
            for v in d["exits"].values()
        )
        boat_icon = " ⛵" if has_boat else ""
        return f"  {tag} {d['name']}{boat_icon}"

    # ── detail rendering ──────────────────────────────────────────────────────
    def _show_detail(self, rid, d):
        lines = []
        key = COLORS["detail_key"]
        val = COLORS["detail_val"]
        dim = COLORS["dim"]
        bright = COLORS["bright"]
        region_color = COLORS.get(d["colour"], dim)

        # Room name
        lines.append(f'<font color="{bright}" size="4"><b>{_esc(d["name"])}</b></font><br>')
        lines.append(f'<font color="{dim}">{_esc(rid)}</font><br>')
        lines.append(f'<font color="{region_color}"><b>{_esc(d["region"])}</b></font><br>')
        lines.append(f'<font color="{COLORS["separator"]}">{"─" * 44}</font><br><br>')

        # Location type
        if d["loc_type"]:
            lines.append(f'<font color="{key}"><b>TYPE</b></font><br>')
            lines.append(f'<font color="{val}">{_esc(d["loc_type"])}</font><br><br>')

        # Coordinates
        if d["coordinates"]:
            cx, cy = d["coordinates"]
            lines.append(f'<font color="{key}"><b>COORDS</b></font><br>')
            lines.append(f'<font color="{val}">({cx}, {cy})</font><br><br>')

        # Description
        if d["description"]:
            lines.append(f'<font color="{key}"><b>DESCRIPTION</b></font><br>')
            for ln in textwrap.wrap(d["description"], width=52):
                lines.append(f'<font color="{val}">{_esc(ln)}</font><br>')
            lines.append('<br>')

        # Exits
        if d["exits"]:
            lines.append(f'<font color="{key}"><b>EXITS</b></font><br>')
            for exit_key, exit_val in d["exits"].items():
                if isinstance(exit_val, dict):
                    etype = exit_val.get("type", "")
                    target = exit_val.get("target", "?")
                    display = exit_val.get("display", "")
                    if etype == "boat_travel":
                        lines.append(
                            f'<font color="{COLORS["exit_boat"]}">⛵ {_esc(exit_key)} → {_esc(display or target)}</font><br>'
                        )
                    else:
                        lines.append(
                            f'<font color="{COLORS["exit_dir"]}">{_esc(exit_key)} → {_esc(target)}</font><br>'
                        )
                else:
                    lines.append(
                        f'<font color="{COLORS["exit_dir"]}">{_esc(exit_key)} → {_esc(exit_val)}</font><br>'
                    )
            lines.append('<br>')

        # NPCs
        if d["npcs"]:
            lines.append(f'<font color="{key}"><b>NPCS</b></font><br>')
            for npc in d["npcs"]:
                lines.append(f'<font color="{COLORS["npc"]}">• {_esc(npc)}</font><br>')
            lines.append('<br>')

        # Items
        items = d["items"]
        if items:
            lines.append(f'<font color="{key}"><b>ITEMS</b></font><br>')
            if isinstance(items, dict):
                for iid, info in items.items():
                    qty = info.get("quantity", 1) if isinstance(info, dict) else ""
                    qty_str = f" ×{qty}" if qty and qty != 1 else ""
                    lines.append(f'<font color="{COLORS["item"]}">• {_esc(iid)}{qty_str}</font><br>')
            elif isinstance(items, list):
                for iid in items:
                    lines.append(f'<font color="{COLORS["item"]}">• {_esc(iid)}</font><br>')

        self._detail.set_text("".join(lines))
