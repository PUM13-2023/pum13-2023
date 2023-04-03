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
import plotly.express as px
import polars as pl

dash.register_page(__name__, path=PATH, nav_item=False)


# sets the colors of the login page
colors = {
    "background": "#E9E9F2",
    "text": "#7FDBFF",
    "meny_back": "#636AF2",
    "white": "#FFFFFF",
    "dark_purp": "#2F3273",
    "black": "#00000",
    "temp": "#ffc0cb",
}


# the main graphical component for the entire csv graph create page page
def layout() -> Component:
    # main background element
    return html.Div(
        className=f'bg-[{colors["background"]}] flex h-screen w-full items-center',
        children=[left_setting_bar(), graph_window(), right_settings_bar()],
    )


# left side settings bar
def left_setting_bar():
    # import button, and settings to the left
    return html.Div(
        className=f'bg-[{colors["temp"]}] flex flex-col items-center ml-5 px-5 h-[80%] w-[20%]   ',
        children=[
            # buttons for import and get from database
            html.Div(
                className=f'bg-[{colors["background"]}] flex flex-row mt-10 h-[9%] w-[100%]',
                children=[
                    # left button
                    csv_button(),
                    html.Div(id="csv_uploaded_data"),
                    # right button for getting data from the database
                    db_button(),
                    html.Div(id="output1"),
                ],
            )
        ],
    )


# button to upload a csv file
def csv_button():
    return dcc.Upload(
        className=f"bg-[{colors['meny_back']}] grow h-[100%] flex flex-col px-4 justify-center"
        " border-2 border-black",
        id="uploaded_data",
        children=html.Div(
            html.A("Import a CSV file"),
        ),
        # false so multiple files cant be uploaded
        multiple=False,
    )


# button to get data from a database
def db_button():
    return html.Button(
        className=f"bg-[{colors['meny_back']}] grow h-[100%] flex flex-col px-4 justify-center"
        " border-2 border-black",
        children=[
            html.Div(
                # className=f'bg-[{colors["background"]}',
                children=[
                    html.P(
                        "Get from database",
                        style={"color": colors["black"]},
                    ),
                ],
            )
        ],
        id="database_button",
        n_clicks=0,
    )


# window to show the created graph
def graph_window():
    return html.Div(
        className=f"bg-[{colors['temp']}] flex justify-center mx-4 h-[62%] w-[55%]",
        children=html.Div(id="graph_output"),
    )


# creates a specific
# def display_graph(df, graph_type):
def display_graph(df):
    #    if(graph_type == "line"):
    # fig = px.line(df, x="x", y="y", title="Test graph from csv file")
    fig = px.line(df, x=list(df["x"]), y=list(df["y"]), title="Test graph from csv file")
    # if graph_type == "scatter":
    #   fig = px.scatter(df, x=list(df["x"]), y=list(df["y"]), title="Test graph from csv file")
    return dcc.Graph(figure=fig)


# right settings bar, choose what kind of a plot
def right_settings_bar():
    return html.Div(
        className=f"bg-[{colors['temp']}] flex flex-row items-center justify-center"
        " h-[80%] w-[20%]",
        children=html.Div(choose_plot()),
    )


# buttons to choose a plot
def choose_plot():
    return html.Div(plot_buttons("scatter", "scatter_button_id"))


def plot_buttons(button_text, button_id):
    return html.Button(
        className=f"bg-[{colors['meny_back']}] grow h-[100%] flex flex-col px-4 justify-center"
        " border-2 border-black",
        children=[
            html.Div(
                children=[
                    html.P(
                        button_text,
                        style={"color": colors["black"]},
                    ),
                ],
            )
        ],
        id=button_id,
        n_clicks=0,
    )


# parses the contents of the inputed csv file using polars
def parse_contents(contents, filename):
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)

    try:
        if "csv" in filename:
            df = pl.read_csv(io.StringIO(decoded.decode("utf-8")))
            return df

    except Exception as e:
        print(e)
        return html.Div(["Error: could not process file"])


@callback(
    Output("graph_output", "children"),
    # input("output_scatter", "sca"),
    Input("uploaded_data", "contents"),
    State("uploaded_data", "filename"),
)

# def update_output(content, filename, sca):
def update_output(content, filename):
    df = parse_contents(content, filename)
    print(df)
    # loc_graph = display_graph(df, sca)
    loc_graph = display_graph(df)
    return loc_graph
