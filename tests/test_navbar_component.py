import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement


PORT = 3030
HOST = '127.0.0.1'
URL = f'http://{HOST}:{PORT}'


@pytest.mark.test_navbar_component
class TestNavbarComponent:
    @pytest.fixture(scope="session")
    def browser_driver(self, request):
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
    def find_buttons(self, browser_driver):
        browser_driver.get(URL)
        navbar = browser_driver.find_element(
            By.ID,
            'main-navbar'
        )
        assert navbar

    def find_navbar(self, browser_driver):
        assert True

    def redirect_home(self, browser_driver):
        assert True

    def redirect_dashboards(self, browser_driver):
        assert True

    def redirect_shared_dashboards(self, browser_driver):
        assert True
