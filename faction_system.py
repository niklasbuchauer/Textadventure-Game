"""
Faction progression system.
"""

FACTIONS = {
    "iron_brotherhood": {
        "name": "Iron Brotherhood",
        "description": "Warriors and guardians who prize resolve.",
        "perk": "+1 defense per rank",
        "rank_stat": "defense",
    },
    "arcane_circle": {
        "name": "Arcane Circle",
        "description": "Scholars and casters pursuing forbidden insight.",
        "perk": "+2 max mana per rank",
        "rank_stat": "max_mana",
    },
    "shadow_court": {
        "name": "Shadow Court",
        "description": "Scouts and spies who value precision and secrecy.",
        "perk": "+1 dexterity per rank",
        "rank_stat": "dexterity",
    },
    "merchant_compact": {
        "name": "Merchant Compact",
        "description": "Deal-makers and pathfinders of the trade roads.",
        "perk": "+1 charisma per rank",
        "rank_stat": "charisma",
    },
}

RANK_THRESHOLDS = [0, 120, 300, 600, 1000, 1600, 2400, 3400, 4700, 6300, 8200]

RANK_TITLES = {
    "iron_brotherhood": [
        "Unaffiliated", "Steel Initiate", "Shield Brother", "Banner Warden", "Iron Marshal",
        "Fortress Champion", "Anvil Vanguard", "Bulwark Lord", "War Bastion", "High Castellan", "Adamant Regent",
    ],
    "arcane_circle": [
        "Unaffiliated", "Candle Adept", "Rune Scribe", "Glyphbinder", "Star Channeler",
        "Aether Scholar", "Void Lecturer", "Sigil Curator", "Eclipse Arcanist", "Astral Provost", "Grand Magister",
    ],
    "shadow_court": [
        "Unaffiliated", "Whisperfoot", "Night Runner", "Veil Agent", "Silk Fang",
        "Moonblade", "Gloom Executor", "Shade Captain", "Crow Regent", "Nocturne Viceroy", "Dusk Sovereign",
    ],
    "merchant_compact": [
        "Unaffiliated", "Ledger Hand", "Road Broker", "Caravan Master", "Coin Architect",
        "Trade Baron", "Harbor Magnate", "Market Syndic", "Guild Chancellor", "Gold Viceroy", "Crown Financier",
    ],
}

RANK_LORE = {
    "iron_brotherhood": {
        1: "You take the oath at the old anvil and are marked in soot and iron.",
        2: "Veterans test your shield arm in rain and mud before the keep gates.",
        3: "You carry the storm banner and are trusted to hold the breach line.",
        4: "Marshals call your name when the walls tremble and men begin to falter.",
        5: "Your hammer-blow is said to ring loud enough to rally a retreating flank.",
        6: "You are given command over the fortress watch and its last reserve.",
        7: "Your sigil is carved into the anvil road where war caravans march.",
        8: "You stand as living rampart while siege engines burn around you.",
        9: "The castle bells answer to your command as the bastion kneels.",
        10: "At coronation steel, you are named Regent of the Unbroken Wall.",
    },
    "arcane_circle": {
        1: "You light the novice candle and copy your first true glyph by hand.",
        2: "Your runes hold steady in stormlight, and the scribes begin to listen.",
        3: "You bind unstable sigils into a single lattice without collapse.",
        4: "Stars are charted by your equations across the observatory glass.",
        5: "You lecture in the aether halls where elder mages once forbade entry.",
        6: "Void scripture is unsealed to you beneath wards older than kings.",
        7: "You curate the forbidden sigils and decide which spells may live.",
        8: "At eclipse, your circle answers and the night itself bends obediently.",
        9: "You preside over astral trials where failed spells can tear the sky.",
        10: "The conclave crowns you Grand Magister, keeper of the final theorem.",
    },
    "shadow_court": {
        1: "You learn to step without breath where lanterns cannot find you.",
        2: "Night couriers trust you with sealed whispers and blood-marked routes.",
        3: "Veil agents report directly to your sign when contracts turn lethal.",
        4: "Your blade is counted among the silk fangs of the inner court.",
        5: "Moonlit hunts are led by your hand through drowned alleys and spires.",
        6: "You execute judgment in silence while the city sleeps unaware.",
        7: "Shades salute when your banner passes beneath the raven balconies.",
        8: "Crown spies carry your seal to kings who fear unseen knives.",
        9: "As Nocturne Viceroy, you govern the dark hours between empires.",
        10: "Dusk Sovereign is spoken only once, and every whisper obeys.",
    },
    "merchant_compact": {
        1: "You are handed a ledger key and assigned your first caravan watch.",
        2: "Road brokers quote your rates from dockside taverns to inland forts.",
        3: "Caravan masters trust you with volatile routes and disputed tariffs.",
        4: "Coin architects seek your sign before mint runs and market openings.",
        5: "Barons of trade concede lanes when your standards reach the harbor.",
        6: "You command freight tides that move nations faster than armies.",
        7: "The syndics vote your terms into law across three great exchanges.",
        8: "Guild chancellors defer when your convoys darken the horizon.",
        9: "As Gold Viceroy, you price famine, peace, and war by the same scale.",
        10: "The Crown names you Financier of the Realm and signs in your ink.",
    },
}

