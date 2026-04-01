"""Shared easing and transition helpers for UI overlays."""


# Unified popup timing profile used across overlays/windows.
UI_OPEN_DUR = 0.24
UI_CLOSE_DUR = 0.18
UI_CONTENT_DUR = 0.20


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
