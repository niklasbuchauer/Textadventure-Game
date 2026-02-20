"""
Skill Tree System
=================
Class-based skill trees with tiered nodes (radial layout):
  - Passive nodes: permanent stat bonuses
  - Active nodes: usable abilities with cooldowns

Each class (Warrior, Rogue, Mage) has 200+ nodes across 5 tiers,
arranged in branches radiating from a center origin node.

The graphical skill tree window is built using Tkinter Canvas with
a radial constellation layout supporting pan/zoom.
"""

import tkinter as tk
from tkinter import font as tkfont
import math

from skill_tree_data import (
    WARRIOR_TREE, ROGUE_TREE, MAGE_TREE,
    SKILL_TREES_DATA, CLASS_BRANCHES,
    WARRIOR_BRANCHES, ROGUE_BRANCHES, MAGE_BRANCHES,
)

# =====================================================================
# SYNERGY / SET BONUSES
# =====================================================================
# When a player unlocks enough skills in the same branch, they receive
# cumulative branch-mastery bonuses (3 / 5 / 8 / 12 node thresholds).

SYNERGY_THRESHOLDS = [
    (3,  "Initiate",    {"attack": 1, "defense": 1}),
    (5,  "Adept",       {"attack": 2, "defense": 1, "health_max_bonus": 5}),
    (8,  "Expert",      {"attack": 3, "defense": 2, "health_max_bonus": 10, "crit_chance_bonus": 0.02}),
    (12, "Master",      {"attack": 5, "defense": 3, "health_max_bonus": 20, "crit_chance_bonus": 0.05}),
]

# Branch-specific extra bonuses layered on top of the generic thresholds
BRANCH_SYNERGY_EXTRAS = {
    # Warrior
    "berserker":    {3: {"attack": 1}, 5: {"attack": 2},  8: {"crit_chance_bonus": 0.03}},
    "tank":         {3: {"defense": 2}, 5: {"defense": 3}, 8: {"health_max_bonus": 15}},
    "archer":       {3: {"attack": 1}, 5: {"crit_chance_bonus": 0.02}, 8: {"attack": 3}},
    "commander":    {3: {"defense": 1}, 5: {"attack": 1, "defense": 1}, 8: {"health_max_bonus": 10}},
    "weaponmaster": {3: {"attack": 2}, 5: {"attack": 2}, 8: {"crit_chance_bonus": 0.04}},
    "gladiator":    {3: {"health_max_bonus": 5}, 5: {"attack": 2}, 8: {"defense": 3}},
    # Rogue
    "assassin":     {3: {"attack": 2}, 5: {"crit_chance_bonus": 0.03}, 8: {"attack": 4}},
    "trickster":    {3: {"defense": 1}, 5: {"defense": 2}, 8: {"attack": 2, "defense": 2}},
    "thief":        {3: {"crit_chance_bonus": 0.01}, 5: {"crit_chance_bonus": 0.02}, 8: {"attack": 2}},
    "bounty_hunter":{3: {"attack": 1}, 5: {"attack": 2}, 8: {"health_max_bonus": 10}},
    "phantom":      {3: {"defense": 1}, 5: {"attack": 2}, 8: {"crit_chance_bonus": 0.03}},
    # Mage
    "fire":         {3: {"attack": 2}, 5: {"attack": 3}, 8: {"crit_chance_bonus": 0.03}},
    "ice":          {3: {"defense": 1}, 5: {"defense": 2}, 8: {"health_max_bonus": 10}},
    "earth":        {3: {"defense": 2}, 5: {"health_max_bonus": 10}, 8: {"defense": 4}},
    "wind":         {3: {"attack": 1}, 5: {"crit_chance_bonus": 0.02}, 8: {"attack": 3}},
    "lightning":    {3: {"attack": 2}, 5: {"attack": 2}, 8: {"crit_chance_bonus": 0.04}},
    "arcane":       {3: {"attack": 1, "defense": 1}, 5: {"attack": 2}, 8: {"health_max_bonus": 10}},
    "healer":       {3: {"health_max_bonus": 5}, 5: {"health_max_bonus": 10}, 8: {"defense": 3}},
    "shadow":       {3: {"attack": 1}, 5: {"crit_chance_bonus": 0.02}, 8: {"attack": 3}},
}


def get_branch_counts(player):
    """Return {branch_name: count} of unlocked skills per branch."""
    class_id = player.stats.get("class", "")
    tree = get_tree_for_class(class_id)
    unlocked = set(get_unlocked_skills(player))
    counts = {}
    for node in tree:
        if node["id"] in unlocked and node.get("branch", "origin") != "origin":
            branch = node["branch"]
            counts[branch] = counts.get(branch, 0) + 1
    return counts


def get_synergy_bonuses(player):
    """
    Calculate total synergy bonuses from all branches.
    Returns (total_bonuses_dict, list_of_active_synergy_descriptions).
    """
    counts = get_branch_counts(player)
    total = {}
    descriptions = []

    for branch, count in counts.items():
        # Generic thresholds
        for threshold, rank, bonuses in SYNERGY_THRESHOLDS:
            if count >= threshold:
                for stat, val in bonuses.items():
                    total[stat] = total.get(stat, 0) + val
                if count < (SYNERGY_THRESHOLDS[SYNERGY_THRESHOLDS.index((threshold, rank, bonuses)) + 1][0]
                            if SYNERGY_THRESHOLDS.index((threshold, rank, bonuses)) + 1 < len(SYNERGY_THRESHOLDS)
                            else 999):
                    descriptions.append(f"{branch.replace('_', ' ').title()} {rank} ({count} nodes)")
            else:
                break

        # Branch-specific extras
        extras = BRANCH_SYNERGY_EXTRAS.get(branch, {})
        for thresh, bonus in sorted(extras.items()):
            if count >= thresh:
                for stat, val in bonus.items():
                    total[stat] = total.get(stat, 0) + val

    return total, descriptions


def apply_synergy_bonuses(player):
    """
    Recalculate and apply synergy bonuses, storing the previous values
    to properly update stats (removing old and adding new).
    """
    old_synergy = player.state.get("_synergy_bonuses", {})
    new_synergy, descriptions = get_synergy_bonuses(player)

    # Remove old synergy bonuses
    for stat, val in old_synergy.items():
        if stat == "health_max_bonus":
            player.stats["health_max"] = player.stats.get("health_max", 100) - val
            player.stats["health"] = min(player.stats.get("health", 100), player.stats.get("health_max", 100))
        else:
            player.stats[stat] = player.stats.get(stat, 0) - val

    # Apply new synergy bonuses
    for stat, val in new_synergy.items():
        if stat == "health_max_bonus":
            player.stats["health_max"] = player.stats.get("health_max", 100) + val
            player.stats["health"] = min(player.stats.get("health", 100) + val, player.stats.get("health_max", 100))
        else:
            player.stats[stat] = player.stats.get(stat, 0) + val

    # Store for next recalculation
    player.state["_synergy_bonuses"] = new_synergy
    player.state["_synergy_descriptions"] = descriptions

    return new_synergy, descriptions


# =====================================================================
# SKILL TREES REGISTRY (imported from skill_tree_data.py)
# =====================================================================

SKILL_TREES = SKILL_TREES_DATA


# =====================================================================
# SKILL TREE LOGIC
# =====================================================================

def get_tree_for_class(class_id):
    """Get the skill tree node list for a class."""
    return SKILL_TREES.get(class_id, [])



def get_node_by_id(class_id, node_id):
    """Find a specific skill node by its ID."""
    tree = get_tree_for_class(class_id)
    for node in tree:
        if node["id"] == node_id:
            return node
    return None


def get_all_nodes_by_id(class_id):
    """Return a dict mapping node_id -> node for quick lookups."""
    return {n["id"]: n for n in get_tree_for_class(class_id)}


def get_unlocked_skills(player):
    """Return list of unlocked skill IDs."""
    return list(player.state.get("unlocked_skills", []))


