"""Button component."""
from typing import Any

from dash import html

from dashboard.components.icon import icon


def button(
    icon_name: str,
    text: str,
    fill: int = 0,
    weight: int = 400,
    grade: int = 0,
    size: int = 16,
    **kwargs: Any,
) -> html.Button:
    """Create a general button containing an icon to the left.

    Args:
        icon_name (str): the name of the icon, for more information see:
            https://fonts.google.com/icons?icon.set=Material+Symbols
        text (str): The text to be displayed inside the button.
        fill (int): Set to 0 for outlined, 1 for filled. Default 0.
        weight (int): Font weight for the icon, range 100-700,
            default 400.
        grade (int): Affects font weight, range -25-200, default 0.
        size (int, optional): The font size in pixels, also sets icon
        size. Defaults to 16
        kwargs (Any): Forwarded to html.Button.

    Returns:
        html.Button: The button.
    """
    class_name = kwargs.pop("className", "")

    return html.Button(
        **kwargs,
        className=(
            f"{class_name} flex bg-white items-center text-[{size}px] px-2 py-1 rounded-lg"
            " drop-shadow-sm hover:drop-shadow-md transition"
        ),
        children=[
            icon(icon_name, fill=fill, weight=weight, grade=grade, size=size + 10),
            html.Span(className="leading-none pl-1", children=text),
        ],
    )
