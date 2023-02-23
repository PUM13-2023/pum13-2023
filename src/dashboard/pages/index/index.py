import dash
from dash import html
from dash.dependencies import Component

from dashboard.components import experimental_component

dash.register_page(__name__, path="/")


def layout() -> Component:
    return html.Div(children=[html.H1(children="Index page!"), experimental_component()])
