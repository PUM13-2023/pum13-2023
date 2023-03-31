import dash
from dash import html, get_asset_url

dash.register_page(__name__, path_template="/dashboards/<dashboard_id>")

buttons = [
    "Presentation view",
    "Share",
    "Add graph"
]

def search_bar():
    bar = html.Div(
        className="flex",
        children=[
            html.Div(
                className="w-40",
                children=["search"]
            ),
            html.Div(
                "bar"
            )
        ]
    )
    return bar

def add_buttons(button_names: list[str]) -> list[html.Button]:
    buttons: list[html.Button] = []

    for item_name in button_names:
        buttons.append(
            html.Button(
            className="flex items-center mx-2 border-2 border-black p-2 rounded-lg ripple",
                children=[
                    html.Img(className="w-[24px] h-[24px] mr-2",src=get_asset_url("share.svg")),
                    html.P(item_name)
                ]
            )
        )
    
    return buttons

def layout(dashboard_id=None):
    dashboard_name = f'Dashboard {dashboard_id}'
    """
    TODO
        Use the dashboard_id to query
        information from the database about that specific dashboard
    """

    return html.Div(
        className="flex",
        children=[
            html.Div(
                className="flex w-screen p-5 items-center",
                children=[
                    html.H1(className="text-3xl",children=[dashboard_name]),
                    html.Div(
                        className="flex ml-auto",
                        children=add_buttons(buttons)
                    ),
                    search_bar()
                ]
            )
        ]
    )
