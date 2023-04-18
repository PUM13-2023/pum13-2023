"""Graph display module.

This module displays different types of graphs based on input,
from either a csv-file or from a database.
"""

import base64
import io
import json
import os
from typing import Any
import pprint
import dash
from dash import callback, dcc, html, Patch
from dash.dependencies import Component, Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go
import polars as pl

from dashboard.components import button, icon

dash.register_page(__name__, path="/create-graph", nav_item=False)

# used to supress warning messages for all components created by layout
suppress_callback_exceptions = True

# for debugging
global debug
debug = True

<<<<<<< HEAD
=======

# Colors used when creating the layout
colors = {
    "background": "#E9E9F2",
    "text": "#7FDBFF",
    "meny_back": "#636AF2",
    "white": "#FFFFFF",
    "dark_purp": "#2F3273",
    "black": "#000000",
    "debug": "#ffc0cb",
    "blue": "#0000FF",
    "red": "#FF0000",
}

>>>>>>> 603fc12 (Fixed docstrings and cleaned the code abit)
event = {"event": "click", "props": ["scatter", "line"]}


# the main graphical component for the entire csv graph create page page
def layout() -> Component:
    """Main layout component that is parent to all other components.

    Returns:
        A html.div component with all other components.
    """
    # main background element
    return html.Div(
        className=f'bg-[{colors["background"]}] flex h-screen',
        children=[
            # dcc.Store(id="df_storage", storage_type="local"),
            dcc.Store(id="df_storage"),
            graph_window(),
            right_settings_bar(),
            dcc.Input(id="graph_index", value=0, className="hidden"),
            dcc.Input(id="num_graphs", value=0, className="hidden")
        ],
    )


def left_setting_bar() -> Component:
    """Left settings bar contaning.

    Returns:
        A component containing the csv_button and db_button.
    """
    # import button, and settings to the left
    return html.Div(  # change back to debug for debugging
        className=f"bg-[{colors['debug']}] flex flex-col items-center ml-5 px-5 h-[80%]" "w-[20%]",
        children=[
            # buttons for import and get from database
            graph_name(),
            x_axis_name(),
            y_axis_name(),
            file_name(),
        ],
    )


def csv_button() -> Component:
    """Button to upload a csv file.

    Returns:
        A dcc.upload containg a csv-file.
    """
    return dcc.Upload(
        className="bg-menu-back duration-150 shrink flex flex-col "
        "cursor-pointer p-3 mr-2 rounded-md hover:bg-dark-purple",
        id="uploaded_data",
        children=html.Div(
            className="flex items-center",
            children=[
                icon("upload", size=36, className="mr-1"),
                html.P(className="whitespace-nowrap", children="CSV-file"),
            ],
        ),
        # True so multiple files can be uploaded
        multiple=True,
    )
    
def download_button(icon, text, id):
    """Predefined button style

    Args:
        icon (_type_): _description_
        text (_type_): _description_
        id (_type_): _description_

    Returns:
        _type_: _description_
    """
    return button(icon_name=icon, text=text, id=id, className="bg-[#636af2] hover:bg-[#2F3273] justify-center flex-1 text-white")

def download_buttons():
    return html.Div(
        className="flex flex-col",
        children=[
            html.P("Download as"),
            html.Div(
                className="flex space-x-2",
                children=[
                    download_button(icon="image", text="Png", id="download_png"),
                    download_button(icon="image", text="Jpeg", id="download_jpeg"),
                    download_button(icon="picture_as_pdf", text="Pdf", id="download_pdf"),
                    download_button(icon="html", text="Html", id="download_html"),
                ]
                     
            ),
            
        ]
    )

def db_button() -> Component:
    """NOT IN USE: button to get data from a database."""
    return button2("Get from database", "database_button")

