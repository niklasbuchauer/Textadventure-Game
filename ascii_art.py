"""
ascii_art.py  —  Central ASCII Art Sprite Library
===================================================
Stone Story RPG-inspired monospace art for all items,
stations, and UI elements in Estoria's Chronicles.

Two layers of art per item:
  ITEM_ICONS   — tiny inline tag (2–5 chars) shown next to item names in panels
  ITEM_SPRITES — multi-line art (5–9 lines) shown in inspect/production overlays

Station art used by crafting minigames is stored in STATION_SPRITES.
Animation frame sequences are stored in ANIMATION_FRAMES.
"""

import pygame

# ──────────────────────────────────────────────────────────────────────────────
#  MINIGAME DIFFICULTY SYSTEM
# ──────────────────────────────────────────────────────────────────────────────
# Global difficulty.  Changed via  set_difficulty("easy"|"normal"|"hard")
# and read by every overlay constructor via  get_diff_params(recipe_tier).

_DIFFICULTY: str = "normal"

# Preset multipliers.  Directions:
#   bar_speed_mult  — bouncing-bar speed   (higher = harder)
#   zone_mult       — catch/pour zone width (lower  = harder)
#   heat_rate_mult  — alchemy heat rising speed (higher = harder)
#   flash_mult      — ritual/show-phase symbol display time  (lower = harder)
#   seq_delta       — extra keys added to forging/rune sequences               (+1 = harder)
#   result_secs     — extra seconds the result screen is shown (cosmetic)
DIFFICULTY_PRESETS: dict = {
    "easy": {
        "bar_speed_mult": 0.55,
        "zone_mult":      1.50,
        "heat_rate_mult": 0.55,
        "flash_mult":     2.20,
        "seq_delta":      -1,
        "result_secs":    1.5,
        "timer_mult":     1.80,  # multiplied against each overlay's BASE_TIMER
    },
    "normal": {
        "bar_speed_mult": 1.00,
        "zone_mult":      1.00,
        "heat_rate_mult": 1.00,
        "flash_mult":     1.00,
        "seq_delta":       0,
        "result_secs":    0.0,
        "timer_mult":     1.00,
    },
    "hard": {
        "bar_speed_mult": 1.50,
        "zone_mult":      0.65,
        "heat_rate_mult": 1.60,
        "flash_mult":     0.55,
        "seq_delta":      +2,
        "result_secs":   -0.5,
        "timer_mult":     0.55,
    },
}

# Per-recipe-tier modifier stacked on top of the global preset.
# tier 1 = basic mats,  tier 2 = refined/mid,  tier 3 = rare/legendary
_TIER_MULTS: dict = {
    1: {"bar_speed_mult": 0.80, "zone_mult": 1.20, "heat_rate_mult": 0.80,
        "flash_mult": 1.30, "seq_delta": -1, "timer_tier_mult": 1.30},
    2: {"bar_speed_mult": 1.00, "zone_mult": 1.00, "heat_rate_mult": 1.00,
        "flash_mult": 1.00, "seq_delta":  0, "timer_tier_mult": 1.00},
    3: {"bar_speed_mult": 1.25, "zone_mult": 0.82, "heat_rate_mult": 1.30,
        "flash_mult": 0.75, "seq_delta": +1, "timer_tier_mult": 0.80},
}

# Ingredients that push a recipe into tier 3 or tier 2
_TIER3_MATS = frozenset({"mithril_ore", "shadow_ore", "shadow_essence",
                          "raw_diamond", "void_crystal", "bone_fragment"})
_TIER2_MATS = frozenset({"gold_ore", "gold_dust", "cave_crystal",
                          "iron_ingot", "mithril_ingot"})


def get_difficulty() -> str:
    """Return the current global difficulty string."""
    return _DIFFICULTY


def set_difficulty(d: str) -> str:
    """Set global difficulty. Returns the new value."""
    global _DIFFICULTY
    if d in DIFFICULTY_PRESETS:
        _DIFFICULTY = d
    return _DIFFICULTY


def infer_recipe_tier(ingredients: dict) -> int:
    """
    Auto-detect a recipe's difficulty tier (1-3) from its ingredient keys.
    Pass the ingredients/materials dict {item_id: count}.
    """
    keys = set(ingredients.keys())
    if keys & _TIER3_MATS:
        return 3
    if keys & _TIER2_MATS:
        return 2
    return 1


def get_diff_params(recipe_tier: int = 2) -> dict:
    """
    Return merged difficulty parameters for a recipe tier.
    Multiplies global preset by the tier modifier.
    """
    diff = DIFFICULTY_PRESETS.get(_DIFFICULTY, DIFFICULTY_PRESETS["normal"])
    tier = _TIER_MULTS.get(max(1, min(3, recipe_tier)), _TIER_MULTS[2])
    return {
        "bar_speed_mult": diff["bar_speed_mult"] * tier["bar_speed_mult"],
        "zone_mult":      diff["zone_mult"]      * tier["zone_mult"],
        "heat_rate_mult": diff["heat_rate_mult"] * tier["heat_rate_mult"],
        "flash_mult":     diff["flash_mult"]     * tier["flash_mult"],
        "seq_delta":      diff["seq_delta"]      + tier["seq_delta"],
        "result_secs":    diff.get("result_secs", 0.0),
        # timer_mult = difficulty scale × tier scale; applied to each overlay's BASE_TIMER
        "timer_mult":     diff.get("timer_mult", 1.0) * tier.get("timer_tier_mult", 1.0),
    }


