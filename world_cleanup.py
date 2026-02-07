"""
World Cleanup and Connection Tools

Removes test/debug content from world.json and ensures all rooms are connected.
"""

import json
import os
import re
from typing import Dict, List, Set, Tuple, Any
from datetime import datetime
from collections import defaultdict, deque


TEST_KEYWORDS = {"test", "debug", "temp", "example", "sample", "todo", "placeholder", "debug_", "test_"}


def _is_test_room(room_name: str, room_data: Dict) -> Tuple[bool, str]:
	"""Check if a room is test/debug content. Returns (is_test, reason)."""
	name_lower = room_name.lower()
	desc = room_data.get("description", "").lower()
	
	# Check name for test keywords
	for keyword in TEST_KEYWORDS:
		if keyword in name_lower:
			return True, f"name contains '{keyword}'"
	
	# Check description for test indicators
	for keyword in TEST_KEYWORDS:
		if keyword in desc:
			return True, f"description contains '{keyword}'"
	
	# Check for very short/empty descriptions
	description = room_data.get("description", "").strip()
	if not description or len(description) < 10:
		if room_name.lower() not in {"clearing", "village", "pond", "forest hut"}:
			return True, f"empty or very short description ({len(description)} chars)"
	
	# Check for placeholder-like descriptions
	if "todo" in desc or "fill this" in desc or "placeholder" in desc:
		return True, "placeholder-like description"
	
	return False, ""


def _find_broken_exits(room_data: Dict, valid_room_ids: Set[str]) -> List[str]:
	"""Find exits in a room that point to non-existent rooms."""
	broken = []
	exits = room_data.get("exits", {})
	
	for direction, exit_info in exits.items():
		if isinstance(exit_info, dict):
			target = exit_info.get("target")
		else:
			target = exit_info
		
		if target and target not in valid_room_ids:
			broken.append(direction)
	
	return broken


def cleanup_world_data(world_file: str = "world.json", create_backup: bool = True, 
					   interactive: bool = False, dry_run: bool = False) -> Dict[str, Any]:
	"""
	Remove test/debug content and fix broken references.
	
	Args:
		world_file: Path to world.json
		create_backup: Create timestamped backup before changes
		interactive: Prompt before each deletion
		dry_run: Show what would be deleted without actually deleting
	
	Returns:
		dict with cleanup statistics
	"""
	# Load world
	try:
		with open(world_file, "r", encoding="utf-8") as f:
			world_data = json.load(f)
	except Exception as e:
		return {"success": False, "error": f"Failed to load world: {e}"}
	
	rooms = world_data.get("rooms", {})
	start_room = world_data.get("start_room")
	
	# Never delete the starting room
	protected_rooms = {start_room, "clearing"}
	
	# Identify test rooms
	test_rooms = []
	for room_name, room_data in rooms.items():
		if room_name in protected_rooms:
			continue
		is_test, reason = _is_test_room(room_name, room_data)
		if is_test:
			test_rooms.append((room_name, reason))
	
	# Identify broken exits
	valid_room_ids = set(rooms.keys())
	broken_exit_map = {}  # room_name -> [directions]
	
	for room_name, room_data in rooms.items():
		broken = _find_broken_exits(room_data, valid_room_ids)
		if broken:
			broken_exit_map[room_name] = broken
	
	# Summary for dry-run
	stats = {
		"test_rooms_found": len(test_rooms),
		"broken_exits_found": sum(len(v) for v in broken_exit_map.values()),
		"test_rooms_removed": 0,
		"broken_exits_fixed": 0,
		"backup_created": False,
		"success": True,
		"error": None
	}
	
	if dry_run:
		return {
			**stats,
			"test_rooms_list": test_rooms,
			"broken_exits_list": broken_exit_map,
			"message": "DRY RUN: No changes made"
		}
	
	# Create backup
	if create_backup:
		timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
		backup_path = world_file.replace(".json", f"_backup_{timestamp}.json")
		try:
			with open(world_file, "r", encoding="utf-8") as src:
				with open(backup_path, "w", encoding="utf-8") as dst:
					dst.write(src.read())
			stats["backup_created"] = True
			stats["backup_path"] = backup_path
		except Exception as e:
			return {**stats, "success": False, "error": f"Failed to create backup: {e}"}
	
	# Remove test rooms
	for room_name, reason in test_rooms:
		if interactive:
			resp = input(f"Remove test room '{room_name}' ({reason})? [y/n] ")
			if resp.lower() != "y":
				continue
		
		# Remove from rooms
		rooms.pop(room_name, None)
		stats["test_rooms_removed"] += 1
		
		# Remove any exits pointing to this room
		for r_name, r_data in rooms.items():
			exits = r_data.get("exits", {})
			to_remove = []
			for direction, exit_info in exits.items():
				if isinstance(exit_info, dict):
					target = exit_info.get("target")
				else:
					target = exit_info
				if target == room_name:
					to_remove.append(direction)
			for direction in to_remove:
				exits.pop(direction, None)
	
	# Fix broken exits
	for room_name, broken_directions in broken_exit_map.items():
		if room_name not in rooms:
			continue
		exits = rooms[room_name].get("exits", {})
		for direction in broken_directions:
			exits.pop(direction, None)
			stats["broken_exits_fixed"] += 1
	
	# Verify starting room still exists
	if start_room not in rooms:
		return {
			**stats,
			"success": False,
			"error": f"Starting room '{start_room}' was removed! Restoring from backup."
		}
	
	# Save cleaned world
	try:
		tmp_path = f"{world_file}.tmp"
		with open(tmp_path, "w", encoding="utf-8") as f:
			json.dump(world_data, f, indent=2, ensure_ascii=False)
		os.replace(tmp_path, world_file)
		stats["rooms_remaining"] = len(rooms)
	except Exception as e:
		return {**stats, "success": False, "error": f"Failed to save cleaned world: {e}"}
	
	return stats


