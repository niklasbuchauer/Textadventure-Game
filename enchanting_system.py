"""
Enchanting System
=================
Altar-based enchanting that enhances equipped items with bonus stats.
Each altar type offers themed enchantments using dungeon-specific materials.

Enchantments are stored per-slot in player.state["enchantments"].
Bonuses are applied on equip and removed on unequip.

Usage:
  enchant       — View available enchantments at current altar
  enchant <num> — Apply chosen enchantment to equipped item
"""

# =====================================================================
# ENCHANTMENT DATABASE
# =====================================================================
# Organized by altar type. Each enchantment:
#   name: display name
#   description: flavor text
#   target_slot: which equipment slot this can enchant ("any" for all)
#   stats: {stat: bonus}
#   materials: {item_id: count} — consumed on enchantment
#   tier: 1-3 (determines power level and material cost)

ENCHANTMENTS = {
    # ── Crystal Altar (Forge of Light) ──
    "altar_crystal": {
        "crystal_clarity": {
            "name": "Crystal Clarity",
            "description": "Imbues the item with light, sharpening the wearer's senses.",
            "target_slot": "any",
            "stats": {"perception": 2},
            "materials": {"cave_crystal": 3},
            "tier": 1,
        },
        "prismatic_ward": {
            "name": "Prismatic Ward",
            "description": "A shimmering shield of crystalline light.",
            "target_slot": "shield",
            "stats": {"defense": 3, "perception": 1},
            "materials": {"cave_crystal": 2, "raw_diamond": 1},
            "tier": 2,
        },
        "radiant_edge": {
            "name": "Radiant Edge",
            "description": "The weapon gleams with searing light energy.",
            "target_slot": "weapon",
            "stats": {"strength": 3, "perception": 2},
            "materials": {"cave_crystal": 3, "raw_diamond": 2},
            "tier": 3,
        },
    },

    # ── Shadow Altar (Shadowforge) ──
    "altar_shadow": {
        "shadow_step": {
            "name": "Shadow Step",
            "description": "Wraps the item in darkness, quickening the wearer.",
            "target_slot": "any",
            "stats": {"dexterity": 2},
            "materials": {"shadow_essence": 3},
            "tier": 1,
        },
        "nightblade": {
            "name": "Nightblade",
            "description": "Darkness coils around the weapon's edge.",
            "target_slot": "weapon",
            "stats": {"strength": 4, "dexterity": 1},
            "materials": {"shadow_essence": 3, "enchanted_charm": 1},
            "tier": 2,
        },
        "void_shroud": {
            "name": "Void Shroud",
            "description": "A cloak of living shadow that absorbs blows.",
            "target_slot": "armor",
            "stats": {"defense": 3, "dexterity": 2},
            "materials": {"shadow_essence": 4, "enchanted_charm": 1},
            "tier": 3,
        },
    },

    # ── Iron Altar (Dwarven Anvil) ──
    "altar_iron": {
        "ironheart": {
            "name": "Ironheart",
            "description": "Dwarven rune-magic hardens the item beyond normal limits.",
            "target_slot": "any",
            "stats": {"constitution": 2},
            "materials": {"iron_ingot": 3},
            "tier": 1,
        },
        "dwarven_bulwark": {
            "name": "Dwarven Bulwark",
            "description": "Rune-inscribed reinforcement of legendary dwarven craft.",
            "target_slot": "shield",
            "stats": {"defense": 4, "constitution": 2},
            "materials": {"iron_ingot": 3, "refined_iron": 1},
            "tier": 2,
        },
        "mountain_fury": {
            "name": "Mountain's Fury",
            "description": "The force of the deep mountain trembles within this weapon.",
            "target_slot": "weapon",
            "stats": {"strength": 5, "constitution": 1},
            "materials": {"iron_ingot": 4, "refined_iron": 2},
            "tier": 3,
        },
    },

    # ── Catacomb Altar (Altar of Binding) ──
    "altar_catacomb": {
        "soul_ward": {
            "name": "Soul Ward",
            "description": "Binds spectral energy to protect the wearer.",
            "target_slot": "any",
            "stats": {"defense": 1, "constitution": 1},
            "materials": {"bone_fragment": 3, "ectoplasm": 1},
            "tier": 1,
        },
        "deathgrip": {
            "name": "Deathgrip",
            "description": "The weapon pulses with necrotic energy.",
            "target_slot": "weapon",
            "stats": {"strength": 3, "constitution": 2},
            "materials": {"bone_fragment": 3, "ectoplasm": 2},
            "tier": 2,
        },
        "lich_blessing": {
            "name": "Lich's Blessing",
            "description": "Ancient undead power flows through the item.",
            "target_slot": "accessory",
            "stats": {"perception": 3, "constitution": 2, "charisma": 1},
            "materials": {"bone_fragment": 4, "ectoplasm": 2, "blood_ruby": 1},
            "tier": 3,
        },
    },

    # ── Forge (basic enchants, available at village blacksmith) ──
    "forge": {
        "sharpen": {
            "name": "Sharpening",
            "description": "A masterful sharpening improves the weapon's edge.",
            "target_slot": "weapon",
            "stats": {"strength": 1},
            "materials": {"iron_ingot": 2},
            "tier": 1,
        },
        "reinforce": {
            "name": "Reinforcement",
            "description": "Extra rivets and padding strengthen the armor.",
            "target_slot": "armor",
            "stats": {"defense": 1},
            "materials": {"iron_ingot": 2, "leather_scrap": 1},
            "tier": 1,
        },
        "polish": {
            "name": "Polish",
            "description": "A fine polish makes the shield gleam and deflect better.",
            "target_slot": "shield",
            "stats": {"defense": 1},
            "materials": {"iron_ingot": 1},
            "tier": 1,
        },
    },
}

