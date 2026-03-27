"""
Companion / pet system.
"""

import time

PETS = {
    "spirit_wolf": {
        "name": "Spirit Wolf",
        "description": "A watchful companion that sharpens your instincts.",
        "bonus_stat": "perception",
    },
    "ember_fox": {
        "name": "Ember Fox",
        "description": "Fast and cunning, always one step ahead.",
        "bonus_stat": "dexterity",
    },
    "stone_turtle": {
        "name": "Stone Turtle",
        "description": "Slow, steady, and impossibly hard to break.",
        "bonus_stat": "defense",
    },
    "arcane_wisp": {
        "name": "Arcane Wisp",
        "description": "A drifting mote that hums with mana.",
        "bonus_stat": "max_mana",
    },
    "luminous_raven": {
        "name": "Luminous Raven",
        "description": "A clever raven that can mend wounds with a soft glow.",
        "bonus_stat": "perception",
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
}

MAX_PET_LEVEL = 30
PET_ADOPTION_COSTS = {
    "spirit_wolf": 120,
    "ember_fox": 150,
    "stone_turtle": 180,
    "arcane_wisp": 220,
    "luminous_raven": 140,
}
PET_FEED_COST_GOLD = 25
PET_FEED_COOLDOWN_SECONDS = 60


def _ensure_pet_state(player):
    state = player.state
    state.setdefault("pets", {})
    state.setdefault("active_pet", None)
    state.setdefault("active_pet_bonus_applied", {})
    state.setdefault("pet_last_feed_at", 0.0)


def _xp_to_next(level):
    return 20 + (level * 12)


def _pet_bonus_data(pet_id, pet_level):
    bonus_stat = PETS.get(pet_id, {}).get("bonus_stat")
    if not bonus_stat:
        return {}
    if bonus_stat == "max_mana":
        return {"max_mana": max(1, pet_level // 2)}
    return {bonus_stat: max(1, pet_level // 5)}


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

    cost = int(PET_ADOPTION_COSTS.get(pid, 150))
    gold = int(player.stats.get("gold", 0))
    if gold < cost:
        return False, f"Adopting {PETS[pid]['name']} costs {cost}g. You only have {gold}g."

    player.stats["gold"] = gold - cost

    pets[pid] = {"level": 1, "xp": 0}
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
    while level < MAX_PET_LEVEL and xp >= _xp_to_next(level):
        xp -= _xp_to_next(level)
        level += 1
        leveled += 1

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
    # Dynamic adoption costs line so new pets appear automatically
    costs_parts = []
    for pid, cost in sorted(PET_ADOPTION_COSTS.items()):
        costs_parts.append(f"{pid} {int(cost)}g")
    result += "  Adoption costs: " + ", ".join(costs_parts) + "\n"
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
        next_xp = _xp_to_next(level) if level < MAX_PET_LEVEL else 0
        result += f"  {icon} {PETS.get(pid, {}).get('name', pid)} (id: {pid})\n"
        result += f"    Level {level}"
        if level < MAX_PET_LEVEL:
            result += f" | XP {xp}/{next_xp}\n"
        else:
            result += " | MAX\n"
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
                rem = int(max(0, until - _time.time()))
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

    result += "\n  Commands: pet adopt <id>, pet activate <id>, pet feed, pet inspect <id>\n"
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

    level = int(pets.get(pid, {}).get("level", 1)) if owned else 1
    xp = int(pets.get(pid, {}).get("xp", 0)) if owned else 0
    next_xp = _xp_to_next(level) if level < MAX_PET_LEVEL else 0

    result = "\n" + "=" * 58 + "\n"
    result += f"  PET INSPECT: {PETS[pid]['name']}\n"
    result += "=" * 58 + "\n"
    result += f"  Description: {PETS[pid].get('description', '')}\n"
    result += f"  Owned: {'yes' if owned else 'no'}\n"
    result += f"  Active: {'yes' if active == pid else 'no'}\n"
    if owned:
        result += f"  Level: {level}"
        if level < MAX_PET_LEVEL:
            result += f" | XP {xp}/{next_xp}\n"
        else:
            result += " | MAX\n"
    result += f"  Stat Bonus: {get_pet_bonus_preview(pid, level)}\n"
    result += f"  Adoption Cost: {int(PET_ADOPTION_COSTS.get(pid, 150))}g\n"
    result += "\n  Ability Roadmap:\n"
    for line in get_pet_ability_preview_lines(pid, level):
        result += f"    {line}\n"
    result += "=" * 58 + "\n"
    return result


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
        remaining = int(cd_until - now)
        return False, f"Ability '{match.get('name')}' is on cooldown for {remaining}s."

    # cleanup expired temporary buffs before applying new effects
    try:
        _cleanup_pet_temp_effects(player)
    except Exception:
        pass

    # Prototype implementation: support the luminous raven's 'ravens_mend'
    if ab_id == "ravens_mend":
        hp = int(player.stats.get("health", 0))
        hp_max = int(player.stats.get("health_max", 100))
        heal = min(20, max(0, hp_max - hp))
        if heal <= 0:
            return False, "You are already at full health."
        player.stats["health"] = hp + heal
        # Give the pet a bit of XP for using its ability
        xp_text = gain_pet_xp(player, 8, source="pet_ability")
        # set cooldown if defined
        cd = int(match.get("cooldown", 30))
        cooldowns[ab_id] = now + cd
        return True, f"{PETS.get(pid, {}).get('name')} used {match.get('name')}! Healed {heal} HP." + xp_text

    # Prototype effects for a few other pet abilities
    if ab_id == "pack_howl":
        # small flat crit chance boost applied as temporary buff
        dur = int(match.get("duration", 45))
        val = 5
        player.stats["crit_chance"] = int(player.stats.get("crit_chance", 0)) + val
        tb = player.state.setdefault("pet_temporary_buffs", {})
        tb[ab_id] = {"stat": "crit_chance", "value": val, "expires_at": now + dur}
        xp_text = gain_pet_xp(player, 5, source="pet_ability")
        cooldowns[ab_id] = now + int(match.get("cooldown", 90))
        return True, f"{PETS.get(pid, {}).get('name')} used {match.get('name')}! +{val} crit chance for {dur}s." + xp_text

    if ab_id == "cinder_dash":
        # grant a bit of gold as a simple offensive loot-proxy
        gain = 10
        player.stats["gold"] = int(player.stats.get("gold", 0)) + gain
        xp_text = gain_pet_xp(player, 5, source="pet_ability")
        cooldowns[ab_id] = now + int(match.get("cooldown", 20))
        return True, f"{PETS.get(pid, {}).get('name')} used {match.get('name')}! You found {gain}g." + xp_text

    if ab_id == "shell_guard":
        # small flat defense boost as temporary buff
        dur = int(match.get("duration", 60))
        val = 2
        player.stats["defense"] = int(player.stats.get("defense", 0)) + val
        tb = player.state.setdefault("pet_temporary_buffs", {})
        tb[ab_id] = {"stat": "defense", "value": val, "expires_at": now + dur}
        xp_text = gain_pet_xp(player, 5, source="pet_ability")
        cooldowns[ab_id] = now + int(match.get("cooldown", 60))
        return True, f"{PETS.get(pid, {}).get('name')} used {match.get('name')}! +{val} defense for {dur}s." + xp_text

    return False, "That ability has no effect (prototype)."
