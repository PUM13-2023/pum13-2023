# specifies the address to this: http://127.0.0.1:8000/login/
# start website in normal cmd python -m dashboard.main
# kör "isort ." i cmd
# kör "black ." i cmd innan commits
# open cmd in vscod with ctrl+shift+p and write new terminal
# to run website in vscode terminal write python .\src\dashboard\main.py

PORT = 8000
ADDRESS = "127.0.0.1"
PATH = "/login"

from gc import callbacks

import dash
from dash import Dash, callback, dcc, html
from dash.dependencies import Component, Input, Output, State

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


# the main graphical component for the entire login page
def layout() -> Component:
    return html.Div(
        className=f'bg-[{colors["background"]}] flex h-screen w-full justify-center items-center',
        children=[
            # Layout for the login meny
            # main rectangle
            html.Div(
                id="login_ui",
                className="flex h-[30%] w-[60%]  ",
                children=[
                    # left rectangle
                    html.Div(
                        className=f'bg-[{colors["meny_back"]}] flex flex-col items-center'
                        " justify-center w-[50%] rounded-l-lg",
                        children=[
                            # used id input field
                            dcc.Input(
                                className="w-[60%] mb-5 px-3 py-1 rounded-full",
                                id="username",
                                type="text",
                                placeholder="username",
                            ),
                            # password input field
                            dcc.Input(
                                className="w-[60%] mb-5 px-3 py-1 rounded-full",
                                id="password",
                                type="password",
                                placeholder="password",
                            ),
                            # login button
                            html.Button(
                                className=f'bg-[{colors["dark_purp"]}] pd-4 w-[30%] rounded-full',
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
                            html.Div(id="output1"),
                        ],
                    ),
                    # right rectangle
                    html.Div(
                        className=f'bg-[{colors["white"]}] flex flex-col items-center'
                        " justify-center w-[50%] rounded-r-lg",
                        children=[
                            html.H1(
                                className=f" mt-4 pd-4 ",
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
                ],
            ),
        ],
    )


# takes the input from the div that contains the input for username, password and login button
@callback(
    Output("output1", "children"),
    Input("login_button", "n_clicks"),
    Input("username", "n_submit"),
    Input("password", "n_submit"),
    State("username", "value"),
    State("password", "value"),
)


# is the loginfunction that checks if a user can login when the login button is pressed.
# currently username: "admin" and login: "admin"
def update_login(n_clicks, username_enter, password_enter, username, password):
    if username == "admin" and password == "admin":
        # return f"You selected: {input_value}"
        return dcc.Location(pathname="/main", id="id1")
    if n_clicks > 0:
        return f"Wrong Input!"
