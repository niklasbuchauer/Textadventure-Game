"""Sprite helpers for home-room pixel art assets."""

import os
import pygame

ASSET_DIR = os.path.join(os.path.dirname(__file__), "Room (home) assets")
TILE_SIZE = 16

SHEET_LAYOUTS = {
    "TopDownHouse_DoorsAndWindows.png": (18, 10),
    "TopDownHouse_FloorsAndWalls.png": (18, 9),
    "TopDownHouse_FloorsAndWalls_OpenDoors.png": (8, 3),
    "TopDownHouse_FurnitureState1.png": (13, 18),
    "TopDownHouse_FurnitureState2.png": (13, 18),
    "TopDownHouse_SmallItems.png": (8, 8),
}

_SHEET_CACHE = {}
_TILE_CACHE = {}


def _get_sheet(sheet_name):
    cached = _SHEET_CACHE.get(sheet_name)
    if cached is not None:
        return cached

    path = os.path.join(ASSET_DIR, sheet_name)
    if not os.path.exists(path):
        _SHEET_CACHE[sheet_name] = None
        return None

    try:
        surf = pygame.image.load(path).convert_alpha()
    except Exception:
        try:
            surf = pygame.image.load(path)
        except Exception:
            surf = None
    _SHEET_CACHE[sheet_name] = surf
    return surf


def _meta_key(meta):
    return (
        meta.get("sheet"),
        int(meta.get("x", 0)),
        int(meta.get("y", 0)),
        int(meta.get("w", 1)),
        int(meta.get("h", 1)),
    )


def get_tile_surface(meta):
    if not isinstance(meta, dict):
        return None

    key = _meta_key(meta)
    cached = _TILE_CACHE.get(key)
    if cached is not None:
        return cached

    sheet_name, x, y, w, h = key
    sheet = _get_sheet(sheet_name)
    if sheet is None:
        _TILE_CACHE[key] = None
        return None

    px = x * TILE_SIZE
    py = y * TILE_SIZE
    pw = w * TILE_SIZE
    ph = h * TILE_SIZE
    if px + pw > sheet.get_width() or py + ph > sheet.get_height():
        _TILE_CACHE[key] = None
        return None

    surf = pygame.Surface((pw, ph), pygame.SRCALPHA)
    surf.blit(sheet, (0, 0), pygame.Rect(px, py, pw, ph))
    _TILE_CACHE[key] = surf
    return surf


def _hex_to_rgb(hex_color):
    text = str(hex_color or "").strip()
    if text.startswith("#") and len(text) == 7:
        try:
            return (int(text[1:3], 16), int(text[3:5], 16), int(text[5:7], 16))
        except ValueError:
            return None
    return None


def choose_sprite_meta(item_def, placed=None):
    if not isinstance(item_def, dict):
        return None

    meta = item_def.get("sprite")
    if not isinstance(meta, dict):
        return None

    placed = placed or {}

    skin = placed.get("skin")
    if skin:
        skin_variants = item_def.get("skin_variants", {})
        if isinstance(skin_variants, dict) and isinstance(skin_variants.get(skin), dict):
            meta = skin_variants[skin]

    texture = placed.get("texture")
    if texture:
        texture_variants = item_def.get("texture_variants", {})
        if isinstance(texture_variants, dict) and isinstance(texture_variants.get(texture), dict):
            meta = texture_variants[texture]

    return meta


def blit_home_item_sprite(target, item_def, placed, rect):
    meta = choose_sprite_meta(item_def, placed)
    base = get_tile_surface(meta)
    if base is None:
        return False

    scaled = pygame.transform.smoothscale(base, (max(1, rect.width), max(1, rect.height)))

    tint_rgb = _hex_to_rgb((placed or {}).get("tint"))
    if tint_rgb:
        tint_layer = pygame.Surface(scaled.get_size(), pygame.SRCALPHA)
        tint_layer.fill((tint_rgb[0], tint_rgb[1], tint_rgb[2], 255))
        scaled.blit(tint_layer, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    target.blit(scaled, rect.topleft)
    return True
