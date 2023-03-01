import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement


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

    @pytest.mark.buttons_exist
    def find_buttons(self, browser_driver):
        pass

    @pytest.mark.navbar_exists
    def find_navbar(self, browser_driver):
        pass

    @pytest.mark.redirect_home
    def redirect_home(self, browser_driver):
        pass

    @pytest.mark.redirect_dashboards
    def redirect_dashboards(self, browser_driver):
        pass

    @pytest.mark.redirect_shared_dashboards
    def redirect_shared_dashoards(self, browser_driver):
        pass
