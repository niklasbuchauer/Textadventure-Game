"""
Companion / pet system.
"""

import time
import math as _math

PETS = {
    "spirit_wolf": {
        "name": "Spirit Wolf",
        "description": "A watchful companion that sharpens your instincts.",
        "bonus_stat": "perception",
        "tier": "common",
        "min_player_level": 1,
        "base_adoption_cost": 120,
        "material_cost": {},
    },
    "ember_fox": {
        "name": "Ember Fox",
        "description": "Fast and cunning, always one step ahead.",
        "bonus_stat": "dexterity",
        "tier": "common",
        "min_player_level": 1,
        "base_adoption_cost": 150,
        "material_cost": {},
    },
    "stone_turtle": {
        "name": "Stone Turtle",
        "description": "Slow, steady, and impossibly hard to break.",
        "bonus_stat": "defense",
        "tier": "common",
        "min_player_level": 1,
        "base_adoption_cost": 180,
        "material_cost": {},
    },
    "arcane_wisp": {
        "name": "Arcane Wisp",
        "description": "A drifting mote that hums with mana.",
        "bonus_stat": "max_mana",
        "tier": "rare",
        "min_player_level": 1,
        "base_adoption_cost": 220,
        "material_cost": {},
    },
    "luminous_raven": {
        "name": "Luminous Raven",
        "description": "A clever raven that can mend wounds with a soft glow.",
        "bonus_stat": "perception",
        "tier": "rare",
        "min_player_level": 1,
        "base_adoption_cost": 140,
        "material_cost": {},
    },
    "iron_badger": {
        "name": "Iron Badger",
        "description": "Short-tempered and armored with stubborn resolve.",
        "bonus_stat": "defense",
        "tier": "common",
        "min_player_level": 5,
        "base_adoption_cost": 220,
        "material_cost": {"iron_ingot": 3},
    },
    "mire_hound": {
        "name": "Mire Hound",
        "description": "Tracks prey through toxic marsh fog.",
        "bonus_stat": "perception",
        "tier": "common",
        "min_player_level": 5,
        "base_adoption_cost": 210,
        "material_cost": {"venom_sac": 1},
    },
    "spark_lizard": {
        "name": "Spark Lizard",
        "description": "Tiny body, dangerous charge.",
        "bonus_stat": "dexterity",
        "tier": "common",
        "min_player_level": 6,
        "base_adoption_cost": 240,
        "material_cost": {"copper_ingot": 4},
    },
    "frost_lynx": {
        "name": "Frost Lynx",
        "description": "A silent hunter cloaked in rime.",
        "bonus_stat": "dexterity",
        "tier": "rare",
        "min_player_level": 10,
        "base_adoption_cost": 420,
        "material_cost": {"frost_crystal": 2},
    },
    "thorn_stag": {
        "name": "Thorn Stag",
        "description": "Ancient antlers pulse with natural vigor.",
        "bonus_stat": "constitution",
        "tier": "rare",
        "min_player_level": 11,
        "base_adoption_cost": 460,
        "material_cost": {"living_bark": 2},
    },
    "storm_owl": {
        "name": "Storm Owl",
        "description": "Reads lightning before it falls.",
        "bonus_stat": "perception",
        "tier": "rare",
        "min_player_level": 12,
        "base_adoption_cost": 500,
        "material_cost": {"storm_feather": 2},
    },
    "brass_golemlet": {
        "name": "Brass Golemlet",
        "description": "A tiny automaton with a heroic punch.",
        "bonus_stat": "strength",
        "tier": "rare",
        "min_player_level": 13,
        "base_adoption_cost": 540,
        "material_cost": {"brass_plate": 3},
    },
    "sunscale_drake": {
        "name": "Sunscale Drake",
        "description": "A radiant drake that devours darkness.",
        "bonus_stat": "strength",
        "tier": "epic",
        "min_player_level": 18,
        "base_adoption_cost": 980,
        "material_cost": {"sun_shard": 2, "dragonscale": 2},
        "achievement_req": "dungeon_master",
    },
    "moonshade_panther": {
        "name": "Moonshade Panther",
        "description": "Steps between light and shadow.",
        "bonus_stat": "dexterity",
        "tier": "epic",
        "min_player_level": 18,
        "base_adoption_cost": 990,
        "material_cost": {"shadow_essence": 3},
        "achievement_req": "boss_slayer",
    },
    "tide_serpent": {
        "name": "Tide Serpent",
        "description": "Crashes with wave-forged momentum.",
        "bonus_stat": "max_mana",
        "tier": "epic",
        "min_player_level": 19,
        "base_adoption_cost": 1040,
        "material_cost": {"aqua_pearl": 2, "frost_crystal": 1},
    },
    "obsidian_ram": {
        "name": "Obsidian Ram",
        "description": "Breaks lines with volcanic force.",
        "bonus_stat": "defense",
        "tier": "epic",
        "min_player_level": 20,
        "base_adoption_cost": 1100,
        "material_cost": {"obsidian_shard": 4},
    },
    "aether_moth": {
        "name": "Aether Moth",
        "description": "Flutters through mana streams.",
        "bonus_stat": "max_mana",
        "tier": "epic",
        "min_player_level": 20,
        "base_adoption_cost": 1080,
        "material_cost": {"arcane_dust": 6},
    },
    "void_hound": {
        "name": "Void Hound",
        "description": "Hunts what reality forgets.",
        "bonus_stat": "perception",
        "tier": "legendary",
        "min_player_level": 25,
        "base_adoption_cost": 1750,
        "material_cost": {"void_essence": 5, "ancient_core": 1},
        "achievement_req": "void_titan_slayer",
    },
    "celestial_gryphon": {
        "name": "Celestial Gryphon",
        "description": "Carries the dawn on silver wings.",
        "bonus_stat": "strength",
        "tier": "legendary",
        "min_player_level": 26,
        "base_adoption_cost": 1820,
        "material_cost": {"star_fragment": 4, "sun_shard": 2},
        "achievement_req": "boss_slayer",
        "quest_req": "sky_trial",
    },
    "chrono_hare": {
        "name": "Chrono Hare",
        "description": "Outruns the next second.",
        "bonus_stat": "dexterity",
        "tier": "legendary",
        "min_player_level": 27,
        "base_adoption_cost": 1880,
        "material_cost": {"time_sand": 4, "arcane_dust": 4},
    },
    "worldroot_titanling": {
        "name": "Worldroot Titanling",
        "description": "A shard of a sleeping giant tree.",
        "bonus_stat": "constitution",
        "tier": "legendary",
        "min_player_level": 28,
        "base_adoption_cost": 1940,
        "material_cost": {"living_bark": 6, "ancient_core": 1},
        "quest_req": "ancient_roots",
    },
    "astral_phoenix": {
        "name": "Astral Phoenix",
        "description": "A reborn firebird from broken stars.",
        "bonus_stat": "max_mana",
        "tier": "mythic",
        "min_player_level": 30,
        "base_adoption_cost": 2600,
        "material_cost": {"star_fragment": 8, "void_essence": 4},
        "achievement_req": "void_titan_slayer",
    },
    "mythic_leviathan_whelp": {
        "name": "Mythic Leviathan Whelp",
        "description": "Tiny now. Cataclysm later.",
        "bonus_stat": "strength",
        "tier": "mythic",
        "min_player_level": 30,
        "base_adoption_cost": 2700,
        "material_cost": {"aqua_pearl": 8, "ancient_core": 2},
        "achievement_req": "dungeon_master",
    },
}

