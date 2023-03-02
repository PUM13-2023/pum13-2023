from dash import html
from dash.dependencies import Component

from dashboard.components.highlight_item import highlight_item

navbar_items = ["Home", "Dashboards", "Shared dashboards" "Logout"]


def generate_navbar_items(item_to_highlight: str = "") -> list[html.P]:
    """
    Returns a list of navbar items with a
    specified name to highlight in the navbar.


    args
    item_to_highlight: Name of the item to mark as highlighted
    """
    return []


def navbar_component(page_name: str = "") -> Component:
    """
    Returns a vertical navbar component
    with a specified highlighted item.
    Empty argument can be passed into this function in order to remove
    highlighted items which is used in subpages
    that aren't correlated to the navbar items

    args
    page_name: Name of the item to be highlighted in the navbar
    """
    return html.Div(
        id="main-navbar",
        className="bg-[#636AF2] justify-center text-left",
        children=[
            html.Div(
                className="inline-block flex-col space-y-2 w-max "
                "[&>a]:px-10 [&>a]:py-5 mt-[3.5rem] "
                "text-white/75 [&>a]:block",
                children=[
                    highlight_item("Home"),
                    html.A("Dashboards", href="Dashboards"),
                    html.A("Shared dashboards", href="Shared Dashboards"),
                ],
            ),
        ],
    )
