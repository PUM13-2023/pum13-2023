import dash
from dash import html
from dash.dependencies import Component, Output, Input


dash.register_page(__name__, path="/", name="Home", order=0, visible_in_nav=True)

default_style = "bg-[#d2d2d2] transition duration-500 ease-in-out"

# This username will be replaced later
username = "cooluser"
LATEST_CONTAINER = "Latest opened dashboards"
SHARED_CONTAINER = "Shared dashboards"

def generate_carousel_items() -> dict[str: any]:
    pass


def carousel_layout(container_title: str) -> html.Div:
    empty_dashboard = ""
    if container_title == LATEST_CONTAINER:
        pass

    return html.Div(
        className="flex flex-col w-full h-full",
        children=[
            html.H2(container_title),
            html.Div(
                className="flex w-full h-full",
                children=[
                    html.Div(
                        className="bg-white w-[17%] h-[80%] flex justify-center items-center",
                        children=[
                            html.P("Create dashboard")
                        ]
                    )
                ]
            )
        ]
    )


def layout() -> Component:
    return html.Div(
        className="flex flex-col w-full h-screen justify-center items-center bg-[#e9e9f2] p-5",
        children=[
            html.Div(
                className="block w-full text-xl",
                children=[
                    html.H1(f'Welcome back {username}'),
                    # Add searchbar here?
                ]
            ),
            html.Button(
                className="bg-[#d2d2d2] w-[50%] h-full flex justify-center items-center rounded-[10px]",
                children=[
                    html.P(className="text-base", children="Create dashboard")
                ],
                id="create-dashboard"
            ),

            carousel_layout("Latest opened dashboards"),
            carousel_layout("Shared dashboards")

        ]
    )


"""@dash.callback(
)
def toggle_create_dashboard_menu(n_clicks: int) -> str:
    return """""
