"""Conftest file for pytest."""
import multiprocessing
import time

from _pytest.fixtures import FixtureRequest
import pytest
from selenium import webdriver
from tests import settings


def pytest_addoption(parser):
    """Pytest function that would addoption."""
    parser.addoption("--browser", action="store", default="")
    parser.addoption("--head", action="store", default="1")


def server(host, port):
    """Start the graphit application."""
    from dashboard import config

    config.MOCK_DB = True

    from dashboard import main

    main.app.run(host, port)


@pytest.fixture(scope="session")
def start_server():
    """Start a local server on a different process."""
    p = multiprocessing.Process(target=server, args=(settings.HOST, settings.PORT))
    p.start()
    time.sleep(settings.SERVER_STARTUP_WAIT)
    yield p
    p.terminate()


@pytest.fixture(scope="class")
def browser_driver(request: FixtureRequest):
    """Create the browser driver with the right request.

    Creates the browser driver for uses in diffrent test.

    Args:
        request (FixtureRequest): For the config given by
        the users.
    """
    driver: webdriver
    match request.config.option.browser:
        case "chrome":
            options = webdriver.ChromeOptions()
            if request.config.option.head == "1":
                options.add_argument("--headless")
            driver = webdriver.Chrome(options=options)
        case "edge":
            options = webdriver.EdgeOptions()
            if request.config.option.head == "1":
                options.add_argument("--headless")
            driver = webdriver.Edge(options=options)
        case "chromium":
            options = webdriver.ChromeOptions()
            if request.config.option.head == "1":
                options.add_argument("--headless")
            driver = webdriver.ChromiumEdge(options=options)
        case _:
            options = webdriver.FirefoxOptions()
            if request.config.option.head == "1":
                options.add_argument("--headless")
            driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(settings.IMPLICIT_WAIT)
    yield driver
    driver.close()
