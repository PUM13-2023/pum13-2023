import dash
from dash import html
from dash.dependencies import Component

from dashboard.components.navbar_component import navbar_component

dash.register_page(__name__, path="/")


def layout() -> Component:
    return html.Div(
        className="flex flex-inline",
        children=[
            navbar_component("Home"),
        ],
    )
