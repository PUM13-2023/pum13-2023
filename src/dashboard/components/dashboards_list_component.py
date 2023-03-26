from typing import List, Tuple

from dash import html
from dash.dependencies import Component


def generate_row_item(content: str) -> Component:
    return html.Span(className="flex-1 border-r-2 pl-2 py-1", children=content)


def generate_list_row(list_row_data: Tuple[int, List[str]]) -> Component:
    index = list_row_data[0]
    list_row = list_row_data[1]
    return html.Div(
        id={"type": "dashboards-list-row", "index": index},
        n_clicks=0,
        className="flex pl-2 justify-start items-center border-b-2 border-gray-400 text-base cursor-pointer hover:bg-gray-200",
        children=[
            html.I("analytics", className="material-symbols-rounded text-2xl"),
        ]
        + list(map(generate_row_item, list_row)),
    )


def dashboards_list_component(
    titles_names: List[str],
    list_rows: List[List[str]],
) -> Component:
    if len(list_rows) > 0 and not all(
        len(titles_names) == len(list_row) for list_row in list_rows
    ):
        raise IndexError(
            f"in {__name__}: The amount of titles does not match the amount of list item columns."
        )

    return html.Div(
        className="bg-white overflow-auto",
        children=[
            html.Div(
                className="bg-white sticky top-0 first:pl-8 flex justify-start border-b-2 border-black text-lg",
                children=list(map(generate_row_item, titles_names)),
            ),
            html.Div(
                children=list(map(generate_list_row, enumerate(list_rows))),
            ),
        ],
    )
