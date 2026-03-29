"""
forging_system.py  —  Forging System & Animated Minigame
==========================================================
A separate, dedicated system for item forging.

Forging differs from basic crafting in:
  • Requires raw ores (not pre-made ingots)
  • Has a rhythm-sequence minigame (hammer-strike pattern)
  • Quality outcome: normal / masterwork / flawless
  • Flawless items have a +15% stat bonus and "(Flawless)" name tag
  • Masterwork items have a +7% stat bonus

Minigame rules:
  • Show a 4-key sequence (W / A / S / D)
  • Player must press them in the correct order
  • 3 rounds total per forge
  • A wrong key resets the current round (no full-fail, just quality penalty)
  • Perfect rounds (0 mistakes) = higher quality tier
  • Results: 3/3 perfect → Flawless, 2/3 → Masterwork, else Normal

Commands added to engine.py:
  forge             — open forging menu at current station
  forge <item>      — start forging a specific item
"""

import random
import time
import math

try:
    from ascii_art import (
        ANIMATION_FRAMES, STATION_SPRITES, get_sprite, get_icon,
        render_ascii_block, render_title, render_label,
        draw_dim_overlay, draw_panel, draw_timer_bar, _ensure_fonts,
        _MONO_FONT, _SMALL_FONT, _TITLE_FONT,
        get_diff_params, infer_recipe_tier,
    )
    ASCII_ART_AVAILABLE = True
except ImportError:
    ASCII_ART_AVAILABLE = False
    def get_diff_params(t=2): return {"bar_speed_mult":1,"zone_mult":1,"heat_rate_mult":1,"flash_mult":1,"seq_delta":0,"result_secs":0,"timer_mult":1.0}
    def infer_recipe_tier(i): return 2
    def draw_timer_bar(*a, **k): pass

# ──────────────────────────────────────────────────────────────────────────────
#  FORGING RECIPE DATABASE
# ──────────────────────────────────────────────────────────────────────────────
# Raw ore-based recipes, separate from crafting_system.py's ingot-based ones.
# Ingredients reference ore/raw materials directly.
# quality_mod: extra base stat bonus applied by this recipe before quality scaling

