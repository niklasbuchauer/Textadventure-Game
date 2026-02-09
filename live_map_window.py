import tkinter as tk
from tkinter import font
import json


class LiveMapWindow:
    """Interactive ASCII map window with fog-of-war support."""
    
    def __init__(self, parent, rooms_data):
        """
        Initialize the live map window.
        
        Args:
            parent: Parent tkinter widget
            rooms_data: Dictionary of all rooms with coordinates
        """
        self.rooms_data = rooms_data
        self.parent = parent
        self.window = None
        self.canvas = None
        self.current_location = None
        self.visited_rooms = set()
        self.reveal_all = False
        
        # Build coordinate map
        self.coord_map = {}  # (x, y) -> room_id
        for room_id, room in rooms_data.items():
            # Handle both Room class objects and dict-based rooms
            if hasattr(room, 'coordinates'):
                coords = tuple(room.coordinates)
            else:
                coords = tuple(room.get('coordinates', [0, 0]))
            self.coord_map[coords] = room_id
            
        # Find map boundaries
        self._calculate_bounds()
    
    def _calculate_bounds(self):
        """Calculate the min/max coordinates for map rendering."""
        if not self.coord_map:
            self.min_x = self.max_x = self.min_y = self.max_y = 0
            return
            
        coords = list(self.coord_map.keys())
        self.min_x = min(c[0] for c in coords)
        self.max_x = max(c[0] for c in coords)
        self.min_y = min(c[1] for c in coords)
        self.max_y = max(c[1] for c in coords)
    
    def create_window(self, x_offset=200, y_offset=100):
        """Create and display the map window."""
        if self.window and self.window.winfo_exists():
            self.window.lift()
            return
        
        self.window = tk.Toplevel(self.parent)
        self.window.title("World Map - Fog of War")
        self.window.geometry("800x600")
        
        # Create toolbar
        toolbar = tk.Frame(self.window, bg='#2c3e50')
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        tk.Label(toolbar, text="Map Controls:", bg='#2c3e50', 
                fg='#ecf0f1', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        tk.Button(toolbar, text="Toggle Reveal", command=self.toggle_reveal,
                 bg='#3498db', fg='white').pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text="Close", command=self.close_window,
                 bg='#e74c3c', fg='white').pack(side=tk.LEFT, padx=2)
        
        reveal_status = "REVEALED" if self.reveal_all else "FOG OF WAR"
        tk.Label(toolbar, text=f"Mode: {reveal_status}", bg='#2c3e50',
                fg='#f39c12', font=('Arial', 9)).pack(side=tk.LEFT, padx=20)
        
        # Create canvas for map
        self.canvas = tk.Canvas(self.window, bg='#1a1a1a', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.redraw_map()
    
    def update_location(self, current_room_id, visited_rooms):
        """
        Update the map with current location and visited rooms.
        
        Args:
            current_room_id: ID of the room the player is currently in
            visited_rooms: Set or list of visited room IDs
        """
        self.current_location = current_room_id
        self.visited_rooms = set(visited_rooms)
        
        if self.window and self.window.winfo_exists():
            self.redraw_map()
    
    def redraw_map(self):
        """Redraw the ASCII map on the canvas."""
        if not self.canvas:
            return
        
        self.canvas.delete("all")
        
        # Set up fonts
        mono_font = font.Font(family="Courier", size=10)
        
        # Calculate cell size based on canvas
        width = self.canvas.winfo_width() if self.canvas.winfo_width() > 1 else 800
        height = self.canvas.winfo_height() if self.canvas.winfo_height() > 1 else 550
        
        map_width = self.max_x - self.min_x + 1
        map_height = self.max_y - self.min_y + 1
        
        # Add margin
        margin_x = 40
        margin_y = 40
        available_width = width - 2 * margin_x
        available_height = height - 2 * margin_y
        
        cell_width = max(30, available_width // (map_width + 1))
        cell_height = max(25, available_height // (map_height + 1))
        
        # Draw grid and rooms
        for (x, y), room_id in sorted(self.coord_map.items()):
            # Calculate canvas position
            grid_x = x - self.min_x
            grid_y = (self.max_y - y)  # Flip Y to have north = up
            
            canvas_x = margin_x + grid_x * cell_width + cell_width // 2
            canvas_y = margin_y + grid_y * cell_height + cell_height // 2
            
            # Determine room display
            room = self.rooms_data.get(room_id, {})
            # Handle both Room class objects and dict-based rooms
            if hasattr(room, 'name'):
                room_name = room.name
            else:
                room_name = room.get('name', 'Unknown')
            
            # Check visibility
            is_visited = room_id in self.visited_rooms
            is_current = room_id == self.current_location
            
            if not is_visited and not self.reveal_all:
                # Fog of war - show ?
                color = '#555555'
                symbol = '?'
                bg_color = '#222222'
            elif is_current:
                # Current location - bright highlight
                color = '#00ff00'
                symbol = '*'
                bg_color = '#1a3a1a'
            elif is_visited or self.reveal_all:
                # Visited room - show with color based on type
                if hasattr(room, 'location_type'):
                    location_type = room.location_type
                else:
                    location_type = room.get('location_type', 'wilderness')
                if location_type == 'building':
                    color = '#e74c3c'
                    symbol = '■'
                elif 'dungeon' in room_id.lower():
                    color = '#9b59b6'
                    symbol = '▼'
                else:
                    color = '#3498db'
                    symbol = '•'
                bg_color = '#1a1a2e'
            else:
                color = '#555555'
                symbol = '?'
                bg_color = '#222222'
            
            # Draw room circle/box
            radius = cell_width // 2 - 5
            self.canvas.create_oval(
                canvas_x - radius, canvas_y - radius,
                canvas_x + radius, canvas_y + radius,
                fill=bg_color, outline=color, width=2
            )
            
            # Draw symbol
            self.canvas.create_text(
                canvas_x, canvas_y,
                text=symbol,
                fill=color,
                font=mono_font,
                anchor=tk.CENTER
            )
            
            # Draw room label (small)
            label = room_name[:10]
            self.canvas.create_text(
                canvas_x, canvas_y + radius + 12,
                text=label,
                fill=color,
                font=("Arial", 7),
                anchor=tk.N,
                width=60
            )
        
        # Draw legend
        legend_y = height - 60
        legend_items = [
            ("*", "#00ff00", "Current Location"),
            ("■", "#e74c3c", "Building"),
            ("▼", "#9b59b6", "Dungeon"),
            ("•", "#3498db", "Wilderness"),
            ("?", "#555555", "Unknown/Unvisited"),
        ]
        
        legend_x = 20
        for symbol, color, label in legend_items:
            self.canvas.create_text(
                legend_x, legend_y,
                text=f"{symbol} {label}",
                fill=color,
                font=("Arial", 8),
                anchor=tk.W
            )
            legend_y += 15
    
    def toggle_reveal(self):
        """Toggle fog of war reveal mode."""
        self.reveal_all = not self.reveal_all
        if self.window and self.window.winfo_exists():
            # Update toolbar status
            status = "REVEALED" if self.reveal_all else "FOG OF WAR"
            self.redraw_map()
    
    def close_window(self):
        """Close the map window."""
        if self.window and self.window.winfo_exists():
            self.window.destroy()
            self.window = None
            self.canvas = None
    
    def is_open(self):
        """Check if map window is currently open."""
        return self.window is not None and self.window.winfo_exists()
