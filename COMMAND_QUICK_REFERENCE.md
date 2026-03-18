# Command System Quick Reference

## New Command Aliases

### Quick Movement
- `n` = go north
- `s` = go south  
- `e` = go east
- `w` = go west
- `u` = go up (stairs)
- `d` = go down (stairs)

### Help Commands
- `help` = Show comprehensive command list
- `commands` = Same as help
- `?` = Same as help

## Home Commands

- `buy home deed` = Purchase your first home deed
- `home` = Travel to your home
- `home edit` = Open the interactive home editor UI
- `home use` = List usable placed home objects + `use <item_id>` commands
- `hearthstone` = Teleport home with Hearthstone
- `leave` / `exit home` = Leave your home
- `place <item> [at x y]` = Place a home item
- `remove <item>` = Remove placed home item
- `home inventory` = List placed home items
- `home upgrades` = Show expansion unlock status
- `rename home <name>` = Rename your home

## Debug Home Commands

- `debug home free` = Instantly grant home ownership
- `debug home items` = Add one copy of every home item
- `debug home reset` = Full home wipe (ownership/layout/upgrades/bonuses)

## Inspect Command

### General Usage
```
inspect <target>
```

### Available Targets

#### Walls (Secret Discovery!)
```
> inspect wall
```
- In boss rooms: May discover secret passages!
- Other rooms: Descriptive feedback about the walls

#### Chests
```
> inspect chest
```
- Shows chest type (wooden, golden, etc.)
- Shows lock status
- Reminds you how to open it

#### Ground/Floor
```
> inspect ground
> inspect floor
```
- Detects items on the ground
- Provides hint to use 'look' for details

#### Traps
```
> inspect trap
```
- Identifies visible traps
- Shows trap type
- Suggests how to disarm

#### Items
```
> inspect <item_name>
```
- Shows quantity and value
- Helpful for inventory management

## Contextual Hints

When you type `help` or `commands`, you'll see hints based on your current room:

- **[HINT]** - Secrets may be nearby!
- **[WARNING]** - Traps detected!
- **[LOOT]** - Items available!
- **[TREASURE]** - Chest present!
- **[EXIT]** - Special exits available!

## Secret Room Discovery

In boss rooms:
1. Type `inspect wall` or `examine wall`
2. If a secret exists, you'll see dramatic ASCII art discovery
3. A secret exit will be added
4. Type `go secret` to enter the hidden chamber

## Example Session

```
> help
[Shows comprehensive command list organized by category]

> n
[Quick move north]

> inspect wall
You carefully examine the walls.
Wait... one section seems different!
*CLICK*
✨ A SECRET PASSAGE HAS BEEN REVEALED! ✨

> go secret
[Enters secret chamber with ASCII art]

> look
[Shows room description with legendary items]

> inspect chest
You inspect the chest closely.
It's a golden chest, securely locked.
Type 'open chest' to attempt to open it.

> open chest
[Opens chest and shows contents]
```

## Tips

- Commands are **not case-sensitive**
- Use single-letter shortcuts (n/s/e/w) for quick navigation
- **Always inspect walls in boss rooms** - they often hide secrets!
- Check `help` frequently - it shows context-specific commands
- The help system adapts to show dungeon/shop commands when relevant
