import dash
from dash import html

dash.register_page(__name__, path="/dashboards", name="Dashboards", order=1, nav_item=True)


def layout() -> html.Div:
    return html.Div()
