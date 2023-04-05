"""Dashboard page stub."""
import dash
from dash import html

dash.register_page(
    __name__, path="/dashboards", name="Dashboards", order=1, nav_item=True, icon_name="dashboard"
)


def layout() -> html.Div:
    """Stub layout for dashboard page."""
    return html.Div()
