from typing import Dict, Optional, OrderedDict

import dash
from dash import Input, Output, callback, dcc, html
from dash.dependencies import Component

HIGHLIGHT_STYLE = "border-r-4 border-r-white text-white bg-[#777DF2]"
NON_HIGHLIGHT_STYLE = "mr-1"


def is_registry_item_visible(item):
    try:
        return item["nav_item"]
    except KeyError:
        return False


def generate_navbar_items(
    page_registry: OrderedDict[str, Dict[str, str]], item_to_highlight: Optional[str] = None
) -> list[dcc.Link]:
    """
    Returns a list of navbar items with a
    specified name to highlight in the navbar.

    args
    item_to_highlight: Name of the item to mark as highlighted
    """
    navbar_list: list[dcc.Link] = []

    for item in page_registry.values():
        if not is_registry_item_visible(item):
            continue

        if item["path"] == item_to_highlight:
            class_name = HIGHLIGHT_STYLE
        else:
            class_name = NON_HIGHLIGHT_STYLE

        navbar_list.append(
            dcc.Link(href=item["path"], children=item["name"], className=class_name)
        )

    return navbar_list


def navbar_component() -> Component:
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
            dcc.Location(id="url", refresh=False),
            html.Div(
                id="main-navbar-container",
                className="inline-block flex-col space-y-2 w-max "
                "[&>a]:px-10 [&>a]:py-5 mt-[3.5rem] "
                "text-white/75 [&>a]:block",
                children=generate_navbar_items(dash.page_registry),
            ),
        ],
    )


@callback(Output("main-navbar-container", "children"), Input("url", "pathname"))
def update_navbar(path_name: str) -> list[Component]:
    return generate_navbar_items(dash.page_registry, path_name)
