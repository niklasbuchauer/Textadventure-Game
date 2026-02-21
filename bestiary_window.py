"""
Bestiary Window (Pygame)
========================
Browse every enemy, mini-boss and boss in the game.
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
    "header":       "#ff4444",
    "text":         "#cccccc",
    "dim":          "#666666",
    "bright":       "#ffffff",
    "detail_key":   "#ff6644",
    "stat_hp":      "#ff8888",
    "stat_atk":     "#ffaa44",
    "stat_def":     "#88aaff",
    "stat_xp":      "#88ff88",
    "stat_gold":    "#ffcc00",
    "loot":         "#ffcc88",
    "ability":      "#cc88ff",
    "cat_crystal":  "#88ccff",
    "cat_iron":     "#aaaaaa",
    "cat_shadow":   "#cc88ff",
    "cat_sunken":   "#88ddcc",
    "cat_overworld":"#88ff88",
    "cat_miniboss": "#ffcc44",
    "cat_boss":     "#ff4444",
    "cat_other":    "#888888",
}

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


def _esc(t):
    return html_module.escape(str(t))


def _build_bestiary():
    registry = {}
    try:
        from combat_system import ENEMY_DATABASE
        for eid, data in ENEMY_DATABASE.items():
            d = dict(data); d["id"] = eid; d["tier"] = "normal"
            d["category"] = _dungeon_to_cat(d.get("dungeon", "any"))
            registry[eid] = d
    except Exception:
        pass
    try:
        from combat_system import MINI_BOSS_DATABASE
        for eid, data in MINI_BOSS_DATABASE.items():
            d = dict(data); d["id"] = eid; d["tier"] = "miniboss"
            d["category"] = "MINI-BOSSES"; registry[eid] = d
    except Exception:
        pass
    try:
        from combat_system import BOSS_DATABASE
        for eid, data in BOSS_DATABASE.items():
            d = dict(data); d["id"] = eid; d["tier"] = "boss"
            d["category"] = "BOSSES"; registry[eid] = d
    except Exception:
        pass
    return registry


def _dungeon_to_cat(k):
    return {"crystal_caverns": "CRYSTAL CAVERNS", "iron_halls": "IRON HALLS",
            "shadow_depths": "SHADOW DEPTHS", "sunken_catacombs": "SUNKEN CATACOMBS",
            "any": "OVERWORLD"}.get(k, "OTHER")


class BestiaryWindow:
    """Searchable bestiary overlay using pygame_gui."""

    def __init__(self, app):
        self.app = app
        self.manager = app.manager
        self._registry = {}
        self._filtered_ids = []

        W, H = app.width, app.height
        ww, wh = 1020, 680
        self.window = UIWindow(
            rect=pygame.Rect((W - ww) // 2, (H - wh) // 2, ww, wh),
            manager=self.manager,
            window_display_title="Bestiary",
            resizable=True,
        )
        iw = ww - 60

        # Search bar
        self._search = UITextEntryLine(
            relative_rect=pygame.Rect(10, 10, iw - 120, 28),
            manager=self.manager, container=self.window,
            placeholder_text="Search creatures...",
        )
        self._status = UILabel(
            relative_rect=pygame.Rect(iw - 100, 12, 100, 24),
            text="Loading...", manager=self.manager, container=self.window,
        )

        # Left list
        lw = int(iw * 0.38)
        self._list = UISelectionList(
            relative_rect=pygame.Rect(10, 46, lw, wh - 130),
            item_list=[], manager=self.manager, container=self.window,
        )

        # Right detail
        self._detail = UITextBox(
            html_text='<font color="#666666">Click a creature to see details.</font>',
            relative_rect=pygame.Rect(lw + 18, 46, iw - lw - 18, wh - 130),
            manager=self.manager, container=self.window,
        )

        self._last_search = ""
        self._load_registry()

    def is_open(self):
        return self.window.alive()

    def _load_registry(self):
        self._registry = _build_bestiary()
        self._apply_filter("")

    def _apply_filter(self, query):
        query = query.lower()
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

        groups = {}
        for eid, d in matches.items():
            groups.setdefault(d["category"], []).append((eid, d))
        for g in groups:
            groups[g].sort(key=lambda x: x[1].get("name", x[0]).lower())

        items = []
        self._filtered_ids = []
        total = 0
        for cat_name in CATEGORY_ORDER:
            group = groups.get(cat_name)
            if not group:
                continue
            items.append(f"── {cat_name} ({len(group)}) ──")
            self._filtered_ids.append(None)
            for eid, d in group:
                tier = d.get("tier", "normal")
                icon = {"normal": "[E]", "miniboss": "[M]", "boss": "[B]"}[tier]
                items.append(f"  {icon} {d.get('name', eid)}")
                self._filtered_ids.append(eid)
                total += 1

        self._list.set_item_list(items)
        self._status.set_text(f"{total} creatures")

        # Build direct text→id lookup for selection matching
        self._text_to_eid = {}
        for i, label in enumerate(items):
            eid = self._filtered_ids[i]
            if eid is not None:
                self._text_to_eid[label] = eid

    def handle_event(self, event):
        if not self.window.alive():
            return False

        # Search text changed
        cur = self._search.get_text().strip()
        if cur != self._last_search:
            self._last_search = cur
            self._apply_filter(cur)

        if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
            if event.ui_element == self._list:
                sel = event.text
                eid = self._text_to_eid.get(sel)
                if eid and eid in self._registry:
                    self._show_detail(eid, self._registry[eid])
                return True
        return False

    def _show_detail(self, eid, d):
        cat = d.get("category", "UNKNOWN")
        _, _, ck = next((c for c in CATEGORIES if c[0] == cat), (None, None, "cat_other"))
        tier = d.get("tier", "normal")
        tier_label = {"normal": "CREATURE", "miniboss": "\u2605 MINI-BOSS",
                      "boss": "\u2620 BOSS"}[tier]
        tier_col = {"normal": "#aaaaaa", "miniboss": "#ffcc44", "boss": "#ff4444"}[tier]
        cat_col = COLORS.get(ck, "#888888")

        lines = []
        lines.append(f'<font color="#ffffff" size="4"><b>{_esc(d.get("name", eid))}</b></font>')
        lines.append(f'<font color="#666666">{_esc(eid)}</font>')
        lines.append(f'<font color="{tier_col}">{_esc(tier_label)}</font>'
                      f'  <font color="{cat_col}">{_esc(cat)}</font>')
        lines.append(f'<font color="#2a2a2a">{"─" * 42}</font>')

        desc = d.get("description", "")
        if desc:
            lines.append(f'<br><font color="{COLORS["detail_key"]}"><b>DESCRIPTION</b></font>')
            for ln in textwrap.wrap(desc, width=52):
                lines.append(f'<font color="#cccccc"> {_esc(ln)}</font>')

        hp = d.get("hp", "?"); atk = d.get("attack", "?")
        dfn = d.get("defense", "?"); xp = d.get("xp_reward", "?")
        gold = d.get("gold_reward", "?")
        lines.append(f'<br><font color="{COLORS["detail_key"]}"><b>STATS</b></font>')
        lines.append(f'<font color="{COLORS["stat_hp"]}"> HP:      {hp}</font>')
        lines.append(f'<font color="{COLORS["stat_atk"]}"> Attack:  {atk}</font>')
        lines.append(f'<font color="{COLORS["stat_def"]}"> Defense: {dfn}</font>')
        lines.append(f'<font color="{COLORS["stat_xp"]}"> XP:     {xp}</font>')
        if isinstance(gold, (list, tuple)) and len(gold) == 2:
            lines.append(f'<font color="{COLORS["stat_gold"]}"> Gold:    {gold[0]}–{gold[1]}</font>')
        else:
            lines.append(f'<font color="{COLORS["stat_gold"]}"> Gold:    {gold}</font>')

        fr = d.get("floor_range")
        if fr:
            lines.append(f'<font color="#cccccc"> Floors:  {fr[0]}–{fr[1]}</font>')

        abilities = d.get("abilities") or []
        if abilities:
            lines.append(f'<br><font color="{COLORS["detail_key"]}"><b>ABILITIES</b></font>')
            for ab in abilities:
                lines.append(f'<font color="{COLORS["ability"]}"> \u2022 {_esc(ab)}</font>')

        loot = d.get("loot") or []
        if loot:
            lines.append(f'<br><font color="{COLORS["detail_key"]}"><b>LOOT TABLE</b></font>')
            for entry in loot:
                if isinstance(entry, (list, tuple)) and len(entry) == 2:
                    item_id, chance = entry
                    pct = int(chance * 100)
                    lines.append(f'<font color="{COLORS["loot"]}"> {pct:>3}%  {_esc(item_id)}</font>')
                else:
                    lines.append(f'<font color="{COLORS["loot"]}"> {_esc(entry)}</font>')

        self._detail.set_text("<br>".join(lines))
