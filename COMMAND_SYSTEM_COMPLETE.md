# Command System Enhancement - Complete Implementation

## April 2026 Registry Overhaul Update

### What changed

1. Added a registry-first dispatcher in `CommandHandler` (`engine.py`) for command routing.
2. Migrated additional command families to registry handlers:
   - Progression: `stats`, `skills`, `ability`, `synergy`, `achievements`, `prestige`, `faction`, `pet`, `party`
   - Equipment: `equip`, `unequip`, `equipment`, `transmog`, `cosmetics`, `artifact`
   - Combat: `attack`, `defend`, `flee`
3. Added canonical metadata map (`_build_command_metadata`) to centralize category/usage/alias definitions for future auto-generated help/docs.
4. Removed redundant legacy branch checks for all migrated commands while preserving fallback for non-migrated command groups.
5. Migrated additional command families into registry handlers:
   - Shop/Bank: `shop`, `bank`, `deposit`, `withdraw`, `balance`, `upgrade bank`
   - NPC interaction: `talk`, `gift/give`, `reputation/rep`
   - Gathering/Crafting stations: `fish`, `bait`, `brew/alchemy`, `smelt`, `ritual`, `enchant`, `fight`
6. Connected metadata to help rendering by generating compact help sections from `_build_command_metadata`.
7. Added new debug QA commands for elite progression testing:
   - `debug loot <boss|miniboss|name>`
   - `debug loot sim <boss|miniboss> <enemy_id> [runs]`
   - `debug set grant <set_name> [equip]`
   - `debug set clear <set_name>`
   - `debug set status <set_name>`
8. Added new debug cosmetics/skin QA commands:
   - `debug cosmetics list`
   - `debug cosmetics unlock <id|all>`
   - `debug cosmetics lock <id|all>`
   - `debug cosmetics apply <slot_or_item> <id|clear>`
   - `debug cosmetics preview <slot>`
   - `debug cosmetics randomize [slot]`
   - `debug cosmetics reset`
   - `debug cosmetics status`

### Validation

- `test_command_system.py` passes after migration.
- `engine.py` has no reported static errors.

### Next migration targets

- Registry migration target set is complete for standard gameplay command groups.
- Remaining non-registry routes are intentional specialized command handlers (secret/easter-egg/puzzle pathways).

## Summary

Successfully implemented comprehensive command system improvements including:
1. ✅ **Fixed "inspect wall" command** - Now fully functional with detailed feedback
2. ✅ **Added comprehensive command list** - Context-aware help system
3. ✅ **Implemented command aliases** - Quick shortcuts (n/s/e/w/u/d)
4. ✅ **Added contextual hints** - Room-specific suggestions

---

## Changes Made

### 1. Enhanced Inspect/Examine Command ([engine.py](engine.py#L1266-L1346))

**What was changed:**
- Expanded `_examine()` method to handle many more inspection targets
- Added detailed feedback for all inspection types
- Improved wall inspection with contextual responses

**New inspection targets:**
- **Walls**: Detects secrets in boss rooms, gives contextual feedback
- **Chests**: Detailed chest inspection with type information
- **Traps**: Trap detection and identification
- **Ground/Floor**: Items detection on the ground
- **Items**: Enhanced item examination with quantity and value
- **Unknown targets**: Helpful suggestions on what to inspect

**Example outputs:**
```
> inspect wall
You carefully examine the walls.
The stone is cold and weathered. Nothing unusual stands out.

> inspect chest
You inspect the chest closely.
It's a wooden chest, securely locked.
Type 'open chest' to attempt to open it.

> inspect ground
You examine the ground.
You see some items scattered about.
Type 'look' to see what's available.
```

---

### 2. Command Aliases ([engine.py](engine.py#L190-L203))

**Added quick movement shortcuts:**
- `n` → `go north`
- `s` → `go south`
- `e` → `go east`
- `w` → `go west`
- `u` → `go up`
- `d` → `go down`