PET_ABILITY_TREES = {
    "spirit_wolf": [
        {"name": "Pack Howl", "unlock_level": 3, "description": "+crit chance burst for 45s", "implemented": True, "id": "pack_howl", "cooldown": 90, "duration": 45},
        {"name": "Hunt Mark", "unlock_level": 8, "description": "Marks target to take extra physical damage", "implemented": False},
    ],
    "ember_fox": [
        {"name": "Cinder Dash", "unlock_level": 3, "description": "Quick strike with burn chance (small gold find)", "implemented": True, "id": "cinder_dash", "cooldown": 20},
        {"name": "Ash Veil", "unlock_level": 9, "description": "Brief evade window after ability use", "implemented": False},
    ],
    "stone_turtle": [
        {"name": "Shell Guard", "unlock_level": 4, "description": "Temporary damage reduction (60s)", "implemented": True, "id": "shell_guard", "cooldown": 60, "duration": 60},
        {"name": "Quake Step", "unlock_level": 10, "description": "Minor stun pulse on block", "implemented": False},
    ],
    "arcane_wisp": [
        {"name": "Mana Spark", "unlock_level": 3, "description": "Small mana restore on hit", "implemented": False},
        {"name": "Aether Lens", "unlock_level": 11, "description": "Amplifies arcane-tag abilities", "implemented": False},
    ],
    "luminous_raven": [
        {"name": "Raven's Mend", "unlock_level": 1, "description": "Heals the owner for a small amount.", "implemented": True, "id": "ravens_mend"},
    ],
    "frost_lynx": [
        {"name": "Glacier Step", "unlock_level": 4, "description": "Temporary defense and dodge boost.", "implemented": True, "id": "glacier_step", "cooldown": 50, "duration": 25},
    ],
    "thorn_stag": [
        {"name": "Verdant Pulse", "unlock_level": 5, "description": "Regenerative burst and constitution aura.", "implemented": True, "id": "verdant_pulse", "cooldown": 70, "duration": 20},
    ],
    "storm_owl": [
        {"name": "Static Wing", "unlock_level": 6, "description": "Boosts crit chance and perception briefly.", "implemented": True, "id": "static_wing", "cooldown": 60, "duration": 20},
    ],
    "sunscale_drake": [
        {"name": "Solar Roar", "unlock_level": 8, "description": "Large temporary strength surge.", "implemented": True, "id": "solar_roar", "cooldown": 90, "duration": 25},
    ],
    "moonshade_panther": [
        {"name": "Night Veil", "unlock_level": 8, "description": "Dexterity burst and stealthy reflexes.", "implemented": True, "id": "night_veil", "cooldown": 85, "duration": 25},
    ],
    "aether_moth": [
        {"name": "Aether Sip", "unlock_level": 9, "description": "Restore a chunk of mana.", "implemented": True, "id": "aether_sip", "cooldown": 45},
    ],
}

MAX_PET_LEVEL = 30
PET_ADOPTION_COSTS = {pid: int(meta.get("base_adoption_cost", 150)) for pid, meta in PETS.items()}
PET_TIER_XP_MULT = {
    "common": 1.00,
    "rare": 1.20,
    "epic": 1.45,
    "legendary": 1.75,
    "mythic": 2.05,
}
PET_TIER_BONUS_MULT = {
    "common": 1.00,
    "rare": 1.25,
    "epic": 1.55,
    "legendary": 1.90,
    "mythic": 2.30,
}
PET_TIER_COMBAT_MULT = {
    "common": 1.00,
    "rare": 1.15,
    "epic": 1.35,
    "legendary": 1.60,
    "mythic": 1.85,
}
PET_FEED_COST_GOLD = 25
PET_FEED_COOLDOWN_SECONDS = 60
PET_BANDAGE_COST_GOLD = 60
PET_INJURY_PROFILES = {
    "light": {"gold_cost": 35, "downtime_wins": 1, "label": "Light"},
    "moderate": {"gold_cost": 60, "downtime_wins": 2, "label": "Moderate"},
    "heavy": {"gold_cost": 95, "downtime_wins": 3, "label": "Heavy"},
    "critical": {"gold_cost": 140, "downtime_wins": 4, "label": "Critical"},
}


