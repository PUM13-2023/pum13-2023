from dash import html, dcc
from dash.dependencies import Component


def navbar_component() -> Component:
    return (
        html.Div(className='navbar',
            children=[
                html.H1("NAVBAR")
            ]
        )
    )
