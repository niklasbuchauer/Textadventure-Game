"""Shared font selection and loading helpers for robust Unicode rendering."""

from __future__ import annotations

import os
from typing import Dict, List, Optional, Tuple

import pygame

UI_FONT_ALIAS = "EstoriaUI"
MONO_FONT_ALIAS = "EstoriaMono"

# Prioritize box drawing support while still checking common game symbols.
_REQUIRED_BOX_GLYPHS = "║╗╣╠╔╝╚┌┐└┘─│━┃"
_REQUIRED_SYMBOL_GLYPHS = "⚔🛡🏆✅◻★☠🔥❄⚗💰🔰⛑🥾🧤💍📿✨💀👑💎"

_UI_SYSTEM_CANDIDATES = [
    "Segoe UI Symbol",
    "Segoe UI Emoji",
    "Segoe UI",
    "Arial Unicode MS",
    "Arial",
]

_MONO_SYSTEM_CANDIDATES = [
    "Cascadia Mono",
    "Consolas",
    "DejaVu Sans Mono",
    "Courier New",
    "Lucida Console",
]

_UI_BUNDLED_FILES = [
    {
        "regular": "NotoSans-Regular.ttf",
        "bold": "NotoSans-Bold.ttf",
        "italic": "NotoSans-Italic.ttf",
        "bold_italic": "NotoSans-BoldItalic.ttf",
    },
    {
        "regular": "DejaVuSans.ttf",
        "bold": "DejaVuSans-Bold.ttf",
        "italic": "DejaVuSans-Oblique.ttf",
        "bold_italic": "DejaVuSans-BoldOblique.ttf",
    },
]

_MONO_BUNDLED_FILES = [
    {
        "regular": "NotoSansMono-Regular.ttf",
        "bold": "NotoSansMono-Bold.ttf",
        "italic": "NotoSansMono-Regular.ttf",
        "bold_italic": "NotoSansMono-Bold.ttf",
    },
    {
        "regular": "DejaVuSansMono.ttf",
        "bold": "DejaVuSansMono-Bold.ttf",
        "italic": "DejaVuSansMono-Oblique.ttf",
        "bold_italic": "DejaVuSansMono-BoldOblique.ttf",
    },
]

_SCORE_CACHE: Dict[str, Tuple[int, int, int]] = {}


def _font_supports_char(font: pygame.font.Font, ch: str) -> bool:
    if not ch:
        return True
    try:
        metrics = font.metrics(ch)
        if metrics and metrics[0] is not None:
            return True
    except Exception:
        pass
    try:
        rendered = font.render(ch, True, (255, 255, 255))
        return rendered.get_width() > 0 and rendered.get_height() > 0
    except Exception:
        return False


def _score_font_path(path: str) -> Tuple[int, int, int]:
    cached = _SCORE_CACHE.get(path)
    if cached is not None:
        return cached

    if not os.path.exists(path):
        score = (0, 0, 0)
        _SCORE_CACHE[path] = score
        return score

    try:
        font = pygame.font.Font(path, 18)
    except Exception:
        score = (0, 0, 0)
        _SCORE_CACHE[path] = score
        return score

    box_hits = sum(1 for ch in _REQUIRED_BOX_GLYPHS if _font_supports_char(font, ch))
    sym_hits = sum(1 for ch in _REQUIRED_SYMBOL_GLYPHS if _font_supports_char(font, ch))
    # Strongly bias toward box glyphs, which are currently the worst tofu offenders.
    weighted = box_hits * 3 + sym_hits
    score = (weighted, box_hits, sym_hits)
    _SCORE_CACHE[path] = score
    return score


def _pick_system_candidate(names: List[str]) -> Optional[Dict[str, Optional[str]]]:
    best = None
    best_score = (-1, -1, -1)

    for name in names:
        regular = pygame.font.match_font(name, bold=False, italic=False)
        if not regular:
            continue

        score = _score_font_path(regular)
        if score > best_score:
            best_score = score
            best = {
                "name": name,
                "regular": regular,
                "bold": pygame.font.match_font(name, bold=True, italic=False) or regular,
                "italic": pygame.font.match_font(name, bold=False, italic=True) or regular,
                "bold_italic": pygame.font.match_font(name, bold=True, italic=True)
                or pygame.font.match_font(name, bold=True, italic=False)
                or regular,
            }

    return best


def _pick_bundled_candidate(fonts_dir: str, specs: List[Dict[str, str]]) -> Optional[Dict[str, Optional[str]]]:
    best = None
    best_score = (-1, -1, -1)

    for spec in specs:
        regular = os.path.join(fonts_dir, spec["regular"])
        if not os.path.exists(regular):
            continue

        score = _score_font_path(regular)
        if score > best_score:
            best_score = score
            best = {
                "name": None,
                "regular": regular,
                "bold": os.path.join(fonts_dir, spec["bold"]),
                "italic": os.path.join(fonts_dir, spec["italic"]),
                "bold_italic": os.path.join(fonts_dir, spec["bold_italic"]),
            }

    if not best:
        return None

    for key in ("bold", "italic", "bold_italic"):
        if not best.get(key) or not os.path.exists(str(best[key])):
            best[key] = best["regular"]

    return best


