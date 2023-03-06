import dash
from dash import html

dash.register_page(
    __name__, path="/dashboards", name="Dashboards", order=1, visible_in_navbar=True
)


def layout() -> html.Div:
    return html.Div()
