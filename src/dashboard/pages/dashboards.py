"""Dashboard page stub."""
import dash
from dash import html

dash.register_page(
    __name__, path="/dashboards", name="Dashboards", order=1, nav_item=True, icon_name="dashboard"
)


def layout() -> html.Div:
    return html.Div(
        className="flex flex-col mx-4",
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
            html.Div(
                className="bg-white",
                children=[
                    html.Div(
                        className="[&>span]:flex-1 [&>span]:border-r-2 [&>span]:ml-2 flex justify-start border-b-2 border-black text-lg",
                        children=[
                            html.Span("Title", className="pl-6"),
                            html.Span("Last edited at"),
                            html.Span("Created at"),
                        ],
                    ),
                    html.Div(
                        className="[&>span]:flex-1 [&>span]:border-r-2  [&>span]:ml-2 flex justify-start items-center border-b-2 border-gray-400 text-base",
                        children=[
                            html.I("analytics", className="material-symbols-rounded"),
                            html.Span(
                                className="flex items-center",
                                children=[
                                    "Dashboard 1",
                                ],
                            ),
                            html.Span("Today"),
                            html.Span("Yesterday"),
                        ],
                    ),
                ],
            ),
        ],
    )