def _ensure_pet_state(player):
    state = player.state
    state.setdefault("pets", {})
    state.setdefault("active_pet", None)
    state.setdefault("active_pet_bonus_applied", {})
    state.setdefault("pet_last_feed_at", 0.0)
    state.setdefault("pet_ability_cooldowns", {})
    state.setdefault("pet_temporary_buffs", {})
    state.setdefault("pet_bond", {})
    state.setdefault("pet_injured", {})

    injury_state = state.get("pet_injured", {})
    if isinstance(injury_state, dict):
        for pid, raw in list(injury_state.items()):
            injury_state[pid] = _normalize_injury_entry(raw)

    pets = state.get("pets", {})
    if isinstance(pets, dict):
        for pid, pdata in list(pets.items()):
            if not isinstance(pdata, dict):
                pets[pid] = {"level": 1, "xp": 0, "tier": PETS.get(pid, {}).get("tier", "common")}
                continue
            pdata.setdefault("level", 1)
            pdata.setdefault("xp", 0)
            pdata.setdefault("tier", PETS.get(pid, {}).get("tier", "common"))


def _xp_to_next(level, pet_id=None):
    base = 20 + (level * 12)
    if not pet_id:
        return base
    tier = PETS.get(pet_id, {}).get("tier", "common")
    mult = float(PET_TIER_XP_MULT.get(tier, 1.0))
    return max(1, int(base * mult))


def _normalize_injury_entry(raw):
    if isinstance(raw, dict):
        sev = str(raw.get("severity", "") or "").lower()
        if not sev:
            return {"severity": "", "wins_left": 0}
        if sev not in PET_INJURY_PROFILES:
            sev = "moderate"
        default_wins = int(PET_INJURY_PROFILES[sev].get("downtime_wins", 2))
        wins_left = int(raw.get("wins_left", default_wins))
        wins_left = max(0, wins_left)
        return {"severity": sev, "wins_left": wins_left}
    if bool(raw):
        return {"severity": "moderate", "wins_left": int(PET_INJURY_PROFILES["moderate"]["downtime_wins"])}
    return {"severity": "", "wins_left": 0}


def _get_pet_injury(player, pet_id):
    entry = _normalize_injury_entry(player.state.get("pet_injured", {}).get(pet_id, {}))
    if not entry.get("severity"):
        return None
    return entry


def _set_pet_injury(player, pet_id, severity):
    sev = str(severity or "").lower()
    injury_map = player.state.setdefault("pet_injured", {})
    if not sev or sev not in PET_INJURY_PROFILES:
        injury_map[pet_id] = {"severity": "", "wins_left": 0}
        return
    injury_map[pet_id] = {
        "severity": sev,
        "wins_left": int(PET_INJURY_PROFILES[sev].get("downtime_wins", 1)),
    }


def _pet_bonus_data(pet_id, pet_level):
    pet_meta = PETS.get(pet_id, {})
    bonus_stat = pet_meta.get("bonus_stat")
    tier = pet_meta.get("tier", "common")
    tier_mult = float(PET_TIER_BONUS_MULT.get(tier, 1.0))
    level = int(max(1, pet_level))
    milestone_bonus = level // 10
    if not bonus_stat:
        return {}
    if bonus_stat == "max_mana":
        mana_bonus = max(1, int(((level ** 1.10) / 2.5) * tier_mult) + milestone_bonus)
        return {"max_mana": mana_bonus}
    bonus_val = max(1, int(((level ** 1.07) / 4.2) * tier_mult) + milestone_bonus)
    return {bonus_stat: bonus_val}


def _format_material_cost(material_cost):
    if not material_cost:
        return "none"
    parts = []
    for item_id, amt in sorted(material_cost.items()):
        parts.append(f"{int(amt)}x {str(item_id).replace('_', ' ')}")
    return ", ".join(parts)


def _has_materials(player, material_cost):
    inv = getattr(player, "inventory", {}) or {}
    for item_id, amt in (material_cost or {}).items():
        if int(inv.get(item_id, 0)) < int(amt):
            return False
    return True


def _consume_materials(player, material_cost):
    if not material_cost:
        return
    inv = getattr(player, "inventory", {}) or {}
    for item_id, amt in material_cost.items():
        need = int(amt)
        have = int(inv.get(item_id, 0))
        inv[item_id] = max(0, have - need)
        if inv[item_id] <= 0:
            inv.pop(item_id, None)


def get_pet_bonus_preview(pet_id, pet_level):
    bonus = _pet_bonus_data(pet_id, pet_level)
    if not bonus:
        return "No stat bonus"
    parts = []
    for stat, val in sorted(bonus.items()):
        parts.append(f"+{int(val)} {stat.replace('_', ' ')}")
    return ", ".join(parts)


def get_pet_ability_preview_lines(pet_id, pet_level, max_lines=None):
    abilities = PET_ABILITY_TREES.get(pet_id, [])
    lines = []
    for ab in abilities:
        unlock_level = int(ab.get("unlock_level", 1))
        unlocked = int(pet_level) >= unlock_level
        status = "UNLOCKED" if unlocked else f"LOCKED (lvl {unlock_level})"
        impl = "coming soon" if not ab.get("implemented", False) else "ready"
        lines.append(f"- {ab.get('name', 'Unknown')} [{status}] [{impl}] :: {ab.get('description', '')}")
    if max_lines is not None:
        return lines[:int(max_lines)]
    return lines


