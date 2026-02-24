# searchable_rooms_window.py  –  Parchment book room browser overlay
#
# Pure-pygame, no pygame_gui widgets.  Follows the same pattern as
# journal_window.py for full visual consistency.
#
# Public interface:
#   handle_event(event) -> bool      consumed?
#   update(dt=0.016)
#   draw(surface)
#   is_open() -> bool

import pygame
import math
import random

# ── Shared colour palette (mirrors journal_window.py) ─────────────────────────
C_PARCHMENT    = (238, 220, 178)
C_PARCHMENT_L  = (248, 234, 196)
C_INK          = ( 38,  22,   6)
C_INK_MID      = ( 80,  50,  18)
C_INK_LIGHT    = (130,  98,  50)
C_HEADER       = (128,  30,  20)
C_LEATHER      = ( 72,  38,  12)
C_COVER        = ( 88,  50,  18)
C_SPINE_LINE   = ( 52,  26,   8)
C_SELECT_BG    = (210, 180, 118)
C_DIVIDER      = (175, 152, 108)
C_SEARCH_BORDER= (130,  98,  50)
C_SEARCH_BG    = (228, 210, 168)

# Region accent colours
REGION_COLORS = {
    "MAINLAND":          ( 80, 110, 140),
    "SUNSTONE ATOLL":    (170, 140,  55),
    "EMERALD ISLE":      ( 55, 130,  75),
    "STORMBREAK REEF":   ( 80, 100, 160),
    "CINDERFORGE ISLE":  (160,  80,  50),
    "DREADMIST ISLE":    (110,  65, 130),
    "WYRMSCALE ISLE":    (150,  50,  40),
    "THE ABYSSAL REACH": (120,  55, 155),
    "DUNGEONS":          (160,  95,  40),
    "OTHER":             ( 90,  90,  90),
}

# Ordered region list: (display_name, id_prefix_list)
REGIONS = [
    ("MAINLAND",          ["port_haven", "blackwood", "harbor", "grand_", "bramble",
                           "swamp", "dark_tor", "hermit", "mine", "river", "cave",
                           "village", "town", "market", "tavern", "shrine", "forest",
                           "road", "crossroads", "gatehouse"]),
    ("SUNSTONE ATOLL",    ["sunstone"]),
    ("EMERALD ISLE",      ["emerald"]),
    ("STORMBREAK REEF",   ["stormbreak"]),
    ("CINDERFORGE ISLE",  ["cinder"]),
    ("DREADMIST ISLE",    ["dreadmist"]),
    ("WYRMSCALE ISLE",    ["wyrm"]),
    ("THE ABYSSAL REACH", ["abyssal"]),
    ("DUNGEONS",          ["dungeon_", "crystal_", "iron_hall", "shadow_", "sunken_",
                           "frozen_", "molten_", "tempest_", "verdant_", "void_",
                           "wyrms_", "halls_"]),
    ("OTHER",             []),
]
REGION_ORDER = [r[0] for r in REGIONS]


# ── Easing helpers ────────────────────────────────────────────────────────────
def _ease_out_cubic(t):
    t = max(0.0, min(1.0, t))
    return 1.0 - (1.0 - t) ** 3

def _blend(col, bg, alpha):
    a = max(0.0, min(1.0, alpha))
    return tuple(int(c * a + b * (1 - a)) for c, b in zip(col[:3], bg[:3]))

def _wrap_text(text, font, max_w):
    words = str(text).split()
    lines, cur = [], ""
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
    return lines or [str(text)]

def _font_pick(size, bold=False):
    for name in ("Palatino Linotype", "Book Antiqua", "Georgia",
                 "Times New Roman", "serif"):
        f = pygame.font.SysFont(name, size, bold=bold)
        if f is not None:
            return f
    return pygame.font.Font(None, size)


