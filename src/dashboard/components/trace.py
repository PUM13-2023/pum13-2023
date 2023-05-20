"""Trace component."""
from typing import Literal

import plotly.graph_objs as go
import polars as pl
from enum import Enum


class TraceType(Enum):
    LINE = "lines"
    SCATTER = "markers"
    BAR = "bar"


def trace(
    df: pl.DataFrame,
    trace_type: TraceType,
    color_input: str,
    name: str,
) -> go.Scatter | go.Bar:
    """Creates a trace based on the chosen type by the user.

    A trace can not be used as an html element
    and must first be embedded into a dcc.Graph
    component. See example.

    Example::

        tr = trace(...)
        fg = go.Figure(data=tr)
        gr = dcc.Graph(figure=fg)

    Args:
        df: a dataframe containg used for creating the trace.
        trace_type: a string used to check what type of trace
        to draw.
        color_input: user chosen color of the trace
        name: user chosen name of the trace.

    Returns:
        fig: a draw trace of the users choice with chosen
        names for the trace and axis.
    """
    cols = df.columns
    if df is None:
        return go.Scatter()
    elif trace_type == TraceType.LINE:
        return go.Scatter(
            x=df[cols[0]],
            y=df[cols[1]],
            marker_color=color_input,
            mode=trace_type.value,
            name=name,
        )
    elif trace_type == TraceType.SCATTER:
        return go.Scatter(
            x=df[cols[0]],
            y=df[cols[1]],
            marker_color=color_input,
            mode=trace_type.value,
            name=name,
        )
    elif trace_type == TraceType.BAR:
        return go.Bar(
            x=df[cols[0]],
            y=df[cols[1]],
            marker_color=color_input,
            name=name,
        )
    else:  # apparently mypy does not detect that all cases are handled.
        return go.Scatter()
