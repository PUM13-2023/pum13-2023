# specifies the address to this: http://127.0.0.1:8000/login/
# start website in normal cmd python -m dashboard.main
# kör "isort ." i cmd
# kör "black ." i cmd innan commits
# open cmd in vscod with ctrl+shift+p and write new terminal
# to run website in vscode terminal write python .\src\dashboard\main.py

PORT = 8000
ADDRESS = "127.0.0.1"

import dash
from dash import Dash, dcc, html
from dash.dependencies import Component, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

dash.register_page(__name__, path="/login")

image_path = "assets/logoTransparent.png"


# sets the colors of the login page
colors = {
    "background": "#E9E9F2",
    "text": "#7FDBFF",
    "meny_back": "#636AF2",
    "white": "#FFFFFF",
    "dark_purp": "#2F3273",
    "black": "#00000",
}

# allowed input
allowed_input = (
    "text",
    "number",
    "password",
)


def layout() -> Component:
    return html.Div(
        className=f'bg-[{colors["background"]}] flex h-full w-full justify-center items-center',
        children=[
            # Layout for the login meny
            # main rectangle
            html.Div(
                className="flex h-[30%] w-[60%]",
                children=[
                    # left rectangle
                    html.Div(
                        className=f'bg-[{colors["meny_back"]}] h-full w-[50%]',
                        children=[
                            # input fields
                            # username field, input is not taken
                            html.Div(
                                dcc.Input(
                                    id="userid",
                                    type="text",
                                    placeholder="username",
                                )
                            ),
                            # password field, input is not aken
                            html.Div(
                                dcc.Input(
                                    id="password",
                                    type="text",
                                    placeholder="password",
                                )
                            ),
                            # Login button, input not taken
                            html.Button(
                                className=f'bg-[{colors["dark_purp"]}]',
                                children=[
                                    html.P("Login"),
                                ],
                                id="verify",
                                n_clicks=0,
                            ),
                            html.Div(id="output1"),
                        ],
                    ),
                    # right rectangle
                    html.Div(
                        className=f'bg-[{colors["white"]}] h-full w-[50%]',
                        children=[
                            html.H1(
                                "Welcome to GraphIt",
                            ),
                            # product logo
                            html.Img(
                                src=image_path,
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )


# @main.callback(
#   dash.dependencies.Output("output1", "children"),
#  [dash.dependencies.Input("verify", "n_clicks")],
# state=[State("user", "value"), State("passw", "value")],
# )
def update_output(n_clicks, uname, passw):
    li = {"admin123": "admin123"}
    if uname == "" or uname == None or passw == "" or passw == None:
        return html.Div(children="", style={"padding-left": "550px", "padding-top": "10px"})
    if uname not in li:
        return html.Div(
            children="Incorrect Username",
            style={"padding-left": "550px", "padding-top": "40px", "font-size": "16px"},
        )
    if li[uname] == passw:
        return html.Div(
            dcc.Link(
                "Access Granted!",
                href="/next_page",
                style={
                    "color": "#183d22",
                    "font-family": "serif",
                    "font-weight": "bold",
                    "text-decoration": "none",
                    "font-size": "20px",
                },
            ),
            style={"padding-left": "605px", "padding-top": "40px"},
        )
    else:
        return html.Div(
            children="Incorrect Password",
            style={"padding-left": "550px", "padding-top": "40px", "font-size": "16px"},
        )
