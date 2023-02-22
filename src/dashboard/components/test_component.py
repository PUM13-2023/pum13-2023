from dash import html
from dash.dependencies import Component


def test_component() -> Component:
    return html.P(children="Test Component")
