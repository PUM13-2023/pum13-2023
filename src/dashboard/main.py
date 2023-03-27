import dash
from dash import Dash, html
from dash.dependencies import Component

from dashboard.components.navbar_component import navbar_component

external_scripts = ["https://tailwindcss.com/", {"src": "https://cdn.tailwindcss.com"}]

app = Dash(__name__, use_pages=True, external_scripts=external_scripts)

PORT = 8000


def page_container() -> Component:
    dash.page_container.className = "grow overflow-auto"

    return html.Div(
        className="flex h-screen",
        children=[
            navbar_component(),
            dash.page_container,
        ],
    )


app.layout = page_container

if __name__ == "__main__":
    app.run("127.0.0.1", PORT, debug=True)
