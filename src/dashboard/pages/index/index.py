import dash
from dash import html
from dash.dependencies import Component

dash.register_page(__name__, path="/")

default_style = "bg-[#d2d2d2] transition duration-500 ease-in-out"


def layout() -> Component:
    return html.Div()


@dash.callback()
def toggle_create_dashboard_menu(n_clicks: int) -> str:
    return ""
