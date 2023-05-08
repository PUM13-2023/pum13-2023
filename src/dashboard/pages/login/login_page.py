"""The layout component of the login page."""

import dash
from dash import callback, dcc, html
from dash.dependencies import Component, Input, Output, State

from dashboard.models.user import login_user

PORT = 8000
ADDRESS = "127.0.0.1"
PATH = "/login"

dash.register_page(__name__, path=PATH, nav_item=False)

NORMAL_FIELD_CLASS = "w-[90%] p-[13px] rounded-full"

ERROR_FIELD_CLASS = (
    "w-[420px] p-[13px] bg-red-50 "
    "placeholder-red-700 rounded-full focus:ring-red-500"
    "focus:border-red-500 dark:text-red-500 "
    "dark:placeholder-red-500 dark:border-red-500"
)

PASS_FIELD_EXTRA_CLASS = " my-4"


def get_username_input_field() -> Component:
    """Return a Dash Input component for entering a username.

    Returns:
        A Dash Input component with the following properties:
        - className: That defaults to the default field class.
        - id: The unique ID for the username field.
        - type: Is text because it is a username field .
        - placeholder: Is the placeholder text.
        - autoFocus: Focus on this element after loaidng the page.
    """
    class_name = NORMAL_FIELD_CLASS
    id = "username"
    type = "text"
    placeholder = "username"
    auto_focus = True
    return dcc.Input(
        className=class_name,
        id=id,
        type=type,
        placeholder=placeholder,
        autoFocus=auto_focus,
    )


def get_password_input_field() -> Component:
    """Return a Dash Input component for entering a password.

    Returns:
        A Dash Input component with the following properties:
        - className: That defaults to the default field class.
        - id: The unique ID for the password field.
        - type: It is password so it hidden when writing in
                your password
        - placeholder: Is the placeholder text.
    """
    class_name = NORMAL_FIELD_CLASS + PASS_FIELD_EXTRA_CLASS
    id = "password"
    type = "password"
    placeholder = "password"
    return dcc.Input(
        className=class_name,
        id=id,
        type=type,
        placeholder=placeholder,
    )


def get_login_button() -> Component:
    """Returns a Dash Button component for a login button.

    Returns:
        A Dash Button component with the following properties:
        - className: The CSS class name for the button.
        - children: The text element of the button.
        - id: The unique ID for the button.
    """
    return html.Button(
        className=("bg-dark-purple w-[40%] p-[10px] " "rounded-full"),
        children=[
            html.Div(
                className="bg-white",
                children=[html.P("Login", className="text-white bg-dark-purple")],
            )
        ],
        id="login_button",
    )


def get_main_left_rectangle() -> Component:
    """Returns a div component for the left of the main rectangle.

    Returns:
        A Dash Div component with the following properties:
        - className: The CSS class name for the rectangle.
        - children: A div component with different text field.
    """
    return html.Div(
        className="bg-menu-back flex flex-col items-center"
        " justify-center w-[600px] rounded-l-lg",
        children=[
            get_username_input_field(),
            get_password_input_field(),
            get_login_button(),
        ],
    )


def get_main_right_rectangle() -> Component:
    """Returns a div component for the right of the main rectangle.

    Returns:
        A Dash Div component with the following properties:
        - className: The CSS class name for the rectangle.
        - children: A div component with picture.
    """
    return html.Div(
        className="bg-white flex flex-col items-center" " justify-center w-[600px] rounded-r-lg",
        children=[
            html.H1(
                className=" mt-4 pd-4 text-2xl",
                children=[
                    "Welcome to GraphIt",
                ],
            ),
            # product logo
            html.Img(
                src=dash.get_asset_url("logoTransparent.png"),
            ),
        ],
    )


def get_error_pop_up() -> Component:
    """Returns a div component for the error pop up.

    Returns:
        A Dash Div component with the following properties:
        - className: The CSS class name for the error pop up.
        - children: A div component of the text of the error.
    """
    return html.Div(
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
    )


def get_main_rectangle() -> Component:
    """Returns a div component for the main rectangle.

    Returns:
        A Dash Div component with the following properties:
        - className: The CSS class name for the main rectangle.
        - children: A div component of the main rectangle.
    """
    return html.Div(
        id="login_ui",
        className="flex h-[350px] w-[600px] md:w-[700px] lg:w-[950px] drop-shadow-lg",
        children=[
            get_main_left_rectangle(),
            get_main_right_rectangle(),
            get_error_pop_up(),
        ],
    )


def layout() -> Component:
    """The layout of the login page."""
    return html.Div(
        className=(
            "bg-background flex h-screen w-full " "justify-center items-center overflow-x-hidden"
        ),
        children=[
            # Layout for the login menu
            get_main_rectangle(),
            dcc.Location(id="login-url", refresh="callback-nav"),
        ],
    )


@callback(
    Output("login-url", "pathname"),
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
) -> tuple[None | dcc.Location, str, str, str]:
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

    if password == "password":
        login_user(username)

        return (
            "/",
            error_pop_up + " hidden",
            NORMAL_FIELD_CLASS,
            NORMAL_FIELD_CLASS + PASS_FIELD_EXTRA_CLASS,
        )

    return (
        dash.no_update,
        error_pop_up.replace("hidden", ""),
        ERROR_FIELD_CLASS,
        ERROR_FIELD_CLASS + PASS_FIELD_EXTRA_CLASS,
    )
