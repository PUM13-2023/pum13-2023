"""Material icon component.

Module for including material icons easily. Supports icon variations.
"""
from typing import Any

from dash import html
from dash.dependencies import Component


def icon_style(fill: int, weight: int, grade: int, size: int) -> dict[str, str]:
    """Return the style dictionary for an icon component.

    The style dictionary contains settings for font variations.

    Args:
        fill (int): Set to 0 for outlined, 1 for filled.
        weight (int): Font weight for the icon, range 100-700.
        grade (int): Affects font weight, range -25-200.
        size (int): Font size in pixels, values 20, 24, 40, 48.
    """
    return {
        "fontVariationSettings": f"'FILL' {fill}, 'wght' {weight}, 'GRAD' {grade}, 'opsz' {size}"
    }


def icon(
    icon_name: str, fill: int = 0, weight: int = 400, grade: int = 0, size: int = 48, **kwargs: Any
) -> Component:
    """Return an icon component.

    Args:
        icon_name (str): the name of the icon, for more information see:
            https://fonts.google.com/icons?icon.set=Material+Symbols
        fill (int): Set to 0 for outlined, 1 for filled. Default 0.
        weight (int): Font weight for the icon, range 100-700,
            default 400.
        grade (int): Affects font weight, range -25-200, default 0.
        size (int): Font size in pixels, values 20, 24, 40, 48.
            Default 48.
        kwargs (Any): Forwarded to html.Span.

    Examples:
        Using filled icons::

            icon("home", fill=1)

        Setting icon color::

            icon("home", className="text-pink-500")
    """
    class_name = kwargs.pop("className", "")
    class_name += " material-symbols-outlined"

    return html.Span(
        className=class_name,
        style=icon_style(fill, weight, grade, size),
        children=icon_name,
        **kwargs,
    )