# Tier icons
TIER_ICONS = {1: "✦", 2: "✦✦", 3: "✦✦✦"}

from progression_system import add_stat_bonus, normalize_core_stats

# =====================================================================
# ENCHANTMENT SYSTEM
# =====================================================================

try:
    from equipment_system import EQUIPMENT_DATABASE, EQUIPMENT_SLOTS
    EQUIP_AVAILABLE = True
except ImportError:
    EQUIP_AVAILABLE = False
    EQUIPMENT_DATABASE = {}
    EQUIPMENT_SLOTS = []


class EnchantingSystem:
    """Manages altar-based enchanting of equipment."""

    def __init__(self, engine):
        self.engine = engine

    def get_current_altar_type(self):
        """Determine what altar type is in the current room.
        Returns altar type string or None."""
        # Delegate to crafting system's station detection
        try:
            if hasattr(self.engine, 'crafting_system') and self.engine.crafting_system:
                return self.engine.crafting_system.get_current_station_type()
        except Exception:
            pass
        return None

    def get_enchantments(self):
        """Get player's current enchantments dict.
        Structure: {slot: {enchant_id, name, stats}}"""
        if not self.engine.player:
            return {}
        return self.engine.player.state.get("enchantments", {})

    def get_available_enchantments(self, altar_type):
        """Get enchantments available at this altar, filtered by what
        the player has equipped and can afford."""
        altar_enchants = ENCHANTMENTS.get(altar_type, {})
        if not altar_enchants:
            return []

        equipment = self.engine.player.state.get("equipment", {})
        current_enchants = self.get_enchantments()
        inv = self.engine.player.inventory

        available = []
        for ench_id, ench in altar_enchants.items():
            target = ench["target_slot"]

            # Check which slots this can apply to
            applicable_slots = []
            if target == "any":
                applicable_slots = [s for s in EQUIPMENT_SLOTS if equipment.get(s)]
            elif equipment.get(target):
                applicable_slots = [target]

            if not applicable_slots:
                continue

            # Check if player has materials
            has_materials = True
            for mat_id, count in ench["materials"].items():
                if inv.get(mat_id, 0) < count:
                    has_materials = False
                    break

            # Check if any applicable slot is not already enchanted with this
            can_apply = False
            for slot in applicable_slots:
                existing = current_enchants.get(slot, {}).get("enchant_id", "")
                if existing != ench_id:
                    can_apply = True
                    break

            available.append({
                "enchant_id": ench_id,
                "enchant": ench,
                "has_materials": has_materials,
                "applicable_slots": applicable_slots,
                "can_apply": can_apply,
            })

        return available

    def show_enchanting_menu(self):
        """Show enchanting options at the current altar."""
        altar_type = self.get_current_altar_type()
        if not altar_type:
            return "There is no enchanting altar here.\nVisit the Blacksmith's Forge or a dungeon altar."

        if not EQUIP_AVAILABLE:
            return "Equipment system not available."

        from crafting_system import STATION_NAMES
        altar_name = STATION_NAMES.get(altar_type, "Enchanting Altar")
        available = self.get_available_enchantments(altar_type)

        result = "\n" + "═" * 55 + "\n"
        result += f"  ✨ ENCHANTING — {altar_name}\n"
        result += "═" * 55 + "\n\n"

        equipment = self.engine.player.state.get("equipment", {})
        current_enchants = self.get_enchantments()

        # Show current equipment and enchantments
        result += "  Current equipment:\n"
        for slot in EQUIPMENT_SLOTS:
            item_id = equipment.get(slot)
            if item_id:
                eq = EQUIPMENT_DATABASE.get(item_id, {})
                name = eq.get("name", item_id.replace("_", " "))
                ench = current_enchants.get(slot)
                if ench:
                    result += f"    {slot.title()}: {name} [✨ {ench['name']}]\n"
                else:
                    result += f"    {slot.title()}: {name}\n"
            else:
                result += f"    {slot.title()}: (empty)\n"

        result += "\n  Available enchantments:\n\n"

        if not available:
            result += "  No enchantments available. You need equipment and materials.\n"
            # Show what materials are needed
            altar_enchants = ENCHANTMENTS.get(altar_type, {})
            if altar_enchants:
                result += "\n  Enchantments at this altar require:\n"
                all_mats = set()
                for ench in altar_enchants.values():
                    for mat in ench["materials"]:
                        all_mats.add(mat)
                for mat in sorted(all_mats):
                    nice = mat.replace("_", " ")
                    have = self.engine.player.inventory.get(mat, 0)
                    result += f"    • {nice} (you have: {have})\n"
        else:
            for i, info in enumerate(available, 1):
                ench = info["enchant"]
                tier_icon = TIER_ICONS.get(ench["tier"], "✦")
                status = "✅" if info["has_materials"] else "❌"

                result += f"  {i}. {status} {tier_icon} {ench['name']}\n"
                result += f"       {ench['description']}\n"

                # Stats
                stats_str = ", ".join(f"+{v} {k.upper()}" for k, v in ench["stats"].items())
                result += f"       Stats: {stats_str}\n"

                # Slot targets
                slots_str = ", ".join(s.title() for s in info["applicable_slots"])
                result += f"       Applies to: {slots_str}\n"

                # Materials
                inv = self.engine.player.inventory
                mat_parts = []
                for mat, need in ench["materials"].items():
                    have = inv.get(mat, 0)
                    nice = mat.replace("_", " ")
                    indicator = "✓" if have >= need else "✗"
                    mat_parts.append(f"{indicator} {nice}: {have}/{need}")
                result += f"       Materials: {', '.join(mat_parts)}\n\n"

        result += "  Enter a number to enchant, or 'cancel'.\n"
        result += "═" * 55 + "\n"

        # Store pending state
        self.engine.pending_enchant = {
            "altar_type": altar_type,
            "available": available,
        }

        return result

    def handle_enchant_choice(self, cmd):
        """Handle player's enchantment choice."""
        pending = self.engine.pending_enchant
        if not pending:
            return None

        self.engine.pending_enchant = None

        cmd = cmd.strip().lower()
        if cmd in ("cancel", "no", "back", "quit", "exit"):
            return "You step away from the altar."

        try:
            idx = int(cmd) - 1
        except ValueError:
            return "Enchanting cancelled."

        available = pending["available"]
        if idx < 0 or idx >= len(available):
            return "Invalid choice. Enchanting cancelled."

        info = available[idx]
        if not info["has_materials"]:
            return "You don't have the required materials for this enchantment."
        if not info["can_apply"]:
            return "This enchantment cannot be applied to any current equipment."

        ench = info["enchant"]
        slots = info["applicable_slots"]

        # If multiple slots, ask which (store for follow-up)
        if len(slots) > 1:
            result = f"\n  Apply {ench['name']} to which item?\n"
            equipment = self.engine.player.state.get("equipment", {})
            for i, slot in enumerate(slots, 1):
                item_id = equipment.get(slot)
                eq = EQUIPMENT_DATABASE.get(item_id, {})
                name = eq.get("name", item_id.replace("_", " ") if item_id else "empty")
                result += f"  {i}. {slot.title()}: {name}\n"
            result += "  Enter a number, or 'cancel'.\n"

            self.engine.pending_enchant = {
                "choosing_slot": True,
                "enchant_info": info,
                "slots": slots,
            }
            return result

        # Apply to the single applicable slot
        return self._apply_enchantment(info["enchant_id"], ench, slots[0])

    def handle_slot_choice(self, cmd):
        """Handle slot selection when enchantment applies to multiple slots."""
        pending = self.engine.pending_enchant
        if not pending or not pending.get("choosing_slot"):
            return None

        self.engine.pending_enchant = None

        cmd = cmd.strip().lower()
        if cmd in ("cancel", "no", "back"):
            return "Enchanting cancelled."

        try:
            idx = int(cmd) - 1
        except ValueError:
            return "Enchanting cancelled."

        slots = pending["slots"]
        if idx < 0 or idx >= len(slots):
            return "Invalid slot. Enchanting cancelled."

        info = pending["enchant_info"]
        return self._apply_enchantment(info["enchant_id"], info["enchant"], slots[idx])

    def _apply_enchantment(self, enchant_id, ench, slot):
        """Apply an enchantment to a specific equipment slot."""
        inv = self.engine.player.inventory
        player = self.engine.player
        equipment = player.state.get("equipment", {})
        item_id = equipment.get(slot)

        if not item_id:
            return f"No item equipped in {slot} slot."

        # Verify materials again
        for mat_id, count in ench["materials"].items():
            if inv.get(mat_id, 0) < count:
                nice = mat_id.replace("_", " ")
                return f"Not enough {nice}."

        # Remove old enchantment bonuses if slot already enchanted
        current_enchants = player.state.get("enchantments", {})
        old_ench = current_enchants.get(slot)
        if old_ench:
            # Remove old stat bonuses
            for stat, val in old_ench.get("stats", {}).items():
                add_stat_bonus(player, stat, -val)

        # Consume materials
        for mat_id, count in ench["materials"].items():
            inv[mat_id] -= count
            if inv[mat_id] <= 0:
                del inv[mat_id]
        self.engine._inventory_changed = True

        # Apply new enchantment
        ench_data = {
            "enchant_id": enchant_id,
            "name": ench["name"],
            "stats": dict(ench["stats"]),
            "tier": ench["tier"],
        }
        if "enchantments" not in player.state:
            player.state["enchantments"] = {}
        player.state["enchantments"][slot] = ench_data

        # Apply stat bonuses
        for stat, val in ench["stats"].items():
            add_stat_bonus(player, stat, val)
        normalize_core_stats(player)

        # Launch Rune Inscription overlay if GUI available (bonus if perfect trace)
        gui = getattr(self.engine, "gui", None)
        if gui is not None:
            overlay = RuneInscriptionOverlay(self, ench, ench_data)
            gui._rune_overlay = overlay

        # Build result
        eq_data = EQUIPMENT_DATABASE.get(item_id, {})
        eq_name = eq_data.get("name", item_id.replace("_", " "))
        tier_icon = TIER_ICONS.get(ench["tier"], "✦")

        result = "\n" + "═" * 55 + "\n"
        result += f"  ✨ ENCHANTMENT APPLIED!\n"
        result += "═" * 55 + "\n\n"
        result += f"  {tier_icon} {ench['name']} → {eq_name}\n\n"
        result += f"  {ench['description']}\n\n"

        stats_str = ", ".join(f"+{v} {k.upper()}" for k, v in ench["stats"].items())
        result += f"  Bonus stats: {stats_str}\n"

        if old_ench:
            result += f"\n  (Replaced: {old_ench['name']})\n"

        # XP for enchanting
        try:
            from progression_system import award_xp, XP_AWARDS
            xp = {1: 15, 2: 30, 3: 50}.get(ench["tier"], 15)
            xp_msg = award_xp(player, xp, "enchanting")
            if xp_msg:
                result += "\n" + xp_msg
        except (ImportError, Exception):
            pass

        result += "\n" + "═" * 55 + "\n"
        return result

    def on_equip(self, slot, item_id):
        """Called when an item is equipped — reapply enchantment bonuses."""
        enchants = self.get_enchantments()
        ench = enchants.get(slot)
        if ench:
            for stat, val in ench.get("stats", {}).items():
                add_stat_bonus(self.engine.player, stat, val)
            normalize_core_stats(self.engine.player)

    def on_unequip(self, slot, item_id):
        """Called when an item is unequipped — remove enchantment bonuses.
        Also clears the enchantment since it was bound to the item."""
        enchants = self.engine.player.state.get("enchantments", {})
        ench = enchants.get(slot)
        if ench:
            for stat, val in ench.get("stats", {}).items():
                add_stat_bonus(self.engine.player, stat, -val)
            # Clear enchantment when item is unequipped
            del enchants[slot]

    def get_enchant_display(self, slot):
        """Get a short display string for an enchantment on a slot."""
        enchants = self.get_enchantments()
        ench = enchants.get(slot)
        if not ench:
            return ""
        tier_icon = TIER_ICONS.get(ench.get("tier", 1), "✦")
        return f" {tier_icon} {ench['name']}"


