"""List component."""

from dash import dcc, html

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


def generate_list_row(index: int, list_row_contents: list[str]) -> dcc.Link:
    """Generate a list row.

    Args:
        index (int): The index of the row.
        list_row_data (list[str]): The contents
        of the row.

    Returns:
        Component: The list row.
    """
    return dcc.Link(
        id={"type": "list-row", "index": index},
        href="/",
        className=(
            "flex pl-2 justify-start items-center border-b-2 border-gray-400"
            " text-base cursor-pointer hover:bg-gray-100"
        ),
        children=[
            icon("analytics", fill=1, size=28),
        ]
        + [generate_row_item(content) for content in list_row_contents],
    )


def generate_list_titles(list_titles: list[str]) -> list[html.Span]:
    """Generate list title elements.

    Args:
        list_titles (list[str]): A list of titles.

    Returns:
        list[html.Span]: A list of title elements.
    """
    return [generate_row_item(title) for title in list_titles]


def generate_list_rows(list_rows: list[list[str]]) -> list[dcc.Link]:
    """Generate list row elements.

    Args:
        list_rows (list[list[str]]): A list of rows.

    Returns:
        list[dcc.Link]: A list of row elements.
    """
    return [generate_list_row(index, row) for index, row in enumerate(list_rows)]


def list_component(list_titles: list[str], list_rows: list[list[str]], _id: str) -> html.Div:
    """Create a list component.

    Args:
        titles_names (list[str]): The titles to display at the top of
        the list.
        list_rows (list[list[str]]): The rows that make up the list
        contents.

    Raises:
        IndexError: If the amount of titles does not match the amount
        of list rows.

    Returns:
        html.Div: A list component.
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
                    "bg-white sticky top-0 first:pl-8 flex justify-start"
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