# Per-faction special requirements for rank advancement.
# Rank index starts at 1 (rank 0 is recruit).
RANK_REQUIREMENTS = {
    "iron_brotherhood": {
        2: [("bosses_killed", 1, "Defeat 1 boss")],
        3: [("dungeons_completed", 2, "Complete 2 dungeons")],
        4: [("bosses_killed", 4, "Defeat 4 bosses")],
        5: [("void_titan_killed", 1, "Defeat the Void Titan")],
        6: [("quests_completed", 12, "Complete 12 quests")],
        7: [("bosses_killed", 8, "Defeat 8 bosses")],
        8: [("dungeons_completed", 10, "Complete 10 dungeons")],
        9: [("kills", 400, "Defeat 400 enemies")],
        10: [("void_titan_killed", 2, "Defeat the Void Titan twice")],
    },
    "arcane_circle": {
        2: [("skills_unlocked", 8, "Unlock 8 skills")],
        3: [("quests_completed", 5, "Complete 5 quests")],
        4: [("dungeons_completed", 4, "Complete 4 dungeons")],
        5: [("void_titan_killed", 1, "Defeat the Void Titan")],
        6: [("skills_unlocked", 18, "Unlock 18 skills")],
        7: [("quests_completed", 14, "Complete 14 quests")],
        8: [("dungeons_completed", 12, "Complete 12 dungeons")],
        9: [("kills", 350, "Defeat 350 enemies")],
        10: [("void_titan_killed", 2, "Defeat the Void Titan twice")],
    },
    "shadow_court": {
        2: [("mini_bosses_killed", 2, "Defeat 2 mini-bosses")],
        3: [("treasure_opened", 12, "Open 12 treasure chests")],
        4: [("bosses_killed", 3, "Defeat 3 bosses")],
        5: [("dungeons_completed", 5, "Complete 5 dungeons")],
        6: [("mini_bosses_killed", 8, "Defeat 8 mini-bosses")],
        7: [("treasure_opened", 32, "Open 32 treasure chests")],
        8: [("bosses_killed", 7, "Defeat 7 bosses")],
        9: [("kills", 420, "Defeat 420 enemies")],
        10: [("void_titan_killed", 2, "Defeat the Void Titan twice")],
    },
    "merchant_compact": {
        2: [("total_gold", 2500, "Earn 2500 total gold")],
        3: [("quests_completed", 8, "Complete 8 quests")],
        4: [("islands_discovered", 2, "Discover 2 islands")],
        5: [("dungeons_completed", 6, "Complete 6 dungeons")],
        6: [("total_gold", 9000, "Earn 9000 total gold")],
        7: [("quests_completed", 18, "Complete 18 quests")],
        8: [("islands_discovered", 4, "Discover 4 islands")],
        9: [("dungeons_completed", 14, "Complete 14 dungeons")],
        10: [("void_titan_killed", 2, "Defeat the Void Titan twice")],
    },
}


def _ensure_faction_state(player):
    state = player.state
    state.setdefault("faction_membership", None)
    state.setdefault("faction_xp", {})
    state.setdefault("faction_rank", {})


def _rank_for_xp(xp):
    xp = int(xp)
    rank = 0
    for i, threshold in enumerate(RANK_THRESHOLDS):
        if xp >= threshold:
            rank = i
    return rank


def _rank_bonus_amount(faction_id, rank):
    stat = FACTIONS.get(faction_id, {}).get("rank_stat")
    if not stat or rank <= 0:
        return 0
    if stat == "max_mana":
        return int(rank) * 2
    return int(rank)


def get_rank_name(faction_id, rank):
    names = RANK_TITLES.get(faction_id, [])
    idx = int(max(0, rank))
    if idx < len(names):
        return names[idx]
    return f"Rank {idx}"


def get_rank_lore(faction_id, rank):
    lore_map = RANK_LORE.get(faction_id, {})
    return lore_map.get(int(rank), "No chronicle has yet been written for this station.")


