"""Test home page."""

import mongoengine
import mongomock
import pytest
from selenium.webdriver.remote.webelement import WebElement
from tests import helper_test_functions as helper
from tests import settings

from dashboard.models import user
from dashboard.pages.index import controller

from .settings import DriverType

CREATE_DASHBOARD_BUTTON_ID = "create-dashboard-btn"
DASHBOARD_MODAL_ID = "modal-container"
LATEST_OPENED_DASHBOARDS_ID = "latest-opened-dashboards"
SHARED_DASHBOARDS_ID = "shared-dashboards"
USERNAME = "home-page-user"
PASSWORD = "password"


"""
TODO
Add tests for modals when modal component is finished
"""
EMPTY_TITLE_OUTPUT = (True, True, False)
EMPTY_DESC_OUTPUT = (True, False, True)
EMPTY_TITLE_DESC_OUTPUT = (True, True, True)
VALID_OUTPUT = (False, False, False)


@pytest.fixture(scope="class")
def login_session(browser_driver: DriverType) -> None:
    """Log in session."""
    browser_driver.get(settings.START_PAGE_URL)
    helper.try_login(browser_driver, USERNAME, PASSWORD)


@pytest.fixture(autouse=True)
def connection():
    """Connect mongoengine to mongomock and return client."""
    conn = mongoengine.connect(
        db="dashboard",
        host="mongodb://localhost",
        mongo_client_class=mongomock.MongoClient,
        uuidRepresentation="standard",
    )

    return conn


@pytest.fixture(autouse=True)
def example_user():
    """Example user."""
    username = "dashboards-page-test-user"
    usr = user.login_user(username)
    return usr


@pytest.mark.test_home_page
class TestHomePage:
    """A class to group functions to test home page."""

    @pytest.mark.usefixtures("start_server", "login_session")
    def test_create_dashboard_button(self, browser_driver: DriverType) -> None:
        """Test the create dashboard button.

        Args:
            browser_driver (DriverType): webdriver used for selenium
        """
        browser_driver.get(settings.HOME_PAGE_URL)

        create_dashboard: WebElement = helper.get_element_by_id(
            browser_driver, CREATE_DASHBOARD_BUTTON_ID
        )
        create_dashboard.click()
        dashboard_modal: WebElement = helper.get_element_by_id(browser_driver, DASHBOARD_MODAL_ID)
        assert "hidden" not in dashboard_modal.get_attribute("class")

    def test_create_dashboard(self) -> None:
        """Tries to create dashboards using callback.

        Args:
            browser_driver (DriverType): webdriver used for selenium
        """
        empty_title_output = controller.add_dashboard_db(0, "", "Text")
        valid_dashboard_output = controller.add_dashboard_db(0, "Title", "Text")
        empty_desc_output = controller.add_dashboard_db(0, "Title", "")
        empty_title_desc_ouput = controller.add_dashboard_db(0, "", "")
        assert empty_title_output == EMPTY_TITLE_OUTPUT
        assert valid_dashboard_output == VALID_OUTPUT
        assert empty_desc_output == EMPTY_DESC_OUTPUT
        assert empty_title_desc_ouput == EMPTY_TITLE_DESC_OUTPUT

    @pytest.mark.usefixtures("start_server", "login_session")
    def test_carousel(self, browser_driver: DriverType) -> None:
        """Check that the carousels are displayed.

        Args:
            browser_driver (DriverType): webdriver used for selenium
        """
        browser_driver.get(settings.HOME_PAGE_URL)
        helper.get_element_by_id(browser_driver, LATEST_OPENED_DASHBOARDS_ID)
        helper.get_element_by_id(browser_driver, SHARED_DASHBOARDS_ID)