# ──────────────────────────────────────────────────────────────────────────────
#  CHEESE ART — Easter egg ("doabigcheese" command)
# ──────────────────────────────────────────────────────────────────────────────
CHEESE_ART = r"""
         _______________
        /               \
       /   DO A BIG      \
      /     CHEESE        \
     /___________________/|
    |  ,---.  ,---.  ,---|/
    | /  O  \/  O  \/  O |
    ||  (_)  |  (_)  |(_)|
    | \     / \     / \  |
    |  '---'   '---'  '--|
    |  AGED HAVENBROOK   |
    |   FINEST CHEDDAR   |
    |____________________|
          |||||||
          ||||||||
"""

# ──────────────────────────────────────────────────────────────────────────────
#  ITEM ICONS  (2–5 chars, monospace-friendly)
# ──────────────────────────────────────────────────────────────────────────────
ITEM_ICONS = {
    # — Weapons —
    "wooden_club":          ")-",
    "rusty_sword":          "|-",
    "rusty_dagger":         "/.",
    "copper_dagger":        "/>",
    "wooden_staff":         "|~",
    "iron_sword":           "|--",
    "iron_axe":             "|>-",
    "iron_mace":            "o|-",
    "steel_dagger":         "/--",
    "bronze_spear":         "|->",
    "hunting_bow":          "c->",
    "steel_mace":           "O|-",
    "bronze_sword":         "|--",
    "silver_rapier":        "*/-",
    "steel_longsword":      "|---",
    "steel_battleaxe":      ">|>-",
    "jeweled_dagger":       "*/>",
    "composite_bow":        "C=->",
    "arcane_staff":         "*|~",
    "spectral_blade":       "~|--",
    "mimic_tooth_dagger":   "!/.",
    "mithril_blade":        "#|--",
    "prismatic_blade":      "*|--",
    "shadow_blade":         "~|--",
    "soul_blade":           "†|--",
    "dragonbone_bow":       "D=->",
    "void_staff":           "O|~",
    "death_knight_blade":   "†|---",
    "nightmare_scythe":     ")/.",
    "void_reaper":          "V|--",
    "crystal_cleaver":      "#>|>",
    "frostbite":            "*|--",
    "worldtree_branch":     "Y|~",
    # — Armor —
    "leather_armor_piece":  "[~]",
    "chainmail":            "[#]",
    "plate_armor":          "[=]",
    "padded_armor":         "[o]",
    "iron_helm":            "(^)",
    "padded_helm":          "(~)",
    "leather_boots":        "}v{",
    "iron_boots":           "}={",
    "crystal_shield":       "(*))",
    "wooden_shield":        "(o)",
    "iron_shield":          "[o]",
    # — Accessories —
    "enchanted_ring":       "0*",
    "void_amulet":          "0~",
    "sovereigns_cloak":     "~v~",
    "lich_crown":           "*^*",
    # — Potions & Consumables —
    "healing_potion":       ")(",
    "lesser_healing_potion":")(.",
    "greater_healing_potion":")(+",
    "regeneration_potion":  ")(~",
    "mana_potion":          ")(o",
    "major_mana_potion":    ")(O",
    "strength_potion":      ")(^",
    "ironhide_potion":      ")([",
    "antidote":             ")(x",
    "poison_cure":          ")(+",
    "fire_resistance":      ")(R",
    "frost_resistance":     ")(r",
    "holy_water":           "(+)",
    "healing_salve":        "~-~",
    "torch":                "/!\\",
    "quality_torch":        "/!!\\",
    # — Food —
    "cooked_fish":          "~o~",
    "grilled_trout":        "~O~",
    "hearty_fish_stew":     "(~)",
    "eel_skewer":           "-~-",
    "grilled_perch":        "~O~",
    "golden_sashimi":       "*O*",
    "rainbow_sushi":        "*~*",
    "leviathan_feast":      "!O!",
    "dried_meat":           "=o=",
    "fresh_bread":          "[o]",
    "hearty_stew":          "(o)",
    "mushroom":             "^o",
    "ale_mug":              "(Y)",
    # — Fish —
    "small_fish":           "<})",
    "river_trout":          "<}>",
    "mudfish":              "<~>",
    "seaweed_clump":        "~v~",
    "large_fish":           "<}}>",
    "cave_eel":             "~-~",
    "striped_perch":        "<|}",
    "swamp_catfish":        "<~}",
    "golden_carp":          "*}*",
    "ancient_pike":         "<}--",
    "ghost_fish":           "~}~",
    "leviathan_fry":        "!}!",
    "prismatic_koi":        "*}>",
    "old_boot":             "[/]",
    "waterlogged_chest":    "[~]",
    # — Materials & Ores —
    "iron_ore":             "*Fe",
    "copper_ore":           "*Cu",
    "gold_ore":             "*Au",
    "mithril_ore":          "*Mi",
    "shadow_ore":           "*Sh",
    "coal":                 "*C_",
    "iron_ingot":           "=Fe",
    "copper_ingot":         "=Cu",
    "gold_ingot":           "=Au",
    "mithril_ingot":        "=Mi",
    "shadow_steel_ingot":   "=Sh",
    "refined_iron":         "=Fe+",
    "stick":                "/",
    "rope_coil":            "oo",
    "wolf_pelt":            "~W~",
    "cave_crystal":         "*c*",
    "shadow_essence":       "~s~",
    "bone_fragment":        "!b!",
    "gold_dust":            ".Au.",
    "rare_crystal":         "*R*",
    # — Bait —
    "worm":                 "~w",
    "cricket":              ".c.",
    "glowworm":             "*w",
    "golden_lure":          "*l*",
    "swamp_grub":           "~g",
    # — Tools —
    "old_fishing_rod":      "/~",
    "lockpick_set":         "/-",
    "faded_map":            "[.]",
    "worn_map":             "[o]",
    "old_spyglass":         "O-",
    "spell_scroll":         "~S~",
    "enchanted_candle":     "/!",
    "prayer_candle":        "/+",
    # — Currency —
    "gold":                 "$",
    "bronze_coin":          "c",

    # — Mythic / Hidden Content —
    "solaris_blade":        "*|==",
    "forgotten_blade":      "?|--",
    "dragonfang_dagger":    "D/>",
    "pirate_captain_sword": "~|--",
    "devs_blade":           "</--",
    "dragonscale_armor":    "[D]",
    "archive_robe":         "[~S]",
    "void_cloak":           "[~~]",
    "crown_of_stars":       "*^*",
    "void_titan_crown":     "V^V",
    "ethereal_orb":         "(*)",
    "clockwork_pendant":    "oTo",
    "starweave_ring":       "*o*",
    "clockwork_boots":      "}T{",
    "voidborn_gauntlets":   "[V]",
    "alchemist_key":        "-K-",
    "shadow_shard":         "~S~",
    "blood_sigil":          "!S!",
    "void_shard":           "oVo",
    "ancient_codex":        "[A]",
    "stellar_dust":         "*..",
    "pirate_charter":       "[P]",
    "void_titan_soul":      "oTo",
    "shrine_blessing":      "(+)",
    "developers_note":      "[D]",
    "void_crystal":         "*V*",
}