FORGING_RECIPES = {
    # ── Blades ────────────────────────────────────────────────────────────────
    "forged_iron_dagger": {
        "name":        "Forged Iron Dagger",
        "category":    "weapon",
        "ingredients": {"iron_ore": 2, "stick": 1},
        "result":      ("iron_dagger", 1),
        "station":     "forge",
        "description": "A freshly forged iron dagger, sharp and reliable.",
        "rounds":      2,
        "quality_mod": {"attack": 1},
    },
    "forged_iron_sword": {
        "name":        "Forged Iron Sword",
        "category":    "weapon",
        "ingredients": {"iron_ore": 3, "stick": 1},
        "result":      ("iron_sword", 1),
        "station":     "forge",
        "description": "Hammered from raw iron ore. The heat of the forge lingers.",
        "rounds":      3,
        "quality_mod": {"attack": 2},
    },
    "forged_steel_longsword": {
        "name":        "Forged Steel Longsword",
        "category":    "weapon",
        "ingredients": {"iron_ore": 5, "coal": 2},
        "result":      ("steel_longsword", 1),
        "station":     "forge",
        "description": "Carbon-hardened steel demands perfect hammer timing.",
        "rounds":      4,
        "quality_mod": {"attack": 4},
    },
    "forged_battle_axe": {
        "name":        "Forged Battle Axe",
        "category":    "weapon",
        "ingredients": {"iron_ore": 4, "stick": 2},
        "result":      ("iron_axe", 1),
        "station":     "forge",
        "description": "An axe head shaped under heavy hammer blows.",
        "rounds":      3,
        "quality_mod": {"attack": 3},
    },
    "forged_mithril_blade": {
        "name":        "Forged Mithril Blade",
        "category":    "weapon",
        "ingredients": {"mithril_ore": 4, "coal": 3, "iron_ore": 1},
        "result":      ("mithril_blade", 1),
        "station":     "forge",
        "description": "Mithril demands exceptional skill and patience at the anvil.",
        "rounds":      5,
        "quality_mod": {"attack": 8},
    },
    # ── Armor ─────────────────────────────────────────────────────────────────
    "forged_chainmail": {
        "name":        "Forged Chainmail",
        "category":    "armor",
        "ingredients": {"iron_ore": 4, "rope_coil": 2},
        "result":      ("chainmail", 1),
        "station":     "forge",
        "description": "Interlocking rings of iron hammered into wearable protection.",
        "rounds":      3,
        "quality_mod": {"defense": 2},
    },
    "forged_plate_armor": {
        "name":        "Forged Plate Armor",
        "category":    "armor",
        "ingredients": {"iron_ore": 6, "coal": 2},
        "result":      ("plate_armor", 1),
        "station":     "forge",
        "description": "Heavy plate requires sustained, precise hammer work.",
        "rounds":      4,
        "quality_mod": {"defense": 4},
    },
    "forged_iron_helm": {
        "name":        "Forged Iron Helm",
        "category":    "armor",
        "ingredients": {"iron_ore": 3},
        "result":      ("iron_helm", 1),
        "station":     "forge",
        "description": "A sturdy helm shaped over the horn of the anvil.",
        "rounds":      2,
        "quality_mod": {"defense": 2},
    },
    "forged_iron_shield": {
        "name":        "Forged Iron Shield",
        "category":    "armor",
        "ingredients": {"iron_ore": 3, "stick": 1},
        "result":      ("iron_shield", 1),
        "station":     "forge",
        "description": "A round shield beaten from a flat iron blank.",
        "rounds":      3,
        "quality_mod": {"defense": 3},
    },
    "forged_iron_boots": {
        "name":        "Forged Iron Boots",
        "category":    "armor",
        "ingredients": {"iron_ore": 2, "rope_coil": 1},
        "result":      ("iron_boots", 1),
        "station":     "forge",
        "description": "Solid iron sabatons.",
        "rounds":      2,
        "quality_mod": {"defense": 1},
    },
}

# Quality tiers
QUALITY_TIERS = {
    "flawless":   {"label": "Flawless",   "stat_mult": 1.15, "color": (180, 255, 180)},
    "masterwork": {"label": "Masterwork", "stat_mult": 1.07, "color": (255, 220, 100)},
    "normal":     {"label": "Normal",     "stat_mult": 1.00, "color": (200, 200, 200)},
}

# Key sequences used in minigame — pool includes 4, 5, and 6-key variants
_KEY_SEQUENCES = [
    # 4-key (baseline)
    ["W", "A", "S", "D"],
    ["W", "D", "S", "A"],
    ["A", "W", "D", "S"],
    ["S", "A", "W", "D"],
    ["D", "S", "A", "W"],
    ["W", "S", "A", "D"],
    ["D", "W", "S", "A"],
    # 5-key (harder / used when seq_delta >= 1)
    ["W", "A", "S", "D", "W"],
    ["D", "W", "A", "S", "D"],
    ["A", "S", "D", "W", "S"],
    ["S", "D", "W", "A", "W"],
    ["W", "D", "A", "W", "S"],
    # 6-key (very hard / used when seq_delta >= 2)
    ["W", "A", "S", "D", "W", "A"],
    ["D", "W", "S", "A", "D", "W"],
    ["A", "D", "W", "S", "A", "S"],
]


# ──────────────────────────────────────────────────────────────────────────────
#  FORGING SYSTEM LOGIC
# ──────────────────────────────────────────────────────────────────────────────