# ── Data helpers ──────────────────────────────────────────────────────────────
def _region_for(room_id: str):
    rid = room_id.lower()
    for name, prefixes in REGIONS[:-1]:
        for p in prefixes:
            if rid.startswith(p) or p in rid:
                return name
    return REGIONS[-1][0]


def _build_room_registry(engine):
    registry = {}
    try:
        raw_rooms = engine.rooms
    except AttributeError:
        return registry

    for rid, rdata in raw_rooms.items():
        if hasattr(rdata, "name"):
            name        = rdata.name or rid
            description = getattr(rdata, "description", "")
            loc_type    = getattr(rdata, "location_type", "")
            exits       = dict(getattr(rdata, "exits", {}))
            npcs        = list(getattr(rdata, "npcs", []) or [])
            items       = getattr(rdata, "items", {})
            coordinates = getattr(rdata, "coordinates", None)
        else:
            name        = rdata.get("name", rid)
            description = rdata.get("description", "")
            loc_type    = rdata.get("location_type", "")
            exits       = dict(rdata.get("exits", {}))
            npcs        = list(rdata.get("npcs", []) or [])
            items       = rdata.get("items", {})
            coordinates = rdata.get("coordinates", None)

        region = _region_for(rid)
        registry[rid] = {
            "name":        name,
            "id":          rid,
            "description": description,
            "loc_type":    loc_type,
            "exits":       exits,
            "npcs":        npcs,
            "items":       items,
            "coordinates": coordinates,
            "region":      region,
        }
    return registry