def _remove_active_bonus(player):
    bonus = dict(player.state.get("active_pet_bonus_applied", {}))
    for stat, val in bonus.items():
        player.stats[stat] = int(player.stats.get(stat, 0)) - int(val)
        if stat == "max_mana":
            player.stats["mana"] = min(int(player.stats.get("mana", 0)), int(player.stats.get("max_mana", 0)))
    player.state["active_pet_bonus_applied"] = {}


def _cleanup_pet_temp_effects(player):
    """Remove expired temporary pet effects and revert stats."""
    import time as _time
    _ensure_pet_state(player)
    now = _time.time()
    tb = player.state.setdefault("pet_temporary_buffs", {})
    to_remove = []
    for buff_id, info in list(tb.items()):
        expires = float(info.get("expires_at", 0))
        if expires and now >= expires:
            # revert stat change
            stat = info.get("stat")
            val = int(info.get("value", 0))
            if stat:
                player.stats[stat] = int(player.stats.get(stat, 0)) - val
            to_remove.append(buff_id)
    for bid in to_remove:
        tb.pop(bid, None)


def _apply_or_refresh_temp_buff(player, buff_id, stat, value, duration_seconds, now_ts):
    """Apply a temporary buff, replacing any previous instance cleanly."""
    tb = player.state.setdefault("pet_temporary_buffs", {})
    existing = tb.get(buff_id)
    if existing:
        old_stat = existing.get("stat")
        old_val = int(existing.get("value", 0))
        if old_stat:
            player.stats[old_stat] = int(player.stats.get(old_stat, 0)) - old_val

    player.stats[stat] = int(player.stats.get(stat, 0)) + int(value)
    tb[buff_id] = {
        "stat": stat,
        "value": int(value),
        "expires_at": float(now_ts) + int(duration_seconds),
    }


def _apply_active_bonus(player):
    active_pet = player.state.get("active_pet")
    pets = player.state.get("pets", {})
    if not active_pet or active_pet not in pets:
        player.state["active_pet_bonus_applied"] = {}
        return

    level = int(pets[active_pet].get("level", 1))
    bonus = _pet_bonus_data(active_pet, level)
    for stat, val in bonus.items():
        player.stats[stat] = int(player.stats.get(stat, 0)) + int(val)
        if stat == "max_mana":
            player.stats["mana"] = int(player.stats.get("mana", 0)) + int(val)
    player.state["active_pet_bonus_applied"] = bonus


def adopt_pet(player, pet_id):
    _ensure_pet_state(player)
    pid = str(pet_id or "").strip().lower().replace(" ", "_")
    if pid not in PETS:
        return False, f"Unknown pet '{pet_id}'."

    pets = player.state.get("pets", {})
    if pid in pets:
        return False, f"You already have {PETS[pid]['name']}."

    pet_meta = PETS.get(pid, {})
    req_level = int(pet_meta.get("min_player_level", 1))
    player_level = int(player.stats.get("level", 1))
    if player_level < req_level:
        return False, f"{PETS[pid]['name']} requires player level {req_level} (you are level {player_level})."

    req_achievement = str(pet_meta.get("achievement_req", "") or "").strip()
    if req_achievement:
        unlocked = set(player.state.get("achievements", []))
        if req_achievement not in unlocked:
            return False, f"{PETS[pid]['name']} requires achievement '{req_achievement}'."

    req_quest = str(pet_meta.get("quest_req", "") or "").strip()
    if req_quest:
        completed_quests = set(player.state.get("completed_quests", []))
        if req_quest not in completed_quests:
            return False, f"{PETS[pid]['name']} requires completed quest '{req_quest}'."

    material_cost = dict(pet_meta.get("material_cost", {}) or {})
    if material_cost and not _has_materials(player, material_cost):
        return False, f"{PETS[pid]['name']} requires materials: {_format_material_cost(material_cost)}."

    cost = int(PET_ADOPTION_COSTS.get(pid, 150))
    gold = int(player.stats.get("gold", 0))
    if gold < cost:
        return False, f"Adopting {PETS[pid]['name']} costs {cost}g. You only have {gold}g."

    player.stats["gold"] = gold - cost
    _consume_materials(player, material_cost)

    pets[pid] = {
        "level": 1,
        "xp": 0,
        "tier": pet_meta.get("tier", "common"),
    }
    if not player.state.get("active_pet"):
        activate_pet(player, pid)
    return True, f"Adopted pet: {PETS[pid]['name']} (-{cost}g)."


def activate_pet(player, pet_id):
    _ensure_pet_state(player)
    pid = str(pet_id or "").strip().lower().replace(" ", "_")
    pets = player.state.get("pets", {})
    if pid not in pets:
        return False, f"You do not own '{pet_id}'."

    _remove_active_bonus(player)
    player.state["active_pet"] = pid
    _apply_active_bonus(player)
    return True, f"Active pet set to {PETS[pid]['name']}."


def feed_active_pet(player):
    _ensure_pet_state(player)
    pid = player.state.get("active_pet")
    if not pid:
        return False, "No active pet to feed."

    now = time.time()
    last_feed = float(player.state.get("pet_last_feed_at", 0.0))
    remaining = PET_FEED_COOLDOWN_SECONDS - int(now - last_feed)
    if remaining > 0:
        return False, f"Your pet is still full. You can feed again in {remaining}s."

    gold = int(player.stats.get("gold", 0))
    if gold < PET_FEED_COST_GOLD:
        return False, f"Feeding costs {PET_FEED_COST_GOLD}g. You only have {gold}g."

    player.stats["gold"] = gold - PET_FEED_COST_GOLD
    player.state["pet_last_feed_at"] = now
    return True, f"Spent {PET_FEED_COST_GOLD}g to feed your companion." + gain_pet_xp(player, 18, source="feeding")


