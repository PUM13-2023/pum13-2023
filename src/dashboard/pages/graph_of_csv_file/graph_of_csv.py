PORT = 8000
ADDRESS = "127.0.0.1"
PATH = "/graph_of_csv_file"

import base64
import datetime
from gc import callbacks
import io

import dash
from dash import Dash, callback, dash_table, dcc, html
from dash.dependencies import Component, Input, Output, State
import pandas as pd
import plotly.express as px

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
            dcc.Upload(
                id="upload-data",
                children=html.Div(["Drag and Drop or ", html.A("Select Files")]),
                style={
                    "width": "100%",
                    "height": "60px",
                    "lineHeight": "60px",
                    "borderWidth": "1px",
                    "borderStyle": "dashed",
                    "borderRadius": "5px",
                    "textAlign": "center",
                    "margin": "10px",
                },
                # Allow multiple files to be uploaded
                multiple=True,
            ),
            html.Div(id="output-data-upload"),
        ],
    )


# def parse_contents(contents, filename, date):
def parse_contents(contents, filename):
    content_type, content_string = contents.split(",")

    # define data frame as global
    # global df
    # global dict_col
    decoded = base64.b64decode(content_string)
    try:
        if "csv" in filename:
            # byt till polars
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))

            # ======== can draw a simple graph based on a csv file, but in a new window
            # fig = px.line(df, x="x", y="y", title="Test graph from csv file")
            # fig.show()

            # ===try to get it to open in the same window
            fig = px.line(df, x="x", y="y", title="Test graph from csv file")
            # fig.show()

            return dcc.Graph(figure=fig)

    except Exception as e:
        print(e)
        return html.Div(["Error: could not process file"])


@callback(
    Output("output-data-upload", "children"),
    Input("upload-data", "contents"),
    State("upload-data", "filename"),
    # State("upload-data", "last_modified"),
)
# def update_output(list_of_contents, list_of_names, list_of_dates):
def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [
            # parse_contents(c, n, d)
            parse_contents(c, n)
            # for c, n, d in zip(list_of_contents, list_of_names, list_of_dates)
            for c, n in zip(list_of_contents, list_of_names)
        ]
        return children
