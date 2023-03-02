from dash import html
from dash.dependencies import Component

HIGHLIGHT_CLASSNAME = "border-r-4 border-r-white text-white bg-[#777DF2]"


def highlight_item(name: str) -> Component:
    return html.A(name, className=HIGHLIGHT_CLASSNAME, href=name)
