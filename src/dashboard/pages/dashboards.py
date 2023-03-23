"""Dashboard page stub."""
import dash
from dash import html

from dashboard.components import dashboards_list_component

dash.register_page(
    __name__, path="/dashboards", name="Dashboards", order=1, nav_item=True, icon_name="dashboard"
)


def layout() -> html.Div:
    return html.Div(
        className="flex flex-col mx-4 max-h-screen",
        children=[
            html.H1(className="text-3xl my-8", children="Dashboards"),
            html.Div(
                className="bg-white rounded-full h-10 flex items-center pl-8 text-gray-600",
                children="Search placeholder...",
            ),
            html.Div(
                className="flex justify-between my-4",
                children=[
                    html.Button(className="bg-white", children="View"),
                    html.Button(className="bg-white", children="Add Dashboard"),
                ],
            ),
            dashboards_list_component(
                ["Title", "Last edited at", "Created at"],
                [
                    ["Dashboard 1", "Today", "Yesterday"],
                    ["Dashboard 2", "3 days ago", "2 days ago"],
                    ["Dashboard 2", "1 year ago", "5 years ago"],
                ]
                * 15,
            ),
        ],
    )
