import dash
from dash import html
from dash.dependencies import Component

dash.register_page(__name__, path="/")


def layout() -> Component:
    return html.Div(children=[html.P("Welcome to index")])
