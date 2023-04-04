"""Index page module."""
import dash
from dash import html
from dash.dependencies import Component

dash.register_page(__name__, path="/", name="Home", order=0, nav_item=True, icon_name="home")


def layout() -> Component:
    """Stub layout for index page."""
    return html.Div(children=[html.P("Welcome to index")])