# ──────────────────────────────────────────────────────────────────────────────
#  ITEM SPRITES  (list of strings, each string = one line)
#  Target: 7–9 lines tall, up to 20 chars wide, Courier New monospace
# ──────────────────────────────────────────────────────────────────────────────
ITEM_SPRITES = {
    # ── WEAPONS ──────────────────────────────────────────────────────────────
    "iron_sword": [
        "     |     ",
        "    /|\\    ",
        "   / | \\   ",
        "  /--+--\\  ",
        "     |     ",
        "    ---    ",
        "     .     ",
    ],
    "steel_longsword": [
        "      |      ",
        "     /|\\     ",
        "    / | \\    ",
        "   /--+--\\   ",
        "      |      ",
        "      |      ",
        "     ---     ",
        "      .      ",
    ],
    "steel_dagger": [
        "    /    ",
        "   /     ",
        "  /      ",
        " /       ",
        "/--      ",
        " \\       ",
        "  .      ",
    ],
    "copper_dagger": [
        "    /    ",
        "   /     ",
        "  /      ",
        " /-      ",
        "  \\      ",
        "   .     ",
    ],
    "hunting_bow": [
        "  (      ",
        " ( \\     ",
        "(   \\    ",
        "(   ->   ",
        "(   /    ",
        " ( /     ",
        "  (      ",
    ],
    "iron_axe": [
        "  /|     ",
        " / |     ",
        "|  |     ",
        " \\ |     ",
        "  \\|     ",
        "   |     ",
        "   .     ",
    ],
    "arcane_staff": [
        "   *     ",
        "  /|     ",
        " / |     ",
        "   |     ",
        "   |     ",
        "   |     ",
        "   o     ",
    ],
    "shadow_blade": [
        "   ~|    ",
        "  ~ |    ",
        " ~  |    ",
        "  ~/|\\   ",
        "    |    ",
        "   ---   ",
        "    .    ",
    ],
    "prismatic_blade": [
        "   *     ",
        "   *|    ",
        "  * |\\   ",
        "  *-+--  ",
        "    |    ",
        "   ---   ",
        "    .    ",
    ],
    "void_reaper": [
        " )--     ",
        ")   --   ",
        " )----   ",
        "  )|     ",
        "  ||     ",
        "  ||     ",
        "   .     ",
    ],
    "frostbite": [
        "    *    ",
        "   *|*   ",
        "  * | *  ",
        " *--+--* ",
        "    |    ",
        "   ---   ",
        "    .    ",
    ],
    # ── ARMOR ─────────────────────────────────────────────────────────────────
    "chainmail": [
        "  /---\\  ",
        " |#####| ",
        " |#####| ",
        " |#####| ",
        " |#####| ",
        "  \\---/  ",
    ],
    "plate_armor": [
        "  /===\\  ",
        " |=====| ",
        " |=====| ",
        " |=.=.=| ",
        " |=====| ",
        "  \\===/  ",
    ],
    "leather_armor_piece": [
        "  /~~~\\  ",
        " |~~~~~| ",
        " |~~~~~| ",
        " |~~~~~| ",
        "  \\~~~/  ",
    ],
    "crystal_shield": [
        "  /*\\    ",
        " / * \\   ",
        "| *** |  ",
        " \\ * /   ",
        "  \\*/    ",
    ],
    "wooden_shield": [
        "  /---\\  ",
        " | [o] | ",
        " | [o] | ",
        " | [o] | ",
        "  \\---/  ",
    ],
    "iron_helm": [
        "  /===\\  ",
        " |=====| ",
        " | (^) | ",
        " |.....| ",
        "  \\===/  ",
    ],
    "leather_boots": [
        " /---\\   ",
        " |~~~|   ",
        " |~~~|   ",
        " |~~~\\___",
        " \\______/",
    ],
    # ── POTIONS ───────────────────────────────────────────────────────────────
    "healing_potion": [
        "   ___   ",
        "  |   |  ",
        "  | + |  ",
        "  |   |  ",
        "  |___|  ",
        " /     \\ ",
        " \\     / ",
        "  \\___/  ",
    ],
    "mana_potion": [
        "   ___   ",
        "  |   |  ",
        "  | o |  ",
        "  |   |  ",
        "  |___|  ",
        " /     \\ ",
        " \\     / ",
        "  \\___/  ",
    ],
    "strength_potion": [
        "   ___   ",
        "  |   |  ",
        "  | ^ |  ",
        "  |   |  ",
        "  |___|  ",
        " /     \\ ",
        " \\     / ",
        "  \\___/  ",
    ],
    "antidote": [
        "   ___   ",
        "  |   |  ",
        "  | x |  ",
        "  |   |  ",
        "  |___|  ",
        " /     \\ ",
        " \\     / ",
        "  \\___/  ",
    ],
    # ── FISH ──────────────────────────────────────────────────────────────────
    "small_fish": [
        "         ",
        "   <}>   ",
        "  <}  >  ",
        " < }   ) ",
        "  <}  >  ",
        "   <}>   ",
        "         ",
    ],
    "river_trout": [
        "         ",
        "   <}}>  ",
        "  <}}  > ",
        " < }}   )",
        "  <}}  > ",
        "   <}}>  ",
        "         ",
    ],
    "golden_carp": [
        "    *    ",
        "   *}*   ",
        "  *}  *  ",
        " * }   ) ",
        "  *}  *  ",
        "   *}*   ",
        "         ",
    ],
    "cave_eel": [
        "         ",
        "  ~~~~~  ",
        " ~~o~~~~  ",
        " ~~~~~~~  ",
        " ~~~~~~~~ ",
        "         ",
    ],
    "leviathan_fry": [
        " !  !    ",
        " !<}}}!  ",
        "!<}}}  ) ",
        "!<}}}   )",
        " !<}}}!  ",
        " !  !    ",
    ],
    "old_boot": [
        " /----\\  ",
        " |~~~~|  ",
        " |~~~~|  ",
        " |~~~~\\_.",
        " \\_______",
    ],
    # ── ORES & INGOTS ─────────────────────────────────────────────────────────
    "iron_ore": [
        "  .---.  ",
        " / * * \\ ",
        "| * Fe* |",
        " \\ * * / ",
        "  '---'  ",
    ],
    "copper_ore": [
        "  .---.  ",
        " / o o \\ ",
        "| o Cu  |",
        " \\ o o / ",
        "  '---'  ",
    ],
    "gold_ore": [
        "  .---.  ",
        " / * * \\ ",
        "| * Au* |",
        " \\ * * / ",
        "  '---'  ",
    ],
    "mithril_ore": [
        "  .---.  ",
        " / # # \\ ",
        "| # Mi# |",
        " \\ # # / ",
        "  '---'  ",
    ],
    "iron_ingot": [
        "         ",
        " /======\\",
        " | IRON |",
        " \\======/",
        "         ",
    ],
    "copper_ingot": [
        "         ",
        " /======\\",
        " | COPP |",
        " \\======/",
        "         ",
    ],
    "gold_ingot": [
        "         ",
        " /======\\",
        " | GOLD |",
        " \\======/",
        "         ",
    ],
    "mithril_ingot": [
        "         ",
        " /======\\",
        " | MITH |",
        " \\======/",
        "         ",
    ],
    "shadow_steel_ingot": [
        "         ",
        " /~~~~~~\\",
        " | SHDW |",
        " \\~~~~~~/",
        "         ",
    ],
    "refined_iron": [
        "         ",
        " /======\\",
        " |+IRON+|",
        " \\======/",
        "         ",
    ],
    # ── MATERIALS ─────────────────────────────────────────────────────────────
    "stick": [
        "      /  ",
        "     /   ",
        "    /    ",
        "   /     ",
        "  /      ",
    ],
    "wolf_pelt": [
        " /\\/\\/\\  ",
        "|  WoLF  |",
        "|  ~~~~  |",
        " \\~~~~~~/ ",
        "  \\~~~~/  ",
    ],
    "cave_crystal": [
        "    *    ",
        "   /|\\   ",
        "  / | \\  ",
        " /  |  \\ ",
        "    |    ",
    ],
    "shadow_essence": [
        "  ~~~~~  ",
        " ~~~ ~~~ ",
        "~ SHADE ~",
        " ~~~ ~~~ ",
        "  ~~~~~  ",
    ],
    # ── FOOD ──────────────────────────────────────────────────────────────────
    "cooked_fish": [
        "   ___   ",
        " ~<}}}~  ",
        " ~{}}}>  ",
        " ~<}}}~  ",
        "  -----  ",
    ],
    "grilled_trout": [
        "  _____  ",
        " ~<}}}}>  ",
        " ~{}}}}>  ",
        " ~<}}}}>  ",
        "  ------  ",
    ],
    "hearty_fish_stew": [
        "  _____  ",
        " /     \\  ",
        "| ~ o ~ | ",
        " \\_____/  ",
        "   (__)   ",
    ],
    "mushroom": [
        "  /---\\  ",
        " /     \\ ",
        "|  ~~~  |",
        "   | |   ",
        "   |_|   ",
    ],
    "ale_mug": [
        "  _____  ",
        " |     |_",
        " |  ~~ ||",
        " | ~~~~ |",
        " |_____|  ",
    ],
    # ── TOOLS ─────────────────────────────────────────────────────────────────
    "torch": [
        "   /!\\   ",
        "   !!!   ",
        "   /!\\   ",
        "    |    ",
        "    |    ",
        "   [|]   ",
    ],
    "old_fishing_rod": [
        "       . ",
        "      /o ",
        "     /   ",
        "    /    ",
        "   /     ",
        "  |      ",
        "  .      ",
    ],
    "lockpick_set": [
        " /---\\   ",
        " | - |   ",
        " | - |   ",
        " | - |   ",
        " \\---/   ",
    ],
    "spell_scroll": [
        "  /---\\  ",
        " /~~~~~\\ ",
        "|  ~ ~  |",
        "|  ~ ~  |",
        " \\~~~~~/ ",
        "  \\---/  ",
    ],

    # ── MYTHIC WEAPONS ────────────────────────────────────────────────────────
    "solaris_blade": [
        "    *    ",
        "   *|*   ",
        "  * | *  ",
        " *--+--* ",
        "    |    ",
        "    |    ",
        "   ---   ",
        "    .    ",
        " MYTHIC  ",
    ],
    "forgotten_blade": [
        "   ???   ",
        "  ?|???  ",
        " ??|??   ",
        "  ?+--   ",
        "    |    ",
        "   ---   ",
        "    .    ",
        " MYTHIC  ",
    ],
    "dragonfang_dagger": [
        "   D     ",
        "  D /    ",
        " D /     ",
        "D /--    ",
        " \\       ",
        "  .      ",
        " MYTHIC  ",
    ],
    "pirate_captain_sword": [
        "     ~   ",
        "    ~|   ",
        "   ~|\\   ",
        "  ~|--   ",
        "    |    ",
        "   ---   ",
        "    .    ",
        " MYTHIC  ",
    ],
    "devs_blade": [
        "   </>   ",
        "  </>|   ",
        " </>--|\\  ",
        "  </>+-- ",
        "     |   ",
        "    ---  ",
        "     .   ",
        " D E V S ",
    ],

    # ── MYTHIC ARMOUR ─────────────────────────────────────────────────────────
    "dragonscale_armor": [
        "  /DDD\\  ",
        " |DDDDD| ",
        " |D>D<D| ",
        " |DDDDD| ",
        " |D>D<D| ",
        "  \\DDD/  ",
        " MYTHIC  ",
    ],
    "archive_robe": [
        "  /~~~\\  ",
        " |~S~~~| ",
        " |~~~~~| ",
        " |~S~~~| ",
        " |~~~~~| ",
        "  \\~~~/  ",
        " MYTHIC  ",
    ],
    "void_cloak": [
        "   .~~~~~~~~~~~~.   ",
        "  /  * .  . * .  \\ ",
        " |  .   void   .  | ",
        " |*.  ________  .*| ",
        "  \\ /  * .  *  \\ /  ",
        "   |  .  .  .   |   ",
        "   /  ~~~~~~~~  \\   ",
        "  / .  * .  * .  \\ ",
        " /_______________\\  ",
        "[   M Y T H I C   ] ",
    ],

    # ── MYTHIC HELMS ──────────────────────────────────────────────────────────
    "crown_of_stars": [
        " *   *   ",
        "* * * *  ",
        " *---*   ",
        " |***|   ",
        " |   |   ",
        "  ---    ",
        " MYTHIC  ",
    ],
    "void_titan_crown": [
        " V   V   ",
        "V V V V  ",
        " V---V   ",
        " |VVV|   ",
        " |   |   ",
        "  ---    ",
        " MYTHIC  ",
    ],

    # ── MYTHIC ACCESSORIES ────────────────────────────────────────────────────
    "ethereal_orb": [
        "  /~~~\\  ",
        " / *** \\ ",
        "| * * * |",
        " \\ *** / ",
        "  \\~~~/  ",
        "   (*)   ",
        " MYTHIC  ",
    ],
    "clockwork_pendant": [
        "  /===\\  ",
        " | o-o | ",
        " |  T  | ",
        " | --- | ",
        "  \\===/  ",
        "   | |   ",
        " MYTHIC  ",
    ],
    "starweave_ring": [
        "   ***   ",
        "  *   *  ",
        " *  *  * ",
        "  *   *  ",
        "   ***   ",
        " MYTHIC  ",
    ],

    # ── MYTHIC TOOLS / KEY ITEMS ──────────────────────────────────────────────
    "alchemist_key": [
        "   O     ",
        "  /|\\    ",
        "   |     ",
        "   |--   ",
        "   |  -  ",
        "         ",
    ],
    "shadow_shard": [
        "   ~     ",
        "  ~S~    ",
        " ~ S ~   ",
        "  ~S~    ",
        "   ~     ",
    ],
    "void_shard": [
        "  .---.  ",
        " / oVo \\ ",
        "| VOID  |",
        " \\ oVo / ",
        "  '---'  ",
        "  RARE!  ",
    ],
    "ancient_codex": [
        "  /===\\  ",
        " |=====| ",
        " | A C | ",
        " |=====| ",
        " |~   ~| ",
        "  \\===/  ",
    ],
}

