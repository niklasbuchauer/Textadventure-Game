"""
Bestiary Window
===============
Browse every enemy, mini-boss and boss in the game.
Same dark design as the Item Database and Room Browser windows.
"""

import tkinter as tk
import textwrap


# ── Colour palette (matches dark game theme) ─────────────────────────────────
COLORS = {
    "bg":           "#0d0d0d",
    "bg_light":     "#161616",
    "bg_panel":     "#111111",
    "border":       "#2a2a2a",
    "header_fg":    "#ff4444",
    "text":         "#cccccc",
    "text_dim":     "#666666",
    "text_bright":  "#ffffff",
    "search_bg":    "#1a1a1a",
    "search_fg":    "#ffffff",
    "select_bg":    "#2a1a1a",
    "select_fg":    "#ff6644",
    "detail_key":   "#ff6644",
    "detail_val":   "#cccccc",
    "scrollbar":    "#333333",
    "category_fg":  "#ffaa00",
    # Per-dungeon accent colours
    "cat_crystal":   "#88ccff",
    "cat_iron":      "#aaaaaa",
    "cat_shadow":    "#cc88ff",
    "cat_sunken":    "#88ddcc",
    "cat_overworld": "#88ff88",
    "cat_miniboss":  "#ffcc44",
    "cat_boss":      "#ff4444",
    "cat_other":     "#888888",
}

# Ordered category list: (display, dungeon_key_list, colour_key)
CATEGORIES = [
    ("CRYSTAL CAVERNS",  ["crystal_caverns"],  "cat_crystal"),
    ("IRON HALLS",       ["iron_halls"],        "cat_iron"),
    ("SHADOW DEPTHS",    ["shadow_depths"],     "cat_shadow"),
    ("SUNKEN CATACOMBS", ["sunken_catacombs"],  "cat_sunken"),
    ("OVERWORLD",        ["any"],               "cat_overworld"),
    ("MINI-BOSSES",      ["__miniboss__"],      "cat_miniboss"),
    ("BOSSES",           ["__boss__"],          "cat_boss"),
    ("OTHER",            [],                    "cat_other"),
]
CATEGORY_ORDER = [c[0] for c in CATEGORIES]


def _build_bestiary():
    """
    Load ENEMY_DATABASE, MINI_BOSS_DATABASE, BOSS_DATABASE from combat_system.
    Returns dict { enemy_id -> entry_dict (augmented) }.
    """
    registry = {}

    try:
        from combat_system import ENEMY_DATABASE
        for eid, data in ENEMY_DATABASE.items():
            d = dict(data)
            d["id"] = eid
            d["tier"] = "normal"
            dungeon = d.get("dungeon", "any")
            # Map dungeon key to category display name
            cat = _dungeon_to_cat(dungeon)
            d["category"] = cat
            registry[eid] = d
    except Exception:
        pass

    try:
        from combat_system import MINI_BOSS_DATABASE
        for eid, data in MINI_BOSS_DATABASE.items():
            d = dict(data)
            d["id"] = eid
            d["tier"] = "miniboss"
            d["category"] = "MINI-BOSSES"
            registry[eid] = d
    except Exception:
        pass

    try:
        from combat_system import BOSS_DATABASE
        for eid, data in BOSS_DATABASE.items():
            d = dict(data)
            d["id"] = eid
            d["tier"] = "boss"
            d["category"] = "BOSSES"
            registry[eid] = d
    except Exception:
        pass

    return registry


def _dungeon_to_cat(dungeon_key: str) -> str:
    mapping = {
        "crystal_caverns":  "CRYSTAL CAVERNS",
        "iron_halls":       "IRON HALLS",
        "shadow_depths":    "SHADOW DEPTHS",
        "sunken_catacombs": "SUNKEN CATACOMBS",
        "any":              "OVERWORLD",
    }
    return mapping.get(dungeon_key, "OTHER")


