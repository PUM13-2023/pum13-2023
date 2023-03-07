import dash
from dash import html
from dash.dependencies import Component
from dashboard.components import create_dashboard_menu

dash.register_page(__name__, path="/")


def layout() -> Component:
    return html.Div(
        children=[
            create_dashboard_menu.dashboard_menu()
        ]
    )


