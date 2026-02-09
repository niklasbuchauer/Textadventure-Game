# Dungeon System Guide

## Overview

The expanded dungeon system features 25+ unique room types, procedural loot distribution, chest spawning, and multi-layer depth exploration with progressively better loot at deeper levels.

## Room Types (25)

### High-Quality Rooms (More Rare Loot & Chests)
- **Collapsed Treasury Vault** - 3-6 items, 35% chest chance
- **Dark Altar Chamber** - 3-5 items, 40% chest chance
- **Ruined Throne Room** - 4-6 items, 45% chest chance
- **Hidden Vault** - 4-7 items, 50% chest chance (BEST LOOT)
- **Spell Scriptorium** - 3-5 items, 32% chest chance
- **Map Chamber** - 2-4 items, 28% chest chance

### Medium-Quality Rooms (Average Loot & Chests)
- **Ancient Armory** - 2-4 items, 15% chest chance
- **Chamber of Torment** - 2-3 items, 8% chest chance
- **Underground Smithy** - 2-4 items, 20% chest chance
- **Guard Barracks** - 2-4 items, 15% chest chance
- **Storage Vault** - 3-5 items, 22% chest chance
- **Ritual Chamber** - 3-5 items, 38% chest chance
- **Warden's Office** - 2-3 items, 30% chest chance
- **Execution Chamber** - 2-4 items, 12% chest chance
- **Ancient Wine Cellar** - 2-4 items, 18% chest chance
- **Desecrated Chapel** - 1-3 items, 15% chest chance
- **Trophy Hall** - 2-4 items, 25% chest chance

### Low-Quality Rooms (Common Items, Few Chests)
- **Forgotten Library** - 1-3 items, 12% chest chance
- **Musty Burial Crypt** - 1-4 items, 18% chest chance
- **Abandoned Prison Block** - 1-2 items, 5% chest chance
- **Underground Well Room** - 1-2 items, 10% chest chance
- **Great Dining Hall** - 1-3 items, 8% chest chance
- **Flooded Sewer Junction** - 1-2 items, 5% chest chance
- **Collapsed Tunnel** - 1-3 items, 10% chest chance
- **Guardhouse Station** - 1-3 items, 10% chest chance
- **Training Grounds** - 2-3 items, 8% chest chance

## Loot Quality Tiers

### Low Tier Items (1-15 gold value)
rusty_dagger, old_boot, torch, broken_chain, moldy_bread, cracked_skull, torn_cloth, bent_fork, empty_bottle, rat_pelt

### Medium Tier Items (15-60 gold value)
iron_sword, leather_armor_piece, silver_ring, healing_salve, quality_torch, lockpick_set, coin_pouch, steel_dagger, worn_map, craftsman_hammer, enchanted_candle, ancient_coin, rope_coil, iron_key

### High Tier Items (60-180 gold value)
gold_chalice, enchanted_ring, steel_longsword, healing_potion, spell_scroll, jeweled_dagger, magic_amulet, royal_signet, masterwork_shield, ancient_tome, platinum_bar, rare_gemstone, enchanted_cloak_fragment

## Chest System

### Chest Types

**Wooden Chest**
- Spawn: Low quality rooms
- Items: 2-4
- Gold Bonus: 10-40
- Common in all room tiers

**Iron-Bound Chest**
- Spawn: Medium & High quality rooms
- Items: 3-6
- Gold Bonus: 40-100
- More valuable than wooden

**Ornate Chest** (RARE)
- Spawn: High quality rooms only
- Items: 4-8
- Gold Bonus: 80-200
- Contains highest value items
- Spawnchance: 50% in Hidden Vault

### Chest Interactions

---

## Time-Gated Dungeon Access

### Schedule (Germany Timezone)
The dungeon operates on a strict schedule in Germany timezone (Europe/Berlin):
- **Opens**: Every 3 hours for exactly 1 hour duration
- **Opening Times**: 00:00, 03:00, 06:00, 09:00, 12:00, 15:00, 18:00, 21:00
- **Closed Duration**: 2 hours between each opening
- **Auto-Closure**: Dungeon automatically closes and all players are teleported out

### Dungeon Entrance (Mysterious Cave Entrance)
**Location**: Coordinates [5, -3] in the Overworld
- Dark cave mouth with mystical runes
- Only accessible when dungeon is open
- Sacred runes indicate opening status

**Interaction When Closed**:
```
The cave entrance is sealed by mysterious energy.
A glowing inscription reads: "The depths shift and change. Return when the stars align."
Next opening: 2 hours 15 minutes
```

