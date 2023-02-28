import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

PORT = 3030
ADDRESS = '127.0.0.1'
URL = f'{ADDRESS}:{str(PORT)}'


@pytest.mark.test_generate_navbar_items
class TestGenerateNavbarItems:
    @pytest.fixture(scope="session")
    def speed_mult(self, request):
        self.spd_mult = float(request.config.option.speedmult)

    @pytest.fixture()
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


