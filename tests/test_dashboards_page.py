"""Test dashboards page functionality."""
import multiprocessing
import time
from typing import List

from dash import html
import pytest
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

from dashboard import main
from dashboard.components.dashboards_list_component import (
    dashboards_list_component,
    generate_list_rows,
    generate_list_titles,
)
from dashboard.pages.paths import DASHBOARDS_PATH

from . import helper_test_functions as helper
from . import settings as settings

driver_type = (
    webdriver.Chrome
    | webdriver.Firefox
    | webdriver.Safari
    | webdriver.Edge
    | webdriver.ChromiumEdge
)

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
    return generate_list_rows(DASHBOARDS_LIST_ROWS)


@pytest.fixture
def dashboards_list_titles() -> List[html.Span]:
    return generate_list_titles(DASHBOARDS_LIST_TITLES)


@pytest.mark.test_dashboards_page
class TestDashboardsPage:
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
    def test_find_dashboards_list(self, browser_driver: driver_type) -> None:
        browser_driver.get(settings.DASHBOARDS_PAGE_URL)
        helper.get_element_by_id(browser_driver, "dashboards-list")

    def test_correct_dashboards_list_dimensions(
        self, dashboards_list_rows: List[html.Div], dashboards_list_titles: List[html.Span]
    ) -> None:
        assert len(dashboards_list_rows) == len(DASHBOARDS_LIST_ROWS)
        assert len(dashboards_list_titles) == len(DASHBOARDS_LIST_TITLES)

    def test_incorrect_dashboards_list_dimensions(self) -> None:
        try:
            dashboards_list_component(DASHBOARDS_LIST_TITLES_TOO_MANY, DASHBOARDS_LIST_ROWS)
            raise AssertionError("Can create dashboards_list_component of faulty dimensions")
        except IndexError:
            assert True
