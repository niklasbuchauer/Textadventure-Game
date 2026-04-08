# commands_window.py  –  Parchment book commands reference overlay
#
# Pure-pygame, no pygame_gui widgets.  Follows the same pattern as
# journal_window.py for full visual consistency.
#
# Public interface:
#   handle_event(event) -> bool      consumed?
#   update(dt=0.016)
#   draw(surface)
#   is_open() -> bool
#   close()

import pygame
import math
import random

from ui_animation import (
    UI_CLOSE_DUR,
    UI_CONTENT_DUR,
    UI_OPEN_DUR,
    ease_in_out_sine,
    ease_out_back,
)

# ── Colour palette (mirrors journal_window.py) ────────────────────────────────
C_PARCHMENT    = (238, 220, 178)
C_PARCHMENT_L  = (248, 234, 196)
C_INK          = ( 38,  22,   6)
C_INK_MID      = ( 80,  50,  18)
C_INK_LIGHT    = (130,  98,  50)
C_HEADER       = (128,  30,  20)
C_LEATHER      = ( 72,  38,  12)
C_COVER        = ( 88,  50,  18)
C_SPINE_LINE   = ( 52,  26,   8)
C_SELECT_BG    = (210, 180, 118)
C_DIVIDER      = (175, 152, 108)
C_SEARCH_BORDER= (130,  98,  50)
C_SEARCH_BG    = (228, 210, 168)

# ── Category accent colours ───────────────────────────────────────────────────
CAT_COLORS = {
    "Movement":      (60,  90, 155),
    "Exploration":   (60, 130,  80),
    "Inventory":     (140, 90,  25),
    "Combat":        (160,  40,  30),
    "NPC":           (100,  60, 140),
    "Ship Travel":   (40, 120, 150),
    "Dungeon":       (140,  58,  20),
    "Home":          (108,  76,  30),
    "Fishing":       (40, 120, 110),
    "Crafting":      (120, 100,  30),
    "Skills":        (80,  80, 150),
    "System":        (80,  80,  80),
    "Debug / Loot":  (95,  70, 130),
    "Debug / Map":   (70, 110,  55),
    "Debug / Player":(110, 75,  30),
    "Debug / Spawn": (150,  50,  40),
    "Debug / World": (45,  100, 130),
    "Debug / Dungeon":(120, 60, 100),
}

