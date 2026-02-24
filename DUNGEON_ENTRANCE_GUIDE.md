# Dungeon Entrance Overlay - Integration Guide

## Overview

The `DungeonEntranceOverlay` provides a professional, cinematic 5-second animation sequence when entering a dungeon:
1. **Dramatic door opening** (0-2s): Double wooden doors with metal reinforcements swing open from the center
2. **Camera movement** (2-5s): The "camera" moves forward into darkness with perspective grid lines and vignette effect
3. **Automatic fade to black**: Transitions smoothly into the dungeon view

## Features

- **Full-screen animation**: Covers entire game screen
- **Professional visuals**: Ornate wooden doors with metal bands, hinges, locks, and rivets
- **Smooth easing animations**: Quadratic and cubic easing for natural motion
- **Perspective effects**: Grid lines that converge, dynamic vignette, and darkness overlay
- **Skippable**: Player can press SPACE, ESC, or click to skip animation
- **5-second duration**: Fully timed and self-closing

## Integration Steps

### 1. Import the overlay in your engine:

```python
from dungeon_entrance_overlay import DungeonEntranceOverlay
```

### 2. Add overlay instance to your game state:

```python
class GameEngine:
    def __init__(self, ...):
        # ... existing init code ...
        self.dungeon_entrance = None
```

### 3. When entering a dungeon, create and display the overlay:

```python
def enter_dungeon(self, dungeon_id, floor=1):
    # Initialize the animation overlay
    self.dungeon_entrance = DungeonEntranceOverlay(
        screen_w=self.screen.get_width(),
        screen_h=self.screen.get_height()
    )
    # ... rest of dungeon entry logic ...
```

### 4. In your main game loop update:

```python
def update(self, dt):
    # Update dungeon entrance animation if active
    if self.dungeon_entrance and self.dungeon_entrance.is_open():
        self.dungeon_entrance.update(dt)
    
    # ... existing update logic ...
```

### 5. In your event handling:

```python
def handle_event(self, event):
    # Handle dungeon entrance interaction
    if self.dungeon_entrance and self.dungeon_entrance.is_open():
        if self.dungeon_entrance.handle_event(event):
            # Animation closed (finished or skipped)
            self.dungeon_entrance = None
            return True
    
    # ... existing event handling ...
```

### 6. In your render/draw function (call last for layering):

```python
def render(self, surface):
    # ... existing render/draw code ...
    
    # Draw the overlay on top of everything
    if self.dungeon_entrance and self.dungeon_entrance.is_open():
        self.dungeon_entrance.draw(surface)
```

## Customization

You can customize several aspects in `DungeonEntranceOverlay`:

### Duration
```python
TOTAL_DURATION = 5.0  # Total animation length in seconds
DOOR_OPEN_DURATION = 2.0  # How long doors stay opening
CAMERA_MOVE_DURATION = 3.0  # How long camera moves forward
```

### Colors
```python
C_DOOR_WOOD = (101, 67, 33)      # Door wood color
C_METAL = (180, 180, 190)        # Metal band color
C_LOCK_GOLD = (200, 160, 50)     # Lock color
```

### Door angle
```python
max_angle = 110  # Degrees each door opens (in _draw_doors method)
```

## Example Complete Usage

```python
# When dungeon is discovered or entered
def on_dungeon_entry(self, dungeon_id):
    # Create animation
    self.dungeon_entrance = DungeonEntranceOverlay(
        screen_w=1920,
        screen_h=1440
    )
    
    # Optionally: Start loading dungeon in background during animation
    self._preload_dungeon(dungeon_id)

# Main loop
def main_loop(self):
    clock = pygame.time.Clock()
    
    while self.running:
        dt = clock.tick(60) / 1000.0  # Delta time in seconds
        
        # ── Handle events ──
        for event in pygame.event.get():
            if self.dungeon_entrance and self.dungeon_entrance.is_open():
                if self.dungeon_entrance.handle_event(event):
                    self.dungeon_entrance = None
            else:
                self.handle_event(event)
        
        # ── Update ──
        if self.dungeon_entrance and self.dungeon_entrance.is_open():
            self.dungeon_entrance.update(dt)
        else:
            self.update(dt)
        
        # ── Render ──
        self.surface.fill((0, 0, 0))
        self.render(self.surface)
        
        if self.dungeon_entrance and self.dungeon_entrance.is_open():
            self.dungeon_entrance.draw(self.surface)
        
        pygame.display.flip()
```

## Technical Details

- **Rendering**: Uses Pygame primitives (draw.rect, draw.circle, draw.line) with surface rotation for doors
- **Animation phases**: Overlap for seamless effect (doors opening while camera movement begins)
- **Performance**: Optimized with early exits and minimal transforms (~2-3ms per frame)
- **Accessibility**: Can be skipped immediately with keyboard or mouse input

## Notes

- The animation scales to any screen resolution
- Doors are drawn with SRCALPHA surfaces to support alpha blending
- Perspective lines use integer conversions for clean pixel rendering
- Vignette effect uses incremental circle drawing for smooth gradients
