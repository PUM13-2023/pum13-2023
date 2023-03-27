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
"""

from typing import Any, Optional, OrderedDict, TypeAlias

import dash
from dash import Input, Output, callback, dcc, html
from dash.dependencies import Component

RegistryItem: TypeAlias = dict[str, Any]
PageRegistry: TypeAlias = OrderedDict[str, RegistryItem]

HIGHLIGHT_STYLE = "border-r-4 border-r-white text-white bg-[#777DF2]"
NON_HIGHLIGHT_STYLE = "mr-1"


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


def generate_navbar_items(
    page_registry: PageRegistry, item_to_highlight: Optional[str] = None
) -> list[dcc.Link]:
    """Generate list of navbar item components.

    A navbar item can be specified by a path to highlight that item in
    the navbar. By default no item is highlighted.

    Args:
        page_registry (PageRegistry): Page registry dictionary.
        item_to_highlight (Optional[str]): Path of highlighted item.
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
    """Return a vertical navbar component.

    Generates navbar items based on Dash's page registry. Pages are
    included in that navbar on an opt-in basis. Pages with ``nav_item``
    set to true are included. For more information see
    ``is_registry_item_visible``.
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
    """Update the selected navbar item based on the current url."""
    return generate_navbar_items(dash.page_registry, path_name)
