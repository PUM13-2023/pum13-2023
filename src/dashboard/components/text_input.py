"""A pre-styled text input component."""

from dash import dcc, html


def text_input(id: str, title: str, description: str) -> html.Div:
    """Pre-styled text input field.

    Args:
        id (str): input id
        title (str): input title
        description (str): placeholder of the input

    Returns:
        html.Div: A pre-styled input with a title and placeholder
    """
    return html.Div(
        className="flex flex-col",
        children=[
            html.P(title, className=""),
            dcc.Input(
                id=id,
                className="p-3 rounded-md shadow-inner bg-background",
                placeholder=description,
            ),
        ],
    )