# Default fallback sprite shown when no sprite is defined for an item
DEFAULT_SPRITE = [
    "  .---.  ",
    " / ??? \\ ",
    "|  ??? |",
    " \\ ??? / ",
    "  '---'  ",
]

def get_icon(item_id: str) -> str:
    """Return the short inline icon for an item. Falls back to a bracketed abbreviation."""
    if item_id in ITEM_ICONS:
        return ITEM_ICONS[item_id]
    # Generate a short abbreviation from the item_id
    parts = item_id.replace("_", " ").split()
    if len(parts) >= 2:
        return parts[0][0].upper() + parts[1][0].upper()
    return item_id[:3].upper() if item_id else "?"

def get_sprite(item_id: str) -> list:
    """Return the multi-line ASCII sprite for an item."""
    return ITEM_SPRITES.get(item_id, DEFAULT_SPRITE)


# ──────────────────────────────────────────────────────────────────────────────
#  STATION SPRITES  (ASCII art for crafting stations)
# ──────────────────────────────────────────────────────────────────────────────
STATION_SPRITES = {
    "forge": [
        "   _____  ",
        "  /=====\\ ",
        " | [===] |",
        " |  |||  |",
        " |_______|",
        "  / | \\ ",
        " /  |  \\ ",
    ],
    "cauldron": [
        "    ___    ",
        "  /     \\  ",
        " | o O o | ",
        " |  ~~~  | ",
        " |_______| ",
        "   |   |   ",
        "   |___|   ",
    ],
    "anvil": [
        "  /-----\\  ",
        " /  ___  \\ ",
        "|  |   |  |",
        " \\ |___| / ",
        "  \\-----/  ",
        "   |   |   ",
        "   |___|   ",
    ],
    "furnace": [
        " /-------\\ ",
        "|  [===]  |",
        "|  | | |  |",
        "|  [===]  |",
        " \\-------/ ",
        "    |_|    ",
    ],
    "campfire": [
        "    /^\\    ",
        "   /^^^\\   ",
        "  /^^^^^\\  ",
        " /   _   \\ ",
        "    / \\    ",
        "   /   \\   ",
        "  /-----\\  ",
    ],
    "altar_crystal": [
        "  *     *  ",
        " * /-\\ *  ",
        "*  |*|  *  ",
        " * \\-/ *  ",
        "  *     *  ",
        "   [===]   ",
        "     |     ",
    ],
    "altar_shadow": [
        "  ~     ~  ",
        " ~ /~\\ ~  ",
        "~  |~|  ~  ",
        " ~ \\~/  ~ ",
        "  ~     ~  ",
        "   [===]   ",
        "     |     ",
    ],
}

