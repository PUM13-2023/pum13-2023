import multiprocessing
from time import sleep
from typing import Any

from dash import html
import pytest
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from src.dashboard import main

TIMEOUT = 3
PORT = 8000
HOST = "127.0.0.1"
URL = f"http://{HOST}:{str(PORT)}"

USERNAME = "cooluser"

# Constants used in search bar
SEARCH_BAR_ID = "search-bar"

# Constants used in welcome message
WELCOME_ID = "home-welcome-user"
WELCOME_MESSAGE = f"Welcome back {USERNAME}"


def server(host, port):
    main.app.run(host, port)


def find_element(browser_driver: webdriver, find_by: By, text: str) -> bool | WebElement:
    """
    Returns the requested element if found else False

    args
    browser_driver: The in use webdriver
    find_by: The find by tag ex. By.ID
    text: The text to search for in the specified tag
    """
    try:
        WebDriverWait(browser_driver, TIMEOUT).until(
            ec.presence_of_element_located((find_by, text))
        )
        return browser_driver.find_element(find_by, text)
    
    except TimeoutException:
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
            welcome_text.text == WELCOME_MESSAGE
        ), f"Welcome message does not match: {WELCOME_MESSAGE}"