# ──────────────────────────────────────────────────────────────────────────────
#  RUNE INSCRIPTION OVERLAY  —  W/A/S/D tracing minigame
# ──────────────────────────────────────────────────────────────────────────────

class RuneInscriptionOverlay:
    """
    W/A/S/D direction-tracing minigame shown after an enchantment is applied.
    Perfect trace → bonus stat (+1 to first enchanted stat).
    Partial trace → no bonus.
    Uses RUNE_SEQUENCES from ascii_art.py (tier-appropriate length).
    """
    DURATION_RESULT = 2.4   # seconds to show result before dismissing

    _KEY_LABELS = {
        "W": "▲", "A": "◀", "S": "▼", "D": "▶",
    }

    def __init__(self, enchanting_system, ench: dict, ench_data: dict):
        self.enchanting_system = enchanting_system
        self.ench      = ench
        self.ench_data = ench_data
        self.done      = False
        self._phase    = "input"  # "input" | "result"
        self._result_t = 0.0
        self._result_text  = ""
        self._result_color = (220, 220, 220)
        self._font  = None
        self._small = None
        self._title = None

        # Pick sequence by tier
        try:
            from ascii_art import RUNE_SEQUENCES
            tier = ench.get("tier", 1)
            key  = {1: "tier1", 2: "tier2", 3: "tier3"}.get(tier, "tier1")
            import random
            sequences = RUNE_SEQUENCES.get(key, [])
            self._sequence = list(random.choice(sequences)) if sequences else list("WASD")
        except ImportError:
            import random
            from itertools import product
            self._sequence = random.choices(["W","A","S","D"], k=4)

        self._idx      = 0   # current step
        self._mistakes = 0
        self._lit_key  = None
        self._lit_t    = 0.0
        self._lit_col  = (60, 220, 60)

    def handle_event(self, event):
        import pygame
        if self.done or self._phase != "input":
            return
        key_map = {
            pygame.K_w: "W", pygame.K_a: "A",
            pygame.K_s: "S", pygame.K_d: "D",
        }
        if event.type == pygame.KEYDOWN:
            pressed = key_map.get(event.key)
            if pressed:
                self._process(pressed)

    def _process(self, key: str):
        expected = self._sequence[self._idx]
        if key == expected:
            self._lit_key = key
            self._lit_t   = 0.38
            self._lit_col = (60, 220, 60)
            self._idx    += 1
            if self._idx >= len(self._sequence):
                self._finish_input()
        else:
            self._mistakes += 1
            self._lit_key = key
            self._lit_t   = 0.38
            self._lit_col = (220, 60, 60)
            self._idx     = 0   # reset

    def _finish_input(self):
        self._phase = "result"
        gui = getattr(self.enchanting_system.engine, "gui", None)
        ench_name = self.ench.get("name", "enchantment")
        if self._mistakes == 0:
            # Perfect — award +1 bonus to first enchanted stat
            player = self.enchanting_system.engine.player
            stat_bonuses = self.ench_data.get("stats", {})
            first_stat   = next(iter(stat_bonuses), None)
            if first_stat:
                player.stats[first_stat] = player.stats.get(first_stat, 0) + 1
                # Update stored ench_data too
                enc_stored = player.state.get("enchantments", {})
                for slot_data in enc_stored.values():
                    if slot_data.get("enchant_id") == self.ench_data.get("enchant_id"):
                        slot_data["stats"][first_stat] = slot_data["stats"].get(first_stat, 0) + 1
                        break
            self._result_text  = f"Perfect rune trace!  +1 {(first_stat or '').upper()} bonus!"
            self._result_color = (100, 255, 100)
            if gui:
                gui.append(
                    f"  ✨ Rune minigame success: {ench_name}. "
                    f"Bonus applied: +1 {(first_stat or 'stat').upper()}."
                )
        else:
            self._result_text  = f"Trace complete  ({self._mistakes} mistake{'s' if self._mistakes>1 else ''}) — no bonus."
            self._result_color = (220, 180, 80)
            if gui:
                gui.append(
                    f"  ⚠️ Rune minigame incomplete: {ench_name}. "
                    f"{self._mistakes} mistake{'s' if self._mistakes > 1 else ''}; no bonus granted."
                )

    def update(self, dt):
        if self.done:
            return
        if self._lit_t > 0:
            self._lit_t = max(0.0, self._lit_t - dt)
        if self._phase == "result":
            self._result_t += dt
            if self._result_t >= self.DURATION_RESULT:
                self.done = True

    def render(self, surface):
        try:
            import pygame
            from ascii_art import (RUNES, render_ascii_block, draw_dim_overlay,
                                   draw_panel, render_label, _ensure_fonts)
            _ensure_fonts()
        except ImportError:
            return

        if self._font is None:
            import pygame
            from font_support import load_font, wrap_font_with_symbol_fallback

            self._font = wrap_font_with_symbol_fallback(
                load_font({}, 14, mono=True, bold=True)
            )
            self._small = wrap_font_with_symbol_fallback(
                load_font({}, 11, mono=True)
            )
            self._title = wrap_font_with_symbol_fallback(
                load_font({}, 18, mono=True, bold=True)
            )

        sw, sh = surface.get_size()
        pw, ph = 460, 320
        px = (sw - pw) // 2
        py = (sh - ph) // 2

        draw_dim_overlay(surface, 150)
        draw_panel(surface, (px, py, pw, ph),
                   title=f"RUNE INSCRIPTION — {self.ench.get('name','').upper()}")

        if self._phase == "input":
            render_label(surface,
                         f"Trace the rune sequence  ({self._idx}/{len(self._sequence)} complete)",
                         px + pw // 2, py + 44, color=(180, 180, 255))
        else:
            render_label(surface, self._result_text,
                         px + pw // 2, py + 44, color=self._result_color)

        # Draw WASD key tiles
        tile_s = 62
        tile_gap = 10
        keys = ["W", "A", "S", "D"]
        total_w = len(keys) * tile_s + (len(keys)-1) * tile_gap
        start_x = px + (pw - total_w) // 2
        tile_y  = py + 80

        for i, k in enumerate(keys):
            tx = start_x + i * (tile_s + tile_gap)
            is_next = (self._phase == "input"
                       and self._idx < len(self._sequence)
                       and self._sequence[self._idx] == k)
            is_done = (self._phase == "input"
                       and any(self._sequence[j] == k for j in range(self._idx)))
            is_lit  = (self._lit_key == k and self._lit_t > 0)

            if is_lit:
                bg_col = (int(self._lit_col[0]*0.3), int(self._lit_col[1]*0.3), int(self._lit_col[2]*0.3))
                bd_col = self._lit_col
                txt_col = (255, 255, 255)
            elif is_next:
                bg_col  = (20, 40, 80)
                bd_col  = (120, 160, 255)
                txt_col = (220, 220, 255)
            elif is_done:
                bg_col  = (15, 50, 15)
                bd_col  = (60, 160, 60)
                txt_col = (120, 200, 120)
            else:
                bg_col  = (22, 22, 40)
                bd_col  = (55, 55, 80)
                txt_col = (100, 100, 130)

            import pygame
            pygame.draw.rect(surface, bg_col,  (tx, tile_y, tile_s, tile_s), border_radius=6)
            pygame.draw.rect(surface, bd_col,  (tx, tile_y, tile_s, tile_s), 2, border_radius=6)
            sym = self._KEY_LABELS.get(k, k)
            sym_surf = self._title.render(sym, True, txt_col)
            surface.blit(sym_surf, (tx + tile_s//2 - sym_surf.get_width()//2,
                                    tile_y + tile_s//2 - sym_surf.get_height()//2))
            key_surf = self._small.render(k, True, (60, 60, 80))
            surface.blit(key_surf, (tx + 4, tile_y + 4))

        # Sequence progress dots
        dot_y  = tile_y + tile_s + 20
        dot_cx = px + pw // 2
        total  = len(self._sequence)
        for j in range(total):
            dx = dot_cx - (total * 14) // 2 + j * 14 + 7
            col = (80, 200, 80) if j < self._idx else (60, 60, 90)
            pygame.draw.circle(surface, col, (dx, dot_y), 5)

        # Instruction
        if self._phase == "input":
            seq_hint = " → ".join(self._sequence)
            render_label(surface, f"Sequence: {seq_hint}",
                         px + pw // 2, py + ph - 64, color=(130, 130, 180), small=True)
            render_label(surface, "Press  W / A / S / D  to trace the rune",
                         px + pw // 2, py + ph - 44, color=(100, 100, 160), small=True)
        else:
            render_label(surface, "Enchantment complete!",
                         px + pw // 2, py + ph - 44, color=(160, 220, 160), small=True)
