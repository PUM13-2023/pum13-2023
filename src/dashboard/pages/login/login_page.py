"""The layout component of the login page."""

import dash
from dash import callback, dcc, html
from dash.dependencies import Component, Input, Output, State

PORT = 8000
ADDRESS = "127.0.0.1"
PATH = "/login"

dash.register_page(__name__, path=PATH, nav_item=False)

# sets the colors of the login page
colors = {
    "background": "#E9E9F2",
    "text": "#7FDBFF",
    "meny_back": "#636AF2",
    "white": "#FFFFFF",
    "dark_purp": "#2F3273",
    "black": "#00000",
}

NORMAL_FIELD_CLASS = "w-[420px] p-[13px] rounded-md shadow-inner shadow-lg"

ERROR_FIELD_CLASS = (
    "w-[420px] p-[13px] bg-red-50 "
    "placeholder-red-700 rounded-md focus:ring-red-500"
    "focus:border-red-500 dark:text-red-500/75 "
    "dark:placeholder-red-500 dark:border-red-500"
)

PASS_FIELD_EXTRA_CLASS = " my-4"


def layout() -> Component:
    """The layout of the login page."""
    return html.Div(
        className=f'bg-[{colors["background"]}] flex h-screen w-full justify-center items-center',
        children=[
            # Layout for the login meny
            # main rectangle
            html.Div(
                id="login_ui",
                className="flex h-[350px] w-[1200px] drop-shadow-lg",
                children=[
                    # left rectangle
                    html.Div(
                        className=f'bg-[{colors["meny_back"]}] flex flex-col items-center'
                        " justify-center w-[600px] rounded-l-lg",
                        children=[
                            html.Div(id="dcc_location_login"),
                            # used id input field
                            dcc.Input(
                                className=NORMAL_FIELD_CLASS,
                                id="username",
                                type="text",
                                placeholder="username",
                                autoFocus=True,
                            ),
                            # password input field
                            dcc.Input(
                                className=NORMAL_FIELD_CLASS + PASS_FIELD_EXTRA_CLASS,
                                id="password",
                                type="password",
                                placeholder="password",
                            ),
                            # login button
                            html.Button(
                                className=(
                                    f'bg-[{colors["dark_purp"]}] w-[40%] p-[10px] ' "rounded-full shadow-lg"
                                ),
                                children=[
                                    html.Div(
                                        className=f'bg-[{colors["white"]}',
                                        children=[
                                            html.P("Login", style={"color": colors["white"]}),
                                        ],
                                    )
                                ],
                                id="login_button",
                                n_clicks=0,
                            ),
                        ],
                    ),
                    # right rectangle
                    html.Div(
                        className=f'bg-[{colors["white"]}] flex flex-col items-center'
                        " justify-center w-[600px] rounded-r-lg",
                        children=[
                            html.H1(
                                className=" mt-4 pd-4 ",
                                children=[
                                    "Welcome to GraphIt",
                                ],
                            ),
                            # product logo
                            html.Img(
                                src=dash.get_asset_url("logoTransparent.png"),
                            ),
                        ],
                    ),
                    # error pop-up
                    html.Div(
                        id="error_input_message",
                        className=(
                            "hidden drop-shadow-2xl fixed bottom-[-100px] "
                            "left-1/2 transform -translate-x-1/2 h-fit w-fit "
                            "fit-content bg-red-100 border border-red-400 "
                            "text-red-700 px-4 py-3 mt-3 rounded"
                        ),
                        children=[
                            html.H2(
                                className="text-center",
                                children="Wrong username or password!",
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )


@callback(
    Output("dcc_location_login", "children"),
    Output("error_input_message", "className"),
    Output("username", "className"),
    Output("password", "className"),
    State("error_input_message", "className"),
    State("username", "value"),
    State("password", "value"),
    Input("username", "n_submit"),
    Input("password", "n_submit"),
    Input("login_button", "n_clicks"),
    prevent_initial_call=True,
)
def update_login(
    error_pop_up: str, username: str, password: str, *_: int
) -> tuple[None or dcc.Location, str, str, str]:
    """Updates login page when inputing the password or username.

    This function updates the username field and password field
    style by updating their className, in which the text field
    would have a red hue to mark that something when wrong.
    The function would also make the error pop up not hidden by
    changing the error_pop_up.

    Args:
        error_pop_up (str): The class name of error pop up element.
        username (str): The class name of the username text field.
        password (str): the class name of the passowrd text field.
    """
    # If it is the correct username and password that we change the page
    # to the home page.
    if username == "admin" and password == "admin":
        return (
            dcc.Location(pathname="", id="dcc_location_login"),
            error_pop_up + " hidden",
            NORMAL_FIELD_CLASS,
            NORMAL_FIELD_CLASS + PASS_FIELD_EXTRA_CLASS,
        )
    else:
        return (
            None,
            error_pop_up.replace("hidden", ""),
            ERROR_FIELD_CLASS,
            ERROR_FIELD_CLASS + PASS_FIELD_EXTRA_CLASS,
        )