# ── Command tables ────────────────────────────────────────────────────────────
# (verb_label, category, description, usage, example)
COMMANDS = [
    # Movement
    ("go <direction>",      "Movement",    "Move in a direction",                          "go <direction>",        "go north"),
    ("n / s / e / w",       "Movement",    "Quick movement shortcuts",                     "n | s | e | w",         "n"),
    ("go up / u",           "Movement",    "Climb stairs to a previous floor",             "go up",                 "go up"),
    ("go down / d",         "Movement",    "Descend stairs to the next floor",             "go down",               "go down"),
    ("enter",               "Movement",    "Enter a building or dungeon",                  "enter",                 "enter"),
    ("leave / exit",        "Movement",    "Leave current location",                       "leave",                 "exit"),
    # Exploration
    ("look / l",            "Exploration", "Look around the current room",                 "look",                  "l"),
    ("examine <target>",    "Exploration", "Examine something closely",                    "examine <target>",      "examine chest"),
    ("inspect <target>",    "Exploration", "Same as examine",                              "inspect <target>",      "inspect wall"),
    ("search",              "Exploration", "Search for hidden items or traps",             "search",                "search"),
    ("fight",               "Exploration", "Engage a visible enemy in the room",           "fight",                 "fight"),
    ("open map",            "Exploration", "Open the live map window",                     "open map",              "open map"),
    ("close map",           "Exploration", "Close the map window",                         "close map",             "close map"),
    ("rooms / areas",       "Exploration", "Browse all game areas in the room browser",    "rooms",                 "areas"),
    ("bestiary / monsters", "Exploration", "Browse all enemies in the bestiary",           "bestiary",              "monsters"),
    # Inventory
    ("inventory / inv / i", "Inventory",   "View your inventory",                          "inventory",             "i"),
    ("take <item>",         "Inventory",   "Pick up an item from the room",                "take <item>",           "take sword"),
    ("drop <item>",         "Inventory",   "Drop an item from your inventory",             "drop <item>",           "drop torch"),
    ("sell <item>",         "Inventory",   "Sell an item for its standard value",          "sell <item>",           "sell iron ore"),
    ("use <item>",          "Inventory",   "Use an item (potion, torch, etc.)",            "use <item>",            "use health potion"),
    # Combat
    ("attack <target>",     "Combat",      "Attack an enemy with your equipped weapon",    "attack <target>",       "attack goblin"),
    ("defend",              "Combat",      "Take a defensive stance",                      "defend",                "defend"),
    ("flee",                "Combat",      "Attempt to flee combat",                        "flee",                  "flee"),
    ("analyze",             "Combat",      "Analyze weakness, resistance, and threat",      "analyze",               "analyze"),
    ("reposition",          "Combat",      "Improve evasion against upcoming enemy attacks", "reposition",            "reposition"),
    ("guard break",         "Combat",      "Break enemy defense and stagger guarded enemies", "guard break",          "guard break"),
    ("interrupt",           "Combat",      "Prepare to cancel the next enemy ability",      "interrupt",             "interrupt"),
    ("charge",              "Combat",      "Charge power for a stronger next attack",       "charge",                "charge"),
    ("skill <name>",        "Combat",      "Use an active skill in combat",                "skill <name>",          "skill fireball"),
    # NPC
    ("talk to <name>",      "NPC",         "Start a conversation with an NPC",             "talk to <name>",        "talk to innkeeper"),
    ("gift <npc> <item>",   "NPC",         "Give an item as a gift to an NPC",             "gift <npc> <item>",     "gift guard apple"),
    ("reputation / rep",    "NPC",         "View your NPC relationship standings",         "reputation",            "rep"),
    ("rep <npc_name>",      "NPC",         "View a specific NPC's relationship",           "rep <npc_name>",        "rep guard captain"),
    # Ship Travel
    ("board",               "Ship Travel", "List all ships at the current dock",           "board",                 "board"),
    ("board mainland",      "Ship Travel", "Return to Grand Harbor by ship",               "board mainland",        "board mainland"),
    ("board <island>",      "Ship Travel", "Sail to a discovered island",                  "board <island>",        "board eastern isle"),
    # Dungeon
    ("open chest",          "Dungeon",     "Open a treasure chest in the room",            "open chest",            "open chest"),
    ("disarm / disarm trap","Dungeon",     "Attempt to disarm a trap",                     "disarm",                "disarm trap"),
    ("go secret",           "Dungeon",     "Enter a secret passage (if discovered)",       "go secret",             "go secret"),
    ("craft / forge",       "Dungeon",     "Use a crafting altar (if present)",            "craft",                 "forge"),
    ("experiment",          "Dungeon",     "Experiment with items to discover recipes",    "experiment",            "experiment"),
    ("use altar",           "Dungeon",     "Same as craft",                                "use altar",             "use altar"),
    # Home
    ("buy home deed",       "Home",        "Buy your first home deed from Elara",          "buy home deed",         "buy home deed"),
    ("home",                "Home",        "Travel to your pocket home",                   "home",                  "home"),
    ("home edit",           "Home",        "Open the interactive home editor",             "home edit",             "home edit"),
    ("home use",            "Home",        "List usable placed home objects + use commands", "home use",              "home use"),
    ("home bonus",          "Home",        "Show active room utility bonus and duration",   "home bonus",            "home bonus"),
    ("leave / exit home",   "Home",        "Return from home to the overworld",            "leave",                 "exit home"),
    ("place <item>",        "Home",        "Place an item inside your home",               "place <item> [at x y]", "place home_workbench at 2 1"),
    ("remove <item>",       "Home",        "Remove a placed home item",                    "remove <item>",         "remove home_workbench"),
    ("home inventory",      "Home",        "List all placed items in your home",           "home inventory",        "home inventory"),
    ("home upgrades",       "Home",        "Show unlocked/locked home rooms",              "home upgrades",         "home upgrades"),
    ("home rooms",          "Home",        "List all home rooms and lock status",          "home rooms",            "home rooms"),
    ("home room <id>",      "Home",        "Switch to an unlocked home room",              "home room <room_id>",   "home room workshop"),
    ("home unlock <id>",    "Home",        "Unlock a new home room with gold",             "home unlock <room_id>", "home unlock garden"),
    ("home containers",     "Home",        "Show storage containers in current room",       "home containers",       "home containers"),
    ("home store <item>",   "Home",        "Store inventory item in room container",        "home store <item> [qty]", "home store herb_bundle 5"),
    ("home take <item>",    "Home",        "Retrieve stored item from room container",      "home take <item> [qty]", "home take herb_bundle 2"),
    ("home spawn <id>",     "Home",        "Set default room when entering home",           "home spawn <room_id>",  "home spawn bedroom"),
    ("home garden",         "Home",        "Show current garden plot status",               "home garden",           "home garden"),
    ("home plant <item>",   "Home",        "Plant seed/crop in garden plots",               "home plant <item> [qty]", "home plant strange_herb 2"),
    ("home harvest",        "Home",        "Harvest all ready crops from garden",           "home harvest",          "home harvest"),
    ("rename home <name>",  "Home",        "Rename your home",                             "rename home <name>",    "rename home Dream Loft"),
    # Fishing
    ("fish",                "Fishing",     "Cast your line (no bait)",                     "fish",                  "fish"),
    ("fish <bait>",         "Fishing",     "Fish with specific bait for better results",   "fish <bait>",           "fish worm"),
    ("bait",                "Fishing",     "View your bait inventory",                     "bait",                  "bait"),
    # Crafting
    ("craft <recipe>",      "Crafting",    "Craft an item using a known recipe",           "craft <recipe>",        "craft iron sword"),
    ("recipes",             "Crafting",    "View all known crafting recipes",              "recipes",               "recipes"),
    # Skills
    ("skills",              "Skills",      "Open the skill tree window",                   "skills",                "skills"),
    ("assign <skill>",      "Skills",      "Assign a skill point to a skill",              "assign <skill>",        "assign fireball"),
    ("abilities",           "Skills",      "List active class abilities",                  "abilities",             "abilities"),
    ("ability <name>",      "Skills",      "Use a class ability",                          "ability <name>",        "ability second_wind"),
    ("synergy",             "Skills",      "Show active class synergies",                  "synergy",               "synergy"),
    ("achievements",        "Skills",      "Show achievement progress",                    "achievements",          "achievements"),
    ("prestige status",     "Skills",      "Show ascension status and bonuses",            "prestige status",       "prestige status"),
    ("prestige",            "Skills",      "Start ascension flow",                         "prestige",              "prestige"),
    ("faction",             "Skills",      "Show faction status and progression",          "faction",               "faction"),
    ("pet",                 "Skills",      "Show companion status (adopt/ability/bandage)", "pet",                   "pet"),
    ("party",               "Skills",      "Open party/faction management window",         "party",                 "party"),
    # Equipment and appearance
    ("equip <item>",        "Inventory",   "Equip a weapon or armor piece",                "equip <item>",          "equip iron_sword"),
    ("unequip <target>",    "Inventory",   "Unequip by slot or item",                      "unequip <target>",      "unequip weapon"),
    ("equipment",           "Inventory",   "Show currently equipped gear",                 "equipment",             "equipment"),
    ("artifact",            "Inventory",   "Show artifact status / manage relic",          "artifact",              "artifact"),
    ("transmog <slot> <skin>", "Inventory", "Apply or clear cosmetic skin override",       "transmog <slot> <skin|clear>", "transmog weapon slayer_crimson"),
    ("cosmetics",           "Inventory",   "Show unlocked cosmetics and active skins",     "cosmetics",             "cosmetics"),
    # Economy
    ("shop",                "Inventory",   "Show shop help and available actions",         "shop",                  "shop"),
    ("shop browse",         "Inventory",   "Browse current shop inventory",                "shop browse",           "shop browse"),
    ("bank",                "Inventory",   "Show bank help and actions",                   "bank",                  "bank"),
    ("deposit <amount>",    "Inventory",   "Deposit gold into the bank",                   "deposit <amount|all>",  "deposit 500"),
    ("withdraw <amount>",   "Inventory",   "Withdraw gold from the bank",                  "withdraw <amount|all>", "withdraw 200"),
    ("balance",             "Inventory",   "Show current bank balance",                    "balance",               "balance"),
    ("upgrade bank",        "Inventory",   "Upgrade bank storage tier",                    "upgrade bank",          "upgrade bank"),
    # Station and utility commands
    ("brew",                "Crafting",    "Open alchemy/brewing interface",               "brew [recipe]",         "brew"),
    ("smelt",               "Crafting",    "Open smelting interface",                      "smelt [recipe]",        "smelt"),
    ("enchant",             "Crafting",    "Open enchanting interface",                    "enchant",               "enchant"),
    ("ritual",              "Crafting",    "Open ritual interface",                        "ritual [name]",         "ritual"),
    ("hearthstone",         "Home",        "Teleport to home using your Hearthstone",      "hearthstone",           "hearthstone"),
    # System
    ("help / commands",     "System",      "Show this commands reference overlay",         "help",                  "commands"),
    ("loot <boss|miniboss|name>", "System", "Preview elite loot tables",                   "loot <target>",         "loot crystal titan"),
    ("journal",             "System",      "Open your journal / quest log",                "journal",               "journal"),
    ("stats",               "System",      "View your character statistics",               "stats",                 "stats"),
    ("save",                "System",      "Save the game",                                "save",                  "save"),
    ("quit / exit",         "System",      "Quit the game",                                "quit",                  "quit"),
]

