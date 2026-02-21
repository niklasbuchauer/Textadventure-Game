"""
settings_window.py  –  Settings panel for Estoria's Chronicles
Opens as a Toplevel, reads from / writes to the AdventureGUI config dict.
"""

import copy
import tkinter as tk
from tkinter import ttk, colorchooser, font as tkfont


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _pick_color(parent, current_color: str, on_change) -> None:
    """Open system color picker; call on_change(hex) if a color was chosen."""
    result = colorchooser.askcolor(color=current_color, parent=parent,
                                   title="Choose colour")
    if result and result[1]:
        on_change(result[1])


# ─────────────────────────────────────────────────────────────────────────────
# Main settings window
# ─────────────────────────────────────────────────────────────────────────────

class SettingsWindow(tk.Toplevel):
    """
    Settings Toplevel window.

    Parameters
    ----------
    parent  : tkinter parent widget
    gui     : AdventureGUI instance  (has .config, .save_config(), .apply_config())
    """

    def __init__(self, parent, gui):
        super().__init__(parent)
        self.gui = gui
        # Work on a deep copy so Cancel discards changes
        self._working = copy.deepcopy(gui.config)

        self.title("⚙  Settings")
        self.resizable(False, False)
        self.grab_set()          # modal-ish
        self.configure(bg="#1e1e1e")

        # ── Tab bar ─────────────────────────────────────────────────────────
        self._tabs: dict[str, tk.Frame] = {}
        self._active_tab = tk.StringVar(value="Visual")

        tab_names = ["Visual", "Gameplay", "Accessibility", "UI Layout"]
        tab_bar = tk.Frame(self, bg="#141414")
        tab_bar.pack(fill="x", side="top")
        for name in tab_names:
            btn = tk.Button(
                tab_bar, text=name,
                command=lambda n=name: self._show_tab(n),
                bg="#141414", fg="#cccccc", relief="flat",
                activebackground="#2a2a2a", activeforeground="#ffffff",
                padx=12, pady=6, font=("Courier New", 9)
            )
            btn.pack(side="left")

        # ── Content area ─────────────────────────────────────────────────────
        self._content = tk.Frame(self, bg="#1e1e1e", padx=16, pady=12)
        self._content.pack(fill="both", expand=True)

        # ── Bottom buttons ────────────────────────────────────────────────────
        btn_frame = tk.Frame(self, bg="#141414", pady=6)
        btn_frame.pack(fill="x", side="bottom")
        tk.Button(btn_frame, text="Save",          command=self._save,
                  bg="#2a5a2a", fg="#ffffff", width=10,
                  font=("Courier New", 9)).pack(side="left",  padx=8)
        tk.Button(btn_frame, text="Reset Defaults", command=self._reset,
                  bg="#5a3a1a", fg="#ffffff", width=14,
                  font=("Courier New", 9)).pack(side="left",  padx=4)
        tk.Button(btn_frame, text="Cancel",         command=self.destroy,
                  bg="#3a1a1a", fg="#ffffff", width=10,
                  font=("Courier New", 9)).pack(side="right", padx=8)

        # Build all tab contents once, then show the first tab
        self._build_visual_tab()
        self._build_gameplay_tab()
        self._build_accessibility_tab()
        self._build_ui_tab()
        self._show_tab("Visual")

        self.update_idletasks()
        # Center over parent
        x = parent.winfo_rootx() + (parent.winfo_width()  - self.winfo_width())  // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")

    # ── Tab management ────────────────────────────────────────────────────────

    def _show_tab(self, name: str) -> None:
        for n, frame in self._tabs.items():
            frame.pack_forget()
        if name in self._tabs:
            self._tabs[name].pack(fill="both", expand=True)
        self._active_tab.set(name)

    # ── Section heading helper ────────────────────────────────────────────────

    @staticmethod
    def _section(parent, text: str) -> tk.Label:
        lbl = tk.Label(parent, text=text, bg="#1e1e1e", fg="#FFD700",
                       font=("Courier New", 9, "bold"), anchor="w")
        lbl.pack(fill="x", pady=(10, 2))
        tk.Frame(parent, height=1, bg="#333333").pack(fill="x", pady=(0, 6))
        return lbl

    @staticmethod
    def _row(parent) -> tk.Frame:
        f = tk.Frame(parent, bg="#1e1e1e")
        f.pack(fill="x", pady=2)
        return f

    @staticmethod
    def _label(parent, text: str, width: int = 22) -> tk.Label:
        return tk.Label(parent, text=text, bg="#1e1e1e", fg="#cccccc",
                        font=("Courier New", 9), width=width, anchor="w")

    # ── VISUAL TAB ───────────────────────────────────────────────────────────

    def _build_visual_tab(self) -> None:
        frame = tk.Frame(self._content, bg="#1e1e1e", width=440)
        self._tabs["Visual"] = frame

        self._section(frame, "Message Colours")

        color_keys = [
            ("combat",   "Combat"),
            ("item",     "Items / Loot"),
            ("dialogue", "Dialogue / NPC"),
            ("status",   "Status"),
            ("warning",  "Warnings"),
            ("system",   "System"),
            ("command",  "Command echo"),
            ("default",  "Default text"),
        ]
        self._color_buttons: dict[str, tk.Button] = {}
        for key, label in color_keys:
            row = self._row(frame)
            self._label(row, label + ":").pack(side="left")
            current = self._working["visual"]["colors"].get(key, "#DCDCDC")
            btn = tk.Button(
                row, bg=current, width=6, relief="solid",
                cursor="hand2",
                command=lambda k=key: self._change_color(k)
            )
            btn.pack(side="left", padx=4)
            self._color_buttons[key] = btn

        self._section(frame, "Font & Size")

        # Font family
        row = self._row(frame)
        self._label(row, "Font family:").pack(side="left")
        families = sorted(set(tkfont.families()))
        self._font_var = tk.StringVar(value=self._working["visual"]["font_family"])
        ttk.Combobox(row, textvariable=self._font_var, values=families,
                     width=22, font=("Courier New", 9)).pack(side="left", padx=4)

        # Font size slider
        row = self._row(frame)
        self._label(row, "Font size:").pack(side="left")
        self._fontsize_var = tk.IntVar(value=self._working["visual"]["font_size"])
        tk.Scale(row, from_=7, to=20, orient="horizontal",
                 variable=self._fontsize_var,
                 bg="#1e1e1e", fg="#cccccc", troughcolor="#333333",
                 highlightthickness=0, length=160).pack(side="left")
        tk.Label(row, textvariable=self._fontsize_var, bg="#1e1e1e",
                 fg="#cccccc", font=("Courier New", 9), width=3).pack(side="left")

        self._section(frame, "Theme")
        self._theme_var = tk.StringVar(value=self._working["visual"]["theme"])
        theme_row = self._row(frame)
        for val, text in [("dark", "Dark"), ("light", "Light")]:
            tk.Radiobutton(
                theme_row, text=text, variable=self._theme_var, value=val,
                bg="#1e1e1e", fg="#cccccc", selectcolor="#2a2a2a",
                activebackground="#1e1e1e", activeforeground="#ffffff",
                font=("Courier New", 9)
            ).pack(side="left", padx=6)

    def _change_color(self, key: str) -> None:
        current = self._working["visual"]["colors"].get(key, "#DCDCDC")
        def _apply(hex_color):
            self._working["visual"]["colors"][key] = hex_color
            self._color_buttons[key].config(bg=hex_color)
        _pick_color(self, current, _apply)

    # ── GAMEPLAY TAB ─────────────────────────────────────────────────────────

    def _build_gameplay_tab(self) -> None:
        frame = tk.Frame(self._content, bg="#1e1e1e", width=440)
        self._tabs["Gameplay"] = frame

        self._section(frame, "Combat Speed")
        self._combat_speed = tk.StringVar(value=self._working["gameplay"]["combat_speed"])
        row = self._row(frame)
        for val, text in [("slow", "Slow"), ("normal", "Normal"), ("fast", "Fast")]:
            tk.Radiobutton(
                row, text=text, variable=self._combat_speed, value=val,
                bg="#1e1e1e", fg="#cccccc", selectcolor="#2a2a2a",
                activebackground="#1e1e1e", activeforeground="#ffffff",
                font=("Courier New", 9)
            ).pack(side="left", padx=8)

        self._section(frame, "Scroll Mode")
        self._scroll_mode = tk.StringVar(value=self._working["gameplay"]["scroll_mode"])
        row = self._row(frame)
        for val, text in [("auto", "Auto-scroll"), ("lock", "Manual / Locked")]:
            tk.Radiobutton(
                row, text=text, variable=self._scroll_mode, value=val,
                bg="#1e1e1e", fg="#cccccc", selectcolor="#2a2a2a",
                activebackground="#1e1e1e", activeforeground="#ffffff",
                font=("Courier New", 9)
            ).pack(side="left", padx=8)

        self._section(frame, "Safety & Difficulty")
        self._confirm_dangerous = tk.BooleanVar(
            value=self._working["gameplay"]["confirm_dangerous"])
        row = self._row(frame)
        tk.Checkbutton(
            row, text="Confirm dangerous actions (delete, quit without save…)",
            variable=self._confirm_dangerous,
            bg="#1e1e1e", fg="#cccccc", selectcolor="#2a2a2a",
            activebackground="#1e1e1e", activeforeground="#ffffff",
            font=("Courier New", 9)
        ).pack(side="left")

        row = self._row(frame)
        self._label(row, "Difficulty modifier:").pack(side="left")
        self._difficulty = tk.DoubleVar(
            value=self._working["gameplay"]["difficulty_modifier"])
        tk.Scale(
            row, from_=0.5, to=2.0, resolution=0.1, orient="horizontal",
            variable=self._difficulty,
            bg="#1e1e1e", fg="#cccccc", troughcolor="#333333",
            highlightthickness=0, length=160
        ).pack(side="left")
        difficulty_lbl = tk.Label(row, bg="#1e1e1e", fg="#cccccc",
                                  font=("Courier New", 9), width=4)
        difficulty_lbl.pack(side="left")
        def _update_diff_lbl(*_):
            difficulty_lbl.config(text=f"{self._difficulty.get():.1f}x")
        self._difficulty.trace_add("write", _update_diff_lbl)
        _update_diff_lbl()

    # ── ACCESSIBILITY TAB ─────────────────────────────────────────────────────

    def _build_accessibility_tab(self) -> None:
        frame = tk.Frame(self._content, bg="#1e1e1e", width=440)
        self._tabs["Accessibility"] = frame

        self._section(frame, "Accessibility")

        self._high_contrast = tk.BooleanVar(
            value=self._working["accessibility"]["high_contrast"])
        row = self._row(frame)
        tk.Checkbutton(
            row, text="High-contrast mode (overrides custom colours)",
            variable=self._high_contrast,
            bg="#1e1e1e", fg="#cccccc", selectcolor="#2a2a2a",
            activebackground="#1e1e1e", activeforeground="#ffffff",
            font=("Courier New", 9)
        ).pack(side="left")

        row = self._row(frame)
        self._label(row, "Text size:").pack(side="left")
        self._a11y_textsize = tk.IntVar(
            value=self._working["accessibility"]["text_size"])
        tk.Scale(
            row, from_=8, to=24, orient="horizontal",
            variable=self._a11y_textsize,
            bg="#1e1e1e", fg="#cccccc", troughcolor="#333333",
            highlightthickness=0, length=160
        ).pack(side="left")
        tk.Label(row, textvariable=self._a11y_textsize, bg="#1e1e1e",
                 fg="#cccccc", font=("Courier New", 9), width=3).pack(side="left")

    # ── UI LAYOUT TAB ─────────────────────────────────────────────────────────

    def _build_ui_tab(self) -> None:
        frame = tk.Frame(self._content, bg="#1e1e1e", width=440)
        self._tabs["UI Layout"] = frame

        self._section(frame, "Panel Layout")
        self._layout_var = tk.StringVar(value=self._working["ui"]["layout"])
        row = self._row(frame)
        for val, text in [
            ("side_by_side", "Side-by-side (main left, combat+items right)"),
            ("stacked",      "Stacked vertically"),
            ("single",       "Single panel (no split)"),
        ]:
            tk.Radiobutton(
                row, text=text, variable=self._layout_var, value=val,
                bg="#1e1e1e", fg="#cccccc", selectcolor="#2a2a2a",
                activebackground="#1e1e1e", activeforeground="#ffffff",
                font=("Courier New", 9)
            ).pack(anchor="w", padx=8, pady=1)

        self._section(frame, "Active Panels")
        panel_defs = [
            ("main",    "Main Output (always on)"),
            ("combat",  "Combat Log"),
            ("items",   "Items / Loot"),
            ("dialogue","Dialogue / NPC"),
            ("system",  "Status / System"),
        ]
        self._panel_vars: dict[str, tk.BooleanVar] = {}
        for key, label in panel_defs:
            bv = tk.BooleanVar(value=self._working["ui"]["panels"].get(key, False))
            if key == "main":
                bv.set(True)   # always on
            self._panel_vars[key] = bv
            row = self._row(frame)
            cb = tk.Checkbutton(
                row, text=label, variable=bv,
                bg="#1e1e1e", fg="#cccccc", selectcolor="#2a2a2a",
                activebackground="#1e1e1e", activeforeground="#ffffff",
                font=("Courier New", 9)
            )
            if key == "main":
                cb.config(state="disabled")
            cb.pack(side="left", padx=4)

        self._section(frame, "Messages & Scroll")

        self._timestamps_var = tk.BooleanVar(
            value=self._working["ui"]["timestamps"])
        row = self._row(frame)
        tk.Checkbutton(
            row, text="Show timestamps on messages",
            variable=self._timestamps_var,
            bg="#1e1e1e", fg="#cccccc", selectcolor="#2a2a2a",
            activebackground="#1e1e1e", activeforeground="#ffffff",
            font=("Courier New", 9)
        ).pack(side="left")

        row = self._row(frame)
        self._label(row, "Max messages / panel:").pack(side="left")
        self._max_msgs_var = tk.IntVar(value=self._working["ui"]["max_messages"])
        tk.Spinbox(
            row, from_=10, to=500, increment=10,
            textvariable=self._max_msgs_var, width=6,
            bg="#2e2e2e", fg="#ffffff", font=("Courier New", 9)
        ).pack(side="left", padx=4)

        # Note about layout changes
        tk.Label(
            frame,
            text="⚠  Layout changes take effect after restart.",
            bg="#1e1e1e", fg="#FFD700",
            font=("Courier New", 8, "italic"), anchor="w"
        ).pack(fill="x", pady=(14, 0))

    # ── Bottom-button handlers ─────────────────────────────────────────────

    def _collect(self) -> dict:
        """Gather all widget values back into the working config dict."""
        # Visual
        self._working["visual"]["font_family"] = self._font_var.get()
        self._working["visual"]["font_size"]   = self._fontsize_var.get()
        self._working["visual"]["theme"]        = self._theme_var.get()
        # Colors are updated live as user picks them

        # Gameplay
        self._working["gameplay"]["combat_speed"]       = self._combat_speed.get()
        self._working["gameplay"]["scroll_mode"]        = self._scroll_mode.get()
        self._working["gameplay"]["confirm_dangerous"]  = self._confirm_dangerous.get()
        self._working["gameplay"]["difficulty_modifier"]= round(self._difficulty.get(), 2)

        # Accessibility
        self._working["accessibility"]["high_contrast"] = self._high_contrast.get()
        self._working["accessibility"]["text_size"]     = self._a11y_textsize.get()

        # UI
        self._working["ui"]["layout"]       = self._layout_var.get()
        self._working["ui"]["timestamps"]   = self._timestamps_var.get()
        self._working["ui"]["max_messages"] = self._max_msgs_var.get()
        for key, bv in self._panel_vars.items():
            self._working["ui"]["panels"][key] = bv.get()

        return self._working

    def _save(self) -> None:
        cfg = self._collect()
        self.gui.config = cfg
        self.gui.save_config()
        self.gui.apply_config()
        self.destroy()

    def _reset(self) -> None:
        """Reload defaults from CONFIG_DEFAULTS and refresh all widgets."""
        from engine import CONFIG_DEFAULTS
        self._working = copy.deepcopy(CONFIG_DEFAULTS)
        # Destroy and rebuild tab contents with fresh data
        for key in list(self._tabs.keys()):
            self._tabs[key].destroy()
        self._tabs.clear()
        self._build_visual_tab()
        self._build_gameplay_tab()
        self._build_accessibility_tab()
        self._build_ui_tab()
        self._show_tab(self._active_tab.get())