# ──────────────────────────────────────────────────────────────────────────────
#  ANIMATION FRAMES
# ──────────────────────────────────────────────────────────────────────────────
#  Each entry is a list of frame lists. Each frame is a list of strings.

ANIMATION_FRAMES = {

    # ── Forging: hammer striking an anvil + shockwave ────────────────────────
    "forging_hammer": [
        # Frame 0: Hammer raised
        [
            "  [###]   ",
            "    |     ",
            "    |     ",
            "          ",
            "  /-----\\ ",
            " /  ___  \\",
            "|___|   |__|",
        ],
        # Frame 1: Hammer mid-swing
        [
            "          ",
            "  [###]   ",
            "    |     ",
            "    v     ",
            "  /-----\\ ",
            " /  ___  \\",
            "|___|   |__|",
        ],
        # Frame 2: Hammer impact
        [
            "          ",
            "          ",
            "  [###]   ",
            " *  |  *  ",
            " */-----\\*",
            " /  ___  \\",
            "|___|   |__|",
        ],
        # Frame 3: Shockwave expanding
        [
            "          ",
            "          ",
            "          ",
            "*  [###] *",
            "* /---\\ * ",
            "/  ___  \\ ",
            "|__|   |__|",
        ],
        # Frame 4: Shockwave fading
        [
            "          ",
            "          ",
            "  [###]   ",
            "    |     ",
            "  /-----\\ ",
            " /  ___  \\",
            "|___|   |__|",
        ],
        # Frame 5: Rest
        [
            "  [###]   ",
            "    |     ",
            "    |     ",
            "          ",
            "  /-----\\ ",
            " /  ___  \\",
            "|___|   |__|",
        ],
    ],

    # ── Alchemy: cauldron with rising bubbles and steam ───────────────────────
    "alchemy_brew": [
        # Frame 0
        [
            "          ",
            "  ~   ~   ",
            "    ___   ",
            "  /     \\ ",
            " |       |",
            " |_______|",
            "   |   |  ",
            "   |___|  ",
        ],
        # Frame 1
        [
            "   o      ",
            "  ~   ~   ",
            "    ___   ",
            "  / o   \\ ",
            " |   O   |",
            " |_______|",
            "   |   |  ",
            "   |___|  ",
        ],
        # Frame 2
        [
            "  o   o   ",
            "   ~ ~    ",
            "    ___   ",
            "  /   O \\ ",
            " | o   o |",
            " |_______|",
            "   |   |  ",
            "   |___|  ",
        ],
        # Frame 3
        [
            " o  O  o  ",
            "  ~   ~   ",
            "    ___   ",
            "  / O o \\ ",
            " |  ~~~  |",
            " |_______|",
            "   |   |  ",
            "   |___|  ",
        ],
        # Frame 4 (boiling)
        [
            " O  o  O  ",
            " o  ~  o  ",
            "    ___   ",
            "  /~~~~~\\ ",
            " |~oOo~~ |",
            " |_______|",
            "   |   |  ",
            "   |___|  ",
        ],
        # Frame 5
        [
            "  O  O    ",
            "  ~  ~  ~ ",
            "    ___   ",
            "  / o o \\ ",
            " |  ~~~  |",
            " |_______|",
            "   |   |  ",
            "   |___|  ",
        ],
    ],

    # ── Smelting: furnace glow with heat shimmer ──────────────────────────────
    "smelting_furnace": [
        # Frame 0: cool
        [
            " /-------\\ ",
            "|  [   ]  |",
            "|  | * |  |",
            "|  [   ]  |",
            " \\-------/ ",
            "    |_|    ",
        ],
        # Frame 1: warming
        [
            " /-------\\ ",
            "|  [===]  |",
            "|  | * |  |",
            "|  [===]  |",
            " \\-------/ ",
            "    |_|    ",
        ],
        # Frame 2: hot
        [
            " /-------\\ ",
            "|* [===] *|",
            "|  |***|  |",
            "|* [===] *|",
            " \\-------/ ",
            "    |_|    ",
        ],
        # Frame 3: very hot (shimmer)
        [
            "*/-~-~-~-\\*",
            "| *[===]* |",
            "| *|***|* |",
            "| *[===]* |",
            " \\-~-~-~-/ ",
            "    |_|    ",
        ],
        # Frame 4: pouring
        [
            " /-------\\ ",
            "|  [===]  |",
            "|  |   |  |",
            "|  [===]  |",
            " \\--   --/ ",
            "   | = |   ",
            "   |___|   ",
        ],
    ],

    # ── Campfire cooking ──────────────────────────────────────────────────────
    "campfire_cook": [
        # Frame 0
        [
            "    ^      ",
            "   /|\\     ",
            "  / | \\    ",
            " /  |  \\   ",
            "/___________\\",
        ],
        # Frame 1
        [
            "   /^\\     ",
            "  /^^^\\    ",
            " / ^^^ \\   ",
            "/   ^   \\  ",
            "/__________\\",
        ],
        # Frame 2
        [
            "  /^^^\\    ",
            " /^^^^^\\   ",
            "/  ^^^  \\  ",
            "/   ^    \\ ",
            "/__________\\",
        ],
        # Frame 3
        [
            "   ^  ^    ",
            "  /|\\^|\\   ",
            " / |  | \\  ",
            "/  |  |  \\ ",
            "/__________\\",
        ],
    ],

    # ── Ritual: animated rune circle ──────────────────────────────────────────
    "ritual_circle": [
        # Frame 0: dim
        [
            "  . - . - .  ",
            " -     -     ",
            ".   . . .   .",
            " -     -     ",
            "  . - . - .  ",
        ],
        # Frame 1: glowing
        [
            "  * - * - *  ",
            " -     -     ",
            "*   * * *   *",
            " -     -     ",
            "  * - * - *  ",
        ],
        # Frame 2: bright
        [
            "  O - O - O  ",
            " -     -     ",
            "O   O O O   O",
            " -     -     ",
            "  O - O - O  ",
        ],
        # Frame 3: dim again
        [
            "  . - . - .  ",
            " -     -     ",
            ".   . . .   .",
            " -     -     ",
            "  . - . - .  ",
        ],
    ],

    # ── Fisher character with rod (used in fishing overlay) ──────────────────
    "fisher_cast": [
        # Frame 0: holding rod
        [
            "   o,     ",
            "  /|\\     ",
            "  / \\     ",
            " |   \\    ",
            " |    o   ",
        ],
        # Frame 1: casting
        [
            "   o,       ",
            "  /|\\___    ",
            "  / \\   \\   ",
            " |        ->",
            "            ",
        ],
        # Frame 2: line in water
        [
            "   o,     ",
            "  /|      ",
            "  / \\     ",
            " |    |   ",
            " |    |   ",
            "~~~~~~|~~~",
            "      v   ",
        ],
    ],

    # ── Fish jumping (catch animation) ───────────────────────────────────────
    "fish_jump": [
        [
            "          ",
            "          ",
            "  <}}>    ",
            "~~~~~~~~~~",
        ],
        [
            "          ",
            "  <}}>    ",
            "   ~~~    ",
            "~~~~~~~~~~",
        ],
        [
            "  <}}>    ",
            "   ~~~    ",
            "          ",
            "~~~~~~~~~~",
        ],
        [
            "  <}}>    ",
            "    \\ /   ",
            "     *    ",
            "~~~~~~~~~~",
        ],
    ],
}


