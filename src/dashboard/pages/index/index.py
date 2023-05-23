"""Index page module."""
from typing import Optional

import dash
from dash import html
from dash_daq import BooleanSwitch
from flask_login import current_user

from dashboard.components import icon, login_required
from dashboard.components.add_dashboard_modal import add_dashboard_modal
import dashboard.pages.index.controller  # noqa: F401

dash.register_page(__name__, path="/", name="Home", order=0, nav_item=True, icon_name="home")

# This username will be replaced later
LATEST_CONTAINER = "Latest opened dashboards"
SHARED_CONTAINER = "Shared dashboards"


def carousel_layout(container_title: str, id_: Optional[str] = None) -> html.Div:
    """Creates a carousel container of dashboards.

        TODO
            Should be rewritten to generate a list
            of carousel items when DB is complete
    Args:
        container_title (str): Title of the carousel container

    Returns:
        html.Div: Div element with a carousel layout
    """
    id = ""
    if container_title == LATEST_CONTAINER:
        empty_dashboard_text = "Create dashboard"
        id = "create-dashboard-btn-carousel"
    else:
        empty_dashboard_text = "Add dashboard from link"

    empty_dashboard_button = html.Div(
        className="flex h-full mb-[3rem]",
        children=[
            html.Button(
                className=(
                    "bg-white transition-all transition duration-150 "
                    "drop-shadow-md w-[20rem] h-[17rem] "
                    "flex border-b-4 hover:border-b-indigo-500 "
                    "justify-center items-center items-baseline flex-col rounded-[2px] "
                    "hover:drop-shadow-[2px_4px_10px_rgba(0,0,0,0.20)] p-5 "
                    "hover:rounded-t-xl mr-[3.5rem]"
                ),
                children=[
                    html.Div(
                        id=id,
                        className="bg-white/70 h-full w-full flex items-center justify-center",
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
        className="flex flex-col h-full",
        children=[
            html.H2(container_title),
            html.Div(className="flex flex-row overflow-x-scroll", children=carousel_list),
        ],
    )

    if id_ is not None:
        carousel_container.id = id_
    return carousel_container


@login_required
def layout() -> html.Div:
    """Layout for home page.

    Returns:
        html.Div: Div tag with the home page layout
    """
    username = current_user.username

    return html.Div(
        className="flex flex-col bg-background p-10 pb-0",
        children=[
            html.Div(id="db-add", className="hidden"),
            BooleanSwitch(id="title", className="hidden", on=False),
            BooleanSwitch(id="desc", className="hidden", on=False),
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
                        className=(
                            "bg-white w-[40rem] h-[25rem] duration-150 "
                            "[&>p]:text-2xl shadow-sm "
                            "hover:shadow-lg flex justify-center flex-col text-black/50 "
                            "items-center rounded-md drop-shadow-[0px_0px_2px_rgba(0,0,0,0.20)] "
                            "hover:text-black hover:rounded-[20px]"
                        ),
                        children=[icon("add_circle", fill=1), html.P("Create dashboard")],
                        id="create-dashboard-btn",
                        n_clicks=0,
                    )
                ],
            ),
            html.Div(
                className="flex-col flex h-full",
                children=[
                    carousel_layout("Latest opened dashboards", id_="latest-opened-dashboards"),
                    carousel_layout("Shared dashboards", id_="shared-dashboards"),
                ],
            ),
            add_dashboard_modal(),
        ],
    )
