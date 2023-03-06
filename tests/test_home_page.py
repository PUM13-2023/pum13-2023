import multiprocessing
from time import sleep

import pytest
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from dash import html

from src.dashboard import main

TIMEOUT = 1.5
PORT = 8000
HOST = "127.0.0.1"
URL = f"http://{HOST}:{str(PORT)}"

USERNAME = "cooluser"

# Constants for search bar
SEARCH_BAR_ID = "search-bar"

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


def server(host, port):
    main.app.run(host, port)


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

    def test_search_bar(self, browser_driver: webdriver) -> None:
        """
        Test that the search bar includes two elements
        a text input and a submit button
        """
        try:
            WebDriverWait(browser_driver, TIMEOUT).until(
                ec.presence_of_element_located((By.ID, SEARCH_BAR_ID))
            )
            search_bar = browser_driver.find_element(By.ID, SEARCH_BAR_ID)
        except TimeoutException:
            search_bar = []

        assert search_bar, "Search bar not found on page"

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
        create_dashboard_menu = self.find_create_dashboard_menu(browser_driver)
        assert create_dashboard_menu, "Create dashboard menu did not pop up"

    def find_create_dashboard_menu(self, browser_driver) -> WebElement | bool:
        """
        Returns the create dashboard menu element if found else
        returns False
        """
        try:
            return browser_driver.find_element(By.ID, CREATE_DASHBOARD_POPUP_ID)
        except NoSuchElementException:
            return False

    def test_latest_opened_dashboards(self, browser_driver: webdriver) -> None:
        """
        Test that the view of the latest opened dashboards exists and
        displays properly
        """
        try:
            WebDriverWait(browser_driver, TIMEOUT).until(ec.presence_of_element_located((By.ID,)))
            create_dashboard = browser_driver.find_element(By.ID, CREATE_DASHBOARD_ID)
        except TimeoutException:
            create_dashboard = False
