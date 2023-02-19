import dash
from dash import Dash, html
from dash.dependencies import Component

app = Dash(__name__, use_pages=True)


def page_container() -> Component:
    return html.Div([html.H1("PUM13-2023"), dash.page_container])


app.layout = page_container

if __name__ == "__main__":
    app.run("127.0.0.1", "8000")
