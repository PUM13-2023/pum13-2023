"""Graph display module.

This module displays different types of graphs based on input,
from either a csv-file or from a database.
"""

import base64
import io
import json
import os

import dash
from dash import callback, dcc, html
from dash.dependencies import Component, Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_daq as daq
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
            dcc.Store(id="df_storage1"),
            dcc.Store(id="df_storage2"),
            # dcc.Download(id="download_pdf"),
            left_setting_bar(),
            graph_window(),
            # dcc.Graph(id="test_graph"),
            right_settings_bar(),
            html.Plaintext(id="color_output1"),
            html.Plaintext(id="color_output2"),
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
            html.Div(
                className=f'bg-[{colors["background"]}] flex flex-row mt-4 h-[12%] w-[100%]',
                children=[
                    # left button
                    csv_button(),
                    # html.Div(id="csv_uploaded_data"),
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
            download_html(),
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


def db_button() -> Component:
    """NOT IN USE: button to get data from a database."""
    return button2("Get from database", "database_button")


def download_png() -> Component:
    """Called to download the created graph as png"""
    return button2("Download as png", "download_png")


def download_jpeg() -> Component:
    """Called to download the created graph as jpeg"""
    return button2("Download as jpg", "download_jpeg")


def download_pdf() -> Component:
    """Called to download the created graph as pdf"""
    return button2("Download as pdf", "download_pdf")


def download_html() -> Component:
    """Called to download the created graph as html"""
    return button2("Download as html", "download_html")


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
        className=f"bg-[{colors['background']}] flex items-center justify-center mt-5 p-2 h-[30%]",
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
        children=[html.Div(id="graph_output"),
        ],
    )


def right_settings_bar_2() -> Component:
    """Right settings bar.

    Returns:
        A html.div containing all the settings components.
    """
    return html.Div(  # change back to debug for debugging
        className=f"bg-[{colors['debug']}] flex flex-col items-center justify-center"
        " h-[80%] w-[20%]",
        children=[
            html.Div("Graph type for graph 1"),
            dcc.RadioItems(
                options=[
                    {"label": "linjediagram", "value": "line"},
                    {"label": "scatter plot", "value": "scatter"},
                    {"label": "histogram", "value": "hist"},
                ],
                value="line",
                id="choose_graph_type",
            ),
            html.Div("Graph type for graph 2"),
            dcc.RadioItems(
                options=[
                    {"label": "linjediagram", "value": "line2"},
                    {"label": "scatter plot", "value": "scatter2"},
                    {"label": "histogram", "value": "hist2"},
                ],
                value="line2",
                id="choose_graph_type2",
            ),
            
        ],
    )


@callback(Output("color_output1", "style"), Input("color_input1", "value"))
def choose_color1(color_input1):
    print("color_input ", color_input1)
    return {"color": color_input1}


@callback(Output("color_output2", "style"), Input("color_input2", "value"))
def choose_color1(color_input2):
    print("color_input ", color_input2)
    return {"color": color_input2}


# def create_fig(
#     df: pl.DataFrame, graph_type: str, graph_name: str, x_axis_name: str, y_axis_name: str
# ) -> Component:
#     """Creates a graph based on the chosen type by the user.

#     Args:
#         df: a dataframe containg used for creating the graph.
#         graph_type: a string used to check what type of graph
#         to draw.
#         graph_name: user chosen name of the graph.
#         x_axis_name: user chosen name of the x-axis.
#         y_axis_name: user chosen name of y-axis


#     Returns:
#         fig: a draw graph of the users choice with chosen
#         names for the graph and axis.

#     """

#     if df is not None:
#         if graph_type == "line":
#             fig = px.line(
#                 df,
#                 x=list(df["x"]),
#                 y=list(df["y"]),
#                 labels={
#                     "x": x_axis_name,
#                     "y": y_axis_name,
#                 },
#                 title=graph_name,
#             )
#         if graph_type == "scatter":
#             fig = px.scatter(
#                 df,
#                 x=list(df["x"]),
#                 y=list(df["y"]),
#                 labels={
#                     "x": x_axis_name,
#                     "y": y_axis_name,
#                 },
#                 title=graph_name,
#             )

#         if graph_type == "hist":
#             fig = px.histogram(
#                 df,
#                 x=list(df["x"]),
#                 labels={
#                     "x": x_axis_name,
#                 },
#                 title=graph_name,
#             )

#     return fig


def create_fig(
    df1: pl.DataFrame,
    df2: pl.DataFrame,
    graph_type: str,
    graph_type2: str,
    graph_name: str,
    x_axis_name: str,
    y_axis_name: str,
    color_output1,
    color_output2,
):
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

    # loc_graph = dcc.Graph(
    #     figure={
    #         "data": [
    #             {
    #                 "x": list(df1["x"]),
    #                 "y": list(df1["y"]),
    #                 "type": graph_type,
    #                 "name": "graph1",
    #             },
    #             {"x": list(df2["x"]), "y": list(df2["y"]), "type": graph_type, "name": "graph2"},
    #         ],
    #         "layout": {
    #             "title": "testgraph",
    #             "name": "test",
    #             "x": "test",
    #             "xname": "test",
    #             "xlabel": "test",
    #             "style": "test",
    #         },
    #     }
    # )
    # return loc_graph
    ###SOMETHING ELSE

    print("create_fig ", color_output1["color"])
    data = []
    if df1 is not None:
        # x1_list = df1["x"].to_list()
        # y1_list = df1["y"].to_list()

        if graph_type == "line":
            fig1 = go.Scatter(
                x=df1["x"],
                y=df1["y"],
                marker_color=color_output1["color"],
                mode="lines",
                name="graf 1",
            )

        if graph_type == "scatter":
            fig1 = go.Scatter(
                x=df1["x"],
                y=df1["y"],
                marker_color=color_output1["color"],
                mode="markers",
                name="graf 1",
            )

        if graph_type == "hist":
            fig1 = go.Histogram(
                # x=x1_list,
                x=df1["y"],
                marker_color=color_output1["color"],
                name="graf 1",
            )
        data.append(fig1)

    if df2 is not None:
        if graph_type2 == "line2":
            fig2 = go.Scatter(
                x=df2["x"],
                y=df2["y"],
                marker_color=color_output2["color"],
                mode="lines",
                name="graf 2",
            )
        if graph_type2 == "scatter2":
            fig2 = go.Scatter(
                x=df2["x"],
                y=df2["y"],
                marker_color=color_output2["color"],
                mode="markers",
                name="graf 2",
            )

        if graph_type2 == "hist2":
            fig2 = go.Histogram(
                x=df2["y"],
                # x=df2["x"],
                marker_color=color_output2["color"],
                name="graf 2",
            )
        data.append(fig2)

    # print("colors test ", colors["background"])
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
    fig = go.Figure(data=data, layout=layout)
    print("fig test ", fig)

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
                    dbc.Label("Choose color for graph 1 "),
                    dbc.Input(
                        type="color",
                        id="color_input1",
                        value="#0000FF",
                        style={"width": 75, "height": 50},
                        debounce=True,
                    ),
                    dbc.Label("Choose color for graph 2 "),
                    dbc.Input(
                        type="color",
                        id="color_input2",
                        value="#FF0000",
                        style={"width": 75, "height": 50},
                        debounce=True,
                    ),
                ],
            
            ),
        ],
    )


