"""Graph display module.

This module displays different types of graphs based on input,
from either a csv-file or from a database.
"""
import base64
import io
import os

import dash
from dash import callback, dcc, html
from dash.dependencies import Component, Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px
import polars as pl

from dashboard.components import button, icon

dash.register_page(__name__, path="/create-graph", nav_item=False)

# for debugging
global debug
debug = True

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
            graph_window(),
            right_settings_bar(),
            dcc.Store(id="session_storage"),
            dcc.Store(id="df_storage"),
            dcc.Store(id="fig_storage"),
            # dcc.Download(id="download_pdf"),
            left_setting_bar(),
        ],
    )


def left_setting_bar() -> Component:
    """Left settings bar contaning.

    Returns:
        A component containing the csv_button and db_button.
    """
    # import button, and settings to the left
    return html.Div(  # change back to temp for debugging
        className=f"bg-[{colors['temp']}] flex flex-col items-center ml-5 px-5 h-[80%]" "w-[20%]",
        children=[
            # buttons for import and get from database
            html.Div(
                className=f'bg-[{colors["background"]}] flex flex-row mt-10 h-[12%] w-[100%]',
                children=[
                    # left button
                    csv_button(),
                    html.Div(id="csv_uploaded_data"),
                    # right button for getting data from the database
                    db_button(),
                    html.Div(id="output_left_setting_bar"),
                ],
            ),
            graph_name(),
            x_axis_name(),
            y_axis_name(),
            file_name(),
            download_png(),
            download_jpeg(),
            download_pdf(),
            download_html()
            # download_as_pdf(),
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
        # false so multiple files cant be uploaded
        multiple=False,
    )


def db_button() -> Component:
    """NOT IN USE: button to get data from a database."""
    return html.Button(
        className=f"bg-[{colors['meny_back']}] flex flex-col px-4 justify-center"
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


def download_png() -> Component:
    """NOT IN USE: button to get data from a database."""
    return html.Button(
        className=f"bg-[{colors['meny_back']}] flex flex-col mt-4 px-4 justify-center"
        " border-2 border-black",
        children=[
            html.Div(
                # className=f'bg-[{colors["background"]}',
                children=[
                    html.P(
                        "Download as png",
                        style={"color": colors["black"]},
                    ),
                ],
            )
        ],
        id="download_png",
        n_clicks=0,
    )


def download_jpeg() -> Component:
    """NOT IN USE: button to get data from a database."""
    return html.Button(
        className=f"bg-[{colors['meny_back']}] flex flex-col mt-4 px-4 justify-center"
        " border-2 border-black",
        children=[
            html.Div(
                # className=f'bg-[{colors["background"]}',
                children=[
                    html.P(
                        "Download as jpeg",
                        style={"color": colors["black"]},
                    ),
                ],
            )
        ],
        id="download_jpeg",
        n_clicks=0,
    )


def download_pdf() -> Component:
    """NOT IN USE: button to get data from a database."""
    return html.Button(
        className=f"bg-[{colors['meny_back']}] flex flex-col mt-4 px-4 justify-center"
        " border-2 border-black",
        children=[
            html.Div(
                # className=f'bg-[{colors["background"]}',
                children=[
                    html.P(
                        "Download as pdf",
                        style={"color": colors["black"]},
                    ),
                ],
            )
        ],
        id="download_pdf",
        n_clicks=0,
    )


def download_html() -> Component:
    """NOT IN USE: button to get data from a database."""
    return html.Button(
        className=f"bg-[{colors['meny_back']}] flex flex-col mt-4 px-4 justify-center"
        " border-2 border-black",
        children=[
            html.Div(
                # className=f'bg-[{colors["background"]}',
                children=[
                    html.P(
                        "Download as html",
                        style={"color": colors["black"]},
                    ),
                ],
            )
        ],
        id="download_html",
        n_clicks=0,
    )


def graph_name():
    """Takes user input for the graph label"""
    return dcc.Input(
        className=f"bg-[{colors['background']}] flex items-center justify-center mt-5 p-2 h-[30%]",
        id="graph_name",
        type="text",
        debounce=True,
        placeholder="Graph name",
    )


def x_axis_name():
    """Takes user input for the x axis label"""
    return dcc.Input(
        className=f"bg-[{colors['background']}] flex items-center justify-center mt-5 p-2 h-[30%]",
        id="x_axis_name",
        type="text",
        debounce=True,
        placeholder="x-axis name",
    )


def y_axis_name():
    """Takes user input for the y axis label"""
    return dcc.Input(
        className=f"bg-[{colors['background']}] flex items-center justify-center mt-5 p-2 h-[30%]",
        id="y_axis_name",
        type="text",
        debounce=True,
        placeholder="y-axis name",
    )


def file_name():
    """Takes user input for the graph label"""
    return dcc.Input(
        className=f"bg-[{colors['background']}] flex items-center justify-center mt-5 p-2 h-[30%]",
        id="file_name",
        type="text",
        debounce=True,
        placeholder="File name",
    )


def graph_window() -> Component:
    """A window used to display the created graph.

    Returns:
        A html.div containing the created graph.
    """
    return html.Div(
        className="bg-white w-full ml-[3rem] my-[3rem] rounded-md shadow-md",
        children=[html.Div(id="graph_output"),
        ],
    )


def create_fig(
    df: pl.DataFrame, graph_type: str, graph_name: str, x_axis_name: str, y_axis_name: str
) -> Component:
    """Creates a graph based on the chosen type by the user.

    Args:
        df: a dataframe containg used for creating the graph.
        graph_type: a string used to check what type of graph
        to draw.
    if df is not None:
        graph_name: user chosen name of the graph.
        x_axis_name: user chosen name of the x-axis.
        y_axis_name: user chosen name of y-axis


    Returns:
        fig: a draw graph of the users choice with chosen
        names for the graph and axis.

    """
    if df is not None:
        if graph_type == "line":
            fig = px.line(
                df,
                x=list(df["x"]),
                y=list(df["y"]),
                labels={
                    "x": x_axis_name,
                    "y": y_axis_name,
                },
                title=graph_name,
            )
        if graph_type == "scatter":
            fig = px.scatter(
                df,
                x=list(df["x"]),
                y=list(df["y"]),
                labels={
                    "x": x_axis_name,
                    "y": y_axis_name,
                },
                title=graph_name,
            )
        if graph_type == "line":
            fig = px.line(df, x=list(df["x"]), y=list(df["y"]), title="Test graph from csv file")
        if graph_type == "histo":
            fig = px.histogram(df, x=list(df["x"]), title="Test graph from csv file")
        return dcc.Graph(className="m-5 shadow-md", figure=fig)


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
        ],
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
                value="line",
                id="choose_graph_type",
            ),
        ],
    )


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


