"""Test dashboards page functionality."""
import multiprocessing
import time
from typing import List

from dash import html
import pytest
from selenium import webdriver

from dashboard import main
from dashboard.components.dashboards_list_component import (
    dashboards_list_component,
    generate_list_rows,
    generate_list_titles,
)

from . import helper_test_functions as helper
from . import settings
from .settings import DriverType

DASHBOARDS_LIST_TITLES = ["Title", "Last edited at", "Created at"]
DASHBOARDS_LIST_TITLES_TOO_MANY = ["Title", "Last edited at", "Created at", "Another one"]

DASHBOARDS_LIST_ROWS = [
    ["Dashboard 1", "Today", "Yesterday"],
    ["Dashboard 2", "3 days ago", "2 days ago"],
    ["Dashboard 2", "1 year ago", "5 years ago"],
]


def server(host: str, port: int) -> None:
    """Start the graphit application."""
    main.app.run(host, port)


@pytest.fixture
def dashboards_list_rows() -> List[html.Div]:
    """Generate dashboard list row elements.

    Returns:
        List[html.Div]: The dashboard list row elements.
    """
    return generate_list_rows(DASHBOARDS_LIST_ROWS)


@pytest.fixture
def dashboards_list_titles() -> List[html.Span]:
    """Generate dashboards list title elements.

    Returns:
        List[html.Span]: The dashboards list title elements.
    """
    return generate_list_titles(DASHBOARDS_LIST_TITLES)


@pytest.mark.test_dashboards_page
class TestDashboardsPage:
    """Class that contains tests for the dashboards page."""

    @pytest.fixture()
    def start_server(self):
        """Start a local server on a different process."""
        p = multiprocessing.Process(target=server, args=(settings.HOST, settings.PORT))
        p.start()
        time.sleep(1)
        yield p
        p.terminate()

    @pytest.mark.usefixtures("start_server")
    @pytest.mark.usefixtures("browser_driver")
    def test_find_dashboards_list(self, browser_driver: DriverType) -> None:
        """Test that the dashboards page list can be found.

        Args:
            browser_driver (DriverType): The browser driver to use.
        """
        browser_driver.get(settings.DASHBOARDS_PAGE_URL)
        helper.get_element_by_id(browser_driver, "dashboards-list")

    def test_correct_dashboards_list_dimensions(
        self, dashboards_list_rows: List[html.Div], dashboards_list_titles: List[html.Span]
    ) -> None:
        """Test generating a dashboards list.

        Test that a dashboards list generated from constants has
        the correct dimensions.

        Args:
            dashboards_list_rows (List[html.Div]): The generated
            dashboards list rows.
            dashboards_list_titles (List[html.Span]): The generated
            dashboards list titles.
        """
        assert len(dashboards_list_rows) == len(DASHBOARDS_LIST_ROWS)
        assert len(dashboards_list_titles) == len(DASHBOARDS_LIST_TITLES)

    def test_incorrect_dashboards_list_dimensions(self) -> None:
        """Test incorrectly generating dashboards list.

        Test that generating a dashboards list with the incorrect
        dimensions will result in an error.

        Raises:
            AssertionError: If a dashboards list with the incorrect
            dimensions is possible to generate.
        """
        try:
            dashboards_list_component(DASHBOARDS_LIST_TITLES_TOO_MANY, DASHBOARDS_LIST_ROWS)
            raise AssertionError("Can create dashboards_list_component of faulty dimensions")
        except IndexError:
            assert True

    @pytest.mark.usefixtures("start_server")
    @pytest.mark.usefixtures("browser_driver")
    def test_add_new_dashboard(self, browser_driver: DriverType) -> None:
        """Test adding a new dashboard.

        Test that adding a new dashboard from the dashboards
        page adds it to the list.

        Args:
            browser_driver (DriverType): The browser driver
            that should be used.
        """
        browser_driver.get(settings.DASHBOARDS_PAGE_URL)

        dashboards_list_items_selector = (
            '#\{\\"child\\"\:\\"list-rows\\"\,\\"parent\\"\:\\"dashboards-list\\"\}'
        )
        dashboards_list_items_before = helper.get_element_by_css_selector(
            browser_driver, dashboards_list_items_selector
        )
        len_before = len(dashboards_list_items_before.get_property("children"))

        add_button = helper.get_element_by_id(browser_driver, "dashboards-add-button")
        add_button.click()

        dashboards_list_items_after = helper.get_element_by_css_selector(
            browser_driver, dashboards_list_items_selector
        )
        len_after = len(dashboards_list_items_after.get_property("children"))

        assert len_before == len_after - 1
