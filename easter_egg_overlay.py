"""Interactive overlay for easter egg rooms."""

import pygame


def _wrap_lines(text, font, width):
    raw = str(text or "").replace("\r\n", "\n").replace("\r", "\n")
    paragraphs = raw.split("\n")
    lines = []
    for para in paragraphs:
        para = para.strip()
        if not para:
            lines.append("")
            continue
        words = para.split()
        current = words[0]
        for word in words[1:]:
            candidate = f"{current} {word}"
            if font.size(candidate)[0] <= width:
                current = candidate
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines or [""]


class EasterEggRoomOverlay:
    def __init__(self, gui, payload):
        self.gui = gui
        self.payload = dict(payload or {})
        self.done = False
        self._pulse_t = 0.0
        self._scroll = 0
        self._hovered_hotspot_id = None
        self._hovered_hotspot_label = ""
        self._hotspot_rects = []
        self._detail_text = self.payload.get("lore", "")
        self._notes_rect_abs = None

        interactions = list(self.payload.get("interactions", []))
        self._interactions_by_id = {}
        for idx, action in enumerate(interactions):
            action_id = str(action.get("action_id") or f"action_{idx}")
            action["action_id"] = action_id
            self._interactions_by_id[action_id] = action

        self._layout = self.payload.get("layout") or {}
        self._tile_legend = dict(self._layout.get("legend") or {})
        self._tile_legend.setdefault("#", {"color": (74, 63, 47)})
        self._tile_legend.setdefault(".", {"color": (30, 31, 34)})
        self._tile_legend.setdefault("~", {"color": (27, 58, 86)})
        self._tile_legend.setdefault("*", {"color": (99, 77, 34)})

        self._font_title = pygame.font.SysFont("Georgia", 28, bold=True)
        self._font_sub = pygame.font.SysFont("Georgia", 18)
        self._font_body = pygame.font.SysFont("Georgia", 18)
        self._font_hint = pygame.font.SysFont("Georgia", 16, bold=True)
        self._font_map = pygame.font.SysFont("Consolas", 12, bold=True)

    def is_open(self):
        return not self.done

    def close(self):
        self.done = True

    def update(self, dt):
        if self.done:
            return
        self._pulse_t = (self._pulse_t + float(dt)) % 1.0

    def handle_event(self, event):
        if self.done:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.close()
                return True
            if event.key in (pygame.K_UP, pygame.K_w):
                self._scroll = max(0, self._scroll - 1)
                return True
            if event.key in (pygame.K_DOWN, pygame.K_s):
                self._scroll += 1
                return True

        if event.type == pygame.MOUSEWHEEL:
            self._scroll = max(0, self._scroll - int(event.y))
            return True

        if event.type == pygame.MOUSEMOTION:
            self._update_hover_state(event.pos)
            return True

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            panel = self._panel_rect()
            if not panel.collidepoint(pos):
                self.close()
                return True

            for hotspot in self._hotspot_rects:
                if hotspot["rect"].collidepoint(pos):
                    action = self._interactions_by_id.get(hotspot["action_id"])
                    if action:
                        self._activate(action)
                    return True
            return True

        return False

    def _panel_rect(self):
        w = max(760, int(self.gui.width * 0.76))
        h = max(470, int(self.gui.height * 0.70))
        x = (self.gui.width - w) // 2
        y = (self.gui.height - h) // 2
        return pygame.Rect(x, y, w, h)

    def _activate(self, action):
        kind = str(action.get("type", "note")).lower()
        if kind == "note":
            self._detail_text = str(action.get("text", ""))
            return

        if kind == "command":
            command = str(action.get("command", "")).strip()
            if not command:
                return
            response = self.gui.engine.process_command(command)
            success_text = str(action.get("success_text", "")).strip()
            if success_text:
                self._detail_text = success_text
            if response:
                self.gui.append(response)
            self.gui._update_combat_status_from_engine()
            self.gui.refresh_inventory_display()
            self.gui._refresh_hotbar()
            return

        if kind == "close":
            self.close()

    def _update_hover_state(self, pos):
        self._hovered_hotspot_id = None
        self._hovered_hotspot_label = ""
        for hotspot in self._hotspot_rects:
            if hotspot["rect"].collidepoint(pos):
                self._hovered_hotspot_id = hotspot["id"]
                self._hovered_hotspot_label = hotspot["label"]
                return

    def _draw_tile_map(self, shell, panel, map_rect):
        grid = list(self._layout.get("grid") or [])
        if not grid:
            pygame.draw.rect(shell, (18, 17, 15, 200), map_rect, border_radius=8)
            pygame.draw.rect(shell, (131, 112, 79, 150), map_rect, 1, border_radius=8)
            txt = self._font_sub.render("No room layout data available.", True, (184, 171, 145))
            shell.blit(txt, txt.get_rect(center=map_rect.center))
            self._hotspot_rects = []
            return

        rows = len(grid)
        cols = max(len(row) for row in grid)
        cell = max(14, min(30, min((map_rect.w - 8) // max(1, cols), (map_rect.h - 8) // max(1, rows))))
        draw_w = cols * cell
        draw_h = rows * cell
        ox = map_rect.x + (map_rect.w - draw_w) // 2
        oy = map_rect.y + (map_rect.h - draw_h) // 2

        pygame.draw.rect(shell, (16, 15, 13, 210), map_rect, border_radius=8)
        pygame.draw.rect(shell, (131, 112, 79, 150), map_rect, 1, border_radius=8)

        for y, row in enumerate(grid):
            for x in range(cols):
                ch = row[x] if x < len(row) else "."
                legend = self._tile_legend.get(ch, self._tile_legend.get(".", {"color": (30, 31, 34)}))
                color = tuple(legend.get("color", (30, 31, 34)))
                accent = tuple(legend.get("accent", (0, 0, 0))) if legend.get("accent") else None
                tile_rect = pygame.Rect(ox + x * cell, oy + y * cell, cell - 1, cell - 1)
                pygame.draw.rect(shell, color, tile_rect)
                pygame.draw.rect(shell, (16, 16, 16), tile_rect, 1)
                if accent and cell >= 16:
                    center = tile_rect.center
                    accent_r = max(2, cell // 7)
                    pygame.draw.circle(shell, accent, center, accent_r)
                if ch not in (".", " ") and cell >= 22:
                    symbol = self._font_map.render(ch, True, (232, 220, 189))
                    shell.blit(symbol, symbol.get_rect(center=tile_rect.center))

        self._hotspot_rects = []
        for hs in list(self._layout.get("hotspots") or []):
            hx, hy = hs.get("x", 0), hs.get("y", 0)
            hw, hh = hs.get("w", 1), hs.get("h", 1)
            local = pygame.Rect(ox + hx * cell, oy + hy * cell, max(1, hw * cell - 1), max(1, hh * cell - 1))
            abs_rect = pygame.Rect(panel.x + local.x, panel.y + local.y, local.w, local.h)
            is_hovered = hs.get("id") == self._hovered_hotspot_id
            border = (233, 196, 94) if is_hovered else (186, 149, 75)
            fill_alpha = 78 if is_hovered else 38
            overlay = pygame.Surface((local.w, local.h), pygame.SRCALPHA)
            overlay.fill((218, 178, 83, fill_alpha))
            shell.blit(overlay, local.topleft)
            pygame.draw.rect(shell, border, local, 2, border_radius=4)

            self._hotspot_rects.append(
                {
                    "id": str(hs.get("id", "")),
                    "label": str(hs.get("label", "Hotspot")),
                    "action_id": str(hs.get("action_id", "")),
                    "rect": abs_rect,
                }
            )

    def draw(self, surface):
        if self.done:
            return

        panel = self._panel_rect()

        dim = pygame.Surface((self.gui.width, self.gui.height), pygame.SRCALPHA)
        dim.fill((8, 8, 10, 178))
        surface.blit(dim, (0, 0))

        shell = pygame.Surface((panel.w, panel.h), pygame.SRCALPHA)
        pygame.draw.rect(shell, (28, 24, 18, 244), pygame.Rect(0, 0, panel.w, panel.h), border_radius=14)
        pygame.draw.rect(shell, (200, 170, 108, 240), pygame.Rect(0, 0, panel.w, panel.h), 2, border_radius=14)

        pulse = 0.5 + 0.5 * (1.0 - abs(self._pulse_t - 0.5) * 2.0)
        accent = int(58 + 28 * pulse)
        pygame.draw.rect(shell, (accent, accent + 20, accent + 32, 40), pygame.Rect(14, 54, panel.w - 28, 4), border_radius=2)

        title = self._font_title.render(self.payload.get("title", "Secret Chamber"), True, (235, 219, 179))
        desc = self._font_sub.render(self.payload.get("description", "A hidden chamber."), True, (196, 182, 153))
        shell.blit(title, (20, 14))
        shell.blit(desc, (20, 62))

        map_label = self._font_hint.render("Room Layout", True, (215, 196, 148))
        shell.blit(map_label, (20, 95))

        map_rect = pygame.Rect(20, 123, panel.w - 40, max(208, int(panel.h * 0.46)))
        self._draw_tile_map(shell, panel, map_rect)

        notes_top = map_rect.bottom + 14
        lore_label = self._font_hint.render("Room Notes", True, (215, 196, 148))
        shell.blit(lore_label, (20, notes_top))

        body_rect = pygame.Rect(20, notes_top + 28, panel.w - 40, panel.h - (notes_top + 96))
        pygame.draw.rect(shell, (20, 18, 14, 190), body_rect, border_radius=8)
        pygame.draw.rect(shell, (131, 112, 79, 150), body_rect, 1, border_radius=8)

        max_w = body_rect.w - 18
        lines = _wrap_lines(self._detail_text or self.payload.get("lore", ""), self._font_body, max_w)
        line_step = 25
        paragraph_gap = 14
        visible_lines = max(1, body_rect.h // line_step)
        max_scroll = max(0, len(lines) - visible_lines)
        self._scroll = min(self._scroll, max_scroll)

        y = body_rect.y + 10
        for line in lines[self._scroll:self._scroll + visible_lines]:
            if line == "":
                y += paragraph_gap
                continue
            txt = self._font_body.render(line, True, (223, 214, 197))
            shell.blit(txt, (body_rect.x + 9, y))
            y += line_step

        self._notes_rect_abs = pygame.Rect(panel.x + body_rect.x, panel.y + body_rect.y, body_rect.w, body_rect.h)

        hover_text = self._hovered_hotspot_label or "Hover map zones to inspect; click to interact"
        hint = self._font_sub.render(f"Esc to close | {hover_text}", True, (170, 157, 130))
        shell.blit(hint, (20, panel.h - 26))

        surface.blit(shell, panel.topleft)
