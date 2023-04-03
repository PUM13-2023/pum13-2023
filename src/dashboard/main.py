"""main module.

This module defines main dash configuration and layout.
If run as main, hosts the server locally.

Running the server locally is not intended for production purposes.

Examples:
    Running locally::

        $ python -m dashboard.main

    Running with gunicorn::

        $ gunicorn -w 4 dashboard.main:server
"""
import dash
from dash import Dash, dcc, html
from dash.dependencies import Component
from flask import Flask

from dashboard.components.navbar_component import navbar_component

external_stylesheets = [
    {
        "href": "/assets/font.css",
        "rel": "stylesheet",
    },
    {
        "href": "/assets/dashboard.css",
        "rel": "stylesheet",
    },
]

server = Flask(__name__)
app = Dash(
    __name__,
    server=server,
    use_pages=True,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True,
)

PORT = 8000


def page_container() -> Component:
    """Main page layout containing navbar and page container."""
    dash.page_container.className = "grow overflow-auto"
    return html.Div(
        id="main",
        className="flex bg-[#E9E9F2] h-screen overflow-x-hidden",
        children=[
            dcc.Location(id="main-url", refresh=False),
            navbar_component(),
            dash.page_container,
        ],
    )


app.layout = page_container


if __name__ == "__main__":
    app.run("0.0.0.0", PORT, debug=True)
