"""Module containing decorators for authentication."""
from collections.abc import Callable
from functools import wraps

from dash import dcc, html
from dash.dev import Component
from flask_login import current_user


def login_required(layout_fn: Callable[[], Component]) -> Callable[[], Component]:
    """Check if the current user is authenticated.

    If the user is not authenticated, the layout is replaced with a
    prompt to login.
    """

    @wraps(layout_fn)
    def wrapper() -> Component:
        if not current_user.is_authenticated:
            return html.Div(
                className="w-full h-screen flex flex-col justify-center items-center",
                children=[
                    dcc.Link("Login to access page.", href="/login", className="text-xl underline")
                ],
            )
        return layout_fn()

    return wrapper
