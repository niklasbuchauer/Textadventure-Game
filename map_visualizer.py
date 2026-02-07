"""
ASCII Grid Map Visualizer for Adventure Game World

Generates readable ASCII maps showing room layout, connections, and player position.
Auto-layouts rooms based on exit directions and connection graph.
"""

import json
import os
from typing import Dict, List, Tuple, Set, Optional
from collections import defaultdict, deque


class MapVisualizer:
	"""Generate ASCII art maps of the game world."""
	
	def __init__(self, world_file: str):
		self.world_file = world_file
		self.world_data = self._load_world()
		self.rooms = self.world_data.get("rooms", {})
		self.start_room = self.world_data.get("start_room", "clearing")
	
	def _load_world(self) -> Dict:
		"""Load world.json safely."""
		try:
			with open(self.world_file, "r", encoding="utf-8") as f:
				return json.load(f)
		except Exception as e:
			raise RuntimeError(f"Failed to load world: {e}")
	
	def _get_room_code(self, room_name: str, max_len: int = 3) -> str:
		"""Generate a 3-letter code for a room name."""
		# Remove common words and take first letters
		words = room_name.lower().replace("_", " ").split()
		code = ""
		for word in words:
			if word not in {"the", "a", "an", "of", "and", "or", "but"}:
				code += word[0]
				if len(code) >= max_len:
					break
		return (code or room_name[0]).upper().ljust(3)[:3]
	
	def _get_room_bracket(self, room_name: str) -> Tuple[str, str]:
		"""Get bracket style based on room location_type."""
		room = self.rooms.get(room_name, {})
		loc_type = room.get("location_type", "wilderness")
		
		brackets = {
			"wilderness": ("|", "|"),
			"settlement": ("[", "]"),
			"building": ("{", "}"),
			"transition": ("~", "~")
		}
		return brackets.get(loc_type, ("|", "|"))
	
	def _build_connection_graph(self) -> Dict[str, Set[str]]:
		"""Build a graph of room connections."""
		graph = defaultdict(set)
		for room_name, room_data in self.rooms.items():
			exits = room_data.get("exits", {})
			for direction, exit_info in exits.items():
				if isinstance(exit_info, dict):
					target = exit_info.get("target")
				else:
					target = exit_info
				if target and target in self.rooms:
					graph[room_name].add(target)
					# Make bidirectional for layout purposes
					graph[target].add(room_name)
		return graph
	
	def _find_reachable_rooms(self) -> Set[str]:
		"""Find all rooms reachable from start_room using BFS."""
		if self.start_room not in self.rooms:
			return set()
		
		graph = self._build_connection_graph()
		visited = set()
		queue = deque([self.start_room])
		visited.add(self.start_room)
		
		while queue:
			current = queue.popleft()
			for neighbor in graph.get(current, set()):
				if neighbor not in visited:
					visited.add(neighbor)
					queue.append(neighbor)
		
		return visited
	
	def _get_exit_direction(self, room_name: str, target_name: str) -> Optional[str]:
		"""Get the direction of exit from room_name to target_name."""
		room = self.rooms.get(room_name, {})
		exits = room.get("exits", {})
		for direction, exit_info in exits.items():
			if isinstance(exit_info, dict):
				target = exit_info.get("target")
			else:
				target = exit_info
			if target == target_name:
				return direction
		return None
	
	def _assign_coordinates(self, start_room: str) -> Dict[str, Tuple[int, int]]:
		"""Assign X,Y coordinates to rooms using BFS from start_room."""
		coordinates = {}
		if start_room not in self.rooms:
			return coordinates
		
		# Direction to coordinate offset mapping
		direction_offsets = {
			"north": (0, -1),
			"south": (0, 1),
			"east": (1, 0),
			"west": (-1, 0)
		}
		
		coordinates[start_room] = (0, 0)
		visited = {start_room}
		queue = deque([start_room])
		
		while queue:
			current = queue.popleft()
			current_x, current_y = coordinates[current]
			
			room = self.rooms.get(current, {})
			exits = room.get("exits", {})
			
			for direction, exit_info in exits.items():
				if isinstance(exit_info, dict):
					target = exit_info.get("target")
				else:
					target = exit_info
				
				if not target or target not in self.rooms or target in visited:
					continue
				
				# Calculate new position based on direction
				if direction in direction_offsets:
					dx, dy = direction_offsets[direction]
					new_x = current_x + dx
					new_y = current_y + dy
				else:
					# Named exits: place nearby if possible
					new_x = current_x + 1
					new_y = current_y
				
				# Check for collision and offset if necessary
				attempt = 0
				while (new_x, new_y) in coordinates.values() and attempt < 4:
					new_x += 1
					attempt += 1
				
				coordinates[target] = (new_x, new_y)
				visited.add(target)
				queue.append(target)
		
		return coordinates
	
	def _render_grid(self, coordinates: Dict[str, Tuple[int, int]], current_player_room: Optional[str] = None) -> str:
		"""Render ASCII grid based on room coordinates."""
		if not coordinates:
			return "(No rooms to display)"
		
		# Find grid bounds
		xs = [x for x, y in coordinates.values()]
		ys = [y for x, y in coordinates.values()]
		min_x, max_x = min(xs), max(xs)
		min_y, max_y = min(ys), max(ys)
		
		# Add padding
		min_x -= 1
		max_x += 1
		min_y -= 1
		max_y += 1
		
		width = max_x - min_x + 1
		height = max_y - min_y + 1
		
		# Create grid
		grid = [[None for _ in range(width)] for _ in range(height)]
		
		# Place rooms
		for room_name, (x, y) in coordinates.items():
			grid_x = x - min_x
			grid_y = y - min_y
			grid[grid_y][grid_x] = room_name
		
		# Render
		lines = []
		
		# Header with X coordinates
		header = "    "
		for x in range(min_x, max_x + 1):
			header += f"{x:3d} "
		lines.append(header)
		
		# Each row
		for grid_y, row in enumerate(grid):
			y = min_y + grid_y
			
			# Top border
			border = "   +" + "+".join(["---"] * width) + "+"
			lines.append(border)
			
			# Room row
			room_line = f"{y:2d} "
			for grid_x, room_name in enumerate(row):
				if room_name:
					code = self._get_room_code(room_name)
					if room_name == current_player_room:
						code = f"*{code[1:]}" if len(code) > 1 else "*"
					left, right = self._get_room_bracket(room_name)
					cell = f"{left}{code}{right}"
				else:
					cell = "|   |"
				room_line += cell
			room_line += "|"
			lines.append(room_line)
		
		# Bottom border
		border = "   +" + "+".join(["---"] * width) + "+"
		lines.append(border)
		
		return "\n".join(lines)
	
	def _build_legend(self, coordinates: Dict[str, Tuple[int, int]]) -> str:
		"""Build legend showing room codes and names."""
		lines = ["LEGEND:", ""]
		
		# Sort by code
		rooms_list = sorted(coordinates.items(), key=lambda x: self._get_room_code(x[0]))
		
		for room_name, (x, y) in rooms_list:
			code = self._get_room_code(room_name)
			left, right = self._get_room_bracket(room_name)
			room_type = self.rooms.get(room_name, {}).get("location_type", "?")
			marker = f"{left}{code}{right}"
			lines.append(f"  {marker} {room_name:<25} ({room_type:<10}) [{x:2d},{y:2d}]")
		
		return "\n".join(lines)
	
	def _list_disconnected(self, reachable: Set[str]) -> str:
		"""List rooms not reachable from start_room."""
		disconnected = [r for r in self.rooms.keys() if r not in reachable]
		
		if not disconnected:
			return "✓ All rooms connected!"
		
		lines = ["⚠ DISCONNECTED ROOMS:", ""]
		for room_name in sorted(disconnected):
			room_type = self.rooms.get(room_name, {}).get("location_type", "?")
			lines.append(f"  • {room_name:<25} ({room_type})")
		
		return "\n".join(lines)
	
	def _list_jump_connections(self, coordinates: Dict[str, Tuple[int, int]]) -> str:
		"""List non-adjacent (jump) connections."""
		jumps = []
		
		for room_name, room_data in self.rooms.items():
			if room_name not in coordinates:
				continue
			
			exits = room_data.get("exits", {})
			x1, y1 = coordinates[room_name]
			
			for direction, exit_info in exits.items():
				if isinstance(exit_info, dict):
					target = exit_info.get("target")
				else:
					target = exit_info
				
				if not target or target not in coordinates:
					continue
				
				x2, y2 = coordinates[target]
				distance = abs(x2 - x1) + abs(y2 - y1)
				
				# Adjacent = distance of 1
				if distance > 1:
					display = exit_info.get("display", direction) if isinstance(exit_info, dict) else direction
					jumps.append(f"{room_name} → {display} → {target}")
		
		if not jumps:
			return ""
		
		lines = ["JUMP CONNECTIONS (non-adjacent):", ""]
		for jump in sorted(jumps):
			lines.append(f"  {jump}")
		
		return "\n".join(lines)
	
	def generate_map(self, start_room: Optional[str] = None, current_player_room: Optional[str] = None, compact: bool = False) -> str:
		"""Generate full map visualization."""
		if start_room is None:
			start_room = self.start_room
		
		if current_player_room is None:
			current_player_room = self.start_room
		
		reachable = self._find_reachable_rooms()
		coordinates = self._assign_coordinates(start_room)
		
		# Filter to reachable rooms
		coordinates = {k: v for k, v in coordinates.items() if k in reachable}
		
		lines = []
		lines.append("=" * 70)
		lines.append("  WORLD MAP")
		lines.append("=" * 70)
		lines.append("")
		
		# Summary stats
		total_rooms = len(self.rooms)
		connected_rooms = len(reachable)
		disconnected_count = total_rooms - connected_rooms
		
		lines.append(f"Grid Size: {len(coordinates)} reachable rooms / {total_rooms} total")
		lines.append(f"Starting Room: {start_room}")
		if current_player_room != start_room:
			lines.append(f"Player Location: {current_player_room} *")
		lines.append("")
		
		# Render grid
		grid_display = self._render_grid(coordinates, current_player_room)
		lines.append(grid_display)
		lines.append("")
		
		# Legend
		legend = self._build_legend(coordinates)
		lines.append(legend)
		lines.append("")
		
		# Jump connections
		jumps = self._list_jump_connections(coordinates)
		if jumps:
			lines.append(jumps)
			lines.append("")
		
		# Disconnected rooms
		disconnected = self._list_disconnected(reachable)
		lines.append(disconnected)
		lines.append("")
		
		# Statistics
		lines.append("=" * 70)
		lines.append(f"STATISTICS: {connected_rooms} connected, {disconnected_count} disconnected")
		lines.append("=" * 70)
		
		return "\n".join(lines)


# Test/demo if run directly
if __name__ == "__main__":
	import sys
	world_file = sys.argv[1] if len(sys.argv) > 1 else "world.json"
	
	try:
		viz = MapVisualizer(world_file)
		print(viz.generate_map())
	except Exception as e:
		print(f"Error: {e}")
