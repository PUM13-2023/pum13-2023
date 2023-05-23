"""A pre-styled text input component."""
from typing import Any

from dash import dcc, html


def text_input(title: str, description: str, **kwargs: Any) -> html.Div:
    """Pre-styled text input field.

    Args:
        title (str): input title
        description (str): placeholder of the input
        kwargs (Any): Forwarded to dcc.Input.

    Returns:
        html.Div: A pre-styled input with a title and placeholder
    """
    return html.Div(
        className="flex flex-col",
        children=[
            html.Label(title),
            dcc.Input(
                **kwargs,
                className="p-3 rounded-md shadow-inner bg-background",
                placeholder=description,
            ),
        ],
    )
