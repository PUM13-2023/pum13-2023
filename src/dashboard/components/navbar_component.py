from typing import Dict, OrderedDict

import dash
from dash import dcc, html
from dash.dependencies import Component

HIGHLIGHT_STYLE = "border-r-4 border-r-white text-white bg-[#777DF2]"


def generate_navbar_items(
    page_registry: OrderedDict[str, Dict[str, str]], item_to_highlight: str = ""
) -> list[dcc.Link]:
    """
    Returns a list of navbar items with a
    specified name to highlight in the navbar.

    args
    item_to_highlight: Name of the item to mark as highlighted
    """
    navbar_list: list[dcc.Link] = []
    found_highlight_item = False

    for item in page_registry.values():
        if item_to_highlight == "Logout" or item["name"] == item_to_highlight:
            found_highlight_item = True

        class_name = ""
        if item["name"] == item_to_highlight:
            class_name = HIGHLIGHT_STYLE

        navbar_list.append(
            dcc.Link(className=class_name, href=item["path"], children=item["name"])
        )

    if not found_highlight_item:
        return []

    return navbar_list


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
                children=generate_navbar_items(dash.page_registry, page_name),
            ),
        ],
    )
