"""
Searchable Rooms Window
=======================
Browse every game area/room in a searchable, categorised window — same dark
design as the Item Database window.
"""

import tkinter as tk


# ── Colour palette (matches dark game theme) ─────────────────────────────────
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
    "select_bg":    "#1a2a3a",
    "select_fg":    "#00ccff",
    "detail_key":   "#00ccff",
    "detail_val":   "#cccccc",
    "scrollbar":    "#333333",
    "category_fg":  "#ffaa00",
    # area accent colours
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
    ("OTHER",             [],             "area_other"),   # catch-all
]


def _region_for(room_id: str):
    rid = room_id.lower()
    for name, prefixes, colour in REGIONS[:-1]:   # skip catch-all
        for p in prefixes:
            if rid.startswith(p) or p in rid:
                return name, colour
    return REGIONS[-1][0], REGIONS[-1][2]          # OTHER


def _build_room_registry(engine):
    """
    Build a dict  { room_id -> RoomInfo }  from world.json rooms.
    Accepts a GameEngine instance.
    """
    registry = {}
    try:
        raw_rooms = engine.rooms   # dict of room_id -> raw dict or Room obj
    except AttributeError:
        return registry

    for rid, rdata in raw_rooms.items():
        # Support both Room objects and raw dicts
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


# Region display order
REGION_ORDER = [r[0] for r in REGIONS]


