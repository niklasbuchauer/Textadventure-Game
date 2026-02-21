# journal_window.py  –  Animated old-book quest journal overlay
#
# Renders a two-page open-book journal directly onto the pygame surface
# (no pygame_gui widgets) so it can have fully custom visual style and
# frame-accurate animations.
#
# Public interface (matches the _sub_windows contract):
#   handle_event(event) -> bool      consumed?
#   update(dt=0.016)
#   draw(surface)
#   is_open() -> bool

import pygame
import math
import random

# ── Colour palette ────────────────────────────────────────────────────────────

C_PARCHMENT    = (238, 220, 178)   # aged paper
C_PARCHMENT_L  = (248, 234, 196)   # lighter page (right side)
C_INK          = ( 38,  22,   6)   # dark writing ink
C_INK_MID      = ( 80,  50,  18)   # medium ink (sub-text)
C_INK_LIGHT    = (130,  98,  50)   # faded ink
C_HEADER       = (128,  30,  20)   # red/brown chapter headings
C_LEATHER      = ( 72,  38,  12)   # spine leather
C_COVER        = ( 88,  50,  18)   # book border/cover
C_SPINE_LINE   = ( 52,  26,   8)   # spine stitching
C_SELECT_BG    = (210, 180, 118)   # selected-quest highlight
C_DONE         = ( 52, 108,  48)   # completed / done green
C_DIVIDER      = (175, 152, 108)   # horizontal rule

# ── Easing helpers ────────────────────────────────────────────────────────────