def is_skill_unlocked(player, skill_id):
    """Check if a specific skill is unlocked."""
    return skill_id in player.state.get("unlocked_skills", [])


def get_available_skills(player):
    """
    Return list of skill nodes the player CAN unlock right now
    (prerequisites met, not already unlocked, has enough skill points).
    """
    class_id = player.stats.get("class", "")
    tree = get_tree_for_class(class_id)
    unlocked = set(get_unlocked_skills(player))
    sp = player.stats.get("skill_points", 0)

    available = []
    for node in tree:
        if node["id"] in unlocked:
            continue
        prereqs_met = all(p in unlocked for p in node.get("prerequisites", []))
        if not prereqs_met:
            continue
        if sp >= node["cost"]:
            available.append(node)

    return available


def unlock_skill(player, skill_id):
    """
    Unlock a skill node for the player.
    Returns: (success: bool, message: str)
    """
    class_id = player.stats.get("class", "")
    node = get_node_by_id(class_id, skill_id)

    if not node:
        return False, "Unknown skill."

    unlocked = set(get_unlocked_skills(player))

    if skill_id in unlocked:
        return False, f"{node['name']} is already unlocked."

    for prereq in node.get("prerequisites", []):
        if prereq not in unlocked:
            prereq_node = get_node_by_id(class_id, prereq)
            prereq_name = prereq_node["name"] if prereq_node else prereq
            return False, f"Requires: {prereq_name}"

    sp = player.stats.get("skill_points", 0)
    if sp < node["cost"]:
        return False, f"Need {node['cost']} skill point{'s' if node['cost'] > 1 else ''}, have {sp}."

    # Spend skill points
    player.stats["skill_points"] = sp - node["cost"]

    # Add to unlocked list
    if "unlocked_skills" not in player.state:
        player.state["unlocked_skills"] = []
    player.state["unlocked_skills"].append(skill_id)

    # Apply stat bonuses
    for stat, value in node.get("stat_bonuses", {}).items():
        if stat == "health_max_bonus":
            player.stats["health_max"] = player.stats.get("health_max", 100) + value
            player.stats["health"] = min(
                player.stats.get("health", 100) + value,
                player.stats.get("health_max", 100)
            )
        elif stat in ("crafting_bonus", "crit_chance_bonus", "disarm_bonus"):
            player.stats[stat] = player.stats.get(stat, 0) + value
        else:
            player.stats[stat] = player.stats.get(stat, 0) + value

    # Build success message
    result = "\n" + "=" * 50 + "\n"
    result += f"  SKILL UNLOCKED: {node['name']}\n"
    result += "=" * 50 + "\n"
    result += f"  {node['description']}\n"

    if node["type"] == "active":
        ability = node.get("ability", {})
        result += f"\n  New ability: {ability.get('name', node['name'])}\n"
        result += f"  Cooldown: {ability.get('cooldown', 0)} turns\n"
        if ability.get("combat"):
            result += "  Usable in combat!\n"
        cmd_name = ability.get('name', '').lower().replace(' ', '_')
        result += f"  Use: ability {cmd_name}\n"

    if node.get("stat_bonuses"):
        result += "\n  Stat changes:\n"
        for stat, val in node["stat_bonuses"].items():
            nice = stat.replace("_", " ").replace("health max bonus", "Max Health")
            nice = nice.replace("crit chance bonus", "Crit Chance")
            nice = nice.replace("crafting bonus", "Crafting Bonus")
            nice = nice.replace("disarm bonus", "Disarm Bonus")
            if isinstance(val, float):
                result += f"    {nice.capitalize()}: +{val:.0%}\n"
            else:
                result += f"    {nice.capitalize()}: +{val}\n"

    result += f"\n  Remaining skill points: {player.stats.get('skill_points', 0)}\n"

    # Recalculate synergy bonuses
    synergy_bonuses, synergy_descs = apply_synergy_bonuses(player)
    if synergy_descs:
        branch = node.get("branch", "origin")
        branch_count = get_branch_counts(player).get(branch, 0)
        # Check if this unlock triggered a new synergy threshold
        for threshold, rank, _ in SYNERGY_THRESHOLDS:
            if branch_count == threshold and branch != "origin":
                result += f"\n  ★ SYNERGY BONUS: {branch.replace('_', ' ').title()} {rank}!\n"
                result += f"    ({branch_count} nodes in {branch.replace('_', ' ').title()} branch)\n"
                extras = BRANCH_SYNERGY_EXTRAS.get(branch, {}).get(threshold, {})
                bonus_list = dict(SYNERGY_THRESHOLDS[[t[0] for t in SYNERGY_THRESHOLDS].index(threshold)][2])
                for s, v in extras.items():
                    bonus_list[s] = bonus_list.get(s, 0) + v
                for stat, val in bonus_list.items():
                    nice = stat.replace("_", " ").replace("health max bonus", "Max HP")
                    nice = nice.replace("crit chance bonus", "Crit%")
                    if isinstance(val, float):
                        result += f"    +{val:.0%} {nice}\n"
                    else:
                        result += f"    +{val} {nice}\n"
                break

    result += "=" * 50 + "\n"

    return True, result


def get_active_abilities(player):
    """Return list of active ability dicts the player has unlocked."""
    class_id = player.stats.get("class", "")
    tree = get_tree_for_class(class_id)
    unlocked = set(get_unlocked_skills(player))

    abilities = []
    for node in tree:
        if node["id"] in unlocked and node["type"] == "active":
            ability = dict(node.get("ability", {}))
            ability["skill_id"] = node["id"]
            ability["skill_name"] = node["name"]
            ability["description"] = node.get("description", "")
            abilities.append(ability)

    return abilities


def use_ability(player, ability_name):
    """Attempt to use an active ability. Returns (success, message, ability_data)."""
    abilities = get_active_abilities(player)
    if not abilities:
        return False, "You don't have any active abilities yet.", None

    # Normalize the search term
    search = ability_name.lower().replace("_", " ").strip()

    # Find matching ability
    found = None
    for ab in abilities:
        ab_name = ab.get("name", "").lower()
        ab_key = ab_name.replace(" ", "_")
        if search in (ab_name, ab_key) or ab_name.startswith(search):
            found = ab
            break

    if not found:
        names = [a["name"] for a in abilities]
        return False, f"Unknown ability. Your abilities: {', '.join(names)}", None

    # Check cooldown
    cooldowns = player.state.get("cooldowns", {})
    cd_key = found["skill_id"]
    remaining = cooldowns.get(cd_key, 0)
    if remaining > 0:
        return False, f"{found['name']} is on cooldown ({remaining} turns remaining).", None

    # Activate the ability
    effect = found.get("effect", "")

    # Set cooldown
    if "cooldowns" not in player.state:
        player.state["cooldowns"] = {}
    player.state["cooldowns"][cd_key] = found.get("cooldown", 10)

    # Combat effects are returned to the engine for processing
    combat_effects = (
        "combat_damage", "combat_crit_attack", "combat_stun",
        "combat_poison", "combat_freeze_attack", "combat_damage_burn",
        "combat_damage_stun", "combat_heal", "combat_execute",
        "combat_bleed_attack", "guaranteed_flee", "buff_attack",
        "extra_gold"
    )

    if effect not in combat_effects:
        _apply_ability_effect(player, effect, found.get("duration", 1), found.get("value", 0))

    result = "\n" + "-" * 50 + "\n"
    result += f"  {found.get('use_text', 'You use ' + found['name'] + '!')}\n"
    result += f"  [{found['name']} active"
    if found.get("duration", 1) > 1:
        result += f" for {found['duration']} turns"
    result += "]\n"
    result += "-" * 50 + "\n"

    return True, result, found


