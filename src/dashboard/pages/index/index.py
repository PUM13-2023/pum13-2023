"""Index page module."""
import dash
from dash import html
from dash.dependencies import Component, Output, Input

dash.register_page(__name__, path="/", name="Home", order=0, nav_item=True)

default_style = "bg-[#d2d2d2] transition duration-500 ease-in-out"

# This username will be replaced later
username = "cooluser"
LATEST_CONTAINER = "Latest opened dashboards"
SHARED_CONTAINER = "Shared dashboards"


def carousel_layout(container_title: str) -> html.Div:
    if container_title == LATEST_CONTAINER:
        empty_dashboard_text = "Create dashboard"
    else:
        empty_dashboard_text = "Add dashboard from link"

    return html.Div(
        className="flex flex-col w-full h-full",
        children=[
            html.H2(container_title),
            html.Div(
                className="flex w-full h-full mb-[3rem]",
                children=[
                    html.Button(
                        className="bg-white transition-all transition duration-500 drop-shadow-md w-[20rem] h-[17rem] "
                                  "flex border-b-4 hover:border-b-indigo-500 "
                                  "justify-center items-center items-baseline flex-col rounded-[2px] "
                                  "hover:drop-shadow-[2px_4px_10px_rgba(0,0,0,0.20)] p-5 " 
                                  "hover:rounded-t-xl"
                                  ,
                        children=[
                            html.Div(
                                className="bg-[#dcdcdc]/70 h-full w-full",
                            ),
                            html.P(className="text-md my-3", children=empty_dashboard_text)
                        ]
                    )
                ]
            )
        ]
    )


def layout() -> Component:
    return html.Div(
        # Welcome text and create button
        className="flex flex-col justify-center items-center bg-[#e9e9f2] p-10 pb-0",
        children=[
            html.Div(
                className="block w-full text-3xl",
                children=[
                    html.H1(f'Welcome back {username}'),
                    # Add searchbar here?
                ]
            ),
            html.Div(
                className="flex justify-center w-full",
                children=[
                    html.Button(
                        className="bg-white w-[40rem] h-[25rem] transition-all duration-300 [&>p]:text-2xl shadow-sm "
                                  "hover:shadow-lg flex justify-center "
                                  "items-center rounded-[10px] drop-shadow-[0px_0px_2px_rgba(0,0,0,0.20)] "
                                  "hover:w-[42rem]"
                                  ,
                        children=[
                            html.P(className="text-black/60", children="Create dashboard")
                        ],
                        id="create-dashboard"
                    )
                ]
            ),

            html.Div(
                className="flex-col flex w-full h-full",
                children=[
                    carousel_layout("Latest opened dashboards"),
                    carousel_layout("Shared dashboards")
                ]
            )
        ]
    )


"""@dash.callback(
)
def toggle_create_dashboard_menu(n_clicks: int) -> str:
    return """""
