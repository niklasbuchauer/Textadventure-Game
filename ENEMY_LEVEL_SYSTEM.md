## Enemy Level Scaling System - Implementation Complete

### Overview
Enemies now scale with dungeon floor depth to prevent high-level players from one-shotting everything. Each enemy has a level displayed in combat that determines their stats.

### Level Calculation Formula

**Regular Enemies:**
- Base level: Random 1-3
- Floor scaling: +3 levels per floor
- Floor 1: Level 1-3
- Floor 2: Level 4-6
- Floor 3: Level 7-9

**Mini-Bosses:**
- Base level: 5
- Floor 1: Level 5
- Floor 2: Level 8
- Floor 3: Level 11

**Bosses:**
- Base level: 8
- Floor 1: Level 8
- Floor 2: Level 11
- Floor 3: Level 14

### Stat Scaling (per level above 1)
- **HP:** +15% per level
- **Attack:** +10% per level
- **Defense:** +8% per level
- **XP Reward:** +20% per level
- **Gold Reward:** +15% per level

### Example Scaling Results

**Crystal Beetle (Base: 20 HP, 5 ATK, 1 DEF)**
- Level 1 (Floor 1): 20 HP, 5 ATK, 1 DEF
- Level 5 (Floor 2): 32 HP, 7 ATK, 1 DEF
- Level 9 (Floor 3): 44 HP, 8 ATK, 1 DEF
- Level 15 (Custom): 62 HP, 9 ATK, 1 DEF

**Crystal Titan Boss (Base: 150 HP, 15 ATK, 5 DEF)**
- Level 8 (Floor 1): 245 HP, 25 ATK, 8 DEF
- Level 14 (Floor 3): 354 HP, 34 ATK, 11 DEF

### UI Display
Enemies now show their level in combat:
```
--------------------------------------------------
  Crystal Beetle [Lv.9]
  HP: [████████████████████] 44/44
--------------------------------------------------
```

Bosses show level + BOSS marker:
```
--------------------------------------------------
  Crystal Titan [Lv.14]  BOSS
  HP: [████████████████████] 354/354
--------------------------------------------------
```

### Debug Command Enhancement
The debug spawn command now accepts an optional level parameter:

**Syntax:** `debug spawn enemy <id> [level]`

**Examples:**
- `debug spawn enemy crystal_beetle` - Spawns at default level (1-3)
- `debug spawn enemy crystal_beetle 10` - Spawns at level 10
- `debug spawn enemy crystal_titan 20` - Spawns boss at level 20

### Files Modified

1. **combat_system.py**
   - Added `calculate_enemy_level()` function
   - Added `scale_enemy_stats()` function
   - Added `get_level_abilities()` stub for future enhancements
   - Updated `CombatState.__init__()` to accept level parameter
   - Updated `CombatState.to_dict()` and `from_dict()` to save/load level
   - Updated `create_enemy_instance()` to calculate level and scale stats
   - Updated `create_boss_instance()` to calculate level and scale stats
   - Updated `create_mini_boss_instance()` to calculate level and scale stats
   - Updated `get_combat_status()` to display `[Lv.X]` badge

2. **engine.py**
   - Updated `_start_combat_encounter()` to accept `floor_num` parameter
   - Added floor_num extraction from room_id when not provided
   - Updated calls to creation functions to pass floor_num
   - Updated `_check_room_enemy()` to pass floor_num for boss spawns
   - Updated `_check_room_enemy()` to pass floor_num for regular enemy spawns

3. **debug_commands.py**
   - Updated spawn command routing to parse optional level parameter
   - Updated `_debug_spawn_enemy()` to accept level parameter
   - Updated `_debug_spawn_enemy()` to apply custom level to all enemy types
   - Updated help text to document level parameter
   - Updated examples to show level usage

### Testing Results

✅ Level calculation working (Floor 1-3 scaling verified)
✅ Stat scaling working (HP, ATK, DEF scale correctly)
✅ Combat UI displaying level badges correctly
✅ Boss level scaling (Floor 1 vs Floor 3 shows major difference)
✅ Save/load compatibility (level persists in to_dict/from_dict)
✅ Debug spawn accepts level parameter
✅ Help documentation updated

### Backward Compatibility
- Old save files without level will default to level 1
- All existing enemies continue to work
- Debug commands without level parameter still work (use auto-calculated level)

### Future Enhancements
The `get_level_abilities()` function is a stub that can be expanded to:
- Lock certain abilities behind level requirements
- Give high-level enemies access to boss-tier abilities
- Add level-specific ability variants

### Impact on Gameplay
- Early floors remain accessible to new players
- Deep floors present serious challenges even to veterans
- Boss fights scale dramatically (Floor 3 boss has 44% more HP than Floor 1)
- Players are rewarded with more XP and gold for defeating higher-level enemies
- Late-game content stays engaging instead of becoming a one-shot fest
