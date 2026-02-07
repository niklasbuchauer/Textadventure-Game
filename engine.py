import json
import os
import sys
import tkinter as tk
from tkinter import simpledialog, messagebox, font

WORLD_FILE = os.path.join(os.path.dirname(__file__), "world.json")
SAVE_FILE = os.path.join(os.path.dirname(__file__), "savegame.json")


class Room:
	"""Represents a room loaded from JSON. Mutable state includes items and actions (if desired)."""
	def __init__(self, data):
		self.name = data.get("name")
		self.description = data.get("description", "")
		self.exits = data.get("exits", {})  # dict: direction -> room_name
		self.items = list(data.get("items", []))  # items present in the room (list allows duplicates)
		# actions: dict mapping exact command string -> effect dict
		# effect dict can contain: response/text, add_item (list), remove_item (list), move_to (room name), effects, conditions
		self.actions = data.get("actions", {})

	def describe(self):
		"""Return room description with aggregated item counts (e.g. '3 bronze coins')."""
		desc = f"{self.name}\n{self.description}\n"
		if self.items:
			# aggregate counts
			counts = {}
			for it in self.items:
				counts[it] = counts.get(it, 0) + 1
			parts = []
			for it, cnt in counts.items():
				if cnt > 1:
					# naive pluralize by adding 's' if necessary
					pl = it + "s" if not it.endswith("s") else it
					parts.append(f"{cnt} {pl}")
				else:
					parts.append(it)
			desc += "You see: " + ", ".join(parts) + "\n"
		if self.exits:
			desc += "Exits: " + ", ".join(self.exits.keys()) + "\n"
		return desc


class Player:
	"""Tracks current room, inventory (dict), and arbitrary state variables (for logic)."""
	def __init__(self, start_room):
		self.current_room = start_room
		# inventory now a dict: { item_name: count }
		self.inventory = {}
		# state holds arbitrary flags, e.g. {"sitting": False}
		self.state = {}
		# stats holds numeric values like gold, health, score
		self.stats = {}

	def to_dict(self):
		# Always serialize inventory as dict of string->int
		return {
			"current_room": self.current_room,
			"inventory": {str(k): int(v) for k, v in (self.inventory or {}).items()},
			"state": self.state,
			"stats": self.stats
		}

	@classmethod
	def from_dict(cls, data):
		p = cls(data.get("current_room"))
		inv = data.get("inventory", {}) or {}
		# Accept either dict or list for backward compatibility
		if isinstance(inv, dict):
			# ensure inventory is dict of string->int
			p.inventory = {str(k): int(v) for k, v in inv.items()}
		elif isinstance(inv, list):
			# convert list like ["coin","coin","apple"] to {"coin":2,"apple":1}
			agg = {}
			for it in inv:
				if it is None:
					continue
				agg[str(it)] = agg.get(str(it), 0) + 1
			p.inventory = agg
		else:
			p.inventory = {}
		p.state = dict(data.get("state", {}))
		p.stats = dict(data.get("stats", {}))
		return p


