from typing import List

from dash import ALL, Input, Output, State, callback, ctx
from dash.dependencies import Component


@callback(
    Output("search-placeholder", "children"),
    Input({"type": "dashboards-list-row", "index": ALL}, "n_clicks"),
    State({"type": "dashboards-list-row", "index": ALL}, "children"),
)
def dashboards_list_row_clicked(n_clicks: int, children: List[Component]) -> Component:
    return children[ctx.triggered_id["index"]][1]["props"]["children"]