def gain_pet_xp(player, amount, source="adventure"):
    _ensure_pet_state(player)
    pid = player.state.get("active_pet")
    if not pid:
        return ""

    pets = player.state.get("pets", {})
    pdata = pets.get(pid)
    if not pdata:
        return ""

    level = int(pdata.get("level", 1))
    xp = int(pdata.get("xp", 0)) + int(max(0, amount))
    leveled = 0
    while level < MAX_PET_LEVEL and xp >= _xp_to_next(level, pid):
        xp -= _xp_to_next(level, pid)
        level += 1
        leveled += 1

    if level >= MAX_PET_LEVEL:
        xp = 0

    pdata["level"] = level
    pdata["xp"] = xp

    # Re-apply bonus because pet level may have changed.
    _remove_active_bonus(player)
    _apply_active_bonus(player)

    text = f"\n  [Pet] +{int(amount)} XP ({source})"
    if leveled > 0:
        text += f"\n  [Pet] {PETS[pid]['name']} reached level {level}!"
    return text


def get_pet_status_text(player):
    _ensure_pet_state(player)
    pets = player.state.get("pets", {})
    active = player.state.get("active_pet")

    # Clean up expired temporary buffs so status reflects current state
    try:
        _cleanup_pet_temp_effects(player)
    except Exception:
        pass

    result = "\n" + "=" * 58 + "\n"
    result += "  COMPANIONS\n"
    result += "=" * 58 + "\n"
    # Tier summary keeps status readable even with a large pet roster.
    tier_counts = {}
    for _pid, meta in PETS.items():
        tier = str(meta.get("tier", "common")).lower()
        tier_counts[tier] = int(tier_counts.get(tier, 0)) + 1
    summary = ", ".join(f"{tier}:{count}" for tier, count in sorted(tier_counts.items()))
    result += f"  Roster: {len(PETS)} pets | Tiers -> {summary}\n"
    result += "  Use 'pet inspect <id>' to see requirements for specific pets.\n"
    result += f"  Feed cost: {PET_FEED_COST_GOLD}g | Cooldown: {PET_FEED_COOLDOWN_SECONDS}s\n\n"

    if not pets:
        result += "  You have no pets yet.\n"
        result += "  Try: pet adopt spirit_wolf\n"
        result += "=" * 58 + "\n"
        return result

    for pid, pdata in sorted(pets.items()):
        icon = "*" if pid == active else "-"
        level = int(pdata.get("level", 1))
        xp = int(pdata.get("xp", 0))
        next_xp = _xp_to_next(level, pid) if level < MAX_PET_LEVEL else 0
        pet_tier = str(PETS.get(pid, {}).get("tier", "common")).lower()
        injury = _get_pet_injury(player, pid)
        result += f"  {icon} {PETS.get(pid, {}).get('name', pid)} (id: {pid})\n"
        result += f"    Tier: {pet_tier.title()} | Level {level}"
        if level < MAX_PET_LEVEL:
            result += f" | XP {xp}/{next_xp}\n"
        else:
            result += " | MAX\n"
        if injury:
            prof = PET_INJURY_PROFILES.get(injury.get("severity", "moderate"), PET_INJURY_PROFILES["moderate"])
            result += (
                f"    Status: Injured [{prof.get('label')}] "
                f"(wins left: {int(injury.get('wins_left', 0))}, use: pet bandage)\n"
            )
        else:
            result += "    Status: Ready\n"
        result += f"    Bonus: {get_pet_bonus_preview(pid, level)}\n"
        for line in get_pet_ability_preview_lines(pid, level, max_lines=2):
            result += f"    {line}\n"
        # show cooldowns for this pet's abilities
        cds = player.state.get("pet_ability_cooldowns", {})
        active_lines = []
        for ab in PET_ABILITY_TREES.get(pid, []):
            ab_id = str(ab.get("id", ab.get("name", "")).lower().replace("'", "").replace(" ", "_"))
            until = float(cds.get(ab_id, 0))
            if until > 0:
                import time as _time
                rem = int(_math.ceil(max(0.0, until - _time.time())))
                active_lines.append(f"{ab.get('name')}: {rem}s")
        if active_lines:
            result += f"    Cooldowns: {', '.join(active_lines)}\n"
        # show active temporary buffs
        tb = player.state.get("pet_temporary_buffs", {})
        tb_lines = []
        import time as _time
        for bid, info in tb.items():
            # only show buffs that belong to this pet by id prefix (best-effort)
            tb_stat = info.get("stat")
            tb_val = info.get("value")
            expires = info.get("expires_at")
            if expires:
                rem = int(max(0, int(expires) - int(_time.time())))
                tb_lines.append(f"{bid} ({tb_stat}+{tb_val}) {rem}s")
        if tb_lines:
            result += f"    Active buffs: {', '.join(tb_lines)}\n"
        result += "\n"

    result += "\n  Commands: pet adopt <id>, pet activate <id>, pet feed, pet bandage, pet inspect <id>, pet ability <id>, pet abilities\n"
    result += "=" * 58 + "\n"
    return result


