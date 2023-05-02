"""Index controller module.

This module is intented to contain callbacks used in the index page. As
of now it is just a stub.
"""
from datetime import datetime

from dash import ALL, Input, Output, State, callback, ctx

from dashboard.models.user import Dashboard, login_user

input_css = "p-3 rounded-md shadow-inner bg-background "


@callback(
    Output({"type": "modal-dialog", "id": "add-dashboard-dialog"}, "open", allow_duplicate=True),
    Input("create-dashboard-btn", "n_clicks"),
    Input("cancel-btn", "n_clicks"),
    prevent_initial_call=True,
)
def toggle_create_dashboard(create_btn: int, cancel_btn: int) -> bool:
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
def add_dashboard_db(n_clicks: int, title: str, desc: str) -> bool | bool | bool:
    """TODO
        * Add empty title and desc error
        * Remove invalid characters
        * Add max length

    Args:
        n_clicks (int): _description_
        title (str): _description_
        desc (str): _description_

    Returns:
        _type_: _description_
    """
    # Dash callback gives warnings if you pass bools to value but works
    empty_title = False
    empty_desc = False
    valid = False

    if title is None:
        empty_title = True

    if desc is None:
        empty_desc = True

    if desc and title:
        valid = True
        add_dashboard(title, desc)

    return not valid, empty_title, empty_desc


@callback(
    Output("dashboard-title", "className"),
    Output("dashboard-desc", "className"),
    Output("dashboard-title", "placeholder"),
    Output("dashboard-desc", "placeholder"),
    Input("title", "on"),
    Input("desc", "on"),
    prevent_initial_call=True,
)
def display_error(title_err: bool, desc_err: bool) -> str | str | str | str:
    title = [input_css, ""]
    desc = [input_css, ""]
    print(desc_err)
    if title_err:
        title[0] += "bg-red-100"
        title[1] = "Title cannot be empty"

    if desc_err:
        desc[0] += "bg-red-100 h-[17rem]"
        desc[1] = "Description cannot be empty"
    else:
        desc[0] += "h-[17rem]"

    return title[0], desc[0], title[1], desc[1]


def add_dashboard(name: str, desc: str) -> None:
    test_user = login_user("dashboards-page-test-user")
    added_dashboard = Dashboard(name=name, description=desc, created=datetime.now())
    test_user.dashboards.append(added_dashboard)
    test_user.save()