**Implementation:**
```python
# Command aliases for easier play
aliases = {
    "n": "north",
    "s": "south",
    "e": "east",
    "w": "west",
    "u": "up",
    "d": "down",
}

# Expand single-letter movement aliases
if verb in aliases and not args:
    verb = "go"
    args = [aliases[cmd.lower()]]
```

---

### 3. Comprehensive Command List ([engine.py](engine.py#L1605-L1691))

**Replaced simple help with context-aware comprehensive system:**

**Features:**
- Beautiful box-drawing character UI
- Context-aware sections (dungeon, shop, system)
- Organized by category (Movement, Exploration, Inventory, etc.)
- Shows relevant commands based on current location

**Sections displayed:**
- 📍 **MOVEMENT** - All navigation commands
- 🔍 **EXPLORATION** - Looking, inspecting, searching, map
- 🎒 **INVENTORY** - Managing items
- ⚔️  **DUNGEON ACTIONS** (when in dungeon) - Chests, traps, secrets
- 🏪 **SHOP COMMANDS** (when in shop) - Buying, selling, negotiating
- 💾 **SYSTEM** - Help, save, quit
- 💡 **TIPS** - Gameplay hints

**Example:**
```
╔════════════════════════════════════════════════════════════════╗
║                     AVAILABLE COMMANDS                         ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  [MOVEMENT]                                                    ║
║  ---------------------------------------------------------------║
║    go <direction>       - Move (north, south, east, west)      ║
║    n / s / e / w        - Quick movement shortcuts             ║
...
```

---

### 4. Contextual Hints System ([engine.py](engine.py#L1693-L1732))

**Added intelligent hint system that detects:**

- 🌟 **Secret rooms**: "This room feels unusual. Try 'inspect wall' to look for secrets!"
- ⚠️  **Traps**: "Be careful! This area looks dangerous. Use 'search' to look for traps."
- 💰 **Loot**: "Items are available here. Use 'take <item>' or look around."
- 📦 **Chests**: "A chest is here! Try 'open chest' to see what's inside."
- 🚪 **Special exits**: Shows availability of secret passages, stairs up/down

**Example output:**
```
[AVAILABLE ACTIONS IN THIS ROOM]
   [HINT] This room feels unusual. Try 'inspect wall' to look for secrets!
   [TREASURE] A chest is here! Try 'open chest' to see what's inside.
   [EXIT] Stairs down available - use 'go down' or 'd'
```

---

### 5. Fixed Help Command Routing ([engine.py](engine.py#L273))

**What was changed:**
- Modified help command to use new comprehensive system
- Removed dependency on debug-only help
- Both `help`, `commands`, and `?` now show comprehensive list

**Before:** Simple text list from debug system
**After:** Beautiful, comprehensive, context-aware command list

---

## Testing Results

All tests **PASSED** ✅

```
[TEST 1] Engine initialization... [PASS]
[TEST 2] Command aliases (n/s/e/w)... [PASS]
[TEST 3] Help/commands display... [PASS]
  - Movement section present
  - Exploration section present
  - Inventory section present
[TEST 4] 'commands' alias... [PASS]
[TEST 5] '?' alias... [PASS]
[TEST 6] Inspect wall command... [PASS]
[TEST 7] Examine command... [PASS]
[TEST 8] Various inspection targets... [PASS]
```

---

## Usage Examples

### Quick Movement
```
> n
[Moves north]

> s
[Moves south]

> u
[Goes upstairs]
```

### Inspection
```
> inspect wall
You carefully examine the walls.
Wait... one section seems different!
*CLICK*
✨ A SECRET PASSAGE HAS BEEN REVEALED! ✨

> inspect chest
You inspect the chest closely.
It's a golden chest, securely locked.
Type 'open chest' to attempt to open it.

> inspect ground
You examine the ground.
You see some items scattered about.
Type 'look' to see what's available.
```

### Help System
```
> help
[Shows comprehensive command list]

> commands
[Shows same comprehensive list]

> ?
[Shows same comprehensive list]
```

---

## Files Modified

