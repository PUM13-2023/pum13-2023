import dash
from dash import html
from dash.dependencies import Component

dash.register_page(__name__, path="/")


def layout() -> Component:
    return html.H1(children="Index page!")
