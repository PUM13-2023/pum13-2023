"""Dashboard page."""

import dash
from dash import html
from flask_login import current_user

from dashboard.components import button, dashboards_list_component, login_required
from dashboard.models.db import connect_user_db
import dashboard.pages.dashboards.controller  # noqa: F401

dash.register_page(
    __name__,
    path="/dashboards",
    name="Dashboards",
    order=1,
    nav_item=True,
    icon_name="dashboard",
)

connect_user_db()


@login_required
def layout() -> html.Div:
    """Create the dashboards page.

    Returns:
        html.Div: The dashboards page.
    """
    return html.Div(
        className="flex flex-col mx-4 py-4 h-screen max-h-screen",
        children=[
            html.H1(className="text-3xl my-8", children="Dashboards"),
            html.Div(
                id="search-placeholder",
                className=(
                    "bg-white rounded-full min-h-[40px] flex items-center pl-8 text-gray-600"
                ),
                children="Search placeholder...",
            ),
            html.Div(
                className="flex justify-between my-4",
                children=[
                    button(className="bg-white", icon_name="list_alt", text="View"),
                    button(
                        id="dashboards-add-button",
                        n_clicks=0,
                        icon_name="add",
                        text="Add Dashboard",
                    ),
                ],
            ),
            html.Div(
                className="flex grow overflow-hidden",
                children=dashboards_list_component(current_user.dashboards, _id="dashboards-list"),
            ),
        ],
    )
