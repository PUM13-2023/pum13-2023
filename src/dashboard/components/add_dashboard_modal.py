"""Modal for add dashboard buttons."""
from dash import dcc, html

from dashboard.components.button import button


def input(id: str, title: str, description: str) -> html.Div:
    """Pre-styled input field.

    Args:
        id (str): Input id
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


def multiline_input(id: str, title: str, description: str) -> html.Div:
    """Pre-styled multiline input.

    Args:
        id (str): id of the multiline input
        title (str): title of the multiline input
        description (str): placeholder of the multiline input

    Returns:
        html.Div: A pre-styled multiline input with a title and placeholder
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


def inputs() -> html.Div:
    """Input container.

    Returns:
        html.Div: Div containing the text inputs
    """
    return html.Div(
        className="flex flex-col px-[5rem] py-5 space-y-4",
        children=[
            html.P("Create dashboard", className="text-3xl"),
            input("dashboard-title", "Dashboard title", "Enter dashboard title..."),
            multiline_input("dashboard-desc", "Description", "Enter dashboard description..."),
        ],
    )


def buttons() -> html.Div:
    """Container for the modal buttons.

    Returns:
        html.Div: A container with buttons for cancel and create dashboard
    """
    return html.Div(
        children=[
            html.Div(
                className="flex bg-menu-back px-[5rem] justify-end h-[5rem] py-3",
                children=[
                    button(
                        id="cancel-btn",
                        icon_name="",
                        text="Cancel",
                        className="bg-none text-white",
                    ),
                    button(
                        id="add-dashboard",
                        icon_name="",
                        text="Create dashboard",
                        className="bg-dark-purple text-white p-5",
                    ),
                ],
            )
        ],
    )


def add_dashboard_modal() -> html.Div:
    """Whole container for the modal.

    Returns:
        html.Div: Contains the inputs and buttons
    """
    return html.Div(
        id="add-dashboard-container",
        className="shadow-md w-[40rem] rounded-md overflow-hidden",
        children=[
            html.Div(
                inputs(),
            ),
            html.Div(buttons()),
        ],
    )