class CommandHandler:
	"""Parse and execute commands. Delegates to GameEngine for state changes.
	All handler methods return a string (the response) instead of printing.
	"""
	def __init__(self, engine):
		self.engine = engine

	def _check_conditions(self, conds):
		"""Check conditions dict: supports {"state": {"key": value}}.
		Returns (True, '') if satisfied, otherwise (False, message).
		"""
		if not conds:
			return True, ""
		# only 'state' supported for now
		state_conds = conds.get("state", {})
		for k, v in state_conds.items():
			if self.engine.player.state.get(k) != v:
				# Allow optional custom 'fail_text' in conditions in future
				return False, conds.get("fail_text") or "You can't do that now."
		return True, ""

	def handle(self, raw):
		cmd = (raw or "").strip()
		if not cmd:
			return ""
		parts = cmd.split()
		verb = parts[0].lower()
		args = parts[1:]

		# Example generic blocking: if sitting, block movement and taking until they stand.
		# To change this behavior, update the blocked_verbs list or add more complex checks.
		if self.engine.player.state.get("sitting"):
			if verb in ("go", "walk", "move", "take", "get", "collect"):
				return "You need to stand up first."

		# First check global commands (work anywhere)
		if cmd in getattr(self.engine, "global_commands", {}):
			effect = self.engine.global_commands[cmd]
			ok, msg = self._check_conditions(effect.get("conditions", {}))
			if not ok:
				return msg
			return self._perform_global_command(effect)

		# check for room-specific action (exact command match)
		room = self.engine.rooms[self.engine.player.current_room]
		if cmd in room.actions:
			effect = room.actions[cmd]
			ok, msg = self._check_conditions(effect.get("conditions", {}))
			if not ok:
				return msg
			return self._perform_action(effect, room, cmd)

		# fallback to built-in verbs
		if verb in ("go", "walk", "move"):
			if not args:
				return "Go where?"
			return self._go(args[0].lower())
		if verb in ("look", "l"):
			return self._look()
		# Support new collect command and keep old aliases
		if verb in ("collect", "take", "get"):
			if not args:
				return "Collect what?"
			return self._collect(" ".join(args))
		if verb == "drop":
			if not args:
				return "Drop what?"
			return self._drop(" ".join(args))
		if verb in ("inventory", "inv", "i"):
			return self._inventory()
		if verb == "save":
			return self.engine.save_game()
		if verb == "load":
			return self.engine.load_game(interactive=False)
		if verb in ("quit", "exit"):
			# set flag so GUI can act on it
			self.engine.should_quit = True
			return "Goodbye."
		if verb in ("help", "?"):
			return self._help()
		if verb in ("examine", "inspect", "x"):
			if not args:
				return "Examine what?"
			return self._examine(" ".join(args))
		# add sell verb handling
		if verb == "sell":
			if not args:
				return "Sell what?"
			return self._sell(" ".join(args))

		return "I don't understand that."

	def _perform_action(self, effect, room, invoked_cmd):
		# effect is a dict possibly containing keys: text/response, add_item, remove_item, move_to, effects, conditions
		parts = []
		# support both legacy keys: 'response' and new 'text'
		text = effect.get("text") or effect.get("response")
		if text:
			parts.append(text)

		# Apply logical effects: e.g. {"state": {"sitting": True}}
		effects_block = effect.get("effects", {})
		inv_changed = False
		if effects_block:
			# handle state changes
			state_changes = effects_block.get("state", {})
			for k, v in state_changes.items():
				self.engine.player.state[k] = v

			# inventory additions
			for it in effects_block.get("inventory_add", []) if isinstance(effects_block.get("inventory_add", []), list) else []:
				if it:
					self._add_to_inventory(it)
					inv_changed = True
			# inventory removals
			for it in effects_block.get("inventory_remove", []) if isinstance(effects_block.get("inventory_remove", []), list) else []:
				if it:
					self._remove_from_inventory(it)
					inv_changed = True

		# add/remove items (older action keys)
		for it in effect.get("add_item", []):
			target = effect.get("add_target", "player")
			if target == "player":
				self._add_to_inventory(it)
				inv_changed = True
			else:
				if it not in room.items:
					room.items.append(it)
		for it in effect.get("remove_item", []):
			target = effect.get("remove_target", "room")
			if target == "room":
				if it in room.items:
					room.items.remove(it)
			else:
				# remove from player
				if it in self.engine.player.inventory:
					self._remove_from_inventory(it)
					inv_changed = True

		# move player if specified
		if "move_to" in effect:
			new_room = effect["move_to"]
			if new_room in self.engine.rooms:
				self.engine.player.current_room = new_room
				parts.append(self.engine.rooms[new_room].describe())
			else:
				parts.append(f"Cannot move to {new_room} (unknown room).")

		# notify engine that inventory changed so UI can refresh
		if inv_changed:
			try:
				self.engine._inventory_changed = True
			except Exception:
				pass

		return "\n".join(parts)

	def _perform_global_command(self, effect):
		"""Apply a global command's effects: text, inventory changes, state changes, and stats."""
		parts = []
		# support legacy keys too
		text = effect.get("text") or effect.get("response")
		if text:
			parts.append(text)

		inv_changed = False

		# inventory add/remove via effects
		for it in effect.get("effects", {}).get("inventory_add", []):
			if it:
				self._add_to_inventory(it)
				inv_changed = True
		for it in effect.get("effects", {}).get("inventory_remove", []):
			if it:
				self._remove_from_inventory(it)
				inv_changed = True

		# state changes
		for k, v in effect.get("effects", {}).get("state", {}).items():
			self.engine.player.state[k] = v

		# stats modifications: can be numbers to set or sign-prefixed increments
		stats_block = effect.get("effects", {}).get("stats", {})
		for k, v in stats_block.items():
			# support integer set or incremental value (e.g., 1 or "+1")
			cur = self.engine.player.stats.get(k, 0)
			if isinstance(v, str) and (v.startswith("+") or v.startswith("-")):
				try:
					cur += int(v)
				except ValueError:
					pass
				self.engine.player.stats[k] = cur
			elif isinstance(v, (int, float)):
				# treat as increment:
				self.engine.player.stats[k] = cur + v
			else:
				# fallback: set as-is
				self.engine.player.stats[k] = v

		# notify engine that inventory changed so UI can refresh
		if inv_changed:
			try:
				self.engine._inventory_changed = True
			except Exception:
				pass

		return "\n".join(parts)

	def _go(self, direction):
		"""Navigate to an exit: supports both compass directions and named locations."""
		if self.engine.player.state.get("sitting"):
			return "You need to stand up first."
		
		room = self.engine.rooms[self.engine.player.current_room]
		exits = room.exits
		
		# Handle old-style exits (backward compatibility): "exits": {"north": "room_id"}
		if not exits:
			return "There are no exits here."
		
		# Check for exact exit match (handles both old string format and new dict format)
		target_room_id = None
		exit_info = None
		
		if direction in exits:
			exit_data = exits[direction]
			if isinstance(exit_data, str):
				# Old format: direct room ID
				target_room_id = exit_data
			elif isinstance(exit_data, dict):
				# New format: exit object
				target_room_id = exit_data.get("target")
				exit_info = exit_data
		
		if not target_room_id or target_room_id not in self.engine.rooms:
			# Show available exits based on location type
			location_type = room.__dict__.get('location_type', 'wilderness')
			return self._describe_exits(room, location_type)
		
		# Move player
		self.engine.player.current_room = target_room_id
		dest_room = self.engine.rooms[target_room_id]
		
		# Show transition text if available
		if exit_info and isinstance(exit_info, dict):
			transition_text = exit_info.get("transition_text")
			if transition_text:
				result = f"{transition_text}\n\n"
				result += dest_room.describe()
				return result
		
		return dest_room.describe()
	
	def _describe_exits(self, room, location_type="wilderness"):
		"""Format exit description based on location type."""
		exits = room.exits or {}
		if not exits:
			return "There are no exits here."
		
		directional = []
		named = []
		
		for direction, exit_data in exits.items():
			if isinstance(exit_data, str):
				# Old format
				if direction in {"north", "south", "east", "west"}:
					directional.append(direction)
				else:
					named.append(direction)
			elif isinstance(exit_data, dict):
				# New format
				exit_type = exit_data.get("type", "direction")
				display = exit_data.get("display", direction)
				if exit_type == "direction":
					directional.append(direction)
				else:
					named.append(display)
		
		parts = []
		
		if location_type == "settlement" or location_type == "building":
			if named:
				parts.append(f"You can travel to: {', '.join(named)}")
			if directional:
				parts.append(f"Compass directions: {', '.join(directional)}")
		else:
			# Wilderness style
			if directional:
				parts.append(f"Exits: {', '.join(directional)}")
			if named:
				parts.append(f"You can also travel to: {', '.join(named)}")
		
		if not parts:
			return "There are no exits here."
		
		return "\n".join(parts)

	def _look(self):
		room = self.engine.rooms[self.engine.player.current_room]
		return room.describe()

	# helper inventory modifiers
	def _add_to_inventory(self, item_name, count=1):
		if not item_name:
			return
		inv = self.engine.player.inventory
		inv[item_name] = inv.get(item_name, 0) + int(count)

	def _remove_from_inventory(self, item_name, count=1):
		inv = self.engine.player.inventory
		if item_name not in inv:
			return False
		try:
			cnt = int(count)
		except Exception:
			cnt = 1
		if inv[item_name] > cnt:
			inv[item_name] -= cnt
		else:
			# remove key
			inv.pop(item_name, None)
		return True

	def _collect(self, item_spec):
		"""Collect an item from the current room into the player's inventory.
		Supports: 'collect <item>' or 'collect <N> <item>' where N is an integer count.
		"""
		if not self.engine.player:
			return "No game in progress."
		room = self.engine.rooms.get(self.engine.player.current_room)
		if room is None:
			return "You are nowhere."

		spec = (item_spec or "").strip()
		if not spec:
			return "Collect what?"
		# parse optional leading count
		toks = spec.split()
		count = 1
		item = spec
		if toks:
			try:
				first = int(toks[0])
				if first > 0 and len(toks) > 1:
					count = first
					item = " ".join(toks[1:])
			except Exception:
				# not a number; treat entire spec as item name
				item = spec

		item = item.strip()
		if not item:
			return "Collect what?"

		available = room.items.count(item)
		if available <= 0:
			return "There is no such item here."
		to_take = min(count, available)
		# remove that many occurrences from room.items
		removed = 0
		for _ in range(to_take):
			try:
				room.items.remove(item)
				removed += 1
			except ValueError:
				break
		if removed <= 0:
			return "There is no such item here."
		# add to player's inventory
		self._add_to_inventory(item, removed)
		try:
			self.engine._inventory_changed = True
		except Exception:
			pass
		if removed == 1:
			return f"collected `{item}`"
		else:
			return f"collected {removed} `{item}`"

	def _drop(self, item_name):
		"""Drop an item from the player's inventory into the current room.
		Decrement count, and add to room.items.
		"""
		if not self.engine.player:
			return "No game in progress."
		item_name = item_name.strip()
		if not item_name:
			return "Drop what?"
		inv = self.engine.player.inventory
		if item_name in inv:
			# decrement count or remove
			if inv[item_name] > 1:
				inv[item_name] -= 1
			else:
				inv.pop(item_name, None)
			# add to current room items
			room = self.engine.rooms.get(self.engine.player.current_room)
			if room is None:
				# put it back if something goes wrong
				inv[item_name] = inv.get(item_name, 0) + 1
				return "You are nowhere to drop that."
			# add an instance to room items (allow duplicates)
			room.items.append(item_name)
			# mark inventory changed for UI
			try:
				self.engine._inventory_changed = True
			except Exception:
				pass
			return f"You drop the {item_name}."
		else:
			return "You don't have that."

	def _inventory(self):
		inv = self.engine.player.inventory
		if inv:
			parts = []
			for k, v in inv.items():
				parts.append(f"{k} x{v}")
			return "You are carrying: " + ", ".join(parts)
		else:
			return "You are carrying nothing."

	def _help(self):
		return "Commands: go [dir], look, collect [item], drop [item], inventory, save, load, quit\nRooms may also define custom actions (try commands specific to the room)."

	def _examine(self, target):
		# check inventory and room items
		if target in self.engine.player.inventory:
			return f"You look closely at the {target}. It looks ordinary."
		room = self.engine.rooms[self.engine.player.current_room]
		if target in room.items:
			return f"You examine the {target} in the room. It looks useful."
		return "You don't see that here."

	def _sell(self, item_name):
		"""Sell one unit of item_name for its worth (in gold)."""
		if not self.engine.player:
			return "No game in progress."
		item_name = item_name.strip()
		if not item_name:
			return "Sell what?"
		inv = self.engine.player.inventory
		if item_name not in inv or inv[item_name] <= 0:
			return "You don't have that."
		# lookup worth (must be present in engine.item_worth)
		worth_map = getattr(self.engine, "item_worth", {}) or {}
		if item_name not in worth_map:
			return "That can't be sold."
		try:
			price = int(worth_map.get(item_name, 0))
		except Exception:
			price = 0
		# remove one from inventory
		self._remove_from_inventory(item_name, 1)
		# add gold to player's stats
		self.engine.player.stats["gold"] = int(self.engine.player.stats.get("gold", 0)) + price
		# notify UI
		try:
			self.engine._inventory_changed = True
		except Exception:
			pass
		return f"You sold 1 {item_name} for {price} gold."


