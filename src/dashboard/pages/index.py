import dash
from dash import html

dash.register_page(__name__, path="/")


def layout():
    return html.H1(children="Index page!")
