"""
ritual_system.py  —  Altar Ritual System & Memory Puzzle Minigame
==================================================================
Activate rituals at the various altars to unlock temporary altar
blessings or special recipe unlocks.

Minigame: Simon Says memory puzzle.
  • A 3×3 grid of 9 runic symbols is displayed.
  • During the "show" phase each correct symbol briefly lights up
    in the secret order (1–N flashes, each for 0.6 s).
  • During the "input" phase the player presses number keys 1–9
    matching the symbols in the shown order.
  • Wrong input: one life lost (2 lives total per ritual).
  • Perfect (no mistakes): full blessing duration.
  • Partial (1 mistake): halved duration.
  • 2 mistakes: ritual fails, materials consumed.

Commands added to engine.py:
  ritual           — list available rituals at current altar
  ritual <id>      — start ritual
"""

import random
import math

try:
    from ascii_art import (
        ANIMATION_FRAMES, RUNES, render_ascii_block, render_title,
        render_label, draw_dim_overlay, draw_panel, draw_timer_bar, _ensure_fonts,
        get_diff_params, infer_recipe_tier,
    )
    ASCII_ART_AVAILABLE = True
except ImportError:
    ASCII_ART_AVAILABLE = False
    RUNES = {}
    def get_diff_params(tier=2):
        return {"bar_speed_mult":1.0,"zone_mult":1.0,"heat_rate_mult":1.0,
                "flash_mult":1.0,"seq_delta":0,"result_secs":0.0,"timer_mult":1.0}
    def infer_recipe_tier(ing): return 2
    def draw_timer_bar(*a, **k): pass

# ──────────────────────────────────────────────────────────────────────────────
#  RITUAL DATABASE
# ──────────────────────────────────────────────────────────────────────────────
# materials      — consumed on attempt (even on fail)
# blessing       — effect granted on success
# altar          — altar station type required
# sequence_len   — number of symbols in the memory sequence (difficulty)

RITUAL_DATABASE = {
    # ── Crystal Altar ─────────────────────────────────────────────────────────
    "ritual_crystal_clarity": {
        "name":         "Rite of Clarity",
        "altar":        "altar_crystal",
        "description":  "The forge of light blesses you with heightened perception for 10 moves.",
        "materials":    {"cave_crystal": 2},
        "blessing":     {"perception": 3, "duration": 10},
        "sequence_len": 3,
    },
    "ritual_prismatic_ward": {
        "name":         "Prismatic Ward",
        "altar":        "altar_crystal",
        "description":  "Crystal light weaves into a ward, reducing next 3 damage instances.",
        "materials":    {"cave_crystal": 3, "gold_dust": 1},
        "blessing":     {"damage_ward": 3, "duration": 3},
        "sequence_len": 4,
    },
    # ── Shadow Altar ──────────────────────────────────────────────────────────
    "ritual_shadow_step": {
        "name":         "Shadow Step",
        "altar":        "altar_shadow",
        "description":  "The shadows embrace you — greatly boosted dexterity for 8 moves.",
        "materials":    {"shadow_essence": 2},
        "blessing":     {"dexterity": 5, "duration": 8},
        "sequence_len": 3,
    },
    "ritual_void_shroud": {
        "name":         "Void Shroud",
        "altar":        "altar_shadow",
        "description":  "The void wraps around you — +4 DEF and DEX for 6 moves.",
        "materials":    {"shadow_essence": 3, "bone_fragment": 1},
        "blessing":     {"defense": 4, "dexterity": 4, "duration": 6},
        "sequence_len": 5,
    },
    # ── Iron Altar ────────────────────────────────────────────────────────────
    "ritual_ironheart": {
        "name":         "Ironheart Rite",
        "altar":        "altar_iron",
        "description":  "The ancient forge-spirit surges: +6 CON for 8 moves.",
        "materials":    {"iron_ingot": 2},
        "blessing":     {"constitution": 6, "duration": 8},
        "sequence_len": 3,
    },
    "ritual_mountains_fury": {
        "name":         "Mountain's Fury",
        "altar":        "altar_iron",
        "description":  "Dwarven wrath channels into your weapon — +7 STR for 5 moves.",
        "materials":    {"iron_ingot": 3, "mithril_ore": 1},
        "blessing":     {"strength": 7, "duration": 5},
        "sequence_len": 5,
    },
    # ── Catacomb Altar ────────────────────────────────────────────────────────
    "ritual_soul_ward": {
        "name":         "Soul Ward",
        "altar":        "altar_catacomb",
        "description":  "The souls of the fallen protect you — +6 DEF for 6 moves.",
        "materials":    {"bone_fragment": 3},
        "blessing":     {"defense": 6, "duration": 6},
        "sequence_len": 4,
    },
    "ritual_lich_pact": {
        "name":         "Pact of the Lich",
        "altar":        "altar_catacomb",
        "description":  "At terrible cost — resurrect at 50 HP if you die within 8 moves.",
        "materials":    {"bone_fragment": 5, "shadow_essence": 2},
        "blessing":     {"auto_revive": True, "revive_hp": 50, "duration": 8},
        "sequence_len": 6,
    },
}

