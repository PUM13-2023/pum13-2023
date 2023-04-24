"""Test list component."""
from datetime import datetime, timedelta

import pytest

from dashboard.components.dashboards_list_component import generate_list_row_contents
from dashboard.models.user import Dashboard

now = datetime.now()
a_minute_ago = now - timedelta(minutes=1)
an_hour_ago = now - timedelta(hours=1)
a_day_ago = now - timedelta(days=1)

TIMES: list[tuple[datetime, str]] = [
    (a_minute_ago, "A minute ago"),
    (an_hour_ago, "An hour ago"),
    (a_day_ago, "A day ago"),
]

DASHBOARDS = [
    Dashboard(name="Dashboard 1", created=TIMES[0][0]),
    Dashboard(name="Dashboard 2", created=TIMES[1][0]),
    Dashboard(name="Dashboard 3", created=TIMES[2][0]),
]


@pytest.fixture
def dashboards_list_rows_contents() -> list[list[str]]:
    """Generate dashboard list row elements.

    Returns:
        list[html.Div]: The dashboard list row elements.
    """
    return [generate_list_row_contents(now, dashboard) for dashboard in DASHBOARDS]


@pytest.mark.test_dashboards_list_component
class TestDashboardsListComponent:
    """Class that contains tests for the dashboards list component."""

    def test_generate_list_row_contents(
        self, dashboards_list_rows_contents: list[list[str]]
    ) -> None:
        """Test that generated list row contents is valid."""
        assert all(
            (
                list_row_contents[0] == DASHBOARDS[i].name
                and list_row_contents[1] == TIMES[i][1]
                and list_row_contents[2] == TIMES[i][1]
                for i, list_row_contents in enumerate(dashboards_list_rows_contents)
            )
        )
