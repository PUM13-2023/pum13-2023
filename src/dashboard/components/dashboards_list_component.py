"""Dashboards list component."""

from datetime import datetime, timedelta

from dash.dependencies import Component

from dashboard.models.user import Dashboard

from .list_component import list_component


def generate_list_row_contents(dashboard: Dashboard) -> list[str]:
    """Generate list row from a Dashboard model.

    Args:
        dashboard (Dashboard): A Dashboard model.

    Returns:
        list[str]: A list row.
    """
    datetime_now = datetime.now()

    def get_readable_time_delta(since: datetime) -> str:
        time_delta: timedelta = datetime_now - since
        seconds = int(time_delta.total_seconds())
        days = time_delta.days
        hours = seconds // 3600
        minutes = seconds // 60
        if days > 0:
            if days >= 7:
                # NOTE: locale will change %b !
                return since.strftime("%d %b. %Y")
            if days > 1:
                return f"{days} days ago"

            return "A day ago"
        if hours > 0:
            if hours > 1:
                return f"{hours} hours ago"

            return "An hour ago"
        if minutes > 0:
            if minutes > 1:
                return f"{minutes} minutes ago"

            return "A minute ago"

        return f"{time_delta.seconds} seconds ago"

    return [
        dashboard.name,
        get_readable_time_delta(dashboard.modified),
        get_readable_time_delta(dashboard.created),
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
    return list_component(
        ["Title", "Last edited at", "Created at"],
        [generate_list_row_contents(dashboard) for dashboard in dashboards],
        _id,
    )