# ──────────────────────────────────────────────────────────────────────────────
#  ASCII RUNES  (used by Rune Inscription minigame)
# ──────────────────────────────────────────────────────────────────────────────
RUNES = {
    "fire":    [" /^\\ ", "|/ \\|", "| * |", "|\\./|", " \\_/ "],
    "frost":   [" *-* ", "-   -", "| + |", "-   -", " *-* "],
    "void":    [" .~. ", "~   ~", "| o |", "~   ~", " .~. "],
    "iron":    [" |=| ", "|===|", "| # |", "|===|", " |_| "],
    "shadow":  [" ~v~ ", "~   ~", "| ~ |", "~   ~", " ~^~ "],
    "crystal": [" /\\ ", "/ * \\", "|***|", "\\ * /", " \\/ "],
    "soul":    [" (+) ", "(   )", "| t |", "(   )", " (+) "],
    "nature":  [" +++ ", "+   +", "| Y |", "+   +", " +++ "],
}

# ── Rune node layouts for the Inscription minigame (W/A/S/D paths) ───────────
# Each tier defines a list of moves the player must replicate.
RUNE_SEQUENCES = {
    "tier1": ["W", "D", "S", "A"],
    "tier2": ["W", "W", "D", "S", "A"],
    "tier3": ["W", "D", "D", "S", "S", "A", "W"],
}