def _apply_ability_effect(player, effect, duration, value):
    """Apply non-combat ability effects to the player state."""
    active_effects = player.state.get("active_effects", {})

    if effect == "stun_trap":
        active_effects["trap_stunned"] = duration
    elif effect == "temp_defense":
        active_effects["defense_boost"] = {"value": value, "duration": duration}
        player.stats["defense"] = player.stats.get("defense", 0) + value
    elif effect == "reveal_adjacent_traps":
        active_effects["reveal_traps"] = 1
    elif effect == "trap_immunity":
        active_effects["trap_immune"] = duration
    elif effect == "bypass_trap":
        active_effects["sneak_active"] = duration
    elif effect == "guaranteed_detection":
        active_effects["guaranteed_detection"] = duration
    elif effect == "double_loot":
        active_effects["double_loot"] = duration
    elif effect == "phantom_mode":
        active_effects["sneak_active"] = duration
        active_effects["guaranteed_detection"] = duration
    elif effect == "absorb_trap":
        active_effects["trap_immune"] = duration
    elif effect == "heal":
        hp = player.stats.get("health", 100)
        hp_max = player.stats.get("health_max", 100)
        player.stats["health"] = min(hp + value, hp_max)
    elif effect == "reveal_floor":
        active_effects["reveal_floor"] = 1
    elif effect == "archmage_mode":
        active_effects["archmage_mode"] = duration
        active_effects["guaranteed_detection"] = duration

    player.state["active_effects"] = active_effects


def tick_effects(player):
    """
    Called after each player move to decrement durations.
    Also ticks cooldowns. Returns list of expiry messages.
    """
    messages = []

    # Tick cooldowns
    cooldowns = player.state.get("cooldowns", {})
    expired_cds = []
    for key in list(cooldowns.keys()):
        cooldowns[key] -= 1
        if cooldowns[key] <= 0:
            expired_cds.append(key)
    for key in expired_cds:
        del cooldowns[key]

    # Tick active effects
    active = player.state.get("active_effects", {})
    expired = []
    for key in list(active.keys()):
        val = active[key]
        if isinstance(val, dict):
            val["duration"] -= 1
            if val["duration"] <= 0:
                expired.append(key)
                if key == "defense_boost":
                    player.stats["defense"] = max(0, player.stats.get("defense", 0) - val.get("value", 0))
                    messages.append("  Your defense boost fades.")
                elif key == "attack_boost":
                    player.stats["strength"] = max(0, player.stats.get("strength", 0) - val.get("value", 0))
                    messages.append("  Your attack boost fades.")
        elif isinstance(val, int):
            active[key] = val - 1
            if active[key] <= 0:
                expired.append(key)
                if key == "trap_immune":
                    messages.append("  Your trap immunity fades.")
                elif key == "sneak_active":
                    messages.append("  You step out of the shadows.")
                elif key == "guaranteed_detection":
                    messages.append("  Your heightened awareness fades.")
                elif key == "archmage_mode":
                    messages.append("  Your archmage power fades.")
                elif key == "trap_stunned":
                    messages.append("  The stunned trap mechanism resets.")

    for key in expired:
        if key in active:
            del active[key]

    # Clean up one-shot effects
    for key in ("reveal_traps", "reveal_floor"):
        if key in active:
            del active[key]

    player.state["active_effects"] = active

    return messages


def has_active_effect(player, effect_name):
    """Check if player has an active effect."""
    active = player.state.get("active_effects", {})
    val = active.get(effect_name, 0)
    if isinstance(val, dict):
        return val.get("duration", 0) > 0
    return val > 0


# =====================================================================
# GRAPHICAL SKILL TREE WINDOW — Radial Constellation Layout
# =====================================================================

NODE_R = 18            # base node radius (logical)
RING_GAP = 110         # distance between tier rings (logical)
LOGICAL_SIZE = 3000    # logical canvas extent
LCENTER = LOGICAL_SIZE // 2
MINIMAP_W = 180        # minimap size in pixels

# Per-class canvas background
CLASS_BG = {
    "warrior": "#0f0d08",
    "rogue":   "#080d0f",
    "mage":    "#0d080f",
}


