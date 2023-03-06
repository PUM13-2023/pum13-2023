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
navbar_count = 3
HOME_URL = f"{URL}/"
DASHBOARD_URL = f"{URL}/dashboards"
SHARED_DASHBOARDS_URL = f"{URL}/shared-dashboards"


def server(host, port):
    main.app.run(host, port)


@pytest.mark.test_navbar_component
class TestNavbarComponent:
    @pytest.fixture()
    def start_server(self):
        p = multiprocessing.Process(target=server, args=(HOST, PORT))
        p.start()
        time.sleep(1)
        yield p
        p.terminate()

    @pytest.fixture(autouse=True, scope="session")
    def speed_mult(self, request):
        self.spd_mult = float(request.config.option.speedmult)

    @pytest.fixture(scope="session")
    def browser_driver(self, request):
        driver: webdriver
        match request.config.option.browser:
            case "chrome":
                options = webdriver.ChromeOptions()
                options.add_argument("--headless")
                driver = webdriver.Chrome(options=options)
            case "safari":
                # Headless not possible yet?
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

    @pytest.mark.usefixtures("browser_driver")
    @pytest.mark.usefixtures("start_server")
    def test_find_navbar(self, browser_driver: webdriver) -> None:
        """
        Test that a navbar element exists on the page
        """
        browser_driver.get(URL)

        WebDriverWait(browser_driver, TIMEOUT).until(
            ec.presence_of_element_located((By.ID, "main-navbar"))
        )

        navbar = browser_driver.find_element(By.ID, "main-navbar")

        assert navbar, "Navbar could not be found"

    @pytest.mark.usefixtures("browser_driver")
    @pytest.mark.usefixtures("start_server")
    def test_find_buttons(self, browser_driver: webdriver) -> None:
        """
        Test that the navbar items exist on the page
        """
        browser_driver.get(URL)
        WebDriverWait(browser_driver, TIMEOUT).until(
            ec.presence_of_element_located((By.ID, "main-navbar"))
        )

        navbar = browser_driver.find_elements(
            By.TAG_NAME,
            "a",
        )

        assert len(navbar) == navbar_count, "Navbar items do not exist"

    @pytest.mark.usefixtures("browser_driver")
    @pytest.mark.usefixtures("start_server")
    def test_redirect_home(self, browser_driver: webdriver) -> None:
        """
        Test that the Home item redirects to the correct page
        """
        browser_driver.get(URL)
        WebDriverWait(browser_driver, TIMEOUT).until(
            ec.presence_of_element_located((By.ID, "main-navbar"))
        )

        link = browser_driver.find_element(By.LINK_TEXT, "Home")

        assert link.text == "Home"
        link.click()
        assert (
            browser_driver.current_url == HOME_URL
        ), "Page did not redirect to the correct home page"

    @pytest.mark.usefixtures("browser_driver")
    @pytest.mark.usefixtures("start_server")
    def test_redirect_dashboards(self, browser_driver: webdriver) -> None:
        """
        Test that the Dashboards item redirects to the correct page
        """
        browser_driver.back()
        browser_driver.get(URL)

        WebDriverWait(browser_driver, TIMEOUT).until(
            ec.presence_of_element_located((By.ID, "main-navbar"))
        )

        link = browser_driver.find_element(By.LINK_TEXT, "Dashboards")

        link.click()
        assert (
            browser_driver.current_url == DASHBOARD_URL
        ), "Page did not redirect tot the correct dashboards page"

    @pytest.mark.usefixtures("browser_driver")
    @pytest.mark.usefixtures("start_server")
    def test_redirect_shared_dashboards(self, browser_driver: webdriver) -> None:
        """
        Test that the Shared Dashboards item redirects
        to the correct page
        """
        browser_driver.back()
        browser_driver.get(URL)

        WebDriverWait(browser_driver, TIMEOUT).until(
            ec.presence_of_element_located((By.ID, "main-navbar"))
        )

        link = browser_driver.find_element(By.LINK_TEXT, "Shared dashboards")

        link.click()
        assert browser_driver.current_url == SHARED_DASHBOARDS_URL
