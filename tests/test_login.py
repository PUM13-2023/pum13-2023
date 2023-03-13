import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from . import helper_test_functions as helper
from . import settings
from . import helper_test_functions as helper

# Login credentials for the valid test user
WRONG_USERNAME = "not_valid_user"
WRONG_PASSWORD = "not_valid_user_password"

SLEEP_TIME_LOGIN_BUTTON = 2
TIMEOUT_REFRESH = 2

ID_POP_UP_ELEMENT = "login_error_popup"
TIMEOUT_POPUP = 3


@pytest.mark.test_login
class TestLogin:
    @pytest.mark.test_unsuccessful_login
    @pytest.mark.usefixtures("browser_driver")
    def test_unsuccessful_login(self, browser_driver: webdriver):
        browser_driver.get(settings.START_PAGE_URL)
        # Try logging in with wrong password and username
        helper.try_login(WRONG_USERNAME, WRONG_PASSWORD, browser_driver)
        self.check_login_error_pop_up(browser_driver)

        # Try logging in with wrong password
        helper.try_login(settings.USERS_USERNAME, WRONG_PASSWORD, browser_driver)
        self.check_login_error_pop_up(browser_driver)

        # Try logging in with wrong username
        helper.try_login(WRONG_USERNAME, settings.USERS_PASSWORD, browser_driver)
        self.check_login_error_pop_up(browser_driver)

    @pytest.mark.test_successful_login
    @pytest.mark.usefixtures("browser_driver")
    def test_successfull_login(self, browser_driver: webdriver):
        browser_driver.get(settings.START_PAGE_URL)
        helper.try_login(settings.USERS_USERNAME, settings.USERS_PASSWORD, browser_driver)
        # Check that we are still in the homepage after login in
        helper.is_in_home_page(browser_driver)

        # Check that we are still  in the homepage after
        # refreshing in the login page.
        browser_driver.refresh()
        helper.is_in_home_page(browser_driver)

    @pytest.mark.test_logout
    @pytest.mark.usefixtures("browser_driver")
    def test_logout(self, browser_driver: webdriver):
        browser_driver.get(settings.START_PAGE_URL)
        helper.try_login(settings.USERS_USERNAME, settings.USERS_PASSWORD, browser_driver)

        # Check that we are still in the homepage after logging in
        helper.is_in_home_page(browser_driver)

        # Press the log out button
        logout_button = helper.get_logout_button(browser_driver)
        logout_button.click()

        helper.is_in_login_screen()

    def check_login_error_pop_up(self, driver: webdriver) -> None:
        # Check if the login error pop up exist and then
        # refresh the site and check that it does not exist.
        assert self.error_pop_up_exist(webdriver), "There is not any pop error that showed up"
        driver.refresh()
        assert not self.error_pop_up_exist(webdriver), "There is still a pop up after a refresh"

    def error_pop_up_exist(self, driver: webdriver) -> bool:
        # Wait until we found a the element with the pop up id.
        try:
            WebDriverWait(driver, timeout=TIMEOUT_POPUP).until(
                ec.presence_of_element_located((By.ID, ID_POP_UP_ELEMENT))
            )
        except:
            return False

        # Find and return the element
        pop_up_element: WebElement = driver.find_element(By.ID, ID_POP_UP_ELEMENT)
        return pop_up_element is not None
