"""Trace component."""

from enum import Enum

import polars as pl
import plotly.graph_objs as go


class TraceType(Enum):
    """Contains the available trace types."""

    LINE = "lines"
    SCATTER = "markers"
    BAR = "bar"


def trace(
    df: pl.DataFrame,
    trace_type: TraceType,
    trace_color: str,
    name: str,
) -> go.Scatter | go.Bar:
    """Creates a trace based on a trace type.

    A trace can not be used as an html element
    and must first be embedded into a dcc.Graph
    component. See example.

    Example::

        tr = trace(...)
        fg = go.Figure(data=tr)
        gr = dcc.Graph(figure=fg)

    Args:
        df (pl.DataFrame): a dataframe containg used for creating the trace.
        trace_type (TraceType): The type of trace to create.
        trace_color (str): The color of the trace.
        name (str): The name of the trace.

    Returns:
        go.Scatter | go.Bar: The created trace.
    """

    cols = df.columns
    if df is None:
        return go.Scatter()
    elif trace_type == TraceType.LINE:
        return go.Scatter(
            x=df[cols[0]],
            y=df[cols[1]],
            marker_color=trace_color,
            mode=trace_type.value,
            name=name,
        )
    elif trace_type == TraceType.SCATTER:
        return go.Scatter(
            x=df[cols[0]],
            y=df[cols[1]],
            marker_color=trace_color,
            mode=trace_type.value,
            name=name,
        )
    elif trace_type == TraceType.BAR:
        return go.Bar(
            x=df[cols[0]],
            y=df[cols[1]],
            marker_color=trace_color,
            name=name,
        )
    else:  # mypy does not detect that all cases are handled.
        return go.Scatter()
