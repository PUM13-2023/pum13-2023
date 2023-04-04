"""Index page module."""
import dash
from dash import html

from dashboard.components.icon import icon

dash.register_page(__name__, path="/", name="Home", order=0, nav_item=True, icon_name="home")

default_style = "bg-[#d2d2d2] transition duration-500 ease-in-out"

# This username will be replaced later
username = "cooluser"
LATEST_CONTAINER = "Latest opened dashboards"
SHARED_CONTAINER = "Shared dashboards"


def carousel_layout(container_title: str, id=None) -> html.Div:
    """Creates a carousel container of dashboards
        TODO
            Should be rewritten to generate a list
            of carousel items when DB is complete
    Args:
        container_title (str): Title of the carousel container

    Returns:
        html.Div: Div element with a carousel layout
    """
    if container_title == LATEST_CONTAINER:
        empty_dashboard_text = "Create dashboard"
    else:
        empty_dashboard_text = "Add dashboard from link"

    empty_dashboard_button = html.Div(
        className="flex h-full mb-[3rem]",
        children=[
            html.Button(
                className="bg-white transition-all transition duration-500 "
                "drop-shadow-md w-[20rem] h-[17rem] "
                "flex border-b-4 hover:border-b-indigo-500 "
                "justify-center items-center items-baseline flex-col rounded-[2px] "
                "hover:drop-shadow-[2px_4px_10px_rgba(0,0,0,0.20)] p-5 "
                "hover:rounded-t-xl mr-[3.5rem]",
                children=[
                    html.Div(
                        className="bg-[#dcdcdc]/70 h-full w-full flex items-center justify-center",
                        children=[icon("add_circle", fill=1, className="text-4xl text-black/75")],
                    ),
                    html.P(className="text-md my-3", children=empty_dashboard_text),
                ],
            )
        ],
    )

    # Future carousel items are placed in here
    carousel_list = [empty_dashboard_button]

    carousel_container = html.Div(
        id=id,
        className="flex flex-col h-full",
        children=[
            html.H2(container_title),
            html.Div(className="flex flex-row overflow-x-scroll", children=carousel_list),
        ],
    )

    return carousel_container


def layout() -> html.Div:
    return html.Div(
        className="flex flex-col bg-[#e9e9f2] p-10 pb-0",
        children=[
            html.Div(
                className="block w-full text-3xl",
                children=[
                    html.H1(f"Welcome back {username}"),
                    # Add searchbar here?
                ],
            ),
            # Create dashboard button
            html.Div(
                className="flex justify-center w-full",
                children=[
                    html.Button(
                        className="bg-white w-[40rem] h-[25rem] duration-300 "
                        "[&>p]:text-2xl shadow-sm "
                        "hover:shadow-lg flex justify-center flex-col text-black/50 "
                        "items-center rounded-md drop-shadow-[0px_0px_2px_rgba(0,0,0,0.20)] "
                        "hover:text-black hover:rounded-[20px]",
                        children=[icon("add_circle", fill=1), html.P("Create dashboard")],
                        id="create-dashboard",
                    )
                ],
            ),
            html.Div(
                className="flex-col flex h-full",
                children=[
                    carousel_layout("Latest opened dashboards", id="latest-opened-dashboards"),
                    carousel_layout("Shared dashboards", id="shared-dashboards"),
                ],
            ),
        ],
    )
