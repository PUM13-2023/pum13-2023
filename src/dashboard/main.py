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
import os

import dash
from dash import Dash, dcc, html
from dash.dependencies import Component
from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager

from dashboard.components.navbar_component import navbar_component
from dashboard.models.user import User

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

load_dotenv()

server = Flask(__name__)
app = Dash(
    __name__,
    server=server,
    use_pages=True,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True,
)

server.secret_key = os.environ["SECRET_KEY"]
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = "/login"


@login_manager.user_loader
def load_user(user_id: str) -> User:
    """Load a user by id.

    Required by flask-login. For more information, see
    https://flask-login.readthedocs.io/en/latest/#your-user-class
    """
    user: User = User.objects(id=user_id).get()
    user.is_authenticated = True

    return user


PORT = 8000


def page_container() -> Component:
    """Main page layout containing navbar and page container."""
    dash.page_container.className = "grow overflow-auto bg-background"
    return html.Div(
        id="main",
        className="flex h-screen overflow-x-hidden",
        children=[
            dcc.Location(id="main-url", refresh=False),
            navbar_component(),
            dash.page_container,
        ],
    )


app.layout = page_container


if __name__ == "__main__":
    app.run("127.0.0.1", PORT, debug=True)
