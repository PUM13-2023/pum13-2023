"""Dashboards controller module."""

from typing import List

from dash import Input, Output, Patch, State, callback
from dash.dependencies import Component

from dashboard.components.dashboards_list_component import generate_list_row


@callback(
    Output({"parent": "dashboards-list", "child": "list-rows"}, "children"),
    State({"parent": "dashboards-list", "child": "list-rows"}, "children"),
    Input("dashboards-add-button", "n_clicks"),
    prevent_initial_call=True,
)
def dashboards_add_button_clicked(children: List[Component], n_clicks: int) -> Patch:
    """Add dashboard to dashboards list.

    Args:
        children (List[Component]): The dashboards list rows.
        n_clicks (int): The amount of times the button was clicked.

    Returns:
        List[Component]: The dashboards list rows with one more row.
    """
    new_index = 0 if not children else children[-1]["props"]["id"]["index"] + 1
    children_patch = Patch()
    children_patch.append(
        generate_list_row(
            (
                new_index,
                [
                    f"Added Dashboard #{new_index + 1}",
                    f"{new_index} days ago",
                    f"{new_index + 1} days ago",
                ],
            )
        )
    )
    return children_patch
