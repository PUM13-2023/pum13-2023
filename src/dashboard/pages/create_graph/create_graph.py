"""Graph display module.

This module displays different types of graphs based on input,
from either a csv-file or from a database.
"""


import dash
from dash import dcc, html
from dash.dependencies import Component
import dash_bootstrap_components as dbc

from dashboard.components import button, icon, text_input
from dashboard.components.modal import modal_container, modal_dialog
from dashboard.components.trace import TraceType
import dashboard.pages.create_graph.controller  # noqa: F401

from dashboard.models import db
from dashboard.models.data import Data, Settings, DataType
from datetime import datetime

dash.register_page(__name__, path="/create-graph", nav_item=False)

debug = True

event = {"event": "click", "props": ["scatter", "line"]}


# the main graphical component for the entire csv graph create page page
def layout() -> Component:
    """Main layout component that is parent to all other components.

    Returns:
        A html.div component with all other components.
    """

    db.connect_data_db("create_graph_test_db")

    for obj in Settings.objects.filter(test_case="test_case1"):
        obj.delete()
    for obj in Data.objects.filter(type=DataType.XY_PLOT.value):
        obj.delete()

    test_settings = Settings(test_case="test_case1", time=datetime.now())
    test_settings.save()
    test_data = Data(
        settings=test_settings,
        name="test_document1",
        type=DataType.XY_PLOT,
    )
    test_data.x = [1, 2, 3, 4, 5]
    test_data.y = [2, 3, 4, 5, 6]
    test_data.save()

    # main background element
    return html.Div(
        className="bg-background flex h-screen",
        children=[
            graph_window(),
            right_settings_bar(),
            dcc.Download(id="download_fig"),
            modal_container(
                children=[
                    modal_dialog(
                        children=[
                            html.Div(
                                className="[&>*]:m-[4px] w-[300px]",
                                children=[
                                    html.P("Select data from database"),
                                    dcc.Dropdown(
                                        options=[],
                                        placeholder="Select a project",
                                        id="project_selector",
                                    ),
                                    dcc.Dropdown(
                                        options=[],
                                        placeholder="Select a document",
                                        id="document_selector",
                                        disabled=True,
                                    ),
                                    button(
                                        "done",
                                        "Select",
                                        id="database_dialog_select",
                                        className="hover:bg-dark-purple bg-menu-back text-white cursor-pointer",
                                        n_clicks=0,
                                        disabled=True,
                                    ),
                                ],
                            )
                        ],
                        id="database_dialog",
                        open_=False,
                    )
                ]
            ),
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
        children=button(
            "upload", "CSV file", size=26, className="whitespace-nowrap bg-transparent"
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
            text_input(id="file_name", title="Download as", description="Enter file name..."),
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
    # NOTE: dcc.Graph will not shrink dynamically unless
    # min-width is set on the parent element!
    return html.Div(
        className=(
            "[&>*]:mx-[1em] w-full min-w-[220px] bg-white ml-[3rem] my-[3rem] rounded-md shadow-md"
        ),
        children=[
            text_input(id="figure_name", title="Figure name", description="Enter figure name..."),
            dcc.Graph(
                id="graph_id",
                figure={},
                config={"doubleClick": "reset", "showTips": True, "displayModeBar": False},
            ),
            text_input(id="x_axis_name", title="x-axis name", description="Enter x-axis name..."),
            text_input(id="y_axis_name", title="y-axis name", description="Enter y-axis name..."),
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
            text_input(
                id="graph_name",
                title="Graph name",
                description="Enter graph name...",
                disabled=True,
            ),
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
                value="#000000",
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
                        id="database_button",
                        icon_name="database",
                        text="Database",
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
                value=TraceType.LINE.value,
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
