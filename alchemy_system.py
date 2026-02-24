"""
alchemy_system.py  —  Alchemy / Brewing System & Animated Minigame
====================================================================
A new brewing system with:
  • New compound potions and transmutation recipes
  • Animated cauldron with bubbles / steam
  • Heat-gauge minigame: press SPACE when heat enters the reaction zone

Minigame rules:
  • A heat bar rises continuously from 0 → 1
  • A reaction zone (green) is randomly placed at 0.55 – 0.80 heat
  • A danger zone (red) starts at 0.85
  • Player presses SPACE to "complete the brew"
  • perfect  (green zone) → Potent variant  (+50 % effect)
  • ok       (near zone)  → normal variant
  • burned   (red zone)   → Burnt Brew  (sells for 1 gold, no effect)
  • cold     (below zone) → Weak variant  (–30 % effect)

Commands added to engine.py:
  brew            — show alchemy recipes at current station
  brew <recipe>   — start brewing (opens overlay if GUI present)
"""

import random
import math

try:
    from ascii_art import (
        ANIMATION_FRAMES, render_ascii_block, render_title, render_label,
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
#  ALCHEMY RECIPE DATABASE
# ──────────────────────────────────────────────────────────────────────────────
# Produces "potent_X" or "weak_X" variants stored in a quality field.
# result_id is the base item_id; quality prefix is applied afterward.

ALCHEMY_RECIPES = {
    # ── Standard Potions (improved versions) ─────────────────────────────────
    "brew_healing": {
        "name":        "Healing Draught",
        "ingredients": {"mushroom": 2, "mineral_water_flask": 1},
        "result":      "healing_potion",
        "station":     "campfire",
        "description": "A classic restorative. Heat must be controlled.",
        "temp_label":  "Simmering",
    },
    "brew_greater_healing": {
        "name":        "Greater Healing Draught",
        "ingredients": {"giant_truffle": 1, "mineral_water_flask": 2, "honey": 1},
        "result":      "greater_healing_potion",
        "station":     "campfire",
        "description": "A concentrated healing brew demanding precise temperature control.",
        "temp_label":  "Rolling Boil",
    },
    "brew_mana": {
        "name":        "Mana Infusion",
        "ingredients": {"luminous_cap": 2, "mineral_water_flask": 1},
        "result":      "mana_potion",
        "station":     "campfire",
        "description": "Crystalline mushrooms dissolved in pure water.",
        "temp_label":  "Gentle Heat",
    },
    "brew_strength": {
        "name":        "Strength Elixir",
        "ingredients": {"strange_herb": 2, "iron_ore": 1},
        "result":      "strength_potion",
        "station":     "campfire",
        "description": "Forge-cold iron shavings catalyse the brew.",
        "temp_label":  "Medium Heat",
    },
    # ── New Compound Potions ──────────────────────────────────────────────────
    "brew_transmutation_oil": {
        "name":        "Transmutation Oil",
        "ingredients": {"cave_crystal": 1, "gold_dust": 2, "mineral_water_flask": 1},
        "result":      "transmutation_oil",
        "station":     "campfire",
        "description": "Alchemical oil used to refine raw ores into higher grades.",
        "temp_label":  "Crystal Catalyst",
    },
    "brew_elixir_of_visions": {
        "name":        "Elixir of Visions",
        "ingredients": {"luminous_cap": 1, "cave_crystal": 1, "strange_herb": 1},
        "result":      "elixir_of_visions",
        "station":     "campfire",
        "description": "Reveals hidden traps and secret passages for 10 moves.",
        "temp_label":  "Mystic Simmer",
    },
    "brew_mutagenic_brew": {
        "name":        "Mutagenic Brew",
        "ingredients": {"shadow_essence": 1, "mushroom": 3, "strange_herb": 2},
        "result":      "mutagenic_brew",
        "station":     "campfire",
        "description": "A volatile brew that temporarily boosts all stats but risks backlash.",
        "temp_label":  "Volatile Heat",
    },
    "brew_philosophers_draught": {
        "name":        "Philosopher's Draught",
        "ingredients": {
            "cave_crystal": 2, "gold_dust": 1, "luminous_cap": 2, "strange_herb": 1
        },
        "result":      "philosophers_draught",
        "station":     "campfire",
        "description": "Legendary draught. Permanently boosts a random stat by 1.",
        "temp_label":  "Perfect Equilibrium",
    },
    "brew_antidote_compound": {
        "name":        "Compound Antidote",
        "ingredients": {"strange_herb": 3, "mineral_water_flask": 1},
        "result":      "antidote",
        "station":     "campfire",
        "description": "Neutralises all poison types in a single dose.",
        "temp_label":  "Gentle Infusion",
    },
    "brew_shadow_tonic": {
        "name":        "Shadow Tonic",
        "ingredients": {"shadow_essence": 2, "mineral_water_flask": 1},
        "result":      "shadow_tonic",
        "station":     "campfire",
        "description": "Heightens dexterity and stealth for 5 moves.",
        "temp_label":  "Dark Boil",
    },
}

# Potent variants: item_id → enhanced effect description
POTENT_EFFECTS = {
    "healing_potion":        "Restore 50% more HP.",
    "greater_healing_potion":"Restore full HP.",
    "mana_potion":           "Restore 50% more MP.",
    "strength_potion":       "+50% attack bonus duration.",
    "transmutation_oil":     "Refines 2 ore at once.",
    "elixir_of_visions":     "Lasts 20 moves instead of 10.",
    "mutagenic_brew":        "Stronger stat boost, reduced backlash.",
    "philosophers_draught":  "Boosts 2 random stats instead of 1.",
    "antidote":              "Also removes curses.",
    "shadow_tonic":          "+10 moves duration, +stealth.",
}

# Item effect overrides for new potions (used by item_effects.py)
NEW_ITEM_EFFECTS = {
    "transmutation_oil": {
        "description":  "Transmutation Oil",
        "use_text":     "You apply the oil to a raw ore, refining its quality.",
        "refine_ore":   True,
    },
    "elixir_of_visions": {
        "description":  "Elixir of Visions",
        "use_text":     "Your sight sharpens — hidden dangers reveal themselves.",
        "reveal_traps": 10,
    },
    "mutagenic_brew": {
        "description":  "Mutagenic Brew",
        "use_text":     "Your body surges! Chaos flows through your veins.",
        "mutagen":      True,
        "duration":     5,
    },
    "philosophers_draught": {
        "description":  "Philosopher's Draught",
        "use_text":     "Ancient wisdom seeps into your bones.",
        "perm_stat_up": 1,
    },
    "shadow_tonic": {
        "description":  "Shadow Tonic",
        "use_text":     "You fade into the shadows...",
        "dexterity_boost": 5,
        "duration": 5,
    },
}

# Quality multipliers for heat zone outcomes
BREW_QUALITY = {
    "potent": {"label": "Potent",   "prefix": "potent_",   "effect_mult": 1.5,  "color": (100, 255, 100)},
    "normal": {"label": "Normal",   "prefix": "",           "effect_mult": 1.0,  "color": (200, 200, 200)},
    "weak":   {"label": "Weak",     "prefix": "weak_",      "effect_mult": 0.7,  "color": (200, 200, 100)},
    "burnt":  {"label": "Burnt",    "prefix": "burnt_",     "effect_mult": 0.0,  "color": (255, 80,  80)},
}

# Heat rate: how fast the gauge fills (fraction per second)
HEAT_RATE = 0.18


# ──────────────────────────────────────────────────────────────────────────────
#  ALCHEMY SYSTEM LOGIC
# ──────────────────────────────────────────────────────────────────────────────

class AlchemySystem:
    """Manages alchemy/brewing state and effects."""

    def __init__(self, engine):
        self.engine = engine
        self.pending_brew = None

    # ── Public API ────────────────────────────────────────────────────────────

    def show_brew_menu(self) -> str:
        """Return the text menu of available alchemy recipes."""
        inv = self.engine.player.inventory
        lines = [
            "\n" + "═" * 55,
            "  ⚗️  ALCHEMY MENU",
            "═" * 55,
            "  Type: brew <recipe_name>  to start brewing.",
            "  Requires a campfire or cauldron.\n",
        ]

        available = []
        unavailable = []

        for rid, recipe in ALCHEMY_RECIPES.items():
            can_brew = all(inv.get(k, 0) >= v
                           for k, v in recipe["ingredients"].items())
            ing = ", ".join(f"{v}x {k.replace('_',' ')}"
                            for k, v in recipe["ingredients"].items())
            entry = f"  {rid:<32s}  [{ing}]"
            if can_brew:
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

    def start_brew(self, recipe_id: str) -> str:
        """Validate materials and open the alchemy overlay."""
        recipe_id = recipe_id.replace(" ", "_").lower()
        # Strip "brew_" prefix if user types just the potion name
        if recipe_id not in ALCHEMY_RECIPES:
            full_id = "brew_" + recipe_id
            if full_id in ALCHEMY_RECIPES:
                recipe_id = full_id

        if recipe_id not in ALCHEMY_RECIPES:
            candidates = [r for r in ALCHEMY_RECIPES if recipe_id in r]
            if len(candidates) == 1:
                recipe_id = candidates[0]
            elif candidates:
                return "Ambiguous recipe. Did you mean: " + ", ".join(candidates) + "?"
            else:
                return (f"  Unknown recipe: '{recipe_id}'.\n"
                        f"  Type 'brew' to see available recipes.")

        recipe = ALCHEMY_RECIPES[recipe_id]

        # Check campfire presence (any room with campfire in name or station type)
        room = self.engine.get_room_data(self.engine.player.current_room)
        station = getattr(room, "crafting_station", None)
        if isinstance(room, dict):
            station = room.get("crafting_station")
        room_name = self.engine.player.current_room.lower()
        if station != "campfire" and "campfire" not in room_name and "camp" not in room_name:
            return ("You need a campfire or cauldron to brew potions.\n"
                    "Try resting at a campsite.")

        # Materials check
        inv = self.engine.player.inventory
        missing = [(k, v - inv.get(k, 0))
                   for k, v in recipe["ingredients"].items()
                   if inv.get(k, 0) < v]
        if missing:
            lines = ["  You don't have the required ingredients:"]
            for name, deficit in missing:
                lines.append(f"    • {name.replace('_',' ')}: need {deficit} more")
            return "\n".join(lines)

        self.pending_brew = {"recipe_id": recipe_id, "recipe": recipe}

        gui = getattr(self.engine, "gui", None)
        if gui is not None:
            overlay = AlchemyOverlay(self, recipe)
            gui._alchemy_overlay = overlay
            return ""

        # Fallback: auto-brew at normal quality
        return self._apply_brew(recipe, quality="normal")

    def _apply_brew(self, recipe: dict, quality: str = "normal") -> str:
        """Deduct ingredients and add brewed potion to inventory."""
        inv = self.engine.player.inventory
        for k, v in recipe["ingredients"].items():
            inv[k] = inv.get(k, 0) - v
            if inv[k] <= 0:
                del inv[k]

        base_id = recipe["result"]
        tier = BREW_QUALITY[quality]

        if quality == "burnt":
            result_id = "burnt_brew"
        elif quality == "potent":
            result_id = f"potent_{base_id}"
        elif quality == "weak":
            result_id = f"weak_{base_id}"
        else:
            result_id = base_id

        self.engine.player.inventory[result_id] = (
            self.engine.player.inventory.get(result_id, 0) + 1
        )
        self.engine._inventory_changed = True
        self.pending_brew = None

        # Award XP
        xp_map = {"potent": 50, "normal": 25, "weak": 10, "burnt": 5}
        try:
            from progression_system import award_xp
            award_xp(self.engine.player, xp_map.get(quality, 25), "alchemy")
        except Exception:
            pass

        label = tier["label"]
        lines = [
            "\n" + "═" * 50,
            f"  ⚗️ Brewing complete!",
            f"  You brewed: {label} {recipe['name']}",
        ]
        if quality == "potent":
            potent_desc = POTENT_EFFECTS.get(base_id, "Enhanced effect!")
            lines.append(f"  ✨ Potent! {potent_desc}")
        elif quality == "burnt":
            lines.append("  💀 The brew burned! A worthless Burnt Brew remains.")
        elif quality == "weak":
            lines.append("  ⚠️  Brewed too cold. Weak variant — reduced effect.")
        lines.append("═" * 50)
        return "\n".join(lines)

    def to_dict(self) -> dict:
        return {}

    def load_from_dict(self, data: dict):
        pass


# ──────────────────────────────────────────────────────────────────────────────
#  ALCHEMY OVERLAY (Pygame animated minigame)
# ──────────────────────────────────────────────────────────────────────────────

class AlchemyOverlay:
    """
    Heat-gauge brewing minigame.

    Left side : animated cauldron with rising bubbles / steam (ASCII frames).
    Right side : vertical heat bar with labelled zones:
                   COLD → WARM → REACTION ZONE (green) → DANGER (red)
    Player presses SPACE when heat is in the green reaction zone.
    """

    PANEL_W = 540
    PANEL_H = 400
    ANIM_FPS = 4    # Base timer: brewing is a slow watchful game — plenty of time to observe
    # the heat bar, but can't ignore it forever.
    BASE_TIMER = 40.0
    def __init__(self, system: AlchemySystem, recipe: dict):
        self.system  = system
        self.recipe  = recipe
        self.done    = False
        self.running = True

        # ── Difficulty scaling ─────────────────────────────────────────────
        ingredients = recipe.get("ingredients", recipe.get("materials", {}))
        recipe_tier = infer_recipe_tier(ingredients)
        dp = get_diff_params(recipe_tier)
        # baseline HEAT_RATE 0.10 (slower than original 0.18) × heat_rate_mult
        self._heat_rate = 0.10 * dp["heat_rate_mult"]
        self._result_secs = 3.0 + max(0.0, dp["result_secs"])

        # Countdown timer
        self._timer_max  = max(8.0, self.BASE_TIMER * dp["timer_mult"])
        self._time_left  = self._timer_max

        # Heat bar state
        self._heat        = 0.0       # 0.0 – 1.0
        self._react_lo    = random.uniform(0.52, 0.65)
        # Zone narrows on hard (zone_mult < 1) wider on easy (zone_mult > 1)
        self._react_hi    = self._react_lo + 0.20 * dp["zone_mult"]
        self._danger_lo   = 0.85

        # Cauldron animation
        self._anim_frame  = 0
        self._anim_timer  = 0.0
        try:
            self._frames = ANIMATION_FRAMES.get("alchemy_brew", [])
        except Exception:
            self._frames = []

        # Flash indicators
        self._result_flash  = 0.0
        self._result_text   = ""
        self._result_color  = (220, 220, 220)
        self._show_result   = False
        self._result_timer  = 0.0

        self._font     = None

    # ── Events ───────────────────────────────────────────────────────────────

    def handle_event(self, event):
        import pygame
        if self.done or self._show_result:
            return
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                self._complete_brew()

    def _complete_brew(self):
        self.running = False
        h = self._heat

        if h >= self._danger_lo:
            quality = "burnt"
        elif self._react_lo <= h <= self._react_hi:
            quality = "potent"
        elif h >= self._react_lo - 0.08:
            quality = "normal"
        else:
            quality = "weak"

        result = self.system._apply_brew(self.recipe, quality=quality)
        tier = BREW_QUALITY[quality]
        self._result_text  = tier["label"]
        self._result_color = tier["color"]
        self._show_result  = True
        self._result_timer = 0.0

        gui = getattr(self.system.engine, "gui", None)
        if gui and result:
            gui.append(result)

    # ── Update ────────────────────────────────────────────────────────────────

    def update(self, dt):
        if self.done:
            return

        if self.running:
            self._heat = min(1.0, self._heat + self._heat_rate * dt)
            # Auto-trigger at danger overflow
            if self._heat >= 1.0 and not self._show_result:
                self._complete_brew()
            # Countdown timer — brew at current heat when time runs out
            if not self._show_result:
                self._time_left -= dt
                if self._time_left <= 0:
                    self._time_left = 0.0
                    self._complete_brew()

        # Cauldron animation
        self._anim_timer += dt
        dur = 1.0 / max(self.ANIM_FPS, 1)
        while self._anim_timer >= dur:
            self._anim_timer -= dur
            if self._frames:
                self._anim_frame = (self._anim_frame + 1) % len(self._frames)

        # Result timer
        if self._show_result:
            self._result_timer += dt
            if self._result_timer >= self._result_secs:
                self.done = True

    # ── Render ────────────────────────────────────────────────────────────────

    def render(self, surface):
        import pygame
        self._ensure_fonts()

        sw, sh = surface.get_size()
        pw, ph = self.PANEL_W, self.PANEL_H
        px = (sw - pw) // 2
        py = (sh - ph) // 2

        draw_dim_overlay(surface, 150)
        draw_panel(surface, (px, py, pw, ph),
                   title=f"BREWING: {self.recipe['name'].upper()}")

        # Countdown timer bar
        if not self._show_result:
            draw_timer_bar(surface, px, py, pw, self._time_left, self._timer_max)

        # ── Cauldron ASCII animation (left half) ──────────────────────────────
        frame_lines = self._frames[self._anim_frame % len(self._frames)] if self._frames else []
        art_x = px + 30
        art_y = py + 55
        render_ascii_block(surface, frame_lines, art_x, art_y,
                           color=(200, 200, 200), line_height=16)

        # ── Vertical heat bar (right half) ────────────────────────────────────
        bar_x   = px + pw - 90
        bar_y   = py + 55
        bar_w   = 32
        bar_h   = ph - 130

        # Background
        pygame.draw.rect(surface, (30, 30, 50),  (bar_x, bar_y, bar_w, bar_h))
        pygame.draw.rect(surface, (80, 80, 120), (bar_x, bar_y, bar_w, bar_h), 1)

        # Cold zone (blue)
        cold_h = int(self._react_lo * bar_h)
        pygame.draw.rect(surface, (40, 60, 120),
                         (bar_x, bar_y + bar_h - cold_h, bar_w, cold_h))

        # Reaction zone (green)
        react_y0 = int((1.0 - self._react_hi) * bar_h)
        react_y1 = int((1.0 - self._react_lo) * bar_h)
        pygame.draw.rect(surface, (30, 120, 50),
                         (bar_x, bar_y + react_y0, bar_w, react_y1 - react_y0))

        # Danger zone (red)
        danger_h = int((1.0 - self._danger_lo) * bar_h)
        pygame.draw.rect(surface, (160, 30, 30),
                         (bar_x, bar_y, bar_w, danger_h))

        # Heat fill — bright fill rising from bottom
        fill_h   = int(self._heat * bar_h)
        fill_r   = int(40 + self._heat * 200)
        fill_g   = int(180 - self._heat * 160)
        fill_b   = int(220 - self._heat * 200)
        pygame.draw.rect(surface, (fill_r, fill_g, max(0, fill_b)),
                         (bar_x + 2, bar_y + bar_h - fill_h + 2,
                          bar_w - 4, fill_h - 2))

        # Pulsing border when in reaction zone
        if self._react_lo <= self._heat <= self._react_hi:
            pulse = abs(math.sin(pygame.time.get_ticks() * 0.006))
            alpha = int(100 + pulse * 155)
            glow = pygame.Surface((bar_w + 6, bar_h + 6), pygame.SRCALPHA)
            pygame.draw.rect(glow, (0, 255, 0, alpha),
                             (0, 0, bar_w + 6, bar_h + 6), 3, border_radius=4)
            surface.blit(glow, (bar_x - 3, bar_y - 3))

        # Labels
        label_x = bar_x + bar_w + 8
        render_label(surface, "HOT",  label_x + 18, bar_y + 4,
                     color=(255, 80, 80), small=True)
        render_label(surface, "BREW", label_x + 18,
                     bar_y + react_y0 + (react_y1 - react_y0) // 2 - 6,
                     color=(100, 255, 100), small=True)
        render_label(surface, "COLD", label_x + 18, bar_y + bar_h - 14,
                     color=(100, 150, 255), small=True)

        # "SPACE to brew" instruction
        inst_y = py + ph - 50
        if self.running:
            render_label(surface, "[SPACE]  to complete the brew",
                         px + pw // 2, inst_y, color=(170, 170, 220))

        # Temperature stage label
        if self._heat < self._react_lo - 0.08:
            stage, scol = "Cold", (100, 150, 255)
        elif self._heat < self._react_lo:
            stage, scol = "Almost ready...", (200, 200, 100)
        elif self._heat <= self._react_hi:
            stage, scol = "REACTION ZONE! Press SPACE!", (100, 255, 100)
        elif self._heat < self._danger_lo:
            stage, scol = "Getting too hot!", (255, 180, 50)
        else:
            stage, scol = "BURNING! SPACE NOW!", (255, 50, 50)

        render_label(surface, stage, px + pw // 2, inst_y - 22, color=scol)

        # ── Result overlay ────────────────────────────────────────────────────
        if self._show_result:
            render_title(surface, self._result_text,
                         px + pw // 2, py + ph // 2 - 12,
                         color=self._result_color)

    def _ensure_fonts(self):
        if self._font is None:
            import pygame
            pygame.font.init()
            self._font = pygame.font.SysFont("Courier New", 14)
        _ensure_fonts()
