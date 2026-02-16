"""
Equipment System
================
Allows players to equip weapons, armor, shields, and accessories
into dedicated slots. Equipped items provide stat bonuses that
stack on top of the player's base stats.

Equipment slots:
  - weapon:    Increases strength / attack damage
  - armor:     Increases defense / damage reduction
  - shield:    Increases defense further
  - accessory: Varies (perception, charisma, dexterity, etc.)

Items are moved from inventory into the equipment dict in
player.state["equipment"]. Unequipping returns them to inventory.
"""

# ═════════════════════════════════════════════════════════════════════
# EQUIPMENT DATABASE
# ═════════════════════════════════════════════════════════════════════
# Every equippable item needs an entry here defining its slot and
# stat bonuses. Items NOT in this dict cannot be equipped.
# ═════════════════════════════════════════════════════════════════════

EQUIPMENT_DATABASE = {
    # ── WEAPONS (slot: weapon) ────────────────────────────────────
    "rusty_sword": {
        "name": "Rusty Sword",
        "slot": "weapon",
        "description": "A dull, corroded blade. Better than bare fists.",
        "stats": {"strength": 1},
    },
    "steel_dagger": {
        "name": "Steel Dagger",
        "slot": "weapon",
        "description": "A sharp, reliable dagger forged from iron and wood.",
        "stats": {"strength": 2, "dexterity": 1},
    },
    "iron_sword": {
        "name": "Iron Sword",
        "slot": "weapon",
        "description": "A sturdy iron sword. Dependable in combat.",
        "stats": {"strength": 3},
    },
    "steel_longsword": {
        "name": "Steel Longsword",
        "slot": "weapon",
        "description": "A long, balanced blade of tempered steel.",
        "stats": {"strength": 5, "dexterity": 1},
    },
    "jeweled_dagger": {
        "name": "Jeweled Dagger",
        "slot": "weapon",
        "description": "A beautiful dagger set with precious stones. Deceptively deadly.",
        "stats": {"strength": 3, "charisma": 2},
    },
    "rusty_dagger": {
        "name": "Rusty Dagger",
        "slot": "weapon",
        "description": "A small, battered dagger. Barely functional.",
        "stats": {"strength": 1},
    },
    # Dungeon-crafted weapons
    "prismatic_blade": {
        "name": "Prismatic Blade",
        "slot": "weapon",
        "description": "Splits light into deadly rainbows with each swing.",
        "stats": {"strength": 8, "perception": 2},
    },
    "shadow_blade": {
        "name": "Shadow Blade",
        "slot": "weapon",
        "description": "Forged from void and obsidian. Cuts through shadow and steel.",
        "stats": {"strength": 7, "dexterity": 3},
    },
    "mithril_blade": {
        "name": "Mithril Blade",
        "slot": "weapon",
        "description": "Light as a feather, strong as mountains.",
        "stats": {"strength": 9, "dexterity": 2},
    },
    "soul_blade": {
        "name": "Soul Blade",
        "slot": "weapon",
        "description": "Infused with spectral energy. Glows with ghostly fire.",
        "stats": {"strength": 8, "constitution": 2},
    },

    # ── ARMOR (slot: armor) ───────────────────────────────────────
    "leather_armor_piece": {
        "name": "Leather Armor",
        "slot": "armor",
        "description": "Light armor stitched from wolf pelts. Decent protection.",
        "stats": {"defense": 2, "dexterity": 1},
    },
    "dwarven_masterwork": {
        "name": "Dwarven Masterwork Armor",
        "slot": "armor",
        "description": "Forged using ancient dwarven techniques. Nearly indestructible.",
        "stats": {"defense": 8, "constitution": 3},
    },
    "sovereign_cloak": {
        "name": "Sovereign's Cloak",
        "slot": "armor",
        "description": "Woven from the Shadow Sovereign's essence. Grants partial invisibility.",
        "stats": {"defense": 5, "dexterity": 3, "perception": 2},
    },

    # ── SHIELDS (slot: shield) ────────────────────────────────────
    "broken_shield": {
        "name": "Broken Shield",
        "slot": "shield",
        "description": "A battered shield. Still blocks some blows.",
        "stats": {"defense": 1},
    },
    "masterwork_shield": {
        "name": "Masterwork Shield",
        "slot": "shield",
        "description": "Reforged from scrap into something magnificent.",
        "stats": {"defense": 4, "constitution": 1},
    },
    "crystal_shield": {
        "name": "Crystal Shield",
        "slot": "shield",
        "description": "Living crystal that refracts attacks into harmless light.",
        "stats": {"defense": 6, "perception": 1},
    },

    # ── ACCESSORIES (slot: accessory) ─────────────────────────────
    "silver_ring": {
        "name": "Silver Ring",
        "slot": "accessory",
        "description": "A polished silver ring. Faintly magical.",
        "stats": {"charisma": 1},
    },
    "golden_ring": {
        "name": "Golden Ring",
        "slot": "accessory",
        "description": "A gleaming golden ring. Radiates authority.",
        "stats": {"charisma": 2},
    },
    "enchanted_ring": {
        "name": "Enchanted Ring",
        "slot": "accessory",
        "description": "Humming with crystalline energy.",
        "stats": {"perception": 2, "charisma": 1},
    },
    "magic_amulet": {
        "name": "Magic Amulet",
        "slot": "accessory",
        "description": "Pulses with arcane energy. Sharpens the senses.",
        "stats": {"perception": 2, "constitution": 1},
    },
    "void_amulet": {
        "name": "Void Amulet",
        "slot": "accessory",
        "description": "Pulsing with void energy. Protects against shadow attacks.",
        "stats": {"defense": 3, "constitution": 2},
    },
    "lich_crown": {
        "name": "Lich Crown",
        "slot": "accessory",
        "description": "A crown of dark power, restored from its shattered form.",
        "stats": {"strength": 3, "perception": 3, "constitution": 2},
    },
}

