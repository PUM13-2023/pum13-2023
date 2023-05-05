"""Modal for add dashboard buttons."""
from dash import html

from dashboard.components import modal
from dashboard.components.button import button
from dashboard.components.multiline_input import multiline_input
from dashboard.components.text_input import text_input


def generate_inputs() -> html.Div:
    """Input container.

    Returns:
        html.Div: Div containing the text inputs
    """
    return html.Div(
        className="flex flex-col px-[5rem] py-5 space-y-4",
        children=[
            html.P("Create dashboard", className="text-3xl"),
            text_input("dashboard-title", "Dashboard title", "Enter dashboard title..."),
            multiline_input("dashboard-desc", "Description", "Enter dashboard description..."),
        ],
    )


def generate_buttons() -> html.Div:
    """Container for the modal buttons.

    Returns:
        html.Div: Container with buttons for cancel and create
                  dashboard
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

    This is the function used for the create dashboard modal.
    If you want to use this predefined modal component create
    a callback that modifies the add-dashboard-dialog open
    property.

    Example:
        @callback(
            Output({"type": "modal-dialog",
                    "id": "add-dashboard-dialog"},
                    "open", allow_duplicate=True),
            Input("some_input", "property"),
            prevent_initial_call=True,
        )

    Returns:
        html.Div: Contains the inputs and buttons
    """
    return modal.modal_container(
        children=[
            modal.modal_dialog(
                id="add-dashboard-dialog",
                children=[
                    html.Div(
                        id="add-dashboard-container",
                        className="shadow-md w-[40rem] rounded-md overflow-hidden",
                        children=[
                            html.Div(
                                generate_inputs(),
                            ),
                            generate_buttons(),
                        ],
                    )
                ],
            )
        ]
    )
