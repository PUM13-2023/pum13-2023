"""Index controller module.

Callbacks to the index page.
Callbacks to toggle add dashboard modal
and submitting a new dashboard.
"""

from dash import Input, Output, State, callback, ctx

from dashboard.models.user import add_dashboard

input_css = "p-3 rounded-md shadow-inner bg-background "


@callback(
    Output({"type": "modal-dialog", "id": "add-dashboard-dialog"}, "open", allow_duplicate=True),
    Input("create-dashboard-btn", "n_clicks"),
    Input("create-dashboard-btn-carousel", "n_clicks"),
    Input("cancel-btn", "n_clicks"),
    prevent_initial_call=True,
)
def toggle_create_dashboard(create_btn: int, create_btn_2: int, cancel_btn: int) -> bool:
    """Toggles the create dashboard modal.

    Args:
        create_btn (int): create dashboard button main
        create_btn_2 (int): create dashboard button carousel
        cancel_btn (int): cancel button clicks

    Returns:
        bool: value to toggle modal
    """
    if "cancel-btn" == ctx.triggered_id:
        return False
    return True


@callback(
    Output({"type": "modal-dialog", "id": "add-dashboard-dialog"}, "open", allow_duplicate=True),
    Output("title", "on"),
    Output("desc", "on"),
    Input("add-dashboard", "n_clicks"),
    State("dashboard-title", "value"),
    State("dashboard-desc", "value"),
    prevent_initial_call=True,
)
def add_dashboard_db(n_clicks: int, title: str, desc: str) -> tuple[bool, bool, bool]:
    """Callback to add a new dashboard.

    Args:
        n_clicks (int): n_clicks for the button
        title (str): Dashboard title
        desc (str): Dashboard description

    Returns:
        tuple[bool, bool, bool]: toggle modal bool, empty title bool,
                                 empty desc bool
    """
    # Dash callback gives warnings if you pass bools to value but works
    empty_title = False
    empty_desc = False
    open = True

    if title is None or not title:
        empty_title = True

    if desc is None or not desc:
        empty_desc = True

    if desc and title:
        open = False
        add_dashboard(title, desc)

    return open, empty_title, empty_desc


@callback(
    Output("dashboard-title", "className"),
    Output("dashboard-desc", "className"),
    Output("dashboard-title", "placeholder"),
    Output("dashboard-desc", "placeholder"),
    Input("title", "on"),
    Input("desc", "on"),
    prevent_initial_call=True,
)
def display_error(title_err: bool, desc_err: bool) -> tuple[str, str, str, str]:
    """Callback to display error if title or description is empty.

    Args:
        title_err (bool): Title empty or not
        desc_err (bool): Description empty or not

    Returns:
        tuple[str, str, str , str]: title, desc, title placeholder,
                                    desc placeholder
    """
    title = [input_css, ""]
    desc = [input_css, ""]

    if title_err:
        title[0] += "bg-red-100"
        title[1] = "Title cannot be empty"

    if desc_err:
        desc[0] += "bg-red-100 h-[17rem]"
        desc[1] = "Description cannot be empty"
    else:
        desc[0] += "h-[17rem]"

    return title[0], desc[0], title[1], desc[1]
