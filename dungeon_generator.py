"""
Procedural Dungeon Generation System
Generates multi-floor dungeons with non-linear layouts, loot, chests, traps,
bidirectional stairs, surface exit, and a boss/treasure vault on the final floor.
"""

import random
import datetime
from trap_system import TrapSystem


# ── Room Templates ──────────────────────────────────────────────────

ROOM_TEMPLATES = {
    # High Quality
    "treasury_vault": {
        "name": "Collapsed Treasury Vault",
        "entry_description": "A massive vault door lies broken on the ground. Gleaming treasures glint in the darkness.",
        "chest_spawn_chance": 0.35,
        "item_spawn_count": (3, 6)
    },
    "dark_altar": {
        "name": "Dark Altar Chamber",
        "entry_description": "An ancient altar dominates the room, stained with centuries of ritual.",
        "chest_spawn_chance": 0.40,
        "item_spawn_count": (3, 5)
    },
    "throne_room": {
        "name": "Ruined Throne Room",
        "entry_description": "A massive throne sits upon a crumbling dais, surrounded by faded tapestries.",
        "chest_spawn_chance": 0.45,
        "item_spawn_count": (4, 6)
    },
    "hidden_vault": {
        "name": "Hidden Vault",
        "entry_description": "An impossibly well-preserved chamber reveals why - it was sealed for centuries.",
        "chest_spawn_chance": 0.50,
        "item_spawn_count": (4, 7)
    },
    "spell_scriptorium": {
        "name": "Spell Scriptorium",
        "entry_description": "Shelves of dusty tomes and scattered parchments cover every surface.",
        "chest_spawn_chance": 0.32,
        "item_spawn_count": (3, 5)
    },
    "map_chamber": {
        "name": "Map Chamber",
        "entry_description": "Old maps and charts line the walls, detailing long-forgotten lands.",
        "chest_spawn_chance": 0.28,
        "item_spawn_count": (2, 4)
    },

    # Medium Quality
    "ancient_armory": {
        "name": "Ancient Armory",
        "entry_description": "Rusted weapons line crumbling stone walls. The air reeks of old metal and decay.",
        "chest_spawn_chance": 0.15,
        "item_spawn_count": (2, 4)
    },
    "torture_chamber": {
        "name": "Chamber of Torment",
        "entry_description": "Dark stains cover the walls and floor. You'd rather not think about what happened here.",
        "chest_spawn_chance": 0.08,
        "item_spawn_count": (2, 3)
    },
    "smithy": {
        "name": "Underground Smithy",
        "entry_description": "A forge still radiates faint warmth. Tools and metal scraps litter the workbench.",
        "chest_spawn_chance": 0.20,
        "item_spawn_count": (2, 4)
    },
    "guard_barracks": {
        "name": "Guard Barracks",
        "entry_description": "Rows of bunk beds line the walls, long abandoned.",
        "chest_spawn_chance": 0.15,
        "item_spawn_count": (2, 4)
    },
    "storage_vault": {
        "name": "Storage Vault",
        "entry_description": "Wooden shelves and stone ledges hold forgotten supplies.",
        "chest_spawn_chance": 0.22,
        "item_spawn_count": (3, 5)
    },
    "ritual_chamber": {
        "name": "Ritual Chamber",
        "entry_description": "Strange markings cover the ground in intricate patterns.",
        "chest_spawn_chance": 0.38,
        "item_spawn_count": (3, 5)
    },
    "warden_office": {
        "name": "Warden's Office",
        "entry_description": "A dusty desk and filing cabinets suggest this was once a place of authority.",
        "chest_spawn_chance": 0.30,
        "item_spawn_count": (2, 3)
    },
    "execution_chamber": {
        "name": "Execution Chamber",
        "entry_description": "Stone shackles hang from the walls. An execution block sits in the center.",
        "chest_spawn_chance": 0.12,
        "item_spawn_count": (2, 4)
    },
    "wine_cellar": {
        "name": "Ancient Wine Cellar",
        "entry_description": "Wine racks line the walls, holding bottles too old and precious to ever drink.",
        "chest_spawn_chance": 0.18,
        "item_spawn_count": (2, 4)
    },
    "chapel": {
        "name": "Desecrated Chapel",
        "entry_description": "An altar lies toppled, surrounded by broken religious artifacts.",
        "chest_spawn_chance": 0.15,
        "item_spawn_count": (1, 3)
    },
    "trophy_hall": {
        "name": "Trophy Hall",
        "entry_description": "Mounted weapons and armor adorn the walls, trophies of past conquests.",
        "chest_spawn_chance": 0.25,
        "item_spawn_count": (2, 4)
    },

    # Low Quality
    "library": {
        "name": "Forgotten Library",
        "entry_description": "Moldy books line countless shelves, their pages crumbling to dust.",
        "chest_spawn_chance": 0.12,
        "item_spawn_count": (1, 3)
    },
    "crypt": {
        "name": "Musty Burial Crypt",
        "entry_description": "Stone sarcophagi line the walls, their occupants long undisturbed.",
        "chest_spawn_chance": 0.18,
        "item_spawn_count": (1, 4)
    },
    "prison_block": {
        "name": "Abandoned Prison Block",
        "entry_description": "Iron bars rust on their hinges. Some cells still hold remnants of unfortunate prisoners.",
        "chest_spawn_chance": 0.05,
        "item_spawn_count": (1, 2)
    },
    "well_chamber": {
        "name": "Underground Well Room",
        "entry_description": "A massive well dominates the chamber, its depths lost to darkness.",
        "chest_spawn_chance": 0.10,
        "item_spawn_count": (1, 2)
    },
    "dining_hall": {
        "name": "Great Dining Hall",
        "entry_description": "Long tables gather dust. Decaying food still sits on some plates.",
        "chest_spawn_chance": 0.08,
        "item_spawn_count": (1, 3)
    },
    "sewer_junction": {
        "name": "Flooded Sewer Junction",
        "entry_description": "Foul water runs through grooves in the stone floor. The smell is overwhelming.",
        "chest_spawn_chance": 0.05,
        "item_spawn_count": (1, 2)
    },
    "collapsed_tunnel": {
        "name": "Collapsed Tunnel",
        "entry_description": "Part of the tunnel has caved in, leaving a precarious path through the rubble.",
        "chest_spawn_chance": 0.10,
        "item_spawn_count": (1, 3)
    },
    "guardhouse": {
        "name": "Guardhouse Station",
        "entry_description": "A small station where guards would rest between shifts.",
        "chest_spawn_chance": 0.10,
        "item_spawn_count": (1, 3)
    },
    "training_grounds": {
        "name": "Training Grounds",
        "entry_description": "Training dummies stand in rows, their surfaces scarred from countless practice blows.",
        "chest_spawn_chance": 0.08,
        "item_spawn_count": (2, 3)
    }
}