# Slot display names and icons
SLOT_INFO = {
    "weapon":    {"name": "Weapon",    "icon": "⚔️"},
    "armor":     {"name": "Armor",     "icon": "🛡️"},
    "shield":    {"name": "Shield",    "icon": "🔰"},
    "accessory": {"name": "Accessory", "icon": "💍"},
}

EQUIPMENT_SLOTS = ["weapon", "armor", "shield", "accessory"]


# ═════════════════════════════════════════════════════════════════════
# EQUIPMENT FUNCTIONS
# ═════════════════════════════════════════════════════════════════════

def is_equippable(item_id):
    """Check if an item can be equipped."""
    return item_id in EQUIPMENT_DATABASE


def get_equipment_info(item_id):
    """Get full equipment data for an item, or None."""
    return EQUIPMENT_DATABASE.get(item_id)


def get_equipment(player):
    """Get the player's current equipment dict. Creates it if missing."""
    if "equipment" not in player.state:
        player.state["equipment"] = {s: None for s in EQUIPMENT_SLOTS}
    return player.state["equipment"]


def get_equipped_item(player, slot):
    """Get the item ID equipped in a given slot, or None."""
    equip = get_equipment(player)
    return equip.get(slot)


def equip_item(player, item_name):
    """
    Equip an item from the player's inventory.

    Returns:
        (success: bool, message: str)
    """
    # Normalize item name
    item_id = item_name.lower().replace(" ", "_")

    # Check if item exists in equipment database
    eq_data = EQUIPMENT_DATABASE.get(item_id)
    if not eq_data:
        return False, f"'{item_name.replace('_', ' ')}' cannot be equipped."

    # Check if player has the item in inventory
    inv = player.inventory
    if inv.get(item_id, 0) <= 0:
        return False, f"You don't have a {eq_data['name']} to equip."

    slot = eq_data["slot"]
    slot_info = SLOT_INFO[slot]
    equip = get_equipment(player)

    # If something is already in this slot, unequip it first
    unequip_msg = ""
    old_item = equip.get(slot)
    if old_item:
        old_data = EQUIPMENT_DATABASE.get(old_item, {})
        old_name = old_data.get("name", old_item.replace("_", " "))
        # Return old item to inventory
        inv[old_item] = inv.get(old_item, 0) + 1
        # Remove stat bonuses from old item
        for stat, val in old_data.get("stats", {}).items():
            player.stats[stat] = player.stats.get(stat, 0) - val
        unequip_msg = f"  Unequipped: {old_name}\n"

    # Remove new item from inventory
    inv[item_id] = inv.get(item_id, 0) - 1
    if inv[item_id] <= 0:
        del inv[item_id]

    # Place in equipment slot
    equip[slot] = item_id

    # Apply stat bonuses
    for stat, val in eq_data.get("stats", {}).items():
        player.stats[stat] = player.stats.get(stat, 0) + val

    # Build result message
    result = "\n" + "=" * 50 + "\n"
    result += f"  {slot_info['icon']} EQUIPPED: {eq_data['name']}\n"
    result += "=" * 50 + "\n"
    if unequip_msg:
        result += unequip_msg
    result += f"  Slot: {slot_info['name']}\n"
    result += f"  {eq_data['description']}\n"
    if eq_data.get("stats"):
        result += "\n  Stat bonuses:\n"
        for stat, val in eq_data["stats"].items():
            nice = stat.replace("_", " ").capitalize()
            result += f"    {nice}: +{val}\n"
    result += "=" * 50 + "\n"
    return True, result


