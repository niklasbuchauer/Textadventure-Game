"""
pygame_ui.py  —  Core Pygame UI framework for Estoria's Chronicles

Replaces all tkinter functionality with pygame + pygame_gui.
Contains the main game application, panel system, adventure GUI,
and entry point.
"""

import pygame
import pygame_gui
from pygame_gui.elements import (
    UIButton, UITextBox, UITextEntryLine, UIWindow,
    UILabel, UISelectionList, UIPanel, UIHorizontalSlider,
    UIDropDownMenu,
)
from pygame_gui.core import ObjectID

import json
import os
import sys
import math
import random
import re
import copy
import html as html_module
import time

# ---------------------------------------------------------------------------
#  Constants
# ---------------------------------------------------------------------------
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
THEME_FILE  = os.path.join(BASE_DIR, "pygame_theme.json")
MIN_WIDTH   = 1024
MIN_HEIGHT  = 600
DEFAULT_FPS = 60

# Tag → hex colour (matches CONFIG_DEFAULTS in engine.py)
TAG_COLORS = {
    "combat":      "#FF6B6B",
    "item":        "#98FB98",
    "dialogue":    "#87CEEB",
    "status":      "#87CEFA",
    "warning":     "#FFD700",
    "system":      "#DA70D6",
    "command":     "#AAAAAA",
    "default":     "#DCDCDC",
    "title_gold":  "#FFD700",
    "title_cyan":  "#00FFFF",
    "title_green": "#00FF00",
    "title_purple":"#DA70D6",
    "normal":      "#DCDCDC",
}

# Dark theme colour palette (mirrors engine.py CONFIG_DEFAULTS)
DARK = {
    "bg":           (0x1e, 0x1e, 0x1e),
    "dark_bg":      (0x14, 0x14, 0x14),
    "entry_bg":     (0x2e, 0x2e, 0x2e),
    "hotbar_bg":    (0x1a, 0x1a, 0x1a),
    "panel_hdr":    (0x14, 0x14, 0x14),
    "fg":           (0xdc, 0xdc, 0xdc),
    "gold":         (0xFF, 0xD7, 0x00),
    "sash":         (0x0a, 0x0a, 0x0a),
}

# ---------------------------------------------------------------------------
#  Helpers
# ---------------------------------------------------------------------------

def hex_to_rgb(h):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

def rgb_to_hex(r, g, b):
    return f"#{r:02x}{g:02x}{b:02x}"

def hex_lerp(a, b, t):
    ar, ag, ab = hex_to_rgb(a)
    br, bg_, bb = hex_to_rgb(b)
    return rgb_to_hex(
        int(ar + (br - ar) * t),
        int(ag + (bg_ - ag) * t),
        int(ab + (bb - ab) * t),
    )

def escape_html(text):
    """Escape HTML special chars then convert newlines to <br>."""
    s = html_module.escape(str(text))
    return s.replace("\n", "<br>")


# ═══════════════════════════════════════════════════════════════════════════
#  PygamePanelWidget  –  titled, scrollable, colour-tagged text panel
# ═══════════════════════════════════════════════════════════════════════════

class PygamePanelWidget:
    """
    A self-contained output panel with a gold title bar, scroll-lock toggle,
    and a scrollable UITextBox that renders coloured messages via HTML.
    """

    TITLE_H = 26

    def __init__(self, manager, container, title, msg_type, rect,
                 colors=None):
        self.manager   = manager
        self.container = container
        self.title     = title
        self.msg_type  = msg_type
        self.rect      = pygame.Rect(rect)
        self.colors    = dict(colors or TAG_COLORS)
        self.visible   = True

        self._scroll_locked = False
        self._messages  = []        # [(text, colour_hex, timestamp)]
        self._html_parts = []       # parallel HTML fragments
        self._last_msg  = ""
        self._last_count = 1
        self._max_msgs  = 50
        self._need_scroll = False

        # ── Build widgets ────────────────────────────────────────────────
        th = self.TITLE_H

        self.panel = UIPanel(
            relative_rect=self.rect,
            manager=manager,
            container=container,
        )

        self.title_label = UILabel(
            relative_rect=pygame.Rect(4, 1, self.rect.w - 40, th),
            text=f"  {title}",
            manager=manager,
            container=self.panel,
            object_id=ObjectID("#panel_title", "label"),
        )

        self.lock_btn = UIButton(
            relative_rect=pygame.Rect(self.rect.w - 38, 1, 32, th),
            text="\U0001F513",      # 🔓
            manager=manager,
            container=self.panel,
            object_id=ObjectID("#panel_lock_button", "button"),
        )

        self.text_box = UITextBox(
            html_text="",
            relative_rect=pygame.Rect(
                2, th + 2, self.rect.w - 4, self.rect.h - th - 4),
            manager=manager,
            container=self.panel,
        )

    # ── Resize / reposition ──────────────────────────────────────────────

    def set_rect(self, rect):
        self.rect = pygame.Rect(rect)
        th = self.TITLE_H
        self.panel.set_relative_position((rect.x, rect.y))
        self.panel.set_dimensions((rect.w, rect.h))
        self.title_label.set_relative_position((4, 1))
        self.title_label.set_dimensions((rect.w - 40, th))
        self.lock_btn.set_relative_position((rect.w - 38, 1))
        self.text_box.set_relative_position((2, th + 2))
        self.text_box.set_dimensions((rect.w - 4, rect.h - th - 4))

    # ── Lock toggle ──────────────────────────────────────────────────────

    def toggle_lock(self):
        self._scroll_locked = not self._scroll_locked
        self.lock_btn.set_text(
            "\U0001F512" if self._scroll_locked else "\U0001F513")

    # ── Message insertion ────────────────────────────────────────────────

    def insert_message(self, text, tag="default", timestamp="",
                       max_messages=50):
        self._max_msgs = max_messages
        colour = self.colors.get(tag, self.colors.get("default", "#DCDCDC"))

        # ── Collapse repeated messages ───────────────────────────────────
        if text == self._last_msg and self._last_count >= 1:
            self._last_count += 1
            if self._messages:
                old_text, old_col, old_ts = self._messages[-1]
                clean = re.sub(r"\s+\(\u00d7\d+\)$", "", old_text)
                new = f"{clean}  (\u00d7{self._last_count})"
                self._messages[-1] = (new, old_col, old_ts)
                # Rebuild HTML for that entry
                pre = f'<font color="#AAAAAA">[{old_ts}] </font>' if old_ts else ""
                self._html_parts[-1] = (
                    f'{pre}<font color="{old_col}">'
                    f'{escape_html(new)}</font><br><br>'
                )
                self._full_rebuild()
            return

        # ── New message ──────────────────────────────────────────────────
        self._last_msg   = text
        self._last_count = 1

        prefix = f"[{timestamp}] " if timestamp else ""
        full   = f"{prefix}{text}"

        self._messages.append((full, colour, timestamp))

        ts_html = (f'<font color="#AAAAAA">[{timestamp}] </font>'
                   if timestamp else "")
        frag = (f'{ts_html}<font color="{colour}">'
                f'{escape_html(text)}</font><br><br>')
        self._html_parts.append(frag)

        # ── Trim ─────────────────────────────────────────────────────────
        trimmed = False
        while len(self._messages) > max_messages:
            self._messages.pop(0)
            self._html_parts.pop(0)
            trimmed = True

        if trimmed:
            self._full_rebuild()
        else:
            # Fast path: append only
            try:
                self.text_box.append_html_text(frag)
            except Exception:
                self._full_rebuild()
            self._need_scroll = True

    def _full_rebuild(self):
        """Rebuild the full HTML content from the message buffer."""
        html = "".join(self._html_parts)
        try:
            self.text_box.set_text(html)
        except Exception:
            self.text_box.set_text("")
        self._need_scroll = True

    def update(self):
        """Call once per frame to apply deferred tasks (scroll etc.)."""
        if self._need_scroll and not self._scroll_locked:
            try:
                sb = self.text_box.scroll_bar
                if sb is not None:
                    sb.set_scroll_from_start_percentage(1.0)
            except Exception:
                pass
            self._need_scroll = False

    # ── Colour / appearance ──────────────────────────────────────────────

    def apply_colors(self, colors: dict):
        self.colors.update(colors)

    def clear(self):
        self._messages.clear()
        self._html_parts.clear()
        self._last_msg = ""
        self._last_count = 1
        self.text_box.set_text("")

    def show(self):
        self.panel.show()
        self.visible = True

    def hide(self):
        self.panel.hide()
        self.visible = False


