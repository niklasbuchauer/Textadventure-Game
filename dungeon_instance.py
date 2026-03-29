"""
Active Dungeon Instance Manager
Manages individual dungeon instances, player tracking, and dungeon closure.
"""

import datetime
from dungeon_scheduler import DungeonScheduler
from dungeon_generator import DungeonGenerator


class DungeonInstance:
    """
    Represents an active dungeon instance.
    Handles player tracking, dungeon generation, and auto-closure.
    """
    
    def __init__(self, seed, scheduler=None, dungeon_id=None, entrance_room_id=None):
        """
        Initialize a dungeon instance.
        
        Args:
            seed: Random seed for generation
            scheduler: DungeonScheduler instance (creates if None)
            dungeon_id: Optional dungeon ID (used to check debug overrides)
            entrance_room_id: The overworld room ID to exit to when leaving the dungeon
        """
        self.seed = seed
        self.scheduler = scheduler or DungeonScheduler()
        self.dungeon_id = dungeon_id  # For debug override checks
        self.entrance_room_id = entrance_room_id or "dungeon_forest_entrance"
        # Handle both timezone-aware and local time datetimes
        if self.scheduler.timezone is not None:
            self.generated_at = datetime.datetime.now(self.scheduler.timezone)
        else:
            self.generated_at = datetime.datetime.now()
        self.players_inside = []
        self.dungeon_data = None
        self.active = True
        self.generator = DungeonGenerator(seed)
        
        # Generate the dungeon (seed is passed to generate_complete_dungeon)
        self.dungeon_data = self.generator.generate_complete_dungeon(
            seed,
            entrance_room_id=self.entrance_room_id,
            dungeon_id=self.dungeon_id,
        )
    
    def add_player(self, player):
        """
        Add a player to the dungeon.
        
        Args:
            player: Player object to add
        """
        if player not in self.players_inside:
            self.players_inside.append(player)
    
    def remove_player(self, player):
        """
        Remove a player from the dungeon.
        
        Args:
            player: Player object to remove
        """
        if player in self.players_inside:
            self.players_inside.remove(player)
    
    def is_valid(self):
        """
        Check if this is the current valid dungeon instance.
        Becomes invalid when dungeon closes or a new seed is issued.
        Checks debug override if dungeon_id is set.
        
        Returns:
            bool: True if still valid
        """
        return self.active and self.scheduler.is_dungeon_open(dungeon_id=self.dungeon_id)
    
    def check_if_should_close(self):
        """
        Checks if dungeon should close based on time.
        Called periodically or when player takes action.
        
        Returns:
            bool: True if dungeon should close
        """
        if not self.scheduler.is_dungeon_open():
            self.close_dungeon()
            return True
        return False
    
    def close_dungeon(self):
        """
        Closes dungeon and teleports all players out.
        Also triggers engine cleanup if the engine reference is available.
        """
        self.active = False
        
        message = "\n" + "="*60 + "\n"
        message += "⚠ THE DUNGEON IS CLOSING! ⚠\n"
        message += "="*60 + "\n"
        message += "The magical energy shifts! The dungeon begins collapsing!\n"
        message += "You are being teleported to safety...\n"
        message += "="*60 + "\n"
        
        # Teleport all players to the forest entrance (safe location outside dungeon)
        for player in list(self.players_inside):
            self.teleport_player_out(player)
        
        # Trigger engine cleanup (removes dungeon rooms, updates map)
        engine = getattr(self.scheduler, 'game_engine', None)
        if engine and hasattr(engine, 'cleanup_dungeon'):
            engine.cleanup_dungeon()
        
        # Clear dungeon data
        self.dungeon_data = None
        self.players_inside = []
    
    def teleport_player_out(self, player):
        """
        Teleports player back to dungeon entrance (outside).
        
        Args:
            player: Player to teleport
        """
        if hasattr(player, 'current_room'):
            player.current_room = self.entrance_room_id
        if hasattr(player, 'current_map'):
            player.current_map = "world"
        
        # Return the teleport message
        message = "\nYou appear outside the cave entrance, slightly dizzy.\n"
        message += "The dungeon has sealed itself once more.\n"
        
        return message
    
    def warning_before_close(self, minutes_remaining):
        """
        Generates warning messages for players before dungeon closes.
        
        Args:
            minutes_remaining: Minutes until closure
            
        Returns:
            str: Warning message if applicable
        """
        if minutes_remaining == 10:
            return "\n⚠ WARNING: Dungeon closing in 10 minutes! ⚠\n"
        elif minutes_remaining == 5:
            return "\n⚠ WARNING: Dungeon closing in 5 minutes! ⚠\n"
        elif minutes_remaining == 1:
            return "\n⚠ URGENT: Dungeon closing in 1 minute! Leave now! ⚠\n"
        
        return None
    
    def get_room(self, floor, room_name):
        """
        Get a room from the dungeon.
        
        Args:
            floor: Floor number (1-4)
            room_name: Room ID
            
        Returns:
            dict: Room data or None if not found
        """
        if not self.dungeon_data or not self.active:
            return None
        
        floors = self.dungeon_data.get("floors", {})
        floor_data = floors.get(floor, {})
        rooms = floor_data.get("rooms", {})

        room = rooms.get(room_name)
        if room:
            return room

        # Backward-compat: allow legacy IDs like "floor1_room1" (without dungeon_<seed>_ prefix)
        if not room_name.startswith("dungeon_"):
            compat_name = f"dungeon_{self.seed}_{room_name}"
            room = rooms.get(compat_name)
            if room:
                return room
            # As a final fallback, match by suffix to tolerate varied prefixes
            for rid, rdata in rooms.items():
                if rid.endswith(room_name):
                    return rdata

        return None
    
    def get_floor_rooms(self, floor):
        """
        Get all rooms on a floor.
        
        Args:
            floor: Floor number (1-4)
            
        Returns:
            dict: All rooms on that floor
        """
        if not self.dungeon_data or not self.active:
            return {}
        
        floors = self.dungeon_data.get("floors", {})
        floor_data = floors.get(floor, {})
        
        return floor_data.get("rooms", {})
    
    def get_entrance_room(self, floor):
        """
        Get the entrance room for a floor.
        
        Args:
            floor: Floor number (1-4)
            
        Returns:
            str: Room ID of entrance
        """
        if not self.dungeon_data or not self.active:
            return None
        
        floors = self.dungeon_data.get("floors", {})
        floor_data = floors.get(floor, {})
        
        return floor_data.get("entrance_room")
    
    def get_dungeon_info(self):
        """
        Get basic info about this dungeon instance.
        
        Returns:
            dict: Dungeon info
        """
        return {
            "seed": self.seed,
            "generated_at": self.generated_at.isoformat(),
            "num_floors": self.dungeon_data.get("num_floors", 0) if self.dungeon_data else 0,
            "players_inside": len(self.players_inside),
            "active": self.active
        }