def unequip_item(player, slot_or_name):
    """
    Unequip an item by slot name or item name.

    Returns:
        (success: bool, message: str)
    """
    equip = get_equipment(player)
    slot_or_name = slot_or_name.lower().replace(" ", "_")

    # Try to match by slot first
    if slot_or_name in EQUIPMENT_SLOTS:
        slot = slot_or_name
    else:
        # Try to find by item name
        slot = None
        for s, item_id in equip.items():
            if item_id and (item_id == slot_or_name or
                            item_id.replace("_", " ") == slot_or_name.replace("_", " ")):
                slot = s
                break
        # Also check by display name
        if not slot:
            for s, item_id in equip.items():
                if item_id:
                    eq_data = EQUIPMENT_DATABASE.get(item_id, {})
                    if eq_data.get("name", "").lower().replace(" ", "_") == slot_or_name:
                        slot = s
                        break

    if not slot:
        return False, f"Nothing matching '{slot_or_name.replace('_', ' ')}' is equipped."

    item_id = equip.get(slot)
    if not item_id:
        slot_name = SLOT_INFO.get(slot, {}).get("name", slot)
        return False, f"Nothing is equipped in the {slot_name} slot."

    eq_data = EQUIPMENT_DATABASE.get(item_id, {})
    item_name = eq_data.get("name", item_id.replace("_", " "))
    slot_info = SLOT_INFO[slot]

    # Remove stat bonuses
    for stat, val in eq_data.get("stats", {}).items():
        player.stats[stat] = player.stats.get(stat, 0) - val

    # Return to inventory
    player.inventory[item_id] = player.inventory.get(item_id, 0) + 1

    # Clear slot
    equip[slot] = None

    result = "\n" + "=" * 50 + "\n"
    result += f"  {slot_info['icon']} UNEQUIPPED: {item_name}\n"
    result += "=" * 50 + "\n"
    result += f"  {item_name} returned to inventory.\n"
    if eq_data.get("stats"):
        result += "\n  Removed stat bonuses:\n"
        for stat, val in eq_data["stats"].items():
            nice = stat.replace("_", " ").capitalize()
            result += f"    {nice}: -{val}\n"
    result += "=" * 50 + "\n"
    return True, result


def get_equipment_display(player):
    """
    Get a formatted text display of all equipment slots.

    Returns:
        str: formatted equipment overview
    """
    equip = get_equipment(player)

    result = "\n" + "=" * 50 + "\n"
    result += "  EQUIPMENT\n"
    result += "=" * 50 + "\n"

    for slot in EQUIPMENT_SLOTS:
        info = SLOT_INFO[slot]
        item_id = equip.get(slot)
        if item_id:
            eq_data = EQUIPMENT_DATABASE.get(item_id, {})
            item_name = eq_data.get("name", item_id.replace("_", " "))
            stat_parts = []
            for stat, val in eq_data.get("stats", {}).items():
                nice = stat.replace("_", " ").capitalize()
                stat_parts.append(f"+{val} {nice}")
            stat_str = ", ".join(stat_parts) if stat_parts else ""
            result += f"  {info['icon']} {info['name']:10s} {item_name}"
            if stat_str:
                result += f"  ({stat_str})"
            result += "\n"
        else:
            result += f"  {info['icon']} {info['name']:10s} (empty)\n"

    # Show total equipment bonuses
    totals = get_total_equipment_bonuses(player)
    if any(v != 0 for v in totals.values()):
        result += "\n  --- Total Equipment Bonuses ---\n"
        for stat, val in sorted(totals.items()):
            if val != 0:
                nice = stat.replace("_", " ").capitalize()
                result += f"    {nice}: +{val}\n"

    result += "=" * 50 + "\n"
    return result


def get_total_equipment_bonuses(player):
    """Calculate the total stat bonuses from all equipped items."""
    equip = get_equipment(player)
    totals = {}
    for slot in EQUIPMENT_SLOTS:
        item_id = equip.get(slot)
        if item_id:
            eq_data = EQUIPMENT_DATABASE.get(item_id, {})
            for stat, val in eq_data.get("stats", {}).items():
                totals[stat] = totals.get(stat, 0) + val
    return totals


def get_attack_power(player):
    """
    Calculate the player's total attack power for combat.
    Base: strength stat + weapon bonus.
    """
    strength = player.stats.get("strength", 0)
    # Weapon bonus is already applied to strength via equip_item,
    # but we also add a flat base so unarmed isn't 0
    base_attack = max(1, strength)
    return base_attack


def get_defense_power(player):
    """
    Calculate the player's total defense for combat.
    Defense stat already includes equipment bonuses.
    """
    return player.stats.get("defense", 0)