# ═══════════════════════════════════════════════════════════════════════════
#  GameApp  –  top-level pygame application
# ═══════════════════════════════════════════════════════════════════════════

class GameApp:
    """
    Single Pygame window that hosts the entire game.
    Manages the 60 FPS loop, UIManager, scene transitions
    (title → game), and all overlay windows.
    """

    def __init__(self):
        pygame.init()
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        pygame.display.set_caption("Estoria's Chronicles")

        info = pygame.display.Info()
        self.width  = info.current_w
        self.height = info.current_h
        self.fullscreen = True
        self.surface = pygame.display.set_mode(
            (self.width, self.height), pygame.FULLSCREEN)

        theme = THEME_FILE if os.path.exists(THEME_FILE) else None
        self.manager = pygame_gui.UIManager(
            (self.width, self.height), theme)

        self.clock   = pygame.time.Clock()
        self.running  = True
        self.dt       = 0.0

        # Scene state
        self.scene = "title"       # "title" | "game"
        self.title_screen = None
        self.gui = None            # PygameAdventureGUI (created on game start)

    # ── Main loop ─────────────────────────────────────────────────────────

    def run(self):
        from title_screen import TitleScreen
        self.title_screen = TitleScreen(self)

        while self.running:
            self.dt = self.clock.tick(DEFAULT_FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._on_quit()
                    self.running = False
                    continue

                # F11 toggles fullscreen
                if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                    self.fullscreen = not self.fullscreen
                    info = pygame.display.Info()
                    if self.fullscreen:
                        self.width = info.current_w
                        self.height = info.current_h
                        self.surface = pygame.display.set_mode(
                            (self.width, self.height), pygame.FULLSCREEN)
                    else:
                        # Use a reasonable windowed size
                        self.width = max(MIN_WIDTH, min(info.current_w - 80, 1600))
                        self.height = max(MIN_HEIGHT, min(info.current_h - 80, 900))
                        self.surface = pygame.display.set_mode(
                            (self.width, self.height), pygame.RESIZABLE)
                    self.manager.set_window_resolution((self.width, self.height))
                    if self.scene == "title" and self.title_screen:
                        self.title_screen.on_resize(self.width, self.height)
                    elif self.scene == "game" and self.gui:
                        self.gui.on_resize(self.width, self.height)

                # Window resize (only in windowed mode)
                if event.type == pygame.VIDEORESIZE and not self.fullscreen:
                    self.width  = max(MIN_WIDTH,  event.w)
                    self.height = max(MIN_HEIGHT, event.h)
                    self.surface = pygame.display.set_mode(
                        (self.width, self.height), pygame.RESIZABLE)
                    self.manager.set_window_resolution(
                        (self.width, self.height))
                    if self.scene == "title" and self.title_screen:
                        self.title_screen.on_resize(self.width, self.height)
                    elif self.scene == "game" and self.gui:
                        self.gui.on_resize(self.width, self.height)

                # Block KEYDOWN/KEYUP from pygame_gui when a minigame overlay
                # is active — prevents keys from typing into the command box.
                _overlay_active = False
                if self.scene == "game" and self.gui:
                    _overlay_active = any(
                        getattr(self.gui, _n, None) and
                        not getattr(self.gui, _n).done
                        for _n in (
                            '_fishing_overlay', '_forging_overlay',
                            '_alchemy_overlay', '_smelting_overlay',
                            '_ritual_overlay', '_crafting_overlay',
                            '_rune_overlay',
                        )
                    )
                if not (_overlay_active and event.type in (pygame.KEYDOWN, pygame.KEYUP)):
                    self.manager.process_events(event)

                # Route to active scene
                if self.scene == "title" and self.title_screen:
                    self.title_screen.handle_event(event)
                elif self.scene == "game" and self.gui:
                    self.gui.handle_event(event)

            # ── Update ────────────────────────────────────────────────────
            self.manager.update(self.dt)
            if self.scene == "title" and self.title_screen:
                self.title_screen.update(self.dt)
            elif self.scene == "game" and self.gui:
                self.gui.update(self.dt)

            # ── Render ────────────────────────────────────────────────────
            self.surface.fill(DARK["bg"])

            if self.scene == "title" and self.title_screen:
                self.title_screen.render(self.surface)

            self.manager.draw_ui(self.surface)

            # Overlays drawn AFTER pygame_gui (always on top)
            if self.scene == "title" and self.title_screen:
                self.title_screen.render_overlay(self.surface)
            elif self.scene == "game" and self.gui:
                self.gui.render_overlay(self.surface, self.dt)

            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            pygame.display.flip()

        pygame.quit()

    # ── Scene transitions ─────────────────────────────────────────────────

    def start_game(self):
        """Transition from title screen to the main game."""
        if self.title_screen:
            self.title_screen.cleanup()
            self.title_screen = None
        self.scene = "game"
        self.gui = PygameAdventureGUI(self)
        self.gui.init_engine()

    # ── Quit ──────────────────────────────────────────────────────────────

    def _on_quit(self):
        if self.gui:
            self.gui.on_quit()


# ═══════════════════════════════════════════════════════════════════════════
#  PygameAdventureGUI  –  main game UI (replaces tkinter AdventureGUI)
# ═══════════════════════════════════════════════════════════════════════════

class PygameAdventureGUI:
    """
    Full game interface: toolbar, hotbar, multi-panel text output,
    combat status, command input, and popup overlays.
    """

    # Keywords for auto-routing messages to panels
    _COMBAT_KW = frozenset([
        "attack", "attacks", "damage", "hp", "hit", "miss", "strike",
        "slain", "defeated", "critical", "dodge", "parry", "block",
        "spell", "cast", "kill", "combat", "fight", "round", "enemy",
        "fallen", "dies", "dead", "wound", "bleeding", "stunned",
    ])
    _ITEM_KW = frozenset([
        "received", "picked up", "dropped", "looted", "crafted",
        "equipped", "unequipped", "enchanted", "item", "gold",
        "purchased", "sold", "chest", "reward", "found",
    ])
    _DIALOGUE_KW = frozenset([
        " says", " asks", " replies", " whispers", " shouts",
        "greets you", "dialogue", "speaks",
    ])
    _WARNING_KW = frozenset([
        "warning", "cannot", "can't", "invalid", "error",
        "failed", "unable", "not allowed", "not found",
    ])

    def __init__(self, app: GameApp):
        self.app     = app
        self.manager = app.manager
        self.width   = app.width
        self.height  = app.height

        # ── Load config ──────────────────────────────────────────────────
        self.config = self._load_config()

        # ── Engine / game references ─────────────────────────────────────
        self.engine = None

        # ── Popup window references ──────────────────────────────────────
        self.inventory_win   = None
        self.stats_win       = None
        self.debug_win       = None
        self.journal_win     = None
        self.skill_tree_win  = None
        self.skills_book_win = None
        self.settings_win    = None
        self.bestiary_win   = None
        self.rooms_win      = None
        self.commands_win   = None
        self.home_editor_win = None
        self._popup_windows  = {}     # name -> UIWindow
        self._sub_windows    = []     # windows with handle_event() (rooms/bestiary/items)

        # ── Overlay states ───────────────────────────────────────────────
        self._death_overlay    = None
        self._travel_overlay  = None
        self._dungeon_entrance_overlay = None
        self._fishing_overlay = None
        self._forging_overlay = None
        self._alchemy_overlay = None
        self._smelting_overlay = None
        self._ritual_overlay  = None
        self._crafting_overlay = None
        self._rune_overlay    = None
        self._tooltip         = None

        # ── Hotbar ───────────────────────────────────────────────────────
        self._hotbar_buttons  = []    # (UIButton, ability_dict)
        self._hotbar_visible  = False
        self._hotbar_label    = None

        # ── Combat status ────────────────────────────────────────────────
        self._combat_visible  = False
        self._combat_player_lbl = None
        self._combat_enemy_lbl  = None

        # ── Build all widgets ────────────────────────────────────────────
        self._panels = {}
        self._build_ui()

    # ------------------------------------------------------------------
    #  CONFIG
    # ------------------------------------------------------------------

    @staticmethod
    def _load_config():
        from engine import CONFIG_FILE, CONFIG_DEFAULTS
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            def _merge(base, over):
                result = copy.deepcopy(base)
                for k, v in over.items():
                    if k in result and isinstance(result[k], dict) and isinstance(v, dict):
                        result[k] = _merge(result[k], v)
                    else:
                        result[k] = v
                return result
            return _merge(CONFIG_DEFAULTS, data)
        except Exception:
            return copy.deepcopy(CONFIG_DEFAULTS)

    def save_config(self):
        from engine import CONFIG_FILE
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"[Config] save error: {e}")

    def apply_config(self):
        """Re-apply config to all live panels."""
        vcfg = self.config["visual"]
        colors = vcfg["colors"]
        if self.config["accessibility"]["high_contrast"]:
            colors = {
                "combat": "#FF4444", "item": "#44FF44",
                "dialogue": "#44CCFF", "status": "#AAAAFF",
                "warning": "#FFFF00", "system": "#FF44FF",
                "command": "#FFFFFF", "default": "#FFFFFF",
            }
        for pw in self._panels.values():
            pw.apply_colors(colors)

    # ------------------------------------------------------------------
    #  BUILD UI
    # ------------------------------------------------------------------

    _TOOLBAR_H = 40
    _HOTBAR_H  = 32
    _INPUT_H   = 34
    _COMBAT_H  = 28
    _MARGIN    = 4

    def _build_ui(self):
        m   = self.manager
        W   = self.width
        H   = self.height
        TH  = self._TOOLBAR_H
        HBH = self._HOTBAR_H
        IH  = self._INPUT_H
        MG  = self._MARGIN

        # ── Toolbar background panel ─────────────────────────────────────
        self.toolbar_panel = UIPanel(
            relative_rect=pygame.Rect(0, 0, W, TH),
            manager=m,
            object_id=ObjectID("#toolbar_panel", "panel"),
        )

        oid = ObjectID("#toolbar_button", "button")
        bx = MG
        btn_w = 110
        btn_h = TH - 8
        btn_y = 4

        self.inv_btn = UIButton(
            relative_rect=pygame.Rect(bx, btn_y, btn_w, btn_h),
            text="■ Inventory", manager=m,
            container=self.toolbar_panel, object_id=oid)
        bx += btn_w + 4

        self.stats_btn = UIButton(
            relative_rect=pygame.Rect(bx, btn_y, 80, btn_h),
            text="▲ Stats", manager=m,
            container=self.toolbar_panel, object_id=oid)
        bx += 84

        self.debug_btn = UIButton(
            relative_rect=pygame.Rect(bx, btn_y, 80, btn_h),
            text="● Debug", manager=m,
            container=self.toolbar_panel, object_id=oid)
        bx += 84

        # Conditional buttons (always created; hidden if system unavailable)
        self.skills_btn = UIButton(
            relative_rect=pygame.Rect(bx, btn_y, 80, btn_h),
            text="★ Skills", manager=m,
            container=self.toolbar_panel, object_id=oid)
        bx += 84

        self.journal_btn = UIButton(
            relative_rect=pygame.Rect(bx, btn_y, 90, btn_h),
            text="○ Journal", manager=m,
            container=self.toolbar_panel, object_id=oid)
        bx += 94

        self.commands_btn = UIButton(
            relative_rect=pygame.Rect(bx, btn_y, 106, btn_h),
            text="► Commands", manager=m,
            container=self.toolbar_panel, object_id=oid)
        bx += 110

        self.home_editor_btn = UIButton(
            relative_rect=pygame.Rect(bx, btn_y, 106, btn_h),
            text="H Home Edit", manager=m,
            container=self.toolbar_panel, object_id=oid)
        bx += 110

        # Status label
        self.status_label = UILabel(
            relative_rect=pygame.Rect(bx, btn_y, 200, btn_h),
            text="", manager=m,
            container=self.toolbar_panel,
            object_id=ObjectID("#status_label", "label"),
        )

        # Settings button (far right)
        self.settings_btn = UIButton(
            relative_rect=pygame.Rect(W - 44, btn_y, 36, btn_h),
            text="◆", manager=m,
            container=self.toolbar_panel,
            object_id=ObjectID("#settings_button", "button"),
        )

        # ── Hotbar background ────────────────────────────────────────────
        self.hotbar_panel = UIPanel(
            relative_rect=pygame.Rect(0, TH, W, HBH),
            manager=m,
            object_id=ObjectID("#hotbar_panel", "panel"),
        )
        self._hotbar_label = UILabel(
            relative_rect=pygame.Rect(4, 2, 80, HBH - 4),
            text="Abilities:", manager=m,
            container=self.hotbar_panel,
            object_id=ObjectID("#hotbar_label", "label"),
        )

        # ── Command input (bottom) ───────────────────────────────────────
        self.entry = UITextEntryLine(
            relative_rect=pygame.Rect(
                MG, H - IH - MG, W - MG * 2, IH),
            manager=m,
        )
        self._hint_font = None  # lazy-loaded for the hint text drawn in render_overlay

        # ── Combat status bar (above input, hidden initially) ────────────
        csy = H - IH - MG - self._COMBAT_H - 2
        self._combat_panel = UIPanel(
            relative_rect=pygame.Rect(0, csy, W, self._COMBAT_H),
            manager=m,
            object_id=ObjectID("#combat_panel", "panel"),
        )
        self._combat_panel.hide()

        self._combat_player_lbl = UILabel(
            relative_rect=pygame.Rect(8, 1, W // 2 - 16, self._COMBAT_H - 2),
            text="", manager=m,
            container=self._combat_panel,
            object_id=ObjectID("#combat_player_label", "label"),
        )
        self._combat_enemy_lbl = UILabel(
            relative_rect=pygame.Rect(
                W // 2, 1, W // 2 - 16, self._COMBAT_H - 2),
            text="", manager=m,
            container=self._combat_panel,
            object_id=ObjectID("#combat_enemy_label", "label"),
        )

        # ── Multi-panel area ─────────────────────────────────────────────
        self._build_panels()

    # ------------------------------------------------------------------
    #  PANELS
    # ------------------------------------------------------------------

    def _panels_rect(self):
        """Return the rectangle available for the panel area."""
        top = self._TOOLBAR_H + self._HOTBAR_H
        bot = self._INPUT_H + self._MARGIN * 2
        if self._combat_visible:
            bot += self._COMBAT_H + 2
        return pygame.Rect(
            self._MARGIN, top,
            self.width - self._MARGIN * 2,
            self.height - top - bot)

    def _build_panels(self):
        ui   = self.config["ui"]
        vcfg = self.config["visual"]
        layout    = ui.get("layout", "side_by_side")
        panels_on = ui.get("panels", {})

        colors = dict(vcfg["colors"])
        if self.config["accessibility"]["high_contrast"]:
            colors = {
                "combat": "#FF4444", "item": "#44FF44",
                "dialogue": "#44CCFF", "status": "#AAAAFF",
                "warning": "#FFFF00", "system": "#FF44FF",
                "command": "#FFFFFF", "default": "#FFFFFF",
            }

        pr = self._panels_rect()

        defs = [
            ("main",     "Main Output",    "default"),
            ("combat",   "Combat Log",     "combat"),
            ("items",    "Items / Loot",   "item"),
            ("dialogue", "Dialogue / NPC", "dialogue"),
            ("system",   "Status / System","system"),
        ]

        def _make(key, title, mtype, rect, visible=True):
            pw = PygamePanelWidget(
                self.manager, None, title, mtype, rect, colors)
            if not visible:
                pw.hide()
            self._panels[key] = pw
            return pw

        if layout == "single":
            _make("main", "Main Output", "default", pr)
            # Hidden panels — created off-screen for message routing
            off = pygame.Rect(-9999, -9999, 200, 100)
            for key, title, mt in defs[1:]:
                pw = _make(key, title, mt, off, visible=False)

        elif layout == "stacked":
            n_visible = 1 + sum(1 for k, _, _ in defs[1:]
                                if panels_on.get(k, False))
            ph = pr.h // max(n_visible, 1)
            y = pr.y
            _make("main", "Main Output", "default",
                  pygame.Rect(pr.x, y, pr.w, ph))
            y += ph + 2
            off = pygame.Rect(-9999, -9999, 200, 100)
            for key, title, mt in defs[1:]:
                if panels_on.get(key, False):
                    _make(key, title, mt,
                          pygame.Rect(pr.x, y, pr.w, ph))
                    y += ph + 2
                else:
                    _make(key, title, mt, off, visible=False)

        else:  # side_by_side (default)
            left_w  = int(pr.w * 0.60)
            right_w = pr.w - left_w - 4

            _make("main", "Main Output", "default",
                  pygame.Rect(pr.x, pr.y, left_w, pr.h))

            right_keys = [k for k, _, _ in defs[1:]
                          if panels_on.get(k, False)]
            if right_keys:
                rh = pr.h // max(len(right_keys), 1)
                ry = pr.y
                off = pygame.Rect(-9999, -9999, 200, 100)
                for key, title, mt in defs[1:]:
                    if key in right_keys:
                        _make(key, title, mt,
                              pygame.Rect(pr.x + left_w + 4, ry,
                                          right_w, rh))
                        ry += rh + 2
                    else:
                        _make(key, title, mt, off, visible=False)
            else:
                off = pygame.Rect(-9999, -9999, 200, 100)
                for key, title, mt in defs[1:]:
                    _make(key, title, mt, off, visible=False)

    def _relayout_panels(self):
        """Recalculate panel positions after a resize."""
        ui   = self.config["ui"]
        layout    = ui.get("layout", "side_by_side")
        panels_on = ui.get("panels", {})
        pr = self._panels_rect()

        defs_keys = [
            ("main", True),
            ("combat",   panels_on.get("combat",   True)),
            ("items",    panels_on.get("items",    True)),
            ("dialogue", panels_on.get("dialogue", False)),
            ("system",   panels_on.get("system",   False)),
        ]

        if layout == "single":
            if "main" in self._panels:
                self._panels["main"].set_rect(pr)

        elif layout == "stacked":
            vis = [(k, v) for k, v in defs_keys if v]
            if not vis:
                vis = [("main", True)]
            ph = pr.h // max(len(vis), 1)
            y = pr.y
            for k, _ in vis:
                if k in self._panels:
                    self._panels[k].set_rect(
                        pygame.Rect(pr.x, y, pr.w, ph))
                    y += ph + 2

        else:  # side_by_side
            left_w  = int(pr.w * 0.60)
            right_w = pr.w - left_w - 4

            if "main" in self._panels:
                self._panels["main"].set_rect(
                    pygame.Rect(pr.x, pr.y, left_w, pr.h))

            right_keys = [k for k, v in defs_keys[1:] if v]
            if right_keys:
                rh = pr.h // max(len(right_keys), 1)
                ry = pr.y
                for k in right_keys:
                    if k in self._panels:
                        self._panels[k].set_rect(
                            pygame.Rect(pr.x + left_w + 4, ry,
                                        right_w, rh))
                        ry += rh + 2

    # ------------------------------------------------------------------
    #  RESIZE
    # ------------------------------------------------------------------

    def on_resize(self, w, h):
        self.width  = w
        self.height = h

        # Toolbar
        self.toolbar_panel.set_dimensions((w, self._TOOLBAR_H))
        self.settings_btn.set_relative_position((w - 44, 4))

        # Hotbar
        self.hotbar_panel.set_dimensions((w, self._HOTBAR_H))

        # Entry
        IH = self._INPUT_H
        MG = self._MARGIN
        self.entry.set_relative_position((MG, h - IH - MG))
        self.entry.set_dimensions((w - MG * 2, IH))

        # Combat status
        csy = h - IH - MG - self._COMBAT_H - 2
        self._combat_panel.set_relative_position((0, csy))
        self._combat_panel.set_dimensions((w, self._COMBAT_H))
        self._combat_player_lbl.set_dimensions((w // 2 - 16, self._COMBAT_H - 2))
        self._combat_enemy_lbl.set_relative_position((w // 2, 1))
        self._combat_enemy_lbl.set_dimensions((w // 2 - 16, self._COMBAT_H - 2))

        # Panels
        self._relayout_panels()

    # ------------------------------------------------------------------
    #  EVENT HANDLING
    # ------------------------------------------------------------------

    def handle_event(self, event):
        # ── Dungeon entrance overlay (highest priority) ─────────────────
        if self._dungeon_entrance_overlay and not self._dungeon_entrance_overlay.is_done():
            self._dungeon_entrance_overlay.handle_event(event)
            return

        # ── Overlay input intercepts ─
        for _ov in (self._fishing_overlay, self._forging_overlay,
                    self._alchemy_overlay, self._smelting_overlay,
                    self._ritual_overlay, self._crafting_overlay,
                    self._rune_overlay):
            if _ov and not _ov.done:
                _ov.handle_event(event)
                return

        # ── Book overlays (inventory/stats/debug/skills/journal/settings/commands/bestiary/rooms) ─
        for _bov in (self.journal_win, self.inventory_win,
                     self.stats_win, self.debug_win, self.skills_book_win,
                     self.settings_win, self.commands_win, self.home_editor_win,
                     self.bestiary_win, self.rooms_win):
            if _bov and hasattr(_bov, 'is_open') and _bov.is_open() \
                    and hasattr(_bov, 'handle_event'):
                if _bov.handle_event(event):
                    return

        # ── Forward to sub-windows (rooms/bestiary/items/skill tree) ─────
        self._sub_windows = [w for w in self._sub_windows if w.is_open()]
        for w in self._sub_windows:
            w.handle_event(event)

        # ── Forward to live map window ────────────────────────────────────
        _mw = getattr(self.engine, 'map_window', None)
        if _mw and _mw.is_open():
            _mw.handle_event(event)

        # ── pygame_gui button presses ────────────────────────────────────
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            ui = event.ui_element
            if ui == self.inv_btn:
                self.toggle_inventory_window()
            elif ui == self.stats_btn:
                self.toggle_stats_window()
            elif ui == self.debug_btn:
                self.toggle_debug_window()
            elif ui == self.skills_btn:
                self.toggle_skills_window()
            elif ui == self.journal_btn:
                self.toggle_journal_window()
            elif ui == self.commands_btn:
                self.toggle_commands_window()
            elif ui == self.home_editor_btn:
                self.toggle_home_editor_window()
            elif ui == self.settings_btn:
                self._open_settings()
            else:
                # Check panel lock buttons
                for pw in self._panels.values():
                    if ui == pw.lock_btn:
                        pw.toggle_lock()
                        return
                # Check hotbar buttons
                for btn, ab in self._hotbar_buttons:
                    if ui == btn:
                        cmd = ab.get("name", "").lower().replace(" ", "_")
                        if cmd:
                            self._hotbar_use(cmd)
                        return

        # ── Text entry finished (Enter key) ──────────────────────────────
        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
            if event.ui_element == self.entry:
                self.on_enter()

        # ── Keyboard shortcuts ───────────────────────────────────────────
        if event.type == pygame.KEYDOWN:
            mods = pygame.key.get_mods()
            # Ctrl+S  save
            if event.key == pygame.K_s and (mods & pygame.KMOD_CTRL):
                self.on_save_shortcut()
            # Ctrl+L  load
            elif event.key == pygame.K_l and (mods & pygame.KMOD_CTRL):
                self.on_load_shortcut()
            # Number keys 1-8 for hotbar
            elif event.key in range(pygame.K_1, pygame.K_9):
                slot = event.key - pygame.K_1 + 1
                self._hotbar_key(slot)

        # ── Window close events ──────────────────────────────────────────
        if event.type == pygame_gui.UI_WINDOW_CLOSE:
            ui = event.ui_element
            for name, win in list(self._popup_windows.items()):
                if ui == win:
                    del self._popup_windows[name]
                    # Clear specific references
                    if name == "inventory":
                        self.inventory_win = None
                    elif name == "stats":
                        self.stats_win = None
                    elif name == "debug":
                        self.debug_win = None
                    break
            # Skill tree window
            if self.skill_tree_win and hasattr(self.skill_tree_win, 'window'):
                if ui == self.skill_tree_win.window:
                    self.skill_tree_win = None
            # Sub-windows (rooms/bestiary/items)
            self._sub_windows = [
                w for w in self._sub_windows
                if not (hasattr(w, 'window') and w.window == ui)
            ]

    # ------------------------------------------------------------------
    #  UPDATE (per-frame)
    # ------------------------------------------------------------------

    def update(self, dt):
        for pw in self._panels.values():
            pw.update()

        # Update death overlay
        if self._death_overlay:
            self._death_overlay.update(dt)
            if self._death_overlay.done:
                text = self._death_overlay.respawn_text
                self._death_overlay = None
                self.append(text)
                self.refresh_inventory_display()
                self._refresh_hotbar()

        # Update dungeon entrance overlay
        if self._dungeon_entrance_overlay:
            self._dungeon_entrance_overlay.update(dt)
            if self._dungeon_entrance_overlay.is_done():
                self._dungeon_entrance_overlay = None

        # Update travel overlay
        if self._travel_overlay:
            self._travel_overlay.update(dt)
            if self._travel_overlay.done:
                text = self._travel_overlay.deferred_text
                self._travel_overlay = None
                if text:
                    self.append(text)
                self.refresh_inventory_display()
                self._refresh_hotbar()

        # Update overlays
        for _ovname in ('_fishing_overlay', '_forging_overlay',
                        '_alchemy_overlay', '_smelting_overlay',
                        '_ritual_overlay', '_crafting_overlay',
                        '_rune_overlay'):
            _ov = getattr(self, _ovname, None)
            if _ov:
                _ov.update(dt)
                if _ov.done:
                    setattr(self, _ovname, None)

        # Tick sub-windows (settings slider labels, etc.)
        self._sub_windows = [w for w in self._sub_windows if w.is_open()]
        for w in self._sub_windows:
            if hasattr(w, 'update'):
                w.update()

        # Book overlays tick
        _bov_refs = ['journal_win','inventory_win','stats_win',
                     'debug_win','skills_book_win','settings_win',
                     'commands_win','home_editor_win','bestiary_win','rooms_win']
        for _rn in _bov_refs:
            _w = getattr(self, _rn, None)
            if _w and hasattr(_w,'is_open'):
                if _w.is_open():
                    _w.update(dt)
                else:
                    setattr(self, _rn, None)

        # Live map — tick once per frame (deferred redraws)
        _mw = getattr(self.engine, 'map_window', None)
        if _mw and _mw.is_open():
            _mw.tick()

    # ------------------------------------------------------------------
    #  RENDER OVERLAYS (drawn after pygame_gui)
    # ------------------------------------------------------------------

    def render_overlay(self, surface, dt):
        # ── Command-input hint text (purely visual, non-interactive) ─────────
        # Drawn when the entry box is empty so the user knows what it's for.
        if self.entry and not self.entry.get_text():
            if self._hint_font is None:
                self._hint_font = pygame.font.SysFont("Courier New", 14)
            r = self.entry.get_abs_rect()
            hint_surf = self._hint_font.render(
                "Type a command...", True, (90, 90, 110))
            surface.blit(hint_surf, (r.x + 8, r.y + (r.height - hint_surf.get_height()) // 2))

        if self._death_overlay:
            self._death_overlay.render(surface)
        if self._dungeon_entrance_overlay:
            self._dungeon_entrance_overlay.draw(surface)
        if self._travel_overlay:
            self._travel_overlay.render(surface)
        for _ov in (self._fishing_overlay, self._forging_overlay,
                    self._alchemy_overlay, self._smelting_overlay,
                    self._ritual_overlay, self._crafting_overlay,
                    self._rune_overlay):
            if _ov and not _ov.done:
                _ov.render(surface)
        # Live map — single direct blit bypassing pygame_gui compositing
        _mw = getattr(self.engine, 'map_window', None)
        if _mw and _mw.is_open():
            _mw.render_direct(surface)
        # Book overlays drawn last (always on top)
        for _bov in (self.journal_win, self.inventory_win,
                     self.stats_win, self.debug_win, self.skills_book_win,
                     self.settings_win, self.commands_win, self.home_editor_win,
                     self.bestiary_win, self.rooms_win):
            if _bov and hasattr(_bov,'is_open') and _bov.is_open() and hasattr(_bov,'draw'):
                _bov.draw(surface)

    # ------------------------------------------------------------------
    #  MESSAGE ROUTING
    # ------------------------------------------------------------------

    @staticmethod
    def _detect_type(text):
        lower = text.lower()
        words = set(lower.split())
        if any(k in words for k in PygameAdventureGUI._COMBAT_KW):
            return "combat"
        if any(k in lower for k in PygameAdventureGUI._ITEM_KW):
            return "item"
        if any(k in lower for k in PygameAdventureGUI._DIALOGUE_KW):
            return "dialogue"
        if any(k in lower for k in PygameAdventureGUI._WARNING_KW):
            return "warning"
        return "default"

    def append(self, text, msg_type=None):
        if not text:
            return
        if msg_type is None:
            if text.startswith("> "):
                msg_type = "command"
            else:
                msg_type = self._detect_type(text)

        ts = ""
        if self.config.get("ui", {}).get("timestamps", False):
            from datetime import datetime
            ts = datetime.now().strftime("%H:%M")

        max_msgs = self.config.get("ui", {}).get("max_messages", 50)

        panel_map = {
            "combat": "combat", "item": "items",
            "dialogue": "dialogue", "system": "system",
            "status": "system",
        }
        panel_key = panel_map.get(msg_type, "main")

        target = self._panels.get(panel_key)
        if target is None or not target.visible:
            target = self._panels["main"]

        target.insert_message(text, tag=msg_type,
                              timestamp=ts, max_messages=max_msgs)

        # Mirror to main
        if panel_key != "main":
            main_p = self._panels.get("main")
            if main_p and main_p is not target:
                main_p.insert_message(text, tag=msg_type,
                                      timestamp=ts, max_messages=max_msgs)

    # ------------------------------------------------------------------
    #  COMMAND INPUT
    # ------------------------------------------------------------------

    def on_enter(self):
        cmd = self.entry.get_text().strip()
        self.entry.set_text("")
        if not cmd:
            return

        self.append(f"> {cmd}")

        if not self.engine:
            self.append("Engine is still loading. Please wait...")
            return

        resp = self.engine.process_command(cmd)

        # Travel animation
        travel = getattr(self.engine, "pending_travel_animation", None)
        if travel is not None:
            self.engine.pending_travel_animation = None
            self.refresh_inventory_display()
            self._refresh_hotbar()
            self._start_travel_animation(travel, resp or "")
            return

        # Special return values
        if resp == "__OPEN_ROOMS__":
            self._open_rooms_window()
            return
        if resp == "__OPEN_BESTIARY__":
            self._open_bestiary_window()
            return

        if resp:
            if "\U0001F480 YOU HAVE FALLEN! \U0001F480" in resp:
                self._start_death_screen(resp)
                self.refresh_inventory_display()
                self._refresh_hotbar()
                self.update_combat_status()
                return
            msg_type = self._detect_type(resp)
            self.append(resp, msg_type)

        self._update_combat_status_from_engine()
        self.refresh_inventory_display()
        self._refresh_hotbar()

        if getattr(self.engine, "should_quit", False):
            self.append("Exiting...")
            self.on_quit()
            self.app.running = False

    # ------------------------------------------------------------------
    #  SAVE / LOAD SHORTCUTS
    # ------------------------------------------------------------------

    def on_save_shortcut(self):
        if not self.engine:
            self.append("Engine not ready.")
            return
        self.append(self.engine.save_game())

    def on_load_shortcut(self):
        if not self.engine:
            self.append("Engine not ready.")
            return
        self.append(self.engine.load_game())
        self.refresh_inventory_display()
        self._refresh_hotbar()

    # ------------------------------------------------------------------
    #  COMBAT STATUS BAR
    # ------------------------------------------------------------------

    def update_combat_status(self, player=None, enemy=None):
        if player is None and enemy is None:
            if self._combat_visible:
                self._combat_panel.hide()
                self._combat_visible = False
                self._relayout_panels()
            return

        if not self._combat_visible:
            self._combat_panel.show()
            self._combat_visible = True
            self._relayout_panels()

        if player:
            hp  = getattr(player, "hp", None) or player.stats.get("hp", "?")
            mhp = getattr(player, "max_hp", None) or player.stats.get("max_hp", "?")
            mp  = getattr(player, "mp", None) or player.stats.get("mp", 0)
            mmp = getattr(player, "max_mp", None) or player.stats.get("max_mp", 0)
            name = getattr(player, "name", "Player") or "Player"
            bar_len = 12
            try:
                filled = round(int(hp) / max(int(mhp), 1) * bar_len)
                hp_bar = "\u2588" * filled + "\u2591" * (bar_len - filled)
            except Exception:
                hp_bar = ""
            self._combat_player_lbl.set_text(
                f"\u25b6 {name}  HP [{hp_bar}] {hp}/{mhp}  MP {mp}/{mmp}")

        if enemy:
            ehp  = getattr(enemy, "hp", None)
            emhp = getattr(enemy, "max_hp", None)
            ename = getattr(enemy, "name", str(enemy)[:20])
            if ehp is not None and emhp:
                bar_len = 12
                try:
                    filled = round(int(ehp) / max(int(emhp), 1) * bar_len)
                    e_bar = "\u2588" * filled + "\u2591" * (bar_len - filled)
                except Exception:
                    e_bar = ""
                self._combat_enemy_lbl.set_text(
                    f"{ename}  HP [{e_bar}] {ehp}/{emhp} \u25c0")
            else:
                self._combat_enemy_lbl.set_text(f"Enemy: {ename} \u25c0")
        else:
            self._combat_enemy_lbl.set_text("")

    def _update_combat_status_from_engine(self):
        if not self.engine or not self.engine.player:
            return
        pending = getattr(self.engine, "pending_combat", None)
        if pending and isinstance(pending, dict):
            class _EP:
                pass
            ep = _EP()
            ep.name   = pending.get("name", "Enemy")
            ep.hp     = pending.get("hp", "?")
            ep.max_hp = pending.get("max_hp", ep.hp)
            self.update_combat_status(self.engine.player, ep)
        else:
            self.update_combat_status()

    # ------------------------------------------------------------------
    #  DEATH SCREEN
    # ------------------------------------------------------------------

    def _start_death_screen(self, respawn_text):
        from death_screen import DeathOverlay
        self._death_overlay = DeathOverlay(
            self.app.width, self.app.height, respawn_text)

    # ------------------------------------------------------------------
    #  TRAVEL ANIMATION
    # ------------------------------------------------------------------

    def _start_travel_animation(self, island_name, deferred_text):
        from travel_animation import TravelOverlay
        self._travel_overlay = TravelOverlay(
            self.app.width, self.app.height, island_name, deferred_text)

    # ------------------------------------------------------------------
    #  HOTBAR
    # ------------------------------------------------------------------

    def _refresh_hotbar(self):
        # Kill old buttons
        for btn, _ in self._hotbar_buttons:
            btn.kill()
        self._hotbar_buttons.clear()

        try:
            from engine import PROGRESSION_AVAILABLE
            if not PROGRESSION_AVAILABLE:
                self._hotbar_visible = False
                return
            from skill_tree import get_active_abilities
        except Exception:
            self._hotbar_visible = False
            return

        if not self.engine or not self.engine.player:
            self._hotbar_visible = False
            return

        abilities = get_active_abilities(self.engine.player)
        if not abilities:
            self._hotbar_visible = False
            return

        self._hotbar_visible = True
        cooldowns = self.engine.player.state.get("cooldowns", {})
        in_combat = getattr(self.engine, "pending_combat", None) is not None

        bx = 90
        for idx, ab in enumerate(abilities):
            cd = cooldowns.get(ab["skill_id"], 0)
            name = ab.get("name", "?")
            effect = ab.get("effect", "")
            is_combat = ab.get("combat", False)
            usable_outside = effect in (
                "combat_heal", "buff_attack", "temp_defense", "heal")
            slot = idx + 1

            txt = (f"[{slot}] {name} ({cd}T)" if cd > 0
                   else f"[{slot}] {name}")

            # Pick object ID for styling
            if cd > 0:
                oid = ObjectID("#hotbar_button", "button")
            elif is_combat and in_combat:
                oid = ObjectID("#hotbar_combat_button", "button")
            elif is_combat and not in_combat and not usable_outside:
                oid = ObjectID("#hotbar_dimmed_button", "button")
            else:
                oid = ObjectID("#hotbar_button", "button")

            btn = UIButton(
                relative_rect=pygame.Rect(bx, 2, len(txt) * 9 + 16, 26),
                text=txt, manager=self.manager,
                container=self.hotbar_panel,
                object_id=oid,
            )
            if cd > 0:
                btn.disable()

            self._hotbar_buttons.append((btn, ab))
            bx += len(txt) * 9 + 20

    def _hotbar_use(self, ability_cmd_name):
        if not self.engine:
            return
        try:
            from skill_tree import get_active_abilities
            in_combat = getattr(self.engine, "pending_combat", None) is not None
            if not in_combat:
                abilities = get_active_abilities(self.engine.player)
                for ab in abilities:
                    key = ab.get("name", "").lower().replace(" ", "_")
                    if key == ability_cmd_name:
                        effect = ab.get("effect", "")
                        usable = effect in (
                            "combat_heal", "buff_attack",
                            "temp_defense", "heal")
                        if ab.get("combat", False) and not usable:
                            self.append(
                                f"\n  \u26A0 {ab.get('name')} can only "
                                f"be used in combat!\n")
                            return
                        break
        except Exception:
            pass

        resp = self.engine.process_command(f"ability {ability_cmd_name}")
        if resp:
            self.append(resp)
        self._refresh_hotbar()
        self.refresh_inventory_display()

    def _hotbar_key(self, slot):
        if not self._hotbar_visible or not self._hotbar_buttons:
            return
        idx = slot - 1
        if 0 <= idx < len(self._hotbar_buttons):
            btn, ab = self._hotbar_buttons[idx]
            if btn.is_enabled:
                cmd = ab.get("name", "").lower().replace(" ", "_")
                if cmd:
                    self._hotbar_use(cmd)

    # ------------------------------------------------------------------
    #  INVENTORY WINDOW
    # ------------------------------------------------------------------

    def toggle_inventory_window(self):
        if self.inventory_win and self.inventory_win.is_open():
            self.inventory_win.close()
            return
        from book_overlay import InventoryOverlay
        self.inventory_win = InventoryOverlay(self)

    def refresh_inventory_display(self):
        # Update toolbar status label
        try:
            total = 0; total_value = 0
            if self.engine and self.engine.player:
                inv  = self.engine.player.inventory or {}
                wmap = getattr(self.engine, "item_worth", {}) or {}
                total = sum(inv.values())
                for n, c in inv.items():
                    total_value += int(wmap.get(n, 0)) * int(c)
            self.status_label.set_text(
                f"Items: {total}  |  Value: {total_value}g")
        except Exception:
            pass
        # Refresh overlay if open
        if self.inventory_win and hasattr(self.inventory_win, '_refresh'):
            self.inventory_win._refresh()

    # ------------------------------------------------------------------
    #  STATS WINDOW
    # ------------------------------------------------------------------

    def toggle_stats_window(self):
        if self.stats_win and self.stats_win.is_open():
            self.stats_win.close()
            return
        from book_overlay import StatsOverlay
        self.stats_win = StatsOverlay(self)

    def _refresh_stats_content(self):
        """Legacy stub – stats are now self-rendered by StatsOverlay."""
        pass

    # ------------------------------------------------------------------
    #  JOURNAL WINDOW
    # ------------------------------------------------------------------

    def toggle_journal_window(self):
        if self.journal_win and self.journal_win.is_open():
            self.journal_win.close()
            return
        from journal_window import JournalWindow
        self.journal_win = JournalWindow(self)

    # ------------------------------------------------------------------
    #  DEBUG WINDOW
    # ------------------------------------------------------------------

    def toggle_debug_window(self):
        if self.debug_win and self.debug_win.is_open():
            self.debug_win.close()
            return
        from book_overlay import DebugOverlay
        self.debug_win = DebugOverlay(self)

    # ------------------------------------------------------------------
    #  SKILLS WINDOW
    # ------------------------------------------------------------------

    def toggle_skills_window(self):
        if self.skills_book_win and self.skills_book_win.is_open():
            self.skills_book_win.close()
            return
        try:
            from engine import PROGRESSION_AVAILABLE
            if not PROGRESSION_AVAILABLE:
                return
        except Exception:
            return
        if not (self.engine and self.engine.player):
            return
        cls = self.engine.player.stats.get("class", "none")
        if cls == "none":
            self.append("\u26a0\ufe0f Choose a class first! Type 1, 2, or 3.")
            return
        from book_overlay import SkillTreeBookOverlay
        self.skills_book_win = SkillTreeBookOverlay(self)

    # ------------------------------------------------------------------
    #  SETTINGS
    # ------------------------------------------------------------------

    def _open_settings(self):
        if self.settings_win and self.settings_win.is_open():
            self.settings_win.close()
            return
        try:
            from book_overlay import SettingsOverlay
            self.settings_win = SettingsOverlay(self)
        except Exception as e:
            self.append(f"[Settings] Could not open: {e}", "warning")

    # ------------------------------------------------------------------
    #  ROOM / BESTIARY BROWSER
    # ------------------------------------------------------------------

    def _open_rooms_window(self):
        try:
            if self.rooms_win and self.rooms_win.is_open():
                self.rooms_win.close()
                return
            from searchable_rooms_window import RoomsOverlay
            self.rooms_win = RoomsOverlay(self, self.engine)
        except Exception as e:
            self.append(f"[Room Browser] Could not open: {e}")

    def _open_bestiary_window(self):
        try:
            if self.bestiary_win and self.bestiary_win.is_open():
                self.bestiary_win.close()
                return
            from bestiary_window import BestiaryOverlay
            self.bestiary_win = BestiaryOverlay(self)
        except Exception as e:
            self.append(f"[Bestiary] Could not open: {e}")

    def toggle_commands_window(self):
        try:
            if self.commands_win and self.commands_win.is_open():
                self.commands_win.close()
                return
            from commands_window import CommandsOverlay
            self.commands_win = CommandsOverlay(self)
        except Exception as e:
            self.append(f"[Commands] Could not open: {e}")

    def toggle_home_editor_window(self):
        try:
            if self.home_editor_win and self.home_editor_win.is_open():
                self.home_editor_win.close()
                return
            from home_editor_overlay import HomeEditorOverlay
            self.home_editor_win = HomeEditorOverlay(self)
        except Exception as e:
            self.append(f"[Home Editor] Could not open: {e}", "warning")

    # ------------------------------------------------------------------
    #  ENGINE INIT
    # ------------------------------------------------------------------

    def init_engine(self):
        try:
            from engine import GameEngine, SAVE_FILE
            self.engine = GameEngine(gui=self)
        except Exception as e:
            self.append(f"FATAL: {e}", "warning")
            return

        if getattr(self.engine, "sample_world_created", False):
            self.append(
                f"A sample world.json was created at:\n"
                f"{self.engine.world_file}\n"
                f"Edit it to expand your world.")

        if os.path.exists(SAVE_FILE):
            msg = self.engine.load_game()
            self.append(msg)
            if self.engine.player is None:
                msg = self.engine.new_game()
                self.append(msg)
        else:
            msg = self.engine.new_game()
            self.append(msg)

        self.refresh_inventory_display()
        self._refresh_hotbar()

    # ------------------------------------------------------------------
    #  QUIT
    # ------------------------------------------------------------------

    def on_quit(self):
        try:
            if self.engine and self.engine.player:
                self.engine.save_game()
        except Exception:
            pass


# ═══════════════════════════════════════════════════════════════════════════
#  Entry point
# ═══════════════════════════════════════════════════════════════════════════

def main():
    try:
        app = GameApp()
        app.run()
    except KeyboardInterrupt:
        print("\nGame interrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nCRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