@callback(Output("color_picker_output1", "value"), Input("color_picker1", "value"))
def update_output(value):
    return value


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
    # [Output("df_storage", "dict")],
    [Output("df_storage1", "data"), Output("df_storage2", "data")],
    Input("uploaded_data", "contents"),
    State("uploaded_data", "filename"),
)
def store_dataframe(contents: str, filename: str) -> list[str]:
    """Stores the uploaded frame in the form of a dataframe.

    Args:
        contents: uploaded csv-file the content.
        filename: name of the csv-file.

    Returns:
        The a json version of the dataframe from the
        parsed csv-file.
    """
    # print("contents ", contents)
    # print("contents[0] ", contents[0])
    # print("contents[1] ", contents[1])
    # print("len(contents) ", len(contents))
    # print("filename", filename)
    # if contents is None:
    #     raise PreventUpdate

    # try:
    #     df = parse_contents(contents, filename)

    # except ValueError:
    #     raise PreventUpdate

    if contents is None:
        raise PreventUpdate

    try:
        if len(contents) == 2:
            df1 = parse_contents(contents[0], filename)
            df2 = parse_contents(contents[1], filename)
            # test = json.dumps({"graph1": df1, "graph2": df2})
            # return test
            return [df1.write_json(), df2.write_json()]

        else:
            df1 = parse_contents(contents[0], filename)
            return [df1.write_json(), None]
    except ValueError:
        raise PreventUpdate

    # print("df1 ", df1)
    # print("df2 ", df2)


