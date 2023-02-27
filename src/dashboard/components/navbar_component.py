from dash import html
from dash.dependencies import Component
from dashboard.components.highlight_item import highlight_item


def navbar_component() -> Component:
    return (
        html.Div(
            className='bg-[#636AF2] justify-center text-left',
            children=[
                html.Div(
                    className='inline-block flex-col space-y-2 w-max [&>p]:px-10 [&>p]:py-5',
                    children=[
                        highlight_item('Home'),
                        html.P('Dashboards'),
                        highlight_item('TEST'),
                        html.P('Shared dashboards')]

                ),
            ]
        )
    )
