"""The controller for create_graph."""

from typing import Any, Tuple

from dash import Input, Output, Patch, State, callback, dcc
from dash.exceptions import PreventUpdate
import plotly.graph_objs as go
import polars as pl

from dashboard.components import trace
from dashboard.components.trace import TraceType
from dashboard.utilities import convert_to_dataframes
from dashboard.models import db
from dashboard.models.data import Data, DataType, XyData
from bson.objectid import ObjectId
import polars as pl


@callback(
    Output("graph_id", "figure", allow_duplicate=True),
    Input("choose_graph_type", "value"),
    State("graph_id", "figure"),
    State("graph_selector", "value"),
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
    try:
        trace_type = TraceType(graph_type)
    except ValueError as err:
        raise PreventUpdate from err

    data_frame = pl.DataFrame({"x": graph_data["data"][i]["x"], "y": graph_data["data"][i]["y"]})
    color = graph_data["data"][i]["marker"]
    patched_figure = Patch()
    patched_figure["data"][i] = trace(data_frame, trace_type, color["color"], graph_name)
    return patched_figure


@callback(
    Output("graph_id", "figure", allow_duplicate=True),
    Input("color_input", "value"),
    State("graph_selector", "value"),
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
    patched_figure["data"][i]["marker"]["color"] = color
    return patched_figure


@callback(
    Output("graph_id", "figure", allow_duplicate=True),
    Input("graph_name", "value"),
    State("graph_selector", "value"),
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
    patched_figure = Patch()
    patched_figure["data"][i]["name"] = name
    return patched_figure


@callback(
    Output("download_fig", "data"),
    Input("download_png", "n_clicks"),
    State("graph_id", "figure"),
    State("file_name", "value"),
    prevent_initial_call=True,
)
def download_fig(n_clicks: int, fig_dict: dict[str, Any], file_name: str) -> Any:
    """Callback for downloading figures.

    Args:
        n_clicks (int): number of clicks
        fig_dict (dict[str, Any]): figure to download as dictionary
        file_name (str): desired filename

    Returns:
        Any: The file download
    """
    try:
        fig = go.Figure(fig_dict)
    except ValueError as val_err:
        raise PreventUpdate from val_err

    return dcc.send_bytes(fig.write_image, f"{file_name}.png")


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
    Output("graph_id", "figure"),
    Output("graph_selector", "options"),
    Output("graph_selector", "value"),
    Output("graph_name", "disabled"),
    Input("uploaded_data", "contents"),
    prevent_initial_call=True,
)
def render_figure_from_upload(
    contents: list[str],
) -> Tuple[go.Figure, list[dict[str, str | int]], int, bool]:
    data_frames = convert_to_dataframes(contents)
    return render_figure(data_frames)


def render_figure(
    data_frames: list[pl.DataFrame],
) -> Tuple[go.Figure, list[dict[str, str | int]], int, bool]:
    """Renders the figure using CSV-files.

    Returns:
        dcc.Graph: Graph to be rendered
        list[dict[str: str]]: list of all the graph names
    """
    created_figs: list[go.Scatter | go.Bar] = []
    figure_names: list[dict[str, str | int]] = []

    for num, df in enumerate(data_frames):
        loc_fig = trace(df, TraceType.LINE, "#000000", name=f"Graph {num}")
        label: str = loc_fig["name"]
        figure_names.append({"label": label, "value": num})
        created_figs.append(loc_fig)

    fig = go.Figure(
        data=created_figs,
        layout=go.Layout(
            plot_bgcolor="#FFFFFF",
            xaxis=go.layout.XAxis(linecolor="black", gridcolor="gray"),
            yaxis=go.layout.YAxis(linecolor="black", gridcolor="gray"),
        ),
    )

    return fig, figure_names, 0, False


@callback(
    Output({"type": "modal-dialog", "id": "database_dialog"}, "open", allow_duplicate=True),
    Output("project_selector", "options"),
    Input("database_button", "n_clicks"),
    prevent_initial_call=True,
)
def open_database_dialog(n_clicks: int) -> Tuple[bool, list[dict[str, str]]]:
    """Opens the database dialog."""
    project_dbs = db.list_project_dbs()
    print(project_dbs)
    database_dialog_open = True
    project_selector_options = [
        {"label": project_db, "value": project_db}
        for project_db in project_dbs
        # {"label": "works", "value": "WORKS?"}
    ]
    return database_dialog_open, project_selector_options


@callback(
    Output("document_selector", "disabled"),
    Output("document_selector", "options"),
    Input("project_selector", "value"),
    prevent_initial_call=True,
)
def populate_document_selector(project_db: str) -> Tuple[bool, list[dict[str, str]]]:
    """Opens the database dialog."""
    if project_db is None:
        document_selector_disabled = True
        document_selector_options = []
    else:
        db.connect_data_db(project_db)
        document_selector_disabled = False
        document_selector_options = [
            {"label": document.name, "value": str(document.id)}
            for document in Data.objects()
            # {"label": "works", "value": "WORKS!"}
        ]

    return document_selector_disabled, document_selector_options


@callback(
    Output("database_dialog_select", "disabled"),
    Input("document_selector", "value"),
    prevent_initial_call=True,
)
def enable_database_dialog_select(document_id: str):
    return False


@callback(
    Output({"type": "modal-dialog", "id": "database_dialog"}, "open", allow_duplicate=True),
    Output("project_selector", "options", allow_duplicate=True),
    Output("document_selector", "disabled", allow_duplicate=True),
    Output("document_selector", "options", allow_duplicate=True),
    Output("graph_id", "figure", allow_duplicate=True),
    Output("graph_selector", "options", allow_duplicate=True),
    Output("graph_selector", "value", allow_duplicate=True),
    Output("graph_name", "disabled", allow_duplicate=True),
    Input("database_dialog_select", "n_clicks"),
    State("document_selector", "value"),
    prevent_initial_call=True,
)
def close_database_dialog(n_clicks: int, document_id: str):
    """Handle closing of the database dialog."""

    document: Data = Data.objects.get(id=ObjectId(document_id), type=DataType.XY_PLOT.value)

    xy_data: XyData = document.resolve()

    df = pl.DataFrame({"x": xy_data.x, "y": xy_data.y})

    return False, [], True, [], *render_figure([df])