DEBUG_COMMANDS = [
    # Debug / Map
    ("debug reveal map",       "Debug / Map",    "Reveal all rooms on the map",                   "debug reveal map",                "debug reveal map"),
    ("debug hide map",         "Debug / Map",    "Hide all rooms on the map",                     "debug hide map",                  "debug hide map"),
    # Debug / Player
    ("debug heal",             "Debug / Player", "Restore HP and MP to full",                     "debug heal",                      "debug heal"),
    ("debug gold <amount>",    "Debug / Player", "Set your gold to a specific amount",            "debug gold <amount>",             "debug gold 9999"),
    ("debug level <n>",        "Debug / Player", "Set your character level",                      "debug level <n>",                 "debug level 10"),
    ("debug skill points <n>", "Debug / Player", "Set your available skill points",               "debug skill points <n>",          "debug skill points 20"),
    ("debug stats",            "Debug / Player", "Show detailed player stats",                    "debug stats",                     "debug stats"),
    ("debug home free",        "Debug / Player", "Grant free home ownership",                      "debug home free",                 "debug home free"),
    ("debug home items",       "Debug / Player", "Add one copy of every home item",                "debug home items",                "debug home items"),
    ("debug home reset",       "Debug / Player", "Fully wipe home ownership and home state",       "debug home reset",                "debug home reset"),
    # Debug / Spawn
    ("debug spawn enemy <id>", "Debug / Spawn",  "Spawn an enemy in the current room",            "debug spawn enemy <id> [level]",  "debug spawn enemy goblin 5"),
    ("debug spawn item <id>",  "Debug / Spawn",  "Spawn an item in your inventory",               "debug spawn item <id>",           "debug spawn item iron_sword"),
    ("debug enemies",          "Debug / Spawn",  "List all available enemy IDs",                  "debug enemies",                   "debug enemies"),
    ("debug items list",       "Debug / Spawn",  "List all available item IDs",                   "debug items list",                "debug items list"),
    ("debug items all",        "Debug / Spawn",  "Open the full item browser window",             "debug items all",                 "debug items all"),
    ("debug loot <target>",    "Debug / Loot",   "Preview elite loot tables via debug",           "debug loot <boss|miniboss|name>", "debug loot crystal titan"),
    ("debug loot sim <type> <id> [runs]", "Debug / Loot", "Simulate elite drops over many runs", "debug loot sim <boss|miniboss> <id> [runs]", "debug loot sim boss crystal_titan 100"),
    ("debug set grant <set> [equip]", "Debug / Player", "Grant all items from a set",            "debug set grant <set_name> [equip]", "debug set grant crystal titan regalia equip"),
    ("debug set clear <set>",  "Debug / Player", "Remove set items from inventory/equipment",     "debug set clear <set_name>",      "debug set clear crystal titan regalia"),
    ("debug set status <set>", "Debug / Player", "Show owned/equipped status for a set",          "debug set status <set_name>",     "debug set status lich king regalia"),
    ("debug cosmetics list",   "Debug / Player", "List all cosmetic skin IDs and unlock states",   "debug cosmetics list",             "debug cosmetics list"),
    ("debug cosmetics unlock <id|all>", "Debug / Player", "Unlock one or all cosmetics",           "debug cosmetics unlock <id|all>",  "debug cosmetics unlock all"),
    ("debug cosmetics lock <id|all>",   "Debug / Player", "Relock one or all cosmetics",           "debug cosmetics lock <id|all>",    "debug cosmetics lock slayer_crimson"),
    ("debug cosmetics apply <slot> <id|clear>", "Debug / Player", "Apply/clear skin override",     "debug cosmetics apply <slot> <id|clear>", "debug cosmetics apply weapon slayer_crimson"),
    ("debug cosmetics preview <slot>", "Debug / Player", "Show valid skins for a specific slot",    "debug cosmetics preview <slot>",   "debug cosmetics preview weapon"),
    ("debug cosmetics randomize [slot]", "Debug / Player", "Randomize valid unlocked skins on equipped gear or one slot", "debug cosmetics randomize [slot]", "debug cosmetics randomize weapon"),
    ("debug cosmetics reset",  "Debug / Player", "Clear all active cosmetic overrides",             "debug cosmetics reset",            "debug cosmetics reset"),
    ("debug cosmetics status", "Debug / Player", "Show unlocked skins and active overrides",        "debug cosmetics status",           "debug cosmetics status"),
    # Debug / World
    ("debug teleport <room>",  "Debug / World",  "Teleport to any room by ID",                    "debug teleport <room_id>",        "debug teleport port_haven"),
    ("debug rooms [page]",     "Debug / World",  "List all rooms (with pagination)",              "debug rooms [page]",              "debug rooms 2"),
    # Debug / Dungeon
    ("debug dungeon list",     "Debug / Dungeon","List all active dungeons",                      "debug dungeon list",              "debug dungeon list"),
    ("debug dungeon open",     "Debug / Dungeon","Force-open a dungeon at current location",      "debug dungeon open [room_id]",    "debug dungeon open"),
    ("debug dungeon close <id>","Debug / Dungeon","Force-close a specific dungeon",               "debug dungeon close <id>",        "debug dungeon close dungeon_1"),
    ("debug dungeon check",    "Debug / Dungeon","Check dungeon integrity / consistency",         "debug dungeon check",             "debug dungeon check"),
    ("debug dungeon entrance", "Debug / Dungeon","Test dungeon entrance animation (5s)",          "debug dungeon entrance",          "debug dungeon entrance"),
    ("debug mode traps",       "Debug / Dungeon","Toggle free trap disarm mode",                  "debug mode traps",                "debug mode traps"),
    # Debug / Quests
    ("debug quest list",       "Debug / Quests", "List all quests with IDs and requirements",     "debug quest list",                "debug quest list"),
    ("debug quest activate <id>", "Debug / Quests", "Activate a quest by ID (respects requirements)", "debug quest activate <id>",   "debug quest activate blacksmith_errand"),
    ("debug quest complete <id>", "Debug / Quests", "Complete quest, trigger rewards & fanfare",  "debug quest complete <id>",       "debug quest complete blacksmith_errand"),
    # Debug / Minigames
    ("debug minigame",              "Debug / Minigames", "List all available minigame overlay IDs", "debug minigame",                  "debug minigame"),
    ("debug minigame forge [id]",   "Debug / Minigames", "Launch forging rhythm minigame",          "debug minigame forge [id]",       "debug minigame forge"),
    ("debug minigame brew [id]",    "Debug / Minigames", "Launch alchemy heat-gauge minigame",      "debug minigame brew [id]",        "debug minigame brew"),
    ("debug minigame smelt [ore]",  "Debug / Minigames", "Launch smelting timing-bar minigame",     "debug minigame smelt [ore]",      "debug minigame smelt iron_ore"),
    ("debug minigame ritual [id]",  "Debug / Minigames", "Launch ritual Simon Says memory puzzle",  "debug minigame ritual [id]",      "debug minigame ritual"),
    ("debug minigame craft [id]",   "Debug / Minigames", "Launch crafting sparkle animation",       "debug minigame craft [id]",       "debug minigame craft"),
    ("debug minigame cook [name]",  "Debug / Minigames", "Launch campfire cooking timing bar",      "debug minigame cook [name]",      "debug minigame cook stew"),
    ("debug minigame rune [tier]",  "Debug / Minigames", "Launch rune inscription trace puzzle",    "debug minigame rune [tier]",      "debug minigame rune 1"),
    ("debug minigame difficulty",   "Debug / Minigames", "Show current minigame difficulty setting","debug minigame difficulty",       "debug minigame difficulty"),
    ("debug minigame difficulty <level>", "Debug / Minigames", "Set minigame difficulty level (easy|normal|hard)", "debug minigame difficulty <level>", "debug minigame difficulty hard"),
]