def button2(button_text: str, button_id: str) -> Component:
    return html.Button(
        className=f"bg-[{colors['meny_back']}] flex flex-col mt-4 px-4 justify-center"
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


def graph_name() -> Component:
    """Takes user input for the graph label"""
    return input_field("graph_name", "Graph name")


def x_axis_name() -> Component:
    """Takes user input for the x axis label"""
    return input_field("x_axis_name", "x-axis name")


def y_axis_name() -> Component:
    """Takes user input for the y axis label"""
    return input_field("y_axis_name", "y-axis name")


def file_name() -> Component:
    """Takes user input for the graph label"""
    return input_field("file_name", "File name")


def input_field(loc_id: str, loc_placeholder: str) -> Component:
    """Input_field that lets user choose a color

    Args:
        loc_id: local id of the input field
        loc_placeholder: a placeholder color

    Returns:

    """
    return dcc.Input(
        className=f"bg-[{colors['background']}] flex items-center justify-center mt-5 p-2 rounded-md shadow-inner",
        id=loc_id,
        type="text",
        debounce=True,
        placeholder=loc_placeholder,
    )


def graph_window() -> Component:
    """A window used to display the created graph.

    Returns:
        A html.div containing the created graph.
    """
    return html.Div(
        className="bg-white w-full ml-[3rem] my-[3rem] rounded-md shadow-md",
        children=[
            input_field("graph_name", "Graph name"),
            html.Div(id="graph_output"),
            x_axis_name(),
            y_axis_name(),
            file_name(),
        ],
    )


def create_fig(
    df: pl.DataFrame,
    graph_type: str,
    # graph_name: str,
    # x_axis_name: str,
    # y_axis_name: str,
    color_input: str,
    num: int,
    id="",
) -> go.Figure:
    """Creates a graph based on the chosen type by the user.

    Args:
        df: a dataframe containg used for creating the graph.
        graph_type: a string used to check what type of graph
        to draw.
        color_output: user chosen color of the graph
        num: the graph number
    if df is not None:
        graph_name: user chosen name of the graph.
        x_axis_name: user chosen name of the x-axis.
        y_axis_name: user chosen name of y-axis


    Returns:
        fig: a draw graph of the users choice with chosen
        names for the graph and axis.

    """
    # data = []
    if df is not None:
        # x1_list = df["x"].to_list()
        # y1_list = df["y"].to_list()

        if graph_type == "line":
            fig = go.Scatter(
                x=df["x"],
                y=df["y"],
                marker_color=color_input,
                mode="lines",
                name="graf " + str(num),
                uid=id
            )

        if graph_type == "scatter":
            fig = go.Scatter(
                x=df["x"],
                y=df["y"],
                marker_color=color_input,
                mode="markers",
                name="graf " + str(num),
            )

        if graph_type == "histo":
            fig = go.Histogram(
                # x=x1_list,
                x=df["y"],
                marker_color=color_input,
                name="graf " + str(num),
            )

    return fig


def top_right_settings() -> html.Div:
    """Buttons for the graph settings.

    Returns:
        html.Div: A div containing the buttons used for graph settings
    """
    # Container
    return html.Div(
        className="flex flex-col space-y-4",
        children=[
            html.Div(
                className="flex items-center",
                children=[
                    icon("settings", fill=1, size=36),
                    html.H1(
                        className="text-[1.5rem] w-full text-center", children="Customize graph"
                    ),
                ],
            ),
            upload_buttons(),
            radio_buttons(),
            download_buttons(),
            color_picker()

        ],
    )

def color_picker():
    return html.Div(
        className="flex flex-col",
        children=[
            html.Label("Line color"),
            dbc.Input(
                type="color",
                id="color_input",
                value="#0000FF",
                style={"width": 75, "height": 50},
                debounce=True,
            ),
        ]
    )

def upload_buttons() -> html.Div:
    """Buttons for uploading file.

    Returns:
        html.Div: Div with upload buttons with either CSV or database
    """
    return html.Div(
        className="flex flex-col",
        children=[
            html.P("Upload data"),
            html.Div(
                className="flex text-white",
                children=[
                    csv_button(),
                    button(
                        "database",
                        "Database",
                        size=18,
                        className="bg-[#636af2] hover:bg-[#2F3273] justify-center flex-1",
                    ),
                ],
            ),
        ],
    )


def radio_buttons() -> html.Div:
    """Radio buttons for the graph type.

    Returns:
        html.Div: Div with radio buttons
    """
    return html.Div(
        className="flex flex-col",
        children=[
            html.P("Plot type "),
            dcc.RadioItems(
                className="flex space-x-2",
                options=[
                    radio_item("Line", "line", "show_chart"),
                    radio_item("Bar", "histo", "bar_chart"),
                    radio_item("Scatter", "scatter", "scatter_plot"),
                ],
                inputClassName="peer hidden",
                value="line",
                labelStyle={"": ""},
                labelClassName="flex-1",
                id="choose_graph_type",
            ),
        ],
    )


def right_settings_bar() -> Component:
    """Right settings bar.

    Returns:
        A html.div containing all the settings components.
    """
    return html.Div(
        className="bg-white flex flex-col m-[3rem] p-[2rem] shadow-md rounded-lg",
        children=[
            top_right_settings(),
            # Lower part of the settings bar
            html.Div(
                className="flex mt-auto justify-center space-x-2 text-white",
                children=[
                    button(
                        "cancel",
                        "Cancel",
                        size=18,
                        id="cancel-graph",
                        className="bg-[#636af2] px-5 hover:bg-[#2F3273]",
                    ),
                    button(
                        "check",
                        "Create dashboard",
                        size=18,
                        id="create-graph",
                        className="bg-[#636af2] px-5 py-3 hover:bg-[#2F3273]",
                    ),
                ],
            ),
        ],
    )


@callback(Output("graph_1", "figure"), Input("color_input", "value"))
def choose_color1(color_input: str) -> dict[str, Any]:
    patched_figure = Patch()
    patched_figure["data"][0]["marker"]["color"] = color_input
    return patched_figure


def radio_item(name: str, value: str, icon_name: str) -> dict[str, html.Div]:
    """Creates a styled radio button.

    Args:
        name (str): Text that the radio should display
        value (str): checked value
        icon_name (str): name of the icon
    Returns:
        dict[str, html.Div]: Dictionary containing label and
        values required for dcc.RadioItems
    """
    classname = (
        "peer-checked:opacity-100 peer-checked:shadow-lg peer-checked:bg-[#03c04a] "
        "peer-checked:text-[#2f3273] flex flex-col items-center p-3 cursor-pointer "
        "bg-[#636af2] rounded-md shadow-md duration-150 hover:bg-[#2F3273] text-white"
    )
    return {
        "label": [
            html.Div(className=classname, children=[icon(icon_name, size=40), html.P(name)]),
        ],
        "value": value,
    }


def parse_contents(contents: str) -> pl.DataFrame:
    """Parses the input from a csv-file.

    Args:
        contents: the csv-file content.
        filename: the csv-file name.

    Returns:
        A parsed and read version of the csv-file.
    """
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)

    return pl.read_csv(io.StringIO(decoded.decode("utf-8")))