class GameEngine:
	"""Main engine: loads world, manages game state, save/load functionality.
	All public methods return strings to be displayed by the UI.
	"""
	def __init__(self, world_file=WORLD_FILE):
		self.world_file = world_file
		self.rooms = {}  # name -> Room
		self.player = None
		self.cmd = None
		self.should_quit = False
		self.sample_world_created = False  # set True if we auto-create a sample world.json
		# defaults loaded from world: default stats and global commands
		self.default_stats = {}
		self.global_commands = {}
		# default starting inventory from world.json (if present) - list form in world; convert to dict for runtime
		self.default_inventory = []
		# runtime flag to indicate inventory changed (UI may poll or check after commands)
		self._inventory_changed = False
		# item worth mapping (item_name -> int gold)
		self.item_worth = {}
		self.load_world()

	def load_world(self):
		# If world file does not exist, create a sample (so users can edit it without touching code)
		if not os.path.exists(self.world_file):
			sample = {
				"start_room": "Village",
				"rooms": {
					"Village": {
						"description": "A small peaceful village. A path leads north to a Forest.",
						"exits": {"north": "Forest"},
						"items": ["map"],
						"actions": {
							"look at well": "The old well is dry, but you see carved symbols on the rim."
						}
					},
					"Forest": {
						"description": "A dark forest filled with tall trees. A cave mouth yawns to the east.",
						"exits": {"south": "Village", "east": "Cave"},
						"items": ["stick"],
						"actions": {
							"climb tree": "You climb a low branch and get a better view of the surroundings."
						}
					},
					"Cave": {
						"description": "A damp cave. It's dim but you spot something glinting deeper inside.",
						"exits": {"west": "Forest"},
						"items": ["old coin"],
						"actions": {
							"search": "You search the cave and find an old coin half-buried in mud."
						}
					}
				}
			}
			try:
				with open(self.world_file, "w", encoding="utf-8") as f:
					json.dump(sample, f, indent=2)
				self.sample_world_created = True
			except Exception as e:
				# If writing fails, raise so GUI can show an error
				raise RuntimeError(f"Failed to create sample world file: {e}")

		# Load the world file
		try:
			with open(self.world_file, "r", encoding="utf-8") as f:
				data = json.load(f)
		except FileNotFoundError:
			# shouldn't happen because we auto-created above, but keep safety
			raise FileNotFoundError(f"World file not found: {self.world_file}")
		except Exception as e:
			# Any JSON parse error or IO error should be reported
			raise RuntimeError(f"Failed to load world file: {e}")

		# create rooms
		self.rooms = {}
		rooms_data = data.get("rooms", {})
		# load item worth mapping if present
		raw_worth = data.get("item_worth", {}) or {}
		if isinstance(raw_worth, dict):
			wmap = {}
			for k, v in raw_worth.items():
				try:
					wmap[str(k)] = int(v)
				except Exception:
					try:
						wmap[str(k)] = int(float(v))
					except Exception:
						wmap[str(k)] = 0
			self.item_worth = wmap
		else:
			self.item_worth = {}
		for rname, rdata in rooms_data.items():
			if not isinstance(rdata, dict):
				continue
			rdata.setdefault("description", "")
			rdata.setdefault("exits", {})
			# support 'items' as either list (legacy) or dict mapping item->count (new)
			raw_items = rdata.get("items", []) if ("items" in rdata) else []
			if isinstance(raw_items, dict):
				# expand mapping into a list with repeated entries
				items_expanded = []
				for it, cnt in raw_items.items():
					try:
						n = int(cnt)
					except Exception:
						try:
							n = int(float(cnt))
						except Exception:
							n = 1
					for _ in range(max(0, n)):
						items_expanded.append(str(it))
				rdata["items"] = items_expanded
			else:
				# assume list-like; coerce to list of strings
				rdata["items"] = [str(it) for it in (raw_items or [])]
			rdata.setdefault("actions", {})
			# Normalize actions: allow "action": "response string", old {"response":...}, or new structured form
			normalized_actions = {}
			for act_cmd, act_val in rdata.get("actions", {}).items():
				if isinstance(act_val, str):
					# simple string => text-only action
					normalized_actions[act_cmd] = {"text": act_val}
				elif isinstance(act_val, dict):
					# map legacy 'response' to 'text' for consistency
					act_copy = dict(act_val)
					if "response" in act_copy and "text" not in act_copy:
						act_copy["text"] = act_copy.pop("response")
					# keep 'effects' and 'conditions' if present
					normalized_actions[act_cmd] = act_copy
				else:
					continue
			rdata["actions"] = normalized_actions
			rdata.setdefault("name", rname)
			self.rooms[rname] = Room(rdata)
		# after reading `data` from JSON file:
		# load default stats and global commands
		self.default_stats = dict(data.get("default_stats", {}))
		# Normalize default_inventory: support both dict and list in world.json
		raw_def_inv = data.get("default_inventory", {}) if ("default_inventory" in data) else {}
		if isinstance(raw_def_inv, dict):
			# already dict of counts
			self.default_inventory = {str(k): int(v) for k, v in raw_def_inv.items()}
		elif isinstance(raw_def_inv, list):
			# convert list to dict counts
			agg = {}
			for it in raw_def_inv:
				if it is None:
					continue
				agg[str(it)] = agg.get(str(it), 0) + 1
			self.default_inventory = agg
		else:
			# fallback empty dict
			self.default_inventory = {}

		gcmds = data.get("global_commands", {}) or {}
		# normalize global commands: allow string or dict
		n_gcmds = {}
		for cmd, val in gcmds.items():
			if isinstance(val, str):
				n_gcmds[cmd] = {"text": val, "effects": {}}
			elif isinstance(val, dict):
				vcopy = dict(val)
				# legacy 'response' -> 'text'
				if "response" in vcopy and "text" not in vcopy:
					vcopy["text"] = vcopy.pop("response")
				# ensure effects key exists
				vcopy.setdefault("effects", {})
				n_gcmds[cmd] = vcopy
		self.global_commands = n_gcmds

		# Determine start room: prefer "start_room", fall back to legacy "start"
		self.start_room = data.get("start_room") or data.get("start") or (next(iter(self.rooms)) if self.rooms else None)
		# handler
		self.cmd = CommandHandler(self)
		# ensure item_worth exists even if not in file
		self.item_worth = getattr(self, "item_worth", {}) or {}

	def new_game(self):
		if not self.start_room:
			return "No start room defined."
		self.player = Player(self.start_room)
		# initialize player stats with defaults from world
		self.player.stats = dict(self.default_stats)
		# initialize player inventory from default_inventory (dict counts)
		inv = {}
		for it, cnt in (self.default_inventory or {}).items():
			try:
				c = int(cnt)
			except Exception:
				c = 1
			if it:
				inv[str(it)] = inv.get(str(it), 0) + max(0, c)
		self.player.inventory = inv
		self.should_quit = False
		# reset inventory-changed flag
		self._inventory_changed = True
		out = []
		out.append("Starting new game...")
		out.append(self.rooms[self.player.current_room].describe())
		return "\n".join(out)

	def save_game(self, path=SAVE_FILE):
		"""Persist runtime game state to path.
		Stores player's full state and the current per-room items so collected items stay removed.
		"""
		if not self.player:
			return "No game in progress to save."

		# Build a save structure containing only runtime-modified state (player + room items)
		state = {
			"player": self.player.to_dict(),  # inventory serialized as dict by Player.to_dict()
			"rooms": {}
		}
		for name, room in self.rooms.items():
			# persist only the dynamic item list for each room
			# save as aggregated mapping item -> count so editor/game show counts consistently
			item_counts = {}
			for it in (room.items or []):
				if it is None:
					continue
				item_counts[str(it)] = item_counts.get(str(it), 0) + 1
			state["rooms"][name] = {"items": item_counts}
		# persist item worth mapping so save contains current worth table (helps editors/changes)
		state["item_worth"] = {str(k): int(v) for k, v in (self.item_worth or {}).items()}

		# Write atomically
		tmp_path = f"{path}.tmp"
		try:
			with open(tmp_path, "w", encoding="utf-8") as f:
				json.dump(state, f, indent=2, ensure_ascii=False)
			# Use os.replace for atomic swap across platforms
			os.replace(tmp_path, path)
			# reset inventory-changed flag after successful save
			self._inventory_changed = False
			return f"Game saved to {path}."
		except Exception as e:
			# attempt to clean up tmp file if present
			try:
				if os.path.exists(tmp_path):
					os.remove(tmp_path)
			except Exception:
				pass
			return f"Failed to save: {e}"

	def load_game(self, path=SAVE_FILE, interactive=True):
		"""Load runtime state previously saved with save_game.
		Only applies player state and per-room item lists; other room definitions from the world file remain intact.
		"""
		if not os.path.exists(path):
			return "No savegame found."

		try:
			with open(path, "r", encoding="utf-8") as f:
				state = json.load(f)
		except Exception as e:
			return f"Failed to load save: {e}"

		# Validate and restore player (supports both dict and legacy list formats)
		player_data = state.get("player")
		if not isinstance(player_data, dict):
			return "Save file is corrupted (missing player data)."

		try:
			self.player = Player.from_dict(player_data)
		except Exception as e:
			return f"Failed to restore player from save: {e}"
		# if saved, restore item_worth mapping (optional)
		if isinstance(state.get("item_worth"), dict):
			wmap = {}
			for k, v in state.get("item_worth", {}).items():
				try:
					wmap[str(k)] = int(v)
				except Exception:
					try:
						wmap[str(k)] = int(float(v))
					except Exception:
						wmap[str(k)] = 0
			self.item_worth = wmap
		# ensure item_worth exists
		self.item_worth = getattr(self, "item_worth", {}) or {}

		# Apply saved per-room item lists without touching other room metadata.
		rooms_state = state.get("rooms", {})
		if isinstance(rooms_state, dict):
			for name, info in rooms_state.items():
				if name in self.rooms and isinstance(info, dict):
					raw_items = info.get("items")
					expanded = None
					# support mapping (item->count) or legacy list
					if isinstance(raw_items, dict):
						exp = []
						for it, cnt in raw_items.items():
							try:
								n = int(cnt)
							except Exception:
								try:
									n = int(float(cnt))
								except Exception:
									n = 1
							for _ in range(max(0, n)):
								exp.append(str(it))
						expanded = exp
					elif isinstance(raw_items, list):
						expanded = [str(it) for it in raw_items]
					# Apply expanded list if available
					if isinstance(expanded, list):
						if expanded:
							self.rooms[name].items = expanded
						else:
							# saved empty => preserve world items if present
							if not self.rooms[name].items:
								self.rooms[name].items = []
		# Ensure flags
		self.should_quit = False
		# signal that inventory changed so UI may refresh
		self._inventory_changed = True

		out = [f"Loaded game from {path}."]
		# If player's current room exists in world, show its description; otherwise choose a fallback
		cur = getattr(self.player, "current_room", None)
		if cur and cur in self.rooms:
			out.append(self.rooms[cur].describe())
		else:
			# fallback to engine start room
			if self.start_room and self.start_room in self.rooms:
				self.player.current_room = self.start_room
				out.append(self.rooms[self.start_room].describe())
			else:
				out.append("Loaded game, but current room not found in world.")
		return "\n".join(out)

	def process_command(self, cmd: str):
		"""Process a command string and return the text output for display.
		The GUI should prepend the echoed input (e.g. '> cmd') itself if desired.
		"""
		if not self.player:
			return "No game in progress. Start a new game or load one."
		response = self.cmd.handle(cmd)
		return response or ""