**Interaction When Open**:
```
The magical barrier has faded! The dungeon entrance is open.
⚠ WARNING: The dungeon will close in 47 minutes
⚠ If you are inside when it closes, you will be teleported back to the entrance!
Do you wish to enter? (yes/no)
```

---

## Trap System

### Trap Types and Frequencies

| Trap | Trigger Chance | Damage | Difficulty | Special Effect |
|------|--------|--------|-----------|-----------------|
| Hidden Spike Trap | 30% | 10-25 | Medium | Leaves visible trap |
| Poison Dart Trap | 25% | 5-15 | Hard | Poison 3 turns (3 dmg/turn) |
| Concealed Pit | 20% | 15-30 | Easy | Fall damage |
| Poison Gas Trap | 15% | 8-20 | Hard | Area effect, lingering |
| Crushing Ceiling | 10% | 20-40 | Medium | Can attempt escape |
| Magical Rune Trap | 20% | 12-28 | Very Hard | Magic damage |

### Trap Mechanics
- **Detection**: 40% chance to notice trap before triggering
- **Disarming**: Requires appropriate tools (lockpick_set, rope_coil, etc.)
- **Failed Disarm**: 40% chance to trigger trap when disarm fails
- **Status Effects**: Poison and other effects possible
- **Permanence**: Disarmed/triggered traps remain so for dungeon duration

### Disarm Difficulties and Success Rates
- **Easy**: 70% success rate (Pit Trap)
- **Medium**: 50% success rate (Spike Trap, Crushing Ceiling)
- **Hard**: 30% success rate (Poison Dart, Gas Trap)
- **Very Hard**: 15% success rate (Magic Rune)

### Warning Signs
Each trap has visual or environmental hints:
- Spike Trap: Scratches on floor, suspicious holes
- Poison Dart: Tiny holes in walls
- Pit Trap: Hollow-sounding floor
- Gas Trap: Faint chemical smell
- Crushing Ceiling: Ceiling mechanisms and grooves
- Magic Rune: Glowing symbols carved into floor

---

## Procedural Generation Rules

### Floor Generation
Each dungeon instance generates 2-4 floors:
- **Floor 1**: 8-12 rooms (mostly low/medium quality)
- **Floor 2**: 6-10 rooms (balanced quality)
- **Floor 3**: 5-8 rooms (mostly medium/high quality)
- **Floor 4**: 3-6 rooms (mostly high quality, if exists)
- **Floor 4 Boss Room**: Final chamber with best loot

### Room Quality Distribution by Floor
- **Floor 1**: 50% low, 40% medium, 10% high
- **Floor 2**: 30% low, 50% medium, 20% high
- **Floor 3**: 15% low, 50% medium, 35% high
- **Floor 4**: 5% low, 40% medium, 55% high

### Trap Frequency by Floor
- **Floor 1**: 15% of rooms (1-2 traps expected)
- **Floor 2**: 25% of rooms (1-3 traps expected)
- **Floor 3**: 35% of rooms (2-3 traps expected)
- **Floor 4**: 50% of rooms (2-3 traps expected)

### Layout Types
- **Linear**: Simple path through rooms (primary layout)
- **Branching**: Multiple paths with optional rooms (future expansion)
- **Grid**: 2D maze layout (future expansion)
- **Hub**: Central room with spokes (future expansion)

### Loot Scaling by Floor
Base item values increase with depth:
- **Floor 1**: Base values
- **Floor 2**: +20% item values, better chest spawns
- **Floor 3**: +40% item values, rarer items more common
- **Floor 4**: +60% item values, best loot guaranteed

---

## Unique Seed System

### Seed Generation
Each dungeon instance receives a unique seed based on:
- Current date in Germany timezone (YYYYMMDD)
- Current 3-hour opening cycle (00, 03, 06, 09, 12, 15, 18, 21)
- **Format**: YYYYMMDD + HH (e.g., 202602091600 for Feb 9, 2026 at 16:00)

### Consequences
- Same seed = Completely identical dungeon
- Different seed = Completely different layout, rooms, and loot
- **Same opening time each day** = Same dungeon (e.g., every day at 03:00 has same layout)
- Different opening times = Different dungeons (e.g., 06:00 opening is different from 09:00)

### Replay Value
- 8 unique dungeons per day (one for each opening time)
- Pattern repeats after ~64 days (when date/hour combinations cycle)
- Players encouraged to explore all variations

---