class ForgingSystem:
    """Manages forging: checks stations, deducts materials, applies quality."""

    def __init__(self, engine):
        self.engine = engine
        self.pending_forge = None          # set while minigame runs
        self._forging_skill_xp = 0
        self._forging_level = 1

    # ── Public API ────────────────────────────────────────────────────────────

    def show_forge_menu(self) -> str:
        """Return the text menu listing available forging recipes."""
        room = self.engine.get_room_data(self.engine.player.current_room)
        station = getattr(room, "crafting_station", None)
        if isinstance(room, dict):
            station = room.get("crafting_station")

        if station != "forge":
            return (
                "You need to be at a Blacksmith's Forge to use forging.\n"
                "Look for the village blacksmith or a forge station."
            )

        inv = self.engine.player.inventory
        lines = ["\n" + "═" * 55,
                 "  🔨  FORGING MENU",
                 "═" * 55,
                 "  Type: forge <recipe_name>  to begin forging.\n"]

        available = []
        unavailable = []

        for rid, recipe in FORGING_RECIPES.items():
            can_forge = all(inv.get(k, 0) >= v
                            for k, v in recipe["ingredients"].items())
            ing = ", ".join(f"{v}x {k.replace('_',' ')}"
                            for k, v in recipe["ingredients"].items())
            entry = f"  {rid:<30s}  [{ing}]"
            if can_forge:
                available.append(entry)
            else:
                needed = [f"{v-inv.get(k,0)}x {k.replace('_',' ')}"
                          for k, v in recipe["ingredients"].items()
                          if inv.get(k, 0) < v]
                unavailable.append(entry + f"\n    (need: {', '.join(needed)})")

        if available:
            lines.append("  ── AVAILABLE ──")
            lines.extend(available)
        if unavailable:
            lines.append("\n  ── NEED MORE MATERIALS ──")
            lines.extend(unavailable)

        lines.append("═" * 55)
        return "\n".join(lines)

    def start_forge(self, recipe_id: str) -> str:
        """Validate and start forging. Opens overlay if pygame GUI is available."""
        recipe_id = recipe_id.replace(" ", "_").lower()

        # Try fuzzy match
        if recipe_id not in FORGING_RECIPES:
            candidates = [r for r in FORGING_RECIPES if recipe_id in r]
            if len(candidates) == 1:
                recipe_id = candidates[0]
            elif candidates:
                names = ", ".join(candidates)
                return f"  Ambiguous recipe. Did you mean: {names}?"
            else:
                return (f"  Unknown forging recipe: '{recipe_id}'.\n"
                        f"  Type 'forge' to see available recipes.")

        recipe = FORGING_RECIPES[recipe_id]

        # Station check
        room = self.engine.get_room_data(self.engine.player.current_room)
        station = getattr(room, "crafting_station", None)
        if isinstance(room, dict):
            station = room.get("crafting_station")
        if station != recipe.get("station", "forge"):
            return "You need to be at a Blacksmith's Forge to forge this."

        # Materials check
        inv = self.engine.player.inventory
        missing = [(k, v - inv.get(k, 0))
                   for k, v in recipe["ingredients"].items()
                   if inv.get(k, 0) < v]
        if missing:
            lines = ["  You don't have the required materials:"]
            for name, deficit in missing:
                lines.append(f"    • {name.replace('_',' ')}: need {deficit} more")
            return "\n".join(lines)

        # Store pending
        self.pending_forge = {
            "recipe_id": recipe_id,
            "recipe":    recipe,
        }

        # Open overlay if pygame GUI available
        gui = getattr(self.engine, "gui", None)
        if gui is not None:
            overlay = ForgingOverlay(self, recipe)
            gui._forging_overlay = overlay
            return ""   # GUI will handle result display

        # Fallback: text-only auto-craft at normal quality
        return self._apply_forge(recipe, quality="normal")

    def _apply_forge(self, recipe: dict, quality: str = "normal") -> str:
        """Deduct ingredients and add result item(s) to inventory."""
        inv = self.engine.player.inventory
        # Deduct
        for k, v in recipe["ingredients"].items():
            inv[k] = inv.get(k, 0) - v
            if inv[k] <= 0:
                del inv[k]

        result_id, qty = recipe["result"]
        self.engine.player.inventory[result_id] = (
            self.engine.player.inventory.get(result_id, 0) + qty
        )
        # Store quality flag in player state
        quality_records = self.engine.player.state.setdefault("forged_quality", {})
        quality_records[result_id] = quality

        self.engine._inventory_changed = True
        self.pending_forge = None

        tier = QUALITY_TIERS[quality]
        q_label = tier["label"]
        display_name = recipe["name"]
        if quality != "normal":
            display_name = f"{display_name} [{q_label}]"

        xp_map = {"flawless": 60, "masterwork": 40, "normal": 20}
        self._award_forge_xp(xp_map.get(quality, 20))

        lines = [
            "\n" + "═" * 50,
            f"  🔨 Forging complete!",
            f"  You crafted: {display_name} x{qty}",
            f"  Quality: {q_label}",
            "═" * 50,
        ]
        if quality == "flawless":
            lines.insert(2, "  ✨ FLAWLESS WORK! Your timing was perfect!")
        elif quality == "masterwork":
            lines.insert(2, "  ⭐ Masterwork quality! Excellent effort!")

        return "\n".join(lines)

    def _award_forge_xp(self, amount: int):
        """Award XP to the forging meta-skill and progression system."""
        self._forging_skill_xp += amount
        try:
            from progression_system import award_xp
            award_xp(self.engine.player, amount, "forging")
        except Exception:
            pass

    def to_dict(self) -> dict:
        return {
            "forging_skill_xp": self._forging_skill_xp,
            "forging_level":    self._forging_level,
        }

    def load_from_dict(self, data: dict):
        if isinstance(data, dict):
            self._forging_skill_xp = data.get("forging_skill_xp", 0)
            self._forging_level    = data.get("forging_level", 1)