# ═══════════════════════════════════════════════════════════════════════════════
class RoomsOverlay:
    """
    Full-screen parchment room browser overlay.
    Left page: search + room list.  Right page: selected room detail.
    """

    OPEN_DUR    = 0.38
    CLOSE_DUR   = 0.26
    CONTENT_DUR = 0.30
    _SPOTS_SEED = 6173

    def __init__(self, gui, engine):
        self.gui     = gui
        self._engine = engine
        self._alive   = True
        self._closing = False
        self._anim    = 0.0
        self._cfade   = 0.0

        self._registry: dict = {}
        self._flat:     list = []   # [(region|None, rid|None, label), …]
        self._sel_idx:  int  = -1

        self._search_text:   str  = ""
        self._search_active: bool = False
        self._scroll:        int  = 0
        self._rows_visible:  int  = 0

        self._book_rect   = pygame.Rect(0, 0, 0, 0)
        self._close_rect  = pygame.Rect(0, 0, 0, 0)
        self._search_rect = pygame.Rect(0, 0, 0, 0)
        self._row_rects: list = []
        self._sf    = 1.0
        self._dst_x = 0
        self._dst_y = 0

        self._fcache: dict = {}
        self._load_data()

    # ── Lifecycle ──────────────────────────────────────────────────────────────

    def is_open(self) -> bool:
        return self._alive

    def close(self):
        if not self._closing:
            self._closing = True

    # ── Fonts ──────────────────────────────────────────────────────────────────

    def _f(self, size, bold=False):
        key = (size, bold)
        if key not in self._fcache:
            self._fcache[key] = _font_pick(size, bold)
        return self._fcache[key]

    # ── Data ───────────────────────────────────────────────────────────────────

    def _load_data(self):
        self._registry = _build_room_registry(self._engine)
        self._apply_filter("")

    def _apply_filter(self, query):
        q = query.lower().strip()
        if q:
            matches = {
                rid: d for rid, d in self._registry.items()
                if q in rid.lower()
                or q in d["name"].lower()
                or q in d["region"].lower()
                or q in (d["description"] or "").lower()
            }
        else:
            matches = self._registry

        groups: dict = {}
        for rid, d in matches.items():
            groups.setdefault(d["region"], []).append((rid, d))
        for reg in groups:
            groups[reg].sort(key=lambda x: x[1]["name"].lower())

        flat = []
        for region_name in REGION_ORDER:
            room_items = groups.get(region_name)
            if not room_items:
                continue
            flat.append((region_name, None, f"{region_name}  ({len(room_items)})"))
            for rid, d in room_items:
                loc  = d["loc_type"]
                tag  = f"[{loc[:3].upper()}]" if loc else "[   ]"
                boat = any(isinstance(v, dict) and v.get("type") == "boat_travel"
                           for v in d["exits"].values())
                flat.append((None, rid, f"  {tag}  {d['name']}" + (" ⛵" if boat else "")))

        self._flat   = flat
        self._scroll = 0
        if self._sel_idx >= len(flat):
            self._sel_idx = -1

    # ── Update ─────────────────────────────────────────────────────────────────

    def update(self, dt=0.016):
        if self._closing:
            self._anim = max(0.0, self._anim - dt / self.CLOSE_DUR)
            if self._anim <= 0.0:
                self._alive = False
            return
        self._anim  = min(1.0, self._anim  + dt / self.OPEN_DUR)
        self._cfade = min(1.0, self._cfade + dt / self.CONTENT_DUR)

    # ── Events ─────────────────────────────────────────────────────────────────

    def handle_event(self, event) -> bool:
        if not self._alive or self._closing:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.close(); return True
            if self._search_active:
                if event.key == pygame.K_BACKSPACE:
                    self._search_text = self._search_text[:-1]
                    self._apply_filter(self._search_text)
                    return True
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    self._search_active = False; return True
                elif event.unicode and event.unicode.isprintable():
                    self._search_text += event.unicode
                    self._apply_filter(self._search_text)
                    return True
            if event.key == pygame.K_UP:
                self._move_sel(-1); return True
            if event.key == pygame.K_DOWN:
                self._move_sel(1); return True

        if event.type == pygame.MOUSEWHEEL:
            self._scroll = max(0, self._scroll - event.y)
            return True

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            if self._close_rect.collidepoint(pos):
                self.close(); return True
            if self._search_rect.collidepoint(pos):
                self._search_active = True; return True
            else:
                self._search_active = False
            for rect, fidx in self._row_rects:
                if rect.collidepoint(pos):
                    _, rid, _ = self._flat[fidx]
                    if rid is not None:
                        self._sel_idx = fidx
                    return True
            if not self._book_rect.collidepoint(pos):
                self.close()
            return True

        return False

    def _move_sel(self, delta):
        ri_list = [i for i, (_, rid, _) in enumerate(self._flat) if rid is not None]
        if not ri_list:
            return
        if self._sel_idx < 0 or self._sel_idx not in ri_list:
            self._sel_idx = ri_list[0] if delta > 0 else ri_list[-1]
        else:
            ci = ri_list.index(self._sel_idx)
            ci = max(0, min(len(ri_list) - 1, ci + delta))
            self._sel_idx = ri_list[ci]
        if self._sel_idx < self._scroll:
            self._scroll = self._sel_idx
        elif self._rows_visible and self._sel_idx >= self._scroll + self._rows_visible:
            self._scroll = self._sel_idx - self._rows_visible + 1

    # ── Draw ───────────────────────────────────────────────────────────────────

    def draw(self, surface):
        if not self._alive:
            return
        scale = _ease_out_cubic(self._anim)
        if scale < 0.02:
            return

        sw, sh = surface.get_size()
        BW = min(860, sw - 40)
        BH = min(590, sh - 40)

        bg_s = pygame.Surface((sw, sh), pygame.SRCALPHA)
        bg_s.fill((0, 0, 0, int(165 * scale)))
        surface.blit(bg_s, (0, 0))

        if scale < 0.995:
            sbw = max(2, int(BW * scale))
            sbh = max(2, int(BH * scale))
            self._sf    = sbw / BW
            self._dst_x = (sw - sbw) // 2
            self._dst_y = (sh - sbh) // 2
        else:
            sbw = sbh = 0
            self._sf    = 1.0
            self._dst_x = (sw - BW) // 2
            self._dst_y = (sh - BH) // 2

        book_surf = pygame.Surface((BW, BH), pygame.SRCALPHA)
        self._draw_book(book_surf, BW, BH)

        if scale < 0.995:
            scaled = pygame.transform.smoothscale(book_surf, (sbw, sbh))
            surface.blit(scaled, (self._dst_x, self._dst_y))
        else:
            surface.blit(book_surf, (self._dst_x, self._dst_y))

        def _tr(r):
            return pygame.Rect(int(self._dst_x + r.x * self._sf),
                               int(self._dst_y + r.y * self._sf),
                               max(1, int(r.width  * self._sf)),
                               max(1, int(r.height * self._sf)))

        self._book_rect   = pygame.Rect(self._dst_x, self._dst_y,
                                         int(BW * self._sf), int(BH * self._sf))
        self._close_rect  = _tr(self._close_rect)
        self._search_rect = _tr(self._search_rect)
        self._row_rects   = [(_tr(r), fi) for r, fi in self._row_rects]

    # ── Core book draw ─────────────────────────────────────────────────────────

    def _draw_book(self, surf, BW, BH):
        MID = BW // 2
        cf  = self._cfade

        sh_s = pygame.Surface((BW + 28, BH + 28), pygame.SRCALPHA)
        pygame.draw.rect(sh_s, (0, 0, 0, 85), pygame.Rect(16, 16, BW, BH), border_radius=10)
        surf.blit(sh_s, (-14, -14))

        pygame.draw.rect(surf, C_PARCHMENT,   pygame.Rect(0,       0, BW // 2 + 3, BH), border_radius=8)
        pygame.draw.rect(surf, C_PARCHMENT_L, pygame.Rect(MID - 2, 0, BW // 2 + 2, BH), border_radius=8)

        rng = random.Random(self._SPOTS_SEED)
        spot_s = pygame.Surface((BW, BH), pygame.SRCALPHA)
        for _ in range(130):
            pygame.draw.circle(spot_s, (90, 60, 22, rng.randint(10, 30)),
                               (rng.randint(6, BW - 6), rng.randint(6, BH - 6)),
                               rng.randint(2, 7))
        surf.blit(spot_s, (0, 0))

        pygame.draw.rect(surf, C_LEATHER, pygame.Rect(MID - 11, 0, 22, BH))
        pygame.draw.rect(surf, C_COVER,   pygame.Rect(MID - 4,  0,  4, BH))
        for i in range(1, 7):
            ly = int(BH * i / 7)
            pygame.draw.rect(surf, C_SPINE_LINE, pygame.Rect(MID - 11, ly - 2, 22, 4), border_radius=1)

        pygame.draw.rect(surf, C_COVER, pygame.Rect(0, 0, BW, BH), width=3, border_radius=8)

        pad = 16
        lf = pygame.Rect(pad,      pad, BW // 2 - pad - 14, BH - pad * 2)
        rf = pygame.Rect(MID + 14, pad, BW // 2 - pad - 14, BH - pad * 2)
        pygame.draw.rect(surf, C_INK_LIGHT, lf, width=1)
        pygame.draw.rect(surf, C_INK_LIGHT, rf, width=1)

        self._draw_left_page(surf, lf, cf)
        self._draw_right_page(surf, rf, cf, 0, 0)

        fade_a = int(255 * (1.0 - cf))
        if fade_a > 4:
            for rect, base in ((lf, C_PARCHMENT), (rf, C_PARCHMENT_L)):
                fs = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
                fs.fill((*base, fade_a))
                surf.blit(fs, (rect.x, rect.y))

        cbr = pygame.Rect(BW - 34, 6, 26, 26)
        sf = self._sf if self._sf else 1.0
        mx_r, my_r = pygame.mouse.get_pos()
        mx_l = (mx_r - self._dst_x) / sf
        my_l = (my_r - self._dst_y) / sf
        c_col = (190, 80, 60) if cbr.collidepoint(mx_l, my_l) else (148, 56, 40)
        pygame.draw.rect(surf, c_col, cbr, border_radius=5)
        _xs = self._f(13, bold=True).render("✕", True, (255, 238, 228))
        surf.blit(_xs, _xs.get_rect(center=cbr.center))
        self._close_rect = cbr  # book-local; translated to screen in draw()

    # ── Left page ──────────────────────────────────────────────────────────────

    def _draw_left_page(self, surf, frame, cf):
        ink   = _blend(C_INK,       C_PARCHMENT, cf)
        mid   = _blend(C_INK_MID,   C_PARCHMENT, cf)
        head  = _blend(C_HEADER,    C_PARCHMENT, cf)
        light = _blend(C_INK_LIGHT, C_PARCHMENT, cf)
        div   = _blend(C_DIVIDER,   C_PARCHMENT, cf)

        surf.blit(self._f(17, bold=True).render("Room Browser", True, head),
                  (frame.x + 6, frame.y + 3))
        pygame.draw.line(surf, div, (frame.x + 4, frame.y + 25),
                         (frame.x + frame.width - 4, frame.y + 25), 1)

        # Search bar
        sb_y = frame.y + 31
        sbr  = pygame.Rect(frame.x + 2, sb_y, frame.width - 4, 22)
        self._search_rect = sbr  # book-local; translated to screen in draw()
        pygame.draw.rect(surf, _blend(C_SEARCH_BG,     C_PARCHMENT, cf), sbr, border_radius=3)
        pygame.draw.rect(surf, _blend(C_SEARCH_BORDER, C_PARCHMENT, cf), sbr, width=1, border_radius=3)
        disp  = self._search_text[-28:] if self._search_text else "Search rooms…"
        t_col = ink if self._search_text else light
        ss    = self._f(10).render(disp, True, t_col)
        surf.blit(ss, (sbr.x + 5, sbr.y + 4))
        if self._search_active and int(pygame.time.get_ticks() / 530) % 2 == 0:
            pygame.draw.line(surf, ink,
                             (sbr.x + 5 + ss.get_width() + 1, sbr.y + 4),
                             (sbr.x + 5 + ss.get_width() + 1, sbr.y + 18), 1)
        pygame.draw.line(surf, div, (frame.x + 4, sb_y + 26),
                         (frame.x + frame.width - 4, sb_y + 26), 1)

        list_top = sb_y + 30
        row_h    = 20
        avail_h  = frame.bottom - list_top - 18
        self._rows_visible = max(1, avail_h // row_h)

        max_scroll = max(0, len(self._flat) - self._rows_visible)
        self._scroll = max(0, min(self._scroll, max_scroll))

        self._row_rects = []
        y = list_top
        sf = self._sf if self._sf else 1.0
        mx_s = int((pygame.mouse.get_pos()[0] - self._dst_x) / sf)
        my_s = int((pygame.mouse.get_pos()[1] - self._dst_y) / sf)

        for fi in range(self._scroll, min(self._scroll + self._rows_visible, len(self._flat))):
            region, rid, label = self._flat[fi]
            abs_r = pygame.Rect(frame.x, y, frame.width, row_h)  # book-local

            if rid is None:
                reg_col = _blend(REGION_COLORS.get(region, (90, 90, 90)), C_PARCHMENT, cf)
                surf.blit(self._f(9, bold=True).render(label, True, reg_col),
                          (frame.x + 4, y + 2))
                pygame.draw.line(surf, _blend(C_DIVIDER, C_PARCHMENT, cf * 0.6),
                                 (frame.x + 4, y + row_h - 1),
                                 (frame.x + frame.width - 4, y + row_h - 1), 1)
            else:
                self._row_rects.append((abs_r, fi))
                is_sel = (fi == self._sel_idx)
                is_hov = abs_r.collidepoint(mx_s, my_s)
                if is_sel:
                    hs = pygame.Surface((frame.width, row_h), pygame.SRCALPHA)
                    hs.fill((*C_SELECT_BG, int(175 * cf)))
                    surf.blit(hs, (frame.x, y))
                elif is_hov:
                    hs = pygame.Surface((frame.width, row_h), pygame.SRCALPHA)
                    hs.fill((*C_SELECT_BG, int(70 * cf)))
                    surf.blit(hs, (frame.x, y))
                surf.blit(self._f(10, bold=is_sel).render(label[:38], True,
                                                           ink if is_sel else mid),
                          (frame.x + 6, y + 4))
            y += row_h

        # Scrollbar
        if len(self._flat) > self._rows_visible:
            th = max(14, int(avail_h * self._rows_visible / len(self._flat)))
            ty = list_top + int((avail_h - th) * self._scroll / max(1, max_scroll))
            pygame.draw.rect(surf, light,
                             pygame.Rect(frame.right - 5, list_top, 3, avail_h), border_radius=1)
            pygame.draw.rect(surf, _blend(C_INK_MID, C_PARCHMENT, cf),
                             pygame.Rect(frame.right - 5, ty, 3, th), border_radius=1)

        n = sum(1 for _, rid, _ in self._flat if rid is not None)
        surf.blit(self._f(10).render(f"{n} rooms  ·  Esc to close", True, light),
                  (frame.x + 4, frame.bottom - 14))

    # ── Right page ─────────────────────────────────────────────────────────────

    def _draw_right_page(self, surf, frame, cf, ox, oy):
        ink   = _blend(C_INK,       C_PARCHMENT_L, cf)
        mid   = _blend(C_INK_MID,   C_PARCHMENT_L, cf)
        head  = _blend(C_HEADER,    C_PARCHMENT_L, cf)
        light = _blend(C_INK_LIGHT, C_PARCHMENT_L, cf)
        div   = _blend(C_DIVIDER,   C_PARCHMENT_L, cf)

        if self._sel_idx < 0 or self._sel_idx >= len(self._flat):
            return self._draw_empty_right(surf, frame, head, mid, light, div)
        _, rid, _ = self._flat[self._sel_idx]
        if rid is None:
            return self._draw_empty_right(surf, frame, head, mid, light, div)
        d = self._registry.get(rid)
        if not d:
            return self._draw_empty_right(surf, frame, head, mid, light, div)

        # Room name
        surf.blit(self._f(16, bold=True).render(d["name"][:34], True, head),
                  (frame.x + 5, frame.y + 3))
        pygame.draw.line(surf, div, (frame.x + 4, frame.y + 25),
                         (frame.x + frame.width - 4, frame.y + 25), 1)

        y = frame.y + 30
        reg_col = _blend(REGION_COLORS.get(d["region"], (90, 90, 90)), C_PARCHMENT_L, cf)
        surf.blit(self._f(10, bold=True).render(d["region"], True, reg_col),
                  (frame.x + 6, y)); y += 16
        surf.blit(self._f(9).render(rid, True, light), (frame.x + 6, y)); y += 14

        # Type badge
        if d["loc_type"]:
            ts = self._f(9, bold=True).render(d["loc_type"].upper(), True,
                                               _blend((100, 70, 30), C_PARCHMENT_L, cf))
            tbg = pygame.Rect(frame.x + 4, y, ts.get_width() + 8, ts.get_height() + 4)
            pygame.draw.rect(surf, _blend((210, 190, 140), C_PARCHMENT_L, cf * 0.7), tbg, border_radius=3)
            pygame.draw.rect(surf, _blend(C_INK_LIGHT, C_PARCHMENT_L, cf), tbg, width=1, border_radius=3)
            surf.blit(ts, (frame.x + 8, y + 2))
            y += tbg.height + 6

        pygame.draw.line(surf, div, (frame.x + 4, y), (frame.x + frame.width - 4, y), 1); y += 6

        # Description
        desc = d.get("description", "")
        if desc:
            for line in _wrap_text(desc, self._f(10), frame.width - 12):
                surf.blit(self._f(10).render(line, True, mid), (frame.x + 6, y))
                y += 15
                if y > frame.y + 150:
                    break
            y += 4

        pygame.draw.line(surf, div, (frame.x + 4, y), (frame.x + frame.width - 4, y), 1); y += 6

        def _section(title, items_list, col, fmt=None):
            nonlocal y
            if not items_list or y > frame.bottom - 40:
                return
            surf.blit(self._f(11, bold=True).render(title, True, ink), (frame.x + 6, y)); y += 14
            for item in items_list:
                if y > frame.bottom - 20:
                    break
                txt = fmt(item) if fmt else str(item)
                surf.blit(self._f(10).render(txt[:44], True, col), (frame.x + 8, y)); y += 13
            y += 3

        # Exits
        exits = d.get("exits", {})
        if exits and y < frame.bottom - 50:
            surf.blit(self._f(11, bold=True).render("EXITS", True, ink), (frame.x + 6, y)); y += 14
            exit_col = _blend((70, 90, 130), C_PARCHMENT_L, cf)
            boat_col = _blend((55, 120, 100), C_PARCHMENT_L, cf)
            for ek, ev in exits.items():
                if y > frame.bottom - 20:
                    break
                if isinstance(ev, dict):
                    is_boat = ev.get("type") == "boat_travel"
                    target  = ev.get("display") or ev.get("target", "?")
                    txt_e   = f"{'⛵' if is_boat else '→'}  {ek}  →  {target}"
                    col_e   = boat_col if is_boat else exit_col
                else:
                    txt_e = f"→  {ek}  →  {ev}"
                    col_e = exit_col
                surf.blit(self._f(10).render(txt_e[:44], True, col_e), (frame.x + 8, y)); y += 13
            y += 3

        # Coordinates
        coords = d.get("coordinates")
        if coords and y < frame.bottom - 30:
            cx, cy2 = coords
            surf.blit(self._f(10).render(f"Coordinates: ({cx}, {cy2})", True, light),
                      (frame.x + 6, y)); y += 14

        # NPCs
        npcs = d.get("npcs") or []
        if npcs and y < frame.bottom - 40:
            _section("NPCS", npcs, _blend((140, 110, 40), C_PARCHMENT_L, cf))

        # Items
        items_d = d.get("items") or {}
        if items_d and y < frame.bottom - 40:
            if isinstance(items_d, dict):
                item_lines = []
                for iid, info in items_d.items():
                    qty = info.get("quantity", 1) if isinstance(info, dict) else ""
                    item_lines.append(f"{iid}" + (f" ×{qty}" if qty and qty != 1 else ""))
            elif isinstance(items_d, list):
                item_lines = [str(i) for i in items_d]
            else:
                item_lines = []
            _section("ITEMS", item_lines, _blend((70, 120, 60), C_PARCHMENT_L, cf))

    def _draw_empty_right(self, surf, frame, head, mid, light, div):
        surf.blit(self._f(16, bold=True).render("Room Browser", True, head),
                  (frame.x + 6, frame.y + 3))
        pygame.draw.line(surf, div, (frame.x + 4, frame.y + 25),
                         (frame.x + frame.width - 4, frame.y + 25), 1)
        y = frame.y + 38
        for line in ["", "Every room and area in the",
                     "world is catalogued here.",
                     "", "Search by name, region,",
                     "or description.", "",
                     "Click a room to read details.",
                     "", "", "— Esc to close —"]:
            surf.blit(self._f(12).render(line, True, light if line.startswith("—") else mid),
                      (frame.x + 8, y))
            y += 18


# Backward-compatibility alias
SearchableRoomsWindow = RoomsOverlay

