"""Dashboards list component."""

from typing import Dict, List, Tuple

from dash import html
from dash.dependencies import Component

from dashboard.components.icon import icon


def generate_row_item(content: str) -> html.Span:
    """Generate a list row item.

    Args:
        content (str): The content to display inside the row item.

    Returns:
        Component: The list row item.
    """
    return html.Span(
        className=(
            "last:border-r-0 flex-1 border-r-2 pl-2 py-1 text-ellipsis overflow-hidden"
            " whitespace-nowrap"
        ),
        children=content,
    )


def generate_list_row(list_row_data: Tuple[int, List[str]]) -> html.Div:
    """Generate a list row.

    Args:
        list_row_data (Tuple[int, List[str]]): The row index and
        content of the row.

    Returns:
        Component: The list row.
    """
    index = list_row_data[0]
    list_row = list_row_data[1]
    return html.Div(
        id={"type": "dashboards-list-row", "index": index},
        n_clicks=0,
        className=(
            "flex pl-2 justify-start items-center border-b-2 border-gray-400"
            " text-base cursor-pointer hover:bg-gray-100"
        ),
        children=[icon("analytics", fill=1, size=28)] + list(map(generate_row_item, list_row)),
    )


def generate_list_titles(list_titles: List[str]) -> List[html.Span]:
    """Generate list title elements.

    Args:
        list_titles (List[str]): A list of titles.

    Returns:
        List[html.Div]: A list of title elements.
    """
    return list(map(generate_row_item, list_titles))


def generate_list_rows(list_rows: List[List[str]]) -> list[html.Div]:
    """Generate list row elements.

    Args:
        list_rows (List[List[str]]): A list of rows.

    Returns:
        list[html.Div]: A list of row elements.
    """
    return list(map(generate_list_row, enumerate(list_rows)))


def dashboards_list_component(
    list_titles: List[str],
    list_rows: List[List[str]],
    _id: (str | Dict[str, str]) = "",
) -> Component:
    """Create the dashboards list component.

    Args:
        titles_names (List[str]): The titles to display at the top of
        the list.
        list_rows (List[List[str]]): The rows that make up the list
        contents.

    Raises:
        IndexError: If the amount of titles does not match the amount
        of list rows.

    Returns:
        Component: The dashboards list component.
    """
    if len(list_rows) > 0 and not all(len(list_titles) == len(list_row) for list_row in list_rows):
        raise IndexError(
            f"in {__name__}: The amount of list titles does not match the amount of list rows."
        )

    return html.Div(
        id=_id,
        className="bg-white overflow-auto grow drop-shadow-sm rounded",
        children=[
            html.Div(
                className=(
                    "bg-white sticky top-0 first:pl-9 flex justify-start"
                    " border-b-2 border-black text-lg"
                ),
                children=generate_list_titles(list_titles),
            ),
            html.Div(
                id={"parent": _id, "child": "list-rows"},
                className="w-full",
                children=generate_list_rows(list_rows),
            ),
        ],
    )
