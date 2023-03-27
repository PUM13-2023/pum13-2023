import dash
from dash import html

dash.register_page(
    __name__, path="/shared-dashboards", name="Shared dashboards", order=2, nav_item=True
)


def layout() -> html.Div:
    return html.Div()
