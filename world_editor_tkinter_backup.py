import json
import os
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog, font, ttk

WORLD_FILE = os.path.join(os.path.dirname(__file__), "world.json")


class WorldEditor:
	def __init__(self, root):
		self.root = root
		self.root.title("Adventure World Editor")
		self.font = font.Font(family="Segoe UI Mono", size=10)

		# Data model: {"start_room": None or str, "rooms": {name: {description, exits, items, actions}}}
		self.world = {"start_room": None, "rooms": {}}
		self.world_data = self.world  # alias for compatibility with caller code
		self.current_room = None
		self.world_path = WORLD_FILE

		# Build UI
		self.build_ui()

		# Load or create blank world
		if os.path.exists(self.world_path):
			if not self.load_world(self.world_path):
				self.create_blank_world()
		else:
			# create a blank world so user can immediately start
			self.create_blank_world()
			# suggest saving to disk
			messagebox.showinfo("Blank world", f"No world found. A blank world was created in memory.\nUse Save World to write to {self.world_path}")

		self.refresh_room_list()

	def build_ui(self):
		# Use a Notebook to separate "Room Editor" and "Commands & Stats"
		self.notebook = ttk.Notebook(self.root)
		self.notebook.pack(fill="both", expand=True)

		# Tabs
		self.room_tab = tk.Frame(self.notebook)
		self.cmd_tab = tk.Frame(self.notebook)
		self.notebook.add(self.room_tab, text="Room Editor")
		self.notebook.add(self.cmd_tab, text="Commands & Stats")

		# Build room editor inside self.room_tab (reuse original layout but attach to tab)
		parent = self.room_tab
		# Left = rooms, right = room editor (same layout as before, but parented to 'parent')
		left = tk.Frame(parent, padx=6, pady=6)
		left.pack(side="left", fill="y")
		right = tk.Frame(parent, padx=6, pady=6)
		right.pack(side="right", fill="both", expand=True)

		# Left: Room list and controls
		tk.Label(left, text="Rooms").pack(anchor="w")
		self.room_list = tk.Listbox(left, width=28, height=22, font=self.font)
		self.room_list.pack()
		# bind selection lazily
		self.room_list.bind("<<ListboxSelect>>", lambda e: self._call_method("on_room_select", e))

		# Add a read-only label showing the current start room (requirement)
		self.start_label = tk.Label(left, text="Current Start: None", fg="blue")
		self.start_label.pack(anchor="w", pady=(4, 6))

		btn_frame = tk.Frame(left)
		btn_frame.pack(fill="x", pady=6)
		# use lazy call wrappers so attribute lookup happens on click, not during build
		tk.Button(btn_frame, text="Add", width=8, command=lambda: self._call_method("add_room")).pack(side="left")
		tk.Button(btn_frame, text="Rename", width=8, command=lambda: self._call_method("rename_room")).pack(side="left")
		tk.Button(btn_frame, text="Delete", width=8, command=lambda: self._call_method("delete_room")).pack(side="left")
		# existing Set as Start button already wired to set_start_room via lazy call
		tk.Button(left, text="Set as Start", command=lambda: self._call_method("set_start_room")).pack(fill="x", pady=(6, 0))

		# Save / Load buttons
		io_frame = tk.Frame(left)
		io_frame.pack(fill="x", pady=8)
		tk.Button(io_frame, text="Load World...", command=lambda: self._call_method("load_world_dialog")).pack(fill="x")
		tk.Button(io_frame, text="Save World...", command=lambda: self._call_method("save_world_dialog")).pack(fill="x", pady=(6,0))

		# Right: Editor panels
		# Top: Name and preview of start-room indicator
		name_frame = tk.Frame(right)
		name_frame.pack(fill="x")
		tk.Label(name_frame, text="Room Name").pack(anchor="w")
		self.name_var = tk.StringVar()
		self.name_entry = tk.Entry(name_frame, textvariable=self.name_var, font=self.font)
		self.name_entry.pack(fill="x")
		# Note: renaming is handled via Rename button to correctly update dict keys.
		tk.Label(name_frame, text="(Use Rename to change the room key)").pack(anchor="w")

		# Description
		tk.Label(right, text="Description").pack(anchor="w", pady=(6,0))
		self.desc_text = tk.Text(right, height=5, font=self.font, wrap="word")
		self.desc_text.pack(fill="x")

		# Exits editor
		exits_frame = tk.LabelFrame(right, text="Exits (direction -> room)")
		exits_frame.pack(fill="x", pady=(6,0))
		self.exits_list = tk.Listbox(exits_frame, height=4, font=self.font)
		self.exits_list.pack(fill="x")
		eadd = tk.Frame(exits_frame)
		eadd.pack(fill="x", pady=4)
		self.exit_dir = tk.Entry(eadd, width=12, font=self.font)
		self.exit_dir.pack(side="left")
		self.exit_target_var = tk.StringVar()
		self.exit_target_menu = tk.OptionMenu(eadd, self.exit_target_var, "")
		self.exit_target_menu.config(width=16)
		self.exit_target_menu.pack(side="left", padx=6)
		# Exits editor: use lazy wrappers for add/remove
		tk.Button(eadd, text="Add Exit", command=lambda: self._call_method("add_exit")).pack(side="left", padx=4)
		tk.Button(eadd, text="Remove Exit", command=lambda: self._call_method("remove_exit")).pack(side="left", padx=4)

		# Items editor
		items_frame = tk.LabelFrame(right, text="Items")
		items_frame.pack(fill="x", pady=(6,0))
		self.items_list = tk.Listbox(items_frame, height=4, font=self.font)
		self.items_list.pack(fill="x")
		iadd = tk.Frame(items_frame)
		iadd.pack(fill="x", pady=4)
		self.item_entry = tk.Entry(iadd, font=self.font)
		self.item_entry.pack(side="left", fill="x", expand=True)
		# small count entry so user can add multiple copies at once
		self.item_count_entry = tk.Entry(iadd, width=6, font=self.font)
		self.item_count_entry.pack(side="left", padx=6)
		self.item_count_entry.insert(0, "1")
		# Items editor: bind selection lazily and button commands lazily
		tk.Button(iadd, text="Add", command=lambda: self._call_method("add_item")).pack(side="left", padx=4)
		tk.Button(iadd, text="Remove", command=lambda: self._call_method("remove_item")).pack(side="left", padx=4)

		# Actions editor
		actions_frame = tk.LabelFrame(right, text="Actions (command -> response)")
		actions_frame.pack(fill="both", expand=True, pady=(6,0))
		self.actions_list = tk.Listbox(actions_frame, font=self.font, height=6)
		self.actions_list.pack(fill="both", expand=True)
		self.actions_list.bind("<<ListboxSelect>>", lambda e: self._call_method("on_action_select", e))
		act_controls = tk.Frame(actions_frame)
		act_controls.pack(fill="x", pady=4)
		self.act_cmd_entry = tk.Entry(act_controls, font=self.font)
		self.act_cmd_entry.pack(fill="x", expand=True, side="left")
		self.act_resp_entry = tk.Entry(act_controls, font=self.font)
		self.act_resp_entry.pack(fill="x", expand=True, side="left", padx=6)
		# New small inputs for logic: effects and conditions (JSON)
		self.act_effects_entry = tk.Entry(act_controls, font=self.font)
		self.act_effects_entry.pack(fill="x", expand=True, side="left", padx=6)
		self.act_effects_entry.insert(0, '{"state": {"sitting": true}}')  # placeholder hint
		self.act_conditions_entry = tk.Entry(act_controls, font=self.font)
		self.act_conditions_entry.pack(fill="x", expand=True, side="left", padx=6)
		self.act_conditions_entry.insert(0, '{"state": {"sitting": false}}')
		# Actions editor: bind selection lazily and button commands lazily
		tk.Button(act_controls, text="Add / Update", command=lambda: self._call_method("add_action")).pack(side="left", padx=4)
		tk.Button(act_controls, text="Remove", command=lambda: self._call_method("remove_action")).pack(side="left", padx=4)

		# Bottom: Save room button and preview
		bot = tk.Frame(right)
		bot.pack(fill="x", pady=6)
		tk.Button(bot, text="Save Room", command=lambda: self._call_method("save_room")).pack(side="left")
		tk.Button(bot, text="Preview Room", command=lambda: self._call_method("preview_room")).pack(side="left", padx=6)

		self.preview = tk.Text(right, height=6, font=self.font, bg="#f7f7f7")
		self.preview.pack(fill="both", expand=True, pady=(6,0))

		# Now build the Commands & Stats panel in self.cmd_tab
		self.build_commands_tab(self.cmd_tab)

	# New methods for Commands & Stats
	def build_commands_tab(self, parent):
		# Commands list
		top = tk.Frame(parent, padx=6, pady=6)
		top.pack(fill="both", expand=True)
		left = tk.Frame(top)
		left.pack(side="left", fill="y")
		right = tk.Frame(top)
		right.pack(side="right", fill="both", expand=True)

		tk.Label(left, text="Global Commands").pack(anchor="w")
		self.gcmd_list = tk.Listbox(left, width=30, height=20, font=self.font)
		self.gcmd_list.pack()
		btns = tk.Frame(left)
		btns.pack(fill="x", pady=6)
		tk.Button(btns, text="Add Command", command=self.gcmd_add).pack(fill="x")
		tk.Button(btns, text="Edit Command", command=self.gcmd_edit).pack(fill="x", pady=4)
		tk.Button(btns, text="Delete Command", command=self.gcmd_delete).pack(fill="x")

		# Command editor on right
		tk.Label(right, text="Command").pack(anchor="w")
		self.gcmd_name = tk.Entry(right, font=self.font)
		self.gcmd_name.pack(fill="x")
		tk.Label(right, text="Response Text").pack(anchor="w", pady=(6,0))
		self.gcmd_text = tk.Entry(right, font=self.font)
		self.gcmd_text.pack(fill="x")
		tk.Label(right, text="Inventory Add (comma-separated)").pack(anchor="w", pady=(6,0))
		self.gcmd_inv_add = tk.Entry(right, font=self.font)
		self.gcmd_inv_add.pack(fill="x")
		tk.Label(right, text="Inventory Remove (comma-separated)").pack(anchor="w", pady=(6,0))
		self.gcmd_inv_rem = tk.Entry(right, font=self.font)
		self.gcmd_inv_rem.pack(fill="x")
		tk.Label(right, text="State changes (JSON)").pack(anchor="w", pady=(6,0))
		self.gcmd_state = tk.Entry(right, font=self.font)
		self.gcmd_state.pack(fill="x")
		tk.Label(right, text="Stat changes (JSON or comma like gold:+1)").pack(anchor="w", pady=(6,0))
		self.gcmd_stats = tk.Entry(right, font=self.font)
		self.gcmd_stats.pack(fill="x")

		tk.Button(right, text="Save Command", command=self.gcmd_save).pack(pady=6)

		# Stats manager (defaults)
		stat_frame = tk.LabelFrame(right, text="Default Stats")
		stat_frame.pack(fill="x", pady=(6,0))
		self.stats_list = tk.Listbox(stat_frame, height=6, font=self.font)
		self.stats_list.pack(fill="x")
		stat_ctrl = tk.Frame(stat_frame)
		stat_ctrl.pack(fill="x", pady=4)
		self.stat_name = tk.Entry(stat_ctrl, width=12, font=self.font)
		self.stat_name.pack(side="left", padx=4)
		self.stat_value = tk.Entry(stat_ctrl, width=12, font=self.font)
		self.stat_value.pack(side="left", padx=4)
		tk.Button(stat_ctrl, text="Add/Set", command=self.stat_add).pack(side="left", padx=4)
		tk.Button(stat_ctrl, text="Remove", command=self.stat_remove).pack(side="left", padx=4)

		# Inventory preview: world items (read-only) and player start inventory (editable)
		inv_frame = tk.LabelFrame(right, text="Inventory Preview")
		inv_frame.pack(fill="both", pady=(6,0), expand=True)

		inv_left = tk.Frame(inv_frame)
		inv_left.pack(side="left", fill="both", expand=True, padx=(0,6))
		inv_right = tk.Frame(inv_frame)
		inv_right.pack(side="right", fill="both", expand=True)

		tk.Label(inv_left, text="World Items (aggregate)").pack(anchor="w")
		self.world_items_list = tk.Listbox(inv_left, height=8, font=self.font)
		self.world_items_list.pack(fill="both", expand=True)

		# player start inventory on the right
		tk.Label(inv_right, text="Player Start Inventory").pack(anchor="w")
		self.player_start_list = tk.Listbox(inv_right, height=8, font=self.font)
		self.player_start_list.pack(fill="both", expand=True)

		ps_ctrl = tk.Frame(inv_right)
		ps_ctrl.pack(fill="x", pady=4)
		self.ps_entry = tk.Entry(ps_ctrl, font=self.font)
		self.ps_entry.pack(side="left", fill="x", expand=True)
		# Add a small count entry to specify quantities
		self.ps_count_entry = tk.Entry(ps_ctrl, width=6, font=self.font)
		self.ps_count_entry.pack(side="left", padx=4)
		self.ps_count_entry.insert(0, "1")
		tk.Button(ps_ctrl, text="Add to Start", command=self.add_player_start_item).pack(side="left", padx=4)
		tk.Button(ps_ctrl, text="Remove Selected", command=self.remove_player_start_item).pack(side="left", padx=4)
		# small refresh button
		tk.Button(inv_frame, text="Refresh Items", command=self.refresh_inventory_views).pack(anchor="e", pady=4)

		# Load existing global commands/stats into UI
		self.refresh_global_commands()
		self.refresh_stats_list()
		# populate inventory views
		self.refresh_inventory_views()

	def refresh_global_commands(self):
		self.gcmd_list.delete(0, "end")
		for name in sorted(self.world.get("global_commands", {}).keys()):
			self.gcmd_list.insert("end", name)

	def refresh_stats_list(self):
		self.stats_list.delete(0, "end")
		for k, v in sorted(self.world.get("default_stats", {}).items()):
			self.stats_list.insert("end", f"{k} = {v}")

	# Command CRUD handlers
	def gcmd_add(self):
		self.gcmd_name.delete(0, "end")
		self.gcmd_text.delete(0, "end")
		self.gcmd_inv_add.delete(0, "end")
		self.gcmd_inv_rem.delete(0, "end")
		self.gcmd_state.delete(0, "end")
		self.gcmd_stats.delete(0, "end")

	def gcmd_edit(self):
		sel = self.gcmd_list.curselection()
		if not sel:
			return
		name = self.gcmd_list.get(sel[0])
		cmd = self.world.setdefault("global_commands", {}).get(name, {})
		self.gcmd_name.delete(0, "end"); self.gcmd_name.insert(0, name)
		self.gcmd_text.delete(0, "end"); self.gcmd_text.insert(0, cmd.get("text") or cmd.get("response", ""))
		effects = cmd.get("effects", {})
		self.gcmd_inv_add.delete(0, "end"); self.gcmd_inv_add.insert(0, ",".join(effects.get("inventory_add", [])))
		self.gcmd_inv_rem.delete(0, "end"); self.gcmd_inv_rem.insert(0, ",".join(effects.get("inventory_remove", [])))
		self.gcmd_state.delete(0, "end"); self.gcmd_state.insert(0, json.dumps(effects.get("state", {})))
		self.gcmd_stats.delete(0, "end"); self.gcmd_stats.insert(0, json.dumps(effects.get("stats", {})))

	def gcmd_delete(self):
		sel = self.gcmd_list.curselection()
		if not sel:
			return
		name = self.gcmd_list.get(sel[0])
		if not messagebox.askyesno("Delete", f"Delete global command '{name}'?"):
			return
		self.world.get("global_commands", {}).pop(name, None)
		self.refresh_global_commands()

	def gcmd_save(self):
		name = self.gcmd_name.get().strip()
		if not name:
			messagebox.showerror("Invalid", "Command name required.")
			return
		text = self.gcmd_text.get().strip()
		inv_add = [s.strip() for s in self.gcmd_inv_add.get().split(",") if s.strip()]
		inv_rem = [s.strip() for s in self.gcmd_inv_rem.get().split(",") if s.strip()]
		# parse JSON fields
		try:
			state = json.loads(self.gcmd_state.get()) if self.gcmd_state.get().strip() else {}
		except Exception as e:
			messagebox.showerror("Invalid state JSON", e); return
		# stats may be JSON or simple "gold:+1,score:+5"
		stats_raw = self.gcmd_stats.get().strip()
		stats = {}
		if stats_raw:
			try:
				if (stats_raw.startswith("{") and stats_raw.endswith("}")):
					stats = json.loads(stats_raw)
				else:
					for part in stats_raw.split(","):
						if ":" in part:
							k, v = part.split(":", 1)
							stats[k.strip()] = v.strip()
			except Exception as e:
				messagebox.showerror("Invalid stats", e); return
		# build command object
		obj = {"text": text, "effects": {"inventory_add": inv_add, "inventory_remove": inv_rem, "state": state, "stats": stats}}
		self.world.setdefault("global_commands", {})[name] = obj
		self.refresh_global_commands()

	# Stats handlers
	def stat_add(self):
		k = self.stat_name.get().strip()
		if not k:
			return
		v = self.stat_value.get().strip()
		try:
			vnum = int(v)
		except:
			try:
				vnum = float(v)
			except:
				vnum = v
		self.world.setdefault("default_stats", {})[k] = vnum
		self.refresh_stats_list()

	def stat_remove(self):
		sel = self.stats_list.curselection()
		if not sel:
			return
		item = self.stats_list.get(sel[0])
		k = item.split("=", 1)[0].strip()
		self.world.get("default_stats", {}).pop(k, None)
		self.refresh_stats_list()

	# Integrate global_commands and default_stats into load/save
	def load_world(self, path):
		try:
			with open(path, "r", encoding="utf-8") as f:
				data = json.load(f)
		except Exception as e:
			messagebox.showerror("Error", f"Failed to load: {e}")
			return False

		# Normalize structure: support both "start_room" and legacy "start"
		start = data.get("start_room") or data.get("start")
		rooms = data.get("rooms", {})
		# Validate rooms structure
		if not isinstance(rooms, dict):
			messagebox.showerror("Error", "Invalid world format: 'rooms' must be an object/dictionary.")
			return False
		# Normalize each room entry
		nrooms = {}
		for name, r in rooms.items():
			if not isinstance(r, dict):
				continue
			desc = r.get("description", "")
			exits = r.get("exits", {}) or {}
			items = r.get("items", []) or []
			actions = r.get("actions", {}) or {}
			# normalize action values: string -> {"response": str}
			nactions = {}
			for cmd, val in actions.items():
				if isinstance(val, str):
					nactions[cmd] = {"response": val}
				elif isinstance(val, dict):
					nactions[cmd] = val
			nrooms[name] = {"description": desc, "exits": dict(exits), "items": list(items), "actions": nactions}
		self.world = {"start_room": start, "rooms": nrooms, "global_commands": {}, "default_stats": {}, "item_worth": {}}
		# preserve if JSON had them
		if isinstance(data.get("global_commands"), dict):
			# normalize strings to dicts if necessary
			for k, v in data["global_commands"].items():
				if isinstance(v, str):
					self.world["global_commands"][k] = {"text": v, "effects": {}}
				else:
					self.world["global_commands"][k] = v
		if isinstance(data.get("default_stats"), dict):
			self.world["default_stats"] = dict(data["default_stats"])
		# preserve item worth mapping if present
		if isinstance(data.get("item_worth"), dict):
			w = {}
			for k, v in data.get("item_worth", {}).items():
				try:
					w[str(k)] = int(v)
				except Exception:
					try:
						w[str(k)] = int(float(v))
					except Exception:
						w[str(k)] = 0
			self.world["item_worth"] = w
		# load default_inventory if present: support dict or list legacy formats
		raw_def_inv = data.get("default_inventory", {})
		if isinstance(raw_def_inv, dict):
			# ensure string->int
			ninv = {}
			for k, v in raw_def_inv.items():
				try:
					ninv[str(k)] = int(v)
				except Exception:
					# if value not int, default to 1
					ninv[str(k)] = 1
			self.world["default_inventory"] = ninv
		elif isinstance(raw_def_inv, list):
			# convert list -> dict counts
			agg = {}
			for it in raw_def_inv:
				if it is None:
					continue
				agg[str(it)] = agg.get(str(it), 0) + 1
			self.world["default_inventory"] = agg
		else:
			self.world["default_inventory"] = {}

		# if no start room defined, pick first
		if not self.world["start_room"] and nrooms:
			self.world["start_room"] = next(iter(nrooms))
		self.world_path = path
		self.current_room = None
		# keep alias in sync
		self.world_data = self.world
		self.refresh_room_list()
		# select start room
		if self.world["start_room"]:
			self.select_room_in_list(self.world["start_room"])
			self.current_room = self.world["start_room"]
			self.load_room_to_editor(self.current_room)
		# refresh inventory views after the world and rooms are loaded
		self.refresh_inventory_views()
		return True

	# Save / Load dialogs (file chooser wrappers)
	def save_world_dialog(self):
		"""Prompt for a filename and save the current world to JSON."""
		path = filedialog.asksaveasfilename(title="Save world as", defaultextension=".json",
											filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
											initialfile=os.path.basename(self.world_path) or "world.json")
		if not path:
			return
		# Ensure model alias up-to-date
		self.world_data = self.world
		if self.save_world(path):
			messagebox.showinfo("Saved", "World saved successfully!")
			self.world_path = path
			# refresh UI if needed
			self.refresh_room_list()
			self.refresh_global_commands()
			self.refresh_stats_list()
			self.refresh_inventory_views()

	def load_world_dialog(self):
		"""Prompt for a world file and load it into the editor."""
		path = filedialog.askopenfilename(title="Open world file", defaultextension=".json",
										  filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
		if not path:
			return
		ok = self.load_world(path)
		if ok:
			messagebox.showinfo("Loaded", f"World loaded from:\n{path}")
		else:
			messagebox.showerror("Error", "Failed to load world file.")
		# refresh UI in case load_world didn't already
		self.refresh_room_list()
		self.refresh_global_commands()
		self.refresh_stats_list()
		self.refresh_inventory_views()

	def save_world(self, path):
		# Validate: no empty room names, and exits point to valid rooms
		if not isinstance(self.world.get("rooms"), dict):
			messagebox.showerror("Invalid", "World has no rooms.")
			return False
		for name, data in self.world["rooms"].items():
			if not name.strip():
				messagebox.showerror("Invalid", "Room names cannot be empty.")
				return False
			for d, targ in data.get("exits", {}).items():
				if targ not in self.world["rooms"]:
					messagebox.showerror("Invalid", f"Exit target '{targ}' in room '{name}' does not exist.")
					return False
		# Compose JSON structure expected by engine
		out = {"start_room": self.world.get("start_room"), "rooms": {}}
		# include rooms as before
		for name, data in self.world["rooms"].items():
			# aggregate room items into a mapping item->count for clarity in saved JSON
			raw_items = data.get("items", []) or []
			item_counts = {}
			for it in raw_items:
				if it is None:
					continue
				item_counts[str(it)] = item_counts.get(str(it), 0) + 1
			out["rooms"][name] = {
				"description": data.get("description", ""),
				"exits": data.get("exits", {}),
				"items": item_counts,
				"actions": data.get("actions", {})
			}
		# include global commands and default stats
		if self.world.get("global_commands"):
			out["global_commands"] = self.world["global_commands"]
		if self.world.get("default_stats"):
			out["default_stats"] = self.world["default_stats"]
		# include item worth mapping if present
		if self.world.get("item_worth"):
			out["item_worth"] = {str(k): int(v) for k, v in self.world["item_worth"].items()}
		# include default starting inventory as dict (normalize if necessary)
		def_inv = self.world.get("default_inventory", {}) or {}
		# ensure dict of string->int
		ninv = {}
		if isinstance(def_inv, dict):
			for k, v in def_inv.items():
				try:
					ninv[str(k)] = int(v)
				except Exception:
					ninv[str(k)] = 1
		elif isinstance(def_inv, list):
			agg = {}
			for it in def_inv:
				if it is None:
					continue
				agg[str(it)] = agg.get(str(it), 0) + 1
			ninv = agg
		out["default_inventory"] = ninv

		# ...existing save logic writes 'out' to disk...
		try:
			with open(path, "w", encoding="utf-8") as f:
				json.dump(out, f, indent=2, ensure_ascii=False)
			self.world_path = path
			# keep alias in sync
			self.world_data = self.world
			return True
		except Exception as e:
			messagebox.showerror("Error", f"Failed to save world: {e}")
			return False

	# Ensure a canonical blank world structure
	def create_blank_world(self):
		"""Create a new blank world structure so user can start editing immediately."""
		self.world = {
			"start_room": "Village",
			"rooms": {
				"Village": {
					"description": "A peaceful village.",
					"exits": {},
					"items": [],
					"actions": {}
				}
			},
			"global_commands": {},
			"default_stats": {},
			"default_inventory": []
		}
		# keep alias in sync
		self.world_data = self.world
		self.current_room = "Village"
		self.refresh_room_list()
		self.load_room_to_editor("Village")

	# Add missing method: repopulate the room list and exit-target menu
	def refresh_room_list(self):
		"""Refresh the rooms Listbox and the exit-target OptionMenu, and update start-room label."""
		# rooms list
		try:
			self.room_list.delete(0, "end")
		except Exception:
			# if UI not yet built, silently return
			return
		for name in sorted(self.world.get("rooms", {}).keys()):
			label = name
			if self.world.get("start_room") == name:
				label = f"{name} (start)"
			self.room_list.insert("end", label)
		# Update exit target menu
		try:
			menu = self.exit_target_menu["menu"]
			menu.delete(0, "end")
			for name in sorted(self.world.get("rooms", {}).keys()):
				menu.add_command(label=name, command=lambda v=name: self.exit_target_var.set(v))
			# ensure exit_target_var has some value
			names = list(self.world.get("rooms", {}).keys())
			if names:
				self.exit_target_var.set(names[0])
			else:
				self.exit_target_var.set("")
		except Exception:
			# UI may not be fully initialised; ignore
			pass

		# Update start_label to reflect current start room
		try:
			start = self.world.get("start_room")
			self.start_label.config(text=f"Current Start: {start}" if start else "Current Start: None")
		except Exception:
			# ignore if label not yet created
			pass

	# Add missing helper: safely call methods by name (used for lazy UI binding)
	def _call_method(self, name, *args, **kwargs):
		"""Call instance method by name when the UI widget is activated.
		Shows an error if the method does not exist.
		"""
		fn = getattr(self, name, None)
		if callable(fn):
			return fn(*args, **kwargs)
		else:
			messagebox.showerror("Internal error", f"Method not implemented: {name}")

	# Select a room in the Listbox by name (handles the " (start)" suffix)
	def select_room_in_list(self, name):
		"""Select the given room name in the room_list Listbox."""
		if not name:
			return
		try:
			for i in range(self.room_list.size()):
				val = self.room_list.get(i)
				# match the display label that may include " (start)"
				if val.split(" (start)")[0] == name:
					self.room_list.selection_clear(0, "end")
					self.room_list.selection_set(i)
					self.room_list.see(i)
					break
		except Exception:
			# UI may not be ready; ignore silently
			pass

	# Handle Listbox selection events (kept simple for reuse with lazy binding)
	def on_room_select(self, event=None):
		"""Called when the user selects a room in the Listbox."""
		try:
			sel = self.room_list.curselection()
			if not sel:
				return
			label = self.room_list.get(sel[0])
			name = label.split(" (start)")[0]
			self.current_room = name
			self.load_room_to_editor(name)
		except Exception:
			# ignore unexpected errors during selection handling
			pass

	def load_room_to_editor(self, name):
		"""Populate editor fields with data for room 'name'."""
		if not name or "rooms" not in self.world or name not in self.world["rooms"]:
			return
		data = self.world["rooms"][name]
		# name and description
		try:
			self.name_var.set(name)
			self.desc_text.delete("1.0", "end")
			self.desc_text.insert("1.0", data.get("description", ""))
		except Exception:
			# UI may not be ready
			pass
		# exits
		try:
			self.exits_list.delete(0, "end")
			for d, targ in data.get("exits", {}).items():
				self.exits_list.insert("end", f"{d} -> {targ}")
		except Exception:
			pass
		# items (AGGREGATED: show "name | count" if multiple)
		try:
			self.items_list.delete(0, "end")
			counts = {}
			for it in data.get("items", []):
				counts[it] = counts.get(it, 0) + 1
			for it, cnt in sorted(counts.items(), key=lambda x: x[0].lower()):
				if cnt > 1:
					self.items_list.insert("end", f"{it} | {cnt}")
				else:
					self.items_list.insert("end", it)
		except Exception:
			pass
		# actions (show text and indicate if logic/effects present)
		try:
			self.actions_list.delete(0, "end")
			for cmd, act in data.get("actions", {}).items():
				if isinstance(act, dict):
					text = act.get("text") or act.get("response", "")
					have_logic = ""
					if act.get("effects") or act.get("conditions"):
						have_logic = " [logic]"
					self.actions_list.insert("end", f"{cmd} -> {text}{have_logic}")
				else:
					self.actions_list.insert("end", f"{cmd} -> {str(act)}")
		except Exception:
			pass

	# New helpers: inventory preview refresh and player-start edits
	def refresh_inventory_views(self):
		"""Refresh both world items (aggregate) and player start inventory listboxes."""
		# world items: aggregate unique items from all rooms
		world_items = []
		for rdata in self.world.get("rooms", {}).values():
			for it in rdata.get("items", []):
				if it not in world_items:
					world_items.append(it)
		# update listbox
		try:
			self.world_items_list.delete(0, "end")
			for it in sorted(world_items):
				self.world_items_list.insert("end", it)
		except Exception:
			pass

		# player start inventory: now a dict of item->count
		self.world.setdefault("default_inventory", {})
		try:
			self.player_start_list.delete(0, "end")
			for it, cnt in sorted(self.world.get("default_inventory", {}).items(), key=lambda x: x[0].lower()):
				self.player_start_list.insert("end", f"{it} | {cnt}")
		except Exception:
			pass

	def add_player_start_item(self):
		"""Add the item in ps_entry to the player's default starting inventory with count from ps_count_entry."""
		name = self.ps_entry.get().strip()
		if not name:
			# allow quick pick from world items
			sel = self.world_items_list.curselection()
			if not sel:
				return
			name = self.world_items_list.get(sel[0])
		if not name:
			return
		# parse count
		count_raw = self.ps_count_entry.get().strip()
		try:
			count = int(count_raw)
		except Exception:
			count = 1
		if count <= 0:
			count = 1
		self.world.setdefault("default_inventory", {})
		# increment existing count
		self.world["default_inventory"][name] = self.world["default_inventory"].get(name, 0) + count
		self.ps_entry.delete(0, "end")
		self.ps_count_entry.delete(0, "end")
		self.ps_count_entry.insert(0, "1")
		self.refresh_inventory_views()

	def remove_player_start_item(self):
		"""Remove selected item from player's default starting inventory entirely."""
		sel = self.player_start_list.curselection()
		if not sel:
			return
		text = self.player_start_list.get(sel[0])
		# format "name | count"
		if " | " in text:
			name = text.split(" | ", 1)[0].strip()
		else:
			name = text.strip()
		self.world.setdefault("default_inventory", {})
		if name in self.world["default_inventory"]:
			self.world["default_inventory"].pop(name, None)
		self.refresh_inventory_views()

	# Item add/remove handlers for the room editor (support quantity)
	def add_item(self):
		"""Add item(s) to the currently selected room using the count from item_count_entry."""
		name = self.item_entry.get().strip()
		if not name:
			return
		try:
			cnt = int(self.item_count_entry.get().strip())
		except Exception:
			cnt = 1
		if cnt <= 0:
			cnt = 1
		if "rooms" not in self.world or not self.current_room or self.current_room not in self.world["rooms"]:
			messagebox.showwarning("No room", "Select a room first.")
			return
		items = self.world["rooms"][self.current_room].setdefault("items", [])
		for _ in range(cnt):
			items.append(name)
		# reset inputs and refresh UI
		self.item_entry.delete(0, "end")
		self.item_count_entry.delete(0, "end")
		self.item_count_entry.insert(0, "1")
		self.load_room_to_editor(self.current_room)
		self.refresh_inventory_views()

	def remove_item(self):
		"""Remove the selected item occurrence from the current room (removes the specific list entry)."""
		sel = self.items_list.curselection()
		if not sel:
			return
		idx = sel[0]
		if "rooms" not in self.world or not self.current_room or self.current_room not in self.world["rooms"]:
			return
		room_items = self.world["rooms"][self.current_room].get("items", [])
		# items_list is populated in the same order as room_items, so pop by index
		if 0 <= idx < len(room_items):
			room_items.pop(idx)
		self.load_room_to_editor(self.current_room)
		self.refresh_inventory_views()

	# Room CRUD
	def add_room(self):
		name = simpledialog.askstring("Add room", "Room name:")
		if not name:
			return
		name = name.strip()
		if not name:
			return
		if "rooms" not in self.world:
			self.world["rooms"] = {}
		if name in self.world["rooms"]:
			messagebox.showerror("Exists", "Room already exists.")
			return
		self.world["rooms"][name] = {"description": "", "exits": {}, "items": [], "actions": {}}
		# set as current and persist
		self.current_room = name
		self.refresh_room_list()
		self.select_room_in_list(name)
		self.load_room_to_editor(name)
		# save world to disk so engine can pick up changes
		try:
			self.save_world(self.world_path)
		except Exception:
			pass

	def rename_room(self):
		if not self.current_room:
			messagebox.showwarning("No selection", "Select a room first.")
			return
		new = simpledialog.askstring("Rename room", "New name:", initialvalue=self.current_room)
		if not new:
			return
		new = new.strip()
		if not new or new == self.current_room:
			return
		if new in self.world.get("rooms", {}):
			messagebox.showerror("Exists", "A room with that name already exists.")
			return
		# move data to new key and update any exits pointing to the old name
		data = self.world["rooms"].pop(self.current_room)
		self.world["rooms"][new] = data
		for r, rd in self.world["rooms"].items():
			# update exits mapping values
			for d, targ in list(rd.get("exits", {}).items()):
				if targ == self.current_room:
					rd["exits"][d] = new
		# update start room if needed
		if self.world.get("start_room") == self.current_room:
			self.world["start_room"] = new
		self.current_room = new
		self.refresh_room_list()
		self.select_room_in_list(new)
		self.load_room_to_editor(new)
		try:
			self.save_world(self.world_path)
		except Exception:
			pass

	def delete_room(self):
		if not self.current_room:
			messagebox.showwarning("No selection", "Select a room first.")
			return
		if not messagebox.askyesno("Delete", f"Delete room '{self.current_room}'?"):
			return
		# remove room and any exits that pointed to it
		self.world["rooms"].pop(self.current_room, None)
		for r, rd in self.world["rooms"].items():
			for d, targ in list(rd.get("exits", {}).items()):
				if targ == self.current_room:
					rd["exits"].pop(d, None)
		# fix start_room if needed
		if self.world.get("start_room") == self.current_room:
			self.world["start_room"] = next(iter(self.world["rooms"]), None)
		self.current_room = None
		self.refresh_room_list()
		try:
			self.save_world(self.world_path)
		except Exception:
			pass

	# Exits
	def add_exit(self):
		if not self.current_room:
			messagebox.showwarning("No selection", "Select a room first.")
			return
		dirn = self.exit_dir.get().strip()
		target = self.exit_target_var.get().strip()
		if not dirn or not target:
			return
		room = self.world["rooms"].setdefault(self.current_room, {})
		ex = room.setdefault("exits", {})
		ex[dirn] = target
		self.load_room_to_editor(self.current_room)
		self.refresh_room_list()
		try:
			self.save_world(self.world_path)
		except Exception:
			pass

	def remove_exit(self):
		sel = self.exits_list.curselection()
		if not sel or not self.current_room:
			return
		text = self.exits_list.get(sel[0])
		if "->" in text:
			dirn = text.split("->", 1)[0].strip()
			self.world["rooms"][self.current_room].get("exits", {}).pop(dirn, None)
		self.load_room_to_editor(self.current_room)
		try:
			self.save_world(self.world_path)
		except Exception:
			pass

	# Actions
	def add_action(self):
		if not self.current_room:
			messagebox.showwarning("No room", "Select a room first.")
			return
		cmd = self.act_cmd_entry.get().strip()
		if not cmd:
			messagebox.showerror("Invalid", "Action command required.")
			return
		resp = self.act_resp_entry.get().strip()
		# parse JSON fields gracefully
		try:
			effects = json.loads(self.act_effects_entry.get()) if self.act_effects_entry.get().strip() else {}
		except Exception as e:
			messagebox.showerror("Invalid JSON in effects", str(e)); return
		try:
			conds = json.loads(self.act_conditions_entry.get()) if self.act_conditions_entry.get().strip() else {}
		except Exception as e:
			messagebox.showerror("Invalid JSON in conditions", str(e)); return
		obj = {"text": resp}
		if effects:
			obj["effects"] = effects
		if conds:
			obj["conditions"] = conds
		self.world["rooms"].setdefault(self.current_room, {}).setdefault("actions", {})[cmd] = obj
		self.load_room_to_editor(self.current_room)
		try:
			self.save_world(self.world_path)
		except Exception:
			pass

	def remove_action(self):
		sel = self.actions_list.curselection()
		if not sel or not self.current_room:
			return
		text = self.actions_list.get(sel[0])
		# action list shows "cmd -> ..." so extract cmd
		if "->" in text:
			cmd = text.split("->", 1)[0].strip()
		else:
			cmd = text.strip()
		self.world["rooms"].setdefault(self.current_room, {}).get("actions", {}).pop(cmd, None)
		self.load_room_to_editor(self.current_room)
		try:
			self.save_world(self.world_path)
		except Exception:
			pass

	def on_action_select(self, event=None):
		sel = self.actions_list.curselection()
		if not sel or not self.current_room:
			return
		text = self.actions_list.get(sel[0])
		cmd = text.split("->", 1)[0].strip() if "->" in text else text.strip()
		act = self.world["rooms"].get(self.current_room, {}).get("actions", {}).get(cmd, {})
		self.act_cmd_entry.delete(0, "end"); self.act_cmd_entry.insert(0, cmd)
		self.act_resp_entry.delete(0, "end"); self.act_resp_entry.insert(0, act.get("text") or act.get("response", ""))
		self.act_effects_entry.delete(0, "end"); self.act_effects_entry.insert(0, json.dumps(act.get("effects", {})) if act.get("effects") else "")
		self.act_conditions_entry.delete(0, "end"); self.act_conditions_entry.insert(0, json.dumps(act.get("conditions", {})) if act.get("conditions") else "")

	# Save the currently edited room back to the world model and persist world.json
	def save_room(self):
		"""Write the editor fields into self.world['rooms'][name] and save file."""
		name = self.name_var.get().strip()
		if not name:
			messagebox.showerror("Invalid", "Room name required.")
			return
		# ensure rooms dict exists
		self.world.setdefault("rooms", {})
		# If renaming via entry (user warned), handle moving key if current_room differs
		if self.current_room and name != self.current_room:
			# if new name exists, error
			if name in self.world["rooms"]:
				messagebox.showerror("Invalid", "A room with that name already exists.")
				return
			# move data
			data = self.world["rooms"].pop(self.current_room)
			self.world["rooms"][name] = data
			# update any exits to point to new name
			for r, rd in self.world["rooms"].items():
				for d, targ in list(rd.get("exits", {}).items()):
					if targ == self.current_room:
						rd["exits"][d] = name
			# update start_room if necessary
			if self.world.get("start_room") == self.current_room:
				self.world["start_room"] = name
			self.current_room = name

		# ensure there's an object to update
		room = self.world["rooms"].setdefault(name, {"description": "", "exits": {}, "items": [], "actions": {}})
		# description
		room["description"] = self.desc_text.get("1.0", "end").strip()
		# exits already updated via add/remove; nothing special here
		# items: keep underlying list shape; editor shows aggregated counts, but we need to ensure items list reflects counts
		# read items_list contents (format "name" or "name | count")
		items = []
		try:
			for i in range(self.items_list.size()):
				txt = self.items_list.get(i)
				if " | " in txt:
					it, cnt = txt.split(" | ", 1)
					try:
						n = int(cnt.strip())
					except Exception:
						n = 1
					for _ in range(max(0, n)):
						items.append(it.strip())
				else:
					items.append(txt.strip())
		except Exception:
			# fallback: keep existing room items
			items = list(room.get("items", []))
		room["items"] = items
		# actions: already updated via add_action/remove_action; keep as-is
		# persist to disk
		ok = self.save_world(self.world_path)
		if ok:
			messagebox.showinfo("Saved", f"Room '{name}' saved and world persisted.")
		else:
			messagebox.showerror("Error", "Failed to save world.")
		# refresh UI
		self.refresh_room_list()
		self.select_room_in_list(name)
		self.load_room_to_editor(name)

	def preview_room(self):
		"""Show a preview of the room using current editor fields."""
		name = self.name_var.get().strip() or "<unnamed>"
		desc = self.desc_text.get("1.0", "end").strip()
		exits = []
		try:
			for i in range(self.exits_list.size()):
				exits.append(self.exits_list.get(i))
		except Exception:
			pass
		items = []
		try:
			for i in range(self.items_list.size()):
				items.append(self.items_list.get(i))
		except Exception:
			pass
		lines = [name, desc]
		if items:
			lines.append("You see: " + ", ".join(items))
		if exits:
			# show only directions
			edirs = [e.split("->",1)[0].strip() for e in exits]
			lines.append("Exits: " + ", ".join(edirs))
		try:
			self.preview.delete("1.0", "end")
			self.preview.insert("1.0", "\n".join(lines))
		except Exception:
			pass

	# New methods for bulk operations (add after build_commands_tab method)
	def show_bulk_operations_menu(self):
		"""Show menu for bulk room creation and modification."""
		win = tk.Toplevel(self.root)
		win.title("Bulk Operations")
		win.geometry("400x600")
		
		frame = tk.Frame(win, padx=6, pady=6)
		frame.pack(fill="both", expand=True)
		
		tk.Label(frame, text="Bulk Room Creation & Modification", font=self.font, weight="bold").pack(anchor="w", pady=(0,12))
		
		# Grid generator
		tk.Label(frame, text="Create Room Grid", font=self.font, weight="bold").pack(anchor="w", pady=(12,4))
		grid_frame = tk.Frame(frame)
		grid_frame.pack(fill="x")
		
		tk.Label(grid_frame, text="Width:").pack(side="left", padx=4)
		width_var = tk.StringVar(value="5")
		tk.Entry(grid_frame, textvariable=width_var, width=6).pack(side="left", padx=4)
		
		tk.Label(grid_frame, text="Height:").pack(side="left", padx=4)
		height_var = tk.StringVar(value="5")
		tk.Entry(grid_frame, textvariable=height_var, width=6).pack(side="left", padx=4)
		
		tk.Label(frame, text="Room Type:").pack(anchor="w", pady=(6,2))
		type_var = tk.StringVar(value="wilderness")
		type_menu = tk.OptionMenu(frame, type_var, "wilderness", "settlement", "building", "transition")
		type_menu.pack(fill="x", pady=(0,6))
		
		tk.Label(frame, text="Template (optional):").pack(anchor="w", pady=(6,2))
		template_var = tk.StringVar()
		template_menu = tk.OptionMenu(frame, template_var, "", "forest", "tavern", "dungeon_cell")
		template_menu.pack(fill="x", pady=(0,6))
		
		tk.Label(frame, text="Grid Prefix Name:").pack(anchor="w", pady=(6,2))
		prefix_var = tk.StringVar(value="Area")
		tk.Entry(frame, textvariable=prefix_var).pack(fill="x", pady=(0,6))
		
		def do_grid():
			try:
				from world_builder import create_room_grid, add_example_templates
				# Ensure templates exist
				add_example_templates(self.world_path)
				# Create grid
				created, msg = create_room_grid(
					int(width_var.get()),
					int(height_var.get()),
					start_id=1000 + len(self.world.get("rooms", {})),
					location_type=type_var.get(),
					world_file=self.world_path,
					template_name=template_var.get() or None,
					region_name=prefix_var.get()
				)
				messagebox.showinfo("Grid Created", msg)
				self.load_world(self.world_path)
			except Exception as e:
				messagebox.showerror("Error", str(e))
		
		tk.Button(frame, text="Create Grid", command=do_grid).pack(fill="x", pady=(0,12))
		
		# Batch modify
		tk.Label(frame, text="Batch Modify Rooms", font=self.font, weight="bold").pack(anchor="w", pady=(12,4))
		
		tk.Label(frame, text="Operation:").pack(anchor="w", pady=(6,2))
		op_var = tk.StringVar(value="add_item")
		op_menu = tk.OptionMenu(frame, op_var, "add_item", "remove_item", "add_exit", "change_location_type")
		op_menu.pack(fill="x", pady=(0,6))
		
		tk.Label(frame, text="Filter by Location Type (optional):").pack(anchor="w", pady=(6,2))
		filter_var = tk.StringVar()
		filter_menu = tk.OptionMenu(frame, filter_var, "", "wilderness", "settlement", "building", "transition")
		filter_menu.pack(fill="x", pady=(0,6))
		
		tk.Label(frame, text="Parameter (e.g., item name):").pack(anchor="w", pady=(6,2))
		param_var = tk.StringVar()
		tk.Entry(frame, textvariable=param_var).pack(fill="x", pady=(0,6))
		
		def do_batch():
			try:
				from world_builder import filter_rooms, batch_modify_rooms
				# Filter rooms
				criteria = {}
				if filter_var.get():
					criteria["location_type"] = filter_var.get()
				room_ids = filter_rooms(self.world_path, criteria)
				
				if not room_ids:
					messagebox.showinfo("Batch Modify", "No rooms match the filter.")
					return
				
				# Execute operation
				op = op_var.get()
				params = {}
				if op == "add_item":
					params = {"item_name": param_var.get(), "quantity": 1}
				elif op == "change_location_type":
					params = {"new_type": param_var.get()}
				
				results = batch_modify_rooms(room_ids, op, self.world_path, **params)
				msg = f"Success: {results['success_count']}\nFailed: {len(results['failed_ids'])}"
				messagebox.showinfo("Batch Modify", msg)
				self.load_world(self.world_path)
			except Exception as e:
				messagebox.showerror("Error", str(e))
		
		tk.Button(frame, text="Apply Batch Operation", command=do_batch).pack(fill="x")

def main():
	root = tk.Tk()
	app = WorldEditor(root)
	root.mainloop()


if __name__ == "__main__":
	main()

# Notes / How to extend:
# - To add richer item data (e.g., descriptions, attributes), replace items list with objects:
#     "items": [{"id":"map","description":"A folded map"}]
#   Update both editor UI and save/load normalization to handle the new shape.
# - To add more complex actions (add_item/remove_item/move_to), the editor currently stores actions as dicts.
#   Extend the action UI to edit those extra keys.
# - To link this editor's output to the main game, save the file as world.json in the game folder
#   or open it from the game's Start dialog. The engine supports "start_room" and room entries as used here.
# - UI improvements: add drag/drop for rooms, a graphical map, or an "auto-validate" button to check connectivity.
# - The editor creates a blank world if none is loaded so you can start authoring immediately.
