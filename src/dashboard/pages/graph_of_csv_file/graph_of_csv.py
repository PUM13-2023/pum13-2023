import base64
import io

import dash
from dash import callback, dcc, html
from dash.dependencies import Component, Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px
import polars as pl

PATH = "/graph_of_csv_file"
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

event = {"event": "click", "props": ["scatter", "line"]}


# the main graphical component for the entire csv graph create page page
def layout() -> Component:
    """
    Main layout component that is parent to all other components
    """
    # main background element
    return html.Div(
        className=f'bg-[{colors["background"]}] flex h-screen w-full items-center',
        children=[left_setting_bar(), graph_window(), right_settings_bar()],
    )


def left_setting_bar() -> Component:
    """
    Left settings bar contaning buttons for uploading a csv-file
    """
    # import button, and settings to the left
    return html.Div(  # change back to temp for debugging
        className=f'bg-[{colors["background"]}] flex flex-col items-center ml-5 px-5 h-[80%] w-[20%]   ',
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
                    html.Div(id="output_left_setting_bar"),
                ],
            )
        ],
    )


def csv_button() -> Component:
    """
    button to upload a csv file
    """
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


def db_button() -> Component:
    """
    NOT IN USE: button to get data from a database
    """
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


def graph_window() -> Component:
    """
    A parent window used to display the graph
    """
    return html.Div(  # change back to temp for debugging
        className=f"bg-[{colors['background']}] flex justify-center mx-4 h-[62%] w-[55%]",
        children=html.Div(id="graph_output"),
    )


def display_graph(df: pl.DataFrame, graph_type: str) -> Component:
    """
    Displays a graph based in the chosen type by the user
    """
    if df is not None:
        # print("graph_type ", graph_type)
        if graph_type == "scatter":
            fig = px.scatter(
                df, x=list(df["x"]), y=list(df["y"]), title="Test graph from csv file"
            )
        if graph_type == "line":
            fig = px.line(df, x=list(df["x"]), y=list(df["y"]), title="Test graph from csv file")
        if graph_type == "hist":
            fig = px.histogram(df, x=list(df["x"]), title="Test graph from csv file")
        return dcc.Graph(figure=fig)


def right_settings_bar() -> Component:
    """
    right settings bar, containing the different types graphs that can be chosen for display
    """
    return html.Div(  # change back to temp for debugging
        className=f"bg-[{colors['background']}] flex flex-col items-center justify-center"
        " h-[80%] w-[20%]",
        children=[
            dcc.RadioItems(
                options=[
                    {"label": "linjediagram", "value": "line"},
                    {"label": "scatter plot", "value": "scatter"},
                    {"label": "histogram", "value": "hist"},
                ],
                value="line",
                id="choose_graph_type",
            )
        ],
    )


def parse_contents(contents: str, filename: str) -> pl.DataFrame:
    """
    Parses the input from a csv-file and returns it in the form of a polars dataframe
    """
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)

    if "csv" in filename:
        df = pl.read_csv(io.StringIO(decoded.decode("utf-8")))
        return df


@callback(
    Output("graph_output", "children"),
    Input("uploaded_data", "contents"),
    State("uploaded_data", "filename"),
    State("choose_graph_type", "value"),
)
def update_output(content: str, filename: str, value: str) -> Component:
    """
    Uses parse_contents to the input from a csv file into a dataframe. Takes that data frame and
    creates a graph of it based in the chosen graph type
    """
    if content is None:
        raise PreventUpdate

    # print(f"{value=}")
    df = parse_contents(content, filename)
    loc_graph = display_graph(df, value)
    return loc_graph