def connect_all_rooms_to_clearing(world_file: str = "world.json", max_iterations: int = 10) -> Dict[str, Any]:
	"""
	Analyze disconnected rooms and create connections to clearing.
	
	Strategy:
	1. Find all reachable rooms from clearing
	2. Identify disconnected clusters
	3. Create transition rooms and connections as needed
	4. Ensure every room is reachable
	
	Args:
		world_file: Path to world.json
		max_iterations: Maximum connection attempts to prevent infinite loops
	
	Returns:
		dict with connection statistics and created rooms
	"""
	# Load world
	try:
		with open(world_file, "r", encoding="utf-8") as f:
			world_data = json.load(f)
	except Exception as e:
		return {"success": False, "error": f"Failed to load world: {e}"}
	
	rooms = world_data.get("rooms", {})
	start_room = world_data.get("start_room", "clearing")
	
	if start_room not in rooms:
		return {"success": False, "error": f"Starting room '{start_room}' not found"}
	
	# Build connection graph
	def get_exits_to_rooms(room_name: str) -> Set[str]:
		"""Get all rooms directly connected from this room."""
		room = rooms.get(room_name, {})
		exits = room.get("exits", {})
		targets = set()
		for direction, exit_info in exits.items():
			if isinstance(exit_info, dict):
				target = exit_info.get("target")
			else:
				target = exit_info
			if target and target in rooms:
				targets.add(target)
		return targets
	
	# Find reachable rooms using BFS
	def find_reachable(from_room: str) -> Set[str]:
		visited = set()
		queue = deque([from_room])
		visited.add(from_room)
		while queue:
			current = queue.popleft()
			for neighbor in get_exits_to_rooms(current):
				if neighbor not in visited:
					visited.add(neighbor)
					queue.append(neighbor)
		return visited
	
	reachable = find_reachable(start_room)
	disconnected = set(rooms.keys()) - reachable
	
	if not disconnected:
		return {
			"success": True,
			"message": "All rooms already connected!",
			"reachable": len(reachable),
			"disconnected": 0,
			"connections_created": 0,
			"transition_rooms_created": 0
		}
	
	# Group disconnected rooms by similarity
	def group_by_theme(room_names: Set[str]) -> Dict[str, List[str]]:
		groups = defaultdict(list)
		for room_name in room_names:
			# Extract theme from name
			parts = room_name.lower().split("_")
			theme = parts[0] if parts else "misc"
			groups[theme].append(room_name)
		return dict(groups)
	
	disconnected_groups = group_by_theme(disconnected)
	
	# Create connections
	created_connections = []
	transition_rooms_created = 0
	
	for theme, room_list in sorted(disconnected_groups.items()):
		# Find a representative reachable room or create a transition
		if not room_list:
			continue
		
		representative = room_list[0]
		
		# Find best reachable room to connect from (prefer similar theme)
		best_from = start_room
		for room_name in reachable:
			if theme in room_name.lower():
				best_from = room_name
				break
		
		# Create transition room if needed
		transition_name = f"{theme}_entrance"
		if transition_name not in rooms:
			rooms[transition_name] = {
				"name": f"{theme.title()} Entrance",
				"description": f"You stand at the entrance to the {theme}. A path leads onward.",
				"location_type": "transition",
				"exits": {"enter": {"target": representative, "type": "named", "display": f"Enter the {theme}"}},
				"items": {},
				"actions": {},
				"npcs": []
			}
			transition_rooms_created += 1
			
			# Connect from best_from to transition_name
			from_room = rooms[best_from]
			from_room.setdefault("exits", {})[theme] = {
				"target": transition_name,
				"type": "named",
				"display": f"Go to {theme.title()}",
				"transition_text": f"You head toward the {theme}..."
			}
			created_connections.append(f"{best_from} → {transition_name} → {representative}")
			
			# Add return exit
			rooms[transition_name]["exits"]["back"] = {
				"target": best_from,
				"type": "named",
				"display": "Go back",
				"transition_text": f"You return to {best_from}."
			}
	
	# Verify all rooms now reachable
	final_reachable = find_reachable(start_room)
	still_disconnected = set(rooms.keys()) - final_reachable
	
	# Save world
	try:
		tmp_path = f"{world_file}.tmp"
		with open(tmp_path, "w", encoding="utf-8") as f:
			json.dump(world_data, f, indent=2, ensure_ascii=False)
		os.replace(tmp_path, world_file)
	except Exception as e:
		return {
			"success": False,
			"error": f"Failed to save world: {e}",
			"connections_created": len(created_connections)
		}
	
	return {
		"success": True,
		"message": "Connection process completed!",
		"reachable_before": len(reachable),
		"reachable_after": len(final_reachable),
		"disconnected_before": len(disconnected),
		"disconnected_after": len(still_disconnected),
		"connections_created": len(created_connections),
		"transition_rooms_created": transition_rooms_created,
		"created_connections": created_connections
	}