def get_pet_inspect_text(player, pet_id):
    _ensure_pet_state(player)
    pid = str(pet_id or "").strip().lower().replace(" ", "_")
    if pid not in PETS:
        return f"Unknown pet '{pet_id}'."

    pets = player.state.get("pets", {})
    owned = pid in pets
    active = player.state.get("active_pet")
    injury = _get_pet_injury(player, pid)

    level = int(pets.get(pid, {}).get("level", 1)) if owned else 1
    xp = int(pets.get(pid, {}).get("xp", 0)) if owned else 0
    next_xp = _xp_to_next(level, pid) if level < MAX_PET_LEVEL else 0
    pdata = PETS.get(pid, {})
    req_level = int(pdata.get("min_player_level", 1))
    req_achievement = str(pdata.get("achievement_req", "") or "").strip()
    req_quest = str(pdata.get("quest_req", "") or "").strip()
    req_materials = dict(pdata.get("material_cost", {}) or {})

    result = "\n" + "=" * 58 + "\n"
    result += f"  PET INSPECT: {PETS[pid]['name']}\n"
    result += "=" * 58 + "\n"
    result += f"  Description: {PETS[pid].get('description', '')}\n"
    result += f"  Tier: {str(pdata.get('tier', 'common')).title()}\n"
    result += f"  Owned: {'yes' if owned else 'no'}\n"
    result += f"  Active: {'yes' if active == pid else 'no'}\n"
    if injury:
        prof = PET_INJURY_PROFILES.get(injury.get("severity", "moderate"), PET_INJURY_PROFILES["moderate"])
        result += f"  Injury: {prof.get('label')} (wins left: {int(injury.get('wins_left', 0))})\n"
    else:
        result += "  Injury: none\n"
    if owned:
        result += f"  Level: {level}"
        if level < MAX_PET_LEVEL:
            result += f" | XP {xp}/{next_xp}\n"
        else:
            result += " | MAX\n"
    result += f"  Stat Bonus: {get_pet_bonus_preview(pid, level)}\n"
    result += f"  Adoption Cost: {int(PET_ADOPTION_COSTS.get(pid, 150))}g\n"
    result += f"  Required Level: {req_level}\n"
    if req_achievement:
        result += f"  Required Achievement: {req_achievement}\n"
    if req_quest:
        result += f"  Required Quest: {req_quest}\n"
    if req_materials:
        result += f"  Required Materials: {_format_material_cost(req_materials)}\n"
    result += "\n  Ability Roadmap:\n"
    for line in get_pet_ability_preview_lines(pid, level):
        result += f"    {line}\n"
    result += "=" * 58 + "\n"
    return result


def get_active_pet_hotbar_abilities(player, max_abilities=4):
    """Return unlocked implemented abilities for the active pet for UI hotbar use."""
    _ensure_pet_state(player)
    pid = player.state.get("active_pet")
    if not pid:
        return []
    pdata = player.state.get("pets", {}).get(pid, {})
    level = int(pdata.get("level", 1))
    abilities = []
    for ab in PET_ABILITY_TREES.get(pid, []):
        if not ab.get("implemented", False):
            continue
        if level < int(ab.get("unlock_level", 1)):
            continue
        abilities.append(ab)
    return abilities[: int(max_abilities)]


def get_pet_combat_action(player):
    """Build simple combat action data for hybrid pet turns."""
    _ensure_pet_state(player)
    pid = player.state.get("active_pet")
    if not pid:
        return None
    pdata = player.state.get("pets", {}).get(pid, {})
    injury = _get_pet_injury(player, pid)
    if injury:
        return None
    level = int(pdata.get("level", 1))
    tier = str(PETS.get(pid, {}).get("tier", "common")).lower()
    tier_mult = float(PET_TIER_COMBAT_MULT.get(tier, 1.0))
    # Baseline contribution kept moderate relative to player attacks.
    base = 2.0 + (level * 0.8)
    damage = max(1, int(base * tier_mult))
    base_hp = 30 + (level * 6)
    hp_mult = 1.0 + ((tier_mult - 1.0) * 0.7)
    max_hp = max(10, int(base_hp * hp_mult))
    defense = max(0, int((level * 0.35) * tier_mult))
    dodge = min(0.28, 0.05 + level * 0.003 + (tier_mult - 1.0) * 0.05)
    return {
        "pet_id": pid,
        "pet_name": PETS.get(pid, {}).get("name", pid),
        "tier": tier,
        "level": level,
        "damage": damage,
        "max_hp": max_hp,
        "defense": defense,
        "dodge": dodge,
        "bonus_stat": PETS.get(pid, {}).get("bonus_stat", ""),
    }


def apply_pet_combat_aftermath(player, combat):
    """Persist combat injuries from the combat state back to player pet state."""
    _ensure_pet_state(player)
    if not combat:
        return ""
    pet_state = getattr(combat, "pet_combatant", None)
    if not pet_state:
        return ""
    pid = str(pet_state.get("pet_id", "") or "")
    if not pid:
        return ""

    knocked = bool(getattr(combat, "pet_knocked", False))
    hp = int(pet_state.get("hp", 0))
    max_hp = max(1, int(pet_state.get("max_hp", 1)))
    hp_ratio = float(hp) / float(max_hp)

    severity = ""
    if knocked:
        severity = "critical"
    elif hp_ratio <= 0.15:
        severity = "heavy"
    elif hp_ratio <= 0.35:
        severity = "moderate"
    elif hp_ratio <= 0.55:
        severity = "light"

    if severity:
        _set_pet_injury(player, pid, severity)
        profile = PET_INJURY_PROFILES.get(severity, PET_INJURY_PROFILES["moderate"])
        return (
            f"\n  [Pet] {pet_state.get('pet_name', 'Companion')} was injured "
            f"[{profile.get('label')}] in battle."
            f" Wins to recover: {int(profile.get('downtime_wins', 0))}."
            f" Use 'pet bandage' for immediate recovery."
        )
    return ""


