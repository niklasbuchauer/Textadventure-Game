# book_overlay.py  –  Parchment book overlay base + Inventory / Stats / Debug / Skills
#
# All four overlays share the same old-book visual style as JournalWindow.
# They are rendered directly onto the game surface (no pygame_gui widgets).
#
# Public interface (compatible with _sub_windows / journal_win conventions):
#   handle_event(event) -> bool
#   update(dt)
#   draw(surface)
#   is_open() -> bool
#   close()

import pygame
import math
import random

# ── Palette (matches journal_window.py) ──────────────────────────────────────
C_PARCHMENT   = (238, 220, 178)
C_PARCHMENT_L = (248, 234, 196)
C_INK         = ( 38,  22,   6)
C_INK_MID     = ( 80,  50,  18)
C_INK_LIGHT   = (130,  98,  50)
C_HEADER      = (128,  30,  20)
C_LEATHER     = ( 72,  38,  12)
C_COVER       = ( 88,  50,  18)
C_SPINE_LINE  = ( 52,  26,   8)
C_SELECT_BG   = (210, 180, 118)
C_DONE        = ( 52, 108,  48)
C_DIVIDER     = (175, 152, 108)
C_SEARCH_BG   = (225, 205, 158)
C_SEARCH_CUR  = (160,  60,  30)
C_GOLD        = (185, 140,  20)
C_BLUE        = ( 45,  80, 158)
C_RED         = (148,  35,  25)
C_GREEN       = ( 45, 110,  45)

# ── Helpers ───────────────────────────────────────────────────────────────────

def _ease_out(t):
    t = max(0.0, min(1.0, t))
    return 1.0 - (1.0 - t) ** 3

def _ease_io(t):
    t = max(0.0, min(1.0, t))
    return 4 * t**3 if t < 0.5 else 1.0 - (-2*t+2)**3 / 2

def _blend(col, bg, a):
    a = max(0.0, min(1.0, a))
    return tuple(int(c*a + b*(1-a)) for c, b in zip(col[:3], bg[:3]))

