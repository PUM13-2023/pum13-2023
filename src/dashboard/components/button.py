"""Button component."""
from typing import Any, TypedDict

from dash import html

from dashboard.components.icon import icon


class IconKWArgs(TypedDict, total=False):
    """Class for typing icon kwargs passed to the button component."""

    fill: int
    weight: int
    grade: int


def button(
    icon_name: str,
    text: str,
    size: int = 16,
    icon_kwargs: IconKWArgs | None = None,
    **kwargs: Any,
) -> html.Button:
    """Create a general button containing an icon to the left.

    Args:
        icon_name (str): the name of the icon, for more information see:
            https://fonts.google.com/icons?icon.set=Material+Symbols
        text (str): The text to be displayed inside the button.
        size (int, optional): The font size in pixels, also sets icon
            size to size + 10. Defaults to 16
        icon_kwargs (IconKWArgs, optional): Forwarded to icon. For more
            information see the icon component docstring.
        kwargs (Any): Forwarded to html.Button.

    Returns:
        html.Button: The button.
    """
    class_name = kwargs.pop("className", "")
    _icon_kwargs: IconKWArgs = icon_kwargs if icon_kwargs else {}

    return html.Button(
        **kwargs,
        className=(
            f"{class_name} flex bg-white items-center text-[{size}px] px-2 py-1 rounded-lg"
            " drop-shadow-sm hover:drop-shadow-md transition"
        ),
        children=[
            icon(icon_name, size=size + 10, **_icon_kwargs),
            html.Span(className="leading-none pl-1", children=text),
        ],
    )
