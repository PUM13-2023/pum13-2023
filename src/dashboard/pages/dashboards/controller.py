"""Dashboards controller module."""

from datetime import datetime

from dash import Input, Output, Patch, callback
from flask_login import current_user

from dashboard.components.dashboards_list_component import generate_list_row_contents
from dashboard.components.list_component import generate_list_row
from dashboard.models.user import Dashboard


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
    new_index = len(current_user.dashboards)
    created = datetime.now()
    added_dashboard = Dashboard(name=f"Added Dashboard #{new_index + 1}", created=created)
    current_user.dashboards.append(added_dashboard)
    current_user.save()

    children_patch = Patch()
    children_patch.append(
        generate_list_row(new_index, generate_list_row_contents(created, added_dashboard))
    )
    return children_patch
