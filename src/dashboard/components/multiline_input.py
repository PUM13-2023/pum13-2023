"""A pre-styled multiline input component."""


from dash import dcc, html


def multiline_input(id: str, title: str, description: str) -> html.Div:
    """Pre-styled multiline input.

    Args:
        id (str): id of the multiline input
        title (str): title of the multiline input
        description (str): placeholder of the multiline input

    Returns:
        html.Div: pre-styled multiline input with title and placeholder
    """
    return html.Div(
        className="flex flex-col",
        children=[
            html.P(title, className=""),
            dcc.Textarea(
                id=id,
                draggable=False,
                className="p-3 rounded-md shadow-inner h-[17rem] bg-background",
                placeholder=description,
            ),
        ],
    )
