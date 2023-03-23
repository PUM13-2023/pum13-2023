from typing import List

from dash import html
from dash.dependencies import Component


def generate_list_item(content: str) -> Component:
    return html.Span(className="flex-1 border-r-2 pl-2 py-1", children=content)


def generate_list_row(list_row: List[str]) -> Component:
    return html.Div(
        className="flex pl-2 justify-start items-center border-b-2 border-gray-400 text-base",
        children=[
            html.I("analytics", className="material-symbols-rounded text-2xl"),
        ]
        + list(map(generate_list_item, list_row)),
    )


def dashboards_list_component(titles_names: List[str], list_rows: List[List[str]]) -> Component:
    if len(list_rows) > 0 and not all(
        len(titles_names) == len(list_cols) for list_cols in list_rows
    ):
        raise IndexError(
            f"in {__name__}: The amount of titles does not match the amount of list item columns."
        )

    return html.Div(
        className="bg-white overflow-auto",
        children=[
            html.Div(
                className="bg-white sticky top-0 first:pl-8 flex justify-start border-b-2 border-black text-lg",
                children=list(map(generate_list_item, titles_names)),
            ),
            html.Div(
                children=list(map(generate_list_row, list_rows)),
            ),
        ],
    )
