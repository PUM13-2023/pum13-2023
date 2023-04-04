"""Shared dashboards page."""
import dash
from dash import html

dash.register_page(
    __name__,
    path="/shared-dashboards",
    name="Shared dashboards",
    order=2,
    nav_item=True,
    icon_name="share",
)


def layout() -> html.Div:
    """Stub layout for shared dashboards page."""
    return html.Div()
