"""Regression checks for Unicode glyph handling in panel text and font loading."""

import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame

import pygame_ui as pui
from font_support import load_font


def test_load_font_renders_box_chars():
    font = load_font({}, 16)
    surf = font.render("╔═╗", True, (255, 255, 255))
    assert surf.get_width() > 0 and surf.get_height() > 0


def test_panel_fallback_replaces_only_unsupported_glyphs():
    sample = "╔═╗ ⚔️ 💰"

    original_ready = pui._PANEL_FALLBACK_READY
    original_unsupported = set(pui._PANEL_UNSUPPORTED_GLYPHS)
    try:
        pui._PANEL_FALLBACK_READY = True
        pui._PANEL_UNSUPPORTED_GLYPHS = {"╔", "═", "╗", "⚔", "💰"}
        replaced = pui.normalize_panel_text_icons(sample)
        assert replaced == "+=+ [SWORDS] [GOLD]"

        pui._PANEL_UNSUPPORTED_GLYPHS = set()
        preserved = pui.normalize_panel_text_icons(sample)
        assert preserved == "╔═╗ ⚔ 💰"
    finally:
        pui._PANEL_FALLBACK_READY = original_ready
        pui._PANEL_UNSUPPORTED_GLYPHS = original_unsupported


def test_configure_panel_glyph_fallback_marks_ready():
    pui.configure_panel_glyph_fallback({})
    assert pui._PANEL_FALLBACK_READY is True


def test_panel_format_preserves_spacing_for_box_layout():
    message = "╔══╗\n║  LIST  ║\n╚══╝"
    html = pui._format_panel_message(message, "#ffffff", "#cccccc")

    assert "&nbsp;&nbsp;" in html
    assert "╔══╗" in html
    assert "<br>" in html


def test_panel_format_keeps_normal_text_without_nbsp():
    message = "normal text with two spaces: a  b"
    html = pui._format_panel_message(message, "#ffffff", "#cccccc")

    assert "&nbsp;" not in html


def test_box_layout_detector_recognizes_ascii_fallback_boxes():
    ascii_box = "+====+\n| item |\n+====+"
    assert pui._is_box_layout_message(ascii_box) is True


if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    tests = [
        test_load_font_renders_box_chars,
        test_panel_fallback_replaces_only_unsupported_glyphs,
        test_configure_panel_glyph_fallback_marks_ready,
        test_panel_format_preserves_spacing_for_box_layout,
        test_panel_format_keeps_normal_text_without_nbsp,
        test_box_layout_detector_recognizes_ascii_fallback_boxes,
    ]
    for test_fn in tests:
        test_fn()
        print(f"PASS: {test_fn.__name__}")
    print("All unicode glyph fallback tests passed.")
    pygame.quit()