@callback(
    Output("num_graphs", "value"),
    Input("uploaded_data", "contents"),
)
def number_of_graphs(contents):
    return len(contents)

@callback(
    [Output("df_storage", "data")],
    Input("uploaded_data", "contents"),
)
def store_dataframe(contents: str) -> tuple[list[dict[str, list[Any]]]]:
    """Stores the uploaded frame in the form of a dataframe.

    Args:
        contents: uploaded csv-file the content.
        filename: name of the csv-file.

    Returns:
        The a json version of the dataframe from the
        parsed csv-file.
    """
    loc_list = []
    if contents is None:
        raise PreventUpdate

    try:
        for i in contents:
            temp_df = parse_contents(i)

            loc_list.append(temp_df)
        return ([df.to_dict(as_series=False) for df in loc_list],)

    except ValueError:
        raise PreventUpdate
    
@callback(
    Output("graph_id", "figure"),
    Input("color_input", "value"),
)
def patch_color(color):
    patched_figure = Patch()
    patched_figure["data"][0]["marker"] = {"color": color}
    return patched_figure
    

@callback(
    Output("graph_output", "children"),
    Input("df_storage", "data"),
    Input("choose_graph_type", "value"),
    Input("graph_name", "value"),
    Input("x_axis_name", "value"),
    Input("y_axis_name", "value"),
    Input("file_name", "value"),
    Input("download_png", "n_clicks"),
    Input("download_jpeg", "n_clicks"),
    Input("download_pdf", "n_clicks"),
    Input("download_html", "n_clicks"),
    Input("graph_index", "value")
)
def main(
    df_storage: Component,
    choose_graph_type: str,
    graph_name: str,
    x_axis_name: str,
    y_axis_name: str,
    file_name: str,
    download_png: bool,
    download_jpeg: bool,
    download_html: bool,
    download_pdf: bool,
    graph_index
) -> Component:
    """Main function for the code.

    Args:
        df_storage: the stored df frame in json format.
        choose_graph_type: the type of graph that shall be displayed.
        graph_name: user chosen name of the graph.
        x_axis_name: user chosen name of the x-axis.
        y_axis_name: user chosen name of y-axis
        download_png: button to download png of the graph
        download_jpeg: button to download jpeg of the graph
        download_pdf: button to download pdf of the graph
        download_html: button to download html of the graph

    Returns:
        A graph in the form of a plotly figure.

    Downloads:
        a png, jpeg, pdf or html image of the created graph
        into the folder /graph_images in the top folder

    """
    if graph_name == None:
        graph_name = "Graph name"
    if x_axis_name == None:
        x_axis_name = "x-axis name"
    if y_axis_name == None:
        y_axis_name = "y-axis name"
    if file_name == None:
        file_name = "filename"

    if df_storage is None:
        raise PreventUpdate
    if not os.path.exists("graph_images"):
        os.mkdir("graph_images")

    loc_config = {"doubleClick": "reset", "showTips": True, "displayModeBar": False}

    if df_storage is not None:
        data_frames = [pl.from_dict(x) for x in df_storage]

    created_figs = []
    for num, i in enumerate(data_frames):
        loc_fig = create_fig(
            i,
            choose_graph_type,
            # graph_name,
            # x_axis_name,
            # y_axis_name,
            "#000000",
            num + 1,
            id="graph_"+ str(num)
        )
        created_figs.append(loc_fig)
    
    
    layout = go.Layout(
        title=graph_name,
        # to not show grid-lines
        # , showgrid=False
        # to choose background color
        # plot_bgcolor="#FFFFFF",
        xaxis=dict(title=x_axis_name, linecolor=colors["black"], fixedrange=True),
        yaxis=dict(title=y_axis_name, linecolor=colors["black"], fixedrange=True),
        # paper_bgcolor="rgba(0,0,0,0)",
        # plot_bgcolor="rgba(0,0,0,0)"
    )

    fig = go.Figure(data=created_figs, layout=layout)

    print(fig.to_json())
    
    if download_png:
        fig.write_image(file=f'graph_images/{file_name}', format="png", width=1920, height=1080)
    if download_jpeg:
        fig.write_image("graph_images/" + file_name + ".jpeg", width=1920, height=1080)
    if download_pdf:
        fig.write_image("graph_images/" + file_name + ".pdf", width=1920, height=1080)
    if download_html:
        fig.write_html("graph_images/" + file_name + ".html")

    loc_graph = dcc.Graph(figure=fig, config=loc_config, id="graph_id")
    return loc_graph
