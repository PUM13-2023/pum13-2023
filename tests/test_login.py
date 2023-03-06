from time import sleep

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from . import helper_test_functions as helper
from . import settings
from . import helper_test_functions as helper

# Login credentials for the valid test user
WRONG_USERNAME = "not_valid_user"
WRONG_PASSWORD = "not_valid_user_password"

SLEEP_TIME_LOGIN_BUTTON = 2
SLEEP_TIME_REFRESH = 2

ID_POP_UP_ELEMENT = "login_error_popup"


@pytest.mark.test_login
class TestLogin:
    @pytest.mark.test_unsuccessful_login
    @pytest.mark.usefixtures("browser_driver", "speed_mult")
    def test_unsuccessful_login(self, browser_driver: webdriver, speed_mult: float):
        browser_driver.get(settings.START_PAGE_URL)
        # Try logging in with wrong password and username
        helper.try_login(WRONG_USERNAME, WRONG_PASSWORD, browser_driver, speed_mult)
        self.check_login_error_pop_up(browser_driver)

        # Try logging in with wrong password
        helper.try_login(settings.USERS_USERNAME, WRONG_PASSWORD, browser_driver, speed_mult)
        self.check_login_error_pop_up(browser_driver)

        # Try logging in with wrong username
        helper.try_login(WRONG_USERNAME, settings.USERS_PASSWORD, browser_driver, speed_mult)
        self.check_login_error_pop_up(browser_driver)

    @pytest.mark.test_successful_login
    @pytest.mark.usefixtures("browser_driver", "speed_mult")
    def test_successfull_login(self, browser_driver: webdriver, speed_mult: float):
        browser_driver.get(settings.START_PAGE_URL)
        helper.try_login(settings.USERS_USERNAME, settings.USERS_PASSWORD, browser_driver, float)
        # Check that we are still in the homepage after login in
        helper.is_in_home_page(browser_driver)

        # Check that we are still  in the homepage after
        # refreshing in the login page.
        browser_driver.refresh()
        helper.is_in_home_page(browser_driver)

    @pytest.mark.test_logout
    @pytest.mark.usefixtures("browser_driver", "speed_mult")
    def test_logout(self, browser_driver: webdriver, speed_mult: float):
        browser_driver.get(settings.START_PAGE_URL)
        helper.try_login(
            settings.USERS_USERNAME, settings.USERS_PASSWORD, browser_driver, speed_mult
        )

        # Check that we are still in the homepage after logging in
        helper.is_in_home_page(browser_driver)
        sleep(self.spd_mult * SLEEP_TIME_REFRESH)

        # Press the log out button
        logout_button = helper.get_logout_button(browser_driver)
        logout_button.click()

        helper.is_in_login_screen()

    def check_login_error_pop_up(self, driver: webdriver) -> None:
        # Check if the login error pop up exist and then
        # refresh the site and check that it does not exist.
        pop_up_element: WebElement = driver.find_element(By.ID, ID_POP_UP_ELEMENT)
        assert pop_up_element is not None
        driver.refresh()
        sleep(self.spd_mult * SLEEP_TIME_REFRESH)
        pop_up_element: WebElement = driver.find_element(By.ID, ID_POP_UP_ELEMENT)
        assert pop_up_element is None
