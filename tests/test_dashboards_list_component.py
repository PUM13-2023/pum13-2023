"""Test list component."""
from datetime import datetime

import pytest

from dashboard.components.dashboards_list_component import generate_list_row_contents
from dashboard.models.user import Dashboard

t1 = datetime.now()
t2 = datetime.now()
t3 = datetime.now()

DASHBOARDS = [
    Dashboard(name="Dashboard 1", created=t1),
    Dashboard(name="Dashboard 2", created=t2),
    Dashboard(name="Dashboard 3", created=t3),
]


@pytest.fixture
def dashboards_list_rows_contents() -> list[list[str]]:
    """Generate dashboard list row elements.

    Returns:
        list[html.Div]: The dashboard list row elements.
    """
    return [generate_list_row_contents(dashboard) for dashboard in DASHBOARDS]


@pytest.mark.test_dashboards_list_component
class TestDashboardsListComponent:
    """Class that contains tests for the dashboards list component."""

    def test_generate_list_row_contents(self, dashboards_list_rows_contents: list[list[str]]):
        """Test that generated list row contents is valid."""
        assert all(
            (
                list_row_contents[0] == DASHBOARDS[i].name
                for i, list_row_contents in enumerate(dashboards_list_rows_contents)
            )
        )
