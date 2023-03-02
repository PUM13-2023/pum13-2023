import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from dashboard.components.navbar_component import navbar_items

TIMEOUT = 3
PORT = 3030
HOST = "127.0.0.1"
URL = f"http://{HOST}:{str(PORT)}"
navbar_count = len(navbar_items)
HOME_URL = f"{URL}/Home"
DASHBOARD_URL = f"{URL}/Dashboards"
SHARED_DASHBOARDS_URL = f"{URL}/Shared Dashboards"


@pytest.mark.test_navbar_component
class TestNavbarComponent:
    @pytest.fixture(scope="session")
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
    def test_find_navbar(self, browser_driver: webdriver) -> None:
        """
        Test that a navbar element exists on the page
        """
        browser_driver.get(URL)

        WebDriverWait(browser_driver, TIMEOUT).until(
            ec.presence_of_element_located((By.ID, "main-navbar"))
        )

        navbar = browser_driver.find_element(By.ID, "main-navbar")

        assert navbar

    @pytest.mark.usefixtures("browser_driver")
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

        assert len(navbar) == navbar_count

    @pytest.mark.usefixtures("browser_driver")
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
        assert browser_driver.current_url == HOME_URL

    @pytest.mark.usefixtures("browser_driver")
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

        assert link.text == "Dashboards"
        link.click()
        assert browser_driver.current_url == DASHBOARD_URL

    @pytest.mark.usefixtures("browser_driver")
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

        link = browser_driver.find_element(By.LINK_TEXT, "Shared Dashboards")

        assert link.text == "Shared Dashboards"
        link.click()
        assert browser_driver.current_url == SHARED_DASHBOARDS_URL
