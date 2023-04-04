"""Test for navbar functionality."""
import multiprocessing
import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from dashboard import main

TIMEOUT = 3
PORT = 3030
HOST = "127.0.0.1"
URL = f"http://{HOST}:{str(PORT)}"
NAVBAR_COUNT = 4
HOME_URL = f"{URL}/"
DASHBOARD_URL = f"{URL}/dashboards"
SHARED_DASHBOARDS_URL = f"{URL}/shared-dashboards"


def server(host, port):
    """Start the graphit application."""
    main.app.run(host, port)


@pytest.mark.test_navbar_component
class TestNavbarComponent:
    """Class that tests the Navbar component."""

    @pytest.fixture()
    def start_server(self):
        """Start a local server on a different process."""
        p = multiprocessing.Process(target=server, args=(HOST, PORT))
        p.start()
        time.sleep(1)
        yield p
        p.terminate()

    @pytest.mark.usefixtures("start_server")
    def test_find_navbar(self, browser_driver: webdriver) -> None:
        """Test that a navbar element exists on the page."""
        browser_driver.get(URL)

        WebDriverWait(browser_driver, TIMEOUT).until(
            ec.presence_of_element_located((By.ID, "main-navbar"))
        )

        navbar = browser_driver.find_element(By.ID, "main-navbar")

        assert navbar, "Navbar could not be found"

    @pytest.mark.usefixtures("start_server")
    def test_find_buttons(self, browser_driver: webdriver) -> None:
        """Test that the navbar items exist on the page."""
        browser_driver.get(URL)
        WebDriverWait(browser_driver, TIMEOUT).until(
            ec.presence_of_element_located((By.ID, "main-navbar"))
        )
        navbar = browser_driver.find_element(By.ID, "main-navbar")
        navbar_items = navbar.find_elements(
            By.TAG_NAME,
            "a",
        )

        assert len(navbar_items) == NAVBAR_COUNT, "Navbar items do not exist"

    @pytest.mark.usefixtures("start_server")
    def test_redirect_home(self, browser_driver: webdriver) -> None:
        """Test that the Home item redirects to the correct page."""
        browser_driver.get(URL)
        WebDriverWait(browser_driver, TIMEOUT).until(
            ec.presence_of_element_located((By.ID, "upper-navbar-container"))
        )

        link = browser_driver.find_element(By.ID, "Home-button-navbar")

        assert link.text == "home\nHome"

        link.click()
        assert (
            browser_driver.current_url == HOME_URL
        ), "Page did not redirect to the correct home page"

    @pytest.mark.usefixtures("start_server")
    def test_redirect_dashboards(self, browser_driver: webdriver) -> None:
        """Test so Dashboards item redirects to correct page."""
        browser_driver.back()
        browser_driver.get(URL)

        WebDriverWait(browser_driver, TIMEOUT).until(
            ec.presence_of_element_located((By.ID, "main-navbar"))
        )

        link = browser_driver.find_element(By.ID, "Dashboards-button-navbar")

        link.click()
        assert (
            browser_driver.current_url == DASHBOARD_URL
        ), "Page did not redirect to the correct dashboards page"

    @pytest.mark.usefixtures("start_server")
    def test_redirect_shared_dashboards(self, browser_driver: webdriver) -> None:
        """Test so Shared Dashboards item redirects to correct page."""
        browser_driver.back()
        browser_driver.get(URL)

        WebDriverWait(browser_driver, TIMEOUT).until(
            ec.presence_of_element_located((By.ID, "main-navbar"))
        )

        link = browser_driver.find_element(By.ID, "Shared dashboards-button-navbar")

        link.click()
        assert browser_driver.current_url == SHARED_DASHBOARDS_URL