## Dungeon Closure & Teleportation

### Auto-Closure System
- Kicks all players out automatically when clock hits closing hour
- **No exceptions**: All players teleported regardless of activity

### Warning System
Players receive progressive warnings:
- **10 minutes before**: ⚠ WARNING: Dungeon closing in 10 minutes! ⚠
- **5 minutes before**: ⚠ WARNING: Dungeon closing in 5 minutes! ⚠
- **1 minute before**: ⚠ URGENT: Dungeon closing in 1 minute! Leave now! ⚠

### Teleportation
When dungeon closes:
```
⚠ THE DUNGEON IS CLOSING! ⚠
The magical energy shifts! The dungeon begins collapsing!
You are being teleported to safety...

You appear outside the cave entrance, slightly dizzy.
The dungeon has sealed itself once more.
```

### Data Persistence
- **Kept**: Player inventory (all collected loot and items)
- **Kept**: Player health status
- **Lost**: Dungeon layout (regenerates on next opening)
- **Lost**: Visited room status (resets for next instance)
- **Lost**: Trap state (regenerated next opening)

---

## Complete Workflow Example

### Scenario: Wednesday 02:00 Germany Time
Player wants to enter dungeon at 03:00 opening.

**At 02:15**:
```
> go enter
The cave entrance is sealed by mysterious energy.
A glowing inscription reads: "The depths shift and change. Return when the stars align."
Next opening: 45 minutes
```

**At 02:52**:
```
> go enter
The cave entrance is sealed by mysterious energy.
Next opening: 8 minutes
```

**At 03:00 - Dungeon Opens**:
```
> go enter
The magical barrier has faded! The dungeon entrance is open.
⚠ WARNING: The dungeon will close in 60 minutes
Do you wish to enter? (yes/no)
> yes

[Generating new dungeon with seed 20260209_03...]
You descend into the depths...

Dungeon Floor 1: Collapsed Treasury Vault
A massive vault door lies broken on the ground.
Gleaming treasures glint in the darkness.
Items: gold chalice x1, enchanted ring x1
Chests: Wooden chest (3 items, 12 gold)
Exits: east
```

**At 03:45 - Halfway Point**:
```
You are exploring safely, collecting loot.
```

**At 03:50 - Warning**:
```
⚠ WARNING: Dungeon closing in 10 minutes! ⚠

[Player can continue exploring or leave]
```

**At 03:52 - Trap Encounter**:
```
> go east
Ancient Armory
Rusted weapons line crumbling stone walls.
⚠ You notice scratches on the floor and suspicious holes.

> search for traps
You found a SPIKE TRAP! (Armed)

> disarm trap
[Roll... Success!]
You successfully disarm the spike trap!
```

**At 03:59 - Final Warning**:
```
⚠ URGENT: Dungeon closing in 1 minute! Leave now! ⚠
```

**At 04:00 - Dungeon Closes**:
```
⚠ THE DUNGEON IS CLOSING! ⚠
The magical energy shifts! The dungeon begins collapsing!
You are being teleported to safety...

You appear outside the cave entrance, slightly dizzy.
The dungeon has sealed itself once more.

Next opening: 3 hours 0 minutes
```

**Inventory Saved**:
- gold chalice (100 gold)
- enchanted ring (120 gold)
- Wooden chest contents (3 items, 12 gold)
- Total earned: ~360 gold

**At 04:00 - Dungeon Sealed**:
```
> go enter
The cave entrance is sealed by mysterious energy.
Next opening: 3 hours 0 minutes
[All dungeon data cleared, new seed generated at next opening]
```

**At 06:00 - Next Opening**:
```
> go enter
The magical barrier has faded! The dungeon entrance is open.

[NEW dungeon generated with seed 20260209_06...]
[Completely different from 03:00 instance!]
```

---

## Integration Notes

### For Players
- Check the dungeon status whenever you visit the entrance
- Plan your exploration time around the 1-hour window
- Keep valuable items in inventory (don't leave them in dungeon)
- Use traps encounters to find rare loot in harder rooms
- Multiple players can explore same dungeon instance simultaneously

### For Developers
- Tree modules manage the system:
  - `dungeon_scheduler.py`: Time checking
  - `dungeon_generator.py`: Procedural generation
  - `trap_system.py`: Trap mechanics
  - `dungeon_instance.py`: Active instance management
- Dungeon seed stored for exact reproduction
- No permanent dungeon data saved (temporary instance)
- Player data saved normally (inventory, health, etc.)
