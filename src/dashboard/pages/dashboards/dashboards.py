"""Dashboard page."""

import dash
from dash import html

from dashboard.components import button, dashboards_list_component
from dashboard.models.db import connect_user_db
from dashboard.models.user import login_user
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


def layout() -> html.Div:
    """Create the dashboards page.

    Returns:
        html.Div: The dashboards page.
    """
    test_user = login_user("dashboards-page-test-user")

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
                children=dashboards_list_component(test_user.dashboards, _id="dashboards-list"),
            ),
        ],
    )
