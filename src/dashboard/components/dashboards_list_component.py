"""Dashboards list component."""

from datetime import datetime

from dash.dependencies import Component

from dashboard.models.user import Dashboard
from dashboard.utilities import to_human_time_delta

from .list_component import list_component


def generate_list_row_contents(time: datetime, dashboard: Dashboard) -> list[str]:
    """Generate list row from a Dashboard model.

    Args:
        time (datetime): A point in time when this
        function is called. Generally this would
        be a fixed point in time in a sequence of
        calls.
        dashboard (Dashboard): A Dashboard model.

    Returns:
        list[str]: A list row.
    """
    return [
        dashboard.name,
        to_human_time_delta(time, dashboard.modified),
        to_human_time_delta(time, dashboard.created),
    ]


def dashboards_list_component(dashboards: list[Dashboard], _id: str) -> Component:
    """Create a dashboards list component.

    Args:
        titles_names (List[str]): The titles to display at the top of
        the list.
        list_rows (List[List[str]]): The rows that make up the list
        contents.

    Raises:
        IndexError: If the amount of titles does not match the amount
        of list rows.

    Returns:
        Component: A dashboards list component.
    """
    now = datetime.now()

    return list_component(
        ["Title", "Last edited at", "Created at"],
        [generate_list_row_contents(now, dashboard) for dashboard in dashboards],
        _id,
    )
