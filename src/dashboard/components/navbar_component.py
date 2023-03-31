"""Navbar component.

This module implements a navbar component. The navbar generates items
based on Dash's page registry. Pages are by default hidden from the
navbar. To show a page in the navbar, set ``nav_item=True`` when calling
``dash.register_page``. Navbar items can also be explicitly hidden by
setting ``nav_item=False``. The title of the navbar item is set by the
``name`` attribute in the page registry.

Which item is highlighted is automatically updated via a callback.

Todo:
    * Add support for a page registry option to use a different name in
      the navbar.
    * Add logout functionality

"""
from typing import Any, Optional, OrderedDict, TypeAlias

import dash
from dash import Input, Output, callback, dcc, get_asset_url, html
from dash.dcc import Link
from dash.dependencies import Component
from dashboard.components import icon

RegistryItem: TypeAlias = dict[str, Any]
PageRegistry: TypeAlias = OrderedDict[str, RegistryItem]

HIGHLIGHT_STYLE = "border-r-4 mt-2 border-r-white text-white bg-[#5B60A8] "
NON_HIGHLIGHT_STYLE = (
    "mr-1 mt-2 hover:text-white opacity-80 hover:opacity-95 transition ease-in-out "
)


def is_registry_item_visible(item: RegistryItem) -> bool:
    """Return True if item should be visible in the navbar.

    Items are hidden by default, and are only visible if the
    ``nav_item`` attribute is set to True.
    """
    try:
        visible: bool = item["nav_item"]

        return visible
    except KeyError:
        return False


def generate_navbar_page_items(
    page_registry: PageRegistry, item_to_highlight: Optional[str] = None
) -> html.Div:
    """Generate Div of navbar item components based on pages.

    A navbar item can be specified by a path to highlight that item in
    the navbar. By default, no item is highlighted.

    Args:
        page_registry (PageRegistry): Page registry dictionary.
        item_to_highlight (Optional[str]): Path of highlighted item.
    """
    upper_navbar_list: list[dcc.Link] = []

    for item in page_registry.values():
        if not is_registry_item_visible(item):
            continue

        if item["path"] == item_to_highlight:
            class_name = HIGHLIGHT_STYLE
        else:
            class_name = NON_HIGHLIGHT_STYLE

        upper_navbar_list.append(
            dcc.Link(
                href=item["path"],
                className=f"{class_name}",
                children=[
                    html.Div(
                        className="flex items-center space-x-4",
                        children=[
                            html.Img(src=get_asset_url(f'{item["name"].lower()}.svg')),
                            html.P(item["name"]),
                        ],
                    )
                ],
            )
        )
    upper_navbar_div = html.Div(children=upper_navbar_list, className="inline-block flex-col w-max flex"
                "[&>a]:px-5 [&>a]:py-5 mt-[3.5rem] mb-[3.5rem] "
                "text-white/75 [&>a]:block",)
    return upper_navbar_div

def generate_lower_navbar_div():
    """Generates div for the lower part of the navbar
    
    This function generates the lower part of the navbar, this is a div containing
    a list of the diffrent components. Currently a log out button.
    """
    lower_navbar_list: list[dcc.Link] = []

    lower_navbar_list.append(
        dcc.Link(
                href="/login",
                className=NON_HIGHLIGHT_STYLE,
                children=[
                    html.Div(
                        className="flex items-center space-x-4",
                        children=[
                            icon("logout"), #TODO fix font size
                            html.P("Logout"),
                        ],
                    )
                ],
            )
    )
    lower_navbar_div = html.Div(children=lower_navbar_list, className="inline-block flex-col w-max flex "
                "[&>a]:px-5 [&>a]:py-5 mt-[3.5rem] mb-[3.5rem] "
                "text-white/75 [&>a]:block",)
    return lower_navbar_div
    
    
#TODO fix 2 diffrent fuctions. one for page items and one for whacky other stuff
#TODO they should both return 1 div.
#TODO fix all docstrings

def navbar_component() -> Component:
    """Return a vertical navbar component.

    Generates navbar items based on Dash's page registry. Pages are
    included in that navbar on an opt-in basis. Pages with ``nav_item``
    set to true are included. For more information see
    ``is_registry_item_visible``.
    """
    return html.Div(
        id="main-navbar",     
        className="bg-[#4D549B] justify-center text-left flex shadow-md",
        children=[
            dcc.Location(id="url", refresh=False),
            html.Div(
                id="main-navbar-container",
                className="flex flex-col justify-between",
                children=generate_navbar_contents(dash.page_registry),
            ),
        ],
    )

def generate_navbar_contents(page_registry: PageRegistry, item_to_highlight: Optional[str] = None
) -> list[html.Div]:
    """Generate a list containing two divs. First div contains links to all 
    pages, second div contains buttons and toggles.

    Read docstring for generate_navbar_page_items for first div. And #TODO second name

    Args:
        page_registry (PageRegistry): Page registry dictionary.
        item_to_highlight (Optional[str]): Path of highlighted item.
    """
    return [generate_navbar_page_items(page_registry, item_to_highlight),
            generate_lower_navbar_div()] #TODO fix this to button generator
            

@callback(Output("main-navbar-container", "children"), Input("url", "pathname"),prevent_initial_call=True)
def update_navbar(path_name: str) -> list[Component]:
    """Update the selected navbar item based on the current url."""
    return generate_navbar_contents(dash.page_registry, path_name)