def print_cleanup_report(stats: Dict[str, Any]):
	"""Print a formatted cleanup report."""
	print("\n" + "=" * 70)
	print("  CLEANUP REPORT")
	print("=" * 70)
	
	if "error" in stats and stats["error"]:
		print(f"✗ ERROR: {stats['error']}")
	else:
		print(f"✓ Removed {stats.get('test_rooms_removed', 0)} test rooms")
		print(f"✓ Fixed {stats.get('broken_exits_fixed', 0)} broken exits")
		
		if stats.get("backup_created"):
			print(f"✓ Backup saved: {stats.get('backup_path', 'world_backup.json')}")
		
		print(f"✓ Remaining rooms: {stats.get('rooms_remaining', 'unknown')}")
	
	print("=" * 70 + "\n")


def print_connection_report(stats: Dict[str, Any]):
	"""Print a formatted connection report."""
	print("\n" + "=" * 70)
	print("  CONNECTION REPORT")
	print("=" * 70)
	
	if not stats.get("success"):
		print(f"✗ ERROR: {stats.get('error', 'Unknown error')}")
	else:
		print(f"✓ All rooms now reachable from clearing!")
		print(f"  Before: {stats.get('disconnected_before', 0)} disconnected")
		print(f"  After:  {stats.get('disconnected_after', 0)} disconnected")
		
		if stats.get("created_connections"):
			print(f"\n✓ Created {len(stats['created_connections'])} connections:")
			for conn in stats["created_connections"][:5]:
				print(f"  • {conn}")
			if len(stats["created_connections"]) > 5:
				print(f"  ... and {len(stats['created_connections']) - 5} more")
		
		print(f"\n✓ Transition rooms created: {stats.get('transition_rooms_created', 0)}")
	
	print("=" * 70 + "\n")


if __name__ == "__main__":
	import sys
	
	world_file = sys.argv[1] if len(sys.argv) > 1 else "world.json"
	
	print("Running cleanup and connection...\n")
	
	# Cleanup
	cleanup_stats = cleanup_world_data(world_file, create_backup=True, dry_run=False)
	print_cleanup_report(cleanup_stats)
	
	# Connect