# ──────────────────────────────────────────────────────────────────────────────
#  RENDER HELPER  (used by all overlay classes)
# ──────────────────────────────────────────────────────────────────────────────

_MONO_FONT = None
_SMALL_FONT = None
_TITLE_FONT = None

def _ensure_fonts():
    global _MONO_FONT, _SMALL_FONT, _TITLE_FONT
    if _MONO_FONT is None:
        pygame.font.init()
        _MONO_FONT  = pygame.font.SysFont("Courier New", 14)
        _SMALL_FONT = pygame.font.SysFont("Courier New", 11)
        _TITLE_FONT = pygame.font.SysFont("Courier New", 17, bold=True)


def render_ascii_block(surface, lines, x, y,
                        color=(220, 220, 220), line_height=16,
                        bg_color=None, pad=4):
    """
    Blit a list of text lines as a monospace ASCII block onto *surface*.
    If bg_color is given, a filled rect is drawn behind the text.
    Returns the (width, height) of the block drawn.
    """
    _ensure_fonts()
    if not lines:
        return 0, 0
    max_w = max(_MONO_FONT.size(ln)[0] for ln in lines)
    total_h = len(lines) * line_height

    if bg_color:
        pygame.draw.rect(surface, bg_color,
                         (x - pad, y - pad, max_w + pad * 2, total_h + pad * 2))

    for i, line in enumerate(lines):
        surf = _MONO_FONT.render(line, True, color)
        surface.blit(surf, (x, y + i * line_height))
    return max_w, total_h