def parse_contents(contents: str, filename: str) -> pl.DataFrame:
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
    [Output("df_storage", "data")],
    Input("uploaded_data", "contents"),
    State("uploaded_data", "filename"),
)
def store_dataframe(contents: str, filename: str) -> str:
    """Stores the uploaded frame in the form of a dataframe.

    Args:
        contents: uploaded csv-file the content.
        filename: name of the csv-file.

    Returns:
        The a json version of the dataframe from the
        parsed csv-file.
    """

    if contents is None:
        raise PreventUpdate

    try:
        df = parse_contents(contents, filename)

    except ValueError:
        raise PreventUpdate

    return [df.write_json()]


@callback(
    Output("graph_output", "children"),
    # Output("fig_test", "data"),
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
)
def update_main(
    df_storage,
    choose_graph_type: str,
    graph_name: str,
    x_axis_name: str,
    y_axis_name: str,
    file_name: str,
    download_png,
    download_jpeg,
    download_html,
    download_pdf,
) -> Component:
    """Update_output creates graph from a stored dataframe.

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

    df = pl.read_json(io.StringIO(df_storage))
    loc_fig = create_fig(df, choose_graph_type, graph_name, x_axis_name, y_axis_name)

    if not os.path.exists("graph_images"):
        os.mkdir("graph_images")

    if download_png:
        loc_fig.write_image("graph_images/" + file_name + ".png", width=1920, height=1080)
    if download_jpeg:
        loc_fig.write_image("graph_images/" + file_name + ".jpeg", width=1920, height=1080)
    if download_pdf:
        loc_fig.write_image("graph_images/" + file_name + ".pdf", width=1920, height=1080)
    if download_html:
        loc_fig.write_html("graph_images/" + file_name + ".html")

    loc_graph = dcc.Graph(figure=loc_fig)

    return loc_graph
