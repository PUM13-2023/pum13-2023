import multiprocessing
from time import sleep

from dash import html
import pytest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from src.dashboard import main
from src.dashboard.pages.index.index import default_style

TIMEOUT = 1.5
PORT = 8000
HOST = "127.0.0.1"
URL = f"http://{HOST}:{str(PORT)}"


USERNAME = "cooluser"
SHARED_LINK_POPUP_ID = "add-shared-link"

# Constants for welcome message
WELCOME_ID = "home-welcome-user"
welcome_message = f"Welcome back {USERNAME}"

# Constants for create dashboard button
CREATE_DASHBOARD_ID = "create-dashboard"
CREATE_DASHBOARD_POPUP_ID = "create-dashboard-menu"

# Constants for latest opened dashboards container
LATEST_OPENED_CONTAINER_ID = "latest-opened-container"
LATEST_OPENED_TEXT = "Latest opened dashboards"
LATEST_OPENED_DASHBOARD_BOX1_ID = ""
LATEST_CREATE_DASHBOARD_ID = "create-dashboard-l"

# Constants for latest shared dashboards
LATEST_SHARED_CONTAINER_ID = "latest-shared-container"
LATEST_SHARED_TEXT = "Latest shared dashboards"
SHARED_CREATE_DASHBOARD_ID = "create-dashboard-s"


def server(host, port):
    main.app.run(host, port)


def find_create_dashboard_menu(browser_driver, create_dashboard_id) -> WebElement | bool:
    """
    Returns the create dashboard menu element if found else
    returns False
    """
    try:
        return browser_driver.find_element(By.ID, create_dashboard_id)
    except NoSuchElementException:
        return False


def try_open_add_shared(browser_driver: webdriver) -> WebElement | bool:
    """
    Try to open the add shared link menu
    """
    try:
        return browser_driver.find_element(By.ID, SHARED_LINK_POPUP_ID)
    except NoSuchElementException:
        return False


@pytest.mark.test_home_page
class TestHomePage:
    @pytest.fixture(autouse=True)
    def start_server(self):
        p = multiprocessing.Process(target=server, args=(HOST, PORT))
        p.start()
        sleep(1)
        yield p
        p.terminate()

    @pytest.fixture(scope="session")
    def speed_mult(self, request):
        self.spd_mult = float(request.config.option.speedmult)

    @pytest.fixture(autouse=True)
    def browser_driver(self, request):
        driver: webdriver
        match request.config.option.browser:
            case "chrome":
                options = webdriver.ChromeOptions()
                options.add_argument("--headless")
                driver = webdriver.Chrome(options=options)
            case "safari":
                driver = webdriver.Safari()
            case "edge":
                options = webdriver.EdgeOptions()
                options.add_argument("--headless")
                driver = webdriver.Edge(options=options)
            case "chromium":
                driver = webdriver.ChromiumEdge().create_options().add_argument("--headless")
            case _:
                options = webdriver.FirefoxOptions()
                options.add_argument("--headless")
                driver = webdriver.Firefox(options=options)
        yield driver
        driver.close()

    def test_welcome_text(self, browser_driver: webdriver) -> None:
        """
        Tests that the welcome text displayed on homepage exists
        """
        try:
            WebDriverWait(browser_driver, TIMEOUT).until(
                ec.presence_of_element_located((By.ID, WELCOME_ID))
            )
            welcome_text = browser_driver.find_element(By.ID, WELCOME_ID)
        except TimeoutException:
            welcome_text = False

        assert welcome_text, "Welcome message not found on page"
        assert (
            welcome_text.text == welcome_message
        ), f"Welcome message does not match: {welcome_message}"

    def test_create_dashboard(self, browser_driver: webdriver) -> None:
        """
        Tests that the create dashboard button exists on the page
        and that the button opens the new dashboard pop-up menu
        """
        try:
            WebDriverWait(browser_driver, TIMEOUT).until(
                ec.presence_of_element_located((By.ID, CREATE_DASHBOARD_ID))
            )
            create_dashboard = browser_driver.find_element(By.ID, CREATE_DASHBOARD_ID)
        except TimeoutException:
            create_dashboard = False

        assert create_dashboard, "Create dashboard button not found on page"
        create_dashboard.click()
        create_dashboard_menu = find_create_dashboard_menu(
            browser_driver, CREATE_DASHBOARD_POPUP_ID
        )
        assert create_dashboard_menu, "Create dashboard menu did not pop up"

    def test_latest_opened_dashboards(self, browser_driver: webdriver) -> None:
        """
        Test that the view of the latest opened dashboards exists and
        displays properly
        """
        try:
            WebDriverWait(browser_driver, TIMEOUT).until(
                ec.presence_of_element_located((By.ID, LATEST_SHARED_CONTAINER_ID))
            )
            latest_dashboards_container = browser_driver.find_element(By.ID, CREATE_DASHBOARD_ID)
            dashboard_children = latest_dashboards_container.find_elements(By.TAG_NAME, "div")
            container_text = latest_dashboards_container.find_element(By.TAG_NAME, "h2")
            create_dashboard = latest_dashboards_container.find_element(
                By.ID, LATEST_CREATE_DASHBOARD_ID
            )
        except TimeoutException:
            dashboard_children = False
            container_text = ""
            latest_dashboards_container = False
            create_dashboard = html.Button()

        assert latest_dashboards_container, "Latest opened dashboards view not found on page"
        assert dashboard_children, "Latest opened dashboards view is empty"
        assert (
            container_text == LATEST_OPENED_TEXT
        ), "Title of latest opened dashboards view is wrong"
        create_dashboard.click()
        assert find_create_dashboard_menu(
            browser_driver, CREATE_DASHBOARD_POPUP_ID
        ), "Create dashboard menu did not pop-up"

    def test_latest_shared_dashboards(self, browser_driver: webdriver) -> None:
        """
        Test that the view of shared opened dashboards exists
        and displays properly
        """
        try:
            WebDriverWait(browser_driver, TIMEOUT).until(
                ec.presence_of_element_located((By.ID, LATEST_SHARED_CONTAINER_ID))
            )
            shared_dashboards_container = browser_driver.find_element(
                By.ID, LATEST_SHARED_CONTAINER_ID
            )
            container_text = shared_dashboards_container.find_element(By.TAG_NAME, "h2")
            shared_children = shared_dashboards_container.find_element(By.TAG_NAME, "div")
            create_dashboard = shared_dashboards_container.find_element(
                By.ID, SHARED_CREATE_DASHBOARD_ID
            )
        except TimeoutException:
            shared_dashboards_container = False
            container_text = ""
            shared_children = False
            create_dashboard = html.Button()

        assert shared_dashboards_container, "Latest shared dashboards container not found on page"
        assert container_text, "Title of latest shared dashboards view is wrong"
        assert shared_children, "Latest shared dashboards view is empty"
        create_dashboard.click()

        assert try_open_add_shared(browser_driver), "Add shared link menu did not pop-up"

    def test_display_callback(self):
        """
        Test that the toggle callback returns the correct style value
        """
        toggle_off = toggle_create_dashboard_menu(0)
        toggle_on = toggle_create_dashboard_menu(1)
        assert toggle_off == "hidden", "Hidden style was not correctly returned"
        assert toggle_on == default_style, "Default toggle style was not correctly returned"
