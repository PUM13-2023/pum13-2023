"""Test home page"""

import multiprocessing

import pytest
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

from dashboard import main

from . import helper_test_functions as helper

HOST = "127.0.0.1"
PORT = 8000
URL = f"http://{HOST}:{str(PORT)}"

CREATE_DASHBOARD_BUTTON_ID = "create-dashboard"
LATEST_OPENED_DASHBOARDS_ID = "latest-opened-dashboards"
SHARED_DASHBOARDS_ID = "shared-dashboards"


"""
TODO
Add tests for modals when modal component is finished
"""


def server(host, port):
    """Start the graphit application."""
    main.app.run(host, port)


@pytest.mark.test_home_page
class TestHomePage:
    """A class to group functions to test the dashboard capabilities."""

    @pytest.fixture(scope="session", autouse=True)
    def start_server(self):
        """Start a local server on a different process."""
        p = multiprocessing.Process(target=server, args=(HOST, PORT))
        p.start()
        yield p
        p.terminate()

    def test_create_dashboard_button(self, browser_driver: webdriver) -> None:
        """Check that the create dashboard button exists

        Args:
            browser_driver (webdriver): webdriver used for selenium
        """
        browser_driver.get(URL)

        element: WebElement = helper.get_element_by_id(browser_driver, CREATE_DASHBOARD_BUTTON_ID)
        assert element

    def test_carousel(self, browser_driver: webdriver) -> None:
        """Check that the carousels are displayed

        Args:
            browser_driver (webdriver): webdriver used for selenium
        """
        browser_driver.get(URL)
        helper.get_element_by_id(browser_driver, LATEST_OPENED_DASHBOARDS_ID)
        helper.get_element_by_id(browser_driver, SHARED_DASHBOARDS_ID)
