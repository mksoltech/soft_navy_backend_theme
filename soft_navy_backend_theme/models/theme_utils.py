# -*- coding: utf-8 -*-
# Copyright 2026 MKSOL TECH
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import re


HEX_COLOR_RE = re.compile(r"^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$")


def normalize_hex(color, fallback="#000000"):
    """Return a valid 6-digit hex color or fallback."""
    if not color or not isinstance(color, str):
        return fallback
    color = color.strip()
    if not HEX_COLOR_RE.match(color):
        return fallback
    if len(color) == 4:
        return "#%s%s%s%s%s%s" % (
            color[1], color[1], color[2], color[2], color[3], color[3]
        )
    return color.upper()


def hex_to_rgb(hex_color):
    hex_color = normalize_hex(hex_color).lstrip("#")
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(r, g, b):
    return "#%02X%02X%02X" % (
        max(0, min(255, int(r))),
        max(0, min(255, int(g))),
        max(0, min(255, int(b))),
    )


def darken(hex_color, factor=0.1):
    r, g, b = hex_to_rgb(hex_color)
    return rgb_to_hex(r * (1 - factor), g * (1 - factor), b * (1 - factor))


def lighten(hex_color, factor=0.1):
    r, g, b = hex_to_rgb(hex_color)
    return rgb_to_hex(
        r + (255 - r) * factor,
        g + (255 - g) * factor,
        b + (255 - b) * factor,
    )


def rgba(hex_color, alpha):
    r, g, b = hex_to_rgb(hex_color)
    return "rgba(%d, %d, %d, %.2f)" % (r, g, b, alpha)
