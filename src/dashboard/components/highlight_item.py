from dash import html
from dash.dependencies import Component


def highlight_item(name: str) -> Component:
    return (
        html.P(
            name,
            className='border-r-4 border-r-white text-white bg-[#777DF2]'
        )
    )