# Rune symbol keys for the grid (9 symbols)
GRID_SYMBOLS = ["fire", "frost", "void", "iron", "shadow",
                "crystal", "soul", "nature", "fire"]

# Compact single-char representations for each symbol (for ASCII grid)
SYMBOL_CHARS = {
    "fire":    "^",
    "frost":   "*",
    "void":    "o",
    "iron":    "#",
    "shadow":  "~",
    "crystal": "+",
    "soul":    "†",
    "nature":  "Y",
}


# ──────────────────────────────────────────────────────────────────────────────
#  RITUAL SYSTEM LOGIC
# ──────────────────────────────────────────────────────────────────────────────

class RitualSystem:
    """Manages altar rituals and applies blessings."""

    def __init__(self, engine):
        self.engine = engine

    # ── Public API ────────────────────────────────────────────────────────────

    def show_ritual_menu(self) -> str:
        """List available rituals for the current altar."""
        room    = self.engine.get_room_data(self.engine.player.current_room)
        station = getattr(room, "crafting_station", None)
        if isinstance(room, dict):
            station = room.get("crafting_station")

        relevant = {rid: r for rid, r in RITUAL_DATABASE.items()
                    if r.get("altar") == station}

        if not relevant:
            return ("No rituals are available here.\n"
                    "Seek an altar: Crystal, Shadow, Iron, or Catacomb.")

        altar_names = {
            "altar_crystal":  "Forge of Light",
            "altar_shadow":   "The Shadowforge",
            "altar_iron":     "Dwarven Eternal Anvil",
            "altar_catacomb": "Catacomb Soul Altar",
        }
        altar_label = altar_names.get(station, station)

        inv   = self.engine.player.inventory
        lines = [
            "\n" + "═" * 55,
            f"  ✦  RITUALS — {altar_label}",
            "═" * 55,
            "  Type: ritual <ritual_id>  to begin.\n",
        ]
        for rid, r in relevant.items():
            can_do = all(inv.get(k, 0) >= v for k, v in r["materials"].items())
            mats   = ", ".join(f"{v}x {k.replace('_',' ')}" for k, v in r["materials"].items())
            marker = "  ✓" if can_do else "  ✗"
            lines.append(f"{marker} {rid}")
            lines.append(f"    {r['name']} — {r['description']}")
            lines.append(f"    Cost: {mats}   Sequence: {r['sequence_len']} symbols")
            lines.append("")

        lines.append("═" * 55)
        return "\n".join(lines)

    def start_ritual(self, ritual_id: str) -> str:
        """Validate and start a ritual, opening the overlay."""
        ritual_id = ritual_id.replace(" ", "_").lower()
        if ritual_id not in RITUAL_DATABASE:
            candidates = [r for r in RITUAL_DATABASE if ritual_id in r]
            if len(candidates) == 1:
                ritual_id = candidates[0]
            elif candidates:
                return "Ambiguous ritual. Did you mean: " + ", ".join(candidates) + "?"
            else:
                return f"Unknown ritual '{ritual_id}'. Type 'ritual' to list available ones."

        ritual = RITUAL_DATABASE[ritual_id]

        # Station check
        room    = self.engine.get_room_data(self.engine.player.current_room)
        station = getattr(room, "crafting_station", None)
        if isinstance(room, dict):
            station = room.get("crafting_station")
        if station != ritual["altar"]:
            altar_names = {
                "altar_crystal":  "Forge of Light",
                "altar_shadow":   "The Shadowforge",
                "altar_iron":     "Dwarven Eternal Anvil",
                "altar_catacomb": "Catacomb Soul Altar",
            }
            needed = altar_names.get(ritual["altar"], ritual["altar"])
            return f"This ritual requires the {needed}."

        # Materials check
        inv     = self.engine.player.inventory
        missing = [(k, v - inv.get(k, 0))
                   for k, v in ritual["materials"].items()
                   if inv.get(k, 0) < v]
        if missing:
            lines = ["  You lack the required offerings:"]
            for name, deficit in missing:
                lines.append(f"    • {name.replace('_',' ')}: need {deficit} more")
            return "\n".join(lines)

        # Consume materials immediately (fail still costs them)
        for k, v in ritual["materials"].items():
            inv[k] = inv.get(k, 0) - v
            if inv[k] <= 0:
                del inv[k]
        self.engine._inventory_changed = True

        gui = getattr(self.engine, "gui", None)
        if gui is not None:
            overlay = RitualOverlay(self, ritual_id, ritual)
            gui._ritual_overlay = overlay
            return ""

        # Fallback: auto-succeed at full blessing
        return self._apply_blessing(ritual, mistakes=0)

    def _apply_blessing(self, ritual: dict, mistakes: int) -> str:
        """Apply the ritual blessing to the player."""
        if mistakes >= 2:
            return (
                "\n  ✗ The ritual failed — the spirits are displeased.\n"
                "    Your offerings were consumed.\n"
            )

        blessing = ritual["blessing"].copy()
        duration = blessing.get("duration", 5)
        if mistakes == 1:
            duration = max(1, duration // 2)
            blessing["duration"] = duration

        # Apply to active effects
        active = self.engine.player.state.setdefault("active_effects", {})
        name   = ritual["name"]

        if blessing.get("auto_revive"):
            active["auto_revive"] = {
                "revive_hp": blessing["revive_hp"],
                "duration":  duration,
            }
        else:
            for stat in ("strength", "defense", "dexterity",
                         "perception", "constitution"):
                amt = blessing.get(stat, 0)
                if amt:
                    # Temporary buff via temp_buffs list
                    self.engine.player.state.setdefault("temp_buffs", []).append({
                        "stat":       stat,
                        "amount":     amt,
                        "turns_left": duration,
                    })
                    old = self.engine.player.stats.get(stat, 0)
                    self.engine.player.stats[stat] = old + amt

            if blessing.get("damage_ward"):
                active["damage_ward"] = {
                    "charges":  blessing["damage_ward"],
                    "duration": duration,
                }

        # XP
        try:
            from progression_system import award_xp
            award_xp(self.engine.player, 80 if mistakes == 0 else 40, "ritual")
        except Exception:
            pass

        quality = "perfectly" if mistakes == 0 else "partially"
        lines = [
            "\n" + "═" * 50,
            f"  ✦  {name}",
            f"  Ritual completed {quality}!",
        ]
        if mistakes == 1:
            lines.append(f"  ⚠️  One mistake — blessing lasts {duration} moves (halved).")
        else:
            lines.append(f"  ✨ Blessing active for {duration} moves!")

        for stat in ("strength", "defense", "dexterity", "perception", "constitution"):
            if blessing.get(stat):
                lines.append(f"  +{blessing[stat]} {stat.upper()}")
        if blessing.get("damage_ward"):
            lines.append(f"  Next {blessing['damage_ward']} damage instances reduced.")
        if blessing.get("auto_revive"):
            lines.append(f"  Auto-revive at {blessing['revive_hp']} HP once.")
        lines.append("═" * 50)
        return "\n".join(lines)

    def to_dict(self) -> dict:
        return {}

    def load_from_dict(self, data: dict):
        pass


# ──────────────────────────────────────────────────────────────────────────────
#  RITUAL OVERLAY (Pygame memory-puzzle minigame)
# ──────────────────────────────────────────────────────────────────────────────

class RitualOverlay:
    """
    Simon Says ritual minigame.

    Phase 1 (SHOW):   symbols highlight one by one to reveal sequence.
    Phase 2 (INPUT):  player presses 1–9 number keys to replicate sequence.
    Phase 3 (RESULT): show success/fail and apply blessing.
    """

    PANEL_W   = 520
    PANEL_H   = 460
    CELL_SIZE = 80
    GRID_COLS = 3
    GRID_ROWS = 3
    # Base timer for the INPUT phase only (show phase is free, no pressure).
    # Needs to be long enough to enter the full sequence after memorising it.
    BASE_TIMER = 40.0  # increased for longer phases

    # Show-phase timing (class defaults; per-instance values set in __init__)
    FLASH_ON  = 0.60   # seconds a symbol shines  (was 0.85, now faster)
    FLASH_OFF = 0.15   # gap between flashes      (was 0.30, now faster)

    def __init__(self, system: RitualSystem, ritual_id: str, ritual: dict):
        self.system     = system
        self.ritual_id  = ritual_id
        self.ritual     = ritual
        self.done       = False

        # ── Difficulty scaling ─────────────────────────────────────────────
        materials = ritual.get("materials", {})
        recipe_tier = infer_recipe_tier(materials)
        dp = get_diff_params(recipe_tier)
        # Per-instance flash timing: baseline 0.60 on / 0.15 off, scaled by flash_mult
        self._flash_on  = 0.60 * dp["flash_mult"]
        self._flash_off = 0.15  # gap doesn't change with difficulty
        self._result_secs = 3.2 + max(0.0, dp["result_secs"])

        # Multi-phase sequence: start with 1 symbol, increase by 1 per phase
        # 5 phases for balanced difficulty (up to 5-symbol sequence)
        self._total_phases = 5
        self._current_phase = 1  # phases are 1-indexed
        self._current_phase_len = 1  # phase 1 requires 1 symbol

        # Countdown timer — runs during input phase only
        self._timer_max  = max(6.0, self.BASE_TIMER * dp["timer_mult"])
        self._time_left  = self._timer_max
        
        # Assign symbols to the 9 grid positions
        syms = (GRID_SYMBOLS * 3)[:9]
        random.shuffle(syms)
        self._grid_syms = syms   # list of 9 symbol keys

        # Master sequence: will grow as we progress through phases
        self._master_sequence = []
        self._phase_state = "show"  # "show" | "input" | "phase_result" | "final_result"

        # Show-phase state
        self._show_idx     = -1    # which step we are currently flashing
        self._show_timer   = 0.0
        self._flashing     = False # True while the symbol is bright

        # Input-phase state
        self._input_idx    = 0
        self._mistakes     = 0
        self._max_mistakes = 2
        self._lit_cell     = None  # cell briefly lit green/red on input
        self._lit_timer    = 0.0
        self._lit_color    = (0, 255, 0)

        # Phase result text
        self._phase_result_text = ""
        self._phase_result_color = (220, 220, 220)
        self._phase_result_timer = 0.0

        # Final result
        self._final_result_text = ""
        self._final_result_color = (220, 220, 220)
        self._final_result_timer = 0.0

        # Fonts (lazy)
        self._font       = None
        self._small_font = None
        self._title_font = None
        
        # Generate first phase's new symbol
        self._add_phase_symbol()

    # ── Helper: add a new symbol to the sequence for the current phase ─────────

    def _add_phase_symbol(self):
        """Add one random grid position to the master sequence for this phase."""
        # Pick a random cell index that doesn't duplicate what's already in the sequence
        available = [i for i in range(9) if i not in self._master_sequence]
        if available:
            new_symbol = random.choice(available)
        else:
            # Fallback: all cells used (shouldn't happen with 9 phases max)
            new_symbol = random.randint(0, 8)
        self._master_sequence.append(new_symbol)

    def _advance_to_next_phase(self):
        """Advance to the next phase or finish the ritual."""
        if self._current_phase >= self._total_phases:
            # All phases complete
            self._phase_state = "final_result"
            self._final_result_text = (
                "PERFECT RITUAL!" if self._mistakes == 0
                else "Ritual partial..." if self._mistakes == 1
                else "Ritual FAILED"
            )
            tier_color = (100, 255, 100) if self._mistakes == 0 else (255, 220, 80) if self._mistakes == 1 else (255, 80, 80)
            self._final_result_color = tier_color
            text = self.system._apply_blessing(self.ritual, self._mistakes)
            gui = getattr(self.system.engine, "gui", None)
            if gui and text:
                gui.append(text)
        else:
            # Move to next phase
            self._current_phase += 1
            self._current_phase_len = self._current_phase
            self._phase_state = "phase_result"
            self._phase_result_text = f"Phase {self._current_phase - 1} Complete! Phase {self._current_phase}..."
            self._phase_result_color = (100, 220, 255)
            self._phase_result_timer = 0.0
            # Don't clear input feedback here — let it render; cleared during phase_result->show transition
            self._add_phase_symbol()

    # ── Events ───────────────────────────────────────────────────────────────

    def handle_event(self, event):
        import pygame
        if self.done or self._phase_state != "input":
            return
        if event.type == pygame.KEYDOWN:
            # Number keys 1–9
            if pygame.K_1 <= event.key <= pygame.K_9:
                slot = event.key - pygame.K_1   # 0-indexed
                self._process_input(slot)

    def _process_input(self, slot: int):
        expected = self._master_sequence[self._input_idx]
        if slot == expected:
            # Correct
            self._lit_cell  = slot
            self._lit_timer = 0.4
            self._lit_color = (60, 220, 60)
            self._input_idx += 1
            # Check if this phase is complete
            if self._input_idx >= self._current_phase_len:
                # Phase complete — move to next or finish
                if self._current_phase >= self._total_phases:
                    # All phases done
                    self._phase_state = "final_result"
                    self._final_result_text = (
                        "PERFECT RITUAL!" if self._mistakes == 0
                        else "Ritual partial..." if self._mistakes == 1
                        else "Ritual FAILED"
                    )
                    tier_color = (100, 255, 100) if self._mistakes == 0 else (255, 220, 80) if self._mistakes == 1 else (255, 80, 80)
                    self._final_result_color = tier_color
                    text = self.system._apply_blessing(self.ritual, self._mistakes)
                    gui = getattr(self.system.engine, "gui", None)
                    if gui and text:
                        gui.append(text)
                else:
                    # More phases to go
                    self._advance_to_next_phase()
        else:
            # Wrong
            self._mistakes += 1
            self._lit_cell  = slot
            self._lit_timer = 0.5
            self._lit_color = (220, 60, 60)
            if self._mistakes >= self._max_mistakes:
                # Failed — end ritual
                self._phase_state = "final_result"
                self._final_result_text = "Ritual FAILED"
                self._final_result_color = (255, 80, 80)
                text = self.system._apply_blessing(self.ritual, self._mistakes)
                gui = getattr(self.system.engine, "gui", None)
                if gui and text:
                    gui.append(text)
            else:
                # Reset input for current phase but keep mistakes
                self._input_idx = 0

    # ── Update ────────────────────────────────────────────────────────────────

    def update(self, dt):
        if self.done:
            return

        if self._phase_state == "show":
            self._show_timer += dt
            if not self._flashing:
                # Waiting between flashes
                if self._show_timer >= self._flash_off:
                    self._show_timer = 0.0
                    self._show_idx += 1
                    if self._show_idx >= self._current_phase_len:
                        # All symbols shown for this phase — switch to input
                        self._phase_state = "input"
                        self._input_idx = 0
                        self._time_left = self._timer_max
                        # Clear any residual feedback before input phase
                        self._lit_cell = None
                        self._lit_timer = 0.0
                        self._lit_color = (0, 255, 0)
                        return
                    self._flashing = True
            else:
                # Currently showing a symbol
                if self._show_timer >= self._flash_on:
                    self._show_timer = 0.0
                    self._flashing   = False

        elif self._phase_state == "input":
            if self._lit_timer > 0:
                self._lit_timer = max(0.0, self._lit_timer - dt)

            # Countdown timer during input phase
            self._time_left -= dt
            if self._time_left <= 0:
                self._time_left = 0.0
                # Force fail
                self._mistakes = self._max_mistakes
                self._phase_state = "final_result"
                self._final_result_text = "Ritual FAILED"
                self._final_result_color = (255, 80, 80)
                text = self.system._apply_blessing(self.ritual, self._mistakes)
                gui = getattr(self.system.engine, "gui", None)
                if gui and text:
                    gui.append(text)

        elif self._phase_state == "phase_result":
            self._phase_result_timer += dt
            if self._phase_result_timer >= 1.5:
                # Transition to show next phase
                self._phase_state = "show"
                self._show_idx = -1
                self._show_timer = 0.0
                self._flashing = False
                self._input_idx = 0  # Clear input tracking
                # Clear any lingering input feedback from previous phase
                self._lit_cell = None
                self._lit_timer = 0.0
                self._lit_color = (0, 255, 0)

        elif self._phase_state == "final_result":
            self._final_result_timer += dt
            if self._final_result_timer >= self._result_secs:
                self.done = True

    # ── Render ────────────────────────────────────────────────────────────────

    def render(self, surface):
        import pygame
        self._ensure_fonts()

        sw, sh = surface.get_size()
        pw, ph = self.PANEL_W, self.PANEL_H
        px = (sw - pw) // 2
        py = (sh - ph) // 2

        draw_dim_overlay(surface, 165)
        draw_panel(surface, (px, py, pw, ph),
                   title=f"RITUAL: {self.ritual['name'].upper()}")

        # Countdown timer bar (shown during input phase only — that's when it counts down)
        if self._phase_state == "input":
            draw_timer_bar(surface, px, py, pw, self._time_left, self._timer_max)

        # ── Phase label ───────────────────────────────────────────────────────
        if self._phase_state == "show":
            phase_text  = f"Phase {self._current_phase}/{self._total_phases}: Memorise ({self._show_idx + 1}/{self._current_phase_len})..."
            phase_color = (200, 200, 255)
        elif self._phase_state == "input":
            phase_text  = f"Phase {self._current_phase}/{self._total_phases}: Repeat — step {self._input_idx + 1}/{self._current_phase_len}"
            phase_color = (255, 220, 100)
        elif self._phase_state == "phase_result":
            phase_text = self._phase_result_text
            phase_color = self._phase_result_color
        else:  # final_result
            phase_text  = self._final_result_text
            phase_color = self._final_result_color
        render_label(surface, phase_text, px + pw // 2, py + 44,
                     color=phase_color)

        # ── 3×3 grid of rune cells ────────────────────────────────────────────
        cell_s  = self.CELL_SIZE
        margin  = 12
        grid_w  = 3 * cell_s + 2 * margin
        grid_x  = px + (pw - grid_w) // 2
        grid_y  = py + 80

        for row in range(3):
            for col in range(3):
                idx      = row * 3 + col
                sym_key  = self._grid_syms[idx]
                cx       = grid_x + col * (cell_s + margin)
                cy       = grid_y + row * (cell_s + margin)
                slot_num = idx + 1   # 1-indexed display

                # Determine brightness
                is_lit = False
                cell_col   = (22, 22, 40)
                border_col = (60, 60, 90)
                sym_col    = (130, 130, 160)

                # Show phase
                if self._phase_state == "show":
                    if self._flashing and self._master_sequence[self._show_idx] == idx:
                        is_lit = True
                        cell_col   = (40, 40, 110)
                        border_col = (160, 160, 255)
                        sym_col    = (255, 255, 255)

                # Input + phase-result view
                elif self._phase_state in ("input", "phase_result"):
                    # Check if this cell was just entered (feedback flash)
                    if idx == self._lit_cell and self._lit_timer > 0:
                        is_lit = True
                        cell_col   = (30, 80, 30) if self._lit_color == (60, 220, 60) else (80, 30, 30)
                        border_col = self._lit_color
                        sym_col    = (255, 255, 255)
                    # Otherwise check if cell is in completed sequence (stay green)
                    elif idx in self._master_sequence[:self._input_idx]:
                        cell_col   = (20, 50, 20)
                        border_col = (60, 160, 60)
                        sym_col    = (140, 220, 140)

                pygame.draw.rect(surface, cell_col,
                                 (cx, cy, cell_s, cell_s), border_radius=6)
                pygame.draw.rect(surface, border_col,
                                 (cx, cy, cell_s, cell_s), 2, border_radius=6)

                # Slot number
                num_surf = self._small_font.render(str(slot_num), True, (80, 80, 100))
                surface.blit(num_surf, (cx + 4, cy + 4))

                # Rune symbol char
                char = SYMBOL_CHARS.get(sym_key, "?")
                sym_surf = self._title_font.render(char, True, sym_col)
                surface.blit(sym_surf,
                             (cx + cell_s // 2 - sym_surf.get_width() // 2,
                              cy + cell_s // 2 - sym_surf.get_height() // 2))

                # Pulsing animation glow for currently-being-shown symbol
                if is_lit and self._phase_state == "show":
                    pulse = abs(math.sin(pygame.time.get_ticks() * 0.01))
                    glow = pygame.Surface((cell_s + 8, cell_s + 8), pygame.SRCALPHA)
                    pygame.draw.rect(glow,
                                     (160, 160, 255, int(50 + pulse * 120)),
                                     (0, 0, cell_s + 8, cell_s + 8),
                                     3, border_radius=8)
                    surface.blit(glow, (cx - 4, cy - 4))

        # ── Mistakes indicator ────────────────────────────────────────────────
        mis_y = grid_y + 3 * (cell_s + margin) + 18
        lives_left = self._max_mistakes - self._mistakes
        lives_str  = "Lives: " + "♥ " * lives_left + "♡ " * self._mistakes
        render_label(surface, lives_str, px + pw // 2, mis_y,
                     color=(220, 80, 80))

        # ── Instruction ───────────────────────────────────────────────────────
        if self._phase_state == "input":
            render_label(surface,
                         "Press  [1]–[9]  matching the number keys on the grid",
                         px + pw // 2, mis_y + 26,
                         color=(150, 150, 200), small=True)
        elif self._phase_state == "show":
            render_label(surface,
                         "Watch carefully — then replicate the glowing sequence!",
                         px + pw // 2, mis_y + 26,
                         color=(150, 150, 200), small=True)

    def _ensure_fonts(self):
        if self._font is None:
            import pygame
            from font_support import load_font, wrap_font_with_symbol_fallback

            pygame.font.init()
            self._font = wrap_font_with_symbol_fallback(
                load_font({}, 13, mono=True)
            )
            self._small_font = wrap_font_with_symbol_fallback(
                load_font({}, 11, mono=True)
            )
            self._title_font = wrap_font_with_symbol_fallback(
                load_font({}, 20, mono=True, bold=True)
            )
        _ensure_fonts()