def render_title(surface, text, cx, y, color=(220, 180, 80)):
    """Render centered bold title text at (cx, y)."""
    _ensure_fonts()
    surf = _TITLE_FONT.render(text, True, color)
    surface.blit(surf, (cx - surf.get_width() // 2, y))
    return surf.get_height()


def render_label(surface, text, cx, y, color=(170, 170, 170), small=False):
    """Render centered label (small or normal) at (cx, y)."""
    _ensure_fonts()
    font = _SMALL_FONT if small else _MONO_FONT
    surf = font.render(text, True, color)
    surface.blit(surf, (cx - surf.get_width() // 2, y))
    return surf.get_height()


def draw_timer_bar(surface, px: int, py: int, pw: int,
                   time_left: float, time_max: float,
                   bar_h: int = 6, bar_y_offset: int = 30):
    """
    Draw a thin countdown bar just below the panel title.

    Parameters
    ----------
    surface      : pygame Surface to draw on
    px, py, pw   : panel left, top, width (same values passed to draw_panel)
    time_left    : seconds remaining
    time_max     : total seconds at start (for fraction calculation)
    bar_h        : height of the bar in pixels
    bar_y_offset : distance from py to the top of the bar
    """
    import pygame
    if time_max <= 0:
        return
    frac   = max(0.0, min(1.0, time_left / time_max))
    margin = 6
    bx     = px + margin
    by     = py + bar_y_offset
    bw     = pw - margin * 2

    # Background track
    pygame.draw.rect(surface, (35, 35, 50), (bx, by, bw, bar_h), border_radius=3)

    # Filled portion — green → yellow → red
    if frac > 0.5:
        t   = (frac - 0.5) * 2          # 1→0 as frac goes 1→0.5
        col = (
            int(255 * (1 - t)),          # red rises
            int(220 * t + 180 * (1-t)),  # stays green-ish
            30,
        )
    elif frac > 0.25:
        t   = (frac - 0.25) * 4         # 1→0 as frac goes 0.5→0.25
        col = (255, int(180 * t), 30)    # yellow → orange
    else:
        col = (220, 50, 50)              # red

    fill_w = max(1, int(bw * frac))
    pygame.draw.rect(surface, col, (bx, by, fill_w, bar_h), border_radius=3)

    # Border
    pygame.draw.rect(surface, (70, 70, 100), (bx, by, bw, bar_h), 1, border_radius=3)

    # Seconds label on the right
    _ensure_fonts()
    secs_str  = f"{int(time_left) + 1}s" if time_left > 0 else "0s"
    lbl_surf  = _SMALL_FONT.render(secs_str, True, (160, 160, 180))
    surface.blit(lbl_surf, (bx + bw - lbl_surf.get_width() - 2,
                             by - lbl_surf.get_height() - 1))


def draw_dim_overlay(surface, alpha=140):
    """Dimming backdrop."""
    sw, sh = surface.get_size()
    dim = pygame.Surface((sw, sh), pygame.SRCALPHA)
    dim.fill((0, 0, 0, alpha))
    surface.blit(dim, (0, 0))


def draw_panel(surface, rect, title="",
               bg=(18, 18, 30), border=(80, 80, 130)):
    """Draw a rounded dark panel with an optional title."""
    _ensure_fonts()
    x, y, w, h = rect
    pygame.draw.rect(surface, bg, (x, y, w, h), border_radius=8)
    pygame.draw.rect(surface, border, (x, y, w, h), 2, border_radius=8)
    if title:
        render_title(surface, title, x + w // 2, y + 8)
