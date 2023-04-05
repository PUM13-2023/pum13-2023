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
from dash import Input, Output, State, callback, dcc, html
from dash.dependencies import Component

from dashboard.components.icon import icon

RegistryItem: TypeAlias = dict[str, Any]
PageRegistry: TypeAlias = OrderedDict[str, RegistryItem]

HIGHLIGHT_STYLE = "border-r-4 mt-2 border-r-white text-white bg-[#777df2]/30 "
NON_HIGHLIGHT_STYLE = (
    "mr-1 mt-2 hover:text-white opacity-80 hover:opacity-90 transition ease-in-out"
)
NAVBAR_ICON_SIZE: int = 40


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


def generate_upper_navbar_list(
    page_registry: PageRegistry, item_to_highlight: Optional[str] = None
) -> list[dcc.Link]:
    """Generate list of navbar item components based on pages.

    This list is used on the upper part of the navbar. A navbar item can
    be specified by a path to highlight that item in the navbar. By
    default, no item is highlighted. This is implemented in an upper_
    navbar_div

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
            generate_navbar_link(item["path"], item["name"], class_name, item["icon_name"])
        )

    return upper_navbar_list


def generate_navbar_link(path: str, name: str, class_name: str, icon_name: str) -> dcc.Link:
    """Generate a dcc.Link.

    Helper function to generate a navbar link.

    Args:
        path (str): Used to set where the link should direct you to.
        name (str): Used to set text visible on website
        class_name (str): Tailwind CSS for the link.
        icon_name (str): What google font icon should be used.
    """
    return dcc.Link(
        id=f"{name}-button-navbar",
        href=path,
        className=class_name,
        children=[
            html.Div(
                className="flex items-center space-x-4",
                children=[
                    icon(icon_name, size=NAVBAR_ICON_SIZE, fill=1),
                    html.P(name),
                ],
            )
        ],
    )


def generate_lower_navbar_list() -> list[dcc.Link]:
    """Generates list for the lower part of the navbar.

    This function generates the lower part of the navbar, this is a list
    to be used in the lower navbar div.
    """
    lower_navbar_list: list[dcc.Link] = [
        generate_navbar_link("/login", "Logout", NON_HIGHLIGHT_STYLE, "logout")
    ]

    return lower_navbar_list


def navbar_component() -> Component:
    """Return a vertical navbar component.

    Generates navbar items based on Dash's page registry. Pages are
    included in that navbar on an opt-in basis. Pages with ``nav_item``
    set to true are included. For more information see
    ``is_registry_item_visible``.
    """
    return html.Div(
        id="main-navbar",
        className="bg-[#2f3273] justify-center text-left flex shadow-md hidden",
        children=[
            dcc.Location(id="url", refresh=False),
            html.Div(
                id="main-navbar-container",
                className="flex flex-col justify-between",
                children=generate_navbar_contents(dash.page_registry),
            ),
        ],
    )


def generate_navbar_contents(
    page_registry: PageRegistry, item_to_highlight: Optional[str] = None
) -> list[html.Div]:
    """Generate a list containing two divs.

    First div contains links to all pages, second div contains logout
    button and will in future conatin settings etc.
    Read docstring for generate_upper_navbar_list for first div and read
    generate_lower_navbar_list for the second div.

    Args:
        page_registry (PageRegistry): Page registry dictionary.
        item_to_highlight (Optional[str]): Path of highlighted item.
    """
    upper_navbar_div = html.Div(
        id="upper-navbar-container",
        children=generate_upper_navbar_list(page_registry, item_to_highlight),
        className="inline-block flex-col w-max flex "
        "[&>a]:px-5 [&>a]:py-5 mt-[3.5rem] mb-[3.5rem] "
        "text-white/75 [&>a]:block",
    )
    lower_navbar_div = html.Div(
        id="lower-navbar-container",
        children=generate_lower_navbar_list(),
        className="inline-block flex-col w-max flex "
        "[&>a]:px-5 [&>a]:py-5 mt-[3.5rem] mb-[3.5rem] "
        "text-white/75 [&>a]:block",
    )
    return [upper_navbar_div, lower_navbar_div]


@callback(
    Output("upper-navbar-container", "children"),
    Input("url", "pathname"),
    prevent_initial_call=True,
)
def update_navbar(path_name: str) -> list[dcc.Link]:
    """Update the selected navbar item based on the current url."""
    return generate_upper_navbar_list(dash.page_registry, path_name)


@callback(
    Output("main-navbar", "className"), Input("url", "pathname"), State("main-navbar", "className")
)
def show_navbar(path_name: str, class_name: str) -> str:
    """Update the selected navbar item based on the current url."""
    if path_name.startswith("/login"):
        return class_name + (" hidden" if "hidden" not in class_name else "")
    else:
        return class_name.replace(" hidden", "")
