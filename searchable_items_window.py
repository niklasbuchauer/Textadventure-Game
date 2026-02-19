"""
Searchable Items Window
=======================
Debug tool that displays all items in the game in a searchable, categorized window.
Items are grouped by type and can be filtered by name or ID in real-time.
"""

import tkinter as tk
from tkinter import ttk


# ── Color palette (matches the dark game theme) ──────────────────────────────
COLORS = {
    "bg":           "#0d0d0d",
    "bg_light":     "#161616",
    "bg_panel":     "#111111",
    "border":       "#2a2a2a",
    "header_fg":    "#00ccff",
    "text":         "#cccccc",
    "text_dim":     "#666666",
    "text_bright":  "#ffffff",
    "search_bg":    "#1a1a1a",
    "search_fg":    "#ffffff",
    "select_bg":    "#1a3a1a",
    "select_fg":    "#00ff88",
    "detail_key":   "#00ccff",
    "detail_val":   "#cccccc",
    "scrollbar":    "#333333",
    "category_fg":  "#ffaa00",
    # Rarity colors
    "common":       "#aaaaaa",
    "uncommon":     "#44ff44",
    "rare":         "#4488ff",
    "epic":         "#cc44ff",
    "legendary":    "#ffaa00",
    "mythic":       "#ff4444",
    # Category accent colors
    "cat_weapon":   "#ff6644",
    "cat_armor":    "#4488ff",
    "cat_shield":   "#44ccff",
    "cat_helm":     "#ffcc44",
    "cat_boots":    "#88ff44",
    "cat_gloves":   "#ff44cc",
    "cat_accessory":"#cc88ff",
    "cat_consumable":"#44ff44",
    "cat_material": "#aaaaaa",
    "cat_dungeon":  "#ff8844",
    "cat_world":    "#88ccff",
    "cat_quest":    "#ffff44",
    "cat_other":    "#888888",
}

RARITY_ORDER = ["common", "uncommon", "rare", "epic", "legendary", "mythic"]


def _build_item_registry():
    """
    Aggregate all items from every source into a master registry.
    Returns: dict { item_id -> { name, category, sub_category, description, how_to_get, rarity, sources } }
    """
    registry = {}
    master_sources = {}  # item_id -> set of source labels

    def _add(item_id, source):
        if not item_id or not isinstance(item_id, str) or not item_id.strip():
            return
        master_sources.setdefault(item_id, set()).add(source)

    # ── 1) Equipment database ────────────────────────────────────────
    EQUIPMENT_DATABASE = {}
    try:
        from equipment_system import EQUIPMENT_DATABASE as _EQ
        EQUIPMENT_DATABASE = _EQ
        for k in EQUIPMENT_DATABASE:
            _add(k, "equipment")
    except Exception:
        pass

    # ── 2) Shop item database ────────────────────────────────────────
    SHOP_DATABASE = {}
    try:
        from shop_system import ITEM_DATABASE as _SHOP
        SHOP_DATABASE = _SHOP
        for k in SHOP_DATABASE:
            _add(k, "shop")
    except Exception:
        pass

    # ── 3) Item effects (usable / consumable items) ──────────────────
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

    # ── 4) Crafting recipes ──────────────────────────────────────────
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

    # ── 5) Combat loot drops ─────────────────────────────────────────
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

    # ── 6) World.json items ──────────────────────────────────────────
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

    # ── 7) Fixed dungeon items ────────────────────────────────────────
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

    # ── 8) Quest rewards / objectives ────────────────────────────────
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
    # Build a lookup: recipe output -> recipe data
    recipe_by_output = {}
    for rid, rec in RECIPE_DATABASE.items():
        result_tuple = rec.get("result")
        out_id = result_tuple[0] if isinstance(result_tuple, tuple) else rec.get("output", rid)
        recipe_by_output[out_id] = rec

    # Build enemy name lookup for drop sources
    enemy_drop_map = {}  # item_id -> list of enemy names
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
        # ── Determine name ────────────────────────────────────────────
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
            # Stats
            stats = edata.get("stats", {})
            if stats:
                description += "\nStats: " + ", ".join(f"+{v} {k}" for k, v in stats.items())
            # Source
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
            drops = enemy_drop_map[item_id][:3]  # cap at 3 sources
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

        # Crafting ingredient only (not output)
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


