import dash
from dash import html

dash.register_page(
    __name__, path="/shared-dashboards", name="Shared dashboards", order=2, visible_in_navbar=True
)


def layout() -> html.Div:
    return html.Div()