class BestiaryWindow:
    """
    Dark, searchable Toplevel window listing all enemies/bosses.
    Same UI pattern as SearchableItemsWindow and SearchableRoomsWindow.
    """

    def __init__(self, parent):
        self._registry: dict = {}
        self._filtered_ids: list = []
        self._search_after_id = None

        win = tk.Toplevel(parent)
        win.title("Bestiary")
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
            text="[BESTIARY  —  ALL CREATURES & BOSSES]",
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

        # Main content
        content = tk.Frame(win, bg=COLORS["bg"])
        content.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 6))
        content.columnconfigure(0, weight=2)
        content.columnconfigure(1, weight=3)
        content.rowconfigure(0, weight=1)

        # Left panel – enemy list
        lf = tk.Frame(content, bg=COLORS["bg_panel"], bd=1, relief=tk.FLAT)
        lf.grid(row=0, column=0, sticky="nsew", padx=(0, 4))
        tk.Label(lf, text="ENEMIES",
                 font=("Consolas", 9, "bold"), fg=COLORS["text_dim"],
                 bg=COLORS["bg_panel"], anchor="w").pack(fill=tk.X, padx=6, pady=(4, 0))

        lb_sf = tk.Frame(lf, bg=COLORS["bg_panel"])
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
        self._listbox.bind("<<ListboxSelect>>", self._on_enemy_selected)

        # Right panel – detail
        df = tk.Frame(content, bg=COLORS["bg_panel"], bd=1, relief=tk.FLAT)
        df.grid(row=0, column=1, sticky="nsew", padx=(4, 0))
        tk.Label(df, text="CREATURE DETAILS",
                 font=("Consolas", 9, "bold"), fg=COLORS["text_dim"],
                 bg=COLORS["bg_panel"], anchor="w").pack(fill=tk.X, padx=6, pady=(4, 0))

        det_sf = tk.Frame(df, bg=COLORS["bg_panel"])
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
        self._detail_text.tag_configure("enemy_name",  foreground=COLORS["text_bright"],
                                        font=("Consolas", 14, "bold"))
        self._detail_text.tag_configure("enemy_id",    foreground=COLORS["text_dim"],
                                        font=("Consolas", 10))
        self._detail_text.tag_configure("tier_normal",  foreground="#aaaaaa",
                                        font=("Consolas", 10))
        self._detail_text.tag_configure("tier_miniboss", foreground="#ffcc44",
                                        font=("Consolas", 10, "bold"))
        self._detail_text.tag_configure("tier_boss",    foreground="#ff4444",
                                        font=("Consolas", 10, "bold"))
        self._detail_text.tag_configure("field_key",   foreground=COLORS["detail_key"],
                                        font=("Consolas", 11, "bold"))
        self._detail_text.tag_configure("field_val",   foreground=COLORS["detail_val"])
        self._detail_text.tag_configure("separator",   foreground=COLORS["border"])
        self._detail_text.tag_configure("stat_hp",     foreground="#ff8888")
        self._detail_text.tag_configure("stat_atk",    foreground="#ffaa44")
        self._detail_text.tag_configure("stat_def",    foreground="#88aaff")
        self._detail_text.tag_configure("stat_xp",     foreground="#88ff88")
        self._detail_text.tag_configure("stat_gold",   foreground="#ffcc00")
        self._detail_text.tag_configure("loot",        foreground="#ffcc88")
        self._detail_text.tag_configure("ability",     foreground="#cc88ff")
        self._detail_text.tag_configure("placeholder", foreground=COLORS["text_dim"],
                                        font=("Consolas", 11, "italic"))
        for _, _, ck in CATEGORIES:
            fg = COLORS.get(ck, COLORS["text"])
            self._detail_text.tag_configure(ck, foreground=fg)

        # Footer
        ftr = tk.Frame(win, bg=COLORS["bg"], height=20)
        ftr.pack(fill=tk.X, padx=8, pady=(0, 6))
        tk.Label(ftr,
                 text="Type to search by name or ID  •  Click a creature for details",
                 font=("Consolas", 9), fg=COLORS["text_dim"], bg=COLORS["bg"]).pack(side=tk.LEFT)

    # ── Data loading ──────────────────────────────────────────────────────────
    def _load_registry(self):
        self._status_var.set("Loading creatures…")
        self.window.update_idletasks()
        self._registry = _build_bestiary()
        self._apply_filter("")

    # ── Filtering ─────────────────────────────────────────────────────────────
    def _on_search_changed(self, *_):
        if self._search_after_id:
            self.window.after_cancel(self._search_after_id)
        self._search_after_id = self.window.after(120, self._do_search)

    def _do_search(self):
        self._apply_filter(self._search_var.get().strip().lower())

    def _apply_filter(self, query: str):
        lb = self._listbox
        lb.delete(0, tk.END)
        self._filtered_ids = []

        if query:
            matches = {
                eid: d for eid, d in self._registry.items()
                if query in eid.lower()
                   or query in d.get("name", "").lower()
                   or query in d.get("category", "").lower()
                   or query in d.get("description", "").lower()
            }
        else:
            matches = self._registry

        # Group by category
        groups: dict[str, list] = {}
        for eid, d in matches.items():
            groups.setdefault(d["category"], []).append((eid, d))
        for g in groups:
            groups[g].sort(key=lambda x: x[1].get("name", x[0]).lower())

        total = 0
        for cat_name in CATEGORY_ORDER:
            items = groups.get(cat_name)
            if not items:
                continue
            _, _, ck = next((c for c in CATEGORIES if c[0] == cat_name), (None, None, "cat_other"))
            header = f"  ── {cat_name} ({len(items)}) ──"
            lb.insert(tk.END, header)
            lb.itemconfig(tk.END, fg=COLORS.get(ck, COLORS["category_fg"]),
                          selectbackground=COLORS["bg_panel"],
                          selectforeground=COLORS.get(ck, COLORS["category_fg"]))
            self._filtered_ids.append(None)

            for eid, d in items:
                tier = d.get("tier", "normal")
                icon = {"normal": "[E]", "miniboss": "[M]", "boss": "[B]"}[tier]
                label = f"    {icon} {d.get('name', eid)}"
                lb.insert(tk.END, label)
                lb.itemconfig(tk.END, fg=COLORS.get(ck, COLORS["text"]))
                self._filtered_ids.append(eid)
                total += 1

        self._status_var.set(f"{total} creatures")
        self._show_placeholder()

    # ── Selection ─────────────────────────────────────────────────────────────
    def _on_enemy_selected(self, _event=None):
        sel = self._listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        if idx >= len(self._filtered_ids):
            return
        eid = self._filtered_ids[idx]
        if eid is None:
            return
        d = self._registry.get(eid)
        if d:
            self._show_detail(eid, d)

    def _show_placeholder(self):
        dt = self._detail_text
        dt.config(state=tk.NORMAL)
        dt.delete("1.0", tk.END)
        dt.insert(tk.END, "\n\n  Click a creature to see details.", "placeholder")
        dt.config(state=tk.DISABLED)

    def _show_detail(self, eid: str, d: dict):
        dt = self._detail_text
        dt.config(state=tk.NORMAL)
        dt.delete("1.0", tk.END)

        cat = d.get("category", "UNKNOWN")
        _, _, ck = next((c for c in CATEGORIES if c[0] == cat), (None, None, "cat_other"))
        tier = d.get("tier", "normal")
        tier_label = {"normal": "CREATURE", "miniboss": "  ★ MINI-BOSS", "boss": "  ☠ BOSS"}[tier]

        # Name
        dt.insert(tk.END, f"\n  {d.get('name', eid)}\n", "enemy_name")
        dt.insert(tk.END, f"  {eid}\n", "enemy_id")
        dt.insert(tk.END, f"  {tier_label}  •  {cat}\n", f"tier_{tier}")
        dt.insert(tk.END, "  " + "─" * 42 + "\n", "separator")

        # Description
        desc = d.get("description", "")
        if desc:
            dt.insert(tk.END, "\n  DESCRIPTION\n", "field_key")
            for line in textwrap.wrap(desc, width=52):
                dt.insert(tk.END, f"   {line}\n", "field_val")

        # Stats
        hp   = d.get("hp", "?")
        atk  = d.get("attack", "?")
        dfn  = d.get("defense", "?")
        xp   = d.get("xp_reward", "?")
        gold = d.get("gold_reward", ("?", "?"))
        floor_range = d.get("floor_range", None)

        dt.insert(tk.END, "\n  STATS\n", "field_key")
        dt.insert(tk.END, f"   HP:       {hp}\n",       "stat_hp")
        dt.insert(tk.END, f"   Attack:   {atk}\n",      "stat_atk")
        dt.insert(tk.END, f"   Defense:  {dfn}\n",      "stat_def")
        dt.insert(tk.END, f"   XP Reward:{xp}\n",       "stat_xp")
        if isinstance(gold, (list, tuple)) and len(gold) == 2:
            dt.insert(tk.END, f"   Gold:     {gold[0]}–{gold[1]}\n", "stat_gold")
        else:
            dt.insert(tk.END, f"   Gold:     {gold}\n", "stat_gold")
        if floor_range:
            dt.insert(tk.END, f"   Floors:   {floor_range[0]}–{floor_range[1]}\n", "field_val")

        # Abilities
        abilities = d.get("abilities") or []
        if abilities:
            dt.insert(tk.END, "\n  ABILITIES\n", "field_key")
            for ab in abilities:
                dt.insert(tk.END, f"   • {ab}\n", "ability")

        # Loot
        loot = d.get("loot") or []
        if loot:
            dt.insert(tk.END, "\n  LOOT TABLE\n", "field_key")
            for entry in loot:
                if isinstance(entry, (list, tuple)) and len(entry) == 2:
                    item_id, chance = entry
                    pct = int(chance * 100)
                    dt.insert(tk.END, f"   {pct:>3}%  {item_id}\n", "loot")
                else:
                    dt.insert(tk.END, f"   {entry}\n", "loot")

        dt.config(state=tk.DISABLED)
