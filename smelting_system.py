"""
smelting_system.py  —  Ore Smelting System & Furnace Minigame
==============================================================
Processes raw ores into metal ingots at a smeltery / blacksmith furnace.

Minigame: horizontal timing bar (same mechanic as fishing).
  • Marker bounces; press SPACE when it's in the pour zone.
  • Perfect pour → Refined ingot  (+1 quality tier for forging)
  • Good pour    → normal ingot
  • Miss         → slag (low-value byproduct)

Each ore type has a different bar speed and zone width.
Batch smelting (e.g. "smelt 5 iron_ore") requires one press per ore.

Commands added to engine.py:
  smelt            — show smelting recipes at current station
  smelt <ore>      — smelt one unit of that ore
  smelt <n> <ore>  — smelt n units (one timing bar per unit)
"""

import random

try:
    from ascii_art import (
        ANIMATION_FRAMES, STATION_SPRITES,
        render_ascii_block, render_title, render_label,
        draw_dim_overlay, draw_panel, draw_timer_bar, _ensure_fonts,
        get_diff_params, infer_recipe_tier,
    )
    ASCII_ART_AVAILABLE = True
except ImportError:
    ASCII_ART_AVAILABLE = False
    def get_diff_params(tier=2):
        return {"bar_speed_mult":1.0,"zone_mult":1.0,"heat_rate_mult":1.0,
                "flash_mult":1.0,"seq_delta":0,"result_secs":0.0,"timer_mult":1.0}
    def infer_recipe_tier(ing): return 2
    def draw_timer_bar(*a, **k): pass

# ──────────────────────────────────────────────────────────────────────────────
#  SMELT RECIPE DATABASE
# ──────────────────────────────────────────────────────────────────────────────

SMELT_RECIPES = {
    "copper_ore": {
        "name":        "Copper Ore",
        "result":      "copper_ingot",
        "refined":     "refined_copper",
        "bar_speed":   1.4,
        "zone_width":  0.28,    # 28% green zone (easiest)
        "description": "Common copper, easy to melt.",
        "color":       (184, 115, 51),
    },
    "iron_ore": {
        "name":        "Iron Ore",
        "result":      "iron_ingot",
        "refined":     "refined_iron",
        "bar_speed":   1.7,
        "zone_width":  0.24,
        "description": "Robust iron. Requires steady pouring.",
        "color":       (120, 120, 140),
    },
    "gold_ore": {
        "name":        "Gold Ore",
        "result":      "gold_ingot",
        "refined":     "refined_gold",
        "bar_speed":   2.0,
        "zone_width":  0.20,
        "description": "Precious gold. Easily spoiled by misjudged heat.",
        "color":       (255, 210, 50),
    },
    "mithril_ore": {
        "name":        "Mithril Ore",
        "result":      "mithril_ingot",
        "refined":     "refined_mithril",
        "bar_speed":   2.6,
        "zone_width":  0.14,
        "description": "Rare mithril. Demands expert timing.",
        "color":       (130, 190, 255),
    },
    "shadow_ore": {
        "name":        "Shadow Ore",
        "result":      "shadow_steel_ingot",
        "refined":     "refined_shadow_steel",
        "bar_speed":   2.2,
        "zone_width":  0.16,
        "description": "Unstable shadow ore. Volatile at high temperatures.",
        "color":       (100, 80, 160),
    },
    "coal": {
        "name":        "Coal",
        "result":      "coal_block",
        "refined":     "high_grade_coal",
        "bar_speed":   1.5,
        "zone_width":  0.30,
        "description": "Process coal into dense fuel blocks.",
        "color":       (60, 60, 60),
    },
}

SMELT_QUALITY = {
    "refined": {"label": "Refined",  "color": (100, 255, 180), "value_mult": 2.0},
    "normal":  {"label": "Ingot",    "color": (200, 200, 200), "value_mult": 1.0},
    "slag":    {"label": "Slag",     "color": (160, 120, 80),  "value_mult": 0.1},
}


# ──────────────────────────────────────────────────────────────────────────────
#  SMELTING SYSTEM LOGIC
# ──────────────────────────────────────────────────────────────────────────────