def advance_pet_recovery(player, wins=1):
    """Reduce injury downtime after combat victories and auto-recover pets at zero."""
    _ensure_pet_state(player)
    injury_map = player.state.setdefault("pet_injured", {})
    if not injury_map:
        return ""

    step = max(0, int(wins))
    if step <= 0:
        return ""

    recovered = []
    for pid in list(injury_map.keys()):
        entry = _normalize_injury_entry(injury_map.get(pid, {}))
        sev = entry.get("severity", "")
        if not sev:
            continue
        entry["wins_left"] = max(0, int(entry.get("wins_left", 0)) - step)
        if entry["wins_left"] <= 0:
            injury_map[pid] = {"severity": "", "wins_left": 0}
            recovered.append(PETS.get(pid, {}).get("name", pid.replace("_", " ").title()))
        else:
            injury_map[pid] = entry

    if not recovered:
        return ""
    return "\n  [Pet] Recovered after recent victories: " + ", ".join(recovered) + "."


def bandage_active_pet(player):
    """Heal active pet injuries using a bandage item or gold fallback."""
    _ensure_pet_state(player)
    pid = player.state.get("active_pet")
    if not pid:
        return False, "No active pet to bandage."

    injury_map = player.state.setdefault("pet_injured", {})
    injury = _normalize_injury_entry(injury_map.get(pid, {}))
    severity = injury.get("severity", "")
    if not severity:
        return False, f"{PETS.get(pid, {}).get('name', 'Your pet')} is not injured."

    profile = PET_INJURY_PROFILES.get(severity, PET_INJURY_PROFILES["moderate"])
    gold_cost = int(profile.get("gold_cost", PET_BANDAGE_COST_GOLD))

    inv = getattr(player, "inventory", {}) or {}
    if int(inv.get("bandage", 0)) > 0:
        inv["bandage"] = int(inv.get("bandage", 0)) - 1
        if inv["bandage"] <= 0:
            inv.pop("bandage", None)
        injury_map[pid] = {"severity": "", "wins_left": 0}
        return True, (
            f"Used 1x bandage to recover {PETS.get(pid, {}).get('name', 'your pet')} "
            f"from {profile.get('label')} injury."
        )

    gold = int(player.stats.get("gold", 0))
    if gold < gold_cost:
        return False, (
            f"Bandaging requires 1x bandage item or {gold_cost}g ({profile.get('label')} injury). "
            f"You only have {gold}g and no bandage item."
        )

    player.stats["gold"] = gold - gold_cost
    injury_map[pid] = {"severity": "", "wins_left": 0}
    return True, (
        f"Paid {gold_cost}g to recover {PETS.get(pid, {}).get('name', 'your pet')} "
        f"from {profile.get('label')} injury."
    )


def _pet_ability_ravens_mend(player, pid, match, cooldowns, ab_id, now):
    hp = int(player.stats.get("health", 0))
    hp_max = int(player.stats.get("health_max", 100))
    heal = min(20, max(0, hp_max - hp))
    if heal <= 0:
        return False, "You are already at full health."
    player.stats["health"] = hp + heal
    xp_text = gain_pet_xp(player, 8, source="pet_ability")
    cooldowns[ab_id] = now + int(match.get("cooldown", 30))
    return True, f"{PETS.get(pid, {}).get('name')} used {match.get('name')}! Healed {heal} HP." + xp_text


def _pet_ability_pack_howl(player, pid, match, cooldowns, ab_id, now):
    dur = int(match.get("duration", 45))
    val = 5
    _apply_or_refresh_temp_buff(player, ab_id, "crit_chance", val, dur, now)
    xp_text = gain_pet_xp(player, 5, source="pet_ability")
    cooldowns[ab_id] = now + int(match.get("cooldown", 90))
    return True, f"{PETS.get(pid, {}).get('name')} used {match.get('name')}! +{val} crit chance for {dur}s." + xp_text


def _pet_ability_cinder_dash(player, pid, match, cooldowns, ab_id, now):
    gain = 10
    player.stats["gold"] = int(player.stats.get("gold", 0)) + gain
    xp_text = gain_pet_xp(player, 5, source="pet_ability")
    cooldowns[ab_id] = now + int(match.get("cooldown", 20))
    return True, f"{PETS.get(pid, {}).get('name')} used {match.get('name')}! You found {gain}g." + xp_text


def _pet_ability_shell_guard(player, pid, match, cooldowns, ab_id, now):
    dur = int(match.get("duration", 60))
    val = 2
    _apply_or_refresh_temp_buff(player, ab_id, "defense", val, dur, now)
    xp_text = gain_pet_xp(player, 5, source="pet_ability")
    cooldowns[ab_id] = now + int(match.get("cooldown", 60))
    return True, f"{PETS.get(pid, {}).get('name')} used {match.get('name')}! +{val} defense for {dur}s." + xp_text


def _pet_ability_glacier_step(player, pid, match, cooldowns, ab_id, now):
    dur = int(match.get("duration", 25))
    _apply_or_refresh_temp_buff(player, ab_id + "_def", "defense", 3, dur, now)
    _apply_or_refresh_temp_buff(player, ab_id + "_dex", "dexterity", 2, dur, now)
    xp_text = gain_pet_xp(player, 7, source="pet_ability")
    cooldowns[ab_id] = now + int(match.get("cooldown", 50))
    return True, f"{PETS.get(pid, {}).get('name')} used {match.get('name')}! +3 defense and +2 dexterity for {dur}s." + xp_text