def _progress_value(player, key):
    if key == "islands_discovered":
        return len(player.state.get("unlocked_islands", []) or [])

    tracking = player.state.get("achievement_tracking", {})
    if key in tracking:
        return int(tracking.get(key, 0))
    return int(player.state.get(key, 0))


def _requirements_for_rank(faction_id, rank):
    return list(RANK_REQUIREMENTS.get(faction_id, {}).get(int(rank), []))


def _requirements_met(player, faction_id, rank):
    reqs = _requirements_for_rank(faction_id, rank)
    missing = []
    for key, needed, label in reqs:
        have = _progress_value(player, key)
        if have < int(needed):
            missing.append((label, have, int(needed)))
    return len(missing) == 0, missing


def _rank_line(player, faction_id, rank):
    xp_need = RANK_THRESHOLDS[min(rank, len(RANK_THRESHOLDS) - 1)]
    reqs = _requirements_for_rank(faction_id, rank)
    if not reqs:
        return f"    Rank {rank}: {xp_need} XP"

    parts = []
    for key, needed, label in reqs:
        have = _progress_value(player, key)
        ok = "OK" if have >= int(needed) else "LOCKED"
        parts.append(f"{label} ({have}/{int(needed)} {ok})")
    return f"    Rank {rank}: {xp_need} XP + " + " | ".join(parts)


def get_faction_rank_visual_data(player, faction_id=None):
    _ensure_faction_state(player)
    current_member = player.state.get("faction_membership")
    target = faction_id or current_member
    if not target or target not in FACTIONS:
        return {"faction_id": None, "faction_name": None, "current_rank": 0, "current_xp": 0, "ranks": []}

    fid = str(target).strip().lower().replace(" ", "_")
    if fid not in FACTIONS:
        return {"faction_id": None, "faction_name": None, "current_rank": 0, "current_xp": 0, "ranks": []}

    current_rank = int(player.state.get("faction_rank", {}).get(fid, 0))
    current_xp = int(player.state.get("faction_xp", {}).get(fid, 0))

    rows = []
    for rank in range(1, len(RANK_THRESHOLDS)):
        xp_need = int(RANK_THRESHOLDS[rank])
        reqs = []
        for key, needed, label in _requirements_for_rank(fid, rank):
            have = _progress_value(player, key)
            reqs.append({
                "label": label,
                "have": int(have),
                "needed": int(needed),
                "met": int(have) >= int(needed),
            })
        rows.append({
            "rank": rank,
            "name": get_rank_name(fid, rank),
            "lore": get_rank_lore(fid, rank),
            "xp_required": xp_need,
            "xp_met": current_xp >= xp_need,
            "unlocked": current_rank >= rank,
            "requirements": reqs,
            "requirements_met": all(r["met"] for r in reqs),
        })

    return {
        "faction_id": fid,
        "faction_name": FACTIONS[fid]["name"],
        "current_rank": current_rank,
        "current_rank_name": get_rank_name(fid, current_rank),
        "current_xp": current_xp,
        "ranks": rows,
    }


def get_faction_rank_roadmap_text(player, faction_id=None):
    _ensure_faction_state(player)
    current_member = player.state.get("faction_membership")
    target = faction_id or current_member

    if not target or target not in FACTIONS:
        return "Choose a faction to preview: faction ranks <faction_id>"

    fid = str(target).strip().lower().replace(" ", "_")
    if fid not in FACTIONS:
        return f"Unknown faction '{target}'."

    current_rank = int(player.state.get("faction_rank", {}).get(fid, 0))
    current_xp = int(player.state.get("faction_xp", {}).get(fid, 0))

    result = "\n" + "=" * 58 + "\n"
    result += f"  RANK ROADMAP: {FACTIONS[fid]['name']}\n"
    result += "=" * 58 + "\n"
    result += f"  Current Rank: {current_rank} ({get_rank_name(fid, current_rank)}) | XP: {current_xp}\n"
    result += "\n"

    for rank in range(1, len(RANK_THRESHOLDS)):
        marker = "*" if rank == current_rank else "-"
        result += f"  {marker} " + _rank_line(player, fid, rank).strip() + f" | {get_rank_name(fid, rank)}\n"

    if current_rank < len(RANK_THRESHOLDS) - 1:
        next_rank = current_rank + 1
        met, missing = _requirements_met(player, fid, next_rank)
        xp_need = RANK_THRESHOLDS[next_rank]
        result += "\n"
        if current_xp < xp_need:
            result += f"  Next rank needs {xp_need - current_xp} more faction XP.\n"
        if met:
            result += "  Special requirements met for the next rank.\n"
        else:
            result += "  Missing for next rank:\n"
            for label, have, needed in missing:
                result += f"    - {label}: {have}/{needed}\n"

    result += "=" * 58 + "\n"
    return result