class SearchableRoomsWindow:
    """
    Dark, searchable Toplevel window that lists all game rooms/areas.
    Follows the same UI pattern as SearchableItemsWindow.
    """

    def __init__(self, parent, engine):
        self._engine  = engine
        self._registry: dict = {}
        self._filtered_ids: list = []
        self._search_after_id = None

        win = tk.Toplevel(parent)
        win.title("Room Browser")
        win.geometry("1020x680")
        win.minsize(760, 500)
        win.configure(bg=COLORS["bg"])
        self.window = win

        self._build_ui()
        self._load_registry()

    def is_open(self):
        return bool(self.window and self.window.winfo_exists())

    # ── UI construction ────────────────────────────────────────────────────────
    def _build_ui(self):
        win = self.window

        # Header
        tk.Label(
            win,
            text="[ROOM & AREA BROWSER]",
            font=("Consolas", 14, "bold"),
            fg=COLORS["header_fg"],
            bg=COLORS["bg"],
            anchor="center",
        ).pack(fill=tk.X, padx=8, pady=(8, 2))
        tk.Frame(win, height=1, bg=COLORS["border"]).pack(fill=tk.X, padx=8, pady=(0, 4))

        # Search bar
        sf = tk.Frame(win, bg=COLORS["bg"])
        sf.pack(fill=tk.X, padx=8, pady=(0, 4))
        tk.Label(sf, text="Search:", font=("Consolas", 11),
                 fg=COLORS["text"], bg=COLORS["bg"]).pack(side=tk.LEFT, padx=(0, 6))

        self._search_var = tk.StringVar()
        self._search_var.trace_add("write", self._on_search_changed)
        entry = tk.Entry(sf, textvariable=self._search_var,
                         font=("Consolas", 12),
                         bg=COLORS["search_bg"], fg=COLORS["search_fg"],
                         insertbackground=COLORS["header_fg"],
                         relief=tk.FLAT, bd=4, width=32)
        entry.pack(side=tk.LEFT, ipady=4)
        entry.focus_set()

        tk.Button(sf, text="✕", font=("Consolas", 10),
                  fg=COLORS["text_dim"], bg=COLORS["bg_light"],
                  activebackground=COLORS["border"], activeforeground=COLORS["text"],
                  relief=tk.FLAT, bd=0, padx=6, pady=2, cursor="hand2",
                  command=lambda: self._search_var.set("")).pack(side=tk.LEFT, padx=4)

        self._status_var = tk.StringVar(value="Loading…")
        tk.Label(sf, textvariable=self._status_var,
                 font=("Consolas", 10), fg=COLORS["text_dim"],
                 bg=COLORS["bg"]).pack(side=tk.RIGHT, padx=6)

        tk.Frame(win, height=1, bg=COLORS["border"]).pack(fill=tk.X, padx=8, pady=(0, 4))

        # Main content: list (left) + detail (right)
        content = tk.Frame(win, bg=COLORS["bg"])
        content.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 6))
        content.columnconfigure(0, weight=2)
        content.columnconfigure(1, weight=3)
        content.rowconfigure(0, weight=1)

        # Left panel
        list_frame = tk.Frame(content, bg=COLORS["bg_panel"], bd=1, relief=tk.FLAT)
        list_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 4))
        tk.Label(list_frame, text="AREAS & ROOMS",
                 font=("Consolas", 9, "bold"), fg=COLORS["text_dim"],
                 bg=COLORS["bg_panel"], anchor="w").pack(fill=tk.X, padx=6, pady=(4, 0))

        lb_sf = tk.Frame(list_frame, bg=COLORS["bg_panel"])
        lb_sf.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        lb_scroll = tk.Scrollbar(lb_sf, bg=COLORS["scrollbar"])
        lb_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self._listbox = tk.Listbox(
            lb_sf,
            font=("Consolas", 11),
            bg=COLORS["bg_panel"],
            fg=COLORS["text"],
            selectbackground=COLORS["select_bg"],
            selectforeground=COLORS["select_fg"],
            activestyle="none",
            relief=tk.FLAT, bd=0, highlightthickness=0,
            yscrollcommand=lb_scroll.set,
            exportselection=False,
        )
        self._listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        lb_scroll.config(command=self._listbox.yview)
        self._listbox.bind("<<ListboxSelect>>", self._on_room_selected)

        # Right panel
        det_frame = tk.Frame(content, bg=COLORS["bg_panel"], bd=1, relief=tk.FLAT)
        det_frame.grid(row=0, column=1, sticky="nsew", padx=(4, 0))
        tk.Label(det_frame, text="ROOM DETAILS",
                 font=("Consolas", 9, "bold"), fg=COLORS["text_dim"],
                 bg=COLORS["bg_panel"], anchor="w").pack(fill=tk.X, padx=6, pady=(4, 0))

        det_sf = tk.Frame(det_frame, bg=COLORS["bg_panel"])
        det_sf.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        det_scroll = tk.Scrollbar(det_sf, bg=COLORS["scrollbar"])
        det_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self._detail_text = tk.Text(
            det_sf,
            font=("Consolas", 11),
            bg=COLORS["bg_panel"], fg=COLORS["text"],
            relief=tk.FLAT, bd=0, highlightthickness=0,
            wrap=tk.WORD, state=tk.DISABLED,
            yscrollcommand=det_scroll.set,
        )
        self._detail_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        det_scroll.config(command=self._detail_text.yview)

        # Text tags
        self._detail_text.tag_configure("room_name",  foreground=COLORS["text_bright"],
                                        font=("Consolas", 14, "bold"))
        self._detail_text.tag_configure("room_id",    foreground=COLORS["text_dim"],
                                        font=("Consolas", 10))
        self._detail_text.tag_configure("field_key",  foreground=COLORS["detail_key"],
                                        font=("Consolas", 11, "bold"))
        self._detail_text.tag_configure("field_val",  foreground=COLORS["detail_val"])
        self._detail_text.tag_configure("separator",  foreground=COLORS["border"])
        self._detail_text.tag_configure("region_tag", foreground=COLORS["category_fg"],
                                        font=("Consolas", 10, "bold"))
        self._detail_text.tag_configure("placeholder", foreground=COLORS["text_dim"],
                                        font=("Consolas", 11, "italic"))
        self._detail_text.tag_configure("exit_boat",  foreground="#00ffcc")
        self._detail_text.tag_configure("exit_dir",   foreground="#88aacc")
        self._detail_text.tag_configure("npc",        foreground="#ffcc44")
        self._detail_text.tag_configure("item",       foreground="#88ff88")
        # Per-region colours
        for _, _, ck in REGIONS:
            self._detail_text.tag_configure(ck, foreground=COLORS.get(ck, COLORS["text"]))

        # Footer
        ftr = tk.Frame(win, bg=COLORS["bg"], height=20)
        ftr.pack(fill=tk.X, padx=8, pady=(0, 6))
        tk.Label(ftr,
                 text="Type to search by room name or ID  •  Click a room for details",
                 font=("Consolas", 9), fg=COLORS["text_dim"], bg=COLORS["bg"]).pack(side=tk.LEFT)

    # ── Data loading ──────────────────────────────────────────────────────────
    def _load_registry(self):
        self._status_var.set("Loading rooms…")
        self.window.update_idletasks()
        self._registry = _build_room_registry(self._engine)
        self._apply_filter("")

    # ── Filtering ─────────────────────────────────────────────────────────────
    def _on_search_changed(self, *_):
        if self._search_after_id:
            self.window.after_cancel(self._search_after_id)
        self._search_after_id = self.window.after(120, self._do_search)

    def _do_search(self):
        self._apply_filter(self._search_var.get().strip().lower())

    def _apply_filter(self, query):
        lb = self._listbox
        lb.delete(0, tk.END)
        self._filtered_ids = []

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

        total = 0
        for region_name in REGION_ORDER:
            items = regions.get(region_name)
            if not items:
                continue
            # Category header
            _, _, ck = next((r for r in REGIONS if r[0] == region_name), (None, None, "area_other"))
            header_text = f"  ── {region_name} ({'%d' % len(items)}) ──"
            lb.insert(tk.END, header_text)
            lb.itemconfig(tk.END, fg=COLORS.get(ck, COLORS["category_fg"]),
                          selectbackground=COLORS["bg_panel"],
                          selectforeground=COLORS.get(ck, COLORS["category_fg"]))
            self._filtered_ids.append(None)   # header sentinel

            for rid, d in items:
                loc = d["loc_type"]
                tag = f"[{loc[:3].upper()}]" if loc else "[   ]"
                has_boat = any(
                    isinstance(v, dict) and v.get("type") == "boat_travel"
                    for v in d["exits"].values()
                )
                boat_icon = " ⛵" if has_boat else ""
                label = f"    {tag} {d['name']}{boat_icon}"
                lb.insert(tk.END, label)
                lb.itemconfig(tk.END, fg=COLORS.get(ck, COLORS["text"]))
                self._filtered_ids.append(rid)
                total += 1

        self._status_var.set(f"{total} rooms")
        self._show_placeholder()

    # ── Selection ─────────────────────────────────────────────────────────────
    def _on_room_selected(self, _event=None):
        sel = self._listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        if idx >= len(self._filtered_ids):
            return
        rid = self._filtered_ids[idx]
        if rid is None:
            return   # header row
        d = self._registry.get(rid)
        if d:
            self._show_detail(rid, d)

    def _show_placeholder(self):
        dt = self._detail_text
        dt.config(state=tk.NORMAL)
        dt.delete("1.0", tk.END)
        dt.insert(tk.END, "\n\n  Click a room to see details.", "placeholder")
        dt.config(state=tk.DISABLED)

    def _show_detail(self, rid: str, d: dict):
        dt = self._detail_text
        dt.config(state=tk.NORMAL)
        dt.delete("1.0", tk.END)

        # Room name
        dt.insert(tk.END, f"\n  {d['name']}\n", "room_name")
        # ID & region
        dt.insert(tk.END, f"  {rid}\n", "room_id")
        dt.insert(tk.END, f"  {d['region']}\n", d["colour"])
        dt.insert(tk.END, "  " + "─" * 42 + "\n", "separator")

        # Location type & coords
        if d["loc_type"]:
            dt.insert(tk.END, "\n  TYPE       ", "field_key")
            dt.insert(tk.END, f"{d['loc_type']}\n", "field_val")
        if d["coordinates"]:
            cx, cy = d["coordinates"]
            dt.insert(tk.END, "  COORDS     ", "field_key")
            dt.insert(tk.END, f"({cx}, {cy})\n", "field_val")

        # Description
        if d["description"]:
            dt.insert(tk.END, "\n  DESCRIPTION\n", "field_key")
            # Word-wrap at ~52 chars
            desc = d["description"]
            import textwrap
            for line in textwrap.wrap(desc, width=52):
                dt.insert(tk.END, f"   {line}\n", "field_val")

        # Exits
        if d["exits"]:
            dt.insert(tk.END, "\n  EXITS\n", "field_key")
            for key, val in d["exits"].items():
                if isinstance(val, dict):
                    etype = val.get("type", "")
                    target = val.get("target", "?")
                    display = val.get("display", "")
                    if etype == "boat_travel":
                        line = f"   ⛵ {key!s:<22} → {display or target}\n"
                        dt.insert(tk.END, line, "exit_boat")
                    else:
                        line = f"   {key!s:<22} → {target}\n"
                        dt.insert(tk.END, line, "exit_dir")
                else:
                    line = f"   {key!s:<22} → {val}\n"
                    dt.insert(tk.END, line, "exit_dir")

        # NPCs
        if d["npcs"]:
            dt.insert(tk.END, "\n  NPCS\n", "field_key")
            for npc in d["npcs"]:
                dt.insert(tk.END, f"   • {npc}\n", "npc")

        # Items
        items = d["items"]
        if items:
            dt.insert(tk.END, "\n  ITEMS\n", "field_key")
            if isinstance(items, dict):
                for iid, info in items.items():
                    qty = info.get("quantity", 1) if isinstance(info, dict) else ""
                    qty_str = f" ×{qty}" if qty and qty != 1 else ""
                    dt.insert(tk.END, f"   • {iid}{qty_str}\n", "item")
            elif isinstance(items, list):
                for iid in items:
                    dt.insert(tk.END, f"   • {iid}\n", "item")

        dt.config(state=tk.DISABLED)
