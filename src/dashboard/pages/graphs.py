from collections import OrderedDict

import dash
from dash import get_asset_url, html

from dashboard.components.icon import icon

dash.register_page(__name__, path_template="/dashboards/<dashboard_id>")

# Ordered dict containing the name of the button and its corresponding icon name
# Find the icon names here https://fonts.google.com/icons?icon.set=Material+Symbols
buttons = OrderedDict(
    [("Presentation view", "present_to_all"), ("Share", "share"), ("Add graph", "add")]
)


def add_buttons(button_names: OrderedDict[str, str]) -> list[html.Button]:
    buttons: list[html.Button] = []

    for name, icon_ in button_names.items():
        buttons.append(
            html.Button(
                className="flex items-center mx-2 border-2 p-2 rounded-lg drop-shadow-lg transition ease-in-out hover:text-white hover:bg-[#777df2]",
                children=[icon(icon_, className="mr-2"), html.P(name)],
            )
        )

    return buttons


def layout(dashboard_id=None):
    dashboard_name = f"Dashboard {dashboard_id}"
    """
    TODO
        Use the dashboard_id to query
        information from the database about that specific dashboard
    """

    return html.Div(
        className="flex",
        children=[
            html.Div(
                className="flex w-screen p-5 items-center",
                children=[
                    html.H1(className="text-3xl", children=[dashboard_name]),
                    html.Div(className="flex ml-auto", children=add_buttons(buttons)),
                ],
            )
        ],
    )