@callback(
    Output("graph_output", "children"),
    # Output("test_graph", "figure"),
    Input("df_storage1", "data"),
    Input("df_storage2", "data"),
    Input("choose_graph_type", "value"),
    Input("choose_graph_type2", "value"),
    Input("graph_name", "value"),
    Input("x_axis_name", "value"),
    Input("y_axis_name", "value"),
    Input("file_name", "value"),
    Input("download_png", "n_clicks"),
    Input("download_jpeg", "n_clicks"),
    Input("download_pdf", "n_clicks"),
    Input("download_html", "n_clicks"),
    Input("color_output1", "style"),
    Input("color_output2", "style"),
)
def main(
    df_storage1: Component,
    df_storage2: Component,
    choose_graph_type: str,
    choose_graph_typ2: str,
    graph_name: str,
    x_axis_name: str,
    y_axis_name: str,
    file_name: str,
    download_png: bool,
    download_jpeg: bool,
    download_html: bool,
    download_pdf: bool,
    color_output1,
    color_output2,
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
    print("color_output1 ", color_output1)
    if graph_name == None:
        graph_name = "Graph name"
    if x_axis_name == None:
        x_axis_name = "x-axis name"
    if y_axis_name == None:
        y_axis_name = "y-axis name"
    if file_name == None:
        file_name = "filename"

    if df_storage1 is None:
        raise PreventUpdate
    if not os.path.exists("graph_images"):
        os.mkdir("graph_images")

    # print("df_storage1 ", df_storage1)
    # print("df_storage2 ", df_storage2)
    loc_config = {"doubleClick": "reset", "showTips": True, "displayModeBar": False}

    if (df_storage1 and df_storage2) is not None:
        df1 = pl.read_json(io.StringIO(df_storage1))
        df2 = pl.read_json(io.StringIO(df_storage2))
        loc_fig = create_fig(
            df1,
            df2,
            choose_graph_type,
            choose_graph_typ2,
            graph_name,
            x_axis_name,
            y_axis_name,
            color_output1,
            color_output2,
        )
        # if download_png:
        #     loc_fig2.write_image("graph_images/" + file_name + ".png", width=1920, height=1080)
        # if download_jpeg:
        #     loc_fig2.write_image("graph_images/" + file_name + ".jpeg", width=1920, height=1080)
        # if download_pdf:
        #     loc_fig2.write_image("graph_images/" + file_name + ".pdf", width=1920, height=1080)
        # if download_html:
        #     loc_fig2.write_html("graph_images/" + file_name + ".html", width=1920, height=1080)

        # TESTING
        # print("list(df[x]) ", list(df1["x"]), " ", list(df1["y"]))

        # loc_graph2 = dcc.Graph(figure=loc_fig, config=loc_config)
        # return loc_graph2
        # return loc_fig2

    else:
        df1 = pl.read_json(io.StringIO(df_storage1))
        df2 = None
        loc_fig = create_fig(
            df1,
            df2,
            choose_graph_type,
            choose_graph_typ2,
            graph_name,
            x_axis_name,
            y_axis_name,
            color_output1,
            color_output2,
        )
        # loc_fig1 = create_fig2(df1, choose_graph_type, graph_name, x_axis_name, y_axis_name)

        # downloads the created graph into the folder "graph_images"
        # if download_png:
        #     loc_fig1.write_image("graph_images/" + file_name + ".png", width=1920, height=1080)
        # if download_jpeg:
        #     loc_fig1.write_image("graph_images/" + file_name + ".jpeg", width=1920, height=1080)
        # if download_pdf:
        #     loc_fig1.write_image("graph_images/" + file_name + ".pdf", width=1920, height=1080)
        # if download_html:
        #     loc_fig1.write_html("graph_images/" + file_name + ".html")

        # loc_graph1 = dcc.Graph(figure=loc_fig, config=loc_config)

        # return loc_graph1
        # return loc_fig1

    if download_png:
        loc_fig.write_image("graph_images/" + file_name + ".png", width=1920, height=1080)
    if download_jpeg:
        loc_fig.write_image("graph_images/" + file_name + ".jpeg", width=1920, height=1080)
    if download_pdf:
        loc_fig.write_image("graph_images/" + file_name + ".pdf", width=1920, height=1080)
    if download_html:
        loc_fig.write_html("graph_images/" + file_name + ".html")

    loc_graph = dcc.Graph(figure=loc_fig, config=loc_config)
    return loc_graph

    # loc_fig1 = create_fig(df1, choose_graph_type, graph_name, x_axis_name, y_axis_name)
    # loc_fig2 = create_fig(df2, choose_graph_type, graph_name, x_axis_name, y_axis_name)

    # test = dcc.Graph(
    #     figure={
    #         "data": [
    #             {
    #                 "x": list(df1["x"]),
    #                 "y": list(df1["y"]),
    #                 "type": "line",
    #                 "name": "graph1",
    #             },
    #             {"x": list(df2["x"]), "y": list(df2["y"]), "type": "bar", "name": "graph2"},
    #         ],
    #         "layout": {
    #             "title": "testgraph",
    #             "name": "test",
    #             "x": "test",
    #             "xname": "test",
    #             "xlabel": "test",
    #             "style": "test",
    #         },
    #     }
    # )

    # if not os.path.exists("graph_images"):
    #    os.mkdir("graph_images")
