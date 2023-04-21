"""Test list component."""
from typing import List

from dash import dcc, html
import pytest

from dashboard.components.list_component import (
    generate_list_rows,
    generate_list_titles,
    list_component,
)

LIST_TITLES = ["Title", "Last edited at", "Created at"]
LIST_TITLES_TOO_MANY = ["Title", "Last edited at", "Created at", "Another one"]

LIST_ROWS = [
    ["Dashboard 1", "Today", "Yesterday"],
    ["Dashboard 2", "3 days ago", "2 days ago"],
    ["Dashboard 2", "1 year ago", "5 years ago"],
]


@pytest.fixture
def list_rows() -> List[dcc.Link]:
    """Generate dashboard list row elements.

    Returns:
        List[html.Div]: The dashboard list row elements.
    """
    return generate_list_rows(LIST_ROWS)


@pytest.fixture
def list_titles() -> List[html.Span]:
    """Generate dashboards list title elements.

    Returns:
        List[html.Span]: The dashboards list title elements.
    """
    return generate_list_titles(LIST_TITLES)


@pytest.mark.test_list_component
class TestListComponent:
    """Class that contains tests for the list component."""

    def test_correct_list_dimensions(
        self, list_rows: List[html.Div], list_titles: List[html.Span]
    ) -> None:
        """Test generating a list.

        Test that a list generated from constants has
        the correct dimensions.

        Args:
            list_rows (List[html.Div]): The generated
            list rows.
            list_titles (List[html.Span]): The generated
            list titles.
        """
        assert len(list_rows) == len(LIST_ROWS)
        assert len(list_titles) == len(LIST_TITLES)

    def test_incorrect_list_dimensions(self) -> None:
        """Test incorrectly generating a list.

        Test that generating a list with the incorrect
        dimensions will result in an error.

        Raises:
            AssertionError: If a list with the incorrect
            dimensions is possible to generate.
        """
        try:
            list_component(LIST_TITLES_TOO_MANY, LIST_ROWS, "id")
            raise AssertionError("Can create dashboards_list_component of faulty dimensions")
        except IndexError:
            assert True