# Global dungeon instance holder
_current_dungeon = None
_current_seed = None


def get_current_dungeon(scheduler, entrance_room_id=None):
    """
    Get or create the current dungeon instance.
    Returns new dungeon if seed has changed.
    
    Args:
        scheduler: DungeonScheduler instance
        entrance_room_id: The overworld room ID to exit to when leaving
        
    Returns:
        DungeonInstance: Current dungeon or None if closed
    """
    global _current_dungeon, _current_seed
    
    current_seed = scheduler.get_current_dungeon_seed()
    
    # If seed changed, need new dungeon
    if current_seed != _current_seed or _current_dungeon is None or not _current_dungeon.is_valid():
        _current_dungeon = DungeonInstance(current_seed, scheduler, entrance_room_id=entrance_room_id)
        _current_seed = current_seed
    
    return _current_dungeon


def close_current_dungeon():
    """
    Close the current dungeon instance.
    """
    global _current_dungeon
    
    if _current_dungeon:
        _current_dungeon.close_dungeon()
        _current_dungeon = None


def set_current_dungeon(dungeon_instance, seed):
    """
    Directly set the current dungeon instance and seed (for debug purposes).
    
    Args:
        dungeon_instance: DungeonInstance to set as current
        seed: The seed used for this dungeon
    """
    global _current_dungeon, _current_seed
    _current_dungeon = dungeon_instance
    _current_seed = seed