# Category order for display
CATEGORY_ORDER = [
    "Equipment",
    "Crafted",
    "Consumable",
    "Material",
    "Dungeon Loot",
    "World Item",
    "Quest Item",
    "Other",
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


class SearchableItemsWindow:
    """Searchable items database window."""

    def __init__(self, parent, game_engine=None):
        self.parent = parent
        self.game_engine = game_engine
        self.window = None
        self._registry = {}          # full item registry
        self._filtered_ids = []      # currently displayed item IDs
        self._filtered_labels = []   # parallel list of label metadata
        self._search_var = None
        self._listbox = None
        self._detail_text = None
        self._status_var = None
        self._search_after_id = None

    # ── lifecycle ────────────────────────────────────────────────────
    def create_window(self):
        """Create and show the window."""
        if self.window and self.window.winfo_exists():
            self.window.lift()
            return

        self.window = tk.Toplevel(self.parent)
        self.window.title("Item Database — Debug Search")
        self.window.geometry("1000x680")
        self.window.minsize(760, 500)
        self.window.configure(bg=COLORS["bg"])
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)

        self._build_ui()
        self._load_registry()

    def close_window(self):
        """Close the window."""
        if self.window and self.window.winfo_exists():
            self.window.destroy()
        self.window = None

    def is_open(self):
        """Return True if window is currently visible."""
        return bool(self.window and self.window.winfo_exists())

    # ── UI construction ──────────────────────────────────────────────
    def _build_ui(self):
        win = self.window

        # ── Header ──────────────────────────────────────────────────
        header = tk.Label(
            win,
            text="[ITEM DATABASE SEARCH]",

            font=("Consolas", 14, "bold"),
            fg=COLORS["header_fg"],
            bg=COLORS["bg"],
            anchor="center",
        )
        header.pack(fill=tk.X, padx=8, pady=(8, 2))

        tk.Frame(win, height=1, bg=COLORS["border"]).pack(fill=tk.X, padx=8, pady=(0, 4))

        # ── Search bar row ───────────────────────────────────────────
        search_frame = tk.Frame(win, bg=COLORS["bg"])
        search_frame.pack(fill=tk.X, padx=8, pady=(0, 4))

        tk.Label(
            search_frame,
            text="Search:",

            font=("Consolas", 11),
            fg=COLORS["text"],
            bg=COLORS["bg"],
        ).pack(side=tk.LEFT, padx=(0, 6))

        self._search_var = tk.StringVar()
        self._search_var.trace_add("write", self._on_search_changed)

        search_entry = tk.Entry(
            search_frame,
            textvariable=self._search_var,
            font=("Consolas", 12),
            bg=COLORS["search_bg"],
            fg=COLORS["search_fg"],
            insertbackground=COLORS["header_fg"],
            relief=tk.FLAT,
            bd=4,
            width=32,
        )
        search_entry.pack(side=tk.LEFT, ipady=4)
        search_entry.focus_set()

        # Clear button
        tk.Button(
            search_frame,
            text="✕",
            font=("Consolas", 10),
            fg=COLORS["text_dim"],
            bg=COLORS["bg_light"],
            activebackground=COLORS["border"],
            activeforeground=COLORS["text"],
            relief=tk.FLAT,
            bd=0,
            padx=6,
            pady=2,
            cursor="hand2",
            command=lambda: self._search_var.set(""),
        ).pack(side=tk.LEFT, padx=4)

        # Status label (item count)
        self._status_var = tk.StringVar(value="Loading…")
        tk.Label(
            search_frame,
            textvariable=self._status_var,
            font=("Consolas", 10),
            fg=COLORS["text_dim"],
            bg=COLORS["bg"],
        ).pack(side=tk.RIGHT, padx=6)

        tk.Frame(win, height=1, bg=COLORS["border"]).pack(fill=tk.X, padx=8, pady=(0, 4))

        # ── Main content: list (left) + detail (right) ───────────────
        content = tk.Frame(win, bg=COLORS["bg"])
        content.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 6))
        content.columnconfigure(0, weight=2)
        content.columnconfigure(1, weight=3)
        content.rowconfigure(0, weight=1)

        # ── Left panel: item list ────────────────────────────────────
        list_frame = tk.Frame(content, bg=COLORS["bg_panel"], bd=1, relief=tk.FLAT)
        list_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 4))

        tk.Label(
            list_frame,
            text="ITEMS",

            font=("Consolas", 9, "bold"),
            fg=COLORS["text_dim"],
            bg=COLORS["bg_panel"],
            anchor="w",
        ).pack(fill=tk.X, padx=6, pady=(4, 0))

        lb_scroll_frame = tk.Frame(list_frame, bg=COLORS["bg_panel"])
        lb_scroll_frame.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        lb_scrollbar = tk.Scrollbar(lb_scroll_frame, bg=COLORS["scrollbar"])
        lb_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._listbox = tk.Listbox(
            lb_scroll_frame,
            font=("Consolas", 11),
            bg=COLORS["bg_panel"],
            fg=COLORS["text"],
            selectbackground=COLORS["select_bg"],
            selectforeground=COLORS["select_fg"],
            activestyle="none",
            relief=tk.FLAT,
            bd=0,
            highlightthickness=0,
            yscrollcommand=lb_scrollbar.set,
            exportselection=False,
        )
        self._listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        lb_scrollbar.config(command=self._listbox.yview)
        self._listbox.bind("<<ListboxSelect>>", self._on_item_selected)

        # ── Right panel: item detail ──────────────────────────────────
        detail_frame = tk.Frame(content, bg=COLORS["bg_panel"], bd=1, relief=tk.FLAT)
        detail_frame.grid(row=0, column=1, sticky="nsew", padx=(4, 0))

        tk.Label(
            detail_frame,
            text="ITEM DETAILS",
            font=("Consolas", 9, "bold"),
            fg=COLORS["text_dim"],
            bg=COLORS["bg_panel"],
            anchor="w",
        ).pack(fill=tk.X, padx=6, pady=(4, 0))

        det_scroll_frame = tk.Frame(detail_frame, bg=COLORS["bg_panel"])
        det_scroll_frame.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        det_scrollbar = tk.Scrollbar(det_scroll_frame, bg=COLORS["scrollbar"])
        det_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._detail_text = tk.Text(
            det_scroll_frame,
            font=("Consolas", 11),
            bg=COLORS["bg_panel"],
            fg=COLORS["text"],
            relief=tk.FLAT,
            bd=0,
            highlightthickness=0,
            wrap=tk.WORD,
            state=tk.DISABLED,
            yscrollcommand=det_scrollbar.set,
        )
        self._detail_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        det_scrollbar.config(command=self._detail_text.yview)

        # Text tags for detail panel
        self._detail_text.tag_configure("field_key", foreground=COLORS["detail_key"], font=("Consolas", 11, "bold"))
        self._detail_text.tag_configure("field_val", foreground=COLORS["detail_val"])
        self._detail_text.tag_configure("item_name", foreground=COLORS["text_bright"], font=("Consolas", 14, "bold"))
        self._detail_text.tag_configure("separator", foreground=COLORS["border"])
        self._detail_text.tag_configure("rarity_common",    foreground=COLORS["common"])
        self._detail_text.tag_configure("rarity_uncommon",  foreground=COLORS["uncommon"])
        self._detail_text.tag_configure("rarity_rare",      foreground=COLORS["rare"])
        self._detail_text.tag_configure("rarity_epic",      foreground=COLORS["epic"])
        self._detail_text.tag_configure("rarity_legendary", foreground=COLORS["legendary"])
        self._detail_text.tag_configure("rarity_mythic",    foreground=COLORS["mythic"])
        self._detail_text.tag_configure("how_to_get",       foreground="#88ffaa")
        self._detail_text.tag_configure("placeholder",      foreground=COLORS["text_dim"], font=("Consolas", 11, "italic"))

        # ── Footer ───────────────────────────────────────────────────
        footer = tk.Frame(win, bg=COLORS["bg"], height=20)
        footer.pack(fill=tk.X, padx=8, pady=(0, 6))
        tk.Label(
            footer,
            text="Type to search by item name or ID  •  Click an item for details  •  debug spawn item <id> to add to inventory",
            font=("Consolas", 9),
            fg=COLORS["text_dim"],
            bg=COLORS["bg"],
        ).pack(side=tk.LEFT)

    # ── Data loading ─────────────────────────────────────────────────
    def _load_registry(self):
        """Build item registry and populate the list."""
        self._status_var.set("Loading items…")
        self.window.update_idletasks()

        self._registry = _build_item_registry()
        self._apply_filter("")

    # ── Filtering ────────────────────────────────────────────────────
    def _on_search_changed(self, *_):
        """Debounce search: wait 120ms after last keystroke."""
        if self._search_after_id:
            self.window.after_cancel(self._search_after_id)
        self._search_after_id = self.window.after(120, self._do_search)

    def _do_search(self):
        query = self._search_var.get().strip().lower()
        self._apply_filter(query)

    def _apply_filter(self, query):
        """Rebuild the listbox based on current search query."""
        try:
            self._apply_filter_inner(query)
        except Exception as exc:
            import traceback
            tb = traceback.format_exc()
            lb = self._listbox
            lb.delete(0, tk.END)
            lb.insert(tk.END, f"  ERROR building item list:")
            lb.insert(tk.END, f"  {exc}")
            for line in tb.strip().splitlines()[-6:]:
                lb.insert(tk.END, f"  {line}")
            if self._status_var:
                self._status_var.set("Error")

    def _apply_filter_inner(self, query):
        """Inner (unchecked) filter logic."""
        lb = self._listbox
        lb.delete(0, tk.END)
        self._filtered_ids = []  # [item_id | None for headers]
        self._filtered_labels = []

        # Filter registry
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

        # Sort within each category by name
        for cat in categories:
            categories[cat].sort(key=lambda x: x[1]["name"].lower())

        total = 0
        for cat in CATEGORY_ORDER:
            if cat not in categories:
                continue
            items = categories[cat]
            icon = CATEGORY_ICONS.get(cat, "•")

            # Category header (sentinel = None)
            header_label = f"  {icon}  {cat.upper()}  ({len(items)})"
            self._filtered_ids.append(None)
            self._filtered_labels.append(("header", header_label, cat))
            lb.insert(tk.END, header_label)
            lb.itemconfig(tk.END, fg=COLORS["category_fg"])

            for iid, data in items:
                rarity = data.get("rarity", "common")
                rarity_icon = _rarity_icon(rarity)
                display = f"    {rarity_icon} {data['name']}"
                self._filtered_ids.append(iid)
                self._filtered_labels.append(("item", iid, data))
                lb.insert(tk.END, display)
                lb.itemconfig(tk.END, fg=_rarity_color(rarity))
                total += 1

        # Update any remaining categories not in CATEGORY_ORDER
        for cat, items in categories.items():
            if cat in CATEGORY_ORDER:
                continue
            icon = CATEGORY_ICONS.get(cat, "•")
            header_label = f"  {icon}  {cat.upper()}  ({len(items)})"
            self._filtered_ids.append(None)
            self._filtered_labels.append(("header", header_label, cat))
            lb.insert(tk.END, header_label)
            lb.itemconfig(tk.END, fg=COLORS["category_fg"])
            for iid, data in items:
                rarity = data.get("rarity", "common")
                rarity_icon = _rarity_icon(rarity)
                display = f"    {rarity_icon} {data['name']}"
                self._filtered_ids.append(iid)
                self._filtered_labels.append(("item", iid, data))
                lb.insert(tk.END, display)
                lb.itemconfig(tk.END, fg=_rarity_color(rarity))
                total += 1

        if total == 0 and query:
            self._status_var.set("No items found")
            self._filtered_ids.append(None)
            self._filtered_labels.append(("msg", "", None))
            lb.insert(tk.END, "  No items match your search.")
            lb.itemconfig(tk.END, fg=COLORS["text_dim"])
        else:
            self._status_var.set(f"{total} items")

        # Clear detail panel when filter changes
        self._show_placeholder()

    # ── Detail panel ─────────────────────────────────────────────────
    def _on_item_selected(self, event):
        sel = self._listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        if idx >= len(self._filtered_ids):
            return
        item_id = self._filtered_ids[idx]
        if item_id is None:
            return  # clicked a category header
        data = self._registry.get(item_id)
        if data:
            self._show_detail(item_id, data)

    def _show_placeholder(self):
        t = self._detail_text
        t.config(state=tk.NORMAL)
        t.delete("1.0", tk.END)
        t.insert(tk.END, "\n\n  Select an item from the list to view details.", "placeholder")
        t.config(state=tk.DISABLED)

    def _show_detail(self, item_id, data):
        t = self._detail_text
        t.config(state=tk.NORMAL)
        t.delete("1.0", tk.END)

        rarity = data.get("rarity", "common")
        rarity_tag = f"rarity_{rarity}"

        # Item name
        t.insert(tk.END, f"\n  {data['name']}\n", "item_name")

        # Rarity badge
        rarity_icon = _rarity_icon(rarity)
        t.insert(tk.END, f"  {rarity_icon} {rarity.upper()}", rarity_tag)

        # Category / sub-category
        cat = data["category"]
        sub = data.get("sub_category", "")
        cat_str = f"  {cat}"
        if sub:
            cat_str += f" › {sub}"
        t.insert(tk.END, f"    {cat_str}\n\n", "field_val")

        # Separator
        t.insert(tk.END, "  " + "─" * 44 + "\n\n", "separator")

        # ID field
        t.insert(tk.END, "  ID\n", "field_key")
        t.insert(tk.END, f"  {item_id}\n\n", "field_val")

        # Description
        t.insert(tk.END, "  DESCRIPTION\n", "field_key")
        desc = data.get("description") or "No description available."
        for line in desc.split("\n"):
            t.insert(tk.END, f"  {line}\n", "field_val")
        t.insert(tk.END, "\n")

        # How to get
        t.insert(tk.END, "  HOW TO GET\n", "field_key")
        how = data.get("how_to_get") or "Unknown"
        for line in how.split("\n"):
            t.insert(tk.END, f"  {line}\n", "how_to_get")
        t.insert(tk.END, "\n")

        # Sources (raw)
        sources = data.get("sources", [])
        if sources:
            t.insert(tk.END, "  SOURCES\n", "field_key")
            t.insert(tk.END, f"  {', '.join(sources)}\n\n", "field_val")

        # Spawn hint
        t.insert(tk.END, "  " + "─" * 44 + "\n", "separator")
        t.insert(tk.END, f"  To add: debug spawn item {item_id}\n", "field_val")

        t.config(state=tk.DISABLED)


# ── Helpers ───────────────────────────────────────────────────────────────────

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
