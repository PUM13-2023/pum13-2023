from typing import Any, Tuple

from dash import Input, Output, Patch, State, callback, dcc, no_update
import jsonpickle
import plotly.graph_objs as go
import polars as pl

from dashboard.components import trace
from dashboard.components.trace import GraphTypes
from dashboard.utilities import convert_to_dataframes


@callback(Output("graph_index", "value"), Input("graph_selector", "value"))
def dropdown_select_graph(graph_value: int) -> int:
    """Stores the current selectd graph index.

    Args:
        graph_value (int): The index of the graph to select

    Returns:
        int: Graph index
    """
    return graph_value


@callback(
    Output("graph_id", "figure", allow_duplicate=True),
    Input("choose_graph_type", "value"),
    State("graph_id", "figure"),
    State("graph_index", "value"),
    State("graph_name", "value"),
    prevent_initial_call=True,
)
def patch_graph_type(
    graph_type: GraphTypes, graph_data: dict[str, list[Any]], i: int, graph_name: str
) -> Patch:
    """A patched figure object that patches the graph type.

    Args:
        graph_type (str): The new graph type
        graph_data (_type_): Current graph data
        i (int): Graph index

    Returns:
        Patch: Patched figure with new graph type
    """
    i = int(i)  # NOTE: for some reason this is a string...
    data_frame = pl.DataFrame({"x": graph_data["data"][i]["x"], "y": graph_data["data"][i]["y"]})
    color = graph_data["data"][i]["marker"]
    patched_figure = Patch()
    patched_figure["data"][i] = trace(
        data_frame, trace_type=graph_type, color_input=color["color"], name=graph_name
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
    i = int(i)  # NOTE: for some reason this is a string...
    patched_figure = Patch()
    patched_figure["data"][i]["marker"] = {"color": color}
    return patched_figure


@callback(
    Output("graph_id", "figure", allow_duplicate=True),
    Input("graph_name", "value"),
    State("graph_index", "value"),
    prevent_initial_call=True,
)
def patch_graph_name(name: str, i: int) -> Patch:
    """Updates a selected graphs name.

    Args:
        name (str): Name of the graph
        index (int): Selected graph index

    Returns:
        Patch: New figure with patched graph name
    """
    i = int(i)  # NOTE: for some reason this is a string...
    patched_figure = Patch()
    patched_figure["data"][i]["name"] = name
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
    if not isinstance(figure, go.Figure):
        return no_update

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
    Output("graph_output", "children"),
    Output("graph_selector", "options"),
    Output("graph_selector", "value"),
    Output("fig_json", "value"),
    Output("graph_name", "disabled"),
    Input("uploaded_data", "contents"),
    prevent_initial_call=True,
)
def render_figure(
    contents: list[str],
) -> Tuple[dcc.Graph, list[dict[str, str | int]], str, str, bool]:
    """Renders the figure using CSV-files.

    Returns:
        dcc.Graph: Graph to be rendered
        list[dict[str: str]]: list of all the graph names
    """
    created_figs: list[go.Scatter | go.Bar] = []
    figure_names: list[dict[str, str | int]] = []
    data_frames = convert_to_dataframes(contents)

    for num, i in enumerate(data_frames):
        loc_fig = trace(i, "line", "#000000", name=f"Graph {num}")
        label: str = loc_fig["name"]
        figure_names.append({"label": label, "value": num})
        created_figs.append(loc_fig)

    loc_config = {"doubleClick": "reset", "showTips": True, "displayModeBar": False}
    fig = go.Figure(data=created_figs)
    loc_graph = dcc.Graph(figure=fig, id="graph_id", config=loc_config)
    pickle: str | None = jsonpickle.encode(fig)
    if pickle is None:
        return no_update, no_update, no_update, no_update, no_update

    return loc_graph, figure_names, str(figure_names[0]["value"]), pickle, False
