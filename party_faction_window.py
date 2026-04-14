"""
Interactive party/faction overlay window for pygame UI.
"""

import pygame
from font_support import load_font

from faction_system import FACTIONS, get_faction_rank_visual_data
from pet_system import (
    PETS,
    PET_ADOPTION_COSTS,
    PET_FEED_COST_GOLD,
    PET_FEED_COOLDOWN_SECONDS,
    get_pet_bonus_preview,
    get_pet_ability_preview_lines,
)


class PartyFactionOverlay:
    """Fullscreen overlay with tabs for faction and companion management."""

    def __init__(self, gui):
        self.gui = gui
        self._alive = True

        self._tab = "faction"
        self._action_buttons = []
        self._faction_rank_hitboxes = []
        self._expanded_rank = None

        self._panel_rect = pygame.Rect(0, 0, 0, 0)
        self._close_rect = pygame.Rect(0, 0, 0, 0)
        self._faction_tab_rect = pygame.Rect(0, 0, 0, 0)
        self._party_tab_rect = pygame.Rect(0, 0, 0, 0)

        font_profile = getattr(gui, "font_profile", {}) or {}
        self._font_title = load_font(font_profile, 30, bold=True)
        self._font_header = load_font(font_profile, 22, bold=True)
        self._font_body = load_font(font_profile, 18)
        self._font_small = load_font(font_profile, 16)

    def is_open(self):
        return self._alive

    def close(self):
        self._alive = False

    def update(self, dt=0.016):
        _ = dt

    def _run_command(self, command):
        if not self.gui or not getattr(self.gui, "engine", None):
            return

        self.gui.append(f"> {command}", "command")
        resp = self.gui.engine.process_command(command)
        if resp:
            msg_type = self.gui._detect_type(resp) if hasattr(self.gui, "_detect_type") else None
            self.gui.append(resp, msg_type)

        if hasattr(self.gui, "_update_combat_status_from_engine"):
            self.gui._update_combat_status_from_engine()
        if hasattr(self.gui, "refresh_inventory_display"):
            self.gui.refresh_inventory_display()
        if hasattr(self.gui, "_refresh_hotbar"):
            self.gui._refresh_hotbar()

    def handle_event(self, event):
        if not self._alive:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.close()
                return True
            if event.key == pygame.K_TAB:
                self._tab = "party" if self._tab == "faction" else "faction"
                return True

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos

            if self._close_rect.collidepoint(pos):
                self.close()
                return True

            if self._faction_tab_rect.collidepoint(pos):
                self._tab = "faction"
                return True

            if self._party_tab_rect.collidepoint(pos):
                self._tab = "party"
                return True

            if self._tab == "faction":
                for rect, row in self._faction_rank_hitboxes:
                    if rect.collidepoint(pos):
                        rank = int(row.get("rank", 0))
                        self._expanded_rank = None if self._expanded_rank == rank else rank
                        return True

            for rect, command in self._action_buttons:
                if rect.collidepoint(pos):
                    self._run_command(command)
                    return True

            if self._panel_rect.collidepoint(pos):
                return True

        return False

    def _wrap_text(self, text, font, max_w):
        words = str(text or "").split()
        lines = []
        cur = ""
        for word in words:
            test = (cur + " " + word).strip()
            if font.size(test)[0] <= max_w:
                cur = test
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        return lines

    def _draw_button(self, surface, rect, label, command):
        mouse = pygame.mouse.get_pos()
        hover = rect.collidepoint(mouse)
        bg = (95, 70, 45) if hover else (72, 52, 34)
        border = (180, 146, 84)

        pygame.draw.rect(surface, bg, rect, border_radius=6)
        pygame.draw.rect(surface, border, rect, 2, border_radius=6)

        text = self._font_small.render(label, True, (240, 225, 185))
        surface.blit(text, (rect.x + 10, rect.y + (rect.height - text.get_height()) // 2))

        self._action_buttons.append((rect.copy(), command))

    def _draw_tabs(self, surface):
        mouse = pygame.mouse.get_pos()

        for rect, key, title in (
            (self._faction_tab_rect, "faction", "Faction"),
            (self._party_tab_rect, "party", "Companions"),
        ):
            active = self._tab == key
            hover = rect.collidepoint(mouse)
            base = (138, 102, 59) if active else (86, 63, 42)
            if hover and not active:
                base = (104, 74, 48)
            pygame.draw.rect(surface, base, rect, border_radius=8)
            pygame.draw.rect(surface, (206, 170, 107), rect, 2, border_radius=8)

            text = self._font_body.render(title, True, (246, 232, 196))
            surface.blit(text, (rect.centerx - text.get_width() // 2, rect.centery - text.get_height() // 2))

    def _draw_faction_tab(self, surface, content_rect):
        player = self.gui.engine.player
        state = player.state
        membership = state.get("faction_membership")
        rank_map = state.get("faction_rank", {})
        xp_map = state.get("faction_xp", {})

        y = content_rect.y + 8
        title = self._font_header.render("Faction Standing", True, (64, 38, 18))
        surface.blit(title, (content_rect.x, y))
        y += 36

        if membership and membership in FACTIONS:
            data = FACTIONS[membership]
            line_1 = f"Current: {data['name']}"
            line_2 = f"Rank: {int(rank_map.get(membership, 0))}"
            line_3 = f"XP: {int(xp_map.get(membership, 0))}"
            line_4 = f"Perk: {data.get('perk', 'N/A')}"
            for line in (line_1, line_2, line_3, line_4):
                txt = self._font_body.render(line, True, (48, 32, 16))
                surface.blit(txt, (content_rect.x, y))
                y += 28

            self._draw_button(
                surface,
                pygame.Rect(content_rect.right - 210, content_rect.y + 10, 190, 34),
                "Refresh Status",
                "faction status",
            )
            self._draw_button(
                surface,
                pygame.Rect(content_rect.right - 210, content_rect.y + 52, 190, 34),
                "Leave Faction",
                "faction leave",
            )

            card = pygame.Rect(content_rect.x, y + 8, content_rect.width, 92)
            pygame.draw.rect(surface, (234, 216, 173), card, border_radius=8)
            pygame.draw.rect(surface, (168, 132, 74), card, 2, border_radius=8)
            name = self._font_small.render(data["name"], True, (42, 26, 10))
            desc = self._font_small.render(data.get("description", ""), True, (76, 52, 22))
            surface.blit(name, (card.x + 10, card.y + 10))
            surface.blit(desc, (card.x + 10, card.y + 36))

            visual = get_faction_rank_visual_data(player, membership)
            rows = visual.get("ranks", [])
            table_top = card.bottom + 8
            table_h = content_rect.bottom - table_top - 8
            table = pygame.Rect(content_rect.x, table_top, content_rect.width, table_h)
            pygame.draw.rect(surface, (240, 226, 192), table, border_radius=8)
            pygame.draw.rect(surface, (168, 132, 74), table, 2, border_radius=8)

            self._faction_rank_hitboxes = []

            row_h = 22
            max_rows = max(1, (table.height - 10) // row_h)
            shown = rows[:max_rows]

            y0 = table.y + 6
            expanded_row_rect = None
            expanded_row_data = None
            for i, row in enumerate(shown):
                unlocked = bool(row.get("unlocked"))
                xp_met = bool(row.get("xp_met"))
                req_met = bool(row.get("requirements_met"))
                if unlocked:
                    col = (44, 110, 56)
                    status = "Unlocked"
                elif xp_met and req_met:
                    col = (88, 112, 44)
                    status = "Ready"
                else:
                    col = (118, 78, 44)
                    status = "Locked"

                rr = pygame.Rect(table.x + 6, y0 + i * row_h, table.width - 12, row_h - 2)
                pygame.draw.rect(surface, (248, 238, 210), rr, border_radius=5)
                pygame.draw.rect(surface, col, rr, 2 if int(row.get("rank", 0)) == self._expanded_rank else 1, border_radius=5)
                self._faction_rank_hitboxes.append((rr.copy(), row))

                reqs = row.get("requirements", [])
                req_done = sum(1 for r in reqs if r.get("met"))
                req_total = len(reqs)
                req_txt = "-" if req_total == 0 else f"{req_done}/{req_total} req"
                txt = f"R{row.get('rank')} {row.get('name')} | {row.get('xp_required')} XP | {req_txt} | {status}"
                surf = self._font_small.render(txt[:98], True, (52, 34, 14))
                surface.blit(surf, (rr.x + 6, rr.y + 2))

                if int(row.get("rank", 0)) == self._expanded_rank:
                    expanded_row_rect = rr
                    expanded_row_data = row

            if expanded_row_rect and expanded_row_data:
                details = []
                details.append(f"Requirements for Rank {expanded_row_data.get('rank')}:")
                reqs = expanded_row_data.get("requirements", [])
                if reqs:
                    for req in reqs:
                        check = "OK" if req.get("met") else "LOCKED"
                        details.append(f"- {req.get('label')}: {req.get('have')}/{req.get('needed')} ({check})")
                else:
                    details.append("- No special requirements")
                details.append("")
                details.append("Lore:")
                lore_lines = self._wrap_text(expanded_row_data.get("lore", ""), self._font_small, table.width - 24)
                details.extend(lore_lines)

                panel_h = 14 + (len(details) * 18)
                panel_w = table.width - 12
                dd_x = table.x + 6
                dd_y = expanded_row_rect.bottom + 4
                if dd_y + panel_h > table.bottom - 4:
                    dd_y = expanded_row_rect.y - panel_h - 4
                dd_y = max(table.y + 4, dd_y)

                dd = pygame.Rect(dd_x, dd_y, panel_w, min(panel_h, table.height - 8))
                pygame.draw.rect(surface, (252, 244, 221), dd, border_radius=8)
                pygame.draw.rect(surface, (116, 84, 46), dd, 2, border_radius=8)

                ty = dd.y + 8
                for line in details:
                    if ty + 16 > dd.bottom - 4:
                        break
                    ts = self._font_small.render(line[:112], True, (54, 35, 15))
                    surface.blit(ts, (dd.x + 8, ty))
                    ty += 18

            if len(rows) > len(shown):
                more = self._font_small.render(f"+{len(rows) - len(shown)} more ranks", True, (96, 68, 36))
                surface.blit(more, (table.right - more.get_width() - 8, table.bottom - more.get_height() - 4))
            return
        else:
            self._faction_rank_hitboxes = []
            self._expanded_rank = None
            txt = self._font_body.render("No faction joined this run.", True, (48, 32, 16))
            surface.blit(txt, (content_rect.x, y))
            y += 30
            txt = self._font_small.render("Choose one faction to lock in your allegiance:", True, (66, 42, 20))
            surface.blit(txt, (content_rect.x, y))
            y += 34

        card_w = (content_rect.width - 18) // 2
        card_h = 88
        col_gap = 18

        for idx, (fid, data) in enumerate(FACTIONS.items()):
            col = idx % 2
            row = idx // 2
            card_x = content_rect.x + col * (card_w + col_gap)
            card_y = y + row * (card_h + 14)
            card = pygame.Rect(card_x, card_y, card_w, card_h)

            pygame.draw.rect(surface, (234, 216, 173), card, border_radius=8)
            pygame.draw.rect(surface, (168, 132, 74), card, 2, border_radius=8)

            name = self._font_small.render(data["name"], True, (42, 26, 10))
            desc = self._font_small.render(data.get("perk", ""), True, (76, 52, 22))
            surface.blit(name, (card.x + 10, card.y + 10))
            surface.blit(desc, (card.x + 10, card.y + 34))

            if not membership:
                self._draw_button(
                    surface,
                    pygame.Rect(card.right - 104, card.bottom - 34, 94, 26),
                    "Join",
                    f"faction join {fid}",
                )

    def _draw_party_tab(self, surface, content_rect):
        player = self.gui.engine.player
        state = player.state
        pets = state.get("pets", {})
        active_pet = state.get("active_pet")

        y = content_rect.y + 8
        title = self._font_header.render("Companion Roster", True, (64, 38, 18))
        surface.blit(title, (content_rect.x, y))
        y += 36

        eco_line = self._font_small.render(
            f"Adopt: costs gold | Feed: {PET_FEED_COST_GOLD}g, cooldown {PET_FEED_COOLDOWN_SECONDS}s",
            True,
            (76, 52, 22),
        )
        surface.blit(eco_line, (content_rect.x, y))
        y += 26

        self._draw_button(
            surface,
            pygame.Rect(content_rect.right - 210, content_rect.y + 10, 190, 34),
            "Refresh Pets",
            "pet status",
        )

        if active_pet and active_pet in PETS:
            active_name = PETS[active_pet]["name"]
            txt = self._font_body.render(f"Active: {active_name}", True, (48, 32, 16))
            surface.blit(txt, (content_rect.x, y))
            self._draw_button(
                surface,
                pygame.Rect(content_rect.x + 250, y - 2, 130, 28),
                "Feed Active",
                "pet feed",
            )
            y += 34
        else:
            txt = self._font_body.render("Active: none", True, (48, 32, 16))
            surface.blit(txt, (content_rect.x, y))
            y += 34

        card_h = 80
        for idx, (pid, pdata) in enumerate(PETS.items()):
            card = pygame.Rect(content_rect.x, y + idx * (card_h + 10), content_rect.width, card_h)
            pygame.draw.rect(surface, (234, 216, 173), card, border_radius=8)
            pygame.draw.rect(surface, (168, 132, 74), card, 2, border_radius=8)

            owned = pid in pets
            level = int(pets.get(pid, {}).get("level", 1)) if owned else 1
            status = "Owned" if owned else "Not adopted"
            if pid == active_pet:
                status = "Active"
            adopt_cost = int(PET_ADOPTION_COSTS.get(pid, 150))

            name = self._font_small.render(PETS[pid]["name"], True, (42, 26, 10))
            bonus_text = get_pet_bonus_preview(pid, level)
            desc = self._font_small.render(f"{status} | Level {level} | {bonus_text}", True, (76, 52, 22))
            surface.blit(name, (card.x + 10, card.y + 10))
            surface.blit(desc, (card.x + 10, card.y + 34))

            ab_lines = get_pet_ability_preview_lines(pid, level, max_lines=1)
            if ab_lines:
                ab_txt = self._font_small.render(ab_lines[0][:72], True, (96, 68, 36))
                surface.blit(ab_txt, (card.x + 10, card.y + 56))
            elif not owned:
                price_txt = self._font_small.render(f"Adoption Cost: {adopt_cost}g", True, (96, 68, 36))
                surface.blit(price_txt, (card.x + 10, card.y + 56))

            if not owned:
                self._draw_button(
                    surface,
                    pygame.Rect(card.right - 112, card.bottom - 34, 102, 26),
                    "Adopt",
                    f"pet adopt {pid}",
                )
            elif pid != active_pet:
                self._draw_button(
                    surface,
                    pygame.Rect(card.right - 112, card.bottom - 34, 102, 26),
                    "Activate",
                    f"pet activate {pid}",
                )

            self._draw_button(
                surface,
                pygame.Rect(card.right - 224, card.bottom - 34, 102, 26),
                "Inspect",
                f"pet inspect {pid}",
            )

    def draw(self, surface):
        if not self._alive:
            return

        w, h = surface.get_size()
        dim = pygame.Surface((w, h), pygame.SRCALPHA)
        dim.fill((10, 10, 16, 165))
        surface.blit(dim, (0, 0))

        pw = min(900, w - 70)
        ph = min(640, h - 70)
        self._panel_rect = pygame.Rect((w - pw) // 2, (h - ph) // 2, pw, ph)

        panel = self._panel_rect
        pygame.draw.rect(surface, (244, 228, 190), panel, border_radius=12)
        pygame.draw.rect(surface, (140, 103, 54), panel, 3, border_radius=12)

        header_rect = pygame.Rect(panel.x, panel.y, panel.width, 62)
        pygame.draw.rect(surface, (125, 86, 48), header_rect, border_radius=12)
        title = self._font_title.render("Party and Faction", True, (250, 234, 196))
        surface.blit(title, (panel.x + 18, panel.y + 14))

        self._close_rect = pygame.Rect(panel.right - 54, panel.y + 14, 36, 30)
        pygame.draw.rect(surface, (168, 60, 54), self._close_rect, border_radius=6)
        x_txt = self._font_body.render("X", True, (255, 236, 220))
        surface.blit(x_txt, (self._close_rect.centerx - x_txt.get_width() // 2, self._close_rect.y + 2))

        self._faction_tab_rect = pygame.Rect(panel.x + 20, panel.y + 74, 170, 36)
        self._party_tab_rect = pygame.Rect(panel.x + 202, panel.y + 74, 190, 36)
        self._draw_tabs(surface)

        content_rect = pygame.Rect(panel.x + 20, panel.y + 126, panel.width - 40, panel.height - 146)
        pygame.draw.rect(surface, (248, 236, 205), content_rect, border_radius=10)
        pygame.draw.rect(surface, (184, 150, 90), content_rect, 2, border_radius=10)

        self._action_buttons = []
        if self._tab == "faction":
            self._draw_faction_tab(surface, content_rect)
        else:
            self._draw_party_tab(surface, content_rect)

        hint = self._font_small.render("ESC closes. TAB switches tabs.", True, (88, 60, 34))
        surface.blit(hint, (panel.x + 20, panel.bottom - 24))
