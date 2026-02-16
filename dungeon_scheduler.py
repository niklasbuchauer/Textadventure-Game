"""
Dungeon Time-Gating System
Manages dungeon opening/closing schedule based on Germany timezone.
Dungeon opens every 3 hours for 1 hour duration.
"""

import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError  # Modern replacement for pytz (Python 3.9+)


class DungeonScheduler:
    """
    Manages the time-gated dungeon schedule.
    Dungeon opens: 00:00, 03:00, 06:00, 09:00, 12:00, 15:00, 18:00, 21:00 (Germany time)
    Each opening lasts 1 hour.
    """
    
    def __init__(self, game_engine=None):
        """
        Initialize scheduler.
        
        Args:
            game_engine: Optional reference to GameEngine for debug overrides
        """
        self.game_engine = game_engine
        
        # Try to use timezone-aware datetimes, fall back to naive UTC if tzdata unavailable
        self.timezone = None
        self.timezone_name = 'UTC (no tzdata)'
        self.using_fallback = False
        
        # First, try Europe/Berlin (ideal)
        try:
            self.timezone = ZoneInfo('Europe/Berlin')
            self.timezone_name = 'Europe/Berlin'
        except (ZoneInfoNotFoundError, Exception):
            # Europe/Berlin not available, try UTC with zoneinfo
            try:
                self.timezone = ZoneInfo('UTC')
                self.timezone_name = 'UTC (zoneinfo)'
                self.using_fallback = True
            except (ZoneInfoNotFoundError, Exception):
                # zoneinfo/tzdata not available at all - use naive UTC
                # This is OK - we'll just use datetime.utcnow() without timezone info
                self.timezone = None
                self.timezone_name = 'UTC (naive - tzdata not installed)'
                self.using_fallback = True
                print(
                    "[WARNING] Timezone data (tzdata) not available on this system.\n"
                    "          Using UTC for dungeon scheduling.\n"
                    "          To fix: pip install --force-reinstall tzdata"
                )
        
        self.open_duration_hours = 1
        self.cycle_duration_hours = 3
        self.open_hours = [0, 3, 6, 9, 12, 15, 18, 21]
    
    def _get_current_time(self):
        """
        Get current time using either timezone-aware datetime or system local time.
        
        Returns:
            datetime.datetime: Current time (timezone-aware if tzdata available, 
                             local system time otherwise)
        """
        if self.timezone is not None:
            # Use timezone-aware datetime
            return datetime.datetime.now(self.timezone)
        else:
            # Use system local time (naive datetime) when tzdata not available
            # This is better than UTC since user's system clock is in local time
            return datetime.datetime.now()
    
    def is_dungeon_open(self, dungeon_id=None):
        """
        Checks if dungeon is currently open based on Germany time (or UTC if tzdata unavailable).
        Also checks debug force-open overrides if a dungeon_id is provided.
        
        Args:
            dungeon_id: Optional dungeon ID to check for debug override
            
        Returns:
            bool: True if dungeon is open (by schedule OR debug override), False if closed
        """
        # CRITICAL: Check debug override FIRST
        if dungeon_id and self.game_engine:
            if hasattr(self.game_engine, 'debug_force_open_dungeons'):
                if dungeon_id in self.game_engine.debug_force_open_dungeons:
                    return True  # Force-opened by debug command
        
        # Normal time-based check
        now = self._get_current_time()
        current_hour = now.hour
        
        return current_hour in self.open_hours
    
    def get_time_until_next_opening(self):
        """
        Returns time remaining until dungeon opens next.
        
        Returns:
            tuple: (hours, minutes) until next opening
            str: Human-readable time (e.g., "2 hours 15 minutes")
        """
        now = self._get_current_time()
        current_hour = now.hour
        current_minute = now.minute
        current_second = now.second
        
        # Find next opening hour
        next_opening = None
        for hour in self.open_hours:
            if hour > current_hour:
                next_opening = hour
                break
        
        if next_opening is None:
            # Next opening is tomorrow at 00:00
            next_opening = self.open_hours[0]
            hours_until = (24 - current_hour - 1) + 1
            minutes_until = 60 - current_minute
        else:
            hours_until = next_opening - current_hour - 1
            minutes_until = 60 - current_minute
        
        if minutes_until == 60:
            hours_until += 1
            minutes_until = 0
        
        time_str = f"{hours_until} hours {minutes_until} minutes" if hours_until > 0 else f"{minutes_until} minutes"
        
        return (hours_until, minutes_until), time_str
    
    def get_time_until_closing(self):
        """
        Returns time remaining until dungeon closes (if currently open).
        
        Returns:
            tuple: (hours, minutes) until closing
            str: Human-readable time
        """
        if not self.is_dungeon_open():
            return None, "Dungeon is closed"
        
        now = self._get_current_time()
        current_minute = now.minute
        current_second = now.second
        
        minutes_until = 60 - current_minute - 1
        hours_until = 0
        
        if minutes_until < 0:
            minutes_until += 60
            hours_until = -1
        
        # If very close to hour boundary, round up slightly
        if minutes_until < 0:
            minutes_until = 0
            hours_until = 0
        
        # More accurate: minutes from now until next hour
        minutes_until = 59 - current_minute
        
        time_str = f"{minutes_until} minutes"
        
        return (hours_until, minutes_until), time_str
    
    def get_current_dungeon_seed(self):
        """
        Returns a unique seed for current dungeon instance.
        Changes each time dungeon opens (every 3 hours).
        Seed format: YYYYMMDD_HH (where HH is opening hour: 00, 03, 06, etc.)
        
        Returns:
            int: Seed for random generation
        """
        now = self._get_current_time()
        
        # Create seed based on date and opening cycle
        date_str = now.strftime("%Y%m%d")
        
        # Determine which 3-hour cycle we're in
        cycle_hour = (now.hour // 3) * 3
        
        seed = int(f"{date_str}{cycle_hour:02d}")
        
        return seed
    
    def get_status_message(self):
        """
        Returns a formatted status message about dungeon availability.
        
        Returns:
            str: Status message
        """
        if self.is_dungeon_open():
            _, time_str = self.get_time_until_closing()
            return f"[OPEN] DUNGEON OPEN - Closes in {time_str}"
        else:
            _, time_str = self.get_time_until_next_opening()
            return f"[CLOSED] DUNGEON CLOSED - Opens in {time_str}"
    
    def get_next_opening_time(self):
        """
        Returns when the dungeon will next open.
        
        Returns:
            str: Formatted time string (e.g., "03:00")
        """
        now = self._get_current_time()
        current_hour = now.hour
        
        next_opening = None
        for hour in self.open_hours:
            if hour > current_hour:
                next_opening = hour
                break
        
        if next_opening is None:
            next_opening = self.open_hours[0]
        
        return f"{next_opening:02d}:00"
    
    def get_schedule_text(self):
        """
        Returns formatted schedule of dungeon opening times.
        
        Returns:
            str: Formatted schedule
        """
        schedule = """
╔════════════════════════════════════╗
║    DUNGEON SCHEDULE (Germany Time)  ║
╠════════════════════════════════════╣
║  00:00 - 01:00 OPEN                 ║
║  03:00 - 04:00 OPEN                 ║
║  06:00 - 07:00 OPEN                 ║
║  09:00 - 10:00 OPEN                 ║
║  12:00 - 13:00 OPEN                 ║
║  15:00 - 16:00 OPEN                 ║
║  18:00 - 19:00 OPEN                 ║
║  21:00 - 22:00 OPEN                 ║
╚════════════════════════════════════╝
        """
        return schedule

    def to_dict(self):
        """
        Serialize dungeon scheduler state for saving.
        Most state is derived from current time, so we only save debug overrides.
        """
        data = {}
        # Save debug force-open overrides if they exist
        if self.game_engine and hasattr(self.game_engine, 'debug_force_open_dungeons'):
            data["debug_force_open"] = list(self.game_engine.debug_force_open_dungeons)
        return data

    def load_from_dict(self, data):
        """
        Restore dungeon scheduler state from saved data.
        Restores debug force-open overrides.
        """
        if isinstance(data, dict):
            # Restore debug overrides
            debug_open = data.get("debug_force_open", [])
            if debug_open and self.game_engine:
                if not hasattr(self.game_engine, 'debug_force_open_dungeons'):
                    self.game_engine.debug_force_open_dungeons = set()
                self.game_engine.debug_force_open_dungeons.update(debug_open)


# Global scheduler instance
_global_scheduler = None


def get_scheduler(game_engine=None):
    """Get or create global scheduler instance."""
    global _global_scheduler
    if _global_scheduler is None:
        _global_scheduler = DungeonScheduler(game_engine=game_engine)
    elif game_engine is not None and _global_scheduler.game_engine is None:
        _global_scheduler.game_engine = game_engine
    return _global_scheduler
