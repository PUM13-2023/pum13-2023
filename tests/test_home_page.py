"""Test home page."""

import pytest
from selenium.webdriver.remote.webelement import WebElement
from tests import helper_test_functions as helper
from tests import settings

from .settings import DriverType

CREATE_DASHBOARD_BUTTON_ID = "create-dashboard"
LATEST_OPENED_DASHBOARDS_ID = "latest-opened-dashboards"
SHARED_DASHBOARDS_ID = "shared-dashboards"
USERNAME = "home-page-user"
PASSWORD = "password"


"""
TODO
Add tests for modals when modal component is finished
"""


@pytest.fixture(scope="class")
def login_session(browser_driver: DriverType) -> None:
    """Log in session."""
    browser_driver.get(settings.START_PAGE_URL)
    helper.try_login(browser_driver, USERNAME, PASSWORD)


@pytest.mark.test_home_page
class TestHomePage:
    """A class to group functions to test the dashboard capabilities."""

    @pytest.mark.usefixtures("start_server", "login_session")
    def test_create_dashboard_button(self, browser_driver: DriverType) -> None:
        """Check that the create dashboard button exists.

        Args:
            browser_driver (DriverType): webdriver used for selenium
        """
        browser_driver.get(settings.URL)

        element: WebElement = helper.get_element_by_id(browser_driver, CREATE_DASHBOARD_BUTTON_ID)
        assert element

    @pytest.mark.usefixtures("start_server", "login_session")
    def test_carousel(self, browser_driver: DriverType) -> None:
        """Check that the carousels are displayed.

        Args:
            browser_driver (DriverType): webdriver used for selenium
        """
        browser_driver.get(settings.URL)
        helper.get_element_by_id(browser_driver, LATEST_OPENED_DASHBOARDS_ID)
        helper.get_element_by_id(browser_driver, SHARED_DASHBOARDS_ID)