# ── Chest Templates ────────────────────────────────────────────────

CHEST_TEMPLATES = {
    "wooden_chest": {
        "name": "Wooden Chest",
        "item_count": (2, 4),
        "gold_bonus": (10, 40),
        "rarity_weights": {"common": 0.6, "uncommon": 0.35, "rare": 0.05, "epic": 0.0}
    },
    "iron_chest": {
        "name": "Iron-Bound Chest",
        "item_count": (3, 6),
        "gold_bonus": (40, 100),
        "rarity_weights": {"common": 0.3, "uncommon": 0.5, "rare": 0.15, "epic": 0.05}
    },
    "ornate_chest": {
        "name": "Ornate Chest",
        "item_count": (4, 8),
        "gold_bonus": (80, 200),
        "rarity_weights": {"common": 0.1, "uncommon": 0.3, "rare": 0.4, "epic": 0.2}
    }
}

# ── Item Database ──────────────────────────────────────────────────

ITEM_DATABASE = {
    # Low tier
    "rusty_dagger": {"value": 5, "tier": "low"},
    "old_boot": {"value": 2, "tier": "low"},
    "torch": {"value": 3, "tier": "low"},
    "broken_chain": {"value": 4, "tier": "low"},
    "moldy_bread": {"value": 1, "tier": "low"},
    "cracked_skull": {"value": 6, "tier": "low"},
    "torn_cloth": {"value": 2, "tier": "low"},
    "bent_fork": {"value": 3, "tier": "low"},
    "empty_bottle": {"value": 2, "tier": "low"},
    "rat_pelt": {"value": 4, "tier": "low"},
    # Medium tier
    "iron_sword": {"value": 30, "tier": "medium"},
    "leather_armor_piece": {"value": 25, "tier": "medium"},
    "silver_ring": {"value": 40, "tier": "medium"},
    "healing_salve": {"value": 35, "tier": "medium"},
    "quality_torch": {"value": 15, "tier": "medium"},
    "lockpick_set": {"value": 50, "tier": "medium"},
    "coin_pouch": {"value": 20, "tier": "medium"},
    "steel_dagger": {"value": 35, "tier": "medium"},
    "worn_map": {"value": 45, "tier": "medium"},
    "craftsman_hammer": {"value": 38, "tier": "medium"},
    "enchanted_candle": {"value": 55, "tier": "medium"},
    "ancient_coin": {"value": 60, "tier": "medium"},
    "rope_coil": {"value": 20, "tier": "medium"},
    "iron_key": {"value": 25, "tier": "medium"},
    # High tier
    "gold_chalice": {"value": 100, "tier": "high"},
    "enchanted_ring": {"value": 120, "tier": "high"},
    "steel_longsword": {"value": 110, "tier": "high"},
    "healing_potion": {"value": 85, "tier": "high"},
    "spell_scroll": {"value": 95, "tier": "high"},
    "jeweled_dagger": {"value": 105, "tier": "high"},
    "magic_amulet": {"value": 130, "tier": "high"},
    "royal_signet": {"value": 140, "tier": "high"},
    "masterwork_shield": {"value": 125, "tier": "high"},
    "ancient_tome": {"value": 115, "tier": "high"},
    "platinum_bar": {"value": 150, "tier": "high"},
    "rare_gemstone": {"value": 145, "tier": "high"},
    "enchanted_cloak_fragment": {"value": 135, "tier": "high"},
}