def _ease_out_cubic(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return 1.0 - (1.0 - t) ** 3

def _ease_in_out(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return 4 * t ** 3 if t < 0.5 else 1.0 - ((-2 * t + 2) ** 3) / 2

# ── Utility ───────────────────────────────────────────────────────────────────

def _blend(col, bg, alpha_0_1: float):
    """Blend col towards bg.  alpha_0_1=1 → pure col,  0 → pure bg."""
    a = max(0.0, min(1.0, alpha_0_1))
    return tuple(int(c * a + b * (1 - a)) for c, b in zip(col[:3], bg[:3]))

def _wrap_text(text: str, font: pygame.font.Font, max_w: int) -> list:
    words = text.split()
    lines: list = []
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
    return lines or [text]

def _font_pick(size: int, bold: bool = False) -> pygame.font.Font:
    """Load the best available serif/antiqua font."""
    for name in ("Palatino Linotype", "Book Antiqua", "Georgia",
                 "Times New Roman", "serif"):
        f = pygame.font.SysFont(name, size, bold=bold)
        if f is not None:
            return f
    return pygame.font.Font(None, size)


# ═══════════════════════════════════════════════════════════════════════════════
class JournalWindow:
    """
    Full-screen book overlay for the Quest Journal.
    Draws directly to the game surface (not a pygame_gui UIWindow).
    """

    OPEN_DUR    = 0.38   # seconds – book opening animation
    CLOSE_DUR   = 0.26
    CONTENT_DUR = 0.30   # text fade-in after open
    TURN_DUR    = 0.22   # right-page turn flash

    # Pre-built aged-texture spots (seeded, so they don't flicker each frame)
    _SPOTS_SEED = 7331

    def __init__(self, gui):
        self.gui = gui

        # State
        self._alive    = True
        self._closing  = False
        self._anim     = 0.0      # 0→1 open, 1→0 close
        self._cfade    = 0.0      # 0→1 content fade
        self._turn_t   = 1.0      # page-turn timer (1 = idle)
        self._turn_dir = 1

        # Data
        self._active:    list = []
        self._completed: list = []
        self._sel_idx:   int  = 0

        # Click-region cache (absolute screen coords)
        self._book_rect:       pygame.Rect = pygame.Rect(0, 0, 0, 0)
        self._close_rect:      pygame.Rect = pygame.Rect(0, 0, 0, 0)
        self._refresh_rect:    pygame.Rect = pygame.Rect(0, 0, 0, 0)
        self._quest_rows:      list        = []   # [(abs_rect, index), …]

        # Particles: [x, y, vx, vy, age, max_age, radius]
        self._particles: list = []

        # Font cache  {(size, bold): Font}
        self._fcache: dict = {}

        self._refresh_quests()

    # ── Lifecycle ──────────────────────────────────────────────────────────────

    def is_open(self) -> bool:
        return self._alive

    def close(self):
        if not self._closing:
            self._closing = True

    # ── Font helpers ───────────────────────────────────────────────────────────

    def _f(self, size: int, bold: bool = False) -> pygame.font.Font:
        key = (size, bold)
        if key not in self._fcache:
            self._fcache[key] = _font_pick(size, bold)
        return self._fcache[key]

    # ── Data ───────────────────────────────────────────────────────────────────

    def _refresh_quests(self):
        try:
            qm = self.gui.engine.quest_manager
            self._active    = qm.get_active_quests()    # list of (qdef, qs)
            self._completed = qm.get_completed_quests() # list of qdef
        except Exception:
            self._active    = []
            self._completed = []
        self._sel_idx = max(0, min(self._sel_idx, len(self._active) - 1))
        self._cfade   = 0.0   # re-fade content after refresh

    # ── Update ─────────────────────────────────────────────────────────────────

    def update(self, dt: float = 0.016):
        if self._closing:
            self._anim = max(0.0, self._anim - dt / self.CLOSE_DUR)
            if self._anim <= 0.0:
                self._alive = False
            return
        self._anim  = min(1.0, self._anim  + dt / self.OPEN_DUR)
        self._cfade = min(1.0, self._cfade + dt / self.CONTENT_DUR)
        self._turn_t = min(1.0, self._turn_t + dt / self.TURN_DUR)
        self._update_particles(dt)

    def _update_particles(self, dt: float):
        if random.random() < dt * 3.5 and len(self._particles) < 22:
            self._particles.append([
                random.uniform(-20, 20),     # x  (relative to book-top-centre)
                random.uniform(-4, 4),       # y
                random.uniform(-12, 12),     # vx
                random.uniform(-28, -12),    # vy  (drift upward)
                0.0,                         # age
                random.uniform(1.8, 3.6),    # max_age
                random.uniform(1.0, 2.2),    # radius
            ])
        for p in self._particles:
            p[4] += dt
            p[0] += p[2] * dt
            p[1] += p[3] * dt
        self._particles = [p for p in self._particles if p[4] < p[5]]

    # ── Events ─────────────────────────────────────────────────────────────────

    def handle_event(self, event: pygame.event.Event) -> bool:
        if not self._alive or self._closing:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_j):
                self.close()
                return True
            if event.key == pygame.K_UP:
                self._move_sel(-1)
                return True
            if event.key == pygame.K_DOWN:
                self._move_sel(1)
                return True
            if event.key == pygame.K_r:
                self._refresh_quests()
                return True

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            # Close
            if self._close_rect.collidepoint(pos):
                self.close()
                return True
            # Refresh
            if self._refresh_rect.collidepoint(pos):
                self._refresh_quests()
                return True
            # Quest row
            for rect, idx in self._quest_rows:
                if rect.collidepoint(pos):
                    if self._sel_idx != idx:
                        self._start_turn(1 if idx > self._sel_idx else -1)
                        self._sel_idx = idx
                    return True
            # Click outside book → close
            if not self._book_rect.collidepoint(pos):
                self.close()
            return True

        if event.type == pygame.MOUSEWHEEL:
            # Scroll through quest list
            self._move_sel(-event.y)
            return True

        return False

    def _move_sel(self, delta: int):
        n = len(self._active)
        if n == 0:
            return
        new = max(0, min(n - 1, self._sel_idx + delta))
        if new != self._sel_idx:
            self._start_turn(1 if delta > 0 else -1)
            self._sel_idx = new

    def _start_turn(self, direction: int):
        self._turn_dir = direction
        self._turn_t   = 0.0
        self._cfade    = 0.2   # small dip then recover

    # ── Draw ───────────────────────────────────────────────────────────────────

    def draw(self, surface: pygame.Surface):
        if not self._alive:
            return

        scale  = _ease_out_cubic(self._anim)
        if scale < 0.02:
            return

        sw, sh = surface.get_size()

        # Book dimensions at full size
        BW = min(820, sw - 40)
        BH = min(575, sh - 40)
        bx = (sw - BW) // 2
        by = (sh - BH) // 2

        # Semi-transparent dark backdrop
        bg_alpha = int(165 * scale)
        bg = pygame.Surface((sw, sh), pygame.SRCALPHA)
        bg.fill((0, 0, 0, bg_alpha))
        surface.blit(bg, (0, 0))

        # Scale effect: draw book to offscreen surface, scale, blit
        if scale < 0.995:
            sbw = max(2, int(BW * scale))
            sbh = max(2, int(BH * scale))
            book_surf = pygame.Surface((BW, BH), pygame.SRCALPHA)
            self._draw_book(book_surf, BW, BH, 0, 0)
            scaled = pygame.transform.smoothscale(book_surf, (sbw, sbh))
            sx = (sw - sbw) // 2
            sy = (sh - sbh) // 2
            surface.blit(scaled, (sx, sy))
            self._book_rect = pygame.Rect(sx, sy, sbw, sbh)
            # Adjust click-regions for scale
            scale_factor = sbw / BW
            self._book_rect  = pygame.Rect(sx, sy, sbw, sbh)
            # For scaled book, click regions need re-mapping
            self._close_rect   = self._scale_rect(bx, by, BW, BH, sw, sh,
                                                   BW - 34, 6, 26, 26, sx, sy, scale_factor)
            self._refresh_rect = self._scale_rect(bx, by, BW, BH, sw, sh,
                                                   BW - 34, BH - 38, 26, 26, sx, sy, scale_factor)
        else:
            self._draw_book(surface, BW, BH, bx, by)
            self._book_rect = pygame.Rect(bx, by, BW, BH)

        # Dust particles (absolute screen coords, above book)
        cx = sw // 2
        cy = by + 20
        for p in self._particles:
            lf = 1.0 - (p[4] / p[5])
            a  = int(190 * lf * scale)
            r  = max(1, int(p[6]))
            ps = pygame.Surface((r * 2 + 2, r * 2 + 2), pygame.SRCALPHA)
            pygame.draw.circle(ps, (200, 172, 118, a), (r + 1, r + 1), r)
            surface.blit(ps, (int(cx + p[0]) - r - 1, int(cy + p[1]) - r - 1))

    @staticmethod
    def _scale_rect(bx, by, BW, BH, sw, sh, rx, ry, rw, rh, sx, sy, sf):
        return pygame.Rect(
            int(sx + rx * sf), int(sy + ry * sf),
            int(rw * sf),      int(rh * sf)
        )

    # ── Core book draw ─────────────────────────────────────────────────────────

    def _draw_book(self, surf: pygame.Surface, BW: int, BH: int,
                   ox: int, oy: int):
        """Draw the open book onto `surf` at offset (ox, oy)."""
        MID = ox + BW // 2
        cf  = self._cfade   # content alpha  0→1

        # ── Drop shadow ────────────────────────────────────────────────────────
        sh_surf = pygame.Surface((BW + 28, BH + 28), pygame.SRCALPHA)
        pygame.draw.rect(sh_surf, (0, 0, 0, 85),
                         pygame.Rect(16, 16, BW, BH), border_radius=10)
        surf.blit(sh_surf, (ox - 14, oy - 14))

        # ── Left page ──────────────────────────────────────────────────────────
        lp = pygame.Rect(ox, oy, BW // 2 + 3, BH)
        pygame.draw.rect(surf, C_PARCHMENT, lp, border_radius=8)

        # ── Right page ─────────────────────────────────────────────────────────
        rp = pygame.Rect(MID - 2, oy, BW // 2 + 2, BH)
        pygame.draw.rect(surf, C_PARCHMENT_L, rp, border_radius=8)

        # ── Aged texture spots ─────────────────────────────────────────────────
        rng = random.Random(self._SPOTS_SEED)
        spot_surf = pygame.Surface((BW, BH), pygame.SRCALPHA)
        for _ in range(130):
            sx_rel = rng.randint(6, BW - 6)
            sy_rel = rng.randint(6, BH - 6)
            r  = rng.randint(2, 7)
            a  = rng.randint(10, 30)
            pygame.draw.circle(spot_surf, (90, 60, 22, a),
                               (sx_rel, sy_rel), r)
        surf.blit(spot_surf, (ox, oy))

        # ── Spine ──────────────────────────────────────────────────────────────
        spine = pygame.Rect(MID - 11, oy, 22, BH)
        pygame.draw.rect(surf, C_LEATHER, spine)
        # Highlight strip
        pygame.draw.rect(surf, C_COVER,
                         pygame.Rect(MID - 4, oy, 4, BH))
        # Stitching lines
        for i in range(1, 7):
            ly = oy + int(BH * i / 7)
            pygame.draw.rect(surf, C_SPINE_LINE,
                             pygame.Rect(MID - 11, ly - 2, 22, 4),
                             border_radius=1)

        # ── Page edges / outer border ──────────────────────────────────────────
        pygame.draw.rect(surf, C_COVER,
                         pygame.Rect(ox, oy, BW, BH), width=3, border_radius=8)

        # ── Inner page frames ──────────────────────────────────────────────────
        pad = 16
        lf_rect = pygame.Rect(ox + pad, oy + pad,
                               BW // 2 - pad - 14, BH - pad * 2)
        rf_rect = pygame.Rect(MID + 14, oy + pad,
                               BW // 2 - pad - 14, BH - pad * 2)
        pygame.draw.rect(surf, C_INK_LIGHT, lf_rect, width=1)
        pygame.draw.rect(surf, C_INK_LIGHT, rf_rect, width=1)

        # ── Content ────────────────────────────────────────────────────────────
        self._draw_left_page(surf, lf_rect, cf, ox, oy)
        self._draw_right_page(surf, rf_rect, cf, ox, oy)

        # ── Content fade-in overlay (per page) ────────────────────────────────
        fade_a = int(255 * (1.0 - cf))
        if fade_a > 4:
            for rect in (lf_rect, rf_rect):
                fs = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
                base = C_PARCHMENT if rect == lf_rect else C_PARCHMENT_L
                fs.fill((*base, fade_a))
                surf.blit(fs, (rect.x, rect.y))

        # ── Page-turn shimmer on right page ────────────────────────────────────
        if self._turn_t < 1.0:
            progress = _ease_in_out(self._turn_t)
            shimmer_a = int(100 * math.sin(progress * math.pi))
            if shimmer_a > 2:
                ts = pygame.Surface((rf_rect.width, rf_rect.height), pygame.SRCALPHA)
                ts.fill((255, 250, 230, shimmer_a))
                surf.blit(ts, (rf_rect.x, rf_rect.y))

        # ── Close button (top-right corner) ────────────────────────────────────
        cbr = pygame.Rect(ox + BW - 34, oy + 6, 26, 26)
        mx, my = pygame.mouse.get_pos()
        # Adjust mouse pos if drawn to offscreen surface
        ch = (mx - ox, my - oy) if (ox, oy) != (0, 0) else (mx, my)
        c_hover = cbr.collidepoint(ox + BW - 34, oy + 6) or cbr.collidepoint(*ch)
        c_col   = (190, 80, 60) if c_hover else (148, 56, 40)
        pygame.draw.rect(surf, c_col, cbr, border_radius=5)
        ct_s = self._f(13, bold=True).render("✕", True, (255, 238, 228))
        surf.blit(ct_s, ct_s.get_rect(center=cbr.center))
        self._close_rect = cbr.move(ox, oy) if (ox, oy) != (0, 0) else cbr

        # ── Refresh button (bottom-right) ──────────────────────────────────────
        rbr = pygame.Rect(ox + BW - 34, oy + BH - 36, 26, 26)
        r_hover = rbr.collidepoint(*ch)
        r_col   = (78, 112, 55) if r_hover else (60, 88, 42)
        pygame.draw.rect(surf, r_col, rbr, border_radius=5)
        rt_s = self._f(14).render("↺", True, (210, 238, 195))
        surf.blit(rt_s, rt_s.get_rect(center=rbr.center))
        self._refresh_rect = rbr.move(ox, oy) if (ox, oy) != (0, 0) else rbr

    # ── Left page: quest list ──────────────────────────────────────────────────

    def _draw_left_page(self, surf, frame: pygame.Rect, cf: float,
                        ox: int, oy: int):
        ink   = _blend(C_INK,      C_PARCHMENT,   cf)
        mid   = _blend(C_INK_MID,  C_PARCHMENT,   cf)
        head  = _blend(C_HEADER,   C_PARCHMENT,   cf)
        light = _blend(C_INK_LIGHT,C_PARCHMENT,   cf)
        div   = _blend(C_DIVIDER,  C_PARCHMENT,   cf)
        done  = _blend(C_DONE,     C_PARCHMENT,   cf)

        # ── Page title ─────────────────────────────────────────────────────────
        t_surf = self._f(17, bold=True).render("Active Quests", True, head)
        surf.blit(t_surf, (frame.x + 6, frame.y + 5))
        x1, x2 = frame.x + 4, frame.x + frame.width - 4
        pygame.draw.line(surf, div, (x1, frame.y + 27), (x2, frame.y + 27), 1)

        # ── Decorative scroll flourishes ───────────────────────────────────────
        # Small diamond
        dm_x, dm_y = frame.x + frame.width // 2, frame.y + 27
        pygame.draw.polygon(surf, div,
                            [(dm_x, dm_y - 4), (dm_x + 4, dm_y),
                             (dm_x, dm_y + 4), (dm_x - 4, dm_y)])

        # ── Quest rows ─────────────────────────────────────────────────────────
        self._quest_rows = []
        y = frame.y + 36

        if not self._active:
            es = self._f(12).render("No active quests.", True, mid)
            surf.blit(es, (frame.x + 8, y + 6))
        else:
            mx, my = pygame.mouse.get_pos()
            for i, (qdef, qs) in enumerate(self._active):
                row_h  = 40
                qrect  = pygame.Rect(frame.x, y, frame.width, row_h)
                # Absolute screen rect for hit-testing
                abs_r  = qrect.move(ox, oy) if (ox, oy) != (0, 0) else qrect
                self._quest_rows.append((abs_r, i))

                is_sel = (i == self._sel_idx)
                is_hov = abs_r.collidepoint(mx, my)

                if is_sel:
                    hs = pygame.Surface((frame.width, row_h), pygame.SRCALPHA)
                    hs.fill((*C_SELECT_BG, int(175 * cf)))
                    surf.blit(hs, (frame.x, y))
                elif is_hov:
                    hs = pygame.Surface((frame.width, row_h), pygame.SRCALPHA)
                    hs.fill((*C_SELECT_BG, int(80 * cf)))
                    surf.blit(hs, (frame.x, y))

                # Status dot
                try:
                    from quest_system import QuestState
                    ready = qs.status == QuestState.STATUS_COMPLETE
                except Exception:
                    ready = False
                dot_col = done if ready else head
                pygame.draw.circle(surf, dot_col, (frame.x + 11, y + 10), 4)
                if ready:
                    pygame.draw.circle(surf, _blend(C_PARCHMENT, C_DONE, 0.5),
                                       (frame.x + 11, y + 10), 2)

                # Quest name
                ns = self._f(13, bold=is_sel).render(
                    qdef["name"][:30], True, ink if is_sel else mid)
                surf.blit(ns, (frame.x + 22, y + 2))

                # Sub-text: progress
                try:
                    from quest_system import QuestState
                    if qs.status == QuestState.STATUS_COMPLETE:
                        sub = "Ready to turn in"
                        sc  = done
                    else:
                        done_n = sum(1 for k, obj in enumerate(qdef["objectives"])
                                     if qs.progress.get(k, 0) >= obj.get("count", 1))
                        tot   = len(qdef["objectives"])
                        sub   = f"{done_n}/{tot} objectives"
                        sc    = light
                except Exception:
                    sub = ""
                    sc  = light
                if sub:
                    ss = self._f(10).render(sub, True, sc)
                    surf.blit(ss, (frame.x + 23, y + 20))

                # Row divider
                if i < len(self._active) - 1:
                    pygame.draw.line(surf, div,
                                     (frame.x + 4, y + row_h - 1),
                                     (frame.x + frame.width - 4, y + row_h - 1), 1)

                y += row_h
                if y > frame.bottom - 24:
                    break

        # ── Footer: completed count ────────────────────────────────────────────
        fc_s = self._f(11).render(
            f"Completed: {len(self._completed)}", True, light)
        surf.blit(fc_s, (frame.x + 4, frame.bottom - 15))

    # ── Right page: quest detail ───────────────────────────────────────────────

    def _draw_right_page(self, surf, frame: pygame.Rect, cf: float,
                         ox: int, oy: int):
        ink   = _blend(C_INK,      C_PARCHMENT_L, cf)
        mid   = _blend(C_INK_MID,  C_PARCHMENT_L, cf)
        head  = _blend(C_HEADER,   C_PARCHMENT_L, cf)
        light = _blend(C_INK_LIGHT,C_PARCHMENT_L, cf)
        div   = _blend(C_DIVIDER,  C_PARCHMENT_L, cf)
        done  = _blend(C_DONE,     C_PARCHMENT_L, cf)

        # ── No active quests ───────────────────────────────────────────────────
        if not self._active:
            title_s = self._f(16, bold=True).render("Your Story Awaits", True, head)
            surf.blit(title_s, (frame.x + 6, frame.y + 5))
            pygame.draw.line(surf, div,
                             (frame.x + 4, frame.y + 27),
                             (frame.x + frame.width - 4, frame.y + 27), 1)
            flavour = [
                "",
                "The pages are still blank.",
                "",
                "Seek out the people of this",
                "world — merchants, scholars,",
                "wanderers and kings.",
                "",
                "Every quest begins with a",
                "simple conversation.",
                "",
                "",
                "— J to close this journal —",
            ]
            y = frame.y + 36
            for line in flavour:
                s = self._f(12 if line.startswith("—") else 12).render(
                    line, True, mid if not line.startswith("—") else light)
                surf.blit(s, (frame.x + 8, y))
                y += 18
            return

        # ── Selected quest detail ──────────────────────────────────────────────
        idx        = max(0, min(self._sel_idx, len(self._active) - 1))
        qdef, qs   = self._active[idx]

        # Title
        ts = self._f(16, bold=True).render(qdef["name"][:34], True, head)
        surf.blit(ts, (frame.x + 6, frame.y + 5))
        x1, x2 = frame.x + 4, frame.x + frame.width - 4
        pygame.draw.line(surf, div, (x1, frame.y + 27), (x2, frame.y + 27), 1)

        y = frame.y + 34

        # Description – word-wrapped
        desc = qdef.get("description", "")
        for i, line in enumerate(_wrap_text(desc, self._f(12), frame.width - 16)):
            s = self._f(12).render(line, True, mid)
            surf.blit(s, (frame.x + 8, y))
            y += 17
            if y > frame.y + 118:
                # Ellipsis if truncated
                s = self._f(10).render("…", True, light)
                surf.blit(s, (frame.x + 8, y - 17 + 3))
                break

        y += 6
        # Objective divider + header
        pygame.draw.line(surf, div, (x1, y), (x2, y), 1)
        y += 5
        oh_s = self._f(13, bold=True).render("Objectives", True, ink)
        surf.blit(oh_s, (frame.x + 6, y))
        y += 20

        try:
            from quest_system import QuestState
        except Exception:
            QuestState = None

        for i, obj in enumerate(qdef["objectives"]):
            prog  = qs.progress.get(i, 0)
            count = obj.get("count", 1)
            is_done = prog >= count

            # Bullet circle
            bc = done if is_done else _blend((165, 132, 75), C_PARCHMENT_L, cf)
            pygame.draw.circle(surf, bc, (frame.x + 11, y + 7), 4)
            if is_done:
                pygame.draw.circle(surf, _blend(C_PARCHMENT_L, C_DONE, 0.45),
                                   (frame.x + 11, y + 7), 2)

            obj_text = obj.get("description", "")
            if obj["type"] in ("kill", "collect"):
                obj_text += f"  ({prog}/{count})"

            t_col = done if is_done else ink
            for j, line in enumerate(_wrap_text(obj_text, self._f(12), frame.width - 28)):
                s = self._f(12).render(line, True, t_col)
                surf.blit(s, (frame.x + 22, y + j * 16))
            lines_n = len(_wrap_text(obj_text, self._f(12), frame.width - 28))
            y += max(18, lines_n * 16 + 4)

            if y > frame.bottom - 46:
                break

        # ── Turn-in / hint footer ──────────────────────────────────────────────
        pygame.draw.line(surf, div,
                         (x1, frame.bottom - 26),
                         (x2, frame.bottom - 26), 1)
        try:
            if QuestState and qs.status == QuestState.STATUS_COMPLETE:
                qm       = self.gui.engine.quest_manager
                npc_name = qm._npc_display_name(
                    qdef.get("turn_in", qdef.get("giver", "the quest giver")))
                foot_s = self._f(11).render(
                    f"Return to {npc_name} to claim your reward.", True, done)
            else:
                foot_s = self._f(11).render(
                    "Press J or Esc to close  ·  R to refresh", True, light)
        except Exception:
            foot_s = self._f(11).render("Press J to close", True, light)
        surf.blit(foot_s, (frame.x + 5, frame.bottom - 18))


# ── Quick standalone test ─────────────────────────────────────────────────────
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1024, 720))
    pygame.display.set_caption("Journal test")
    clock  = pygame.time.Clock()

    class _FakeQS:
        STATUS_COMPLETE = "complete"
        progress = {0: 2, 1: 0}
        status   = "active"

    class _FakeQM:
        def get_active_quests(self):
            return [
                ({"id": "q1", "name": "The Lost Sword",
                  "description": "Find the legendary blade of the fallen king in the depths of the dungeon.",
                  "objectives": [{"type": "collect", "description": "Find the sword",
                                  "count": 1},
                                 {"type": "talk",    "description": "Return to Aldric",
                                  "count": 1}]},
                 _FakeQS()),
                ({"id": "q2", "name": "Pest Control",
                  "description": "The inn is overrun with giant rats. Clear them out.",
                  "objectives": [{"type": "kill", "description": "Kill giant rats",
                                  "count": 5}]},
                 type("QS", (), {"progress": {0: 3}, "status": "active"})()),
            ]
        def get_completed_quests(self):
            return [{"id": "q0", "name": "A Simple Errand"}]
        def _npc_display_name(self, n): return n or "???"

    class _FakeEngine:
        quest_manager = _FakeQM()

    class _FakeGUI:
        engine = _FakeEngine()

    jw = JournalWindow(_FakeGUI())
    running = True
    while running:
        dt = clock.tick(60) / 1000
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            jw.handle_event(ev)
        jw.update(dt)
        screen.fill((30, 30, 30))
        jw.draw(screen)
        if not jw.is_open():
            running = False
        pygame.display.flip()
    pygame.quit()
