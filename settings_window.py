"""
settings_window.py  –  Settings panel for Estoria's Chronicles (Pygame)
Opens as a UIWindow overlay, reads from / writes to the PygameAdventureGUI config dict.
"""

import copy
import pygame
import pygame_gui
from pygame_gui.elements import (
    UIButton, UILabel, UITextBox, UIWindow, UIPanel,
    UIHorizontalSlider, UIDropDownMenu, UISelectionList,
)
from pygame_gui.core import ObjectID

from ui_animation import UI_OPEN_DUR, ease_out_cubic


class SettingsWindow:
    """
    Settings overlay window.

    Parameters
    ----------
    app : GameApp
    gui : PygameAdventureGUI  (has .config, .save_config(), .apply_config())
    """

    TAB_NAMES = ["Visual", "Gameplay", "Accessibility", "UI Layout"]
    OPEN_DUR = UI_OPEN_DUR

    def __init__(self, app, gui):
        self.app = app
        self.gui = gui
        self.manager = app.manager
        self._working = copy.deepcopy(gui.config)

        W, H = app.width, app.height
        ww, wh = 520, 540
        self.window = UIWindow(
            rect=pygame.Rect((W - ww) // 2, (H - wh) // 2, ww, wh),
            manager=self.manager,
            window_display_title="\u2699  Settings",
            resizable=False,
        )
        self._open_started_ms = pygame.time.get_ticks()
        self._open_done = False
        self._target_rect = pygame.Rect((W - ww) // 2, (H - wh) // 2, ww, wh)
        self._apply_open_scale(0.90)

        # Inner dimensions (window chrome takes some space)
        iw = ww - 60
        ih = wh - 80

        # ── Tab bar ──────────────────────────────────────────────────────
        self._tab_buttons = {}
        bx = 10
        for name in self.TAB_NAMES:
            btn = UIButton(
                relative_rect=pygame.Rect(bx, 6, 100, 28),
                text=name, manager=self.manager,
                container=self.window,
            )
            self._tab_buttons[name] = btn
            bx += 104

        # ── Content panels (one per tab, stacked same position) ──────────
        content_rect = pygame.Rect(10, 40, iw, ih - 90)
        self._tab_panels = {}
        self._active_tab = None

        self._build_visual_tab(content_rect)
        self._build_gameplay_tab(content_rect)
        self._build_accessibility_tab(content_rect)
        self._build_ui_tab(content_rect)

        # ── Bottom buttons ───────────────────────────────────────────────
        by = ih - 40
        self.save_btn = UIButton(
            relative_rect=pygame.Rect(10, by, 100, 32),
            text="Save", manager=self.manager,
            container=self.window,
        )
        self.reset_btn = UIButton(
            relative_rect=pygame.Rect(120, by, 130, 32),
            text="Reset Defaults", manager=self.manager,
            container=self.window,
        )
        self.cancel_btn = UIButton(
            relative_rect=pygame.Rect(iw - 90, by, 100, 32),
            text="Cancel", manager=self.manager,
            container=self.window,
        )

        self._show_tab("Visual")

    # ── Helpers ──────────────────────────────────────────────────────────

    def is_open(self):
        return self.window.alive()

    def _make_label(self, parent, text, rect):
        return UILabel(
            relative_rect=rect, text=text,
            manager=self.manager, container=parent,
        )

    # ── Tab switching ────────────────────────────────────────────────────

    def _show_tab(self, name):
        for n, panel in self._tab_panels.items():
            if n == name:
                panel.show()
            else:
                panel.hide()
        self._active_tab = name

    def _apply_open_scale(self, scale):
        tr = self._target_rect
        nw = max(320, int(tr.width * scale))
        nh = max(280, int(tr.height * scale))
        nx = tr.x + (tr.width - nw) // 2
        ny = tr.y + (tr.height - nh) // 2
        self.window.set_dimensions((nw, nh))
        self.window.set_relative_position((nx, ny))

    def _tick_open_animation(self):
        if self._open_done or not self.window.alive():
            return
        elapsed = (pygame.time.get_ticks() - self._open_started_ms) / 1000.0
        t = min(1.0, elapsed / self.OPEN_DUR)
        eased = ease_out_cubic(t)
        self._apply_open_scale(0.90 + 0.10 * eased)
        if t >= 1.0:
            self._open_done = True
            self.window.set_dimensions((self._target_rect.width, self._target_rect.height))
            self.window.set_relative_position((self._target_rect.x, self._target_rect.y))

    # ── VISUAL TAB ───────────────────────────────────────────────────────

    def _build_visual_tab(self, rect):
        panel = UIPanel(
            relative_rect=rect, manager=self.manager,
            container=self.window,
        )
        self._tab_panels["Visual"] = panel

        y = 10
        self._make_label(panel, "Message Colours",
                         pygame.Rect(10, y, 200, 24))
        y += 30

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

        self._color_labels = {}
        for key, label in color_keys:
            self._make_label(panel, f"{label}:",
                             pygame.Rect(10, y, 160, 22))
            cur = self._working["visual"]["colors"].get(key, "#DCDCDC")
            clbl = UILabel(
                relative_rect=pygame.Rect(180, y, 100, 22),
                text=cur, manager=self.manager, container=panel,
            )
            self._color_labels[key] = clbl
            y += 26

        y += 10
        self._make_label(panel, "Font Size",
                         pygame.Rect(10, y, 200, 24))
        y += 28

        fs = self._working["visual"]["font_size"]
        self._fontsize_slider = UIHorizontalSlider(
            relative_rect=pygame.Rect(10, y, 200, 24),
            start_value=float(fs), value_range=(7.0, 20.0),
            manager=self.manager, container=panel,
        )
        self._fontsize_label = UILabel(
            relative_rect=pygame.Rect(220, y, 40, 24),
            text=str(fs), manager=self.manager, container=panel,
        )

    # ── GAMEPLAY TAB ─────────────────────────────────────────────────────

    def _build_gameplay_tab(self, rect):
        panel = UIPanel(
            relative_rect=rect, manager=self.manager,
            container=self.window,
        )
        self._tab_panels["Gameplay"] = panel

        y = 10
        self._make_label(panel, "Combat Speed",
                         pygame.Rect(10, y, 200, 24))
        y += 28

        cur_speed = self._working["gameplay"]["combat_speed"]
        speeds = ["slow", "normal", "fast"]
        self._combat_speed_dd = UIDropDownMenu(
            options_list=speeds,
            starting_option=cur_speed if cur_speed in speeds else "normal",
            relative_rect=pygame.Rect(10, y, 200, 30),
            manager=self.manager, container=panel,
        )
        y += 40

        self._make_label(panel, "Scroll Mode",
                         pygame.Rect(10, y, 200, 24))
        y += 28
        cur_scroll = self._working["gameplay"]["scroll_mode"]
        scrolls = ["auto", "lock"]
        self._scroll_mode_dd = UIDropDownMenu(
            options_list=scrolls,
            starting_option=cur_scroll if cur_scroll in scrolls else "auto",
            relative_rect=pygame.Rect(10, y, 200, 30),
            manager=self.manager, container=panel,
        )
        y += 40

        self._make_label(panel, "Difficulty Modifier",
                         pygame.Rect(10, y, 200, 24))
        y += 28
        diff = self._working["gameplay"]["difficulty_modifier"]
        self._difficulty_slider = UIHorizontalSlider(
            relative_rect=pygame.Rect(10, y, 200, 24),
            start_value=float(diff), value_range=(0.5, 2.0),
            manager=self.manager, container=panel,
        )
        self._difficulty_label = UILabel(
            relative_rect=pygame.Rect(220, y, 50, 24),
            text=f"{diff:.1f}x", manager=self.manager, container=panel,
        )
        y += 40

        self._make_label(panel, "Game Feel Intensity",
                         pygame.Rect(10, y, 220, 24))
        y += 28
        cur_feel = self._working["gameplay"].get("game_feel_intensity", "normal")
        feel_levels = ["low", "normal", "high"]
        self._game_feel_dd = UIDropDownMenu(
            options_list=feel_levels,
            starting_option=cur_feel if cur_feel in feel_levels else "normal",
            relative_rect=pygame.Rect(10, y, 200, 30),
            manager=self.manager, container=panel,
        )

    # ── ACCESSIBILITY TAB ────────────────────────────────────────────────

    def _build_accessibility_tab(self, rect):
        panel = UIPanel(
            relative_rect=rect, manager=self.manager,
            container=self.window,
        )
        self._tab_panels["Accessibility"] = panel

        y = 10
        self._make_label(panel, "Accessibility",
                         pygame.Rect(10, y, 200, 24))
        y += 30

        self._high_contrast_btn = UIButton(
            relative_rect=pygame.Rect(10, y, 300, 30),
            text=("High-contrast: ON" if self._working["accessibility"]["high_contrast"]
                  else "High-contrast: OFF"),
            manager=self.manager, container=panel,
        )
        self._high_contrast_on = self._working["accessibility"]["high_contrast"]
        y += 40

        self._make_label(panel, "Text Size",
                         pygame.Rect(10, y, 200, 24))
        y += 28
        ts = self._working["accessibility"]["text_size"]
        self._a11y_size_slider = UIHorizontalSlider(
            relative_rect=pygame.Rect(10, y, 200, 24),
            start_value=float(ts), value_range=(8.0, 24.0),
            manager=self.manager, container=panel,
        )
        self._a11y_size_label = UILabel(
            relative_rect=pygame.Rect(220, y, 40, 24),
            text=str(ts), manager=self.manager, container=panel,
        )

    # ── UI LAYOUT TAB ───────────────────────────────────────────────────

    def _build_ui_tab(self, rect):
        panel = UIPanel(
            relative_rect=rect, manager=self.manager,
            container=self.window,
        )
        self._tab_panels["UI Layout"] = panel

        y = 10
        self._make_label(panel, "Panel Layout",
                         pygame.Rect(10, y, 200, 24))
        y += 28

        layouts = ["side_by_side", "stacked", "single"]
        cur_layout = self._working["ui"]["layout"]
        self._layout_dd = UIDropDownMenu(
            options_list=layouts,
            starting_option=cur_layout if cur_layout in layouts else "side_by_side",
            relative_rect=pygame.Rect(10, y, 260, 30),
            manager=self.manager, container=panel,
        )
        y += 40

        self._make_label(panel, "Active Panels",
                         pygame.Rect(10, y, 200, 24))
        y += 28

        panel_defs = [
            ("combat",  "Combat Log"),
            ("items",   "Items / Loot"),
            ("dialogue","Dialogue / NPC"),
            ("system",  "Status / System"),
        ]
        self._panel_toggle_btns = {}
        for key, label in panel_defs:
            on = self._working["ui"]["panels"].get(key, False)
            btn = UIButton(
                relative_rect=pygame.Rect(10, y, 300, 28),
                text=f"{'[X]' if on else '[ ]'} {label}",
                manager=self.manager, container=panel,
            )
            self._panel_toggle_btns[key] = (btn, on, label)
            y += 32

        y += 10
        self._make_label(panel, "Messages",
                         pygame.Rect(10, y, 200, 24))
        y += 28

        ts_on = self._working["ui"]["timestamps"]
        self._timestamps_btn = UIButton(
            relative_rect=pygame.Rect(10, y, 300, 28),
            text=f"{'[X]' if ts_on else '[ ]'} Show timestamps",
            manager=self.manager, container=panel,
        )
        self._timestamps_on = ts_on
        y += 32

        self._make_label(panel, "Max messages / panel:",
                         pygame.Rect(10, y, 200, 24))
        y += 26
        mm = self._working["ui"]["max_messages"]
        self._max_msgs_slider = UIHorizontalSlider(
            relative_rect=pygame.Rect(10, y, 200, 24),
            start_value=float(mm), value_range=(10.0, 500.0),
            manager=self.manager, container=panel,
        )
        self._max_msgs_label = UILabel(
            relative_rect=pygame.Rect(220, y, 50, 24),
            text=str(mm), manager=self.manager, container=panel,
        )

    # ── Event handler ────────────────────────────────────────────────────

    def handle_event(self, event):
        if not self.window.alive():
            return False

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            ui = event.ui_element

            for name, btn in self._tab_buttons.items():
                if ui == btn:
                    self._show_tab(name)
                    return True

            if ui == self.save_btn:
                self._save()
                return True
            if ui == self.reset_btn:
                self._reset()
                return True
            if ui == self.cancel_btn:
                self.window.kill()
                return True

            if hasattr(self, '_high_contrast_btn') and ui == self._high_contrast_btn:
                self._high_contrast_on = not self._high_contrast_on
                self._high_contrast_btn.set_text(
                    "High-contrast: ON" if self._high_contrast_on
                    else "High-contrast: OFF")
                return True

            if hasattr(self, '_timestamps_btn') and ui == self._timestamps_btn:
                self._timestamps_on = not self._timestamps_on
                self._timestamps_btn.set_text(
                    f"{'[X]' if self._timestamps_on else '[ ]'} Show timestamps")
                return True

            for key, (btn, on, label) in list(self._panel_toggle_btns.items()):
                if ui == btn:
                    on = not on
                    btn.set_text(f"{'[X]' if on else '[ ]'} {label}")
                    self._panel_toggle_btns[key] = (btn, on, label)
                    return True

        return False

    def update(self):
        """Call per-frame to sync slider labels."""
        if not self.window.alive():
            return

        self._tick_open_animation()

        try:
            fs = int(self._fontsize_slider.get_current_value())
            self._fontsize_label.set_text(str(fs))
        except Exception:
            pass

        try:
            d = self._difficulty_slider.get_current_value()
            self._difficulty_label.set_text(f"{d:.1f}x")
        except Exception:
            pass

        try:
            ts = int(self._a11y_size_slider.get_current_value())
            self._a11y_size_label.set_text(str(ts))
        except Exception:
            pass

        try:
            mm = int(self._max_msgs_slider.get_current_value())
            self._max_msgs_label.set_text(str(mm))
        except Exception:
            pass

    # ── Collect / Save / Reset ───────────────────────────────────────────

    def _collect(self):
        w = self._working

        w["visual"]["font_size"] = int(self._fontsize_slider.get_current_value())

        try:
            w["gameplay"]["combat_speed"] = self._combat_speed_dd.selected_option[0]
        except Exception:
            pass
        try:
            w["gameplay"]["scroll_mode"] = self._scroll_mode_dd.selected_option[0]
        except Exception:
            pass
        try:
            w["gameplay"]["game_feel_intensity"] = self._game_feel_dd.selected_option[0]
        except Exception:
            w["gameplay"]["game_feel_intensity"] = w["gameplay"].get("game_feel_intensity", "normal")
        w["gameplay"]["difficulty_modifier"] = round(
            self._difficulty_slider.get_current_value(), 2)

        w["accessibility"]["high_contrast"] = self._high_contrast_on
        w["accessibility"]["text_size"] = int(
            self._a11y_size_slider.get_current_value())

        try:
            w["ui"]["layout"] = self._layout_dd.selected_option[0]
        except Exception:
            pass
        w["ui"]["timestamps"] = self._timestamps_on
        w["ui"]["max_messages"] = int(
            self._max_msgs_slider.get_current_value())
        for key, (btn, on, label) in self._panel_toggle_btns.items():
            w["ui"]["panels"][key] = on

        return w

    def _save(self):
        cfg = self._collect()
        self.gui.config = cfg
        self.gui.save_config()
        self.gui.apply_config()
        self.window.kill()

    def _reset(self):
        from engine import CONFIG_DEFAULTS
        self._working = copy.deepcopy(CONFIG_DEFAULTS)
        self.window.kill()
        SettingsWindow(self.app, self.gui)