class SkillTreeWindow:
    """Radial constellation skill tree with pan, zoom, minimap and
    class-themed visuals (hexagons / diamonds / circles)."""

    # ── construction ──

    def __init__(self, root, player, engine=None):
        self.root = root
        self.player = player
        self.engine = engine
        self.window = None
        self.canvas = None
        self.minimap = None
        self._node_items = {}      # canvas_item_id  -> node_id
        self._positions = {}       # node_id -> (lx, ly) logical
        self._zoom = 1.0
        self._tip_ids = []
        self._pan_origin = None
        self._did_drag = False
        self._sp_lbl = None
        self._det_lbl = None
        self._fonts = {}
        self._search_var = None    # tk.StringVar for search entry
        self._search_matches = set()   # set of node_ids matching search
        self._path_nodes = set()       # set of node_ids on highlighted path
        self._path_edges = set()       # set of (from_id, to_id) tuples on path
        self._search_entry = None
        self._pulse_phase = 0       # 0..7 animation phase for available node glow
        self._pulse_timer = None    # after() ID for pulse animation
        self._hidden_branches = set()  # branch names hidden by filter

    def is_open(self):
        return self.window is not None and self.window.winfo_exists()

    # ── window lifecycle ──

    def create_window(self):
        if self.is_open():
            self.window.lift()
            self.window.focus_force()
            return

        cls_id = self.player.stats.get("class", "warrior")
        cls_name = cls_id.capitalize()
        bg = CLASS_BG.get(cls_id, "#0d0d0d")

        self.window = tk.Toplevel(self.root)
        self.window.title(f"Skill Tree \u2014 {cls_name}")
        self.window.geometry("1600x900")
        self.window.configure(bg="#1a1a1a")
        self.window.resizable(True, True)

        self._fonts = {
            "title":  tkfont.Font(family="Segoe UI", size=12, weight="bold"),
            "bold":   tkfont.Font(family="Segoe UI", size=10, weight="bold"),
            "normal": tkfont.Font(family="Segoe UI", size=9),
            "small":  tkfont.Font(family="Segoe UI", size=7),
            "tiny":   tkfont.Font(family="Segoe UI", size=6),
        }

        # --- top bar ---
        top = tk.Frame(self.window, bg="#222222", padx=12, pady=6)
        top.pack(fill="x")
        tk.Label(top, text=f"{cls_name} Skill Tree",
                 font=self._fonts["title"], bg="#222222", fg="#FFD700"
                 ).pack(side="left")
        tk.Label(top, text=f"Level {self.player.stats.get('level', 1)}",
                 font=self._fonts["bold"], bg="#222222", fg="#999999"
                 ).pack(side="left", padx=20)
        self._sp_lbl = tk.Label(top, font=self._fonts["bold"],
                                bg="#222222", fg="#FFD700")
        self._sp_lbl.pack(side="right")
        self._update_sp()

        # --- legend + zoom ---
        bar = tk.Frame(self.window, bg="#1a1a1a", padx=10, pady=3)
        bar.pack(fill="x")
        legend_items = [
            ("#2a2a2a", "#444444", "Locked"),
            ("#1a3a5a", "#42A5F5", "Available"),
            ("#1a4a1a", "#66BB6A", "Unlocked"),
            ("#4a2a00", "#FF9800", "Active"),
        ]
        for fill, out, label in legend_items:
            c = tk.Canvas(bar, width=14, height=14, bg="#1a1a1a",
                          highlightthickness=0)
            c.create_oval(1, 1, 13, 13, fill=fill, outline=out, width=1)
            c.pack(side="left", padx=(8, 2))
            tk.Label(bar, text=label, font=self._fonts["tiny"],
                     bg="#1a1a1a", fg="#888888").pack(side="left", padx=(0, 6))
        # zoom buttons (right side, reversed so order is − + ⊙)
        for txt, cmd in [
            ("\u2299", self._zoom_home),
            ("+", lambda: self._apply_zoom(1.20)),
            ("\u2212", lambda: self._apply_zoom(1 / 1.20)),
        ]:
            tk.Button(bar, text=txt, width=2, command=cmd,
                      bg="#333333", fg="white", relief="flat",
                      font=self._fonts["small"]).pack(side="right", padx=1)
        tk.Label(bar, text="Zoom:", font=self._fonts["tiny"],
                 bg="#1a1a1a", fg="#666666").pack(side="right", padx=4)

        # --- search bar ---
        sep = tk.Frame(bar, width=2, bg="#444444")
        sep.pack(side="left", fill="y", padx=8, pady=2)
        tk.Label(bar, text="🔍", font=self._fonts["small"],
                 bg="#1a1a1a", fg="#888888").pack(side="left", padx=(4, 2))
        self._search_var = tk.StringVar()
        self._search_var.trace_add("write", lambda *_: self._search_nodes())
        self._search_entry = tk.Entry(bar, textvariable=self._search_var,
                                       width=18, bg="#2a2a2a", fg="#e0e0e0",
                                       insertbackground="#e0e0e0",
                                       font=self._fonts["small"],
                                       relief="flat", bd=2)
        self._search_entry.pack(side="left", padx=2)
        tk.Button(bar, text="✕", width=2, command=self._clear_search,
                  bg="#333333", fg="#FF5555", relief="flat",
                  font=self._fonts["small"]).pack(side="left", padx=1)

        # --- canvas ---
        frame = tk.Frame(self.window, bg=bg)
        frame.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(frame, bg=bg, highlightthickness=0,
                                xscrollincrement=1, yscrollincrement=1)
        self.canvas.pack(fill="both", expand=True)

        # minimap overlay
        self.minimap = tk.Canvas(frame, width=MINIMAP_W, height=MINIMAP_W,
                                 bg="#111111", highlightthickness=1,
                                 highlightbackground="#333333")
        self.minimap.place(relx=1.0, rely=1.0, x=-8, y=-8, anchor="se")
        self.minimap.bind("<Button-1>", self._minimap_click)

        # --- detail bar ---
        det = tk.Frame(self.window, bg="#222222", padx=12, pady=8)
        det.pack(fill="x")
        self._det_lbl = tk.Label(
            det,
            text="Drag to pan  \u00b7  Scroll to zoom  \u00b7  Click a node to view or unlock",
            font=self._fonts["normal"], bg="#222222", fg="#777777",
            wraplength=1500, justify="left", anchor="w")
        self._det_lbl.pack(fill="x")

        # compute & draw
        self._compute_positions()
        self._full_draw()
        self.window.update_idletasks()
        self._center_on_origin()

        # bindings
        self.canvas.bind("<ButtonPress-1>", self._on_press)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)
        self.canvas.bind("<MouseWheel>", self._on_scroll)
        self.canvas.bind("<Motion>", self._on_hover)
        self.canvas.bind("<Button-3>", self._on_right_click)
        self.window.bind("<Control-f>", lambda e: self._focus_search())
        self.window.bind("<Escape>", lambda e: self._clear_search())
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)

        # start pulse animation
        self._start_pulse()

    def close_window(self):
        if self._pulse_timer and self.window:
            try:
                self.window.after_cancel(self._pulse_timer)
            except Exception:
                pass
            self._pulse_timer = None
        if self.window:
            try:
                self.window.destroy()
            except Exception:
                pass
        self.window = None
        self.canvas = None
        self.minimap = None

    def _update_sp(self):
        sp = self.player.stats.get("skill_points", 0)
        if self._sp_lbl:
            self._sp_lbl.config(text=f"Skill Points: {sp}")

    # ── position computation ──

    def _compute_positions(self):
        """Place every node in logical (world) coordinates using a radial
        layout: origin at center, branches fan outward by angle, tiers
        map to concentric rings."""
        cls_id = self.player.stats.get("class", "warrior")
        tree = get_tree_for_class(cls_id)
        branches = CLASS_BRANCHES.get(cls_id, {})

        # group by (branch, tier)
        groups = {}
        for node in tree:
            key = (node.get("branch", "origin"), node["tier"])
            groups.setdefault(key, []).append(node)

        self._positions = {}
        for (branch, tier), nodes in groups.items():
            if tier == 0:
                for n in nodes:
                    self._positions[n["id"]] = (float(LCENTER), float(LCENTER))
                continue

            bdef = branches.get(branch, {"angle_start": 0, "angle_end": 60})
            a0 = math.radians(bdef["angle_start"])
            a1 = math.radians(bdef["angle_end"])
            radius = tier * RING_GAP
            count = len(nodes)

            if count == 1:
                a = (a0 + a1) / 2
                self._positions[nodes[0]["id"]] = (
                    LCENTER + radius * math.cos(a),
                    LCENTER + radius * math.sin(a))
            else:
                pad = (a1 - a0) * 0.08
                span = (a1 - a0) - 2 * pad
                for i, n in enumerate(nodes):
                    a = a0 + pad + span * i / (count - 1)
                    self._positions[n["id"]] = (
                        LCENTER + radius * math.cos(a),
                        LCENTER + radius * math.sin(a))

    # ── coordinate helpers ──

    def _l2c(self, lx, ly):
        """Logical → canvas coordinates (apply zoom)."""
        return lx * self._zoom, ly * self._zoom

    def _c2l(self, cx, cy):
        """Canvas → logical coordinates."""
        return cx / self._zoom, cy / self._zoom

    # ── drawing ──

    def _full_draw(self):
        """Redraw the entire tree at current zoom level."""
        if not self.canvas:
            return

        self.canvas.delete("all")
        self._node_items.clear()

        cls_id = self.player.stats.get("class", "warrior")
        tree = get_tree_for_class(cls_id)
        unlocked = set(get_unlocked_skills(self.player))
        avail = {n["id"] for n in get_available_skills(self.player)}
        branches = CLASS_BRANCHES.get(cls_id, {})
        z = self._zoom

        if not tree:
            self.canvas.create_text(800, 450, text="No skill tree available.",
                                    font=self._fonts["bold"], fill="#ffffff")
            return

        max_t = max(n["tier"] for n in tree)
        ccx, ccy = self._l2c(LCENTER, LCENTER)

        # --- ring guides ---
        for t in range(1, max_t + 1):
            r = t * RING_GAP * z
            self.canvas.create_oval(ccx - r, ccy - r, ccx + r, ccy + r,
                                    outline="#161616", width=1, dash=(3, 8))

        # --- branch separators & labels ---
        # Count nodes per branch for labels
        branch_counts = {}
        branch_unlocked_counts = {}
        for node in tree:
            b = node.get("branch", "origin")
            if b == "origin":
                continue
            branch_counts[b] = branch_counts.get(b, 0) + 1
            if node["id"] in unlocked:
                branch_unlocked_counts[b] = branch_unlocked_counts.get(b, 0) + 1

        for bname, bdef in branches.items():
            if bname == "origin":
                continue
            a_line = math.radians(bdef["angle_start"])
            outer = (max_t + 0.5) * RING_GAP * z
            ex = ccx + outer * math.cos(a_line)
            ey = ccy + outer * math.sin(a_line)
            # Dim separator for hidden branches
            sep_color = "#181818" if bname not in self._hidden_branches else "#0d0d0d"
            self.canvas.create_line(ccx, ccy, ex, ey,
                                    fill=sep_color, width=1, dash=(2, 8))
            mid = math.radians((bdef["angle_start"] + bdef["angle_end"]) / 2)
            lr = (max_t + 1.3) * RING_GAP * z
            lx = ccx + lr * math.cos(mid)
            ly = ccy + lr * math.sin(mid)
            # Label with node counts
            bc = branch_counts.get(bname, 0)
            buc = branch_unlocked_counts.get(bname, 0)
            label_text = bdef["label"]
            if z >= 0.4:
                label_text += f" ({buc}/{bc})"
            label_color = bdef["color"] if bname not in self._hidden_branches else "#333333"
            self.canvas.create_text(lx, ly, text=label_text,
                                    font=self._fonts["small"],
                                    fill=label_color)

        # --- connections ---
        for node in tree:
            nid = node["id"]
            if nid not in self._positions:
                continue
            ncx, ncy = self._l2c(*self._positions[nid])
            for pid in node.get("prerequisites", []):
                if pid not in self._positions:
                    continue
                pcx, pcy = self._l2c(*self._positions[pid])
                both = nid in unlocked and pid in unlocked
                # Check if this edge is on the highlighted path
                on_path = (pid, nid) in self._path_edges or (nid, pid) in self._path_edges
                if on_path:
                    color = "#FFD700"
                    w = 3
                elif both:
                    color = "#3a7a3a"
                    w = 2
                else:
                    color = "#2a2a2a"
                    w = 1
                mx, my = (pcx + ncx) / 2, (pcy + ncy) / 2
                pull = 0.08
                mx += (ccx - mx) * pull
                my += (ccy - my) * pull
                self.canvas.create_line(pcx, pcy, mx, my, ncx, ncy,
                                        fill=color, width=w, smooth=True)

        # --- nodes ---
        nr = NODE_R * z
        # Pulse intensity for available node glow (0.3 → 1.0 → 0.3)
        pulse_t = abs((self._pulse_phase % 16) - 8) / 8.0  # 0..1
        pulse_alpha = 0.3 + 0.7 * pulse_t
        # Convert pulse to a color intensity
        pulse_r = int(66 * pulse_alpha)
        pulse_g = int(165 * pulse_alpha)
        pulse_b = int(245 * pulse_alpha)
        pulse_color = f"#{pulse_r:02x}{pulse_g:02x}{pulse_b:02x}"

        for node in tree:
            nid = node["id"]
            if nid not in self._positions:
                continue
            sx, sy = self._l2c(*self._positions[nid])
            branch = node.get("branch", "origin")
            bdef = branches.get(branch, {})

            # Hide nodes in filtered-out branches
            branch_hidden = branch in self._hidden_branches and branch != "origin"

            # dim non-matching nodes when search is active
            is_search_match = nid in self._search_matches if self._search_matches else False
            is_on_path = nid in self._path_nodes if self._path_nodes else False
            dimmed = (bool(self._search_matches) and not is_search_match and not is_on_path) or branch_hidden

            # state colours
            if nid in unlocked:
                if node["type"] == "active":
                    fill, out = "#4a2a00", "#FF9800"
                else:
                    fill, out = "#1a4a1a", "#66BB6A"
            elif nid in avail:
                fill, out = "#1a3a5a", "#42A5F5"
            else:
                fill, out = "#2a2a2a", "#444444"

            # dim non-matching nodes
            if dimmed:
                fill = "#1a1a1a"
                out = "#2a2a2a"

            # search match highlight (bright golden glow)
            if is_search_match:
                gr = nr + 7
                self.canvas.create_oval(sx - gr, sy - gr, sx + gr, sy + gr,
                                        outline="#FFD700", width=3)

            # path highlight (cyan glow)
            if is_on_path and not is_search_match:
                gr = nr + 5
                self.canvas.create_oval(sx - gr, sy - gr, sx + gr, sy + gr,
                                        outline="#00E5FF", width=2, dash=(4, 3))

            # animated glow ring for available nodes
            if nid in avail and not dimmed:
                gr = nr + 4 + pulse_t * 2  # glow size pulses slightly
                self.canvas.create_oval(sx - gr, sy - gr, sx + gr, sy + gr,
                                        outline=pulse_color, width=2, dash=(3, 3))

            # origin node is larger
            r = nr * 1.6 if node["tier"] == 0 else nr

            # class-specific shape
            shape_id = self._draw_node_shape(cls_id, sx, sy, r, fill, out)
            self._node_items[shape_id] = nid

            # name label
            if z >= 0.35:
                name = node["name"]
                if z < 0.7 and len(name) > 10:
                    name = name[:8] + ".."
                text_fill = "#e0e0e0"
                if dimmed:
                    text_fill = "#555555"
                elif is_search_match:
                    text_fill = "#FFD700"
                tid = self.canvas.create_text(
                    sx, sy, text=name,
                    font=self._fonts["tiny"],
                    fill=text_fill, width=r * 2 - 4,
                    justify="center", tags=("node",))
                self._node_items[tid] = nid

            # active-ability lightning bolt
            if node["type"] == "active" and z >= 0.5:
                self.canvas.create_text(
                    sx, sy + r + 6 * z,
                    text="\u26a1", font=self._fonts["tiny"],
                    fill="#FF9800")

        # scroll region
        margin = 100 * z
        extent = (max_t + 2) * RING_GAP * z
        lo = LCENTER * z - extent
        hi = LCENTER * z + extent
        self.canvas.configure(scrollregion=(
            lo - margin, lo - margin, hi + margin, hi + margin))

        self._draw_minimap()

    def _draw_node_shape(self, cls_id, cx, cy, r, fill, outline):
        """Draw a node shape appropriate for the class."""
        if cls_id == "warrior":
            # hexagon
            pts = []
            for i in range(6):
                a = math.radians(60 * i - 30)
                pts.extend([cx + r * math.cos(a), cy + r * math.sin(a)])
            return self.canvas.create_polygon(
                pts, fill=fill, outline=outline, width=2, tags=("node",))
        elif cls_id == "rogue":
            # diamond
            return self.canvas.create_polygon(
                cx, cy - r, cx + r, cy, cx, cy + r, cx - r, cy,
                fill=fill, outline=outline, width=2, tags=("node",))
        else:
            # circle (mage & fallback)
            return self.canvas.create_oval(
                cx - r, cy - r, cx + r, cy + r,
                fill=fill, outline=outline, width=2, tags=("node",))

    # ── minimap ──

    def _draw_minimap(self):
        if not self.minimap:
            return
        self.minimap.delete("all")

        cls_id = self.player.stats.get("class", "warrior")
        tree = get_tree_for_class(cls_id)
        unlocked = set(get_unlocked_skills(self.player))
        branches = CLASS_BRANCHES.get(cls_id, {})

        max_t = max((n["tier"] for n in tree), default=1)
        world_ext = (max_t + 1.5) * RING_GAP * 2
        scale = MINIMAP_W / world_ext
        half = MINIMAP_W / 2

        for node in tree:
            nid = node["id"]
            if nid not in self._positions:
                continue
            lx, ly = self._positions[nid]
            mx_pos = (lx - LCENTER) * scale + half
            my_pos = (ly - LCENTER) * scale + half
            branch = node.get("branch", "origin")
            bdef = branches.get(branch, {})
            # Highlight search matches and path nodes on minimap
            if nid in self._search_matches:
                color = "#FFD700"
                dr = 4
            elif nid in self._path_nodes:
                color = "#00E5FF"
                dr = 3
            elif nid in unlocked:
                color = "#66BB6A"
                dr = 2
            else:
                color = bdef.get("color", "#555555")
                dr = 2
            self.minimap.create_oval(mx_pos - dr, my_pos - dr,
                                     mx_pos + dr, my_pos + dr,
                                     fill=color, outline="")

        # viewport rectangle
        try:
            sr_str = self.canvas.cget("scrollregion")
            if sr_str:
                sr = [float(x) for x in sr_str.split()]
                sw, sh = sr[2] - sr[0], sr[3] - sr[1]
                xf = self.canvas.xview()
                yf = self.canvas.yview()
                z = self._zoom
                vx0 = (sr[0] + xf[0] * sw) / z
                vy0 = (sr[1] + yf[0] * sh) / z
                vx1 = (sr[0] + xf[1] * sw) / z
                vy1 = (sr[1] + yf[1] * sh) / z
                rx0 = (vx0 - LCENTER) * scale + half
                ry0 = (vy0 - LCENTER) * scale + half
                rx1 = (vx1 - LCENTER) * scale + half
                ry1 = (vy1 - LCENTER) * scale + half
                self.minimap.create_rectangle(
                    rx0, ry0, rx1, ry1,
                    outline="#FFD700", width=1)
        except Exception:
            pass

    # ── pan / zoom ──

    def _on_press(self, event):
        self._pan_origin = (event.x, event.y)
        self._did_drag = False
        self.canvas.scan_mark(event.x, event.y)

    def _on_drag(self, event):
        if self._pan_origin:
            dx = abs(event.x - self._pan_origin[0])
            dy = abs(event.y - self._pan_origin[1])
            if dx > 5 or dy > 5:
                self._did_drag = True
        self.canvas.scan_dragto(event.x, event.y, gain=1)
        self._draw_minimap()

    def _on_release(self, event):
        if not self._did_drag:
            self._handle_click(event)
        self._pan_origin = None

    def _on_scroll(self, event):
        factor = 1.15 if event.delta > 0 else 1 / 1.15
        self._apply_zoom(factor, event.x, event.y)

    def _apply_zoom(self, factor, sx=None, sy=None):
        new_z = self._zoom * factor
        if new_z < 0.2 or new_z > 3.0:
            return
        if sx is None:
            sx = (self.canvas.winfo_width() or 1600) // 2
            sy = (self.canvas.winfo_height() or 900) // 2

        # logical point under mouse before zoom
        old_cx = self.canvas.canvasx(sx)
        old_cy = self.canvas.canvasy(sy)
        lx, ly = old_cx / self._zoom, old_cy / self._zoom

        self._zoom = new_z
        self._full_draw()

        # scroll so the same logical point stays under the mouse
        new_cx = lx * self._zoom
        new_cy = ly * self._zoom
        sr_str = self.canvas.cget("scrollregion")
        if sr_str:
            sr = [float(v) for v in sr_str.split()]
            sw, sh = sr[2] - sr[0], sr[3] - sr[1]
            if sw > 0:
                self.canvas.xview_moveto(
                    max(0, min(1, (new_cx - sx - sr[0]) / sw)))
            if sh > 0:
                self.canvas.yview_moveto(
                    max(0, min(1, (new_cy - sy - sr[1]) / sh)))
        self._draw_minimap()

    def _zoom_home(self):
        self._zoom = 1.0
        self._full_draw()
        self._center_on_origin()

    def _center_on_origin(self):
        """Scroll the canvas so the origin node is centered in the window."""
        self.canvas.update_idletasks()
        sr_str = self.canvas.cget("scrollregion")
        if not sr_str:
            return
        sr = [float(v) for v in sr_str.split()]
        sw, sh = sr[2] - sr[0], sr[3] - sr[1]
        cw = self.canvas.winfo_width() or 1600
        ch = self.canvas.winfo_height() or 900
        target_cx = LCENTER * self._zoom
        target_cy = LCENTER * self._zoom
        if sw > 0:
            self.canvas.xview_moveto(
                max(0, (target_cx - cw / 2 - sr[0]) / sw))
        if sh > 0:
            self.canvas.yview_moveto(
                max(0, (target_cy - ch / 2 - sr[1]) / sh))
        self._draw_minimap()

    # ── pulse animation ──

    def _start_pulse(self):
        """Start the pulse animation for available nodes."""
        if not self.is_open():
            return
        self._pulse_phase = (self._pulse_phase + 1) % 16
        # Only redraw the glow rings, not the full tree (efficient update)
        self._update_pulse_glows()
        self._pulse_timer = self.window.after(150, self._start_pulse)

    def _update_pulse_glows(self):
        """Update only the available-node glow rings without full redraw."""
        if not self.canvas:
            return
        # Delete old pulse glows
        self.canvas.delete("pulse_glow")
        z = self._zoom
        nr = NODE_R * z
        pulse_t = abs((self._pulse_phase % 16) - 8) / 8.0
        pulse_r = int(66 * (0.3 + 0.7 * pulse_t))
        pulse_g = int(165 * (0.3 + 0.7 * pulse_t))
        pulse_b = int(245 * (0.3 + 0.7 * pulse_t))
        pulse_color = f"#{pulse_r:02x}{pulse_g:02x}{pulse_b:02x}"

        avail = {n["id"] for n in get_available_skills(self.player)}
        for nid in avail:
            if nid not in self._positions:
                continue
            if nid in self._search_matches or nid in self._path_nodes:
                continue
            branch = None
            cls_id = self.player.stats.get("class", "warrior")
            node = get_node_by_id(cls_id, nid)
            if node:
                branch = node.get("branch", "origin")
            if branch in self._hidden_branches:
                continue
            sx, sy = self._l2c(*self._positions[nid])
            gr = nr + 4 + pulse_t * 2
            self.canvas.create_oval(sx - gr, sy - gr, sx + gr, sy + gr,
                                    outline=pulse_color, width=2, dash=(3, 3),
                                    tags=("pulse_glow",))

    # ── right-click context menu ──

    def _on_right_click(self, event):
        """Show context menu on right-click near a node."""
        cx = self.canvas.canvasx(event.x)
        cy = self.canvas.canvasy(event.y)

        best_id = None
        best_d = float("inf")
        threshold = NODE_R * self._zoom * 2

        for nid, (lx, ly) in self._positions.items():
            nx, ny = self._l2c(lx, ly)
            d = math.hypot(cx - nx, cy - ny)
            if d < best_d and d < threshold:
                best_d = d
                best_id = nid

        if not best_id:
            # Right-click on empty space: show branch filter menu
            self._show_branch_filter_menu(event)
            return

        cls_id = self.player.stats.get("class", "warrior")
        node = get_node_by_id(cls_id, best_id)
        if not node:
            return

        menu = tk.Menu(self.canvas, tearoff=0, bg="#2a2a2a", fg="#e0e0e0",
                       activebackground="#42A5F5", activeforeground="white",
                       font=self._fonts.get("small"))

        unlocked = set(get_unlocked_skills(self.player))

        # View details
        menu.add_command(
            label=f"📋 {node['name']} — Details",
            command=lambda: self._show_node_details(best_id))

        # Show path to node (if not unlocked)
        if best_id not in unlocked:
            menu.add_command(
                label="🔗 Show Path to Node",
                command=lambda: self._show_path_to(best_id))

        # Navigate to node
        menu.add_command(
            label="🎯 Center on Node",
            command=lambda nid=best_id: self._center_on_node(nid))

        menu.add_separator()

        # Show branch info
        branch = node.get("branch", "origin")
        if branch != "origin":
            menu.add_command(
                label=f"🌿 Filter: Show only '{branch}'",
                command=lambda b=branch: self._filter_branch_only(b))
            menu.add_command(
                label="👁 Show All Branches",
                command=self._show_all_branches)

        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def _show_node_details(self, node_id):
        """Show detailed info about a node in the detail bar."""
        cls_id = self.player.stats.get("class", "warrior")
        node = get_node_by_id(cls_id, node_id)
        if not node:
            return

        unlocked = set(get_unlocked_skills(self.player))
        avail_ids = {n["id"] for n in get_available_skills(self.player)}

        status = "UNLOCKED ✅" if node_id in unlocked else ("AVAILABLE 🔓" if node_id in avail_ids else "LOCKED 🔒")
        info = f"{node['name']} [{status}]  |  {node['description']}"
        info += f"\n  Type: {node['type'].capitalize()}  |  Tier: {node['tier']}  |  Cost: {node['cost']} SP  |  Branch: {node.get('branch', 'origin')}"

        # Show stat bonuses
        bonuses = []
        for key, val in node.items():
            if key in ("attack", "defense", "health_max") and val:
                bonuses.append(f"+{val} {key.replace('_', ' ').title()}")
        if bonuses:
            info += f"\n  Bonuses: {', '.join(bonuses)}"

        # Show prerequisites
        prereqs = node.get("prerequisites", [])
        if prereqs:
            prereq_names = []
            for pid in prereqs:
                pn = get_node_by_id(cls_id, pid)
                if pn:
                    met = "✅" if pid in unlocked else "❌"
                    prereq_names.append(f"{pn['name']} {met}")
                else:
                    prereq_names.append(pid)
            info += f"\n  Requires: {', '.join(prereq_names)}"

        # Show ability details for active nodes
        if node["type"] == "active":
            ab = node.get("ability", {})
            if ab:
                cd = ab.get("cooldown", "?")
                dur = ab.get("duration", 0)
                val = ab.get("value", 0)
                info += f"\n  ⚡ Ability: CD {cd} turns"
                if dur:
                    info += f"  |  Duration: {dur} turns"
                if val:
                    info += f"  |  Value: {val}"

        fg_color = "#66BB6A" if node_id in unlocked else ("#42A5F5" if node_id in avail_ids else "#FF5555")
        self._det_lbl.config(text=info, fg=fg_color)

    def _show_path_to(self, target_id):
        """Highlight the BFS path from unlocked nodes to the target."""
        cls_id = self.player.stats.get("class", "warrior")
        tree = get_tree_for_class(cls_id)
        unlocked = set(get_unlocked_skills(self.player))
        self._path_nodes.clear()
        self._path_edges.clear()
        self._search_matches.clear()
        self._search_matches.add(target_id)
        self._find_path_to_node(cls_id, tree, unlocked, target_id)
        self._full_draw()
        node = get_node_by_id(cls_id, target_id)
        path_len = len(self._path_nodes)
        name = node["name"] if node else target_id
        self._det_lbl.config(
            text=f"🔗 Path to {name}: {path_len} node{'s' if path_len != 1 else ''} required",
            fg="#00E5FF")

    def _center_on_node(self, node_id):
        """Center the canvas view on a specific node."""
        if node_id in self._positions:
            lx, ly = self._positions[node_id]
            self._scroll_to_logical(lx, ly)
            self._draw_minimap()

    def _show_branch_filter_menu(self, event):
        """Show a menu for filtering branches on right-click on empty space."""
        cls_id = self.player.stats.get("class", "warrior")
        branches = CLASS_BRANCHES.get(cls_id, {})

        menu = tk.Menu(self.canvas, tearoff=0, bg="#2a2a2a", fg="#e0e0e0",
                       activebackground="#42A5F5", activeforeground="white",
                       font=self._fonts.get("small"))

        menu.add_command(label="👁 Show All Branches",
                         command=self._show_all_branches)
        menu.add_separator()

        for bname, bdef in branches.items():
            if bname == "origin":
                continue
            label = bdef.get("label", bname)
            hidden = bname in self._hidden_branches
            prefix = "◻️" if hidden else "✅"
            menu.add_command(
                label=f"{prefix} {label}",
                command=lambda b=bname: self._toggle_branch(b))

        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def _toggle_branch(self, branch_name):
        """Toggle visibility of a branch."""
        if branch_name in self._hidden_branches:
            self._hidden_branches.discard(branch_name)
        else:
            self._hidden_branches.add(branch_name)
        self._full_draw()

    def _filter_branch_only(self, branch_name):
        """Show only a single branch, hiding all others."""
        cls_id = self.player.stats.get("class", "warrior")
        branches = CLASS_BRANCHES.get(cls_id, {})
        self._hidden_branches = {b for b in branches if b != "origin" and b != branch_name}
        self._full_draw()

    def _show_all_branches(self):
        """Show all branches (clear filter)."""
        self._hidden_branches.clear()
        self._full_draw()

    # ── click handling ──

    def _handle_click(self, event):
        cx = self.canvas.canvasx(event.x)
        cy = self.canvas.canvasy(event.y)

        best_id = None
        best_d = float("inf")
        threshold = NODE_R * self._zoom * 2

        for nid, (lx, ly) in self._positions.items():
            nx, ny = self._l2c(lx, ly)
            d = math.hypot(cx - nx, cy - ny)
            if d < best_d and d < threshold:
                best_d = d
                best_id = nid

        if not best_id:
            return

        cls_id = self.player.stats.get("class", "warrior")
        node = get_node_by_id(cls_id, best_id)
        if not node:
            return

        unlocked = set(get_unlocked_skills(self.player))

        if best_id in unlocked:
            info = f"[UNLOCKED] {node['name']}  \u2014  {node['description']}"
            if node["type"] == "active":
                ab = node.get("ability", {})
                cd = self.player.state.get("cooldowns", {}).get(best_id, 0)
                info += f"\nCooldown: {'Ready!' if cd == 0 else f'{cd} turns'}"
                if ab.get("combat"):
                    info += "  |  Combat ability"
            self._det_lbl.config(text=info, fg="#66BB6A")
            return

        avail_ids = {n["id"] for n in get_available_skills(self.player)}
        if best_id not in avail_ids:
            unmet = []
            for pid in node.get("prerequisites", []):
                if pid not in unlocked:
                    pn = get_node_by_id(cls_id, pid)
                    unmet.append(pn["name"] if pn else pid)
            sp = self.player.stats.get("skill_points", 0)
            info = f"[LOCKED] {node['name']}  \u2014  {node['description']}\n"
            if unmet:
                info += f"Requires: {', '.join(unmet)}  "
            if sp < node["cost"]:
                info += f"(Need {node['cost']} SP, have {sp})"
            self._det_lbl.config(text=info, fg="#FF5555")
            return

        # attempt to unlock
        success, msg = unlock_skill(self.player, best_id)
        if success:
            self._det_lbl.config(
                text=f"UNLOCKED: {node['name']}!", fg="#FFD700")
            self._full_draw()
            self._update_sp()
            if self.engine and hasattr(self.engine, 'display_message'):
                self.engine.display_message(msg)
        else:
            self._det_lbl.config(text=msg, fg="#FF5555")

    # ── hover / tooltip ──

    def _on_hover(self, event):
        for tid in self._tip_ids:
            try:
                self.canvas.delete(tid)
            except Exception:
                pass
        self._tip_ids.clear()

        cx = self.canvas.canvasx(event.x)
        cy = self.canvas.canvasy(event.y)

        best_id = None
        best_d = float("inf")
        threshold = NODE_R * self._zoom * 2

        for nid, (lx, ly) in self._positions.items():
            nx, ny = self._l2c(lx, ly)
            d = math.hypot(cx - nx, cy - ny)
            if d < best_d and d < threshold:
                best_d = d
                best_id = nid

        if not best_id:
            return

        cls_id = self.player.stats.get("class", "warrior")
        node = get_node_by_id(cls_id, best_id)
        if not node:
            return

        unlocked = set(get_unlocked_skills(self.player))
        avail = {n["id"] for n in get_available_skills(self.player)}
        if best_id in unlocked:
            status = "✅ UNLOCKED"
        elif best_id in avail:
            status = "🔓 AVAILABLE"
        else:
            status = "🔒 LOCKED"

        tip = f"{node['name']} [{status}]"
        if node["type"] == "active":
            tip += "  \u26a1"
        tip += f"\n{node['cost']} SP  \u00b7  Tier {node['tier']}  \u00b7  {node.get('branch', 'origin')}"

        # Show stat bonuses in tooltip
        bonuses = []
        for key in ("attack", "defense", "health_max", "dexterity", "perception"):
            val = node.get(key)
            if val:
                bonuses.append(f"+{val} {key.replace('_', ' ').title()}")
        if bonuses:
            tip += f"\n{', '.join(bonuses)}"

        # Show prerequisites for locked nodes
        if best_id not in unlocked:
            prereqs = node.get("prerequisites", [])
            if prereqs:
                prereq_names = []
                for pid in prereqs:
                    pn = get_node_by_id(cls_id, pid)
                    met = "✅" if pid in unlocked else "❌"
                    prereq_names.append(f"{pn['name'] if pn else pid} {met}")
                tip += f"\nReqs: {', '.join(prereq_names)}"

        # draw tooltip near mouse in canvas coords
        dcx = self.canvas.canvasx(event.x + 18)
        dcy = self.canvas.canvasy(event.y - 10)
        text_id = self.canvas.create_text(
            dcx, dcy, text=tip, anchor="nw",
            font=self._fonts["small"], fill="#e0e0e0")
        bbox = self.canvas.bbox(text_id)
        if bbox:
            bg_id = self.canvas.create_rectangle(
                bbox[0] - 5, bbox[1] - 3, bbox[2] + 5, bbox[3] + 3,
                fill="#2a2a2a", outline="#444444")
            self.canvas.tag_raise(text_id)
            self._tip_ids.extend([bg_id, text_id])
        else:
            self._tip_ids.append(text_id)

    # ── search & path highlighting ──

    def _focus_search(self):
        """Focus the search entry (Ctrl+F shortcut)."""
        if self._search_entry:
            self._search_entry.focus_set()
            self._search_entry.select_range(0, "end")

    def _search_nodes(self):
        """Filter nodes by search text, highlight matches, and show path to first match."""
        if not self.canvas or not self._search_var:
            return
        query = self._search_var.get().strip().lower()
        self._search_matches.clear()
        self._path_nodes.clear()
        self._path_edges.clear()

        if not query or len(query) < 2:
            self._full_draw()
            self._det_lbl.config(
                text="Drag to pan  \u00b7  Scroll to zoom  \u00b7  Click a node to view or unlock",
                fg="#777777")
            return

        cls_id = self.player.stats.get("class", "warrior")
        tree = get_tree_for_class(cls_id)
        if not tree:
            return

        # Find matching nodes (name, description, branch, or id)
        for node in tree:
            name = node.get("name", "").lower()
            desc = node.get("description", "").lower()
            branch = node.get("branch", "").lower()
            nid = node["id"].lower()
            if query in name or query in desc or query in branch or query in nid:
                self._search_matches.add(node["id"])

        if not self._search_matches:
            self._full_draw()
            self._det_lbl.config(text=f"No nodes matching \"{query}\"", fg="#FF5555")
            return

        # Build path from nearest unlocked node to first match
        unlocked = set(get_unlocked_skills(self.player))
        # Find the "best" match to path-find to (prefer available > locked, lower tier)
        target = None
        best_prio = (999, 999)
        avail_ids = {n["id"] for n in get_available_skills(self.player)}
        for nid in self._search_matches:
            node = get_node_by_id(cls_id, nid)
            if not node:
                continue
            prio = (0 if nid in avail_ids else 1, node["tier"])
            if prio < best_prio:
                best_prio = prio
                target = nid

        if target and target not in unlocked:
            self._find_path_to_node(cls_id, tree, unlocked, target)

        # Scroll to center on first match
        if target and target in self._positions:
            lx, ly = self._positions[target]
            self._scroll_to_logical(lx, ly)

        self._full_draw()
        count = len(self._search_matches)
        names = []
        for nid in sorted(self._search_matches):
            node = get_node_by_id(cls_id, nid)
            if node:
                names.append(node["name"])
        name_list = ", ".join(names[:5])
        if len(names) > 5:
            name_list += f" ... (+{len(names) - 5} more)"
        self._det_lbl.config(
            text=f"🔍 Found {count} node{'s' if count != 1 else ''}: {name_list}",
            fg="#FFD700")

    def _clear_search(self):
        """Clear search highlights and reset view."""
        if self._search_var:
            self._search_var.set("")
        self._search_matches.clear()
        self._path_nodes.clear()
        self._path_edges.clear()
        if self.canvas:
            self._full_draw()
        if self._det_lbl:
            self._det_lbl.config(
                text="Drag to pan  \u00b7  Scroll to zoom  \u00b7  Click a node to view or unlock",
                fg="#777777")

    def _find_path_to_node(self, cls_id, tree, unlocked, target_id):
        """BFS from all unlocked nodes to find the shortest prerequisite
        path to the target node. Populates _path_nodes and _path_edges."""
        # Build adjacency: node -> list of nodes it unlocks (children)
        # and reverse: node -> prerequisites (parents)
        parents = {}  # node_id -> list of prerequisite node_ids
        for node in tree:
            parents[node["id"]] = node.get("prerequisites", [])

        # BFS backward from target through prerequisite chains
        # We want: target <- prereq <- prereq <- ... <- unlocked_node
        from collections import deque
        queue = deque()
        queue.append(target_id)
        visited = {target_id}
        came_from = {target_id: None}

        found_start = None
        while queue:
            current = queue.popleft()
            if current in unlocked:
                found_start = current
                break
            for pid in parents.get(current, []):
                if pid not in visited:
                    visited.add(pid)
                    came_from[pid] = current
                    queue.append(pid)

        if found_start is None:
            # Also try forward BFS: from unlocked nodes forward through the tree
            # Build children map
            children = {}
            for node in tree:
                for pid in node.get("prerequisites", []):
                    children.setdefault(pid, []).append(node["id"])

            queue = deque()
            visited.clear()
            came_from.clear()
            for nid in unlocked:
                queue.append(nid)
                visited.add(nid)
                came_from[nid] = None

            while queue:
                current = queue.popleft()
                if current == target_id:
                    found_start = target_id
                    break
                for child_id in children.get(current, []):
                    if child_id not in visited:
                        visited.add(child_id)
                        came_from[child_id] = current
                        queue.append(child_id)

            if found_start == target_id:
                # Reconstruct forward path
                path = []
                cur = target_id
                while cur is not None:
                    path.append(cur)
                    cur = came_from.get(cur)
                path.reverse()
                # Remove unlocked nodes from path display (except endpoints)
                for nid in path:
                    if nid not in unlocked or nid == path[0]:
                        self._path_nodes.add(nid)
                    else:
                        self._path_nodes.add(nid)  # show full chain
                for i in range(len(path) - 1):
                    self._path_edges.add((path[i], path[i + 1]))
                return

            return

        # Reconstruct backward path
        path = []
        cur = found_start
        while cur is not None:
            path.append(cur)
            cur = came_from.get(cur)
        # path goes: unlocked_node -> ... -> target
        for nid in path:
            self._path_nodes.add(nid)
        for i in range(len(path) - 1):
            self._path_edges.add((path[i], path[i + 1]))

    def _scroll_to_logical(self, lx, ly):
        """Scroll the canvas to center on a logical coordinate."""
        if not self.canvas:
            return
        cx, cy = self._l2c(lx, ly)
        # Get canvas visible area
        try:
            sr_str = self.canvas.cget("scrollregion")
            if not sr_str:
                return
            sr = [float(x) for x in sr_str.split()]
            sw, sh = sr[2] - sr[0], sr[3] - sr[1]
            cw = self.canvas.winfo_width()
            ch = self.canvas.winfo_height()
            # Target fraction to place the point at center
            fx = (cx - sr[0] - cw / 2) / sw if sw > 0 else 0
            fy = (cy - sr[1] - ch / 2) / sh if sh > 0 else 0
            self.canvas.xview_moveto(max(0, min(1, fx)))
            self.canvas.yview_moveto(max(0, min(1, fy)))
        except Exception:
            pass

    def _minimap_click(self, event):
        """Click on minimap to navigate the main canvas to that position."""
        if not self.canvas or not self.minimap:
            return
        cls_id = self.player.stats.get("class", "warrior")
        tree = get_tree_for_class(cls_id)
        if not tree:
            return
        max_t = max((n["tier"] for n in tree), default=1)
        world_ext = (max_t + 1.5) * RING_GAP * 2
        scale = MINIMAP_W / world_ext
        half = MINIMAP_W / 2
        # Convert minimap click to logical coords
        lx = (event.x - half) / scale + LCENTER
        ly = (event.y - half) / scale + LCENTER
        self._scroll_to_logical(lx, ly)
        self._draw_minimap()

        self._full_draw()
        self._update_sp()