# ── Helpers ───────────────────────────────────────────────────────────────────
def _font_pick(size: int, bold: bool = False) -> "pygame.font.Font":
    for name in ("Palatino Linotype", "Book Antiqua", "Georgia", "Times New Roman"):
        path = pygame.font.match_font(name, bold=bold)
        if path:
            return pygame.font.Font(path, max(6, size))
    return pygame.font.Font(None, max(8, size + 4))


def _blend(c1, c2, t):
    """t=1 → c1 (text/accent colour),  t=0 → c2 (background — fade start)."""
    t = max(0.0, min(1.0, t))
    return tuple(int(a * t + b * (1 - t)) for a, b in zip(c1, c2))


def _wrap_text(text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        test = cur + (" " if cur else "") + w
        if font.size(test)[0] <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ══════════════════════════════════════════════════════════════════════════════
class CommandsOverlay:
    """
    Full-screen parchment command reference overlay.
    Left page: tabs (Commands/Debug) + search + command list.
    Right page: selected command detail.
    """

    OPEN_DUR    = UI_OPEN_DUR
    CLOSE_DUR   = UI_CLOSE_DUR
    CONTENT_DUR = UI_CONTENT_DUR
    _SPOTS_SEED = 5192

    def __init__(self, gui):
        self.gui      = gui
        self._alive   = True
        self._closing = False
        self._anim    = 0.0
        self._cfade   = 0.0

        self._tab        = 0          # 0=Commands, 1=Debug
        self._flat: list = []         # [(cat|None, idx|None, label), …]
        self._sel_idx    = -1
        self._search_text    = ""
        self._search_active  = False
        self._scroll         = 0
        self._rows_visible   = 0

        self._book_rect   = pygame.Rect(0, 0, 0, 0)
        self._close_rect  = pygame.Rect(0, 0, 0, 0)
        self._search_rect = pygame.Rect(0, 0, 0, 0)
        self._tab0_rect   = pygame.Rect(0, 0, 0, 0)
        self._tab1_rect   = pygame.Rect(0, 0, 0, 0)
        self._row_rects: list = []
        self._sf    = 1.0
        self._dst_x = 0
        self._dst_y = 0

        self._fcache: dict = {}
        self._book_bg_cache_size = (0, 0)
        self._book_bg_cache = None
        self._apply_filter("")

    # ── Lifecycle ──────────────────────────────────────────────────────────────

    def is_open(self) -> bool:
        return self._alive

    def close(self):
        if not self._closing:
            self._closing = True

    # ── Fonts ──────────────────────────────────────────────────────────────────

    def _f(self, size, bold=False):
        key = (size, bold)
        if key not in self._fcache:
            self._fcache[key] = _font_pick(size, bold)
        return self._fcache[key]

    # ── Data ───────────────────────────────────────────────────────────────────

    def _source(self):
        return DEBUG_COMMANDS if self._tab == 1 else COMMANDS

    def _apply_filter(self, query):
        q = query.lower().strip()
        src = self._source()
        matches = [
            (i, row) for i, row in enumerate(src)
            if not q
               or q in row[0].lower()
               or q in row[1].lower()
               or q in row[2].lower()
        ]
        groups: dict = {}
        for idx, row in matches:
            groups.setdefault(row[1], []).append((idx, row))

        flat = []
        seen_cats = []
        for _, row in matches:
            if row[1] not in seen_cats:
                seen_cats.append(row[1])
        for cat in seen_cats:
            items = groups[cat]
            flat.append((cat, None, f"{cat}  ({len(items)})"))
            for idx, row in items:
                flat.append((None, idx, f"  {row[0]}"))

        self._flat   = flat
        self._scroll = 0
        if self._sel_idx >= len(flat):
            self._sel_idx = -1

    # ── Update ─────────────────────────────────────────────────────────────────

    def update(self, dt=0.016):
        if self._closing:
            self._anim = max(0.0, self._anim - dt / self.CLOSE_DUR)
            if self._anim <= 0.0:
                self._alive = False
            return
        self._anim  = min(1.0, self._anim  + dt / self.OPEN_DUR)
        self._cfade = min(1.0, self._cfade + dt / self.CONTENT_DUR)

    # ── Events ─────────────────────────────────────────────────────────────────

    def handle_event(self, event) -> bool:
        if not self._alive or self._closing:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.close(); return True
            if self._search_active:
                if event.key == pygame.K_BACKSPACE:
                    self._search_text = self._search_text[:-1]
                    self._apply_filter(self._search_text)
                    return True
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    self._search_active = False; return True
                elif event.unicode and event.unicode.isprintable():
                    self._search_text += event.unicode
                    self._apply_filter(self._search_text)
                    return True
            if event.key == pygame.K_UP:
                self._move_sel(-1); return True
            if event.key == pygame.K_DOWN:
                self._move_sel(1); return True
            if event.key == pygame.K_TAB:
                self._tab = 1 - self._tab
                self._search_text = ""; self._apply_filter(""); return True

        if event.type == pygame.MOUSEWHEEL:
            self._scroll = max(0, self._scroll - event.y)
            return True

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            if self._close_rect.collidepoint(pos):
                self.close(); return True
            if self._tab0_rect.collidepoint(pos):
                self._tab = 0; self._search_text = ""; self._apply_filter(""); return True
            if self._tab1_rect.collidepoint(pos):
                self._tab = 1; self._search_text = ""; self._apply_filter(""); return True
            if self._search_rect.collidepoint(pos):
                self._search_active = True; return True
            else:
                self._search_active = False
            for rect, fidx in self._row_rects:
                if rect.collidepoint(pos):
                    _, src_idx, _ = self._flat[fidx]
                    if src_idx is not None:
                        self._sel_idx = fidx
                    return True
            if not self._book_rect.collidepoint(pos):
                self.close()
            return True

        return False

    def _move_sel(self, delta):
        ri = [i for i, (_, sidx, _) in enumerate(self._flat) if sidx is not None]
        if not ri:
            return
        if self._sel_idx < 0 or self._sel_idx not in ri:
            self._sel_idx = ri[0] if delta > 0 else ri[-1]
        else:
            ci = ri.index(self._sel_idx)
            ci = max(0, min(len(ri) - 1, ci + delta))
            self._sel_idx = ri[ci]
        if self._sel_idx < self._scroll:
            self._scroll = self._sel_idx
        elif self._rows_visible and self._sel_idx >= self._scroll + self._rows_visible:
            self._scroll = self._sel_idx - self._rows_visible + 1

    # ── Draw ───────────────────────────────────────────────────────────────────

    def draw(self, surface):
        if not self._alive:
            return
        if self._closing:
            motion = ease_in_out_sine(self._anim)
        else:
            motion = min(1.0, ease_out_back(self._anim))
        if motion < 0.02:
            return

        sw, sh = surface.get_size()
        BW = min(880, sw - 40)
        BH = min(600, sh - 40)

        bg_s = pygame.Surface((sw, sh), pygame.SRCALPHA)
        bg_s.fill((0, 0, 0, int(165 * motion)))
        surface.blit(bg_s, (0, 0))

        scale = 0.90 + (0.10 * motion)
        y_offset = int((1.0 - motion) * 14)

        if scale < 0.995:
            sbw = max(2, int(BW * scale))
            sbh = max(2, int(BH * scale))
            self._sf    = sbw / BW
            self._dst_x = (sw - sbw) // 2
            self._dst_y = (sh - sbh) // 2 + y_offset
        else:
            sbw = sbh = 0
            self._sf    = 1.0
            self._dst_x = (sw - BW) // 2
            self._dst_y = (sh - BH) // 2 + y_offset

        book_surf = pygame.Surface((BW, BH), pygame.SRCALPHA)
        self._draw_book(book_surf, BW, BH)

        if scale < 0.995:
            scaled = pygame.transform.smoothscale(book_surf, (sbw, sbh))
            surface.blit(scaled, (self._dst_x, self._dst_y))
        else:
            surface.blit(book_surf, (self._dst_x, self._dst_y))

        def _tr(r):
            return pygame.Rect(int(self._dst_x + r.x * self._sf),
                               int(self._dst_y + r.y * self._sf),
                               max(1, int(r.width  * self._sf)),
                               max(1, int(r.height * self._sf)))

        self._book_rect   = pygame.Rect(self._dst_x, self._dst_y,
                                         int(BW * self._sf), int(BH * self._sf))
        self._close_rect  = _tr(self._close_rect)
        self._search_rect = _tr(self._search_rect)
        self._tab0_rect   = _tr(self._tab0_rect)
        self._tab1_rect   = _tr(self._tab1_rect)
        self._row_rects   = [(_tr(r), fi) for r, fi in self._row_rects]

    # ── Core book draw ─────────────────────────────────────────────────────────

    def _get_book_bg_layer(self, BW, BH):
        if self._book_bg_cache is not None and self._book_bg_cache_size == (BW, BH):
            return self._book_bg_cache

        layer = pygame.Surface((BW, BH), pygame.SRCALPHA)
        MID = BW // 2

        pygame.draw.rect(layer, C_PARCHMENT, pygame.Rect(0, 0, BW // 2 + 3, BH), border_radius=8)
        pygame.draw.rect(layer, C_PARCHMENT_L, pygame.Rect(MID - 2, 0, BW // 2 + 2, BH), border_radius=8)

        rng = random.Random(self._SPOTS_SEED)
        spot_s = pygame.Surface((BW, BH), pygame.SRCALPHA)
        for _ in range(130):
            pygame.draw.circle(spot_s, (90, 60, 22, rng.randint(10, 30)),
                               (rng.randint(6, BW - 6), rng.randint(6, BH - 6)),
                               rng.randint(2, 7))
        layer.blit(spot_s, (0, 0))

        pygame.draw.rect(layer, C_LEATHER, pygame.Rect(MID - 11, 0, 22, BH))
        pygame.draw.rect(layer, C_COVER, pygame.Rect(MID - 4, 0, 4, BH))
        for i in range(1, 7):
            ly = int(BH * i / 7)
            pygame.draw.rect(layer, C_SPINE_LINE, pygame.Rect(MID - 11, ly - 2, 22, 4), border_radius=1)

        pygame.draw.rect(layer, C_COVER, pygame.Rect(0, 0, BW, BH), width=3, border_radius=8)

        self._book_bg_cache = layer
        self._book_bg_cache_size = (BW, BH)
        return layer

    def _draw_book(self, surf, BW, BH):
        MID = BW // 2
        cf  = self._cfade

        sh_s = pygame.Surface((BW + 28, BH + 28), pygame.SRCALPHA)
        pygame.draw.rect(sh_s, (0, 0, 0, 85), pygame.Rect(16, 16, BW, BH), border_radius=10)
        surf.blit(sh_s, (-14, -14))

        surf.blit(self._get_book_bg_layer(BW, BH), (0, 0))

        pad = 16
        lf = pygame.Rect(pad,      pad, BW // 2 - pad - 14, BH - pad * 2)
        rf = pygame.Rect(MID + 14, pad, BW // 2 - pad - 14, BH - pad * 2)
        pygame.draw.rect(surf, C_INK_LIGHT, lf, width=1)
        pygame.draw.rect(surf, C_INK_LIGHT, rf, width=1)

        self._draw_left_page(surf, lf, cf)
        self._draw_right_page(surf, rf, cf)

        fade_a = int(255 * (1.0 - cf))
        if fade_a > 4:
            for rect, base in ((lf, C_PARCHMENT), (rf, C_PARCHMENT_L)):
                fs = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
                fs.fill((*base, fade_a))
                surf.blit(fs, (rect.x, rect.y))

        cbr = pygame.Rect(BW - 34, 6, 26, 26)
        sf = self._sf if self._sf else 1.0
        mx_r, my_r = pygame.mouse.get_pos()
        mx_l = (mx_r - self._dst_x) / sf
        my_l = (my_r - self._dst_y) / sf
        c_col = (190, 80, 60) if cbr.collidepoint(mx_l, my_l) else (148, 56, 40)
        pygame.draw.rect(surf, c_col, cbr, border_radius=5)
        _xs = self._f(13, bold=True).render("✕", True, (255, 238, 228))
        surf.blit(_xs, _xs.get_rect(center=cbr.center))
        self._close_rect = cbr  # book-local; translated to screen in draw()

    # ── Left page ──────────────────────────────────────────────────────────────

    def _draw_left_page(self, surf, frame, cf):
        ink   = _blend(C_INK,       C_PARCHMENT, cf)
        mid   = _blend(C_INK_MID,   C_PARCHMENT, cf)
        head  = _blend(C_HEADER,    C_PARCHMENT, cf)
        light = _blend(C_INK_LIGHT, C_PARCHMENT, cf)
        div   = _blend(C_DIVIDER,   C_PARCHMENT, cf)

        # ── Tabs ──────────────────────────────────────────────────────────────
        tab_w = 98
        tab_h = 24
        tab_y = frame.y + 3
        tabs  = [("Commands", 0), ("Debug", 1)]
        for i, (label, tidx) in enumerate(tabs):
            tr = pygame.Rect(frame.x + i * (tab_w + 6), tab_y, tab_w, tab_h)
            if tidx == self._tab:
                bg_col = _blend(C_SELECT_BG, C_PARCHMENT, cf * 0.8)
                pygame.draw.rect(surf, bg_col, tr, border_radius=4)
                pygame.draw.line(surf, head, (tr.x + 4, tr.bottom), (tr.right - 4, tr.bottom), 2)
                lbl_c = ink
            else:
                lbl_c = light
            surf.blit(self._f(11, bold=(tidx == self._tab)).render(label, True, lbl_c),
                      (tr.x + 8, tr.y + 5))
            # Store book-local; draw() translates to screen
            if tidx == 0:
                self._tab0_rect = tr
            else:
                self._tab1_rect = tr

        pygame.draw.line(surf, div, (frame.x + 4, frame.y + 30),
                         (frame.x + frame.width - 4, frame.y + 30), 1)

        # ── Search bar ────────────────────────────────────────────────────────
        sb_y = frame.y + 34
        sbr  = pygame.Rect(frame.x + 2, sb_y, frame.width - 4, 22)
        self._search_rect = sbr  # book-local; translated to screen in draw()
        pygame.draw.rect(surf, _blend(C_SEARCH_BG,     C_PARCHMENT, cf), sbr, border_radius=3)
        pygame.draw.rect(surf, _blend(C_SEARCH_BORDER, C_PARCHMENT, cf), sbr, width=1, border_radius=3)
        disp  = self._search_text[-30:] if self._search_text else "Search commands…"
        t_col = ink if self._search_text else light
        ss    = self._f(10).render(disp, True, t_col)
        surf.blit(ss, (sbr.x + 5, sbr.y + 4))
        if self._search_active and int(pygame.time.get_ticks() / 530) % 2 == 0:
            pygame.draw.line(surf, ink,
                             (sbr.x + 5 + ss.get_width() + 1, sbr.y + 4),
                             (sbr.x + 5 + ss.get_width() + 1, sbr.y + 18), 1)
        pygame.draw.line(surf, div, (frame.x + 4, sb_y + 26),
                         (frame.x + frame.width - 4, sb_y + 26), 1)

        # ── Command list ──────────────────────────────────────────────────────
        list_top = sb_y + 30
        row_h    = 19
        avail_h  = frame.bottom - list_top - 18
        self._rows_visible = max(1, avail_h // row_h)

        max_scroll = max(0, len(self._flat) - self._rows_visible)
        self._scroll = max(0, min(self._scroll, max_scroll))

        self._row_rects = []
        y = list_top
        sf = self._sf if self._sf else 1.0
        mx_s = int((pygame.mouse.get_pos()[0] - self._dst_x) / sf)
        my_s = int((pygame.mouse.get_pos()[1] - self._dst_y) / sf)

        for fi in range(self._scroll, min(self._scroll + self._rows_visible, len(self._flat))):
            cat, src_idx, label = self._flat[fi]
            abs_r = pygame.Rect(frame.x, y, frame.width, row_h)  # book-local

            if src_idx is None:
                cat_col = _blend(CAT_COLORS.get(cat, (80, 80, 80)), C_PARCHMENT, cf)
                surf.blit(self._f(9, bold=True).render(label, True, cat_col),
                          (frame.x + 4, y + 2))
                pygame.draw.line(surf, _blend(C_DIVIDER, C_PARCHMENT, cf * 0.6),
                                 (frame.x + 4, y + row_h - 1),
                                 (frame.x + frame.width - 4, y + row_h - 1), 1)
            else:
                self._row_rects.append((abs_r, fi))
                is_sel = (fi == self._sel_idx)
                is_hov = abs_r.collidepoint(mx_s, my_s)
                pulse = 0.90 + 0.10 * math.sin(pygame.time.get_ticks() * 0.008)
                if is_sel:
                    hs = pygame.Surface((frame.width, row_h), pygame.SRCALPHA)
                    hs.fill((*C_SELECT_BG, int(175 * cf * pulse)))
                    surf.blit(hs, (frame.x, y))
                    pygame.draw.rect(surf, _blend(C_INK_MID, C_PARCHMENT, cf),
                                     pygame.Rect(frame.x + 3, y + 2, 2, row_h - 4), border_radius=1)
                elif is_hov:
                    hs = pygame.Surface((frame.width, row_h), pygame.SRCALPHA)
                    hs.fill((*C_SELECT_BG, int(70 * cf * pulse)))
                    surf.blit(hs, (frame.x, y))
                text_x = frame.x + 6 + (1 if is_hov else 0) + (1 if is_sel else 0)
                surf.blit(self._f(10, bold=is_sel).render(label[:40], True,
                                                           ink if is_sel else mid),
                          (text_x, y + 3))
            y += row_h

        # Scrollbar
        if len(self._flat) > self._rows_visible:
            th = max(14, int(avail_h * self._rows_visible / len(self._flat)))
            ty = list_top + int((avail_h - th) * self._scroll / max(1, max_scroll))
            pygame.draw.rect(surf, light,
                             pygame.Rect(frame.right - 5, list_top, 3, avail_h), border_radius=1)
            pygame.draw.rect(surf, _blend(C_INK_MID, C_PARCHMENT, cf),
                             pygame.Rect(frame.right - 5, ty, 3, th), border_radius=1)

        n = sum(1 for _, sidx, _ in self._flat if sidx is not None)
        hint = "Tab to switch · Esc to close"
        surf.blit(self._f(9).render(f"{n} commands  ·  {hint}", True, light),
                  (frame.x + 4, frame.bottom - 14))

    # ── Right page ─────────────────────────────────────────────────────────────

    def _draw_right_page(self, surf, frame, cf):
        ink   = _blend(C_INK,       C_PARCHMENT_L, cf)
        mid   = _blend(C_INK_MID,   C_PARCHMENT_L, cf)
        head  = _blend(C_HEADER,    C_PARCHMENT_L, cf)
        light = _blend(C_INK_LIGHT, C_PARCHMENT_L, cf)
        div   = _blend(C_DIVIDER,   C_PARCHMENT_L, cf)

        if self._sel_idx < 0 or self._sel_idx >= len(self._flat):
            return self._draw_empty_right(surf, frame, head, mid, light, div)
        _, src_idx, _ = self._flat[self._sel_idx]
        if src_idx is None:
            return self._draw_empty_right(surf, frame, head, mid, light, div)

        src = self._source()
        if src_idx >= len(src):
            return self._draw_empty_right(surf, frame, head, mid, light, div)

        verb, cat, desc, usage, example = src[src_idx]

        # Verb
        surf.blit(self._f(16, bold=True).render(verb[:34], True, head),
                  (frame.x + 5, frame.y + 3))
        pygame.draw.line(surf, div, (frame.x + 4, frame.y + 25),
                         (frame.x + frame.width - 4, frame.y + 25), 1)

        y = frame.y + 30
        cat_col = _blend(CAT_COLORS.get(cat, (80, 80, 80)), C_PARCHMENT_L, cf)
        surf.blit(self._f(10, bold=True).render(cat, True, cat_col),
                  (frame.x + 6, y)); y += 20

        pygame.draw.line(surf, div, (frame.x + 4, y), (frame.x + frame.width - 4, y), 1); y += 8

        # Description
        surf.blit(self._f(11, bold=True).render("DESCRIPTION", True, ink),
                  (frame.x + 6, y)); y += 16
        for line in _wrap_text(desc, self._f(11), frame.width - 14):
            surf.blit(self._f(11).render(line, True, mid), (frame.x + 8, y)); y += 16
        y += 8

        # Usage
        pygame.draw.line(surf, div, (frame.x + 4, y), (frame.x + frame.width - 4, y), 1); y += 8
        surf.blit(self._f(11, bold=True).render("USAGE", True, ink),
                  (frame.x + 6, y)); y += 15
        ub_col = _blend((45, 90, 140), C_PARCHMENT_L, cf)
        surf.blit(self._f(11).render(usage, True, ub_col), (frame.x + 8, y)); y += 20

        # Example
        surf.blit(self._f(11, bold=True).render("EXAMPLE", True, ink),
                  (frame.x + 6, y)); y += 15
        ex_col = _blend((35, 110, 60), C_PARCHMENT_L, cf)
        surf.blit(self._f(11).render(f"> {example}", True, ex_col),
                  (frame.x + 8, y)); y += 20

        y += 10
        pygame.draw.line(surf, div, (frame.x + 4, y), (frame.x + frame.width - 4, y), 1)

    def _draw_empty_right(self, surf, frame, head, mid, light, div):
        surf.blit(self._f(16, bold=True).render("Commands", True, head),
                  (frame.x + 6, frame.y + 3))
        pygame.draw.line(surf, div, (frame.x + 4, frame.y + 25),
                         (frame.x + frame.width - 4, frame.y + 25), 1)
        y = frame.y + 40
        for line in ["Every command in the game is",
                     "listed in this reference.",
                     "",
                     "Switch tabs with Tab key.",
                     "Search by verb, category,",
                     "or description.",
                     "",
                     "Select a command for details.",
                     "", "",
                     "— Esc to close —"]:
            surf.blit(self._f(12).render(line, True, light if line.startswith("—") else mid),
                      (frame.x + 8, y))
            y += 18
