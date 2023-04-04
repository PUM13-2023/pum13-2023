PORT = 8000
ADDRESS = "127.0.0.1"
PATH = "/graph_of_csv_file"

import base64
import datetime
from gc import callbacks
import io

import dash
from dash import Dash, callback, ctx, dash_table, dcc, html
from dash.dependencies import Component, Input, Output, State
from dash.exceptions import PreventUpdate
from dash_extensions import EventListener
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

event = {"event": "click", "props": ["scatter", "line"]}


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
                    html.Div(id="output_left_setting_bar"),
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


# @callback(Output)


# creates a specific
def display_graph(df, graph_type):
    # def display_graph(df):
    # old
    # if df is not None:
    #     fig = px.line(df, x=list(df["x"]), y=list(df["y"]), title="Test graph from csv file")
    #     return dcc.Graph(figure=fig)
    print("graph_type ", graph_type)
    if df is not None:
        print("graph_type ", graph_type)
        if graph_type == "scatter":
            fig = px.scatter(
                df, x=list(df["x"]), y=list(df["y"]), title="Test graph from csv file"
            )
            # return dcc.Graph(figure=fig)

        if graph_type == "line":
            fig = px.line(df, x=list(df["x"]), y=list(df["y"]), title="Test graph from csv file")
            # return dcc.Graph(figure=fig)
        if graph_type == "histo":
            fig = px.histogram(df, x=list(df["x"]), title="Test graph from csv file")
            # return dcc.Graph(figure=fig)
        return dcc.Graph(figure=fig)


# right settings bar, choose what kind of a plot
def right_settings_bar():
    return html.Div(
        className=f"bg-[{colors['temp']}] flex flex-row items-center justify-center"
        " h-[80%] w-[20%]",
        children=[choose_plot()],
    )


# # buttons to choose a plot
# def choose_plot():
#     return html.Div(
#         [
#             EventListener(
#                 plot_buttons("scatter"),
#                 # plot_buttons("line", "line_button"),
#                 events=[event],
#                 logging=True,
#                 id="b1",
#             ),
#             EventListener(
#                 plot_buttons("line"),
#                 # plot_buttons("line", "line_button"),
#                 events=[event],
#                 logging=True,
#                 id="b2",
#             ),
#             # html.Div(id="output_b2"),
#             html.Div(id="output_b1"),
#         ]
#     )


# @callback(
#     Output("output_b1", "children"),
#     # Output("output_b2", "children")
#     Input("b1", "n_events"),
#     Input("b2", "n_events"),
#     State("b1", "event"),
#     State("b2", "event"),
# )
# def click_event(n_events1, n_events2, e1, e2):
#     # print("n_events ", n_events, " e = ", e)

#     if (e1 and e2) is None:
#         raise PreventUpdate()
#     # print(output_b1)
#     if n_events1:
#         print("debug 1 scatter")
#         logging = False
#     if n_events2:
#         print("debug 2 line")
#         logging = False
#     # for prop in event["props"]:
#     #   if prop == "scatter":
#     #      print("scatter")
#     # if prop == "line":
#     #    print("line")
#     # loc_graph = display_graph(df, prop)
#     # return "test1"


# buttons to choose a plot
def choose_plot():
    return html.Div(
        [
            plot_buttons("scatter", "scatter_button"),
            plot_buttons("line", "line_button"),
            plot_buttons("histogram", "histo_button"),
            html.Div(id="graph_buttons"),
        ]
    )


@callback(
    Output("graph_buttons", "children"),
    Input("scatter_button", "n_clicks"),
    Input("line_button", "n_clicks"),
    Input("histo_button", "n_clicks"),
)
def return_graph_type(scatter_button, line_button, histo_button):
    # NOT A GOOD SOLUTION
    # global msg
    msg = ""
    if "scatter_button" == ctx.triggered_id:
        msg = "scatter"
    if "line_button" == ctx.triggered_id:
        msg = "line"
    if "histo_button" == ctx.triggered_id:
        msg = "histo"
    # return msg
    dcc.Store(id="graph_type_msg", data=msg, storage_type="memory")
    # return msg


# def plot_buttons(button_text):
def plot_buttons(button_text, button_id):
    return html.Button(
        className=f"bg-[{colors['meny_back']}] grow flex flex-col px-4 justify-center"
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
        # n_clicks=0,
    )


# parses the contents of the inputed csv file using polars
def parse_contents(contents, filename):
    # content_type, content_string = contents.split(",")
    # decoded = base64.b64decode(content_string)
    if contents is not None:
        content_type, content_string = contents.split(",")
        decoded = base64.b64decode(content_string)
    else:
        return
    try:
        if "csv" in filename:
            df = pl.read_csv(io.StringIO(decoded.decode("utf-8")))
            return df

    except Exception as e:
        print(e)
        return html.Div(["Error: could not process file"])


@callback(
    Output("graph_output", "children"),
    # Output("output_b1", "children"),
    Input("uploaded_data", "contents"),
    Input("msg_id", "contents"),
    # Input("b1", "n_events"),
    State("uploaded_data", "filename"),
)
def update_output(content, filename, msg_id):
    # def update_output(content, filename, n_events, e):
    df = parse_contents(content, filename)
    # print(df)
    # if (e) is None:
    #     raise PreventUpdate()
    # for prop in event["props"]:
    #     if prop == "scatter":
    #         print("test")
    #         loc_graph = display_graph(df, prop)
    # # print(output_b1)

    loc_graph = display_graph(df, msg_id)
    # loc_graph = display_graph(df)
    return loc_graph
