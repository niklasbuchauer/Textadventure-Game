"""
Skill Tree System
=================
Class-based skill trees with tiered nodes (radial layout):
  - Passive nodes: permanent stat bonuses
  - Active nodes: usable abilities with cooldowns

Each class (Warrior, Rogue, Mage) has 200+ nodes across 5 tiers,
arranged in branches radiating from a center origin node.

The graphical skill tree window uses Pygame with a radial constellation
layout supporting pan/zoom.
"""

import math

from skill_tree_data import (
    WARRIOR_TREE, ROGUE_TREE, MAGE_TREE,
    SKILL_TREES_DATA, CLASS_BRANCHES,
    WARRIOR_BRANCHES, ROGUE_BRANCHES, MAGE_BRANCHES,
    MANA_COSTS,
)

# =====================================================================
# SYNERGY / SET BONUSES
# =====================================================================

SYNERGY_THRESHOLDS = [
    (3,  "Initiate",    {"attack": 1, "defense": 1}),
    (5,  "Adept",       {"attack": 2, "defense": 1, "health_max_bonus": 5}),
    (8,  "Expert",      {"attack": 3, "defense": 2, "health_max_bonus": 10, "crit_chance_bonus": 0.02}),
    (12, "Master",      {"attack": 5, "defense": 3, "health_max_bonus": 20, "crit_chance_bonus": 0.05}),
]