def _wrap(text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if font.size(test)[0] <= max_w:
            cur = test
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines or [text]

def _font(size, bold=False):
    for name in ("Palatino Linotype", "Book Antiqua", "Georgia",
                 "Times New Roman", "serif"):
        f = pygame.font.SysFont(name, size, bold=bold)
        if f: return f
    return pygame.font.Font(None, size)


# ═══════════════════════════════════════════════════════════════════════════
#  BASE BOOK OVERLAY
# ═══════════════════════════════════════════════════════════════════════════
class BookOverlay:
    OPEN_DUR    = 0.36
    CLOSE_DUR   = 0.24
    CONTENT_DUR = 0.28
    TURN_DUR    = 0.20
    _SPOT_SEED  = 4217

    def __init__(self, gui, title_left="", title_right="",
                 width=820, height=570):
        self.gui          = gui
        self.title_left   = title_left
        self.title_right  = title_right
        self._bw          = width
        self._bh          = height
        self._alive       = True
        self._closing     = False
        self._anim        = 0.0
        self._cfade       = 0.0
        self._turn_t      = 1.0
        self._fcache: dict = {}
        self._particles: list = []
        # click regions (absolute screen)
        self._book_rect   = pygame.Rect(0,0,1,1)
        self._close_rect  = pygame.Rect(0,0,1,1)

    # ── Public ───────────────────────────────────────────────────────────────

    def is_open(self): return self._alive
    def close(self):
        if not self._closing:
            self._closing = True

    def update(self, dt=0.016):
        if self._closing:
            self._anim = max(0.0, self._anim - dt / self.CLOSE_DUR)
            if self._anim <= 0.0: self._alive = False
            return
        self._anim  = min(1.0, self._anim  + dt / self.OPEN_DUR)
        self._cfade = min(1.0, self._cfade + dt / self.CONTENT_DUR)
        self._turn_t = min(1.0, self._turn_t + dt / self.TURN_DUR)
        self._tick_particles(dt)
        self._on_update(dt)

    def handle_event(self, event) -> bool:
        if not self._alive or self._closing:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.close(); return True
            return self._on_keydown(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._close_rect.collidepoint(event.pos):
                self.close(); return True
            if not self._book_rect.collidepoint(event.pos):
                self.close(); return True
            return self._on_click(event.pos)
        if event.type == pygame.MOUSEWHEEL:
            return self._on_scroll(event.y)
        return False

    def draw(self, surface: pygame.Surface):
        if not self._alive: return
        sc = _ease_out(self._anim)
        if sc < 0.02: return
        sw, sh = surface.get_size()
        BW = min(self._bw, sw - 40)
        BH = min(self._bh, sh - 40)
        bx = (sw - BW) // 2
        by = (sh - BH) // 2
        # backdrop
        bd = pygame.Surface((sw, sh), pygame.SRCALPHA)
        bd.fill((0, 0, 0, int(160 * sc)))
        surface.blit(bd, (0, 0))
        # scale effect
        if sc < 0.995:
            sbw, sbh = max(2,int(BW*sc)), max(2,int(BH*sc))
            bs = pygame.Surface((BW, BH), pygame.SRCALPHA)
            self._draw_book(bs, BW, BH, 0, 0)
            scaled = pygame.transform.smoothscale(bs, (sbw, sbh))
            sx, sy = (sw-sbw)//2, (sh-sbh)//2
            surface.blit(scaled, (sx, sy))
            self._book_rect  = pygame.Rect(sx, sy, sbw, sbh)
            sf = sbw/BW
            self._close_rect = pygame.Rect(int(sx+(BW-34)*sf), int(sy+6*sf),
                                           int(26*sf), int(26*sf))
        else:
            self._draw_book(surface, BW, BH, bx, by)
            self._book_rect  = pygame.Rect(bx, by, BW, BH)
            self._close_rect = pygame.Rect(bx+BW-34, by+6, 26, 26)
        # dust
        cx, cy = sw//2, by+20
        for p in self._particles:
            lf = 1.0 - p[4]/p[5]
            a  = int(185*lf*sc)
            r  = max(1,int(p[6]))
            ps = pygame.Surface((r*2+2,r*2+2), pygame.SRCALPHA)
            pygame.draw.circle(ps, (200,172,118,a), (r+1,r+1), r)
            surface.blit(ps, (int(cx+p[0])-r-1, int(cy+p[1])-r-1))

    # ── Internals ─────────────────────────────────────────────────────────────

    def _on_update(self, dt): pass
    def _on_keydown(self, event) -> bool: return False
    def _on_click(self, pos) -> bool: return False
    def _on_scroll(self, dy) -> bool: return False
    def _draw_left_page(self, surf, frame, cf): pass
    def _draw_right_page(self, surf, frame, cf): pass

    def _f(self, size, bold=False):
        k = (size, bold)
        if k not in self._fcache:
            self._fcache[k] = _font(size, bold)
        return self._fcache[k]

    def _tick_particles(self, dt):
        if random.random() < dt*3 and len(self._particles) < 18:
            self._particles.append([
                random.uniform(-22,22), random.uniform(-4,4),
                random.uniform(-10,10), random.uniform(-26,-10),
                0.0, random.uniform(1.6,3.4), random.uniform(1.0,2.2)])
        for p in self._particles:
            p[4]+=dt; p[0]+=p[2]*dt; p[1]+=p[3]*dt
        self._particles=[p for p in self._particles if p[4]<p[5]]

    def _start_turn(self):
        self._turn_t = 0.0
        self._cfade  = max(0.15, self._cfade - 0.25)

    def _draw_book(self, surf, BW, BH, ox, oy):
        MID = ox + BW//2
        cf  = self._cfade
        # shadow
        sh = pygame.Surface((BW+28,BH+28), pygame.SRCALPHA)
        pygame.draw.rect(sh,(0,0,0,80),pygame.Rect(16,16,BW,BH),border_radius=10)
        surf.blit(sh,(ox-14,oy-14))
        # pages
        pygame.draw.rect(surf, C_PARCHMENT,   pygame.Rect(ox,oy,BW//2+3,BH), border_radius=8)
        pygame.draw.rect(surf, C_PARCHMENT_L, pygame.Rect(MID-2,oy,BW//2+2,BH), border_radius=8)
        # age spots
        rng = random.Random(self._SPOT_SEED)
        sp = pygame.Surface((BW,BH), pygame.SRCALPHA)
        for _ in range(120):
            sx2=rng.randint(6,BW-6); sy2=rng.randint(6,BH-6)
            r2=rng.randint(2,6); a2=rng.randint(8,26)
            pygame.draw.circle(sp,(90,60,22,a2),(sx2,sy2),r2)
        surf.blit(sp,(ox,oy))
        # spine
        pygame.draw.rect(surf, C_LEATHER, pygame.Rect(MID-11,oy,22,BH))
        pygame.draw.rect(surf, C_COVER,   pygame.Rect(MID-4,oy,4,BH))
        for i in range(1,7):
            ly=oy+int(BH*i/7)
            pygame.draw.rect(surf,C_SPINE_LINE,pygame.Rect(MID-11,ly-2,22,4),border_radius=1)
        # outer border
        pygame.draw.rect(surf,C_COVER,pygame.Rect(ox,oy,BW,BH),width=3,border_radius=8)
        # inner frames
        pad=16
        lf=pygame.Rect(ox+pad,oy+pad,BW//2-pad-14,BH-pad*2)
        rf=pygame.Rect(MID+14,oy+pad,BW//2-pad-14,BH-pad*2)
        pygame.draw.rect(surf,C_INK_LIGHT,lf,width=1)
        pygame.draw.rect(surf,C_INK_LIGHT,rf,width=1)
        # page content
        self._draw_left_page(surf, lf, cf)
        self._draw_right_page(surf, rf, cf)
        # content fade-in
        fadea = int(255*(1.0-cf))
        if fadea>4:
            for rect,pg in ((lf,C_PARCHMENT),(rf,C_PARCHMENT_L)):
                fs=pygame.Surface((rect.width,rect.height),pygame.SRCALPHA)
                fs.fill((*pg,fadea))
                surf.blit(fs,(rect.x,rect.y))
        # page-turn shimmer
        if self._turn_t < 1.0:
            sa = int(90*math.sin(_ease_io(self._turn_t)*math.pi))
            if sa>2:
                ts=pygame.Surface((rf.width,rf.height),pygame.SRCALPHA)
                ts.fill((255,250,230,sa)); surf.blit(ts,(rf.x,rf.y))
        # ── close btn ──────────────────────────────────────────────────────
        cbr = pygame.Rect(ox+BW-34, oy+6, 26, 26)
        mx,my=pygame.mouse.get_pos()
        ch = (mx-ox, my-oy) if (ox,oy)!=(0,0) else (mx,my)
        cc = (190,80,60) if cbr.collidepoint(*ch) else (148,56,40)
        pygame.draw.rect(surf,cc,cbr,border_radius=5)
        cs=self._f(13,True).render("✕",True,(255,238,228))
        surf.blit(cs,cs.get_rect(center=cbr.center))

    # ── Shared page-drawing primitives ───────────────────────────────────────

    def _page_title(self, surf, frame, text, cf, left=True):
        bg = C_PARCHMENT if left else C_PARCHMENT_L
        h  = _blend(C_HEADER, bg, cf)
        d  = _blend(C_DIVIDER, bg, cf)
        s  = self._f(16,True).render(text, True, h)
        surf.blit(s,(frame.x+6, frame.y+5))
        x1,x2=frame.x+4, frame.x+frame.width-4
        pygame.draw.line(surf,d,(x1,frame.y+27),(x2,frame.y+27),1)
        # small diamond
        dm=(frame.x+frame.width//2, frame.y+27)
        pygame.draw.polygon(surf,d,[
            (dm[0],dm[1]-4),(dm[0]+4,dm[1]),
            (dm[0],dm[1]+4),(dm[0]-4,dm[1])])
        return frame.y+36

    def _row_divider(self, surf, frame, y, cf, left=True):
        bg = C_PARCHMENT if left else C_PARCHMENT_L
        d  = _blend(C_DIVIDER, bg, cf)
        pygame.draw.line(surf,d,(frame.x+4,y),(frame.x+frame.width-4,y),1)

    def _footer_hint(self, surf, frame, text, cf, left=True):
        bg = C_PARCHMENT if left else C_PARCHMENT_L
        l  = _blend(C_INK_LIGHT, bg, cf)
        s  = self._f(11).render(text, True, l)
        surf.blit(s,(frame.x+5, frame.bottom-18))
        self._row_divider(surf, frame, frame.bottom-26, cf, left)


# ═══════════════════════════════════════════════════════════════════════════
#  INVENTORY OVERLAY
# ═══════════════════════════════════════════════════════════════════════════
class InventoryOverlay(BookOverlay):

    def __init__(self, gui):
        super().__init__(gui, "Inventory", "Item Details", 820, 580)
        self._items: list = []      # [(name, qty, value_ea), …]
        self._sel   = 0
        self._scroll= 0
        self._search= ""
        self._cursor_blink = 0.0
        self._msg   = ""
        self._msg_t = 0.0
        self._refresh()

    def _refresh(self):
        self._items=[]
        try:
            if self.gui.engine and self.gui.engine.player:
                inv  = self.gui.engine.player.inventory or {}
                wmap = getattr(self.gui.engine,"item_worth",{}) or {}
                q = self._search.lower()
                for name in sorted(inv, key=str.lower):
                    if q and q not in name.lower(): continue
                    self._items.append((name, int(inv[name]),
                                        int(wmap.get(name,0))))
        except Exception:
            pass
        self._sel = max(0, min(self._sel, len(self._items)-1))

    def _on_update(self, dt):
        self._cursor_blink = (self._cursor_blink+dt) % 1.2
        if self._msg_t>0: self._msg_t=max(0.0,self._msg_t-dt)

    def _on_keydown(self, ev) -> bool:
        k = ev.key
        if k == pygame.K_UP:    self._move(-1); return True
        if k == pygame.K_DOWN:  self._move( 1); return True
        if k == pygame.K_e:     self._examine(); return True
        if k == pygame.K_d:     self._drop(); return True
        if k == pygame.K_r:     self._refresh(); return True
        if k == pygame.K_BACKSPACE:
            self._search=self._search[:-1]; self._refresh(); return True
        if ev.unicode and ev.unicode.isprintable():
            self._search+=ev.unicode; self._refresh(); return True
        return False

    def _on_click(self, pos) -> bool:
        for r, i in self._row_hits:
            if r.collidepoint(pos):
                if self._sel!=i: self._start_turn()
                self._sel=i; return True
        for r, act in self._btn_hits:
            if r.collidepoint(pos):
                if act=="examine": self._examine()
                elif act=="drop": self._drop()
                return True
        return False

    def _on_scroll(self, dy) -> bool:
        self._move(-dy); return True

    def _move(self, delta):
        n = len(self._items)
        if n==0: return
        new=max(0,min(n-1,self._sel+delta))
        if new!=self._sel: self._start_turn()
        self._sel=new
        # scroll window
        vis=12
        if self._sel<self._scroll: self._scroll=self._sel
        if self._sel>=self._scroll+vis: self._scroll=self._sel-vis+1

    def _examine(self):
        if not self._items: return
        name=self._items[self._sel][0]
        try:
            r=self.gui.engine.process_command(f"examine {name}")
            if r: self.gui.append(r)
            self._msg=f"Examined: {name}"; self._msg_t=2.5
        except Exception as e:
            self._msg=str(e); self._msg_t=2.0

    def _drop(self):
        if not self._items: return
        name=self._items[self._sel][0]
        try:
            r=self.gui.engine.process_command(f"drop {name}")
            if r: self.gui.append(r)
            self._msg=f"Dropped: {name}"; self._msg_t=2.5
        except Exception:
            pass
        self._refresh()

    def _draw_left_page(self, surf, frame, cf):
        bg=C_PARCHMENT
        ink=_blend(C_INK,bg,cf); mid=_blend(C_INK_MID,bg,cf)
        light=_blend(C_INK_LIGHT,bg,cf); div=_blend(C_DIVIDER,bg,cf)
        sel=_blend(C_SELECT_BG,bg,cf); head=_blend(C_HEADER,bg,cf)
        gold=_blend(C_GOLD,bg,cf)
        y=self._page_title(surf,frame,self.title_left,cf,True)
        # search bar
        sb=pygame.Rect(frame.x+4,y,frame.width-8,22)
        pygame.draw.rect(surf,_blend(C_SEARCH_BG,bg,cf),sb,border_radius=3)
        pygame.draw.rect(surf,div,sb,width=1,border_radius=3)
        disp=self._search if self._search else ""
        cursor=""
        if self._cursor_blink<0.6: cursor="|"
        st=self._f(11).render(f"Search: {disp}{cursor}",True,ink)
        surf.blit(st,(sb.x+4,sb.y+4))
        y+=28
        # column headers
        hs=self._f(10,True).render("Item",True,light)
        surf.blit(hs,(frame.x+4,y))
        hs2=self._f(10,True).render("Qty  Value",True,light)
        surf.blit(hs2,(frame.x+frame.width-70,y))
        y+=14
        pygame.draw.line(surf,div,(frame.x+4,y),(frame.x+frame.width-4,y),1)
        y+=3
        # item rows
        self._row_hits=[]
        vis=12
        mx,my=pygame.mouse.get_pos()
        for i in range(self._scroll, min(self._scroll+vis, len(self._items))):
            name,qty,val=self._items[i]
            rh=22
            row=pygame.Rect(frame.x,y,frame.width,rh)
            # absolute hit rect
            self._row_hits.append((row,i))
            is_sel=(i==self._sel)
            is_hov=row.collidepoint(mx,my)
            if is_sel:
                hs3=pygame.Surface((frame.width,rh),pygame.SRCALPHA)
                hs3.fill((*_blend(C_SELECT_BG,bg,cf),int(180*cf)))
                surf.blit(hs3,(frame.x,y))
            elif is_hov:
                hs3=pygame.Surface((frame.width,rh),pygame.SRCALPHA)
                hs3.fill((*_blend(C_SELECT_BG,bg,cf),int(80*cf)))
                surf.blit(hs3,(frame.x,y))
            ns=self._f(12,is_sel).render(name[:26],True,ink if is_sel else mid)
            surf.blit(ns,(frame.x+6,y+3))
            total=val*qty
            vs=self._f(10).render(f"×{qty}  {total}g",True,gold if is_sel else light)
            surf.blit(vs,(frame.x+frame.width-vs.get_width()-6,y+4))
            y+=rh
            if i<len(self._items)-1:
                pygame.draw.line(surf,div,(frame.x+4,y-1),(frame.x+frame.width-4,y-1),1)
        # scroll hint
        if len(self._items)>vis:
            below=len(self._items)-self._scroll-vis
            ht=""
            if self._scroll>0 and below>0: ht=f"↑ {self._scroll} more  ↓ {below} more"
            elif self._scroll>0: ht=f"↑ {self._scroll} more above"
            else: ht=f"↓ {below} more below"
            ss=self._f(10).render(ht,True,light)
            surf.blit(ss,(frame.x+4,frame.bottom-30))
        # buttons
        self._btn_hits=[]
        bw,bh2=78,22
        by2=frame.bottom-22
        for lbl,act,col in [("E - Examine","examine",(60,95,48)),
                             ("D - Drop","drop",(120,45,35))]:
            bx2=frame.x+4 if act=="examine" else frame.x+4+bw+6
            br=pygame.Rect(bx2,by2,bw,bh2)
            self._btn_hits.append((br,act))
            hov=br.collidepoint(mx,my)
            dc=tuple(min(255,c+30) for c in col) if hov else col
            pygame.draw.rect(surf,_blend(dc,bg,cf),br,border_radius=4)
            bs=self._f(11).render(lbl,True,_blend((245,235,210),bg,cf))
            surf.blit(bs,bs.get_rect(center=br.center))
        # count
        cs=self._f(10).render(f"{len(self._items)} items  R=refresh",True,light)
        surf.blit(cs,(frame.x+4,frame.bottom-42))

    def _draw_right_page(self, surf, frame, cf):
        bg=C_PARCHMENT_L
        ink=_blend(C_INK,bg,cf); mid=_blend(C_INK_MID,bg,cf)
        light=_blend(C_INK_LIGHT,bg,cf); div=_blend(C_DIVIDER,bg,cf)
        head=_blend(C_HEADER,bg,cf); gold=_blend(C_GOLD,bg,cf)
        if not self._items:
            y=self._page_title(surf,frame,"No Items",cf,False)
            s=self._f(12).render("Your inventory is empty.",True,mid)
            surf.blit(s,(frame.x+8,y+8))
            return
        name,qty,val=self._items[self._sel]
        y=self._page_title(surf,frame,name[:20],cf,False)
        # separator
        pygame.draw.line(surf,div,(frame.x+4,y),(frame.x+frame.width-4,y),1)
        y+=8
        # stats block
        for label, value, col in [
            ("Quantity",     f"×{qty}",    ink),
            ("Value (each)", f"{val} gold", gold),
            ("Total worth",  f"{val*qty} gold", gold),
        ]:
            ls=self._f(12,True).render(label+":", True, _blend(C_HEADER,bg,cf*0.9))
            surf.blit(ls,(frame.x+8,y))
            vs=self._f(14).render(value,True,col)
            surf.blit(vs,(frame.x+frame.width//2,y-1))
            y+=22
        y+=4
        pygame.draw.line(surf,div,(frame.x+4,y),(frame.x+frame.width-4,y),1)
        y+=8
        # try to get examine text
        try:
            desc=None
            if self.gui.engine:
                items_db=getattr(self.gui.engine,"items",{}) or {}
                idata=items_db.get(name,{})
                desc=idata.get("description","") or idata.get("desc","")
            if desc:
                ds=self._f(12,True).render("Description:",True,_blend(C_HEADER,bg,cf*0.9))
                surf.blit(ds,(frame.x+8,y)); y+=20
                for line in _wrap(desc,self._f(12),frame.width-18):
                    s=self._f(12).render(line,True,mid)
                    surf.blit(s,(frame.x+8,y)); y+=17
                    if y>frame.bottom-50: break
        except Exception:
            pass
        # status message
        if self._msg and self._msg_t>0:
            pygame.draw.line(surf,div,(frame.x+4,frame.bottom-36),(frame.x+frame.width-4,frame.bottom-36),1)
            ms=self._f(11).render(self._msg,True,_blend(C_GREEN,bg,cf))
            surf.blit(ms,(frame.x+5,frame.bottom-26))
        else:
            self._footer_hint(surf,frame,"↑↓ navigate  E examine  D drop",cf,False)


# ═══════════════════════════════════════════════════════════════════════════
#  STATS OVERLAY
# ═══════════════════════════════════════════════════════════════════════════
class StatsOverlay(BookOverlay):

    def __init__(self, gui):
        super().__init__(gui, "Character", "Attributes", 780, 560)

    def _on_keydown(self, ev):
        if ev.key==pygame.K_r: self._start_turn(); return True
        return False

    def _on_click(self, pos):
        if hasattr(self,"_refresh_rect") and self._refresh_rect.collidepoint(pos):
            self._start_turn(); return True
        return False

    def _draw_left_page(self, surf, frame, cf):
        bg=C_PARCHMENT
        ink=_blend(C_INK,bg,cf); mid=_blend(C_INK_MID,bg,cf)
        light=_blend(C_INK_LIGHT,bg,cf); div=_blend(C_DIVIDER,bg,cf)
        head=_blend(C_HEADER,bg,cf); gold=_blend(C_GOLD,bg,cf)

        y=self._page_title(surf,frame,self.title_left,cf,True)
        if not (self.gui.engine and self.gui.engine.player):
            surf.blit(self._f(12).render("No player data.",True,mid),(frame.x+8,y+8))
            return
        stats=self.gui.engine.player.stats or {}
        try:
            from progression_system import XP_TABLE, MAX_LEVEL
            has_prog=True
        except Exception:
            has_prog=False

        cls=stats.get("class","none")
        lv=stats.get("level",1)
        xp=stats.get("xp",0)
        sp=stats.get("skill_points",0)
        hp=stats.get("health",100)
        gld=stats.get("gold",0)

        # class badge
        if cls!="none":
            badge_bg=_blend((100,28,18),bg,cf*0.85)
            br=pygame.Rect(frame.x+4,y,frame.width-8,26)
            pygame.draw.rect(surf,badge_bg,br,border_radius=5)
            cs_t=cls.upper()
            cs_s=self._f(14,True).render(cs_t,True,_blend((255,230,180),bg,cf))
            surf.blit(cs_s,cs_s.get_rect(center=br.center))
        y+=34

        # Level + XP bar
        ls=self._f(13,True).render(f"Level  {lv}",True,ink)
        surf.blit(ls,(frame.x+6,y)); y+=20
        if has_prog:
            try:
                xp_prev=XP_TABLE[lv-1] if lv>1 else 0
                xp_next=XP_TABLE[lv] if lv<MAX_LEVEL else xp
                prog=xp-xp_prev; total=max(1,xp_next-xp_prev)
                pct=min(1.0,prog/total)
                xp_str=f"{xp}/{xp_next}" if lv<MAX_LEVEL else f"{xp} (MAX)"
            except Exception:
                pct=0.0; xp_str=str(xp)
            bar_w=frame.width-16
            bar_r=pygame.Rect(frame.x+4,y,bar_w,11)
            pygame.draw.rect(surf,_blend((195,175,130),bg,cf),bar_r,border_radius=5)
            if pct>0:
                fill=pygame.Rect(frame.x+4,y,max(1,int(bar_w*pct)),11)
                pygame.draw.rect(surf,_blend((148,46,30),bg,cf),fill,border_radius=5)
            pygame.draw.rect(surf,div,bar_r,width=1,border_radius=5)
            pygame.draw.line(surf,div,(frame.x+4,y+14),(frame.x+frame.width-4,y+14),1)
            xs=self._f(10).render(f"XP: {xp_str}",True,light)
            surf.blit(xs,(frame.x+5,y+16)); y+=32
        else:
            y+=4

        # Vitals
        pygame.draw.line(surf,div,(frame.x+4,y),(frame.x+frame.width-4,y),1); y+=4
        for label, val, col in [
            ("Health",   str(hp),   _blend(C_GREEN,bg,cf)),
            ("Gold",     f"{gld}g", gold),
            ("Skill Pts",str(sp),   _blend(C_BLUE,bg,cf)),
        ]:
            ls2=self._f(12,True).render(label,True,head)
            surf.blit(ls2,(frame.x+8,y))
            vs=self._f(13).render(val,True,col)
            surf.blit(vs,(frame.x+frame.width-vs.get_width()-8,y)); y+=22

        self._footer_hint(surf,frame,"R = refresh",cf,True)

    def _draw_right_page(self, surf, frame, cf):
        bg=C_PARCHMENT_L
        ink=_blend(C_INK,bg,cf); mid=_blend(C_INK_MID,bg,cf)
        light=_blend(C_INK_LIGHT,bg,cf); div=_blend(C_DIVIDER,bg,cf)
        head=_blend(C_HEADER,bg,cf); gold=_blend(C_GOLD,bg,cf)

        y=self._page_title(surf,frame,self.title_right,cf,False)

        if not (self.gui.engine and self.gui.engine.player):
            surf.blit(self._f(12).render("No data.",True,mid),(frame.x+8,y+8))
            return
        stats=self.gui.engine.player.stats or {}
        # RPG attributes
        ATTRS=[
            ("strength",    "⚔  Strength",   C_RED),
            ("defense",     "🛡  Defense",    C_BLUE),
            ("dexterity",   "🏃  Dexterity",  C_GREEN),
            ("perception",  "👁  Perception", C_INK_MID),
            ("charisma",    "💬  Charisma",   (130,80,150)),
            ("constitution","💪  Constitution",C_INK),
        ]
        drawn=False
        for key,label,col in ATTRS:
            v=stats.get(key,0)
            if v<=0: continue
            drawn=True
            # bar style
            max_v=30
            pct=min(1.0,v/max_v)
            bw2=frame.width-16
            bar_r=pygame.Rect(frame.x+4,y,bw2,9)
            pygame.draw.rect(surf,_blend((195,175,130),bg,cf),bar_r,border_radius=4)
            if pct>0:
                fill=pygame.Rect(frame.x+4,y,max(1,int(bw2*pct)),9)
                pygame.draw.rect(surf,_blend(col,bg,cf),fill,border_radius=4)
            pygame.draw.rect(surf,div,bar_r,width=1,border_radius=4)
            ls2=self._f(12).render(label,True,_blend(col,bg,cf))
            surf.blit(ls2,(frame.x+8,y+12))
            vs=self._f(13,True).render(str(v),True,ink)
            surf.blit(vs,(frame.x+frame.width-vs.get_width()-8,y+10))
            y+=34
            if y>frame.bottom-50: break
        if not drawn:
            # fallback: show all stats
            for k in sorted(stats):
                s=self._f(11).render(f"{k}: {stats[k]}",True,mid)
                surf.blit(s,(frame.x+6,y)); y+=17
                if y>frame.bottom-50: break
        self._footer_hint(surf,frame,"Esc to close",cf,False)


# ═══════════════════════════════════════════════════════════════════════════
#  DEBUG OVERLAY
# ═══════════════════════════════════════════════════════════════════════════
class DebugOverlay(BookOverlay):
    """Two-spread debug book.
    Spread 0 (pages 1-2): player.state viewer
    Spread 1 (pages 3-4): toggleable debug flags + quick-action buttons
    """
    _FLIP_DUR = 0.32   # seconds for page-turn animation

    def __init__(self, gui):
        super().__init__(gui, "Debug Flags", "Game State", 780, 560)
        self._page          = 0          # 0 = state viewer, 1 = debug controls
        self._btn_hits: list = []        # [(abs_rect, action_str), ...]
        self._flip_t        = 1.0        # 1.0 = settled; 0→1 = animating
        self._flip_dir      = 0          # +1 forward, -1 backward
        self._flip_target   = 0          # page to switch to mid-flip
        self._flip_switched = False      # whether page swap happened this flip
        self._draw_ox       = 0          # ox from current _draw_book call
        self._draw_oy       = 0          # oy from current _draw_book call
        self._press_flash: dict = {}     # action -> remaining seconds (press feedback)

    # ── draw_book override (captures ox/oy for coord correction) ─────────────

    def _draw_book(self, surf, BW, BH, ox, oy):
        self._draw_ox = ox
        self._draw_oy = oy
        super()._draw_book(surf, BW, BH, ox, oy)

    # ── public ───────────────────────────────────────────────────────────────

    def _on_update(self, dt):
        if self._flip_t < 1.0:
            self._flip_t = min(1.0, self._flip_t + dt / self._FLIP_DUR)
            # Switch page mid-flip (at the fold peak)
            if not self._flip_switched and self._flip_t >= 0.5:
                self._page = self._flip_target
                self._flip_switched = True
                self._start_turn()
        # advance press-flash timers
        expired = [a for a, t in self._press_flash.items() if t <= 0]
        for a in expired:
            del self._press_flash[a]
        for a in list(self._press_flash):
            self._press_flash[a] -= dt

    def _on_keydown(self, ev):
        if ev.key == pygame.K_r:
            self._start_turn(); return True
        if ev.key in (pygame.K_RIGHT, pygame.K_TAB):
            self._flip_page(+1); return True
        if ev.key == pygame.K_LEFT:
            self._flip_page(-1); return True
        return False

    def _on_click(self, pos) -> bool:
        for rect, action in self._btn_hits:
            if rect.collidepoint(pos):
                self._dispatch(action)
                return True
        return True

    # ── page flip ────────────────────────────────────────────────────────────

    def _flip_page(self, delta):
        target = max(0, min(1, self._page + delta))
        if target == self._page or self._flip_t < 1.0:
            return
        self._flip_target   = target
        self._flip_dir      = delta
        self._flip_t        = 0.0
        self._flip_switched = False

    # ── draw override (adds animated page-fold on top) ────────────────────────

    def draw(self, surface: pygame.Surface):
        super().draw(surface)
        if self._flip_t >= 1.0 or self._anim < 0.02:
            return
        sc   = _ease_out(self._anim)
        sw, sh = surface.get_size()
        bw   = min(self._bw, sw - 40)
        bh   = min(self._bh, sh - 40)
        bx   = (sw - bw) // 2
        by   = (sh - bh) // 2

        # Ease-in/out progress for the fold sweep
        t    = _ease_io(self._flip_t)
        # fold_x: x position of the leading edge of the turning page
        # Forward (0→1): sweeps right→left; Backward (1→0): sweeps left→right
        if self._flip_dir > 0:
            fold_x  = bx + bw - int(t * bw)
            page_x  = fold_x
            page_w  = bx + bw - fold_x
        else:
            fold_x  = bx + int(t * bw)
            page_x  = bx
            page_w  = fold_x - bx

        if page_w <= 0:
            return

        # — turning page surface (parchment back/face)
        pg = pygame.Surface((page_w, bh), pygame.SRCALPHA)
        # pick: before midpoint show the page we're leaving, after show arriving
        col = C_PARCHMENT if (self._flip_dir > 0) == (self._flip_t < 0.5) else C_PARCHMENT_L
        pg.fill((*col, int(230 * sc)))
        # add subtle age spots so it looks like real parchment
        rng = random.Random(7777)
        for _ in range(35):
            sx2 = rng.randint(2, max(3, page_w - 2))
            sy2 = rng.randint(2, bh - 2)
            r2  = rng.randint(2, 4)
            a2  = rng.randint(5, 18)
            pygame.draw.circle(pg, (90, 60, 22, a2), (sx2, sy2), r2)
        surface.blit(pg, (page_x, by))

        # — fold highlight (bright strip at the crease edge)
        crease_w = max(4, min(16, page_w))
        crease_x = fold_x if self._flip_dir > 0 else (fold_x - crease_w)
        for i in range(crease_w):
            ratio = i / crease_w if self._flip_dir > 0 else (1 - i / crease_w)
            alpha = int(140 * (1 - ratio) * sc)
            if alpha > 2:
                pygame.draw.line(surface, (255, 248, 225, alpha),
                                 (crease_x + i, by), (crease_x + i, by + bh))

        # — drop shadow on the page behind the fold
        shad_w = min(18, page_w)
        shad_x = (fold_x - shad_w) if self._flip_dir > 0 else fold_x
        for i in range(shad_w):
            ratio = i / shad_w if self._flip_dir > 0 else (1 - i / shad_w)
            alpha = int(55 * ratio * sc)
            if alpha > 2:
                x = shad_x + i
                if bx <= x < bx + bw:
                    pygame.draw.line(surface, (0, 0, 0, alpha),
                                     (x, by), (x, by + bh))

    # ── action dispatch ───────────────────────────────────────────────────────

    def _dispatch(self, action: str):
        # page-flip actions don't need the engine
        if action == "flip_forward":
            self._flip_page(+1)
            return
        if action == "flip_back":
            self._flip_page(-1)
            return
        try:
            e = self.gui.engine
            p = e.player
        except Exception:
            return
        # record press flash (1 second)
        self._press_flash[action] = 1.0
        if action == "toggle_god_mode":
            e.debug_god_mode = not getattr(e, "debug_god_mode", False)
        elif action == "toggle_infinite_mana":
            new = not getattr(e, "debug_infinite_mana", False)
            e.debug_infinite_mana = new
            p.state["debug_infinite_mana"] = new
        elif action == "toggle_disarm_free":
            e.debug_disarm_free = not getattr(e, "debug_disarm_free", False)
        elif action == "toggle_map_reveal":
            new = not getattr(e, "debug_map_reveal", False)
            e.debug_map_reveal = new
            mw = getattr(e, "map_window", None)
            if mw and hasattr(mw, "reveal_all"):
                mw.reveal_all = new
        elif action == "heal_full":
            p.stats["health"] = p.state.get("health_max",
                                 p.stats.get("health_max", 100))
        elif action == "fill_mana":
            p.stats["mana"] = p.stats.get("mana_max",
                              p.state.get("mana_max", 50))
        elif action == "add_gold":
            p.stats["gold"] = p.stats.get("gold", 0) + 100
        elif action == "add_sp":
            p.stats["skill_points"] = p.stats.get("skill_points", 0) + 10
        elif action == "level_up":
            p.stats["level"] = p.stats.get("level", 1) + 1

    # ── routing ───────────────────────────────────────────────────────────────

    def _draw_left_page(self, surf, frame, cf):
        self._btn_hits = []
        if self._page == 0:
            self._draw_state_left(surf, frame, cf)
        else:
            self._draw_toggles(surf, frame, cf)

    def _draw_right_page(self, surf, frame, cf):
        if self._page == 0:
            self._draw_state_right(surf, frame, cf)
        else:
            self._draw_actions(surf, frame, cf)

    # ── spread 0: state viewer ────────────────────────────────────────────────

    def _get_state(self):
        try:
            s = self.gui.engine.player.state or {}
            return sorted(s.items())
        except Exception:
            return []

    def _draw_state_left(self, surf, frame, cf):
        bg  = C_PARCHMENT
        mid = _blend(C_INK_MID, bg, cf)
        y   = self._page_title(surf, frame, "Debug Flags", cf, True)
        items = self._get_state()
        half  = max(1, (len(items) + 1) // 2)
        for k, v in items[:half]:
            vc = _blend(C_GREEN, bg, cf) if v else _blend(C_RED, bg, cf)
            ks = self._f(10, True).render(str(k) + ":", True, mid)
            surf.blit(ks, (frame.x + 6, y))
            vs = self._f(10).render(str(v), True, vc)
            surf.blit(vs, (frame.x + 6 + ks.get_width() + 3, y))
            y += 16
            if y > frame.bottom - 44: break
        if not items:
            surf.blit(self._f(11).render("No flags set.", True,
                      _blend(C_INK_LIGHT, bg, cf)), (frame.x + 8, y + 8))
        # nav button + hint
        self._nav_btn(surf, frame, cf, "Controls \u25ba", "flip_forward",
                      left=True, right_aligned=True)
        self._footer_hint(surf, frame, "R = refresh  \u2192 = controls", cf, True)

    def _draw_state_right(self, surf, frame, cf):
        bg  = C_PARCHMENT_L
        mid = _blend(C_INK_MID, bg, cf)
        y   = self._page_title(surf, frame, "Game State", cf, False)
        items = self._get_state()
        half  = max(1, (len(items) + 1) // 2)
        right_items = items[half:]
        if right_items:
            for k, v in right_items:
                vc = _blend(C_GREEN, bg, cf) if v else _blend(C_RED, bg, cf)
                ks = self._f(10, True).render(str(k) + ":", True, mid)
                surf.blit(ks, (frame.x + 6, y))
                vs = self._f(10).render(str(v), True, vc)
                surf.blit(vs, (frame.x + 6 + ks.get_width() + 3, y))
                y += 16
                if y > frame.bottom - 44: break
        else:
            try:
                e = self.gui.engine
                for line in [f"Room: {e.player.current_room}",
                              f"Rooms loaded: {len(e.rooms)}",
                              f"Level: {e.player.stats.get('level', 1)}"]:
                    surf.blit(self._f(10).render(line, True, mid), (frame.x + 6, y))
                    y += 16
            except Exception:
                pass
        self._footer_hint(surf, frame, "Esc to close", cf, False)

    # ── spread 1: toggles ─────────────────────────────────────────────────────

    def _draw_toggles(self, surf, frame, cf):
        bg  = C_PARCHMENT
        y   = self._page_title(surf, frame, "Debug Toggles", cf, True) + 4
        try:
            e = self.gui.engine
        except Exception:
            e = None

        def _tval(attr):
            return bool(getattr(e, attr, False)) if e else False

        y = self._dbg_toggle(surf, frame, y, cf,
            "God Mode",        _tval("debug_god_mode"),      "toggle_god_mode")
        y = self._dbg_toggle(surf, frame, y, cf,
            "Infinite Mana",   _tval("debug_infinite_mana"), "toggle_infinite_mana")
        y = self._dbg_toggle(surf, frame, y, cf,
            "Free Trap Disarm",_tval("debug_disarm_free"),   "toggle_disarm_free")
        map_on = bool(getattr(e, "debug_map_reveal", False))
        y = self._dbg_toggle(surf, frame, y, cf,
            "Full Map Reveal",  map_on,                       "toggle_map_reveal")

        # small description labels
        descs = [
            "Cannot die (HP stuck at 1)",
            "Abilities cost no mana",
            "Traps cost no items",
            "Reveal all map rooms",
        ]
        y += 4
        lgt = _blend(C_INK_LIGHT, bg, cf)
        for d in descs:
            surf.blit(self._f(9).render("\u2014 " + d, True, lgt), (frame.x + 10, y))
            y += 14

        self._nav_btn(surf, frame, cf, "\u25c4 State View", "flip_back",
                      left=True, right_aligned=False)
        self._footer_hint(surf, frame, "\u2190 = state view", cf, True)

    # ── spread 1: actions ─────────────────────────────────────────────────────

    def _draw_actions(self, surf, frame, cf):
        y = self._page_title(surf, frame, "Quick Actions", cf, False) + 4

        y = self._dbg_btn(surf, frame, y, cf,
            "\u2665  Heal to Full",     "heal_full",
            (55, 110, 50), (80, 155, 75), right=True)
        y = self._dbg_btn(surf, frame, y, cf,
            "\u25c6  Fill Mana",         "fill_mana",
            (42, 70, 150), (65, 105, 200), right=True)
        y = self._dbg_btn(surf, frame, y, cf,
            "+100  Add Gold",            "add_gold",
            (120, 90, 20), (170, 135, 35), right=True)
        y = self._dbg_btn(surf, frame, y, cf,
            "+10  Skill Points",         "add_sp",
            (75, 42, 115), (108, 65, 160), right=True)
        y = self._dbg_btn(surf, frame, y, cf,
            "+1  Level Up",              "level_up",
            (100, 55, 20), (148, 88, 35), right=True)

        self._nav_btn(surf, frame, cf, "\u25c4 State View", "flip_back",
                      left=False, right_aligned=False)
        self._footer_hint(surf, frame, "Esc to close", cf, False)

    # ── button helpers ────────────────────────────────────────────────────────

    def _dbg_toggle(self, surf, frame, y, cf, label, value, action, right=False):
        """Render a labelled ON/OFF toggle row and register its hit rect."""
        bg    = C_PARCHMENT_L if right else C_PARCHMENT
        ink   = _blend(C_INK,     bg, cf)
        mid   = _blend(C_INK_MID, bg, cf)
        ROW_H = 26; BOX_W = 44; BOX_H = 18
        ls    = self._f(11).render(label, True, ink)
        surf.blit(ls, (frame.x + 8, y + (ROW_H - ls.get_height()) // 2))
        bx_   = frame.x + frame.width - BOX_W - 8
        bby   = y + (ROW_H - BOX_H) // 2
        br    = pygame.Rect(bx_, bby, BOX_W, BOX_H)
        mx, my = pygame.mouse.get_pos()
        _ox = self._book_rect.x - self._draw_ox
        _oy = self._book_rect.y - self._draw_oy
        hover  = br.collidepoint(mx - _ox, my - _oy)
        pressed = action in self._press_flash
        on_col = (52, 148, 68)   # green when on
        off_col = (120, 95, 60)  # warm grey when off
        fl = on_col if value else off_col
        if pressed:
            fl = tuple(max(0, c - 38) for c in fl)
        elif hover:
            fl = tuple(min(255, c + 25) for c in fl)
        pygame.draw.rect(surf, fl,  br, border_radius=9)
        pygame.draw.rect(surf, mid, br, width=1, border_radius=9)
        # knob
        kx = bx_ + BOX_W - BOX_H + 2 if value else bx_ + 2
        pygame.draw.circle(surf, (248, 238, 218), (kx + BOX_H // 2 - 2, bby + BOX_H // 2), BOX_H // 2 - 2)
        lbl2 = "ON " if value else "OFF"
        ts2  = self._f(8, True).render(lbl2, True, (20, 14, 6) if value else (100, 80, 50))
        loff = bx_ + 5 if value else bx_ + BOX_H - 2
        surf.blit(ts2, (loff, bby + (BOX_H - ts2.get_height()) // 2))
        # divider
        _blend_c = _blend(C_DIVIDER, bg, cf * 0.5)
        pygame.draw.line(surf, _blend_c,
                         (frame.x + 4, y + ROW_H), (frame.x + frame.width - 4, y + ROW_H), 1)
        self._btn_hits.append((
            pygame.Rect(self._book_rect.x - self._draw_ox + br.x,
                        self._book_rect.y - self._draw_oy + br.y,
                        br.width, br.height), action))
        return y + ROW_H + 3

    def _dbg_btn(self, surf, frame, y, cf, label, action,
                 normal_col, hover_col, right=False):
        """Render a full-width action button and register its hit rect."""
        bg    = C_PARCHMENT_L if right else C_PARCHMENT
        BTN_H = 30; BTN_W = frame.width - 12
        br    = pygame.Rect(frame.x + 6, y, BTN_W, BTN_H)
        mx, my = pygame.mouse.get_pos()
        _ox = self._book_rect.x - self._draw_ox
        _oy = self._book_rect.y - self._draw_oy
        hover  = br.collidepoint(mx - _ox, my - _oy)
        pressed = action in self._press_flash
        if pressed:
            col = tuple(max(0, c - 42) for c in normal_col)
        else:
            col = hover_col if hover else normal_col
        bs     = pygame.Surface((BTN_W, BTN_H), pygame.SRCALPHA)
        pygame.draw.rect(bs, (*col, 220), (0, 0, BTN_W, BTN_H), border_radius=6)
        pygame.draw.rect(bs, (220, 200, 140, 140), (0, 0, BTN_W, BTN_H), width=1, border_radius=6)
        surf.blit(bs, (br.x, br.y))
        ts = self._f(11, True).render(label, True, (245, 238, 218))
        surf.blit(ts, ts.get_rect(center=br.center))
        self._btn_hits.append((
            pygame.Rect(self._book_rect.x - self._draw_ox + br.x,
                        self._book_rect.y - self._draw_oy + br.y,
                        br.width, br.height), action))
        return y + BTN_H + 5

    def _nav_btn(self, surf, frame, cf, label, action, left=True, right_aligned=True):
        """Small navigation button pinned above the footer hint."""
        bg    = C_PARCHMENT_L if not left else C_PARCHMENT
        mid   = _blend(C_INK_MID, bg, cf)
        div   = _blend(C_DIVIDER, bg, cf)
        ts    = self._f(10, True).render(label, True, mid)
        BTN_W = ts.get_width() + 16; BTN_H = 18
        bx_   = (frame.x + frame.width - BTN_W - 4) if right_aligned else (frame.x + 4)
        by_   = frame.bottom - 46
        br    = pygame.Rect(bx_, by_, BTN_W, BTN_H)
        mx, my = pygame.mouse.get_pos()
        _ox = self._book_rect.x - self._draw_ox
        _oy = self._book_rect.y - self._draw_oy
        hover  = br.collidepoint(mx - _ox, my - _oy)
        pressed = action in self._press_flash
        c      = tuple(max(0, x - 28) for x in _blend(C_GOLD, bg, cf)[:3]) if pressed else \
                 (_blend(C_GOLD, bg, cf) if hover else div)
        pygame.draw.rect(surf, (*c[:3], 180), br, border_radius=4)
        pygame.draw.rect(surf, mid, br, width=1, border_radius=4)
        surf.blit(ts, ts.get_rect(center=br.center))
        self._btn_hits.append((
            pygame.Rect(self._book_rect.x - self._draw_ox + br.x,
                        self._book_rect.y - self._draw_oy + br.y,
                        br.width, br.height), action))


# ═══════════════════════════════════════════════════════════════════════════
#  SKILL TREE BOOK OVERLAY  –  radial constellation on parchment frame
# ═══════════════════════════════════════════════════════════════════════════
import math as _math


class SkillTreeBookOverlay(BookOverlay):
    """Radial skill-tree rendered on top of a parchment book frame."""

    _LEFT_W  = 210   # left info-panel width (px)
    _SPINE_W = 14    # decorative mini-spine between panels

    def __init__(self, gui):
        super().__init__(gui, "Skill Tree", "", 1050, 660)
        # ── tree viewport state ───────────────────────────────────────────
        self._positions: dict  = {}       # node_id -> (logical_x, logical_y)
        self._zoom             = 1.0
        self._cam_x            = 1500.0   # LCENTER default
        self._cam_y            = 1500.0
        self._drag_start       = None
        self._did_drag         = False
        self._pulse_phase      = 0
        self._pulse_timer      = 0.0
        self._selected_id      = None     # clicked node id
        self._hover_id         = None     # hovered node id
        self._spin_angle       = 0.0      # rotation for active-node deco
        self._click_flash: dict = {}      # nid -> remaining seconds
        # ── cached tree data ──────────────────────────────────────────────
        self._tree: list       = []
        self._cls_id: str      = "warrior"
        self._unlocked: set    = set()
        self._avail: set       = set()
        self._branches_data: dict = {}
        # ── tree font cache ───────────────────────────────────────────────
        self._tree_fonts: dict = {}
        # ── hit-testing rects (in draw-surface local coords) ─────────────
        self._tree_local_rect  = pygame.Rect(0, 0, 1, 1)
        self._tree_screen_rect = pygame.Rect(0, 0, 1, 1)
        self._refresh()

    # ── data refresh ─────────────────────────────────────────────────────────

    def _refresh(self):
        try:
            from skill_tree import (get_tree_for_class, get_unlocked_skills,
                                    get_available_skills, LCENTER, RING_GAP,
                                    CLASS_BRANCHES)
            if not (self.gui.engine and self.gui.engine.player):
                return
            p = self.gui.engine.player
            self._cls_id      = p.stats.get("class", "warrior")
            self._tree        = get_tree_for_class(self._cls_id)
            self._unlocked    = set(get_unlocked_skills(p))
            self._avail       = {n["id"] for n in get_available_skills(p)}
            self._branches_data = CLASS_BRANCHES.get(self._cls_id, {})
            self._compute_positions(LCENTER, RING_GAP)
        except Exception:
            pass

    # ── position computation (ported from SkillTreeWindow) ───────────────────

    def _compute_positions(self, LCENTER, RING_GAP):
        self._positions = {}
        if not self._tree:
            return
        # group by (branch, tier)
        groups: dict = {}
        for node in self._tree:
            key = (node.get("branch", "origin"), node["tier"])
            groups.setdefault(key, []).append(node["id"])
        for node in self._tree:
            branch = node.get("branch", "origin")
            tier   = node["tier"]
            if tier == 0:
                self._positions[node["id"]] = (float(LCENTER), float(LCENTER))
                continue
            bdef    = self._branches_data.get(branch, {})
            a_start = _math.radians(bdef.get("angle_start", 0))
            a_end   = _math.radians(bdef.get("angle_end",   30))
            radius  = tier * RING_GAP
            grp     = groups.get((branch, tier), [])
            n       = len(grp)
            for i, nid in enumerate(grp):
                if n == 1:
                    a = (a_start + a_end) / 2
                else:
                    pad = (a_end - a_start) * 0.08
                    a   = a_start + pad + (a_end - a_start - 2 * pad) * i / (n - 1)
                self._positions[nid] = (
                    LCENTER + radius * _math.cos(a),
                    LCENTER + radius * _math.sin(a),
                )

    # ── coordinate helpers ────────────────────────────────────────────────────

    def _l2s(self, lx, ly, sw, sh):
        return (
            (lx - self._cam_x) * self._zoom + sw / 2,
            (ly - self._cam_y) * self._zoom + sh / 2,
        )

    def _s2l(self, sx, sy, sw, sh):
        return (
            (sx - sw / 2) / self._zoom + self._cam_x,
            (sy - sh / 2) / self._zoom + self._cam_y,
        )

    # ── tree-specific font cache (pixel/sans) ─────────────────────────────────

    def _tf(self, size):
        if size not in self._tree_fonts:
            for name in ("Segoe UI", "Calibri", "Arial", "sans-serif"):
                f = pygame.font.SysFont(name, size)
                if f:
                    self._tree_fonts[size] = f
                    break
            else:
                self._tree_fonts[size] = pygame.font.Font(None, size)
        return self._tree_fonts[size]

    # ── update ────────────────────────────────────────────────────────────────

    def _on_update(self, dt):
        self._pulse_timer += dt
        if self._pulse_timer >= 0.15:
            self._pulse_timer -= 0.15
            self._pulse_phase += 1
        self._spin_angle = (self._spin_angle + dt * 0.55) % (2 * _math.pi)
        for nid in list(self._click_flash):
            self._click_flash[nid] -= dt
            if self._click_flash[nid] <= 0:
                del self._click_flash[nid]

    # ── events ────────────────────────────────────────────────────────────────

    def handle_event(self, event) -> bool:
        if not self._alive or self._closing:
            return False

        # MOUSEMOTION: pan (if dragging) or update hover
        if event.type == pygame.MOUSEMOTION:
            if self._drag_start is not None:
                dx = event.pos[0] - self._drag_start[0]
                dy = event.pos[1] - self._drag_start[1]
                if abs(dx) > 2 or abs(dy) > 2:
                    self._did_drag = True
                self._cam_x -= dx / self._zoom
                self._cam_y -= dy / self._zoom
                self._drag_start = event.pos
                return True
            # hover detection
            if self._tree_screen_rect.collidepoint(event.pos):
                try:
                    from skill_tree import NODE_R
                except ImportError:
                    NODE_R = 11
                tr   = self._tree_screen_rect
                sx   = event.pos[0] - tr.x
                sy   = event.pos[1] - tr.y
                lx, ly = self._s2l(sx, sy, tr.width, tr.height)
                thresh = NODE_R * 2.0 / self._zoom
                best_id, best_d = None, float("inf")
                for nid, (nlx, nly) in self._positions.items():
                    d = _math.hypot(lx - nlx, ly - nly)
                    if d < best_d and d < thresh:
                        best_d, best_id = d, nid
                self._hover_id = best_id
            else:
                self._hover_id = None
            return False

        # MOUSEBUTTONUP: end drag / fire click
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self._drag_start is not None:
                if not self._did_drag:
                    self._handle_tree_click(event.pos)
                self._drag_start = None
                self._did_drag   = False
                return True

        # MOUSEBUTTONDOWN: intercept close / outside / tree-drag / left-panel
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._close_rect.collidepoint(event.pos):
                self.close(); return True
            if not self._book_rect.collidepoint(event.pos):
                self.close(); return True
            if self._tree_screen_rect.collidepoint(event.pos):
                self._drag_start = event.pos
                self._did_drag   = False
                return True
            return self._on_click(event.pos)

        # KEYDOWN
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.close(); return True
            return self._on_keydown(event)

        # MOUSEWHEEL: zoom when over tree
        if event.type == pygame.MOUSEWHEEL:
            return self._on_scroll(event.y)

        return False

    def _on_keydown(self, ev) -> bool:
        if ev.key == pygame.K_r:
            self._refresh(); return True
        return False

    def _on_scroll(self, dy) -> bool:
        mx, my = pygame.mouse.get_pos()
        if self._tree_screen_rect.collidepoint(mx, my):
            self._zoom = max(0.2, min(3.5, self._zoom * (1.12 ** dy)))
            return True
        return False

    def _handle_tree_click(self, screen_pos):
        tr = self._tree_screen_rect
        sx = screen_pos[0] - tr.x
        sy = screen_pos[1] - tr.y
        lx, ly = self._s2l(sx, sy, tr.width, tr.height)

        try:
            from skill_tree import NODE_R
        except ImportError:
            NODE_R = 11

        best_id, best_d = None, float("inf")
        thresh = NODE_R * 2.2 / self._zoom
        for nid, (nlx, nly) in self._positions.items():
            d = _math.hypot(lx - nlx, ly - nly)
            if d < best_d and d < thresh:
                best_d = d
                best_id = nid

        self._selected_id = best_id
        if best_id:
            self._click_flash[best_id] = 0.45   # seconds to animate
        self._start_turn()

        if not best_id:
            return
        try:
            from skill_tree import unlock_skill
            p = self.gui.engine.player
            if best_id in self._avail and best_id not in self._unlocked:
                ok, msg = unlock_skill(p, best_id)
                self.gui.append(f"{'🌟' if ok else '⚠️'} {msg}")
                if ok:
                    self._refresh()
        except Exception as e:
            self.gui.append(f"[skill tree] {e}")

    # ── draw (override to also compute _tree_screen_rect) ────────────────────

    def draw(self, surface: pygame.Surface):
        super().draw(surface)
        if not self._alive:
            return
        sw = surface.get_width()
        BW = min(self._bw, sw - 40)
        if BW <= 0:
            return
        scale = self._book_rect.width / BW
        ltr   = self._tree_local_rect
        self._tree_screen_rect = pygame.Rect(
            int(self._book_rect.x + ltr.x * scale),
            int(self._book_rect.y + ltr.y * scale),
            int(ltr.width  * scale),
            int(ltr.height * scale),
        )

    # ── book drawing (full override: asymmetric layout) ───────────────────────

    def _draw_book(self, surf, BW, BH, ox, oy):
        LW  = min(self._LEFT_W, BW // 3)
        SPW = self._SPINE_W
        pad = 14
        cf  = self._cfade

        # shadow
        sh_s = pygame.Surface((BW + 28, BH + 28), pygame.SRCALPHA)
        pygame.draw.rect(sh_s, (0, 0, 0, 80), pygame.Rect(16, 16, BW, BH), border_radius=10)
        surf.blit(sh_s, (ox - 14, oy - 14))

        # dark cosmic left panel
        pygame.draw.rect(surf, (8, 10, 24), pygame.Rect(ox, oy, LW, BH), border_radius=8)
        _sp_rng = random.Random(self._SPOT_SEED + 1)
        for _ in range(30):
            _sx2 = _sp_rng.randint(4, LW - 4); _sy2 = _sp_rng.randint(4, BH - 4)
            _sa2 = _sp_rng.randint(15, 45)
            surf.set_at((ox + _sx2, oy + _sy2), (40 + _sa2, 50 + _sa2, 100 + _sa2))
        lf = pygame.Rect(ox + pad, oy + pad, LW - pad - SPW // 2, BH - pad * 2)
        pygame.draw.rect(surf, (25, 35, 70), lf, width=1)

        # decorative spine between panels
        sx_sp = ox + LW
        pygame.draw.rect(surf, C_LEATHER, pygame.Rect(sx_sp, oy, SPW, BH))
        pygame.draw.rect(surf, C_COVER,   pygame.Rect(sx_sp + SPW // 2 - 2, oy, 4, BH))
        for i in range(1, 7):
            ly2 = oy + int(BH * i / 7)
            pygame.draw.rect(surf, C_SPINE_LINE,
                             pygame.Rect(sx_sp, ly2 - 2, SPW, 4), border_radius=1)

        # dark tree canvas area — deep-space cosmos
        tx = ox + LW + SPW
        tw = BW - LW - SPW
        _STAR_TINT = {"warrior": (100, 120, 220),
                      "rogue":   (160, 100, 220),
                      "mage":    (60, 200, 220)}
        cls_bg = {"warrior": (6, 8, 18),
                  "rogue":   (8, 5, 16),
                  "mage":    (4, 10, 18)}.get(self._cls_id, (10, 10, 20))
        tree_surf = pygame.Surface((tw, BH))
        tree_surf.fill(cls_bg)
        # ── Starfield pass (seeded — stable, no flicker) ──────────────────
        import random as _rand_sf
        _srng  = _rand_sf.Random(tw * 31337 + BH)
        _stint = _STAR_TINT.get(self._cls_id, (200, 200, 255))
        _tr, _tg, _tb = _stint
        for _ in range(280):
            _sx = _srng.randint(0, tw - 1); _sy = _srng.randint(0, BH - 1)
            _sa = _srng.randint(30, 110)
            tree_surf.set_at((_sx, _sy), ((_tr*_sa)//255, (_tg*_sa)//255, (_tb*_sa)//255))
        for _ in range(100):
            _sx = _srng.randint(1, tw - 2); _sy = _srng.randint(1, BH - 2)
            _sa = _srng.randint(80, 180)
            pygame.draw.rect(tree_surf, ((_tr*_sa)//255, (_tg*_sa)//255, (_tb*_sa)//255),
                             pygame.Rect(_sx, _sy, 2, 2))
        for _ in range(25):
            _sx = _srng.randint(2, tw - 3); _sy = _srng.randint(2, BH - 3)
            _sa = _srng.randint(150, 240)
            pygame.draw.rect(tree_surf, ((_tr*_sa)//255, (_tg*_sa)//255, (_tb*_sa)//255),
                             pygame.Rect(_sx, _sy, 3, 3))
        self._draw_tree(tree_surf, tw, BH, cf)
        surf.blit(tree_surf, (tx, oy))
        pygame.draw.rect(surf, C_COVER, pygame.Rect(tx, oy, tw, BH), width=2)

        # store local tree rect (ox=0-relative, used by draw() for screen mapping)
        self._tree_local_rect = pygame.Rect(tx - ox, 0, tw, BH)

        # outer book border
        pygame.draw.rect(surf, C_COVER, pygame.Rect(ox, oy, BW, BH),
                         width=3, border_radius=8)

        # left-panel fade-in overlay
        fadea = int(255 * (1.0 - cf))
        if fadea > 4:
            fs = pygame.Surface((lf.width, lf.height), pygame.SRCALPHA)
            fs.fill((8, 10, 24, fadea))
            surf.blit(fs, (lf.x, lf.y))

        # left panel content
        self._draw_left_panel(surf, lf, cf)

        # page-turn shimmer on left panel
        if self._turn_t < 1.0:
            sa = int(90 * _math.sin(_ease_io(self._turn_t) * _math.pi))
            if sa > 2:
                ts2 = pygame.Surface((lf.width, lf.height), pygame.SRCALPHA)
                ts2.fill((255, 250, 230, sa))
                surf.blit(ts2, (lf.x, lf.y))

        # close button
        cbr = pygame.Rect(ox + BW - 34, oy + 6, 26, 26)
        mx_, my_ = pygame.mouse.get_pos()
        ch = (mx_ - ox, my_ - oy) if (ox, oy) != (0, 0) else (mx_, my_)
        cc = (190, 80, 60) if cbr.collidepoint(*ch) else (148, 56, 40)
        pygame.draw.rect(surf, cc, cbr, border_radius=5)
        cs = self._f(13, True).render("✕", True, (255, 238, 228))
        surf.blit(cs, cs.get_rect(center=cbr.center))

    # ── left information panel ────────────────────────────────────────────────

    def _draw_left_panel(self, surf, frame, cf):
        # Cosmic palette (blended with dark bg for fade-in)
        _bg = (8, 10, 24)
        C_TITLE = _blend((140, 180, 255), _bg, cf)
        C_LABEL = _blend((90, 120, 180),  _bg, cf)
        C_VAL   = _blend((210, 225, 255), _bg, cf)
        C_DIM   = _blend((60, 75, 115),   _bg, cf)
        C_DIV   = _blend((28, 38, 75),    _bg, cf)
        C_GLD   = _blend((220, 175, 55),  _bg, cf)
        C_GRN   = _blend((80, 210, 110),  _bg, cf)
        C_AMB   = _blend((220, 140, 40),  _bg, cf)
        C_LCK   = _blend((55, 65, 105),   _bg, cf)

        y = frame.y + 8

        # title row
        ts = self._f(13, True).render("✶  SKILL TREE", True, C_TITLE)
        surf.blit(ts, (frame.x + 6, y)); y += 20
        pygame.draw.line(surf, C_DIV, (frame.x + 4, y), (frame.right - 4, y)); y += 7

        # class + SP row
        cs2 = self._f(11, True).render(self._cls_id.upper(), True, C_VAL)
        surf.blit(cs2, (frame.x + 6, y))
        try:
            sp = self.gui.engine.player.stats.get("skill_points", 0) if self.gui.engine else 0
        except Exception:
            sp = 0
        sps = self._f(11).render(f"{sp} SP", True, C_GLD)
        surf.blit(sps, (frame.right - sps.get_width() - 6, y)); y += 19
        pygame.draw.line(surf, C_DIV, (frame.x + 4, y), (frame.right - 4, y)); y += 8

        sel = self._selected_id
        if sel and self._tree:
            node = next((n for n in self._tree if n["id"] == sel), None)
            if node:
                is_unl = sel in self._unlocked
                is_avl = sel in self._avail

                # name
                name_s = self._f(12, True).render(node["name"], True, C_VAL)
                surf.blit(name_s, (frame.x + 6, y)); y += 18

                # status pill
                if is_unl:
                    pill_bg = (20, 70, 30);  pill_tc = C_GRN;  pill_lbl = "UNLOCKED"
                elif is_avl:
                    pill_bg = (30, 65, 15);  pill_tc = (150, 220, 60); pill_lbl = "AVAILABLE"
                else:
                    pill_bg = (18, 20, 42);  pill_tc = C_LCK;  pill_lbl = "LOCKED"
                sbr = pygame.Rect(frame.x + 6, y, frame.width - 12, 15)
                ps  = pygame.Surface((sbr.width, sbr.height), pygame.SRCALPHA)
                pygame.draw.rect(ps, (*pill_bg, 210), (0, 0, sbr.width, sbr.height), border_radius=4)
                pygame.draw.rect(ps, (*pill_tc, 130), (0, 0, sbr.width, sbr.height), width=1, border_radius=4)
                surf.blit(ps, (sbr.x, sbr.y))
                sts = self._f(9, True).render(pill_lbl, True, pill_tc)
                surf.blit(sts, sts.get_rect(center=sbr.center)); y += 22

                # meta
                for lbl2, val in [
                    ("Tier", str(node.get("tier", "?"))),
                    ("Type", node.get("type", "passive").capitalize()),
                    ("Cost", f"{node.get('cost', '?')} SP"),
                ]:
                    l3 = self._f(9, True).render(lbl2, True, C_LABEL)
                    surf.blit(l3, (frame.x + 6, y))
                    v3 = self._f(9).render(val, True, C_VAL)
                    surf.blit(v3, (frame.x + 46, y)); y += 14

                pygame.draw.line(surf, C_DIV, (frame.x + 4, y), (frame.right - 4, y)); y += 5

                # description
                for line in _wrap(node.get("description", ""), self._f(10), frame.width - 12):
                    ds = self._f(10).render(line, True, C_DIM)
                    surf.blit(ds, (frame.x + 6, y)); y += 13
                    if y > frame.bottom - 52:
                        break

                # stat bonuses
                bonuses = node.get("stat_bonuses", {})
                if bonuses and y < frame.bottom - 38:
                    pygame.draw.line(surf, C_DIV, (frame.x + 4, y),
                                     (frame.right - 4, y)); y += 4
                    for stat, mod in bonuses.items():
                        bs3 = self._f(9).render(f"+{mod} {stat}", True, C_GRN)
                        surf.blit(bs3, (frame.x + 6, y)); y += 13
                        if y > frame.bottom - 28: break

                # unlock hint
                if is_avl and not is_unl:
                    hint = self._f(10).render("← Click to unlock", True, C_GLD)
                    surf.blit(hint, (frame.x + 6, frame.bottom - 24))

        else:
            # idle: legend
            for label, fill, out in [
                ("Locked",    (18, 22, 40),  (45, 55, 90)),
                ("Available", (42, 52, 15),  (150, 220, 60)),
                ("Passive",   (15, 48, 22),  (60, 200, 100)),
                ("Active",    (55, 22, 8),   (220, 140, 40)),
            ]:
                pygame.draw.circle(surf, fill, (frame.x + 11, y + 6), 6)
                pygame.draw.circle(surf, out,  (frame.x + 11, y + 6), 6, 1)
                ls2 = self._f(10).render(label, True, C_LABEL)
                surf.blit(ls2, (frame.x + 23, y)); y += 17
            y += 6
            hs = self._f(10).render("Click a node to", True, C_DIM)
            hs2 = self._f(10).render("view details.", True, C_DIM)
            surf.blit(hs,  (frame.x + 6, y)); y += 14
            surf.blit(hs2, (frame.x + 6, y))

        # footer
        pygame.draw.line(surf, C_DIV, (frame.x + 4, frame.bottom - 25),
                         (frame.right - 4, frame.bottom - 25))
        fh = self._f(9).render("Scroll=zoom  Drag=pan", True, C_DIM)
        surf.blit(fh, (frame.x + 6, frame.bottom - 16))

    # ── radial tree canvas ────────────────────────────────────────────────────

    def _draw_tree(self, surf, sw, sh, cf):
        try:
            from skill_tree import NODE_R, RING_GAP, LCENTER, _hex_to_rgb
        except ImportError:
            return

        tree     = self._tree
        unlocked = self._unlocked
        avail    = self._avail
        branches = self._branches_data
        z        = self._zoom
        cls_id   = self._cls_id

        if not tree:
            txt = self._tf(12).render("No skill tree for this class.", True, (180, 180, 180))
            surf.blit(txt, (sw // 2 - txt.get_width() // 2, sh // 2))
            return

        max_t    = max(n["tier"] for n in tree)
        ccx, ccy = self._l2s(LCENTER, LCENTER, sw, sh)

        # ── faint branch sector tints ─────────────────────────────────────
        sec_surf = pygame.Surface((sw, sh), pygame.SRCALPHA)
        for bname, bdef in branches.items():
            if bname == "origin": continue
            bc  = _hex_to_rgb(bdef.get("color", "#333333"))
            a_s = _math.radians(bdef["angle_start"])
            a_e = _math.radians(bdef["angle_end"])
            outer = (max_t + 0.8) * RING_GAP * z
            npts  = max(3, int(abs(a_e - a_s) * 14))
            pts   = [(int(ccx), int(ccy))]
            for i in range(npts + 1):
                a = a_s + (a_e - a_s) * i / npts
                pts.append((int(ccx + outer * _math.cos(a)),
                            int(ccy + outer * _math.sin(a))))
            if len(pts) >= 3:
                pygame.draw.polygon(sec_surf, (*bc, 9), pts)
        surf.blit(sec_surf, (0, 0))

        # ── ring guides ───────────────────────────────────────────────────
        rg_surf = pygame.Surface((sw, sh), pygame.SRCALPHA)
        for t in range(1, max_t + 1):
            rr = int(t * RING_GAP * z)
            if rr > 4 and -rr < ccx < sw + rr and -rr < ccy < sh + rr:
                alpha = max(10, 32 - t * 4)
                pygame.draw.circle(rg_surf, (18, 28, 58, 60),
                                   (int(ccx), int(ccy)), rr, 1)
        surf.blit(rg_surf, (0, 0))

        # ── branch separators + pill labels ───────────────────────────────
        b_count, b_unl = {}, {}
        for node in tree:
            b = node.get("branch", "origin")
            if b == "origin": continue
            b_count[b] = b_count.get(b, 0) + 1
            if node["id"] in unlocked:
                b_unl[b] = b_unl.get(b, 0) + 1

        sep_surf = pygame.Surface((sw, sh), pygame.SRCALPHA)
        for bname, bdef in branches.items():
            if bname == "origin": continue
            bc     = _hex_to_rgb(bdef.get("color", "#555555"))
            a_line = _math.radians(bdef["angle_start"])
            outer  = (max_t + 0.5) * RING_GAP * z
            ex     = ccx + outer * _math.cos(a_line)
            ey     = ccy + outer * _math.sin(a_line)
            pygame.draw.line(sep_surf, (*bc, 35),
                             (int(ccx), int(ccy)), (int(ex), int(ey)), 1)
        surf.blit(sep_surf, (0, 0))

        if z >= 0.35:
            for bname, bdef in branches.items():
                if bname == "origin": continue
                bc    = _hex_to_rgb(bdef.get("color", "#555555"))
                mid_a = _math.radians((bdef["angle_start"] + bdef["angle_end"]) / 2)
                lr    = (max_t + 1.3) * RING_GAP * z
                lx_b  = ccx + lr * _math.cos(mid_a)
                ly_b  = ccy + lr * _math.sin(mid_a)
                cnt   = b_count.get(bname, 0)
                unc   = b_unl.get(bname, 0)
                lbl   = bdef["label"].upper() + (f"  {unc}/{cnt}" if z >= 0.4 else "")
                t_s   = self._tf(8).render(lbl, True, bc)
                pr    = pygame.Rect(int(lx_b) - t_s.get_width() // 2 - 6,
                                    int(ly_b) - t_s.get_height() // 2 - 3,
                                    t_s.get_width() + 12, t_s.get_height() + 6)
                ps2   = pygame.Surface((pr.width, pr.height), pygame.SRCALPHA)
                pygame.draw.rect(ps2, (*bc, 28), (0, 0, pr.width, pr.height),
                                 border_radius=3)
                pygame.draw.rect(ps2, (*bc, 60), (0, 0, pr.width, pr.height),
                                 width=1, border_radius=3)
                surf.blit(ps2, (pr.x, pr.y))
                surf.blit(t_s, (int(lx_b) - t_s.get_width() // 2,
                                int(ly_b) - t_s.get_height() // 2))

        # ── connections ───────────────────────────────────────────────────
        pulse_t = abs((self._pulse_phase % 16) - 8) / 8.0
        cn_surf = pygame.Surface((sw, sh), pygame.SRCALPHA)
        for node in tree:
            nid = node["id"]
            if nid not in self._positions: continue
            ncx, ncy = self._l2s(*self._positions[nid], sw, sh)
            for pid in node.get("prerequisites", []):
                if pid not in self._positions: continue
                pcx, pcy = self._l2s(*self._positions[pid], sw, sh)
                both   = nid in unlocked and pid in unlocked
                either = nid in avail or pid in avail
                p1     = (int(pcx), int(pcy))
                p2     = (int(ncx), int(ncy))
                if both:
                    pygame.draw.line(cn_surf, (80, 160, 255, 180), p1, p2, 3)
                    pygame.draw.line(cn_surf, (120, 200, 255, 80), p1, p2, 1)
                elif either:
                    a = int(55 + 65 * pulse_t)
                    pygame.draw.line(cn_surf, (150, 220, 60, a), p1, p2, 2)
                else:
                    pygame.draw.line(cn_surf, (20, 28, 50, 100), p1, p2, 1)
        surf.blit(cn_surf, (0, 0))

        # ── nodes ─────────────────────────────────────────────────────────
        # Medieval palette
        # Locked:           dark iron
        # Available:        amber gold
        # Passive unlocked: forest sage
        # Active unlocked:  crimson fire
        _COLS = {
            "locked":    ((18, 22, 40),  (45, 55, 90),   (70, 80, 120)),
            "avail":     ((42, 52, 15),  (150, 220, 60),  (200, 255, 100)),
            "passive":   ((15, 48, 22),  (60, 200, 100),  (120, 230, 150)),
            "active":    ((55, 22, 8),   (220, 140, 40),  (255, 200, 90)),
        }
        nr   = NODE_R * z
        spin = self._spin_angle
        gw_s = pygame.Surface((sw, sh), pygame.SRCALPHA)
        dc_s = pygame.Surface((sw, sh), pygame.SRCALPHA)

        # ── pass 1: glow / halos ──────────────────────────────────────────
        for node in tree:
            nid = node["id"]
            if nid not in self._positions: continue
            px, py   = self._l2s(*self._positions[nid], sw, sh)
            isx, isy = int(px), int(py)
            if isx < -80 or isx > sw + 80 or isy < -80 or isy > sh + 80:
                continue

            is_orig  = (node["tier"] == 0)
            is_act   = (node["type"] == "active")
            is_sel   = (nid == self._selected_id)
            is_hover = (nid == self._hover_id)
            r        = int(nr * 1.7) if is_orig else int(nr)

            if nid in unlocked:
                key = "active" if is_act else "passive"
            elif nid in avail:
                key = "avail"
            else:
                key = "locked"
            fill, out, inner_col = _COLS[key]

            # click flash — brief bright radial burst
            flash = self._click_flash.get(nid, 0)
            if flash > 0:
                ft = flash / 0.45
                fc = (255, 230, 120) if key == "avail" else \
                     (255, 200, 80) if key in ("passive", "active") else (180, 160, 120)
                for gi in range(7, 0, -1):
                    pygame.draw.circle(gw_s, (*fc, int(ft * gi * 20)),
                                       (isx, isy), r + gi * 8)

            # selected: gold sun-halo
            elif is_sel:
                for gi in range(5, 0, -1):
                    pygame.draw.circle(gw_s, (80, 160, 255, 12 + gi * 16),
                                       (isx, isy), r + 3 + gi * 5)
            # hover: cosmic blue tint
            elif is_hover:
                for gi in range(3, 0, -1):
                    pygame.draw.circle(gw_s, (120, 180, 255, 10 + gi * 12),
                                       (isx, isy), r + 2 + gi * 3)
            # available: lime starfield pulse
            elif key == "avail":
                pr2 = int(r + 4 + pulse_t * 3)
                pa  = int(50 + 70 * pulse_t)
                pygame.draw.circle(gw_s, (150, 220, 60, pa), (isx, isy), pr2, 2)
                pygame.draw.circle(gw_s, (100, 180, 40, pa // 3), (isx, isy), pr2 + 5, 1)
            # unlocked: faint cosmic aura
            elif key == "active":
                pygame.draw.circle(gw_s, (220, 140, 40, 25), (isx, isy), r + 8)
            elif key == "passive":
                pygame.draw.circle(gw_s, (60, 200, 100, 20), (isx, isy), r + 7)

        surf.blit(gw_s, (0, 0))

        # ── pass 2: shapes + inner detail ────────────────────────────────
        for node in tree:
            nid = node["id"]
            if nid not in self._positions: continue
            px, py   = self._l2s(*self._positions[nid], sw, sh)
            isx, isy = int(px), int(py)
            if isx < -80 or isx > sw + 80 or isy < -80 or isy > sh + 80:
                continue

            is_orig  = (node["tier"] == 0)
            is_act   = (node["type"] == "active")
            is_sel   = (nid == self._selected_id)
            is_hover = (nid == self._hover_id)
            r        = int(nr * 1.7) if is_orig else int(nr)

            if nid in unlocked:
                key = "active" if is_act else "passive"
            elif nid in avail:
                key = "avail"
            else:
                key = "locked"
            fill, out, inner_col = _COLS[key]

            # outer border highlight when hovered/selected
            brd_w = 3 if (is_sel or is_hover) else 2
            brd_c = (255, 225, 90) if is_sel else out

            self._draw_node_shape(surf, cls_id, isx, isy, r, fill, brd_c,
                                  brd_w=brd_w, is_act=is_act, is_orig=is_orig)

            if z < 0.42:
                continue   # skip labels when zoomed out

            # ── name label ────────────────────────────────────────────────
            if z >= 0.35:
                name  = node["name"]
                if z < 0.65 and len(name) > 10:
                    name = name[:8] + ".."
                max_w = max(28, int(r * 2 + 10))
                lines, cur = [], ""
                for wrd in name.split():
                    test = (cur + " " + wrd).strip()
                    if self._tf(7).size(test)[0] <= max_w or not cur:
                        cur = test
                    else:
                        lines.append(cur); cur = wrd
                if cur: lines.append(cur)
                ty = isy + r + 3
                lc = (255, 255, 120) if is_sel else \
                     (210, 225, 255) if (is_hover or key != "locked") else \
                     (50, 55, 80)
                for line in lines:
                    t_ = self._tf(7).render(line, True, lc)
                    surf.blit(t_, (isx - t_.get_width() // 2, ty))
                    ty += self._tf(7).get_height()

        surf.blit(dc_s, (0, 0))

        # ── HUD ───────────────────────────────────────────────────────────
        hud_s = self._tf(9).render(
            f"Scroll = zoom  ·  Drag = pan  ·  R = refresh",
            True, (80, 100, 160))
        surf.blit(hud_s, (6, sh - 17))

    def _draw_node_shape(self, surf, cls_id, cx, cy, r, fill, outline,
                         brd_w=2, is_act=False, is_orig=False):
        """Uniform circular nodes — cosmic starfield style (all classes)."""
        pygame.draw.circle(surf, fill, (cx, cy), r)
        pygame.draw.circle(surf, outline, (cx, cy), r, brd_w)
        # Centre dot for visual depth
        if r >= 5:
            cdot = (min(255, fill[0] + 40), min(255, fill[1] + 40), min(255, fill[2] + 40))
            pygame.draw.circle(surf, cdot, (cx, cy), max(1, r // 3))
        # Active: extra outer ring
        if is_act and not is_orig and r >= 5:
            pad = r + max(3, r // 3) + 5
            rs  = pygame.Surface((pad * 2, pad * 2), pygame.SRCALPHA)
            pygame.draw.circle(rs, (*outline, 55), (pad, pad), r + max(3, r // 3), 1)
            surf.blit(rs, (cx - pad, cy - pad))


# ═══════════════════════════════════════════════════════════════════════════
#  SETTINGS OVERLAY  –  parchment-book settings panel (no pygame_gui)
# ═══════════════════════════════════════════════════════════════════════════

import copy as _copy

_CFG_DEFAULTS = {
    "visual":        {"font_size": 13},
    "gameplay":      {"combat_speed": "normal", "scroll_mode": "auto",
                      "difficulty_modifier": 1.0},
    "accessibility": {"high_contrast": False, "text_size": 13},
    "ui":            {"layout": "side_by_side", "timestamps": False,
                      "max_messages": 200},
}

_COMBAT_SPEEDS = ["slow", "normal", "fast"]
_SCROLL_MODES  = ["auto", "lock"]
_UI_LAYOUTS    = ["side_by_side", "stacked", "single"]
_DIFF_STEPS    = [0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0]
_DIFF_LABELS   = ["0.5\u00d7", "0.75\u00d7", "1\u00d7", "1.25\u00d7",
                  "1.5\u00d7", "1.75\u00d7", "2\u00d7"]


def _cfg_get(cfg, *keys, default=None):
    d = cfg
    for k in keys:
        if not isinstance(d, dict) or k not in d:
            return default
        d = d[k]
    return d


class SettingsOverlay(BookOverlay):
    """Parchment-book settings overlay — replaces pygame_gui SettingsWindow."""

    _FLASH_DUR = 0.7

    def __init__(self, gui):
        super().__init__(gui,
                         title_left="Configuration",
                         title_right="Interface",
                         width=780, height=540)
        self._working:    dict  = {}
        self._btn_hits:   list  = []
        self._status:     str   = ""
        self._status_t:   float = 0.0
        self._save_flash:  float = 0.0
        self._reset_flash: float = 0.0
        self._load_config()

    # ---- config I/O ---------------------------------------------------

    def _load_config(self):
        try:
            raw = getattr(self.gui, "config", {}) or {}
            self._working = _copy.deepcopy(raw)
        except Exception:
            self._working = {}
        for section, vals in _CFG_DEFAULTS.items():
            if section not in self._working:
                self._working[section] = {}
            for k, v in vals.items():
                if k not in self._working[section]:
                    self._working[section][k] = v

    def _w(self, *keys, default=None):
        return _cfg_get(self._working, *keys, default=default)

    def _wset(self, *keys_and_value):
        keys, val = keys_and_value[:-1], keys_and_value[-1]
        d = self._working
        for k in keys[:-1]:
            d = d.setdefault(k, {})
        d[keys[-1]] = val

    def _save(self):
        try:
            self.gui.config = _copy.deepcopy(self._working)
            if hasattr(self.gui, "save_config"):  self.gui.save_config()
            if hasattr(self.gui, "apply_config"): self.gui.apply_config()
            self._save_flash = self._FLASH_DUR
            self.close()
        except Exception as ex:
            self._status   = f"Error: {ex}"
            self._status_t = 4.0

    def _reset(self):
        self._working      = _copy.deepcopy(_CFG_DEFAULTS)
        self._reset_flash  = self._FLASH_DUR
        self._status       = "Reset to defaults."
        self._status_t     = 2.5

    # ---- lifecycle ----------------------------------------------------

    def _on_update(self, dt):
        for attr in ("_status_t", "_save_flash", "_reset_flash"):
            v = getattr(self, attr)
            if v > 0:
                setattr(self, attr, max(0.0, v - dt))

    def _on_keydown(self, event) -> bool:
        if event.key == pygame.K_s and (event.mod & pygame.KMOD_CTRL):
            self._save(); return True
        return False

    def _on_click(self, pos) -> bool:
        for rect, action in self._btn_hits:
            if rect.collidepoint(pos):
                self._dispatch(action); return True
        return True

    def _dispatch(self, action: str):
        dispatch_map = {
            "font_size_inc":       lambda: self._wset("visual", "font_size",
                                       min(20, self._w("visual","font_size",default=13)+1)),
            "font_size_dec":       lambda: self._wset("visual", "font_size",
                                       max(7,  self._w("visual","font_size",default=13)-1)),
            "text_size_inc":       lambda: self._wset("accessibility","text_size",
                                       min(24,self._w("accessibility","text_size",default=13)+1)),
            "text_size_dec":       lambda: self._wset("accessibility","text_size",
                                       max(8, self._w("accessibility","text_size",default=13)-1)),
            "timestamps_toggle":   lambda: self._wset("ui","timestamps",
                                       not self._w("ui","timestamps",default=False)),
            "hc_toggle":           lambda: self._wset("accessibility","high_contrast",
                                       not self._w("accessibility","high_contrast",default=False)),
            "maxmsg_dec":          lambda: self._wset("ui","max_messages",
                                       max(10, self._w("ui","max_messages",default=200)-10)),
            "maxmsg_inc":          lambda: self._wset("ui","max_messages",
                                       min(500,self._w("ui","max_messages",default=200)+10)),
            "save":  self._save,
            "reset": self._reset,
        }
        if action in dispatch_map:
            dispatch_map[action](); return
        # cycling actions
        def _cycle(keys, store_keys, lst, direction):
            v   = self._w(*keys, default=lst[0])
            idx = lst.index(v) if v in lst else 0
            self._wset(*store_keys, lst[(idx + direction) % len(lst)])
        if action == "combat_speed_prev":
            _cycle(("gameplay","combat_speed"),("gameplay","combat_speed"),_COMBAT_SPEEDS,-1)
        elif action == "combat_speed_next":
            _cycle(("gameplay","combat_speed"),("gameplay","combat_speed"),_COMBAT_SPEEDS,+1)
        elif action == "scroll_mode_prev":
            _cycle(("gameplay","scroll_mode"),("gameplay","scroll_mode"),_SCROLL_MODES,-1)
        elif action == "scroll_mode_next":
            _cycle(("gameplay","scroll_mode"),("gameplay","scroll_mode"),_SCROLL_MODES,+1)
        elif action == "layout_prev":
            _cycle(("ui","layout"),("ui","layout"),_UI_LAYOUTS,-1)
        elif action == "layout_next":
            _cycle(("ui","layout"),("ui","layout"),_UI_LAYOUTS,+1)
        elif action in ("diff_dec","diff_inc"):
            dv = self._w("gameplay","difficulty_modifier",default=1.0)
            try:
                idx = min(range(len(_DIFF_STEPS)),
                          key=lambda i: abs(_DIFF_STEPS[i]-float(dv)))
            except Exception: idx = 2
            d = -1 if action == "diff_dec" else +1
            self._wset("gameplay","difficulty_modifier",
                       _DIFF_STEPS[max(0,min(len(_DIFF_STEPS)-1,idx+d))])

    # ---- drawing helpers ----------------------------------------------

    def _tf(self, sz, bold=False): return self._f(sz, bold)

    def _section_head(self, surf, frame, y, text, cf, right_page=False):
        bg  = C_PARCHMENT_L if right_page else C_PARCHMENT
        div = _blend(C_DIVIDER, bg, cf)
        hdr = _blend(C_HEADER,  bg, cf)
        pygame.draw.line(surf, div, (frame.x+4, y+5), (frame.x+frame.width-4, y+5), 1)
        lbl = self._tf(9, True).render(text, True, hdr)
        lx  = frame.x + (frame.width - lbl.get_width()) // 2
        pygame.draw.rect(surf, bg, pygame.Rect(lx-4, y, lbl.get_width()+8, lbl.get_height()))
        surf.blit(lbl, (lx, y))
        return y + lbl.get_height() + 7

    def _row_stepper(self, surf, frame, y, label, val_txt,
                     act_dec, act_inc, cf, right=False):
        bg     = C_PARCHMENT_L if right else C_PARCHMENT
        ink    = _blend(C_INK,     bg, cf)
        mid    = _blend(C_INK_MID, bg, cf)
        div    = _blend(C_DIVIDER, bg, cf)
        ROW_H  = 22; BTN_W = 18; BTN_H = 16; val_w = 82
        vy     = y + (ROW_H - BTN_H) // 2
        ls     = self._tf(11).render(label, True, ink)
        surf.blit(ls, (frame.x+6, y+(ROW_H-ls.get_height())//2))
        vx     = frame.x + frame.width - val_w - 6
        mx, my = pygame.mouse.get_pos()
        # ◄
        dr = pygame.Rect(vx, vy, BTN_W, BTN_H)
        hd = dr.collidepoint(mx-self._book_rect.x, my-self._book_rect.y)
        dc = _blend(C_GOLD, bg, cf) if hd else div
        pygame.draw.rect(surf, (*dc[:3],200), dr, border_radius=3)
        pygame.draw.rect(surf, mid, dr, width=1, border_radius=3)
        surf.blit(self._tf(11,True).render("\u25c4",True,mid),
                  self._tf(11,True).render("\u25c4",True,mid).get_rect(center=dr.center))
        self._btn_hits.append((pygame.Rect(self._book_rect.x+dr.x,
                                           self._book_rect.y+dr.y,
                                           dr.width,dr.height), act_dec))
        # value
        vl  = self._tf(11).render(val_txt, True, ink)
        vox = vx + BTN_W + (val_w - BTN_W*2 - vl.get_width())//2
        surf.blit(vl, (vox, y+(ROW_H-vl.get_height())//2))
        # ►
        ir = pygame.Rect(vx+val_w-BTN_W, vy, BTN_W, BTN_H)
        hi = ir.collidepoint(mx-self._book_rect.x, my-self._book_rect.y)
        ic = _blend(C_GOLD, bg, cf) if hi else div
        pygame.draw.rect(surf, (*ic[:3],200), ir, border_radius=3)
        pygame.draw.rect(surf, mid, ir, width=1, border_radius=3)
        surf.blit(self._tf(11,True).render("\u25ba",True,mid),
                  self._tf(11,True).render("\u25ba",True,mid).get_rect(center=ir.center))
        self._btn_hits.append((pygame.Rect(self._book_rect.x+ir.x,
                                           self._book_rect.y+ir.y,
                                           ir.width,ir.height), act_inc))
        pygame.draw.line(surf, _blend(C_DIVIDER, bg, cf*0.4),
                         (frame.x+4, y+ROW_H), (frame.x+frame.width-4, y+ROW_H), 1)
        return y + ROW_H + 4

    def _row_toggle(self, surf, frame, y, label, value_bool, action, cf, right=False):
        bg     = C_PARCHMENT_L if right else C_PARCHMENT
        ink    = _blend(C_INK,     bg, cf)
        mid    = _blend(C_INK_MID, bg, cf)
        ROW_H  = 22; BOX_W = 36; BOX_H = 16
        ls     = self._tf(11).render(label, True, ink)
        surf.blit(ls, (frame.x+6, y+(ROW_H-ls.get_height())//2))
        bx  = frame.x + frame.width - BOX_W - 8
        bby = y + (ROW_H - BOX_H) // 2
        br  = pygame.Rect(bx, bby, BOX_W, BOX_H)
        mx, my = pygame.mouse.get_pos()
        ho  = br.collidepoint(mx-self._book_rect.x, my-self._book_rect.y)
        fl  = C_DONE if value_bool else (180, 155, 110)
        if ho: fl = tuple(min(255,c+20) for c in fl)
        pygame.draw.rect(surf, fl,  br, border_radius=8)
        pygame.draw.rect(surf, mid, br, width=1, border_radius=8)
        kx = bx+BOX_W-14 if value_bool else bx+2
        pygame.draw.circle(surf, (248,235,210), (kx+6, bby+BOX_H//2), 6)
        lbl2 = "ON" if value_bool else "OFF"
        ts2  = self._tf(8,True).render(lbl2,True,(30,20,10) if value_bool else (120,100,70))
        loff = bx+4 if value_bool else bx+14
        surf.blit(ts2, (loff, bby+(BOX_H-ts2.get_height())//2))
        self._btn_hits.append((pygame.Rect(self._book_rect.x+br.x,
                                           self._book_rect.y+br.y,
                                           br.width,br.height), action))
        pygame.draw.line(surf, _blend(C_DIVIDER, bg, cf*0.4),
                         (frame.x+4, y+ROW_H), (frame.x+frame.width-4, y+ROW_H), 1)
        return y + ROW_H + 4

    def _action_button(self, surf, frame, y, label, action,
                       normal_col, hover_col, cf, right=False):
        bg     = C_PARCHMENT_L if right else C_PARCHMENT
        BTN_H  = 28; BTN_W = frame.width - 8
        br     = pygame.Rect(frame.x+4, y, BTN_W, BTN_H)
        mx, my = pygame.mouse.get_pos()
        ho     = br.collidepoint(mx-self._book_rect.x, my-self._book_rect.y)
        col    = hover_col if ho else normal_col
        bs     = pygame.Surface((BTN_W, BTN_H), pygame.SRCALPHA)
        pygame.draw.rect(bs, (*col, 220), (0,0,BTN_W,BTN_H), border_radius=6)
        pygame.draw.rect(bs, (255,240,180,160), (0,0,BTN_W,BTN_H), width=1, border_radius=6)
        surf.blit(bs, (br.x, br.y))
        ts = self._tf(11,True).render(label, True, (245,235,210))
        surf.blit(ts, ts.get_rect(center=br.center))
        self._btn_hits.append((pygame.Rect(self._book_rect.x+br.x,
                                           self._book_rect.y+br.y,
                                           br.width,br.height), action))
        return y + BTN_H + 5

    # ---- left page ----------------------------------------------------

    def _draw_left_page(self, surf, frame, cf):
        self._btn_hits = []
        y = self._page_title(surf, frame, "Configuration", cf, left=True) + 4
        y = self._section_head(surf, frame, y, "\u2726  Appearance  \u2726", cf)
        fs = self._w("visual", "font_size", default=13)
        y  = self._row_stepper(surf, frame, y, "UI Font Size", f"{fs} pt",
                                "font_size_dec", "font_size_inc", cf)
        y = self._section_head(surf, frame, y+2, "\u2726  Gameplay  \u2726", cf)
        dv = self._w("gameplay", "difficulty_modifier", default=1.0)
        try:
            di   = min(range(len(_DIFF_STEPS)), key=lambda i: abs(_DIFF_STEPS[i]-float(dv)))
            dlbl = _DIFF_LABELS[di]
        except Exception:
            dlbl = f"{dv}\u00d7"
        y  = self._row_stepper(surf, frame, y, "Difficulty", dlbl,
                                "diff_dec", "diff_inc", cf)
        cs = self._w("gameplay", "combat_speed", default="normal")
        y  = self._row_stepper(surf, frame, y, "Combat Speed", cs.capitalize(),
                                "combat_speed_prev", "combat_speed_next", cf)
        sm = self._w("gameplay", "scroll_mode", default="auto")
        y  = self._row_stepper(surf, frame, y, "Scroll Mode", sm.capitalize(),
                                "scroll_mode_prev", "scroll_mode_next", cf)
        ts = self._w("ui", "timestamps", default=False)
        y  = self._row_toggle(surf, frame, y, "Show Timestamps", ts,
                               "timestamps_toggle", cf)
        hc = self._w("accessibility", "high_contrast", default=False)
        y  = self._row_toggle(surf, frame, y, "High Contrast", hc,
                               "hc_toggle", cf)
        bg   = C_PARCHMENT
        hint = self._tf(9).render("Ctrl+S  \u00b7  ESC to cancel", True,
                                   _blend(C_INK_LIGHT, bg, cf*0.7))
        surf.blit(hint, (frame.x+6, frame.y+frame.height-hint.get_height()-4))

    # ---- right page ---------------------------------------------------

    def _draw_right_page(self, surf, frame, cf):
        y  = self._page_title(surf, frame, "Interface", cf, left=False) + 4
        y  = self._section_head(surf, frame, y, "\u2726  Accessibility  \u2726", cf, right_page=True)
        tz = self._w("accessibility", "text_size", default=13)
        y  = self._row_stepper(surf, frame, y, "Text Size", f"{tz} pt",
                                "text_size_dec", "text_size_inc", cf, right=True)
        y  = self._section_head(surf, frame, y+2, "\u2726  UI Layout  \u2726", cf, right_page=True)
        lv = self._w("ui", "layout", default="side_by_side")
        ll = {"side_by_side":"Side by Side","stacked":"Stacked",
              "single":"Single"}.get(lv, lv.replace("_"," ").title())
        y  = self._row_stepper(surf, frame, y, "Panel Layout", ll,
                                "layout_prev", "layout_next", cf, right=True)
        mm = self._w("ui", "max_messages", default=200)
        y  = self._row_stepper(surf, frame, y, "Max Messages", str(mm),
                                "maxmsg_dec", "maxmsg_inc", cf, right=True)

        y += 14
        sf_t = self._save_flash  / self._FLASH_DUR
        rf_t = self._reset_flash / self._FLASH_DUR
        sv_col = (200,155,30) if sf_t > 0.01 else (55,110,50)
        sv_hov = (90,155,80)
        y  = self._action_button(surf, frame, y,
             "\u2714  Saved!" if sf_t > 0.01 else "\u2714  Save & Close",
             "save", sv_col, sv_hov, cf, right=True)
        rs_col = (110,48,22)
        rs_hov = (155,65,30)
        y  = self._action_button(surf, frame, y,
             "\u21ba  Reset!" if rf_t > 0.01 else "\u21ba  Reset Defaults",
             "reset", rs_col, rs_hov, cf, right=True)

        bg = C_PARCHMENT_L
        if self._status and self._status_t > 0:
            al  = min(1.0, self._status_t)
            sc  = _blend(C_DONE, bg, cf*al)
            ss  = self._tf(10).render(self._status, True, sc)
            surf.blit(ss, (frame.x+(frame.width-ss.get_width())//2, y+4))
