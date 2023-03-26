from typing import List

from dash import ALL, Input, Output, State, callback, ctx, no_update
from dash.dependencies import Component


@callback(
    Output("search-placeholder", "children"),
    Input({"type": "dashboards-list-row", "index": ALL}, "n_clicks"),
    State({"type": "dashboards-list-row", "index": ALL}, "children"),
)
def dashboards_list_row_clicked(n_clicks: int, children: List[Component]) -> Component:
    if not ctx.triggered_id:
        return no_update
    return children[ctx.triggered_id["index"]][1]["props"]["children"]