# ──────────────────────────────────────────────────────────────────────────────
#  FORGING OVERLAY (Pygame animated minigame)
# ──────────────────────────────────────────────────────────────────────────────

class ForgingOverlay:
    """
    Rhythm/sequence forging minigame overlay.

    The player sees a 4-key sequence (W/A/S/D) and must press them in order.
    3 rounds total; a mistake resets the current round (but costs 1 quality point).
    After all rounds, quality is determined and result is applied.

    Visual:
      • Animated hammer hitting an anvil (ASCII frames from ascii_art.py)
      • The item being forged shown on the anvil
      • Key sequence displayed as highlighted tiles
      • Shockwave animation on each correct hit
    """

    PANEL_W    = 560
    PANEL_H    = 440
    ANIM_FPS   = 6        # frames per second for hammer animation
    BASE_TIMER = 15.0     # seconds at normal difficulty / tier-2 materials

    _KEY_MAP = {
        # pygame.K_w / a / s / d
    }

    def __init__(self, system: ForgingSystem, recipe: dict):
        self.system   = system
        self.recipe   = recipe
        self.done     = False
        self.running  = True

        # ── Difficulty scaling ────────────────────────────────────────────────
        ingredients = recipe.get("ingredients", recipe.get("materials", {}))
        recipe_tier = infer_recipe_tier(ingredients)
        dp = get_diff_params(recipe_tier)
        seq_delta = int(dp["seq_delta"])   # extra keys added to each sequence
        self._result_extra = max(0.0, dp["result_secs"])

        # Countdown timer — active while player is forging (not during result display)
        self._timer_max  = max(6.0, self.BASE_TIMER * dp["timer_mult"])
        self._time_left  = self._timer_max

        # Base rounds from recipe, floored at 2, +1 for "longer" baseline
        base_rounds = recipe.get("rounds", 3) + 1  # +1 = baseline longer duration
        self._total_rounds   = max(2, base_rounds)
        self._current_round  = 0
        self._perfect_rounds = 0

        # Build sequences: pick from pool matching desired length
        #   seq_delta -1 uses 4-key, 0 uses 4-key (+1 shown), +1 uses 5-key, +2 uses 6-key
        target_len = 4 + max(0, seq_delta)  # clamp: min 4 keys
        matching = [s for s in _KEY_SEQUENCES if len(s) == target_len]
        if not matching:
            matching = [s for s in _KEY_SEQUENCES if len(s) == 4]
        pool = matching[:]
        random.shuffle(pool)
        self._sequences = [pool[i % len(pool)] for i in range(self._total_rounds)]

        self._current_seq_progress = 0
        self._mistakes_this_round  = 0
        self._round_active         = True

        # Animation state
        self._anim_frame    = 0
        self._anim_timer    = 0.0
        self._hit_flash     = 0.0
        self._wrong_flash   = 0.0
        self._shockwave_r   = 0.0

        # Result phase
        self._result_text   = ""
        self._result_color  = (220, 220, 220)
        self._result_timer  = 0.0
        self._show_result   = False

        # Fonts (lazy)
        self._font       = None
        self._small_font = None
        self._title_font = None

        try:
            self._frames = ANIMATION_FRAMES.get("forging_hammer", [])
        except Exception:
            self._frames = []

    # ── Event handling ────────────────────────────────────────────────────────

    def handle_event(self, event):
        import pygame
        if self.done or not self.running or self._show_result:
            return

        if event.type == pygame.KEYDOWN:
            key_name = pygame.key.name(event.key).upper()
            if key_name in ("W", "A", "S", "D"):
                self._process_key(key_name)

    def _process_key(self, key):
        if self._current_round >= self._total_rounds:
            return

        seq = self._sequences[self._current_round]
        expected = seq[self._current_seq_progress]

        if key == expected:
            # Correct!
            self._current_seq_progress += 1
            self._hit_flash   = 0.25
            self._shockwave_r = 1.0
            self._anim_frame  = 2   # jump to impact frame

            if self._current_seq_progress >= len(seq):
                # Round complete
                if self._mistakes_this_round == 0:
                    self._perfect_rounds += 1
                self._current_round        += 1
                self._current_seq_progress  = 0
                self._mistakes_this_round   = 0

                if self._current_round >= self._total_rounds:
                    self._finish()
        else:
            # Wrong key
            self._mistakes_this_round  += 1
            self._wrong_flash           = 0.4
            self._current_seq_progress  = 0   # reset sequence progress

    def _finish(self):
        """Determine quality and apply forge result."""
        self.running = False

        perfect = self._perfect_rounds
        total   = self._total_rounds
        accuracy = int((perfect / max(total, 1)) * 100)

        if perfect >= total:
            quality = "flawless"
        elif perfect >= total - 1:
            quality = "masterwork"
        else:
            quality = "normal"

        result_text = self.system._apply_forge(self.recipe, quality=quality)

        # Display result with accuracy
        tier = QUALITY_TIERS[quality]
        self._result_text  = f"{tier['label']} — {self._perfect_rounds}/{self._total_rounds} perfect rounds ({accuracy}% accuracy)"
        self._result_color = tier["color"]
        self._show_result  = True
        self._result_timer = 0.0

        # Append engine result to GUI
        gui = getattr(self.system.engine, "gui", None)
        if gui and result_text:
            gui.append(result_text)
    def _timeout(self):
        """Called when the countdown timer runs out."""
        self.running       = False
        self._result_text  = "TIME'S UP  —  NO ITEM FORGED"
        self._result_color = (200, 60, 60)
        self._show_result  = True
        self._result_timer = 0.0
        gui = getattr(self.system.engine, "gui", None)
        if gui:
            recipe_name = self.recipe.get("name", "item")
            gui.append(f"  ❌ Forge failed: {recipe_name}. No item was forged.")
    # ── Update ────────────────────────────────────────────────────────────────

    def update(self, dt):
        if self.done:
            return

        # Advance hammer animation
        self._anim_timer += dt
        frame_dur = 1.0 / max(self.ANIM_FPS, 1)
        while self._anim_timer >= frame_dur:
            self._anim_timer -= frame_dur
            if self._frames:
                self._anim_frame = (self._anim_frame + 1) % len(self._frames)

        # Decay flashes
        self._hit_flash   = max(0.0, self._hit_flash   - dt)
        self._wrong_flash = max(0.0, self._wrong_flash - dt)

        # Decay shockwave
        if self._shockwave_r > 0:
            self._shockwave_r = max(0.0, self._shockwave_r - dt * 4)

        # Countdown timer (only during active forging, not result screen)
        if self.running and not self._show_result:
            self._time_left -= dt
            if self._time_left <= 0:
                self._time_left = 0.0
                self._timeout()

        # Result display timeout — 2.8s baseline + difficulty result_secs bonus
        if self._show_result:
            self._result_timer += dt
            if self._result_timer >= 2.8 + self._result_extra:
                self.done = True

    # ── Render ────────────────────────────────────────────────────────────────

    def render(self, surface):
        import pygame
        self._ensure_fonts()

        sw, sh = surface.get_size()
        pw, ph = self.PANEL_W, self.PANEL_H
        px = (sw - pw) // 2
        py = (sh - ph) // 2

        # Dim background
        draw_dim_overlay(surface, 160)

        # Panel
        draw_panel(surface, (px, py, pw, ph),
                   title=f"FORGING: {self.recipe['name'].upper()}")

        # Countdown timer bar
        if not self._show_result:
            draw_timer_bar(surface, px, py, pw, self._time_left, self._timer_max)

        # ── Hammer + Anvil Animation ──────────────────────────────────────────
        anim_x = px + pw // 2 - 60
        anim_y = py + 45

        frame_lines = self._frames[self._anim_frame % len(self._frames)] if self._frames else []

        # Hit flash (green tint) or wrong flash (red tint)
        if self._wrong_flash > 0:
            art_color = (255, 80, 80)
        elif self._hit_flash > 0:
            art_color = (100, 255, 100)
        else:
            art_color = (200, 200, 200)

        if frame_lines:
            render_ascii_block(surface, frame_lines, anim_x, anim_y,
                               color=art_color, line_height=15)

        # Shockwave — expanding circle
        if self._shockwave_r > 0.05:
            anvil_cx = anim_x + 60
            anvil_cy = anim_y + len(frame_lines) * 15 - 20
            radius = int((1.0 - self._shockwave_r) * 60)
            alpha  = int(self._shockwave_r * 200)
            shock_surf = pygame.Surface((sw, sh), pygame.SRCALPHA)
            pygame.draw.circle(shock_surf, (255, 220, 80, alpha),
                               (anvil_cx, anvil_cy), radius, 2)
            surface.blit(shock_surf, (0, 0))

        # ── Round counter ─────────────────────────────────────────────────────
        round_y = py + 180
        round_text = f"Round  {min(self._current_round + 1, self._total_rounds)} / {self._total_rounds}"
        render_label(surface, round_text, px + pw // 2, round_y,
                     color=(180, 180, 220))

        # ── Key sequence display ──────────────────────────────────────────────
        if self.running and self._current_round < self._total_rounds:
            seq     = self._sequences[self._current_round]
            seq_y   = round_y + 28
            n       = len(seq)
            tile_w  = 48
            spacing = 12
            total_w = n * tile_w + (n - 1) * spacing
            start_x = px + pw // 2 - total_w // 2

            for idx, key_char in enumerate(seq):
                tx = start_x + idx * (tile_w + spacing)
                ty = seq_y

                if idx < self._current_seq_progress:
                    # Already pressed — dim green with checkmark glow
                    tile_col   = (40, 120, 40)
                    border_col = (100, 220, 100)
                    text_col   = (150, 255, 150)
                    glow_col   = (80, 200, 80, 60)
                elif idx == self._current_seq_progress:
                    # Current key — bright pulsing
                    pulse = abs(math.sin(pygame.time.get_ticks() * 0.008))
                    tile_col   = (40 + int(30 * pulse), 40 + int(40 * pulse), 120 + int(40 * pulse))
                    border_col = (180 + int(75 * pulse), 180 + int(75 * pulse), 255)
                    text_col   = (255, 255, 100 + int(155 * pulse))
                    glow_col   = None
                else:
                    # Future keys — dark
                    tile_col   = (30, 30, 50)
                    border_col = (80, 80, 100)
                    text_col   = (120, 120, 140)
                    glow_col   = None

                # Draw glow effect for completed keys
                if glow_col:
                    glow_surf = pygame.Surface((tile_w + 6, tile_w + 6), pygame.SRCALPHA)
                    pygame.draw.rect(glow_surf, glow_col, (0, 0, tile_w + 6, tile_w + 6), border_radius=5)
                    surface.blit(glow_surf, (tx - 3, ty - 3))

                pygame.draw.rect(surface, tile_col,
                                 (tx, ty, tile_w, tile_w), border_radius=5)
                pygame.draw.rect(surface, border_col,
                                 (tx, ty, tile_w, tile_w), 2, border_radius=5)
                key_surf = self._title_font.render(key_char, True, text_col)
                surface.blit(key_surf,
                             (tx + tile_w // 2 - key_surf.get_width() // 2,
                              ty + tile_w // 2 - key_surf.get_height() // 2))

            # Instruction
            inst_y = seq_y + tile_w + 12
            if self._wrong_flash > 0:
                inst_text  = "❌ Wrong key! Reset sequence. Try again..."
                inst_color = (255, 100, 100)
            elif self._current_seq_progress > 0:
                progress = min(len(seq), self._current_seq_progress)
                inst_text  = f"✓ {progress}/{len(seq)} keys correct — Keep going!"
                inst_color = (150, 220, 150)
            else:
                inst_text  = "Press keys in order: W / A / S / D"
                inst_color = (140, 140, 200)
            render_label(surface, inst_text, px + pw // 2, inst_y,
                         color=inst_color)

        # ── Perfect round indicators ──────────────────────────────────────────
        ind_y = py + ph - 80
        ind_x_start = px + pw // 2 - (self._total_rounds * 22) // 2
        for i in range(self._total_rounds):
            ix = ind_x_start + i * 22
            if i < self._current_round:
                seq_was_perfect = (i < self._perfect_rounds)
                col = (80, 220, 80) if seq_was_perfect else (200, 120, 60)
            else:
                col = (60, 60, 80)
            pygame.draw.circle(surface, col, (ix + 8, ind_y + 8), 7)
            pygame.draw.circle(surface, (150, 150, 150), (ix + 8, ind_y + 8), 7, 1)

        # Legend
        render_label(surface,
                     "Green = perfect round   Orange = mistakes made",
                     px + pw // 2, ind_y + 20,
                     color=(120, 120, 120), small=True)

        # ── Result overlay ────────────────────────────────────────────────────
        if self._show_result:
            alpha = min(255, int(self._result_timer * 255))
            overlay_surf = pygame.Surface((pw, 60), pygame.SRCALPHA)
            overlay_surf.fill((0, 0, 0, 160))
            surface.blit(overlay_surf, (px, py + ph // 2 - 30))
            render_title(surface, self._result_text,
                         px + pw // 2, py + ph // 2 - 14,
                         color=self._result_color)

    def _ensure_fonts(self):
        if self._font is None:
            import pygame
            pygame.font.init()
            self._font       = pygame.font.SysFont("Courier New", 14)
            self._small_font = pygame.font.SysFont("Courier New", 11)
            self._title_font = pygame.font.SysFont("Courier New", 18, bold=True)
        # Patch module-level fonts too
        _ensure_fonts()
