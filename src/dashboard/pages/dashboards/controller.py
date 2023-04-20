"""Dashboards controller module."""

from datetime import datetime

from dash import Input, Output, Patch, callback

from dashboard.components.dashboards_list_component import generate_list_row_contents
from dashboard.components.list_component import generate_list_row
from dashboard.models.user import Dashboard, login_user


@callback(
    Output({"parent": "dashboards-list", "child": "list-rows"}, "children"),
    Input("dashboards-add-button", "n_clicks"),
    prevent_initial_call=True,
)
def dashboards_add_button_clicked(n_clicks: int) -> Patch:
    """Add dashboard to dashboards list.

    Args:
        n_clicks (int): The amount of times the button was clicked.

    Returns:
        List[Component]: The dashboards list rows with one more row.
    """
    test_user = login_user("dashboards-page-test-user")
    new_index = len(test_user.dashboards)
    added_dashboard = Dashboard(name=f"Added Dashboard #{new_index + 1}", created=datetime.now())
    test_user.dashboards.append(added_dashboard)
    test_user.save()

    children_patch = Patch()
    children_patch.append(
        generate_list_row((new_index, generate_list_row_contents(added_dashboard)))
    )
    return children_patch