# GUI code: keep in same file for now; inventory UI updated to show Item | Count and search
class AdventureGUI:
	def __init__(self, root):
		# Maximize window on launch
		root.state("zoomed")
		self.root = root
		self.root.title("Unitopia-style Adventure Game")
		# Styling
		self.font = font.Font(family="Courier New", size=10)

		# Text area (read-only for user typing) - create immediately
		self.text = tk.Text(root, wrap="word", bg="#1e1e1e", fg="#dcdcdc", insertbackground="#dcdcdc",
							state="disabled", font=self.font)
		self.text.pack(fill="both", expand=True, padx=6, pady=(6, 0))
		# Scrollbar
		self.scroll = tk.Scrollbar(self.text)
		self.scroll.pack(side="right", fill="y")
		self.text.config(yscrollcommand=self.scroll.set)
		self.scroll.config(command=self.text.yview)

		# Controls frame (keeps layout consistent) with Inventory toggle
		self.controls = tk.Frame(root)
		self.controls.pack(fill="x", padx=6)
		# Inventory toggle button
		self.inv_button = tk.Button(self.controls, text="Inventory", command=self.toggle_inventory_window)
		self.inv_button.pack(side="left", padx=(0, 6))
		# Stats toggle button (placed beside Inventory)
		self.stats_button = tk.Button(self.controls, text="Stats", command=self.toggle_stats_window)
		self.stats_button.pack(side="left", padx=(0,6))
		# Debug toggle button (placed beside Stats)
		self.debug_button = tk.Button(self.controls, text="Debug", command=self.toggle_debug_window)
		self.debug_button.pack(side="left", padx=(0,6))
		# Small status label (optional) to match UI style
		self.status_label = tk.Label(self.controls, text="", font=self.font)
		self.status_label.pack(side="left")

		# Entry for commands - created early so user can type immediately
		self.entry = tk.Entry(root, bg="#2e2e2e", fg="#ffffff", insertbackground="#ffffff", font=self.font)
		self.entry.pack(fill="x", padx=6, pady=6)
		# Ensure entry can take focus immediately
		try:
			self.entry.focus_set()
			self.root.after(0, lambda: self.entry.focus_set())
		except Exception:
			pass

		# Bindings
		self.entry.bind("<Return>", self.on_enter)
		root.bind("<Control-s>", self.on_save_shortcut)
		root.bind("<Control-S>", self.on_save_shortcut)
		root.bind("<Control-l>", self.on_load_shortcut)
		root.bind("<Control-L>", self.on_load_shortcut)

		# Engine will be initialized shortly via _init_engine to avoid blocking UI draw
		self.engine = None

		# Inventory window handle (Toplevel or None)
		self.inventory_win = None
		self.inv_listbox = None
		self.inv_examine_btn = None
		self.inv_drop_btn = None
		self.inv_search_var = None

		# Stats window references
		self.stats_win = None
		self.stats_listbox = None

		# Debug window references
		self.debug_win = None
		self.debug_listbox = None

		# Show a minimal welcome immediately
		self.append("Welcome to the Unitopia-style adventure!")
		# Defer engine creation so the UI is responsive immediately
		self.root.after(50, self._init_engine)
		# Ensure closing the window goes through our quit handler so we can save
		self.root.protocol("WM_DELETE_WINDOW", lambda: self._on_app_quit())

	def _on_app_quit(self):
		"""Save game (if running) and close the application."""
		try:
			# Attempt to save current game state if available
			if getattr(self, "engine", None) and getattr(self.engine, "player", None):
				msg = self.engine.save_game()
				# show save result in console if possible
				try:
					self.append(msg)
				except Exception:
					pass
		except Exception:
			# ignore save errors on shutdown
			pass
		# Destroy main window (end app)
		try:
			self.root.destroy()
		except Exception:
			try:
				self.root.quit()
			except Exception:
				pass

	def _init_engine(self):
		"""Initialize GameEngine after the GUI has been drawn to avoid startup delay."""
		try:
			self.engine = GameEngine()
		except Exception as e:
			messagebox.showerror("Error", str(e))
			self.root.destroy()
			return

		# Inform the user if we auto-created a sample world.json
		if getattr(self.engine, "sample_world_created", False):
			self.append(f"A sample world.json was created at:\n{self.engine.world_file}\nEdit it to expand your world.")

		# Start: if a save exists, load it automatically; otherwise start new game
		if os.path.exists(SAVE_FILE):
			msg = self.engine.load_game()
			self.append(msg)
			# If load failed to create a player, fall back to new game
			if self.engine.player is None:
				msg = self.engine.new_game()
				self.append(msg)
		else:
			msg = self.engine.new_game()
			self.append(msg)

		# Ensure inventory UI reflects current state
		self.refresh_inventory_display()
		try:
			self.root.after(0, lambda: self.entry.focus_set())
		except Exception:
			pass

	def append(self, text):
		# Append text to console area and auto-scroll
		self.text.config(state="normal")
		self.text.insert("end", text + "\n\n")
		self.text.config(state="disabled")
		self.text.see("end")

	def on_enter(self, event=None):
		# Always ensure entry is ready to accept input
		cmd = self.entry.get().strip()
		if not cmd:
			try:
				self.root.after(0, lambda: self.entry.focus_set())
			except Exception:
				pass
			return "break"

		# Echo command in console
		self.append(f"> {cmd}")

		# If engine not ready yet, inform user and do not block
		if not self.engine:
			self.append("Engine is still loading. Please wait...")
			self.entry.delete(0, "end")
			try:
				self.root.after(0, lambda: self.entry.focus_set())
			except Exception:
				pass
			return "break"

		# Process via engine
		resp = self.engine.process_command(cmd)
		if resp:
			self.append(resp)

		# Clear entry and refocus immediately so typing feels responsive
		self.entry.delete(0, "end")
		try:
			self.root.after(0, lambda: self.entry.focus_set())
		except Exception:
			pass

		# Refresh inventory display because commands may have changed inventory
		self.refresh_inventory_display()

		# If engine requested quit, close the GUI
		if getattr(self.engine, "should_quit", False):
			self.append("Exiting...")
			# give UI a moment to show the message, then save + quit
			self.root.after(250, lambda: self._on_app_quit())
		return "break"

	def on_save_shortcut(self, event=None):
		if not self.engine:
			self.append("Engine not ready: cannot save yet.")
			try:
				self.root.after(0, lambda: self.entry.focus_set())
			except Exception:
				pass
			return "break"
		msg = self.engine.save_game()
		self.append(msg)
		# save doesn't change inventory, but keep consistent
		self.refresh_inventory_display()
		try:
			self.root.after(0, lambda: self.entry.focus_set())
		except Exception:
			pass
		return "break"

	def on_load_shortcut(self, event=None):
		if not self.engine:
			self.append("Engine not ready: cannot load yet.")
			try:
				self.root.after(0, lambda: self.entry.focus_set())
			except Exception:
				pass
			return "break"
		msg = self.engine.load_game()
		self.append(msg)
		# After loading, inventory and room items are updated — refresh UI
		self.refresh_inventory_display()
		try:
			self.root.after(0, lambda: self.entry.focus_set())
		except Exception:
			pass
		return "break"

	# Inventory window management and actions
	def toggle_inventory_window(self):
		"""Open or close the Inventory Toplevel window."""
		if self.inventory_win and tk.Toplevel.winfo_exists(self.inventory_win):
			try:
				self.inventory_win.destroy()
			except Exception:
				pass
			self.inventory_win = None
			self.inv_listbox = None
			self.inv_search_var = None
			return
		self.build_inventory_window()

	def build_inventory_window(self):
		"""Create the Inventory Toplevel window with Listbox and action buttons and search."""
		if self.inventory_win and tk.Toplevel.winfo_exists(self.inventory_win):
			return
		win = tk.Toplevel(self.root)
		win.title("Inventory")
		win.geometry("400x500")
		win.resizable(True, True)
		# Make window visually similar: use same font
		frame = tk.Frame(win, padx=6, pady=6)
		frame.pack(fill="both", expand=True)

		tk.Label(frame, text="Player Inventory", font=self.font).pack(anchor="w")
		# Search field
		self.inv_search_var = tk.StringVar()
		search_frame = tk.Frame(frame)
		search_frame.pack(fill="x", pady=(4, 4))
		tk.Label(search_frame, text="Search:", font=self.font).pack(side="left")
		search_entry = tk.Entry(search_frame, textvariable=self.inv_search_var, font=self.font)
		search_entry.pack(side="left", fill="x", expand=True, padx=(6, 0))
		# Bind to update display on change
		self.inv_search_var.trace_add("write", lambda *a: self.refresh_inventory_display())

		# Listbox with item | count display
		listbox = tk.Listbox(frame, height=16, font=self.font)
		listbox.pack(fill="both", expand=True, pady=(4,6))
		listbox.bind("<<ListboxSelect>>", lambda e: self._on_inv_select())

		btn_frame = tk.Frame(frame)
		btn_frame.pack(fill="x", pady=4)
		examine_btn = tk.Button(btn_frame, text="Examine", width=12, command=self.inv_examine)
		examine_btn.pack(side="left", padx=4)
		drop_btn = tk.Button(btn_frame, text="Drop", width=12, command=self.inv_drop)
		drop_btn.pack(side="left", padx=4)

		# Keep references
		self.inventory_win = win
		self.inv_listbox = listbox
		self.inv_examine_btn = examine_btn
		self.inv_drop_btn = drop_btn

		# Initialize state of buttons
		self._on_inv_select()

		# Populate with current inventory
		self.refresh_inventory_display()

		# When user closes window via the window manager, clear reference
		win.protocol("WM_DELETE_WINDOW", lambda: (setattr(self, "inventory_win", None), setattr(self, "inv_listbox", None), setattr(self, "inv_search_var", None), win.destroy()))

	def toggle_stats_window(self):
		"""Open or close the Stats Toplevel window."""
		if self.stats_win and tk.Toplevel.winfo_exists(self.stats_win):
			try:
				self.stats_win.destroy()
			except Exception:
				pass
			self.stats_win = None
			self.stats_listbox = None
			return
		self.build_stats_window()

	def build_stats_window(self):
		"""Create the Stats Toplevel window showing player stats (gold, health, etc.)."""
		if self.stats_win and tk.Toplevel.winfo_exists(self.stats_win):
			return
		win = tk.Toplevel(self.root)
		win.title("Player Stats")
		win.geometry("300x300")
		win.resizable(True, True)
		frame = tk.Frame(win, padx=6, pady=6)
		frame.pack(fill="both", expand=True)

		tk.Label(frame, text="Current Stats", font=self.font).pack(anchor="w")
		lb = tk.Listbox(frame, height=12, font=self.font)
		lb.pack(fill="both", expand=True, pady=(4,6))

		self.stats_win = win
		self.stats_listbox = lb

		# Populate initial values
		self.refresh_stats_display()

		# Clear references when closed
		win.protocol("WM_DELETE_WINDOW", lambda: (setattr(self, "stats_win", None), setattr(self, "stats_listbox", None), win.destroy()))

	def refresh_stats_display(self):
		"""Refresh the stats listbox (if open)."""
		try:
			if not (self.engine and self.engine.player):
				# nothing to show
				if self.stats_listbox:
					self.stats_listbox.delete(0, "end")
				return
			stats = self.engine.player.stats or {}
			# ensure at least default stats keys appear (gold, health)
			# merge defaults -> current to show sensible fields
			for k, v in (self.engine.default_stats or {}).items():
				stats.setdefault(k, v)
			if not self.stats_listbox:
				return
			self.stats_listbox.delete(0, "end")
			# show sorted for consistency
			for k in sorted(stats.keys(), key=lambda s: s.lower()):
				self.stats_listbox.insert("end", f"{k}: {stats.get(k)}")
		except Exception:
			# ignore UI errors
			pass

	def refresh_inventory_display(self):
		"""Refresh the inventory listbox (if open) and update status label."""
		# Update status label with total count (sum of counts)
		try:
			total = 0
			total_value = 0
			if self.engine and self.engine.player:
				inv = self.engine.player.inventory if isinstance(self.engine.player.inventory, dict) else {}
				total = sum(inv.values())
				# compute total value using engine.item_worth
				wmap = getattr(self.engine, "item_worth", {}) or {}
				for n, c in inv.items():
					try:
						w = int(wmap.get(n, 0))
					except Exception:
						w = 0
					total_value += w * int(c)
			# show both counts and total gold value
			self.status_label.config(text=f"Items: {total}  |  Value: {total_value}g")
		except Exception:
			try:
				self.status_label.config(text="")
			except Exception:
				pass

		# Refresh stats window (keeps gold/other stats in sync)
		try:
			if getattr(self, "stats_listbox", None) is not None:
				self.refresh_stats_display()
		except Exception:
			pass

		# Also refresh debug window if open (keeps state display in sync)
		try:
			if getattr(self, "debug_listbox", None) is not None:
				self.refresh_debug_display()
		except Exception:
			pass

		# If inventory window is open, update listbox contents
		if self.inv_listbox is None:
			return
		try:
			# read search filter
			filter_text = ""
			if self.inv_search_var:
				try:
					filter_text = self.inv_search_var.get().strip().lower()
				except Exception:
					filter_text = ""
			self.inv_listbox.delete(0, "end")
			if not (self.engine and self.engine.player):
				return
			inv = self.engine.player.inventory or {}
			wmap = getattr(self.engine, "item_worth", {}) or {}
			# Display sorted by name showing worth next to each item
			for name in sorted(inv.keys(), key=lambda s: s.lower()):
				if filter_text and filter_text not in name.lower():
					continue
				count = inv.get(name, 0)
				try:
					w = int(wmap.get(name, 0))
				except Exception:
					w = 0
				total_item_val = w * int(count)
				# format: "name | count | worth each g | total Xg"
				self.inv_listbox.insert("end", f"{name} | {count} | {w}g each | total {total_item_val}g")
			# clear selection and disable buttons until user picks an item
			self.inv_listbox.selection_clear(0, "end")
			self._on_inv_select()
		except Exception:
			# ignore UI update errors
			pass

	def _on_inv_select(self):
		"""Enable/disable inventory action buttons based on selection."""
		try:
			if not self.inv_listbox:
				return
			sel = self.inv_listbox.curselection()
			has = bool(sel)
			if self.inv_examine_btn:
				self.inv_examine_btn.config(state="normal" if has else "disabled")
			if self.inv_drop_btn:
				self.inv_drop_btn.config(state="normal" if has else "disabled")
		except Exception:
			pass

	def _get_selected_inv_item(self):
		"""Return the item name (not count) from current selection, or None."""
		try:
			if not self.inv_listbox:
				return None
			sel = self.inv_listbox.curselection()
			if not sel:
				return None
			text = self.inv_listbox.get(sel[0])
			# format "name | count"
			if " | " in text:
				name = text.split(" | ", 1)[0].strip()
			else:
				# fallback: entire text
				name = text.strip()
			return name
		except Exception:
			return None

	def inv_examine(self):
		"""Examine the selected inventory item using existing engine 'examine' command."""
		try:
			item = self._get_selected_inv_item()
			if not item:
				messagebox.showinfo("Examine", "Select an item first.")
				return
			# Use engine process_command to leverage existing examine logic
			if not self.engine:
				self.append("Engine not ready.")
				return
			resp = self.engine.process_command(f"examine {item}")
			if resp:
				self.append(resp)
			# refresh (examine doesn't change inventory)
			self.refresh_inventory_display()
			try:
				self.root.after(0, lambda: self.entry.focus_set())
			except Exception:
				pass
		except Exception as e:
			messagebox.showerror("Error", str(e))

	def inv_drop(self):
		"""Drop the selected inventory item using existing engine 'drop' command."""
		try:
			item = self._get_selected_inv_item()
			if not item:
				messagebox.showinfo("Drop", "Select an item first.")
				return
			if not self.engine:
				self.append("Engine not ready.")
				return
			# perform drop through engine to ensure room state changes correctly
			resp = self.engine.process_command(f"drop {item}")
			if resp:
				self.append(resp)
			# Refresh inventory & other views as needed
			self.refresh_inventory_display()
			try:
				self.root.after(0, lambda: self.entry.focus_set())
			except Exception:
				pass
		except Exception as e:
			messagebox.showerror("Error", str(e))

	# Debug window management
	def toggle_debug_window(self):
		"""Open or close the Debug Toplevel window."""
		if self.debug_win and tk.Toplevel.winfo_exists(self.debug_win):
			try:
				self.debug_win.destroy()
			except Exception:
				pass
			self.debug_win = None
			self.debug_listbox = None
			return
		self.build_debug_window()

	def build_debug_window(self):
		"""Create a Debug window showing current engine/player state and reset button."""
		if self.debug_win and tk.Toplevel.winfo_exists(self.debug_win):
			return
		win = tk.Toplevel(self.root)
		win.title("Debug")
		win.geometry("360x340")
		win.resizable(True, True)
		frame = tk.Frame(win, padx=6, pady=6)
		frame.pack(fill="both", expand=True)

		tk.Label(frame, text="Debug Menu", font=self.font).pack(anchor="w")
		lb = tk.Listbox(frame, height=12, font=self.font)
		lb.pack(fill="both", expand=True, pady=(4,6))

		btn_frame = tk.Frame(frame)
		btn_frame.pack(fill="x")
		reset_btn = tk.Button(btn_frame, text="Reset Save / Restart", command=self._debug_reset_save)
		reset_btn.pack(side="left", padx=4)
		close_btn = tk.Button(btn_frame, text="Close", command=lambda: win.destroy())
		close_btn.pack(side="left", padx=4)

		self.debug_win = win
		self.debug_listbox = lb

		# Populate initial values
		self.refresh_debug_display()

		# Clear refs when closed
		win.protocol("WM_DELETE_WINDOW", lambda: (setattr(self, "debug_win", None), setattr(self, "debug_listbox", None), win.destroy()))

	def refresh_debug_display(self):
		"""Refresh debug listbox to show current player.state key/value pairs."""
		try:
			if not (self.engine and self.engine.player):
				if self.debug_listbox:
					self.debug_listbox.delete(0, "end")
				return
			state = self.engine.player.state or {}
			# always show at least an empty state
			if not self.debug_listbox:
				return
			self.debug_listbox.delete(0, "end")
			if not state:
				self.debug_listbox.insert("end", "(no flags set)")
			else:
				for k in sorted(state.keys(), key=lambda s: s.lower()):
					self.debug_listbox.insert("end", f"{k}: {state.get(k)}")
		except Exception:
			pass

	def _debug_reset_save(self):
		"""Delete the save file and restart a fresh game."""
		try:
			if not messagebox.askyesno("Reset Save", "Delete saved game and restart? This cannot be undone."):
				return
			# remove save file if exists
			try:
				if os.path.exists(SAVE_FILE):
					os.remove(SAVE_FILE)
			except Exception as e:
				# inform but continue to restart
				try:
					messagebox.showwarning("Warning", f"Failed to remove save file: {e}")
				except Exception:
					pass
			# reload world definitions from disk so room items are restored to world.json values,
			# then start a fresh game instance. This prevents in-memory mutations from persisting.
			if getattr(self, "engine", None):
				try:
					self.engine.load_world()
				except Exception:
					# if reload fails, continue and attempt to start a new game anyway
					pass
				msg = self.engine.new_game()
				# ensure stats and inventory windows refresh
				try:
					self.refresh_inventory_display()
					self.refresh_stats_display()
					self.refresh_debug_display()
				except Exception:
					pass
				# show feedback
				try:
					self.append("Save deleted. Restarted a new game.")
					if msg:
						self.append(msg)
				except Exception:
					pass
		except Exception as e:
			messagebox.showerror("Error", str(e))


def main():
	# Start GUI directly (no console interaction)
	root = tk.Tk()
	app = AdventureGUI(root)
	root.mainloop()


if __name__ == "__main__":
	main()

# Notes on splitting engine vs GUI later:
# - Move GameEngine, Room, Player, CommandHandler into engine_core.py and import them from a small gui.py that only contains AdventureGUI.
# - Add buttons or menus by creating tk.Menu and adding commands that call app.on_save_shortcut / app.on_load_shortcut / app.on_enter.
# - To add more UI elements (inventory panel, map), create frames beside the text area and update them when the game state changes.
# - The engine exposes save_game/load_game/process_command which makes integration with other UIs straightforward.