BRANCH_SYNERGY_EXTRAS = {
    "berserker":    {3: {"attack": 1}, 5: {"attack": 2},  8: {"crit_chance_bonus": 0.03}},
    "tank":         {3: {"defense": 2}, 5: {"defense": 3}, 8: {"health_max_bonus": 15}},
    "archer":       {3: {"attack": 1}, 5: {"crit_chance_bonus": 0.02}, 8: {"attack": 3}},
    "commander":    {3: {"defense": 1}, 5: {"attack": 1, "defense": 1}, 8: {"health_max_bonus": 10}},
    "weaponmaster": {3: {"attack": 2}, 5: {"attack": 2}, 8: {"crit_chance_bonus": 0.04}},
    "gladiator":    {3: {"health_max_bonus": 5}, 5: {"attack": 2}, 8: {"defense": 3}},
    "assassin":     {3: {"attack": 2}, 5: {"crit_chance_bonus": 0.03}, 8: {"attack": 4}},
    "trickster":    {3: {"defense": 1}, 5: {"defense": 2}, 8: {"attack": 2, "defense": 2}},
    "thief":        {3: {"crit_chance_bonus": 0.01}, 5: {"crit_chance_bonus": 0.02}, 8: {"attack": 2}},
    "bounty_hunter":{3: {"attack": 1}, 5: {"attack": 2}, 8: {"health_max_bonus": 10}},
    "phantom":      {3: {"defense": 1}, 5: {"attack": 2}, 8: {"crit_chance_bonus": 0.03}},
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
    counts = get_branch_counts(player)
    total = {}
    descriptions = []

    for branch, count in counts.items():
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

        extras = BRANCH_SYNERGY_EXTRAS.get(branch, {})
        for thresh, bonus in sorted(extras.items()):
            if count >= thresh:
                for stat, val in bonus.items():
                    total[stat] = total.get(stat, 0) + val

    return total, descriptions


def apply_synergy_bonuses(player):
    old_synergy = player.state.get("_synergy_bonuses", {})
    new_synergy, descriptions = get_synergy_bonuses(player)

    for stat, val in old_synergy.items():
        if stat == "health_max_bonus":
            player.stats["health_max"] = player.stats.get("health_max", 100) - val
            player.stats["health"] = min(player.stats.get("health", 100), player.stats.get("health_max", 100))
        else:
            player.stats[stat] = player.stats.get(stat, 0) - val

    for stat, val in new_synergy.items():
        if stat == "health_max_bonus":
            player.stats["health_max"] = player.stats.get("health_max", 100) + val
            player.stats["health"] = min(player.stats.get("health", 100) + val, player.stats.get("health_max", 100))
        else:
            player.stats[stat] = player.stats.get(stat, 0) + val

    player.state["_synergy_bonuses"] = new_synergy
    player.state["_synergy_descriptions"] = descriptions
    return new_synergy, descriptions


# =====================================================================
# SKILL TREES REGISTRY
# =====================================================================

SKILL_TREES = SKILL_TREES_DATA


# =====================================================================
# SKILL TREE LOGIC
# =====================================================================

def get_tree_for_class(class_id):
    return SKILL_TREES.get(class_id, [])


def get_node_by_id(class_id, node_id):
    tree = get_tree_for_class(class_id)
    for node in tree:
        if node["id"] == node_id:
            return node
    return None


def get_all_nodes_by_id(class_id):
    return {n["id"]: n for n in get_tree_for_class(class_id)}


def get_unlocked_skills(player):
    return list(player.state.get("unlocked_skills", []))


def is_skill_unlocked(player, skill_id):
    return skill_id in player.state.get("unlocked_skills", [])


def get_available_skills(player):
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

    player.stats["skill_points"] = sp - node["cost"]
    if "unlocked_skills" not in player.state:
        player.state["unlocked_skills"] = []
    player.state["unlocked_skills"].append(skill_id)

    for stat, value in node.get("stat_bonuses", {}).items():
        if stat == "health_max_bonus":
            player.stats["health_max"] = player.stats.get("health_max", 100) + value
            player.stats["health"] = min(
                player.stats.get("health", 100) + value,
                player.stats.get("health_max", 100))
        elif stat in ("crafting_bonus", "crit_chance_bonus", "disarm_bonus"):
            player.stats[stat] = player.stats.get(stat, 0) + value
        else:
            player.stats[stat] = player.stats.get(stat, 0) + value

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

    synergy_bonuses, synergy_descs = apply_synergy_bonuses(player)
    if synergy_descs:
        branch = node.get("branch", "origin")
        branch_count = get_branch_counts(player).get(branch, 0)
        for threshold, rank, _ in SYNERGY_THRESHOLDS:
            if branch_count == threshold and branch != "origin":
                result += f"\n  \u2605 SYNERGY BONUS: {branch.replace('_', ' ').title()} {rank}!\n"
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
            ability["mana_cost"] = MANA_COSTS.get(node["id"], ability.get("mana_cost", 0))
            abilities.append(ability)
    return abilities


def use_ability(player, ability_name):
    abilities = get_active_abilities(player)
    if not abilities:
        return False, "You don't have any active abilities yet.", None

    search = ability_name.lower().replace("_", " ").strip()
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

    cooldowns = player.state.get("cooldowns", {})
    cd_key = found["skill_id"]
    remaining = cooldowns.get(cd_key, 0)
    if remaining > 0:
        return False, f"{found['name']} is on cooldown ({remaining} turns remaining).", None

    mana_cost = found.get("mana_cost", 0)
    current_mana = player.stats.get("mana", 0)
    if mana_cost > 0 and current_mana < mana_cost:
        return False, f"Not enough mana!  {found['name']} requires {mana_cost} MP  (you have {current_mana}).", None

    if mana_cost > 0:
        player.stats["mana"] = current_mana - mana_cost

    effect = found.get("effect", "")
    if "cooldowns" not in player.state:
        player.state["cooldowns"] = {}
    player.state["cooldowns"][cd_key] = found.get("cooldown", 10)

    combat_effects = (
        "combat_damage", "combat_crit_attack", "combat_stun",
        "combat_poison", "combat_freeze_attack", "combat_damage_burn",
        "combat_damage_stun", "combat_heal", "combat_execute",
        "combat_bleed_attack", "guaranteed_flee", "buff_attack",
        "extra_gold", "restore_mana"
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
    elif effect == "restore_mana":
        max_mana = player.stats.get("max_mana", 0)
        restore_amt = max(1, int(max_mana * value))
        player.stats["mana"] = min(player.stats.get("mana", 0) + restore_amt, max_mana)
    player.state["active_effects"] = active_effects


def tick_effects(player):
    messages = []
    cooldowns = player.state.get("cooldowns", {})
    expired_cds = []
    for key in list(cooldowns.keys()):
        cooldowns[key] -= 1
        if cooldowns[key] <= 0:
            expired_cds.append(key)
    for key in expired_cds:
        del cooldowns[key]

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

    for key in ("reveal_traps", "reveal_floor"):
        if key in active:
            del active[key]

    player.state["active_effects"] = active
    return messages


def has_active_effect(player, effect_name):
    active = player.state.get("active_effects", {})
    val = active.get(effect_name, 0)
    if isinstance(val, dict):
        return val.get("duration", 0) > 0
    return val > 0


# =====================================================================
# GRAPHICAL SKILL TREE WINDOW — Pygame Radial Constellation Layout
# =====================================================================

import pygame
import pygame_gui
from pygame_gui.elements import (
    UIButton, UILabel, UIWindow, UIImage, UITextEntryLine,
)

NODE_R = 18
RING_GAP = 110
LOGICAL_SIZE = 3000
LCENTER = LOGICAL_SIZE // 2
MINIMAP_W = 180

CLASS_BG = {
    "warrior": (15, 13, 8),
    "rogue":   (8, 13, 15),
    "mage":    (13, 8, 15),
}


def _hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


class SkillTreeWindow:
    """Radial constellation skill tree with pan, zoom, minimap and
    class-themed visuals (hexagons / diamonds / circles). Pygame version."""

    def __init__(self, app, player, engine=None):
        self.app = app
        self.manager = app.manager
        self.player = player
        self.engine = engine
        self.window = None
        self._canvas_image = None       # UIImage for main canvas
        self._canvas_surf = None        # Surface to draw on
        self._minimap_image = None      # UIImage for minimap overlay
        self._minimap_surf = None
        self._sp_label = None
        self._det_label = None
        self._zoom_label_el = None
        self._search_entry = None

        self._positions = {}            # node_id -> (lx, ly) logical
        self._zoom = 1.0
        self._cam_x = float(LCENTER)    # camera center in logical coords
        self._cam_y = float(LCENTER)
        self._drag_start = None
        self._did_drag = False

        self._search_matches = set()
        self._path_nodes = set()
        self._path_edges = set()
        self._hidden_branches = set()
        self._pulse_phase = 0
        self._pulse_timer = 0.0         # accumulator for pulse timing
        self._needs_redraw = True
        self._last_canvas_size = (0, 0)
        self._tooltip_text = ""
        self._tooltip_pos = (0, 0)
        self._det_text = ""
        self._det_color = (119, 119, 119)

        # fonts (initialised lazily)
        self._fonts = {}

    def _init_fonts(self):
        if self._fonts:
            return
        self._fonts = {
            "title":  pygame.font.SysFont("segoeui", 12),
            "bold":   pygame.font.SysFont("segoeui", 10),
            "normal": pygame.font.SysFont("segoeui", 9),
            "small":  pygame.font.SysFont("segoeui", 8),
            "tiny":   pygame.font.SysFont("segoeui", 7),
        }

    def is_open(self):
        return self.window is not None and self.window.alive()

    # ── window lifecycle ──────────────────────────────────────────────────────

    def create_window(self):
        if self.is_open():
            return

        self._init_fonts()
        cls_id = self.player.stats.get("class", "warrior")
        cls_name = cls_id.capitalize()

        W, H = self.app.width, self.app.height
        ww, wh = min(1600, W - 40), min(900, H - 40)
        self.window = UIWindow(
            rect=pygame.Rect((W - ww) // 2, (H - wh) // 2, ww, wh),
            manager=self.manager,
            window_display_title=f"Skill Tree \u2014 {cls_name}",
            resizable=True,
        )
        iw = ww - 60

        # Top bar: class name, level, SP
        y = 4
        self._cls_label = UILabel(
            relative_rect=pygame.Rect(10, y, 200, 20),
            text=f"{cls_name} Skill Tree",
            manager=self.manager, container=self.window,
        )
        self._lvl_label = UILabel(
            relative_rect=pygame.Rect(220, y, 120, 20),
            text=f"Level {self.player.stats.get('level', 1)}",
            manager=self.manager, container=self.window,
        )
        self._sp_label = UILabel(
            relative_rect=pygame.Rect(iw - 160, y, 160, 20),
            text=f"Skill Points: {self.player.stats.get('skill_points', 0)}",
            manager=self.manager, container=self.window,
        )

        # Toolbar: zoom buttons + search
        y = 26
        btn_w = 30
        self._btn_zoom_out = UIButton(
            relative_rect=pygame.Rect(10, y, btn_w, 22),
            text="\u2212", manager=self.manager, container=self.window,
        )
        self._btn_zoom_in = UIButton(
            relative_rect=pygame.Rect(42, y, btn_w, 22),
            text="+", manager=self.manager, container=self.window,
        )
        self._btn_zoom_home = UIButton(
            relative_rect=pygame.Rect(74, y, btn_w, 22),
            text="\u2299", manager=self.manager, container=self.window,
        )

        self._search_entry = UITextEntryLine(
            relative_rect=pygame.Rect(120, y, 180, 22),
            manager=self.manager, container=self.window,
            placeholder_text="Search skills...",
        )

        # Canvas area
        canvas_y = 52
        canvas_h = wh - 130 - canvas_y
        canvas_w = iw
        self._canvas_rect = pygame.Rect(10, canvas_y, canvas_w, canvas_h)
        self._canvas_surf = pygame.Surface((canvas_w, canvas_h))
        self._canvas_image = UIImage(
            relative_rect=self._canvas_rect,
            image_surface=self._canvas_surf,
            manager=self.manager, container=self.window,
        )

        # Minimap (overlaid in bottom-right of canvas)
        mm_x = canvas_w - MINIMAP_W - 2
        mm_y = canvas_y + canvas_h - MINIMAP_W - 2
        self._minimap_surf = pygame.Surface((MINIMAP_W, MINIMAP_W))
        self._minimap_image = UIImage(
            relative_rect=pygame.Rect(mm_x, mm_y, MINIMAP_W, MINIMAP_W),
            image_surface=self._minimap_surf,
            manager=self.manager, container=self.window,
        )

        # Detail bar
        self._det_label = UILabel(
            relative_rect=pygame.Rect(10, wh - 130 + 4, iw, 40),
            text="Drag to pan  \u00b7  Scroll to zoom  \u00b7  Click a node to view or unlock",
            manager=self.manager, container=self.window,
        )
        self._det_text = "Drag to pan  \u00b7  Scroll to zoom  \u00b7  Click a node to view or unlock"
        self._det_color = (119, 119, 119)

        # Compute layout
        self._compute_positions()
        self._cam_x = float(LCENTER)
        self._cam_y = float(LCENTER)
        self._needs_redraw = True
        self.redraw()

    def close_window(self):
        if self.window and self.window.alive():
            self.window.kill()
        self.window = None
        self._canvas_image = None
        self._minimap_image = None

    def _update_sp(self):
        sp = self.player.stats.get("skill_points", 0)
        if self._sp_label and self._sp_label.alive():
            self._sp_label.set_text(f"Skill Points: {sp}")

    # ── position computation ──

    def _compute_positions(self):
        cls_id = self.player.stats.get("class", "warrior")
        tree = get_tree_for_class(cls_id)
        branches = CLASS_BRANCHES.get(cls_id, {})

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

    def _l2s(self, lx, ly):
        """Logical → screen (surface) coordinates."""
        if not self._canvas_surf:
            return 0, 0
        sw, sh = self._canvas_surf.get_size()
        sx = (lx - self._cam_x) * self._zoom + sw / 2
        sy = (ly - self._cam_y) * self._zoom + sh / 2
        return sx, sy

    def _s2l(self, sx, sy):
        """Screen (surface) → logical coordinates."""
        if not self._canvas_surf:
            return LCENTER, LCENTER
        sw, sh = self._canvas_surf.get_size()
        lx = (sx - sw / 2) / self._zoom + self._cam_x
        ly = (sy - sh / 2) / self._zoom + self._cam_y
        return lx, ly

    # ── event handling ──

    def handle_event(self, event):
        if not self.is_open():
            return

        # Button presses
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self._btn_zoom_in:
                self._apply_zoom(1.20)
            elif event.ui_element == self._btn_zoom_out:
                self._apply_zoom(1 / 1.20)
            elif event.ui_element == self._btn_zoom_home:
                self._zoom_home()
            return

        # Search text changed
        if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
            if event.ui_element == self._search_entry:
                self._search_nodes()
            return

        # Mouse wheel zoom over canvas
        if event.type == pygame.MOUSEWHEEL:
            if self._is_mouse_over_canvas():
                factor = 1.15 if event.y > 0 else 1 / 1.15
                self._apply_zoom(factor)
            return

        # Click-drag pan / click-to-select
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._is_mouse_over_canvas():
                self._drag_start = pygame.mouse.get_pos()
                self._did_drag = False
            elif self._is_mouse_over_minimap():
                self._minimap_click(pygame.mouse.get_pos())
            return

        if event.type == pygame.MOUSEMOTION:
            if self._drag_start:
                mx, my = pygame.mouse.get_pos()
                dx = mx - self._drag_start[0]
                dy = my - self._drag_start[1]
                if abs(dx) > 3 or abs(dy) > 3:
                    self._did_drag = True
                self._cam_x -= dx / self._zoom
                self._cam_y -= dy / self._zoom
                self._drag_start = (mx, my)
                self._needs_redraw = True
                self.redraw()
            return

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self._drag_start:
                if not self._did_drag:
                    self._handle_click()
                self._drag_start = None
                self._needs_redraw = True
                self.redraw()
            return

    def _is_mouse_over_canvas(self):
        if not self._canvas_image or not self._canvas_image.alive():
            return False
        mx, my = pygame.mouse.get_pos()
        return self._canvas_image.get_abs_rect().collidepoint(mx, my)

    def _is_mouse_over_minimap(self):
        if not self._minimap_image or not self._minimap_image.alive():
            return False
        mx, my = pygame.mouse.get_pos()
        return self._minimap_image.get_abs_rect().collidepoint(mx, my)

    # ── tick (for pulse animation) ──

    def tick(self, dt):
        """Call from main loop with frame delta time. Drives pulse."""
        if not self.is_open():
            return
        self._pulse_timer += dt
        if self._pulse_timer >= 0.15:
            self._pulse_timer -= 0.15
            self._pulse_phase = (self._pulse_phase + 1) % 16
            self._needs_redraw = True
            self.redraw()

    # ── zoom / pan ──

    def _apply_zoom(self, factor):
        new_z = self._zoom * factor
        if new_z < 0.2 or new_z > 3.0:
            return
        self._zoom = new_z
        self._needs_redraw = True
        self.redraw()

    def _zoom_home(self):
        self._zoom = 1.0
        self._cam_x = float(LCENTER)
        self._cam_y = float(LCENTER)
        self._needs_redraw = True
        self.redraw()

    # ── rendering ──

    def redraw(self):
        if not self.is_open() or not self._canvas_surf:
            return
        if not self._needs_redraw:
            return
        self._needs_redraw = False

        self._full_draw()
        self._draw_minimap()

        if self._canvas_image and self._canvas_image.alive():
            self._canvas_image.set_image(self._canvas_surf)
        if self._minimap_image and self._minimap_image.alive():
            self._minimap_image.set_image(self._minimap_surf)

    def _full_draw(self):
        surf = self._canvas_surf
        sw, sh = surf.get_size()
        cls_id = self.player.stats.get("class", "warrior")
        bg = CLASS_BG.get(cls_id, (13, 13, 13))
        surf.fill(bg)

        tree = get_tree_for_class(cls_id)
        unlocked = set(get_unlocked_skills(self.player))
        avail = {n["id"] for n in get_available_skills(self.player)}
        branches = CLASS_BRANCHES.get(cls_id, {})
        z = self._zoom

        if not tree:
            txt = self._fonts["bold"].render("No skill tree available.", True, (255, 255, 255))
            surf.blit(txt, (sw // 2 - txt.get_width() // 2, sh // 2))
            return

        max_t = max(n["tier"] for n in tree)
        ccx, ccy = self._l2s(LCENTER, LCENTER)

        # Ring guides
        for t in range(1, max_t + 1):
            r = int(t * RING_GAP * z)
            if r > 4:
                center = (int(ccx), int(ccy))
                if -r < ccx < sw + r and -r < ccy < sh + r:
                    pygame.draw.circle(surf, (22, 22, 22), center, r, 1)

        # Branch separators & labels
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
            sep_color = (24, 24, 24) if bname not in self._hidden_branches else (13, 13, 13)
            pygame.draw.line(surf, sep_color, (int(ccx), int(ccy)), (int(ex), int(ey)), 1)

            mid = math.radians((bdef["angle_start"] + bdef["angle_end"]) / 2)
            lr = (max_t + 1.3) * RING_GAP * z
            lx = ccx + lr * math.cos(mid)
            ly = ccy + lr * math.sin(mid)
            bc = branch_counts.get(bname, 0)
            buc = branch_unlocked_counts.get(bname, 0)
            label_text = bdef["label"]
            if z >= 0.4:
                label_text += f" ({buc}/{bc})"
            label_color = _hex_to_rgb(bdef["color"]) if bname not in self._hidden_branches else (51, 51, 51)
            txt = self._fonts["small"].render(label_text, True, label_color)
            surf.blit(txt, (int(lx) - txt.get_width() // 2, int(ly) - txt.get_height() // 2))

        # Connections
        for node in tree:
            nid = node["id"]
            if nid not in self._positions:
                continue
            ncx, ncy = self._l2s(*self._positions[nid])
            for pid in node.get("prerequisites", []):
                if pid not in self._positions:
                    continue
                pcx, pcy = self._l2s(*self._positions[pid])
                both = nid in unlocked and pid in unlocked
                on_path = (pid, nid) in self._path_edges or (nid, pid) in self._path_edges
                if on_path:
                    color = (255, 215, 0)
                    w = 3
                elif both:
                    color = (58, 122, 58)
                    w = 2
                else:
                    color = (42, 42, 42)
                    w = 1
                pygame.draw.line(surf, color, (int(pcx), int(pcy)), (int(ncx), int(ncy)), w)

        # Nodes
        nr = NODE_R * z
        pulse_t = abs((self._pulse_phase % 16) - 8) / 8.0
        pulse_alpha = 0.3 + 0.7 * pulse_t
        pulse_color = (int(66 * pulse_alpha), int(165 * pulse_alpha), int(245 * pulse_alpha))

        icon_font = self._fonts["tiny"]

        for node in tree:
            nid = node["id"]
            if nid not in self._positions:
                continue
            sx, sy = self._l2s(*self._positions[nid])
            isx, isy = int(sx), int(sy)

            # Viewport culling
            if isx < -60 or isx > sw + 60 or isy < -60 or isy > sh + 60:
                continue

            branch = node.get("branch", "origin")
            branch_hidden = branch in self._hidden_branches and branch != "origin"

            is_search_match = nid in self._search_matches if self._search_matches else False
            is_on_path = nid in self._path_nodes if self._path_nodes else False
            dimmed = (bool(self._search_matches) and not is_search_match and not is_on_path) or branch_hidden

            # State colours
            if nid in unlocked:
                if node["type"] == "active":
                    fill, out = (74, 42, 0), (255, 152, 0)
                else:
                    fill, out = (26, 74, 26), (102, 187, 106)
            elif nid in avail:
                fill, out = (26, 58, 90), (66, 165, 245)
            else:
                fill, out = (42, 42, 42), (68, 68, 68)

            if dimmed:
                fill = (26, 26, 26)
                out = (42, 42, 42)

            # Search match glow
            if is_search_match:
                gr = int(nr + 7)
                pygame.draw.circle(surf, (255, 215, 0), (isx, isy), gr, 3)

            # Path highlight glow
            if is_on_path and not is_search_match:
                gr = int(nr + 5)
                pygame.draw.circle(surf, (0, 229, 255), (isx, isy), gr, 2)

            # Available pulse glow
            if nid in avail and not dimmed:
                gr = int(nr + 4 + pulse_t * 2)
                pygame.draw.circle(surf, pulse_color, (isx, isy), gr, 2)

            # Origin node is larger
            r = int(nr * 1.6) if node["tier"] == 0 else int(nr)

            # Draw node shape
            self._draw_node_shape(surf, cls_id, isx, isy, r, fill, out)

            # Icon inside node
            if nid in unlocked and node["tier"] == 0:
                pass  # origin has no special icon when unlocked
            elif nid in avail and z >= 0.5:
                # show nothing special for available (glow is enough)
                pass

            # Name label
            if z >= 0.35:
                name = node["name"]
                if z < 0.7 and len(name) > 10:
                    name = name[:8] + ".."
                text_fill = (224, 224, 224)
                if dimmed:
                    text_fill = (85, 85, 85)
                elif is_search_match:
                    text_fill = (255, 215, 0)

                max_w = max(20, int(r * 2 - 4))
                # Simple word wrapping for node names
                words = name.split()
                lines = []
                current = ""
                for w in words:
                    test = (current + " " + w).strip()
                    tw = self._fonts["tiny"].size(test)[0]
                    if tw <= max_w or not current:
                        current = test
                    else:
                        lines.append(current)
                        current = w
                if current:
                    lines.append(current)

                total_h = len(lines) * self._fonts["tiny"].get_height()
                ty = isy - total_h // 2
                for line in lines:
                    txt = self._fonts["tiny"].render(line, True, text_fill)
                    surf.blit(txt, (isx - txt.get_width() // 2, ty))
                    ty += self._fonts["tiny"].get_height()

            # Active ability lightning bolt
            if node["type"] == "active" and z >= 0.5:
                txt = icon_font.render("\u26a1", True, (255, 152, 0))
                surf.blit(txt, (isx - txt.get_width() // 2, isy + r + int(6 * z)))

        # Legend at bottom-left
        self._draw_legend(surf, sw, sh)

    def _draw_node_shape(self, surf, cls_id, cx, cy, r, fill, outline):
        if cls_id == "warrior":
            pts = []
            for i in range(6):
                a = math.radians(60 * i - 30)
                pts.append((cx + int(r * math.cos(a)), cy + int(r * math.sin(a))))
            pygame.draw.polygon(surf, fill, pts)
            pygame.draw.polygon(surf, outline, pts, 2)
        elif cls_id == "rogue":
            pts = [(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)]
            pygame.draw.polygon(surf, fill, pts)
            pygame.draw.polygon(surf, outline, pts, 2)
        else:
            pygame.draw.circle(surf, fill, (cx, cy), r)
            pygame.draw.circle(surf, outline, (cx, cy), r, 2)

    def _draw_legend(self, surf, sw, sh):
        """Draw a small legend in the bottom-left corner."""
        items = [
            ("Locked",    (42, 42, 42), (68, 68, 68)),
            ("Available", (26, 58, 90), (66, 165, 245)),
            ("Unlocked",  (26, 74, 26), (102, 187, 106)),
            ("Active",    (74, 42, 0),  (255, 152, 0)),
        ]
        x, y = 10, sh - 24
        for label, fill, out in items:
            pygame.draw.circle(surf, fill, (x + 6, y + 6), 6)
            pygame.draw.circle(surf, out, (x + 6, y + 6), 6, 1)
            txt = self._fonts["tiny"].render(label, True, (136, 136, 136))
            surf.blit(txt, (x + 16, y + 1))
            x += txt.get_width() + 26

    # ── minimap ──

    def _draw_minimap(self):
        if not self._minimap_surf:
            return
        mm = self._minimap_surf
        mm.fill((17, 17, 17))

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
            mx = (lx - LCENTER) * scale + half
            my = (ly - LCENTER) * scale + half
            branch = node.get("branch", "origin")
            bdef = branches.get(branch, {})

            if nid in self._search_matches:
                color = (255, 215, 0)
                dr = 4
            elif nid in self._path_nodes:
                color = (0, 229, 255)
                dr = 3
            elif nid in unlocked:
                color = (102, 187, 106)
                dr = 2
            else:
                color = _hex_to_rgb(bdef.get("color", "#555555"))
                dr = 2
            pygame.draw.circle(mm, color, (int(mx), int(my)), dr)

        # Viewport rectangle
        if self._canvas_surf:
            csw, csh = self._canvas_surf.get_size()
            # Convert camera view to logical bounds
            vx0 = self._cam_x - csw / (2 * self._zoom)
            vy0 = self._cam_y - csh / (2 * self._zoom)
            vx1 = self._cam_x + csw / (2 * self._zoom)
            vy1 = self._cam_y + csh / (2 * self._zoom)
            rx0 = int((vx0 - LCENTER) * scale + half)
            ry0 = int((vy0 - LCENTER) * scale + half)
            rx1 = int((vx1 - LCENTER) * scale + half)
            ry1 = int((vy1 - LCENTER) * scale + half)
            rect = pygame.Rect(rx0, ry0, rx1 - rx0, ry1 - ry0)
            pygame.draw.rect(mm, (255, 215, 0), rect, 1)

        # Border
        pygame.draw.rect(mm, (51, 51, 51), (0, 0, MINIMAP_W, MINIMAP_W), 1)

    # ── minimap click ──

    def _minimap_click(self, mouse_pos):
        if not self._minimap_image or not self._minimap_image.alive():
            return
        abs_rect = self._minimap_image.get_abs_rect()
        local_x = mouse_pos[0] - abs_rect.x
        local_y = mouse_pos[1] - abs_rect.y

        cls_id = self.player.stats.get("class", "warrior")
        tree = get_tree_for_class(cls_id)
        if not tree:
            return
        max_t = max((n["tier"] for n in tree), default=1)
        world_ext = (max_t + 1.5) * RING_GAP * 2
        scale = MINIMAP_W / world_ext
        half = MINIMAP_W / 2

        self._cam_x = (local_x - half) / scale + LCENTER
        self._cam_y = (local_y - half) / scale + LCENTER
        self._needs_redraw = True
        self.redraw()

    # ── click handling ──

    def _handle_click(self):
        if not self._canvas_image or not self._canvas_image.alive():
            return
        mx, my = pygame.mouse.get_pos()
        abs_rect = self._canvas_image.get_abs_rect()
        local_x = mx - abs_rect.x
        local_y = my - abs_rect.y

        # Convert to logical coordinates
        lx, ly = self._s2l(local_x, local_y)

        # Find nearest node
        best_id = None
        best_d = float("inf")
        threshold = NODE_R * 2

        for nid, (nlx, nly) in self._positions.items():
            d = math.hypot(lx - nlx, ly - nly)
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
            self._set_detail(info, (102, 187, 106))
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
            self._set_detail(info, (255, 85, 85))
            return

        # Attempt to unlock
        success, msg = unlock_skill(self.player, best_id)
        if success:
            self._set_detail(f"UNLOCKED: {node['name']}!", (255, 215, 0))
            self._needs_redraw = True
            self._update_sp()
            self.redraw()
            if self.engine and hasattr(self.engine, 'display_message'):
                self.engine.display_message(msg)
        else:
            self._set_detail(msg, (255, 85, 85))

    def _set_detail(self, text, color):
        self._det_text = text
        self._det_color = color
        if self._det_label and self._det_label.alive():
            # Truncate to first line for the small label
            display = text.split("\n")[0]
            if len(display) > 120:
                display = display[:117] + "..."
            self._det_label.set_text(display)

    # ── search ──

    def _search_nodes(self):
        if not self._search_entry:
            return
        query = self._search_entry.get_text().strip().lower()
        self._search_matches.clear()
        self._path_nodes.clear()
        self._path_edges.clear()

        if not query or len(query) < 2:
            self._needs_redraw = True
            self._set_detail(
                "Drag to pan  \u00b7  Scroll to zoom  \u00b7  Click a node to view or unlock",
                (119, 119, 119))
            self.redraw()
            return

        cls_id = self.player.stats.get("class", "warrior")
        tree = get_tree_for_class(cls_id)
        if not tree:
            return

        for node in tree:
            name = node.get("name", "").lower()
            desc = node.get("description", "").lower()
            branch = node.get("branch", "").lower()
            nid = node["id"].lower()
            if query in name or query in desc or query in branch or query in nid:
                self._search_matches.add(node["id"])

        if not self._search_matches:
            self._needs_redraw = True
            self._set_detail(f'No nodes matching "{query}"', (255, 85, 85))
            self.redraw()
            return

        # Find best match to path-find to
        unlocked = set(get_unlocked_skills(self.player))
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

        # Center on first match
        if target and target in self._positions:
            self._cam_x, self._cam_y = self._positions[target]

        self._needs_redraw = True
        self.redraw()

        count = len(self._search_matches)
        names = []
        for nid in sorted(self._search_matches):
            node = get_node_by_id(cls_id, nid)
            if node:
                names.append(node["name"])
        name_list = ", ".join(names[:5])
        if len(names) > 5:
            name_list += f" ... (+{len(names) - 5} more)"
        self._set_detail(f"Found {count} node{'s' if count != 1 else ''}: {name_list}", (255, 215, 0))

    def _find_path_to_node(self, cls_id, tree, unlocked, target_id):
        from collections import deque
        parents = {}
        for node in tree:
            parents[node["id"]] = node.get("prerequisites", [])

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
                path = []
                cur = target_id
                while cur is not None:
                    path.append(cur)
                    cur = came_from.get(cur)
                path.reverse()
                for nid in path:
                    self._path_nodes.add(nid)
                for i in range(len(path) - 1):
                    self._path_edges.add((path[i], path[i + 1]))
                return
            return

        path = []
        cur = found_start
        while cur is not None:
            path.append(cur)
            cur = came_from.get(cur)
        for nid in path:
            self._path_nodes.add(nid)
        for i in range(len(path) - 1):
            self._path_edges.add((path[i], path[i + 1]))
