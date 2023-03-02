from dash import html
from dash.dependencies import Component


def experimental_component() -> Component:
    return html.P(children="Test Component")
