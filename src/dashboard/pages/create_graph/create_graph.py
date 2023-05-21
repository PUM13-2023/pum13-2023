"""Graph display module.

This module displays different types of graphs based on input,
from either a csv-file or from a database.
"""


import dash
from dash import dcc, html
from dash.dependencies import Component
import dash_bootstrap_components as dbc

from dashboard.components import button, icon, text_input
from dashboard.components.trace import TraceType
import dashboard.pages.create_graph.controller  # noqa: F401

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
            text_input(id="file_name", placeholder="File name"),
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


def graph_window() -> Component:
    """A window used to display the created graph.

    Returns:
        A html.div containing the created graph.
    """
    return html.Div(
        className="bg-white w-full ml-[3rem] my-[3rem] rounded-md shadow-md",
        children=[
            text_input(id="figure_name", placeholder="Figure name"),
            dcc.Graph(
                id="graph_id",
                className="h-[70%] w-full",
                figure={},
                config={"doubleClick": "reset", "showTips": True, "displayModeBar": False},
            ),
            text_input(id="x_axis_name", placeholder="x-axis name"),
            text_input(id="y_axis_name", placeholder="y-axis name"),
        ],
    )


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
            dcc.Dropdown([], placeholder="Select graph", id="graph_selector"),
            text_input(id="graph_name", placeholder="Name graph", disabled=True),
            radio_buttons(),
            download_buttons(),
            color_picker(),
        ],
    )


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
                    radio_item("Line", TraceType.LINE.value, "show_chart"),
                    radio_item("Bar", TraceType.BAR.value, "bar_chart"),
                    radio_item("Scatter", TraceType.SCATTER.value, "scatter_plot"),
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


def radio_item(name: str, value: str, icon_name: str) -> dict[str, html.Div | str]:
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
        "label": html.Div(className=classname, children=[icon(icon_name, size=40), html.P(name)]),
        "value": value,
    }