class SmeltingSystem:
    """Manages smelting: stat check, batch queuing, result output."""

    def __init__(self, engine):
        self.engine       = engine
        self.pending_smelt = None   # {"ore_id", "recipe", "remaining"}

    # ── Public API ────────────────────────────────────────────────────────────

    def show_smelt_menu(self) -> str:
        """Return text menu of smeltable ores currently in inventory."""
        inv = self.engine.player.inventory
        lines = [
            "\n" + "═" * 55,
            "  🔥  SMELTING MENU",
            "═" * 55,
            "  Type: smelt <ore>         — smelt 1 ore",
            "  Type: smelt <n> <ore>     — smelt n ores\n",
        ]

        found = False
        for ore_id, recipe in SMELT_RECIPES.items():
            qty = inv.get(ore_id, 0)
            if qty > 0:
                found = True
                lines.append(
                    f"  {ore_id:<20s}  x{qty:>3}  →  {recipe['result'].replace('_',' ')}"
                    f"  (speed {recipe['bar_speed']})"
                )
        if not found:
            lines.append("  You have no smeltable ores in your inventory.")

        lines.append("\n  Bonus: perfect timing produces Refined ingots (+50% value,")
        lines.append("         improved crafting results when forging).")
        lines.append("═" * 55)
        return "\n".join(lines)

    def start_smelt(self, args: list) -> str:
        """Parse 'smelt [n] <ore_id>' and open overlay."""
        quantity = 1
        ore_arg  = ""

        if not args:
            return self.show_smelt_menu()

        if len(args) >= 2 and args[0].isdigit():
            quantity = int(args[0])
            ore_arg  = "_".join(args[1:]).lower()
        else:
            ore_arg = "_".join(args).lower()

        # Fuzzy match ore
        ore_id = ore_arg
        if ore_id not in SMELT_RECIPES:
            candidates = [k for k in SMELT_RECIPES if ore_arg in k]
            if len(candidates) == 1:
                ore_id = candidates[0]
            elif candidates:
                return "Ambiguous ore. Did you mean: " + ", ".join(candidates) + "?"
            else:
                return (f"  Unknown ore: '{ore_arg}'.\n"
                        f"  Type 'smelt' to see smeltable ores.")

        # Station check
        if not self._check_smeltery():
            return ("You need to be at a Smeltery or Blacksmith's Forge to smelt ore.\n"
                    "Find the village blacksmith or a dungeon forge.")

        inv = self.engine.player.inventory
        available = inv.get(ore_id, 0)
        if available < 1:
            return f"  You have no {ore_id.replace('_',' ')} to smelt."

        quantity = min(quantity, available)
        recipe   = SMELT_RECIPES[ore_id]

        self.pending_smelt = {
            "ore_id":    ore_id,
            "recipe":    recipe,
            "remaining": quantity,
            "results":   [],
        }

        gui = getattr(self.engine, "gui", None)
        if gui is not None:
            overlay = SmeltingOverlay(self, ore_id, recipe, quantity)
            gui._smelting_overlay = overlay
            return ""

        # Fallback: auto-smelt everything at normal quality
        results = []
        for _ in range(quantity):
            results.append(self._apply_smelt(ore_id, recipe, "normal"))
        return "\n".join(results)

    def _apply_smelt(self, ore_id: str, recipe: dict,
                     quality: str = "normal") -> str:
        """Consume 1 ore, produce result."""
        inv = self.engine.player.inventory
        inv[ore_id] = inv.get(ore_id, 0) - 1
        if inv[ore_id] <= 0:
            del inv[ore_id]

        if quality == "refined":
            result_id = recipe.get("refined", recipe["result"])
        elif quality == "slag":
            result_id = "slag"
        else:
            result_id = recipe["result"]

        inv[result_id] = inv.get(result_id, 0) + 1
        self.engine._inventory_changed = True

        tier = SMELT_QUALITY[quality]
        label = tier["label"]
        result_display = result_id.replace("_", " ").title()

        xp_map = {"refined": 30, "normal": 15, "slag": 5}
        try:
            from progression_system import award_xp
            award_xp(self.engine.player, xp_map.get(quality, 15), "smelting")
        except Exception:
            pass

        if quality == "refined":
            return f"  ⭐ Refined smelt! Produced: {result_display}"
        elif quality == "slag":
            return f"  💀 Missed the pour — produced Slag."
        else:
            return f"  🔥 Smelted: {result_display}"

    def _check_smeltery(self) -> bool:
        """Return True if at a forge or smeltery."""
        room = self.engine.get_room_data(self.engine.player.current_room)
        station = getattr(room, "crafting_station", None)
        if isinstance(room, dict):
            station = room.get("crafting_station")
        if station == "forge":
            return True
        # Also allow "smeltery" room type
        loc_type = getattr(room, "location_type", "")
        if isinstance(room, dict):
            loc_type = room.get("location_type", "")
        return "smeltery" in loc_type.lower() or "forge" in loc_type.lower()

    def to_dict(self) -> dict:
        return {}

    def load_from_dict(self, data: dict):
        pass