def get_faction_status_text(player):
    _ensure_faction_state(player)
    member = player.state.get("faction_membership")

    result = "\n" + "=" * 58 + "\n"
    result += "  FACTIONS\n"
    result += "=" * 58 + "\n"

    if not member:
        result += "  You are not aligned with any faction.\n"
        result += "  Join with: faction join <faction_id>\n\n"
    else:
        fdata = FACTIONS.get(member, {})
        fxp = int(player.state.get("faction_xp", {}).get(member, 0))
        frank = int(player.state.get("faction_rank", {}).get(member, 0))
        result += f"  Current Faction: {fdata.get('name', member)}\n"
        result += f"  Rank: {frank} ({get_rank_name(member, frank)})\n"
        result += f"  XP: {fxp}\n"
        result += f"  Perk: {fdata.get('perk', 'N/A')}\n\n"
        result += "  Leave with: faction leave\n"
        result += "  Rank path is visualized in the Party/Faction window.\n\n"

    result += "  Available factions:\n"
    for fid, fdata in FACTIONS.items():
        result += f"    - {fid}: {fdata['name']}\n"

    result += "=" * 58 + "\n"
    return result


def join_faction(player, faction_id):
    _ensure_faction_state(player)
    fid = str(faction_id or "").strip().lower().replace(" ", "_")
    if fid not in FACTIONS:
        return False, f"Unknown faction '{faction_id}'."

    current = player.state.get("faction_membership")
    if current == fid:
        return False, f"You are already in {FACTIONS[fid]['name']}."
    if current:
        return False, "You are already bound to a faction this run."

    player.state["faction_membership"] = fid
    player.state["faction_xp"][fid] = int(player.state["faction_xp"].get(fid, 0))
    player.state["faction_rank"][fid] = int(player.state["faction_rank"].get(fid, 0))
    return True, f"Joined faction: {FACTIONS[fid]['name']}."


def leave_faction(player):
    _ensure_faction_state(player)
    current = player.state.get("faction_membership")
    if not current or current not in FACTIONS:
        return False, "You are not currently in a faction."

    rank = int(player.state.get("faction_rank", {}).get(current, 0))
    stat = FACTIONS[current].get("rank_stat")
    amount = _rank_bonus_amount(current, rank)
    if amount > 0 and stat:
        if stat == "max_mana":
            player.stats["max_mana"] = int(player.stats.get("max_mana", 0)) - amount
            player.stats["mana"] = min(int(player.stats.get("mana", 0)), int(player.stats.get("max_mana", 0)))
        else:
            player.stats[stat] = int(player.stats.get(stat, 0)) - amount

    player.state["faction_membership"] = None
    return True, f"You left {FACTIONS[current]['name']}."


def add_faction_xp(player, amount, reason="activity"):
    _ensure_faction_state(player)
    fid = player.state.get("faction_membership")
    if not fid or fid not in FACTIONS:
        return ""

    xp_map = player.state.get("faction_xp", {})
    rank_map = player.state.get("faction_rank", {})

    old_xp = int(xp_map.get(fid, 0))
    new_xp = old_xp + int(max(0, amount))
    xp_map[fid] = new_xp

    old_rank = int(rank_map.get(fid, 0))
    target_rank = _rank_for_xp(new_xp)
    new_rank = old_rank

    # Rank-up can be blocked by special requirements even if XP is sufficient.
    for candidate in range(old_rank + 1, target_rank + 1):
        met, _missing = _requirements_met(player, fid, candidate)
        if not met:
            break
        new_rank = candidate

    rank_map[fid] = new_rank

    text = f"\n  [Faction] +{int(amount)} XP ({reason})"
    if new_rank > old_rank:
        # Apply rank-up stat perk.
        stat = FACTIONS[fid].get("rank_stat")
        if stat == "max_mana":
            player.stats["max_mana"] = int(player.stats.get("max_mana", 0)) + 2
            player.stats["mana"] = int(player.stats.get("mana", 0)) + 2
        elif stat:
            player.stats[stat] = int(player.stats.get(stat, 0)) + 1
        text += f"\n  [Faction] Rank up! {FACTIONS[fid]['name']} rank is now {new_rank} ({get_rank_name(fid, new_rank)})."

    if target_rank > new_rank:
        text += "\n  [Faction] Higher ranks have unmet special requirements. Check the Party/Faction window."

    return text
