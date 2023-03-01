import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from dashboard.components.navbar_component import navbar_items

TIMEOUT = 10
PORT = 3030
HOST = '127.0.0.1'
URL = f'http://{HOST}:{str(PORT)}'
navbar_count = len(navbar_items)
HOME_URL = f'{URL}/Home'
DASHBOARD_URL = f'{URL}/Dashboards'
SHARED_DASHBOARDS_URL = f'{URL}/Shared Dashboards'


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
                driver = webdriver.Chrome()
            case "safari":
                driver = webdriver.Safari()
            case "edge":
                driver = webdriver.Edge()
            case "chromium":
                driver = webdriver.ChromiumEdge()
            case _:
                driver = webdriver.Firefox()
        yield driver
        driver.close()

    @pytest.mark.usefixtures('browser_driver')
    def test_find_navbar(self, browser_driver: webdriver) -> None:
        browser_driver.get(URL)

        WebDriverWait(browser_driver, TIMEOUT).until(
            ec.presence_of_element_located((By.ID, "main-navbar"))
        )

        navbar = browser_driver.find_element(
            By.ID,
            'main-navbar'
        )

        assert navbar

    @pytest.mark.usefixtures('browser_driver')
    def test_find_buttons(self, browser_driver: webdriver) -> None:
        browser_driver.get(URL)
        WebDriverWait(browser_driver, TIMEOUT).until(
            ec.presence_of_element_located((By.ID, "main-navbar"))
        )

        navbar = browser_driver.find_elements(
            By.TAG_NAME,
            'a',
        )

        assert len(navbar) == navbar_count

    @pytest.mark.usefixtures('browser_driver')
    def test_redirect_home(self, browser_driver: webdriver) -> None:
        browser_driver.get(URL)
        WebDriverWait(browser_driver, TIMEOUT).until(
            ec.presence_of_element_located((By.ID, "main-navbar"))
        )

        link = browser_driver.find_element(
            By.LINK_TEXT,
            'Home'
        )

        assert link.text == 'Home'
        link.click()
        assert browser_driver.current_url == HOME_URL

    @pytest.mark.usefixtures('browser_driver')
    def test_redirect_dashboards(self, browser_driver: webdriver) -> None:
        browser_driver.back()
        browser_driver.get(URL)

        WebDriverWait(browser_driver, TIMEOUT).until(
            ec.presence_of_element_located((By.ID, "main-navbar"))
        )

        link = browser_driver.find_element(
            By.LINK_TEXT,
            'Dashboards'
        )

        assert link.text == 'Dashboards'
        link.click()
        assert browser_driver.current_url == DASHBOARD_URL

    @pytest.mark.usefixtures('browser_driver')
    def test_redirect_shared_dashboards(self, browser_driver: webdriver) -> None:
        browser_driver.back()
        browser_driver.get(URL)

        WebDriverWait(browser_driver, TIMEOUT).until(
            ec.presence_of_element_located((By.ID, "main-navbar"))
        )

        link = browser_driver.find_element(
            By.LINK_TEXT,
            'Shared Dashboards'
        )

        assert link.text == 'Shared Dashboards'
        link.click()
        assert browser_driver.current_url == SHARED_DASHBOARDS_URL