1. **[engine.py](engine.py)**
   - Lines 190-203: Added command alias system
   - Lines 273: Updated help command routing
   - Lines 1266-1346: Enhanced _examine() method
   - Lines 1605-1691: New comprehensive _show_commands() method
   - Lines 1693-1732: New _get_contextual_hints() method

2. **[test_command_system.py](test_command_system.py)** (new)
   - Comprehensive test suite for all command enhancements

3. **[test_help_output.py](test_help_output.py)** (new)
   - Manual test for help command output

---

## Key Features Summary

✅ **"inspect wall" command** - Fully working, discovers secrets in boss rooms
✅ **Command aliases** - Quick shortcuts: n, s, e, w, u, d
✅ **Comprehensive help** - Beautiful, organized, context-aware command list
✅ **Contextual hints** - Smart suggestions based on current room
✅ **Multiple inspection targets** - Wall, chest, ground, items, traps
✅ **Context awareness** - Different commands shown in dungeons/shops
✅ **User-friendly** - Clear feedback, helpful suggestions, easy navigation

---

## Status: ✅ COMPLETE

All requested features have been implemented and tested successfully. The command system is now comprehensive, user-friendly, and context-aware.

---

## Home Debug Commands (March 2026)

Added dedicated home-debug commands for rapid QA and content iteration:

- `debug home free` - Grants home ownership and initializes home state.
- `debug home items` - Grants one copy of every home item.
- `debug home reset` - Full home wipe: removes ownership and resets name, layout, upgrades, and bonuses.

## Home Use Command (March 2026)

Added a new player-facing command:

- `home use` - Lists all currently usable placed home objects and shows the exact `use <item_id>` command for each.

Debug command visibility updated in:

- Player command handler in `engine.py`
- Pygame command reference in `commands_window.py`
- Quick reference doc in `COMMAND_QUICK_REFERENCE.md`

Command visibility updated in:

- Debug text menu in `debug_commands.py`
- Pygame command reference in `commands_window.py`
- Quick reference doc in `COMMAND_QUICK_REFERENCE.md`

## Home Rooms And Storage Commands (April 2026)

Added a utility-focused home command layer for the room rework foundation:

- `home bonus` - Shows currently active timed home room utility bonus.
- `home rooms` - Lists all home rooms and lock status.
- `home room <room_id>` - Switches active home room when unlocked.
- `home unlock <room_id>` - Unlocks a room using gold.
- `home containers` - Shows room-local storage containers and contents.
- `home store <item> [qty]` - Stores inventory items into current room container.
- `home take <item> [qty]` - Retrieves items from current room container.
- `home spawn <room_id>` - Sets default active home room when entering home.
- `home garden` - Shows plot status for the garden room.
- `home plant <item> [qty]` - Plants seeds/crops in garden plots.
- `home harvest` - Harvests all ready crops in the garden.

Supporting behavior updates:

- `home upgrades` now reports room unlock progression instead of legacy expansions.
- `home use` is now scoped to objects in the active home room.
- Home data now uses schema v2 with a hard reset path from old schema versions.

Command visibility updated in:

- Player command handler in `engine.py`
- Pygame command reference in `commands_window.py`
- Quick reference doc in `COMMAND_QUICK_REFERENCE.md`

## Command Preview Parity And Farming Sources (April 2026)

Command visibility was expanded so implemented commands are discoverable in the pygame command reference and quick docs.

Added preview/list coverage for:

- Progression/meta commands (`abilities`, `ability`, `synergy`, `achievements`, `prestige`, `faction`, `pet`, `party`)
- Equipment/cosmetic commands (`equip`, `unequip`, `equipment`, `artifact`, `transmog`, `cosmetics`)
- Economy/station commands (`shop`, `bank`, `deposit`, `withdraw`, `balance`, `upgrade bank`, `brew`, `smelt`, `enchant`, `ritual`)
- Home travel command (`hearthstone`)

Garden economy availability was also expanded so seeds can be acquired through multiple gameplay loops:

- Shop pools (primary source)
- Fishing loot table (secondary source)
- Dungeon themed loot (tertiary source)
- Overworld encounter drops (tertiary source)
