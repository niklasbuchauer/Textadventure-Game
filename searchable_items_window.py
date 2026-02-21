"""
Searchable Items Window (Pygame)
================================
Debug tool that displays all items in the game in a searchable, categorized
overlay.  Items are grouped by type and can be filtered by name or ID.
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
    "separator":    "#2a2a2a",
    "category":     "#ffaa00",
    "how_to_get":   "#88ffaa",
    # Rarity colours
    "common":       "#aaaaaa",
    "uncommon":     "#44ff44",
    "rare":         "#4488ff",
    "epic":         "#cc44ff",
    "legendary":    "#ffaa00",
    "mythic":       "#ff4444",
}

RARITY_ORDER = ["common", "uncommon", "rare", "epic", "legendary", "mythic"]

CATEGORY_ORDER = [
    "Equipment", "Crafted", "Consumable", "Material",
    "Dungeon Loot", "World Item", "Quest Item", "Other",
]

CATEGORY_ICONS = {
    "Equipment":    "[EQ]",
    "Crafted":      "[CR]",
    "Consumable":   "[CS]",
    "Material":     "[MT]",
    "Dungeon Loot": "[DG]",
    "World Item":   "[WD]",
    "Quest Item":   "[QT]",
    "Other":        "[??]",
}


def _esc(t):
    return html_module.escape(str(t))


def _rarity_color(rarity):
    return COLORS.get(rarity, COLORS["text"])


def _rarity_icon(rarity):
    return {
        "common":    "[C]",
        "uncommon":  "[U]",
        "rare":      "[R]",
        "epic":      "[E]",
        "legendary": "[L]",
        "mythic":    "[M]",
    }.get(rarity, "[C]")


# ── Item registry builder ──────────────────────────────────────────────────
def _build_item_registry():
    """Aggregate all items from every source into a master registry."""
    registry = {}
    master_sources = {}

    def _add(item_id, source):
        if not item_id or not isinstance(item_id, str) or not item_id.strip():
            return
        master_sources.setdefault(item_id, set()).add(source)

    # 1) Equipment database
    EQUIPMENT_DATABASE = {}
    try:
        from equipment_system import EQUIPMENT_DATABASE as _EQ
        EQUIPMENT_DATABASE = _EQ
        for k in EQUIPMENT_DATABASE:
            _add(k, "equipment")
    except Exception:
        pass

    # 2) Shop item database
    SHOP_DATABASE = {}
    try:
        from shop_system import ITEM_DATABASE as _SHOP
        SHOP_DATABASE = _SHOP
        for k in SHOP_DATABASE:
            _add(k, "shop")
    except Exception:
        pass

    # 3) Item effects (usable / consumable items)
    ITEM_EFFECTS = {}
    try:
        from item_effects import ITEM_EFFECTS as _IE
        ITEM_EFFECTS = _IE
        for k in ITEM_EFFECTS:
            _add(k, "item_effects")
    except Exception:
        pass
    try:
        from item_effects import FISHING_LOOT as _FL
        for entry in _FL:
            if isinstance(entry, (list, tuple)) and len(entry) >= 1:
                _add(str(entry[0]), "fishing")
            elif isinstance(entry, dict) and "item" in entry:
                _add(entry["item"], "fishing")
    except Exception:
        pass

    # 4) Crafting recipes
    RECIPE_DATABASE = {}
    try:
        from crafting_system import RECIPE_DATABASE as _REC, STATION_NAMES
        RECIPE_DATABASE = _REC
        for recipe_id, recipe in RECIPE_DATABASE.items():
            result_tuple = recipe.get("result")
            out_id = result_tuple[0] if isinstance(result_tuple, tuple) else recipe.get("output", recipe_id)
            _add(out_id, "crafting_output")
            for ingr in recipe.get("ingredients", {}):
                _add(ingr, "crafting_ingredient")
    except Exception:
        STATION_NAMES = {}

    # 5) Combat loot drops
    ENEMY_DATABASE = {}
    BOSS_DATABASE = {}
    MINI_BOSS_DATABASE = {}
    try:
        from combat_system import ENEMY_DATABASE as _EN, BOSS_DATABASE as _BO, MINI_BOSS_DATABASE as _MB
        ENEMY_DATABASE, BOSS_DATABASE, MINI_BOSS_DATABASE = _EN, _BO, _MB
        for db, label in [(_EN, "enemy_drop"), (_BO, "boss_drop"), (_MB, "mini_boss_drop")]:
            for edata in db.values():
                for drop in edata.get("loot", []):
                    if isinstance(drop, dict):
                        _add(drop.get("item", ""), label)
                    elif isinstance(drop, (list, tuple)) and len(drop) >= 1:
                        _add(str(drop[0]), label)
    except Exception:
        pass

    # 6) World.json items
    try:
        import json, os
        world_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "world.json")
        if os.path.exists(world_path):
            with open(world_path, "r", encoding="utf-8") as f:
                world = json.load(f)
            rooms = world.get("rooms", {})
            room_iter = rooms.values() if isinstance(rooms, dict) else rooms
            for room_data in room_iter:
                for it in room_data.get("items", []):
                    _add(str(it), "world")
    except Exception:
        pass

    # 7) Fixed dungeon items
    try:
        import json, os, glob
        fd_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixed_dungeons")
        if os.path.isdir(fd_dir):
            for fpath in glob.glob(os.path.join(fd_dir, "*.json")):
                dname = os.path.splitext(os.path.basename(fpath))[0]
                with open(fpath, "r", encoding="utf-8") as f:
                    ddata = json.load(f)
                floors = ddata.get("floors", {})
                floor_iter = floors.values() if isinstance(floors, dict) else floors
                for floor in floor_iter:
                    rooms = floor.get("rooms", {})
                    room_iter = rooms.values() if isinstance(rooms, dict) else rooms
                    for room in room_iter:
                        ri = room.get("items", {})
                        for it in (ri.keys() if isinstance(ri, dict) else ri):
                            _add(str(it), f"dungeon:{dname}")
                        for chest in room.get("chests", []):
                            ci = chest.get("items", {})
                            for it in (ci.keys() if isinstance(ci, dict) else ci):
                                _add(str(it), f"dungeon:{dname}")
                            cc = chest.get("contents", {}).get("items", {})
                            for it in (cc.keys() if isinstance(cc, dict) else cc):
                                _add(str(it), f"dungeon:{dname}")
    except Exception:
        pass

    # 8) Quest rewards / objectives
    try:
        from quest_system import QUEST_DATABASE
        for qid, qdef in QUEST_DATABASE.items():
            qname = qdef.get("name", qid)
            for it in qdef.get("rewards", {}).get("items", {}):
                _add(it, f"quest_reward:{qname}")
            for obj in qdef.get("objectives", []):
                if obj.get("type") == "collect":
                    _add(obj.get("item", ""), f"quest_objective:{qname}")
    except Exception:
        pass

    master_sources.pop("", None)

    # ── Build full registry entries ───────────────────────────────────
    recipe_by_output = {}
    for rid, rec in RECIPE_DATABASE.items():
        result_tuple = rec.get("result")
        out_id = result_tuple[0] if isinstance(result_tuple, tuple) else rec.get("output", rid)
        recipe_by_output[out_id] = rec

    enemy_drop_map = {}
    for db, db_type in [(ENEMY_DATABASE, "Enemy"), (BOSS_DATABASE, "Boss"), (MINI_BOSS_DATABASE, "Mini-Boss")]:
        for eid, edata in db.items():
            ename = edata.get("name", eid.replace("_", " ").title())
            for drop in edata.get("loot", []):
                did = ""
                if isinstance(drop, dict):
                    did = drop.get("item", "")
                elif isinstance(drop, (list, tuple)) and len(drop) >= 1:
                    did = str(drop[0])
                if did:
                    enemy_drop_map.setdefault(did, []).append(f"{db_type}: {ename}")

    for item_id, sources in master_sources.items():
        name = item_id.replace("_", " ").title()
        description = ""
        rarity = "common"
        category = "Other"
        sub_category = ""
        how_to_get_parts = []

        # Equipment
        if item_id in EQUIPMENT_DATABASE:
            edata = EQUIPMENT_DATABASE[item_id]
            name = edata.get("name", name)
            description = edata.get("description", "")
            rarity = edata.get("rarity", "common")
            slot = edata.get("slot", "weapon")
            category = "Equipment"
            sub_category = slot.title()
            stats = edata.get("stats", {})
            if stats:
                description += "\nStats: " + ", ".join(f"+{v} {k}" for k, v in stats.items())
            src = edata.get("source", "")
            if src:
                how_to_get_parts.append(f"Source: {src}")

        # Shop
        if item_id in SHOP_DATABASE:
            sdata = SHOP_DATABASE[item_id]
            if not description:
                description = sdata.get("desc", sdata.get("description", ""))
            if name == item_id.replace("_", " ").title():
                name = sdata.get("name", name)
            price = sdata.get("price", sdata.get("value", 0))
            if price:
                how_to_get_parts.append(f"Buy from shop for {price} gold")

        # Item effects (consumables)
        if item_id in ITEM_EFFECTS:
            efdata = ITEM_EFFECTS[item_id]
            if not description:
                description = efdata.get("description", "")
            if category == "Other":
                category = "Consumable"
            effect = efdata.get("effect", "")
            val = efdata.get("value", 0)
            if effect == "heal":
                description = (description or "") + f"\nEffect: Restores {val} HP"
            elif effect in ("buff_attack", "buff_defense", "buff_all"):
                dur = efdata.get("duration", 5)
                description = (description or "") + f"\nEffect: +{val} for {dur} turns"

        # Crafting
        if item_id in recipe_by_output:
            rec = recipe_by_output[item_id]
            ingr = rec.get("ingredients", {})
            station = rec.get("station", "any")
            ingr_str = ", ".join(f"{v}x {k.replace('_',' ')}" for k, v in ingr.items())
            how_to_get_parts.append(f"Craft at {station.replace('_',' ').title()}: {ingr_str}")
            if category == "Other":
                category = "Crafted"

        # Enemy/boss drops
        if item_id in enemy_drop_map:
            drops = enemy_drop_map[item_id][:3]
            how_to_get_parts.append("Drop from: " + ", ".join(drops))
            if category == "Other":
                category = "Dungeon Loot"

        # Quest
        quest_sources = [s for s in sources if s.startswith("quest")]
        if quest_sources:
            qnames = []
            for qs in quest_sources:
                parts = qs.split(":", 1)
                if len(parts) > 1:
                    qnames.append(parts[1])
            if qnames:
                how_to_get_parts.append("Quest: " + ", ".join(qnames))
                if category == "Other":
                    category = "Quest Item"

        # World / dungeon environment
        dungeon_sources = [s for s in sources if s.startswith("dungeon:")]
        if dungeon_sources:
            dnames = [s.split(":", 1)[1].replace("_", " ").title() for s in dungeon_sources]
            how_to_get_parts.append("Found in: " + ", ".join(dnames))
            if category == "Other":
                category = "Dungeon Loot"
        if "world" in sources and category == "Other":
            how_to_get_parts.append("Found in world")
            category = "World Item"

        if "fishing" in sources:
            how_to_get_parts.append("Obtained by fishing")
            if category == "Other":
                category = "Consumable"

        if "crafting_ingredient" in sources and "crafting_output" not in sources and category == "Other":
            category = "Material"

        how_to_get = "\n".join(how_to_get_parts) if how_to_get_parts else "Unknown"

        registry[item_id] = {
            "name": name,
            "id": item_id,
            "category": category,
            "sub_category": sub_category,
            "description": description.strip() if description else "No description available.",
            "how_to_get": how_to_get,
            "rarity": rarity,
            "sources": sorted(sources),
        }

    return registry


# ─────────────────────────────────────────────────────────────────────────────
class SearchableItemsWindow:
    """Searchable item database overlay using pygame_gui."""

    def __init__(self, app, game_engine=None):
        self.app = app
        self.manager = app.manager
        self.game_engine = game_engine
        self._registry = {}
        self._filtered_ids = []
        self._last_query = ""
        self.window = None
        self._search = None
        self._list = None
        self._detail = None
        self._status = None

    # ── lifecycle ─────────────────────────────────────────────────────────────
    def create_window(self):
        """Create and show the window (lazy)."""
        if self.window and self.window.alive():
            return

        W, H = self.app.width, self.app.height
        ww, wh = 1020, 680
        self.window = UIWindow(
            rect=pygame.Rect((W - ww) // 2, (H - wh) // 2, ww, wh),
            manager=self.manager,
            window_display_title="Item Database — Debug Search",
            resizable=True,
        )
        iw = ww - 60

        # Search bar
        self._search = UITextEntryLine(
            relative_rect=pygame.Rect(10, 10, iw - 120, 28),
            manager=self.manager, container=self.window,
            placeholder_text="Search items...",
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
            html_text='<font color="#666666">Select an item from the list to view details.</font>',
            relative_rect=pygame.Rect(lw + 20, 46, iw - lw - 20, wh - 130),
            manager=self.manager, container=self.window,
        )

        self._load_registry()

    def close_window(self):
        if self.window and self.window.alive():
            self.window.kill()
        self.window = None

    def is_open(self):
        return bool(self.window and self.window.alive())

    def handle_event(self, event):
        if not self.is_open():
            return
        if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
            if event.ui_element == self._search:
                self._apply_filter(self._search.get_text().strip().lower())
        elif event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
            if event.ui_element == self._list:
                self._on_item_selected(event.text)

    # ── data loading ──────────────────────────────────────────────────────────
    def _load_registry(self):
        self._registry = _build_item_registry()
        self._apply_filter("")

    # ── filtering ─────────────────────────────────────────────────────────────
    def _apply_filter(self, query):
        self._last_query = query

        if query:
            matches = {
                iid: data for iid, data in self._registry.items()
                if query in iid.lower() or query in data["name"].lower()
            }
        else:
            matches = self._registry

        # Group by category
        categories = {}
        for iid, data in matches.items():
            cat = data["category"]
            categories.setdefault(cat, []).append((iid, data))
        for cat in categories:
            categories[cat].sort(key=lambda x: x[1]["name"].lower())

        items_for_list = []
        self._filtered_ids = []
        total = 0

        for cat in CATEGORY_ORDER:
            if cat not in categories:
                continue
            cat_items = categories[cat]
            icon = CATEGORY_ICONS.get(cat, "•")

            # Category header
            header_label = f"{icon}  {cat.upper()}  ({len(cat_items)})"
            items_for_list.append(header_label)
            self._filtered_ids.append(None)

            for iid, data in cat_items:
                rarity = data.get("rarity", "common")
                ri = _rarity_icon(rarity)
                display = f"  {ri} {data['name']}"
                items_for_list.append(display)
                self._filtered_ids.append(iid)
                total += 1

        # Any remaining categories not in CATEGORY_ORDER
        for cat, cat_items in categories.items():
            if cat in CATEGORY_ORDER:
                continue
            icon = CATEGORY_ICONS.get(cat, "•")
            header_label = f"{icon}  {cat.upper()}  ({len(cat_items)})"
            items_for_list.append(header_label)
            self._filtered_ids.append(None)
            for iid, data in cat_items:
                rarity = data.get("rarity", "common")
                ri = _rarity_icon(rarity)
                display = f"  {ri} {data['name']}"
                items_for_list.append(display)
                self._filtered_ids.append(iid)
                total += 1

        self._list.set_item_list(items_for_list)
        if total == 0 and query:
            self._status.set_text("No items")
        else:
            self._status.set_text(f"{total} items")

        # Build direct text→id lookup for selection matching
        self._text_to_iid = {}
        for i, label in enumerate(items_for_list):
            iid = self._filtered_ids[i]
            if iid is not None:
                self._text_to_iid[label] = iid

    # ── selection ─────────────────────────────────────────────────────────────────────
    def _on_item_selected(self, text):
        iid = self._text_to_iid.get(text)
        if iid:
            data = self._registry.get(iid)
            if data:
                self._show_detail(iid, data)

    # ── detail rendering ──────────────────────────────────────────────────────
    def _show_detail(self, item_id, data):
        lines = []
        key = COLORS["detail_key"]
        val = COLORS["detail_val"]
        dim = COLORS["dim"]
        bright = COLORS["bright"]
        sep = COLORS["separator"]

        rarity = data.get("rarity", "common")
        rarity_col = _rarity_color(rarity)
        ri = _rarity_icon(rarity)

        # Item name
        lines.append(f'<font color="{bright}" size="4"><b>{_esc(data["name"])}</b></font><br>')

        # Rarity + category
        cat = data["category"]
        sub = data.get("sub_category", "")
        cat_str = _esc(cat)
        if sub:
            cat_str += f" › {_esc(sub)}"
        lines.append(f'<font color="{rarity_col}">{ri} {rarity.upper()}</font>')
        lines.append(f'  <font color="{val}">{cat_str}</font><br>')
        lines.append(f'<font color="{sep}">{"─" * 44}</font><br><br>')

        # ID
        lines.append(f'<font color="{key}"><b>ID</b></font><br>')
        lines.append(f'<font color="{val}">{_esc(item_id)}</font><br><br>')

        # Description
        lines.append(f'<font color="{key}"><b>DESCRIPTION</b></font><br>')
        desc = data.get("description") or "No description available."
        for ln in desc.split("\n"):
            lines.append(f'<font color="{val}">{_esc(ln)}</font><br>')
        lines.append('<br>')

        # How to get
        lines.append(f'<font color="{key}"><b>HOW TO GET</b></font><br>')
        how = data.get("how_to_get") or "Unknown"
        for ln in how.split("\n"):
            lines.append(f'<font color="{COLORS["how_to_get"]}">{_esc(ln)}</font><br>')
        lines.append('<br>')

        # Sources
        sources = data.get("sources", [])
        if sources:
            lines.append(f'<font color="{key}"><b>SOURCES</b></font><br>')
            lines.append(f'<font color="{val}">{_esc(", ".join(sources))}</font><br><br>')

        # Spawn hint
        lines.append(f'<font color="{sep}">{"─" * 44}</font><br>')
        lines.append(f'<font color="{val}">To add: debug spawn item {_esc(item_id)}</font><br>')

        self._detail.set_text("".join(lines))