# ──────────────────────────────────────────────────────────────────────────────
#  SMELTING OVERLAY (Pygame animated minigame)
# ──────────────────────────────────────────────────────────────────────────────

class SmeltingOverlay:
    """
    Timing bar smelting minigame.

    Top     : animated ASCII furnace (frames from ascii_art.py)
    Middle  : horizontal timing bar with green pour zone
    Bottom  : batch counter and result display
    """

    PANEL_W = 500
    PANEL_H = 360
    BAR_W   = 380
    BAR_H   = 36
    # Base timer: smelting can involve several ores so allow enough time,
    # but the bouncing bar means you can't just wait indefinitely.
    BASE_TIMER = 25.0

    def __init__(self, system: SmeltingSystem, ore_id: str,
                 recipe: dict, quantity: int):
        self.system       = system
        self.ore_id       = ore_id
        self.recipe       = recipe
        self.quantity     = quantity          # total ores to smelt
        self._remaining   = quantity
        self._results     = []               # quality results per ore
        self.done         = False
        self.running      = True

        # ── Difficulty scaling ─────────────────────────────────────────────
        ore_recipe = recipe or {}
        ore_tier = infer_recipe_tier({ore_id: 1})
        dp = get_diff_params(ore_tier)
        self._zone_mult = dp["zone_mult"]

        # generate zone for first press
        self._zone_start, self._zone_end = self._generate_zone()

        # marker (standard bouncing bar like fishing)
        self._pos       = 0.0
        self._direction = 1
        # ×0.80 baseline slowdown so bar is easier to time; hard difficulty counters this
        self._bar_speed = recipe.get("bar_speed", 1.8) * 0.80 * dp["bar_speed_mult"]

        # Countdown timer (counts across all ores)
        self._timer_max  = max(8.0, self.BASE_TIMER * dp["timer_mult"])
        self._time_left  = self._timer_max

        # flash states
        self._flash_timer = 0.0
        self._flash_color = (255, 255, 255)
        self._flash_text  = ""

        # result auto-advance
        self._pause_timer  = 0.0
        self._in_pause     = False

        # animation
        self._anim_frame  = 0
        self._anim_timer  = 0.0
        try:
            self._frames = ANIMATION_FRAMES.get("smelting_furnace", [])
        except Exception:
            self._frames = []

        self._font = None

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _generate_zone(self):
        w = self.recipe.get("zone_width", 0.22) * getattr(self, "_zone_mult", 1.0)
        w = max(0.08, min(0.50, w))  # clamp between 8% and 50%
        start = random.uniform(0.15, 0.85 - w)
        return start, start + w

    # ── Events ───────────────────────────────────────────────────────────────

    def handle_event(self, event):
        import pygame
        if self.done or self._in_pause:
            return
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                self._pour()

    def _pour(self):
        pos = self._pos
        if self._zone_start <= pos <= self._zone_end:
            sweet_w = (self._zone_end - self._zone_start) * 0.35
            sweet_lo = self._zone_start + (self._zone_end - self._zone_start) * 0.35
            sweet_hi = sweet_lo + sweet_w
            if sweet_lo <= pos <= sweet_hi:
                quality = "refined"
            else:
                quality = "normal"
        else:
            dist = min(abs(pos - self._zone_start), abs(pos - self._zone_end))
            quality = "normal" if dist < 0.10 else "slag"

        result_text = self.system._apply_smelt(self.ore_id, self.recipe, quality)
        self._results.append(quality)
        self._remaining -= 1

        tier = SMELT_QUALITY[quality]
        self._flash_color = tier["color"]
        self._flash_text  = result_text.strip()
        self._flash_timer = 0.5

        self._in_pause    = True
        self._pause_timer = 0.0

        # Jump furnace frame to "pouring" frame
        if len(self._frames) >= 5:
            self._anim_frame = 4

    # ── Update ────────────────────────────────────────────────────────────────

    def update(self, dt):
        if self.done:
            return

        # Furnace animation
        self._anim_timer += dt
        frame_dur = 0.22
        while self._anim_timer >= frame_dur:
            self._anim_timer -= frame_dur
            if self._frames:
                self._anim_frame = (self._anim_frame + 1) % len(self._frames)

        # Flash decay
        self._flash_timer = max(0.0, self._flash_timer - dt)

        # Countdown timer — only counts when actively pressing, not during pause
        if not self._in_pause:
            self._time_left -= dt
            if self._time_left <= 0:
                self._time_left = 0.0
                # Auto-fail: lose remaining ores
                self._remaining = 0
                self._in_pause  = True
                self._pause_timer = 0.0
                self._flash_text  = "TIME'S UP"
                self._flash_color = (200, 60, 60)
                self._flash_timer = 1.0

        if self._in_pause:
            self._pause_timer += dt
            if self._pause_timer >= 1.4:  # 1.4s baseline (was 0.9)
                self._in_pause = False
                if self._remaining <= 0:
                    self.done = True
                else:
                    # Reset bar for next ore
                    self._zone_start, self._zone_end = self._generate_zone()
                    self._pos       = 0.0
                    self._direction = 1
            return

        # Bounce marker
        self._pos += self._direction * self._bar_speed * dt
        if self._pos >= 1.0:
            self._pos = 1.0
            self._direction = -1
        elif self._pos <= 0.0:
            self._pos = 0.0
            self._direction = 1

    # ── Render ────────────────────────────────────────────────────────────────

    def render(self, surface):
        import pygame
        self._ensure_fonts()

        sw, sh = surface.get_size()
        pw, ph = self.PANEL_W, self.PANEL_H
        px = (sw - pw) // 2
        py = (sh - ph) // 2

        draw_dim_overlay(surface, 155)
        ore_name = self.recipe["name"]
        draw_panel(surface, (px, py, pw, ph),
                   title=f"SMELTING: {ore_name.upper()}")

        # Countdown timer bar
        if not self.done:
            draw_timer_bar(surface, px, py, pw, self._time_left, self._timer_max)

        # ── Furnace animation ─────────────────────────────────────────────────
        frame_lines = self._frames[self._anim_frame % len(self._frames)] if self._frames else []
        fx = px + pw // 2 - 55
        fy = py + 45
        ore_color = self.recipe.get("color", (200, 200, 200))
        render_ascii_block(surface, frame_lines, fx, fy,
                           color=ore_color, line_height=15)

        # ── Timing bar ────────────────────────────────────────────────────────
        bar_x = px + (pw - self.BAR_W) // 2
        bar_y = py + ph - 120

        pygame.draw.rect(surface, (35, 35, 60),
                         (bar_x, bar_y, self.BAR_W, self.BAR_H))
        pygame.draw.rect(surface, (80, 80, 110),
                         (bar_x, bar_y, self.BAR_W, self.BAR_H), 1)

        # Pour zone (green)
        z0 = bar_x + int(self._zone_start * self.BAR_W)
        z1 = bar_x + int(self._zone_end   * self.BAR_W)
        pygame.draw.rect(surface, (30, 130, 50),
                         (z0, bar_y, z1 - z0, self.BAR_H))

        # Refined sub-zone inside (brighter green)
        w = self._zone_end - self._zone_start
        sw_lo = self._zone_start + w * 0.35
        sw_hi = sw_lo + w * 0.35
        rs0 = bar_x + int(sw_lo * self.BAR_W)
        rs1 = bar_x + int(sw_hi * self.BAR_W)
        pygame.draw.rect(surface, (60, 220, 80),
                         (rs0, bar_y + 4, rs1 - rs0, self.BAR_H - 8))

        # Marker
        mx = bar_x + int(self._pos * self.BAR_W)
        if self._flash_timer > 0:
            marker_col = self._flash_color
        else:
            marker_col = (255, 255, 255)
        pygame.draw.rect(surface, marker_col, (mx, bar_y, 6, self.BAR_H))
        pygame.draw.rect(surface, (255, 220, 0), (mx, bar_y, 6, self.BAR_H), 1)

        # Zone labels
        render_label(surface, "Pour Zone", (z0 + z1) // 2,
                     bar_y + self.BAR_H + 5,
                     color=(100, 220, 100), small=True)
        render_label(surface, "Refined", (rs0 + rs1) // 2,
                     bar_y + self.BAR_H + 17,
                     color=(120, 255, 140), small=True)

        # Instruction
        inst_y = bar_y - 26
        if not self._in_pause:
            render_label(surface, "[SPACE]  to pour",
                         px + pw // 2, inst_y, color=(170, 170, 220))

        # Flash result text
        if self._flash_timer > 0 and self._flash_text:
            render_label(surface, self._flash_text,
                         px + pw // 2, inst_y,
                         color=self._flash_color)

        # Batch counter
        done_count = self.quantity - self._remaining
        batch_text = f"Ore: {done_count} / {self.quantity}  smelted"
        render_label(surface, batch_text,
                     px + pw // 2, py + ph - 26,
                     color=(160, 160, 160), small=True)

    def _ensure_fonts(self):
        if self._font is None:
            import pygame
            pygame.font.init()
            self._font = pygame.font.SysFont("Courier New", 14)
        _ensure_fonts()
