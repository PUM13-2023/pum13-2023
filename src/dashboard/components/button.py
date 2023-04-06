"""Button component."""
from typing import Dict

from dash import html

from dashboard.components.icon import icon


def button(
    icon_name: str,
    text: str,
    fill: int = 0,
    weight: int = 400,
    grade: int = 0,
    size: int = 16,
    _id: str | Dict[str, str] = "",
) -> html.Button:
    """Create a general button containing an icon to the left.

    Args:
        icon_name (str): The name of the icon to use.
        text (str): The text to be displayed inside the button.
        size (int): The font size in pixels, also sets icon size.

    Returns:
        html.Button: The button.
    """
    return html.Button(
        id=_id,
        className=(
            f"flex bg-white items-center text-[{size}px] px-2 py-1 rounded-lg drop-shadow-sm"
            " hover:drop-shadow-md transition"
        ),
        children=[
            icon(icon_name, fill=fill, weight=weight, grade=grade, size=size + 10),
            html.Span(className="leading-none pl-1", children=text),
        ],
    )
