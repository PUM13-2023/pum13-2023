"""Test dashboards page functionality."""
import multiprocessing
import time
from typing import List

from dash import html
import pytest
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

from dashboard import main
from dashboard.components.dashboards_list_component import generate_list_rows
from dashboard.pages.paths import DASHBOARDS_PATH

from . import helper_test_functions as helper
from . import settings

driver_type = (
    webdriver.Chrome
    | webdriver.Firefox
    | webdriver.Safari
    | webdriver.Edge
    | webdriver.ChromiumEdge
)

DASHBOARDS_LIST_TITLES = ["Title", "Last edited at", "Created at"]

DASHBOARDS_LIST_ROWS = [
    ["Dashboard 1", "Today", "Yesterday"],
    ["Dashboard 2", "3 days ago", "2 days ago"],
    ["Dashboard 2", "1 year ago", "5 years ago"],
]


def server(host, port):
    """Start the graphit application."""
    main.app.run(host, port)


@pytest.fixture
def dashboards_list_rows() -> List[html.Div]:
    return generate_list_rows(DASHBOARDS_LIST_ROWS)


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
        browser_driver.get(settings.START_PAGE_URL + DASHBOARDS_PATH)
        helper.get_element_by_id(browser_driver, "dashboards-list")

    def test_correct_amount_of_rows_in_dashboards_list(self, dashboards_list_rows) -> None:
        assert len(dashboards_list_rows) == len(DASHBOARDS_LIST_ROWS)