def _pick_best_font(fonts_dir: str, bundled_specs: List[Dict[str, str]], system_candidates: List[str]) -> Dict[str, Optional[str]]:
    bundled = _pick_bundled_candidate(fonts_dir, bundled_specs)
    system = _pick_system_candidate(system_candidates)

    if bundled and system:
        bundled_score = _score_font_path(str(bundled["regular"]))
        system_score = _score_font_path(str(system["regular"]))
        return bundled if bundled_score >= system_score else system
    if bundled:
        return bundled
    if system:
        return system

    # Final emergency fallback: pygame default font.
    return {
        "name": None,
        "regular": None,
        "bold": None,
        "italic": None,
        "bold_italic": None,
    }


def setup_ui_font_profile(manager: pygame_gui.UIManager, base_dir: str) -> Dict[str, Optional[str]]:
    """Register deterministic UI/mono font aliases and return runtime profile."""
    fonts_dir = os.path.join(base_dir, "assets", "fonts")

    ui_pick = _pick_best_font(fonts_dir, _UI_BUNDLED_FILES, _UI_SYSTEM_CANDIDATES)
    mono_pick = _pick_best_font(fonts_dir, _MONO_BUNDLED_FILES, _MONO_SYSTEM_CANDIDATES)

    profile: Dict[str, Optional[str]] = {
        "ui_alias": UI_FONT_ALIAS,
        "mono_alias": MONO_FONT_ALIAS,
        "ui_font_name": ui_pick.get("name"),
        "mono_font_name": mono_pick.get("name"),
        "ui_regular_path": ui_pick.get("regular"),
        "ui_bold_path": ui_pick.get("bold"),
        "ui_italic_path": ui_pick.get("italic"),
        "ui_bold_italic_path": ui_pick.get("bold_italic"),
        "mono_regular_path": mono_pick.get("regular"),
        "mono_bold_path": mono_pick.get("bold"),
        "mono_italic_path": mono_pick.get("italic"),
        "mono_bold_italic_path": mono_pick.get("bold_italic"),
    }

    if profile["ui_regular_path"]:
        manager.add_font_paths(
            UI_FONT_ALIAS,
            str(profile["ui_regular_path"]),
            str(profile["ui_bold_path"] or profile["ui_regular_path"]),
            str(profile["ui_italic_path"] or profile["ui_regular_path"]),
            str(profile["ui_bold_italic_path"] or profile["ui_regular_path"]),
        )

    if profile["mono_regular_path"]:
        manager.add_font_paths(
            MONO_FONT_ALIAS,
            str(profile["mono_regular_path"]),
            str(profile["mono_bold_path"] or profile["mono_regular_path"]),
            str(profile["mono_italic_path"] or profile["mono_regular_path"]),
            str(profile["mono_bold_italic_path"] or profile["mono_regular_path"]),
        )

    preload_sizes = [11, 12, 13, 14, 15, 18, 20, 22, 44, 46]
    preload_styles = ["regular", "bold", "italic", "bold_italic"]
    preload = []

    for size in preload_sizes:
        for style in preload_styles:
            preload.append({"name": UI_FONT_ALIAS, "point_size": size, "style": style})
    for size in (11, 14, 17):
        preload.append({"name": MONO_FONT_ALIAS, "point_size": size, "style": "regular"})
        preload.append({"name": MONO_FONT_ALIAS, "point_size": size, "style": "bold"})

    try:
        manager.preload_fonts(preload)
    except Exception:
        # Loading hints should never crash runtime.
        pass

    return profile


def _font_path_for_style(profile: Dict[str, Optional[str]], *, mono: bool, bold: bool, italic: bool) -> Optional[str]:
    prefix = "mono" if mono else "ui"
    if bold and italic:
        return profile.get(f"{prefix}_bold_italic_path")
    if bold:
        return profile.get(f"{prefix}_bold_path")
    if italic:
        return profile.get(f"{prefix}_italic_path")
    return profile.get(f"{prefix}_regular_path")


def load_font(
    profile: Optional[Dict[str, Optional[str]]],
    size: int,
    *,
    bold: bool = False,
    italic: bool = False,
    mono: bool = False,
) -> pygame.font.Font:
    """Create a pygame font using resolved runtime profile with safe fallbacks."""
    prof = profile or {}
    path = _font_path_for_style(prof, mono=mono, bold=bold, italic=italic)

    if path and os.path.exists(path):
        try:
            font = pygame.font.Font(path, size)
            if not bold or path == prof.get("ui_bold_path") or path == prof.get("mono_bold_path"):
                pass
            else:
                font.set_bold(True)
            if italic and path not in (prof.get("ui_italic_path"), prof.get("mono_italic_path")):
                font.set_italic(True)
            return font
        except Exception:
            pass

    if mono:
        fallback_name = prof.get("mono_font_name") or "Consolas"
    else:
        fallback_name = prof.get("ui_font_name") or "Segoe UI Symbol"

    return pygame.font.SysFont(str(fallback_name), size, bold=bold, italic=italic)
