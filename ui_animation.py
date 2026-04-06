"""Shared easing and transition helpers for UI overlays."""

import math


# Unified popup timing profile used across overlays/windows.
# Matches the Journal window timing so all book-style UI feels consistent.
UI_OPEN_DUR = 0.38
UI_CLOSE_DUR = 0.26
UI_CONTENT_DUR = 0.30


def clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


def ease_out_cubic(t: float) -> float:
    t = clamp01(t)
    return 1.0 - (1.0 - t) ** 3


def ease_in_out_cubic(t: float) -> float:
    t = clamp01(t)
    if t < 0.5:
        return 4.0 * t * t * t
    return 1.0 - ((-2.0 * t + 2.0) ** 3) / 2.0


def ease_out_quad(t: float) -> float:
    t = clamp01(t)
    return 1.0 - (1.0 - t) * (1.0 - t)


def ease_out_back(t: float) -> float:
    t = clamp01(t)
    c1 = 1.70158
    c3 = c1 + 1.0
    return 1.0 + c3 * (t - 1.0) ** 3 + c1 * (t - 1.0) ** 2


def ease_in_out_sine(t: float) -> float:
    t = clamp01(t)
    return -(math.cos(math.pi * t) - 1.0) / 2.0
