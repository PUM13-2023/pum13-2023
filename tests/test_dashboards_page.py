"""Test dashboards page functionality."""

import pytest

from . import helper_test_functions as helper
from . import settings
from .settings import DriverType

USERNAME = "dashboards-test-user"
PASSWORD = "password"


@pytest.fixture(scope="class")
def login_session(browser_driver: DriverType) -> None:
    """Log in session."""
    browser_driver.get(settings.START_PAGE_URL)
    helper.try_login(browser_driver, USERNAME, PASSWORD)


@pytest.mark.test_dashboards_page
class TestDashboardsPage:
    """Class that contains tests for the dashboards page."""

    @pytest.mark.usefixtures("start_server", "login_session")
    def test_find_dashboards_list(self, browser_driver: DriverType) -> None:
        """Test that the dashboards page list can be found.

        Args:
            browser_driver (DriverType): The browser driver to use.
        """
        browser_driver.get(settings.DASHBOARDS_PAGE_URL)
        helper.get_element_by_id(browser_driver, "dashboards-list")

    @pytest.mark.usefixtures("start_server", "login_session")
    def test_add_new_dashboard(self, browser_driver: DriverType) -> None:
        """Test adding a new dashboard.

        Test that adding a new dashboard from the dashboards
        page adds it to the list.

        Args:
            browser_driver (DriverType): The browser driver
            that should be used.
        """
        browser_driver.get(settings.DASHBOARDS_PAGE_URL)

        dashboards_list_items_selector = '#\{\\"child\\"\:\\"list-rows\\"\,\\"parent\\"\:\\"dashboards-list\\"\}'  # noqa: W605, E501
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
