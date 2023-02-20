import dash
from dash import html
from dash.dependencies import Component

from . import controller

from components import test_component

dash.register_page(__name__, path="/")


def layout() -> Component:
    return html.Div(children=[html.H1(children="Index page!"), 
                              test_component()])
