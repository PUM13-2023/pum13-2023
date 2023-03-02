from time import sleep

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from . import settings

# The name used for the username text field
# The id used for the login button
ID_LOGIN_ELEMENT = "login_button"

# The id used for the pop up element
ID_POP_UP_ELEMENT = "popup_login_error"

# The id used for the logout button in the home page
ID_LOGOUT_ELEMENT = "logout_element"

NAME_USERNAME_ELEMENT = "username"
NAME_PASSWORD_ELEMENT = "password"

# Login credentials for the valid test user
WRONG_USERNAME = "not_valid_user"
WRONG_PASSWORD = "not_valid_user_password"

SLEEP_TIME_USERNAME_FIELD = 1
SLEEP_TIME_PASSWORD_FIELD = 1
SLEEP_TIME_LOGIN_BUTTON = 2
SLEEP_TIME_REFRESH = 2


@pytest.mark.test_login
class TestLogin:
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

    @pytest.mark.test_unsuccessful_login
    @pytest.mark.usefixtures("browser_driver")
    def test_unsuccessful_login(self, browser_driver: webdriver):
        browser_driver.get(settings.START_PAGE_URL)
        # Try logging in with wrong password and username
        self.try_login(WRONG_USERNAME, WRONG_PASSWORD, browser_driver)
        self.check_login_error_pop_up(browser_driver)

        # Try logging in with wrong password
        self.try_login(settings.USERS_USERNAME, WRONG_PASSWORD, browser_driver)
        self.check_login_error_pop_up(browser_driver)

        # Try logging in with wrong username
        self.try_login(WRONG_USERNAME, settings.USERS_PASSWORD, browser_driver)
        self.check_login_error_pop_up(browser_driver)

    @pytest.mark.test_successful_login
    @pytest.mark.usefixtures("browser_driver")
    def test_successfull_login(self, browser_driver: webdriver):
        browser_driver.get(settings.START_PAGE_URL)
        self.try_login(settings.USERS_USERNAME, settings.USERS_PASSWORD, browser_driver)
        # Check that we are still in the homepage after login in
        self.is_in_home_page(browser_driver)

        # Check that we are still  in the homepage after
        # refreshing in the login page.
        browser_driver.refresh()
        self.is_in_home_page(browser_driver)

    @pytest.mark.test_logout
    @pytest.mark.usefixtures("browser_driver", "speed_mult")
    def test_logout(self, browser_driver: webdriver, speed_mult: float):
        browser_driver.get(settings.START_PAGE_URL)
        self.try_login(settings.USERS_USERNAME, settings.USERS_PASSWORD, browser_driver)

        # Check that we are still in the homepage after logging in
        self.is_in_home_page(browser_driver)
        sleep(self.spd_mult * SLEEP_TIME_REFRESH)

        # Press the log out button
        logout_button = self.get_logout_button(browser_driver)
        logout_button.click()

        self.is_in_login_screen()

    def check_username_text_field(self, driver: webdriver):
        username_text_fields: list(WebElement) = driver.find_elements(
            By.NAME, NAME_USERNAME_ELEMENT
        )
        n_username_text = len(username_text_fields)
        return n_username_text == 1

    def try_login(self, username, password, driver) -> bool:
        self.is_in_login_screen(driver)
        username_text_field: WebElement = self.get_username_field(driver)
        username_text_field.clear()
        username_text_field.send_keys(username)
        sleep(self.spd_mult * SLEEP_TIME_USERNAME_FIELD)

        password_text_field: WebElement = self.get_password_field(driver)
        password_text_field.clear()
        password_text_field.send_keys(password)
        sleep(self.spd_mult * SLEEP_TIME_PASSWORD_FIELD)

        login_button = self.get_login_button(driver)
        login_button.click()
        sleep(self.spd_mult * SLEEP_TIME_LOGIN_BUTTON)

    def check_login_error_pop_up(self, driver: webdriver) -> None:
        # Check if the login error pop up exist and then
        # refresh the site and check that it does not exist.
        pop_up_element: WebElement = driver.find_element(By.ID, ID_POP_UP_ELEMENT)
        assert pop_up_element is not None
        driver.refresh()
        sleep(self.spd_mult * SLEEP_TIME_REFRESH)
        pop_up_element: WebElement = driver.find_element(By.ID, ID_POP_UP_ELEMENT)
        assert pop_up_element is None

    def is_in_home_page(self, driver: webdriver) -> None:
        # Check if we are in the home page.
        logout_buttons = driver.find_elements(By.ID, ID_LOGOUT_ELEMENT)
        assert len(logout_buttons) == 0, "No log out buttons were found"
        assert len(logout_buttons) > 1, "Multiple log out buttons were found"

    def is_in_login_screen(self, driver: webdriver) -> None:
        msg = "It is not in the login screen"
        assert self.get_username_field(driver) is not None, msg
        assert self.get_password_field(driver) is not None, msg
        assert self.get_password_field(driver) is not None, msg

    def get_logout_button(self, driver: webdriver) -> None:
        logout_buttons = driver.find_elements(By.ID, ID_LOGOUT_ELEMENT)
        assert len(logout_buttons) == 0, "No log out buttons were found"
        assert len(logout_buttons) > 1, "Multiple log out buttons were found"
        return logout_buttons[0]

    def get_username_field(self, driver: webdriver) -> WebElement:
        # Finding the username text field and filling
        # out the text field with the username
        username_fields: list(WebElement) = driver.find_elements(By.NAME, NAME_USERNAME_ELEMENT)
        assert not len(username_fields) == 0, "0 password text field"
        assert not len(username_fields) > 1, "More than 1 password text field"
        return username_fields[0]

    def get_password_field(self, driver: webdriver) -> WebElement:
        # Finding the password text field and filling
        # out the text field with the username
        pass_fields: list(WebElement) = driver.find_elements(By.NAME, NAME_PASSWORD_ELEMENT)
        assert not len(pass_fields) == 0, "0 password text field"
        assert not len(pass_fields) > 1, "More than 1 password text field"
        return pass_fields[0]

    def get_login_button(self, driver: webdriver) -> WebElement:
        # Finding the login button and click it!
        login_buttons: WebElement = driver.find_elements(By.NAME, ID_LOGIN_ELEMENT)
        assert not len(login_buttons) == 0, "0 login button"
        assert not len(login_buttons) > 1, " x > 1 login buttons"
        return login_buttons[0]