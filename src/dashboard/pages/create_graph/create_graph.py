"""Graph display module.

This module displays different types of graphs based on input,
from either a csv-file or from a database.
"""

import base64
import io
from typing import Any

import dash
from dash import Patch, State, callback, dcc, html
from dash.dependencies import Component, Input, Output
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import jsonpickle
import plotly.graph_objs as go
import polars as pl

from dashboard.components import button, icon

dash.register_page(__name__, path="/create-graph", nav_item=False)

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
        className="bg-background flex h-screen",
        children=[
            graph_window(),
            right_settings_bar(),
            dcc.Download(id="download_fig"),
            dcc.Input(id="graph_index", value=0, className="hidden"),
            dcc.Input(id="fig_json", className="hidden"),
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


def download_button(icon: str, text: str, id: str) -> html.Button:
    """Predefined button style.

    Args:
        icon str: icon for the button
        text str: text for button
        id str: button id

    Returns:
        html.Button: Styled button used for download buttons
    """
    return button(
        icon_name=icon,
        text=text,
        id=id,
        className="bg-menu-back hover:bg-dark-purple justify-center flex-1 text-white",
    )


def download_buttons() -> html.Div:
    """Div containing the download buttons.

    Returns:
        html.Div: Div with download buttons
    """
    return html.Div(
        className="flex flex-col",
        children=[
            html.P("Download as"),
            file_name(),
            html.Div(
                className="flex space-x-2 mt-2",
                children=[
                    download_button(icon="image", text="Png", id="download_png"),
                    download_button(icon="image", text="Jpeg", id="download_jpeg"),
                    download_button(icon="picture_as_pdf", text="Pdf", id="download_pdf"),
                    download_button(icon="html", text="Html", id="download_html"),
                ],
            ),
        ],
    )


def figure_name() -> Component:
    """Takes user input for the graph label."""
    return input_field("figure_name", "Figure name")


def x_axis_name() -> Component:
    """Takes user input for the x axis label."""
    return input_field("x_axis_name", "x-axis name")


def y_axis_name() -> Component:
    """Takes user input for the y axis label."""
    return input_field("y_axis_name", "y-axis name")


def file_name() -> Component:
    """Takes user input for the graph label."""
    return input_field("file_name", "File name")


def input_field(loc_id: str, loc_placeholder: str, disabled: bool = True) -> Component:
    """Input_field that lets user choose a color.

    Args:
        loc_id: local id of the input field
        loc_placeholder: a placeholder color

    Returns:
        Component: epic component
    """
        
    return dcc.Input(
        className="bg-white flex items-center "
        "justify-center mt-5 p-3 rounded-md shadow-inner border-2",
        id=loc_id,
        type="text",
        debounce=True,
        placeholder=loc_placeholder,
        disabled=disabled,
    )


def graph_window() -> Component:
    """A window used to display the created graph.

    Returns:
        A html.div containing the created graph.
    """
    return html.Div(
        className="bg-white w-full ml-[3rem] my-[3rem] rounded-md shadow-md",
        children=[
            html.Div(className="h-[70] flex w-full flex-1 p-5", children=[
                html.Div(className="border-2 rounded-md h-full w-full shadow-inner", id="graph_output")]),
            html.Div(className = "flex flex-row space-x-2 mt-4 justify-center",
                     children=[
                        input_field("figure_name", "Figure name"),
                        x_axis_name(),
                        y_axis_name(),
                        ])

        ],
    )


def create_fig(
    df: pl.DataFrame,
    graph_type: str,
    color_input: str,
    name: str,
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
        y_axis_name: user chosen name of y-axis.

    Returns:
        fig: a draw graph of the users choice with chosen
        names for the graph and axis.
    """
    cols = df.columns
    fig = None
    if df is not None:
        if graph_type == "line":
            fig = go.Scatter(
                x=df[cols[0]],
                y=df[cols[1]],
                marker_color=color_input,
                mode="lines",
                name=name,
            )

        if graph_type == "scatter":
            fig = go.Scatter(
                x=df[cols[0]],
                y=df[cols[1]],
                marker_color=color_input,
                mode="markers",
                name=name,
            )

        if graph_type == "bar":
            fig = go.Bar(
                x=df[cols[0]],
                y=df[cols[1]],
                marker_color=color_input,
                name=name,
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
            dropdown(),
            input_field("graph_name", "Name graph", disabled=True),
            radio_buttons(),
            download_buttons(),
            color_picker(),
        ],
    )


def dropdown() -> dcc.Dropdown:
    """Makes a dcc dropdown to pick graphs.

    Returns:
        dcc.Dropdown: dropdown containing all of the uploaded graphs
    """
    return dcc.Dropdown([], placeholder="Select graph", id="graph_selector")


def color_picker() -> html.Div:
    """Color picker element.

    Returns:
        html.Div: Element with color picker
    """
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
                        className="bg-menu-back hover:bg-dark-purple justify-center flex-1",
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
                    radio_item("Bar", "bar", "bar_chart"),
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
                        className="bg-menu-back px-5 hover:bg-dark-purple",
                    ),
                    button(
                        "check",
                        "Create graph",
                        size=18,
                        id="create-graph",
                        className="bg-menu-back px-5 py-3 hover:bg-dark-purple",
                    ),
                ],
            ),
        ],
    )


@callback(Output("graph_index", "value"), Input("graph_selector", "value"))
def dropdown_select_graph(graph_value: int) -> int:
    """Stores the current selectd graph index.

    Args:
        graph_value (int): The index of the graph to select

    Returns:
        int: Graph index
    """
    return graph_value


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
    
    content_string = contents.split(",")[-1]
    
    decoded = base64.b64decode(content_string)

    return pl.read_csv(io.StringIO(decoded.decode("utf-8")))


def convert_to_dataframe(contents: str) -> list[dict[str, list[Any]]]:
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
        return [df.to_dict(as_series=False) for df in loc_list]

    except ValueError:
        raise PreventUpdate


@callback(
    Output("graph_id", "figure", allow_duplicate=True),
    Input("choose_graph_type", "value"),
    State("graph_id", "figure"),
    State("graph_index", "value"),
    State("graph_name", "value"),
    prevent_initial_call=True,
)
def patch_graph_type(
    graph_type: str, graph_data: dict[str, list[Any]], i: int, graph_name: str
) -> Patch:
    """A patched figure object that patches the graph type.

    Args:
        graph_type (str): The new graph type
        graph_data (_type_): Current graph data
        i (int): Graph index

    Returns:
        Patch: Patched figure with new graph type
    """
    data_frame = pl.DataFrame({"x": graph_data["data"][i]["x"], "y": graph_data["data"][i]["y"]})
    color = graph_data["data"][i]["marker"]
    patched_figure = Patch()
    patched_figure["data"][i] = create_fig(
        data_frame, graph_type=graph_type, color_input=color["color"], name=graph_name
    )
    return patched_figure


@callback(
    Output("graph_id", "figure", allow_duplicate=True),
    Input("color_input", "value"),
    State("graph_index", "value"),
    prevent_initial_call=True,
)
def patch_color(color: str, i: int) -> Patch:
    """Patched figure with new selected line color.

    Args:
        color (str): New color
        i (int): Graph index

    Returns:
        Patch: Patched figure object with new color
    """
    patched_figure = Patch()
    patched_figure["data"][i]["marker"] = {"color": color}
    return patched_figure


@callback(
    Output("graph_id", "figure", allow_duplicate=True),
    Input("graph_name", "value"),
    State("graph_index", "value"),
    prevent_initial_call=True,
)
def patch_graph_name(name: str, index: int) -> Patch:
    """Updates a selected graphs name.

    Args:
        name (str): Name of the graph
        index (int): Selected graph index

    Returns:
        Patch: New figure with patched graph name
    """
    patched_figure = Patch()
    patched_figure["data"][index]["name"] = name
    return patched_figure


@callback(
    Output("download_fig", "data"),
    Input("download_png", "n_clicks"),
    State("fig_json", "value"),
    State("file_name", "value"),
    prevent_initial_call=True,
)
def download_fig(n_clicks: int, fig_json: str, file_name: str) -> Any:
    """Callback for downloading figures.

    Args:
        n_clicks (int): number of clicks
        fig_json (str): figure stored as a json string
        file_name (str): desired filename

    Returns:
        dict[str, Any | None]: The file download
    """
    figure = jsonpickle.decode(fig_json)
    return dcc.send_bytes(figure.write_image, f"{file_name}.png")


@callback(
    Output("graph_id", "figure", allow_duplicate=True),
    Input("figure_name", "value"),
    prevent_initial_call=True,
)
def patch_figure_name(name: str) -> Patch:
    """Patches figure title.

    Args:
        name (str): figure title

    Returns:
        Patch: Patched figure with new title
    """
    patched_figure = Patch()
    patched_figure["layout"]["title"]["text"] = name
    return patched_figure


@callback(
    Output("graph_id", "figure", allow_duplicate=True),
    Input("x_axis_name", "value"),
    Input("y_axis_name", "value"),
    prevent_initial_call=True,
)
def patch_axis_names(x: str, y: str) -> Patch:
    """Renames figure graph names.

    Args:
        x (str): x-axis name
        y (str): y-axis name

    Returns:
        Patch: Patched figure with new axis names
    """
    patched_figure = Patch()
    patched_figure["layout"]["xaxis"]["title"] = x
    patched_figure["layout"]["yaxis"]["title"] = y
    return patched_figure

@callback(
    Output("figure_name", "disabled"),
    Output("graph_name", "disabled"),
    Output("file_name", "disabled"),
    Output("x_axis_name", "disabled"),
    Output("y_axis_name", "disabled"),
    Input("uploaded_data", "contents"),
    prevent_initial_call=True
)
def enable_inputs(contents):
    return False, False, False, False, False

@callback(
    Output("graph_output", "children"),
    Output("graph_selector", "options"),
    Output("graph_selector", "value"),
    Output("fig_json", "value"),
    Input("uploaded_data", "contents"),
)
def render_figure(contents: str) -> dcc.Graph | list[dict[str, str]]:
    """Renders the figure using CSV-files.

    Returns:
        dcc.Graph: Graph to be rendered
        list[dict[str: str]]: list of all the graph names
    """
    created_figs = []
    figure_names = []
    data_frame = convert_to_dataframe(contents)

    data_frames = [pl.from_dict(x) for x in data_frame]
    for num, i in enumerate(data_frames):
        loc_fig = create_fig(i, "line", "#000000", name=f"Graph {num}")
        figure_names.append({"label": loc_fig["name"], "value": num})
        created_figs.append(loc_fig)

    loc_config = {"doubleClick": "reset", "showTips": True, "displayModeBar": False}
    fig = go.Figure(data=created_figs)
    loc_graph = dcc.Graph(figure=fig, id="graph_id", config=loc_config)
    pickle = jsonpickle.encode(fig)
    return loc_graph, figure_names, figure_names[0]["value"], pickle
