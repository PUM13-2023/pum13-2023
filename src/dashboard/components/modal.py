"""Module containing functionality related to modals."""
from typing import Optional

from dash import ALL, Input, Output, State, callback, ctx, html
from dash.dependencies import Component

from dashboard.utilities import set_classname


@callback(
    Output({"type": "modal-dialog", "id": ALL}, "open"),
    Output("modal-container", "className"),
    State({"type": "modal-dialog", "id": ALL}, "id"),
    State("modal-container", "className"),
    Input("modal-backdrop", "n_clicks"),
    prevent_initial_call=True,
)
def handle_backdrop_click(
    all_ids: list[str], classname: str, n_clicks: int
) -> tuple[list[bool], str]:
    """Handle a click on the backdrop.

    Args:
        all_ids (list[str]): ids of all modals dialogs in container.
        classname (str): classname of modal container.
        n_clicks (int): number of times the backdrop has been clicked.

    Returns:
        Array with filled False with same length of all_ids parameter,
        The classname for the container.
    """
    return [False] * len(all_ids), set_classname(classname, "hidden", True)


@callback(
    Output({"type": "modal-dialog", "id": ALL}, "open", allow_duplicate=True),
    Output("modal-container", "className", allow_duplicate=True),
    State({"type": "modal-dialog", "id": ALL}, "id"),
    State("modal-container", "className"),
    Input({"type": "modal-dialog", "id": ALL}, "open"),
    prevent_initial_call=True,
)
def open_modal(all_ids: list[str], classname: str, open_: list[bool]) -> tuple[list[bool], str]:
    """Handle open attribute modified on modal dialog.

    Args:
        all_ids (list[str]): ids of all modals dialogs in container.
        classname (str): classname of modal container.
        open_ (list[bool]): id of dialog to open.

    Returns:
        Array of bools indicating which dialog should be open,
        classname of modal container
    """
    opened_id: str | None = ctx.triggered_id
    res: list[bool] = [open_[i] if id_ == opened_id else False for i, id_ in enumerate(all_ids)]

    if any(res):
        return res, set_classname(classname, "hidden", False)

    return res, classname


def modal_container(children: Optional[list[Component]]) -> Component:
    """Create a modal container component.

    Args:
        children (list[Component]): The children of the inner modal.

    Returns:
        A modal container dash component.
    """
    children = [] if children is None else children
    container_classname: str = "z-40 absolute w-screen h-screen top-0 left-0"

    # Check if a child is open, if not hide container.
    for child in children:
        if not getattr(child, "open", True):
            container_classname += " hidden"
            break

    return html.Div(
        id="modal-container",
        children=[
            html.Div(
                id="modal-backdrop",
                n_clicks=0,
                className="z-49 w-full h-full opacity-25 bg-black",
            ),
            html.Div(
                id="modal-dialog-container",
                children=children,
            ),
        ],
        className=container_classname,
    )


def modal_dialog(children: list[Component], id: str, open_: Optional[bool] = False) -> Component:
    """Create a simple modal dialog.

    Args:
        children (list[Component]): Children of the modal dialog.
        open_ (Optional[bool]): Specifies if the modal should be open
        by default.

    Returns:
        A modal dash component.

    Example:
        A simple example showing how a button can be used to open
        a modal dialog::

            @callback(
                Output({"type": "modal-dialog", "id": "<id-of-dialog>"},
                "open", allow_duplicate=True),
                Input("<id-of-button>", "n_clicks"),
                prevent_initial_call=True,
            )
            def open_modal(n_clicks):
                return True  # False can be returned to close it.

    """
    return html.Dialog(
        id={"type": "modal-dialog", "id": id},
        open=open_,
        children=children,
        className="absolute z-50 top-0 left-0 p-0 mx-auto my-auto bottom-0",
    )