def _pet_ability_verdant_pulse(player, pid, match, cooldowns, ab_id, now):
    hp = int(player.stats.get("health", 0))
    hp_max = int(player.stats.get("health_max", 100))
    heal = min(16, max(0, hp_max - hp))
    if heal > 0:
        player.stats["health"] = hp + heal
    dur = int(match.get("duration", 20))
    _apply_or_refresh_temp_buff(player, ab_id, "constitution", 2, dur, now)
    xp_text = gain_pet_xp(player, 8, source="pet_ability")
    cooldowns[ab_id] = now + int(match.get("cooldown", 70))
    return True, f"{PETS.get(pid, {}).get('name')} used {match.get('name')}! Healed {heal} HP and gained +2 constitution for {dur}s." + xp_text


def _pet_ability_static_wing(player, pid, match, cooldowns, ab_id, now):
    dur = int(match.get("duration", 20))
    _apply_or_refresh_temp_buff(player, ab_id + "_crit", "crit_chance", 7, dur, now)
    _apply_or_refresh_temp_buff(player, ab_id + "_perc", "perception", 2, dur, now)
    xp_text = gain_pet_xp(player, 8, source="pet_ability")
    cooldowns[ab_id] = now + int(match.get("cooldown", 60))
    return True, f"{PETS.get(pid, {}).get('name')} used {match.get('name')}! +7 crit chance and +2 perception for {dur}s." + xp_text


def _pet_ability_solar_roar(player, pid, match, cooldowns, ab_id, now):
    dur = int(match.get("duration", 25))
    _apply_or_refresh_temp_buff(player, ab_id, "strength", 4, dur, now)
    xp_text = gain_pet_xp(player, 10, source="pet_ability")
    cooldowns[ab_id] = now + int(match.get("cooldown", 90))
    return True, f"{PETS.get(pid, {}).get('name')} used {match.get('name')}! +4 strength for {dur}s." + xp_text


def _pet_ability_night_veil(player, pid, match, cooldowns, ab_id, now):
    dur = int(match.get("duration", 25))
    _apply_or_refresh_temp_buff(player, ab_id, "dexterity", 4, dur, now)
    xp_text = gain_pet_xp(player, 10, source="pet_ability")
    cooldowns[ab_id] = now + int(match.get("cooldown", 85))
    return True, f"{PETS.get(pid, {}).get('name')} used {match.get('name')}! +4 dexterity for {dur}s." + xp_text


def _pet_ability_aether_sip(player, pid, match, cooldowns, ab_id, now):
    max_mana = int(player.stats.get("max_mana", 0))
    if max_mana <= 0:
        return False, "You do not have a mana pool to restore."
    mana = int(player.stats.get("mana", 0))
    restore = max(6, int(max_mana * 0.20))
    actual = min(restore, max_mana - mana)
    if actual <= 0:
        return False, "Your mana is already full."
    player.stats["mana"] = mana + actual
    xp_text = gain_pet_xp(player, 8, source="pet_ability")
    cooldowns[ab_id] = now + int(match.get("cooldown", 45))
    return True, f"{PETS.get(pid, {}).get('name')} used {match.get('name')}! Restored {actual} mana." + xp_text


_PET_ABILITY_DISPATCH = {
    "ravens_mend": _pet_ability_ravens_mend,
    "pack_howl": _pet_ability_pack_howl,
    "cinder_dash": _pet_ability_cinder_dash,
    "shell_guard": _pet_ability_shell_guard,
    "glacier_step": _pet_ability_glacier_step,
    "verdant_pulse": _pet_ability_verdant_pulse,
    "static_wing": _pet_ability_static_wing,
    "solar_roar": _pet_ability_solar_roar,
    "night_veil": _pet_ability_night_veil,
    "aether_sip": _pet_ability_aether_sip,
}


def use_pet_ability(player, ability_query):
    """Attempt to use an active pet ability by name or id for the player's active pet.

    Returns (success: bool, message: str).
    """
    _ensure_pet_state(player)
    pid = player.state.get("active_pet")
    if not pid:
        return False, "No active pet to use abilities from."

    abilities = PET_ABILITY_TREES.get(pid, [])
    if not abilities:
        return False, f"{PETS.get(pid, {}).get('name','Companion')} has no abilities."

    q = str(ability_query or "").strip().lower().replace("'", "").replace(" ", "_")
    # find ability by id or name
    match = None
    for ab in abilities:
        ab_id = str(ab.get("id", "")).lower()
        ab_name = str(ab.get("name", "")).lower().replace("'", "").replace(" ", "_")
        if q == ab_id or q == ab_name:
            match = ab
            break

    if not match:
        return False, f"Ability '{ability_query}' not found for {PETS.get(pid, {}).get('name','pet')}."

    if not match.get("implemented", False):
        return False, f"Ability '{match.get('name')}' is not implemented yet."

    # Cooldown handling
    import time as _time
    _ensure_pet_state(player)
    cooldowns = player.state.setdefault("pet_ability_cooldowns", {})
    ab_id = (match.get("id") or match.get("name", "")).lower().replace("'", "").replace(" ", "_")
    now = _time.time()
    cd_until = float(cooldowns.get(ab_id, 0))
    if now < cd_until:
        remaining = int(_math.ceil(cd_until - now))
        return False, f"Ability '{match.get('name')}' is on cooldown for {remaining}s."

    # cleanup expired temporary buffs before applying new effects
    try:
        _cleanup_pet_temp_effects(player)
    except Exception:
        pass

    handler = _PET_ABILITY_DISPATCH.get(ab_id)
    if not handler:
        return False, "That ability has no effect (prototype)."
    return handler(player, pid, match, cooldowns, ab_id, now)