# ====================================================================
#  Dungeon Generator
# ====================================================================

class DungeonGenerator:
    """
    Procedurally generates multi-floor dungeons with:
      - Non-linear layouts (branching, grid, maze)
      - 20-30 rooms per floor (floor 1), scaling down on deeper floors
      - Bidirectional exits (can go back)
      - Stairs up AND down between floors
      - "leave" exit on floor 1 entrance to return to surface
      - Boss / treasure vault on the final floor
      - Traps placed during generation
    """

    def __init__(self, seed=None):
        """
        Args:
            seed: Optional random seed (kept for backward compat).
                  The actual seed is applied in generate_complete_dungeon().
        """
        self._ctor_seed = seed

        # Room-type quality pools
        self.high_quality_rooms = [
            "treasury_vault", "dark_altar", "throne_room",
            "hidden_vault", "spell_scriptorium", "map_chamber",
        ]
        self.medium_quality_rooms = [
            "ancient_armory", "torture_chamber", "smithy",
            "guard_barracks", "storage_vault", "ritual_chamber",
            "warden_office", "execution_chamber", "wine_cellar",
            "chapel", "trophy_hall",
        ]
        self.low_quality_rooms = [
            "library", "crypt", "prison_block", "well_chamber",
            "dining_hall", "sewer_junction", "collapsed_tunnel",
            "guardhouse", "training_grounds",
        ]

        self.trap_system = TrapSystem()

    # ── public entry-point ──────────────────────────────────────────

    def generate_complete_dungeon(self, seed=None, entrance_room_id=None):
        """
        Generate an entire multi-floor dungeon.

        Args:
            seed: Random seed.  Falls back to the constructor seed if None.
            entrance_room_id: The overworld room ID to exit to (e.g. 'dungeon_forest_entrance').
                              Falls back to 'dungeon_forest_entrance' if None.

        Returns:
            dict: Complete dungeon data.
        """
        seed = seed or self._ctor_seed or int(datetime.datetime.now().strftime("%Y%m%d%H"))
        random.seed(seed)

        print(f"[DungeonGenerator] Generating dungeon with seed: {seed}")

        num_floors = random.randint(2, 4)
        print(f"[DungeonGenerator] Creating {num_floors} floors")

        dungeon_data = {
            "seed": seed,
            "generated_at": datetime.datetime.now().isoformat(),
            "num_floors": num_floors,
            "floors": {},
        }

        # Determine room counts per floor (MUCH larger)
        rooms_per_floor = {}
        for f in range(1, num_floors + 1):
            if f == 1:
                rooms_per_floor[f] = random.randint(20, 30)
            elif f == 2:
                rooms_per_floor[f] = random.randint(15, 25)
            elif f == 3:
                rooms_per_floor[f] = random.randint(12, 20)
            else:
                rooms_per_floor[f] = random.randint(8, 15)

        # Generate each floor
        for floor_num in range(1, num_floors + 1):
            num_rooms = rooms_per_floor[floor_num]
            is_final = (floor_num == num_floors)
            print(f"[DungeonGenerator] Floor {floor_num}: {num_rooms} rooms (final={is_final})")

            floor_data = self._generate_floor(
                floor_num, num_rooms, seed, is_final, num_floors
            )
            dungeon_data["floors"][floor_num] = floor_data

        # ── cross-floor stair linking ───────────────────────────────
        self._link_stairs_across_floors(dungeon_data)

        # ── surface exit on floor 1 ────────────────────────────────
        self._add_surface_exit(dungeon_data, entrance_room_id=entrance_room_id)

        print("[DungeonGenerator] Dungeon generation complete!")
        return dungeon_data

    # ── floor generation ────────────────────────────────────────────

    def _generate_floor(self, floor_number, num_rooms, seed, is_final, total_floors):
        """Generate a single floor with rooms, layout, and traps."""

        quality_weights = {
            1: {"low": 0.50, "medium": 0.40, "high": 0.10},
            2: {"low": 0.30, "medium": 0.50, "high": 0.20},
            3: {"low": 0.15, "medium": 0.50, "high": 0.35},
            4: {"low": 0.05, "medium": 0.40, "high": 0.55},
        }.get(floor_number, {"low": 0.30, "medium": 0.40, "high": 0.30})

        floor_data = {
            "floor_number": floor_number,
            "num_rooms": num_rooms,
            "rooms": {},
            "entrance_room": None,
            "exit_stairs_up": None,
            "exit_stairs_down": None,
            "boss_room": None,
        }

        # Create rooms
        for i in range(num_rooms):
            room_id = f"dungeon_{seed}_floor{floor_number}_room{i + 1}"

            quality = random.choices(
                ["low", "medium", "high"],
                weights=[quality_weights["low"], quality_weights["medium"], quality_weights["high"]],
            )[0]
            room_type = self._select_room_type(quality)
            room = self._create_room(room_id, room_type, quality, floor_number)
            floor_data["rooms"][room_id] = room

        room_ids = list(floor_data["rooms"].keys())

        # Choose and apply layout
        layout = random.choice(["branching", "grid", "maze"])
        if layout == "branching":
            self._apply_branching_layout(floor_data, room_ids, floor_number, seed, is_final)
        elif layout == "grid":
            self._apply_grid_layout(floor_data, room_ids, floor_number, seed, is_final)
        else:
            self._apply_maze_layout(floor_data, room_ids, floor_number, seed, is_final)

        # Add traps
        self.trap_system.add_traps_to_floor(floor_data, floor_number)

        # Add secret room on final floor
        if is_final:
            floor_data = self.add_secret_room(floor_data)

        return floor_data

    # ── layout helpers ──────────────────────────────────────────────

    def _apply_branching_layout(self, floor_data, room_ids, floor_number, seed, is_final):
        """Main corridor with branching side-rooms north/south."""

        rooms = floor_data["rooms"]
        floor_data["entrance_room"] = room_ids[0]

        # Split into main path and branches
        num_main = max(len(room_ids) // 2, 3)
        main_path = room_ids[:num_main]
        branch_pool = room_ids[num_main:]

        # Layout main path going east
        for i, rid in enumerate(main_path):
            rooms[rid]["coordinates"] = [i, 0]

        for i in range(len(main_path) - 1):
            cur, nxt = main_path[i], main_path[i + 1]
            rooms[cur]["exits"]["east"] = {"target": nxt, "type": "direction"}
            rooms[nxt]["exits"]["west"] = {"target": cur, "type": "direction"}

        # Attach branches to interior main-path rooms
        bi = 0
        for mi, mrid in enumerate(main_path[1:-1], 1):
            if bi >= len(branch_pool):
                break
            n_branches = random.randint(0, min(2, len(branch_pool) - bi))
            used_dirs = set()
            for _ in range(n_branches):
                if bi >= len(branch_pool):
                    break
                brid = branch_pool[bi]
                bi += 1

                direction = random.choice(["north", "south"])
                if direction in used_dirs:
                    direction = "south" if direction == "north" else "north"
                used_dirs.add(direction)

                y_off = 1 if direction == "north" else -1
                rooms[brid]["coordinates"] = [mi, y_off]

                opp = "south" if direction == "north" else "north"
                rooms[mrid]["exits"][direction] = {"target": brid, "type": "direction"}
                rooms[brid]["exits"][opp] = {"target": mrid, "type": "direction"}

                # Optionally chain another room off the branch
                if bi < len(branch_pool) and random.random() < 0.35:
                    brid2 = branch_pool[bi]
                    bi += 1
                    rooms[brid2]["coordinates"] = [mi, y_off * 2]
                    rooms[brid]["exits"][direction] = {"target": brid2, "type": "direction"}
                    rooms[brid2]["exits"][opp] = {"target": brid, "type": "direction"}

        # Place any remaining branch rooms
        while bi < len(branch_pool):
            brid = branch_pool[bi]
            bi += 1
            x = random.randint(1, len(main_path) - 2)
            y = random.choice([-2, -1, 1, 2])
            rooms[brid]["coordinates"] = [x, y]

            # Connect to nearest main-path room
            anchor = main_path[x]
            d = "north" if y > 0 else "south"
            od = "south" if y > 0 else "north"
            if d not in rooms[anchor]["exits"]:
                rooms[anchor]["exits"][d] = {"target": brid, "type": "direction"}
                rooms[brid]["exits"][od] = {"target": anchor, "type": "direction"}

        # Stairs & boss
        self._set_floor_endpoints(floor_data, main_path, floor_number, seed, is_final)
        
        # CRITICAL: Validate all rooms connected
        floor_data = self.ensure_all_rooms_connected(floor_data)
        
        return floor_data

    def _apply_grid_layout(self, floor_data, room_ids, floor_number, seed, is_final):
        """Rooms arranged on a 2-D grid with ~70 % of possible connections."""

        rooms = floor_data["rooms"]
        floor_data["entrance_room"] = room_ids[0]

        cols = int(len(room_ids) ** 0.5) + 1
        rows = (len(room_ids) + cols - 1) // cols

        # Assign grid coordinates
        idx = 0
        for row in range(rows):
            for col in range(cols):
                if idx >= len(room_ids):
                    break
                rooms[room_ids[idx]]["coordinates"] = [col, row]
                idx += 1

        # Build coordinate lookup
        coord2rid = {}
        for rid, rd in rooms.items():
            c = rd["coordinates"]
            coord2rid[(c[0], c[1])] = rid

        # Connect adjacent rooms (bidirectional, 70 % of links)
        dir_map = {"north": (0, 1), "south": (0, -1), "east": (1, 0), "west": (-1, 0)}
        opp_map = {"north": "south", "south": "north", "east": "west", "west": "east"}
        for rid, rd in rooms.items():
            x, y = rd["coordinates"]
            for d, (dx, dy) in dir_map.items():
                nxy = (x + dx, y + dy)
                nrid = coord2rid.get(nxy)
                if nrid and d not in rd["exits"] and random.random() < 0.70:
                    rd["exits"][d] = {"target": nrid, "type": "direction"}
                    rooms[nrid]["exits"][opp_map[d]] = {"target": rid, "type": "direction"}

        # Ensure graph is connected (BFS from entrance, connect isolated nodes)
        self._ensure_connected(rooms, room_ids, coord2rid)

        # Stairs & boss
        self._set_floor_endpoints(floor_data, room_ids, floor_number, seed, is_final)

        # Validate all rooms are connected
        floor_data = self.ensure_all_rooms_connected(floor_data)

        return floor_data

    def _apply_maze_layout(self, floor_data, room_ids, floor_number, seed, is_final):
        """Grid with lower connectivity (50 %) to feel maze-like."""

        rooms = floor_data["rooms"]
        floor_data["entrance_room"] = room_ids[0]

        cols = int(len(room_ids) ** 0.5) + 1
        rows = (len(room_ids) + cols - 1) // cols

        idx = 0
        for row in range(rows):
            for col in range(cols):
                if idx >= len(room_ids):
                    break
                rooms[room_ids[idx]]["coordinates"] = [col, row]
                idx += 1

        coord2rid = {}
        for rid, rd in rooms.items():
            c = rd["coordinates"]
            coord2rid[(c[0], c[1])] = rid

        dir_map = {"north": (0, 1), "south": (0, -1), "east": (1, 0), "west": (-1, 0)}
        opp_map = {"north": "south", "south": "north", "east": "west", "west": "east"}
        for rid, rd in rooms.items():
            x, y = rd["coordinates"]
            for d, (dx, dy) in dir_map.items():
                nxy = (x + dx, y + dy)
                nrid = coord2rid.get(nxy)
                if nrid and d not in rd["exits"] and random.random() < 0.50:
                    rd["exits"][d] = {"target": nrid, "type": "direction"}
                    rooms[nrid]["exits"][opp_map[d]] = {"target": rid, "type": "direction"}

        self._ensure_connected(rooms, room_ids, coord2rid)
        self._set_floor_endpoints(floor_data, room_ids, floor_number, seed, is_final)

        # Validate all rooms are connected
        floor_data = self.ensure_all_rooms_connected(floor_data)

        return floor_data

    # ── connectivity guarantee ──────────────────────────────────────

    def ensure_all_rooms_connected(self, floor_data):
        """CRITICAL: Ensure all rooms reachable from entrance with proper reconnection logic."""
        rooms = floor_data["rooms"]
        if not rooms:
            return floor_data
        
        entrance_room = floor_data.get("entrance_room")
        if not entrance_room:
            entrance_room = list(rooms.keys())[0]
        
        # BFS to find all reachable rooms from entrance
        visited = set()
        queue = [entrance_room]
        
        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            
            visited.add(current)
            
            # Add connected rooms
            room = rooms.get(current)
            if not room:
                continue
            
            for exit_data in room.get("exits", {}).values():
                if isinstance(exit_data, dict):
                    target = exit_data.get("target")
                else:
                    target = exit_data
                
                if target and target in rooms and target not in visited:
                    queue.append(target)
        
        # Find disconnected rooms
        all_rooms = set(rooms.keys())
        disconnected = all_rooms - visited
        
        if disconnected:
            print(f"[WARNING] Floor {floor_data.get('floor_number', '?')}: {len(disconnected)} disconnected rooms, reconnecting...")
            
            # Connect each disconnected room to nearest visited room
            for disc_id in list(disconnected):  # Use list() to avoid modification during iteration
                disc_room = rooms[disc_id]
                disc_coords = disc_room.get("coordinates", [0, 0])
                
                # Find nearest connected room by Manhattan distance
                best_room = None
                best_distance = float('inf')
                
                for conn_id in visited:
                    conn_room = rooms[conn_id]
                    conn_coords = conn_room.get("coordinates", [0, 0])
                    
                    distance = abs(disc_coords[0] - conn_coords[0]) + abs(disc_coords[1] - conn_coords[1])
                    
                    if distance < best_distance:
                        best_distance = distance
                        best_room = conn_id
                
                if best_room:
                    conn_room = rooms[best_room]
                    conn_coords = conn_room.get("coordinates", [0, 0])
                    
                    # Calculate proper direction based on relative position
                    dx = disc_coords[0] - conn_coords[0]
                    dy = disc_coords[1] - conn_coords[1]
                    
                    if abs(dx) >= abs(dy):
                        direction = "east" if dx > 0 else "west"
                        opposite = "west" if dx > 0 else "east"
                    else:
                        direction = "north" if dy > 0 else "south"
                        opposite = "south" if dy > 0 else "north"
                    
                    # BIDIRECTIONAL connection
                    conn_room["exits"][direction] = {
                        "target": disc_id,
                        "type": "direction"
                    }
                    disc_room["exits"][opposite] = {
                        "target": best_room,
                        "type": "direction"
                    }
                    
                    print(f"[FIX] Connected {disc_id} to {best_room} via {direction}/{opposite}")
                    
                    # Add to visited
                    visited.add(disc_id)
                    
                    # Re-check for newly reachable rooms
                    queue = [disc_id]
                    while queue:
                        curr = queue.pop(0)
                        for exit_data in rooms[curr].get("exits", {}).values():
                            if isinstance(exit_data, dict):
                                target = exit_data.get("target")
                            else:
                                target = exit_data
                            
                            if target and target in disconnected and target not in visited:
                                visited.add(target)
                                disconnected.discard(target)
                                queue.append(target)
        
        print(f"[OK] Floor {floor_data.get('floor_number', '?')}: All {len(visited)} rooms connected")
        
        return floor_data

    def add_secret_room(self, floor_data):
        """Add secret room to boss room - GUARANTEED to work on final floor."""
        rooms = floor_data["rooms"]
        
        # Find the boss room
        boss_room_id = floor_data.get("boss_room")
        if not boss_room_id:
            # Fallback: search for boss room
            for rid in rooms:
                if rooms[rid].get("is_boss_room"):
                    boss_room_id = rid
                    break
        
        if not boss_room_id:
            print(f"[ERROR] No boss room found for secret room on floor {floor_data.get('floor_number', '?')}!")
            return floor_data

        boss_room = rooms[boss_room_id]
        
        # Create secret room ID
        secret_room_id = f"{boss_room_id}_secret"
        
        # Get boss room coordinates
        boss_coords = boss_room.get("coordinates", [0, 0])
        
        # Create the secret room with ASCII art easter egg and items
        rooms[secret_room_id] = {
            "name": "🌟 HIDDEN CHAMBER 🌟",
            "description": "A secret chamber hidden behind the walls of the treasure vault. "
                          "In the center of the room, strange ASCII art is carved into stone:\n\n"
                          "    ∿ ` ∾ ∿ ` ∾ ∿ ` ∾\n"
                          "   / d o a b i g c h e e s e \\\n"
                          "   \\ ∿ ` ∾ ∿ ` ∾ ∿ ` ∾ /\n"
                          "    ¯ ¯ ¯ ¯ ¯ ¯ ¯ ¯ ¯ ¯ ¯ ¯\n\n"
                          "You feel the presence of something legendary here.",
            "coordinates": [boss_coords[0] + 1, boss_coords[1]],
            "exits": {
                "back": {
                    "target": boss_room_id,
                    "type": "direction",
                    "transition_text": "You carefully return through the hidden passage..."
                }
            },
            "items": ["legendary_artifact", "ancient_relic"],
            "is_secret": True
        }
        
        # Mark boss room as having secret and link to it
        boss_room["has_secret"] = True
        boss_room["secret_room_id"] = secret_room_id
        boss_room["secret_discovered"] = False
        
        # Enhance boss room description with hint
        original_desc = boss_room.get("description", "")
        boss_room["description"] = original_desc + "\n\nThe ornate walls seem to have intricate carvings that catch your eye."
        
        print(f"[Secret] Boss room {boss_room_id} now has secret: {secret_room_id}")
        
        return floor_data

    def _ensure_connected(self, rooms, room_ids, coord2rid):
        """BFS from the first room; connect any isolated nodes to the closest visited one."""

        visited = set()
        queue = [room_ids[0]]
        visited.add(room_ids[0])

        while queue:
            cur = queue.pop(0)
            for _d, edata in rooms[cur].get("exits", {}).items():
                target = edata.get("target", edata) if isinstance(edata, dict) else edata
                if target in rooms and target not in visited:
                    visited.add(target)
                    queue.append(target)

        isolated = [r for r in room_ids if r not in visited]
        dir_map = {"north": (0, 1), "south": (0, -1), "east": (1, 0), "west": (-1, 0)}
        opp_map = {"north": "south", "south": "north", "east": "west", "west": "east"}

        for iso in isolated:
            x, y = rooms[iso]["coordinates"]
            # Try to connect to an adjacent visited room
            connected = False
            for d, (dx, dy) in dir_map.items():
                nrid = coord2rid.get((x + dx, y + dy))
                if nrid and nrid in visited:
                    rooms[iso]["exits"][d] = {"target": nrid, "type": "direction"}
                    rooms[nrid]["exits"][opp_map[d]] = {"target": iso, "type": "direction"}
                    visited.add(iso)
                    connected = True
                    break

            if not connected:
                # Fallback: connect to the closest visited room by Manhattan distance
                best = None
                best_dist = 9999
                for vrid in visited:
                    vx, vy = rooms[vrid]["coordinates"]
                    dist = abs(x - vx) + abs(y - vy)
                    if dist < best_dist:
                        best = vrid
                        best_dist = dist
                if best:
                    rooms[iso]["exits"]["east"] = {"target": best, "type": "direction"}
                    rooms[best]["exits"]["west"] = {"target": iso, "type": "direction"}
                    visited.add(iso)

    # ── stairs / boss / endpoints ───────────────────────────────────

    def _set_floor_endpoints(self, floor_data, path, floor_number, seed, is_final):
        """Set stairs down, boss room, and mark stairs-up room."""

        rooms = floor_data["rooms"]
        last_room_id = path[-1]

        if is_final:
            # Final floor – boss / treasure vault
            floor_data["boss_room"] = last_room_id
            rooms[last_room_id]["name"] = "\U0001f48e TREASURE VAULT \U0001f48e"
            rooms[last_room_id]["description"] = (
                "A magnificent chamber glittering with gold and jewels. "
                "Ancient treasure beyond imagination fills every corner."
            )
            rooms[last_room_id]["is_boss_room"] = True
            rooms[last_room_id]["quality"] = "high"
        else:
            # Add stairs down placeholder (real target linked later)
            floor_data["exit_stairs_down"] = last_room_id
            rooms[last_room_id]["exits"]["down"] = {
                "target": f"dungeon_{seed}_floor{floor_number + 1}_room1",
                "type": "stairs_down",
                "transition_text": f"You descend deeper into the dungeon... Floor {floor_number + 1}.",
            }

        # Stairs up placeholder (except floor 1)
        if floor_number > 1:
            entrance_id = floor_data["entrance_room"]
            floor_data["exit_stairs_up"] = entrance_id
            rooms[entrance_id]["exits"]["up"] = {
                "target": "__link_up__",  # resolved in _link_stairs_across_floors
                "type": "stairs_up",
                "transition_text": f"You climb back up to floor {floor_number - 1}...",
            }

    def _link_stairs_across_floors(self, dungeon_data):
        """Resolve stairs-up targets so they point at the correct stairs-down room."""
        floors = dungeon_data["floors"]
        for fnum, fdata in floors.items():
            if fnum <= 1:
                continue
            up_room_id = fdata.get("exit_stairs_up")
            if not up_room_id:
                continue
            # Previous floor's stairs-down room
            prev_floor = floors.get(fnum - 1, {})
            down_room_id = prev_floor.get("exit_stairs_down")
            if not down_room_id:
                continue
            # Patch the up-exit target
            up_room = fdata["rooms"].get(up_room_id, {})
            up_exit = up_room.get("exits", {}).get("up")
            if up_exit and isinstance(up_exit, dict):
                up_exit["target"] = down_room_id

    def _add_surface_exit(self, dungeon_data, entrance_room_id=None):
        """Add a 'leave' exit in floor-1 entrance so the player can return to the surface."""
        target = entrance_room_id or "dungeon_forest_entrance"
        floor1 = dungeon_data["floors"].get(1)
        if not floor1:
            return
        entrance_id = floor1.get("entrance_room")
        if not entrance_id:
            return
        entrance = floor1["rooms"].get(entrance_id)
        if not entrance:
            return
        entrance["exits"]["leave"] = {
            "target": target,
            "type": "leave_dungeon",
            "transition_text": "You climb back towards the light... You emerge from the dungeon entrance.",
        }
        # Store the return target in dungeon_data for teleport-out scenarios
        dungeon_data["entrance_room_id"] = target
        print(f"[DungeonGenerator] Added surface exit in {entrance_id} -> {target}")

    # ── room creation ───────────────────────────────────────────────

    def _select_room_type(self, quality):
        if quality == "high":
            return random.choice(self.high_quality_rooms)
        elif quality == "medium":
            return random.choice(self.medium_quality_rooms)
        return random.choice(self.low_quality_rooms)

    def _create_room(self, room_id, room_type, quality, floor_number):
        template = ROOM_TEMPLATES.get(room_type, ROOM_TEMPLATES["library"])

        room = {
            "id": room_id,
            "type": room_type,
            "name": template["name"],
            "description": template["entry_description"],
            "quality": quality,
            "floor": floor_number,
            "coordinates": [0, 0],
            "exits": {},
            "items": {},
            "chests": [],
            "traps": [],
            "visited": False,
            "location_type": "building",
        }

        room = self._populate_room_loot(room, quality, floor_number, template)
        room = self._maybe_spawn_chest(room, template["chest_spawn_chance"], floor_number)
        return room

    # ── loot generation ─────────────────────────────────────────────

    def _populate_room_loot(self, room, quality, floor_number, template):
        loot_pools = {
            "low": [k for k, v in ITEM_DATABASE.items() if v["tier"] == "low"],
            "medium": [k for k, v in ITEM_DATABASE.items() if v["tier"] == "medium"],
            "high": [k for k, v in ITEM_DATABASE.items() if v["tier"] == "high"],
        }

        depth_bonus = floor_number - 1
        item_range = template.get("item_spawn_count", (1, 3))
        num_items = random.randint(item_range[0], item_range[1])

        pool = loot_pools.get(quality, loot_pools["low"])
        for _ in range(num_items):
            item_name = random.choice(pool)
            qty = random.randint(1, 2)
            base_value = ITEM_DATABASE.get(item_name, {"value": 10})["value"]
            value = int(base_value * (1 + depth_bonus * 0.2))

            if item_name in room["items"]:
                room["items"][item_name]["quantity"] += qty
            else:
                room["items"][item_name] = {"quantity": qty, "value": value}

        return room

    def _maybe_spawn_chest(self, room, base_chance, floor_number):
        adjusted = base_chance * (1 + (floor_number - 1) * 0.3)
        if random.random() >= adjusted:
            return room

        if room["quality"] == "high":
            ct = random.choices(["wooden_chest", "iron_chest", "ornate_chest"], [0.2, 0.5, 0.3])[0]
        elif room["quality"] == "medium":
            ct = random.choices(["wooden_chest", "iron_chest"], [0.6, 0.4])[0]
        else:
            ct = "wooden_chest"

        room["chests"].append({
            "type": ct,
            "opened": False,
            "contents": self._generate_chest_contents(ct, floor_number),
        })
        return room

    def _generate_chest_contents(self, chest_type, floor_number):
        cd = CHEST_TEMPLATES.get(chest_type, CHEST_TEMPLATES["wooden_chest"])
        num_items = random.randint(cd["item_count"][0], cd["item_count"][1])
        gold = random.randint(cd["gold_bonus"][0], cd["gold_bonus"][1])
        gold = int(gold * (1 + (floor_number - 1) * 0.4))

        rarity_to_pool = {"common": "low", "uncommon": "medium", "rare": "high", "epic": "high"}
        loot_pools = {
            "low": [k for k, v in ITEM_DATABASE.items() if v["tier"] == "low"][:5],
            "medium": [k for k, v in ITEM_DATABASE.items() if v["tier"] == "medium"][:5],
            "high": [k for k, v in ITEM_DATABASE.items() if v["tier"] == "high"][:5],
        }

        contents = {"items": {}, "gold": gold}
        weights = cd["rarity_weights"]
        for _ in range(num_items):
            rarity = random.choices(list(weights.keys()), list(weights.values()))[0]
            pool_key = rarity_to_pool[rarity]
            item = random.choice(loot_pools[pool_key])
            val = ITEM_DATABASE.get(item, {"value": 10})["value"]
            if rarity == "epic":
                val = int(val * 1.5)
            if item in contents["items"]:
                contents["items"][item]["quantity"] += 1
            else:
                contents["items"][item] = {"quantity": 1, "value": val}
        return contents
