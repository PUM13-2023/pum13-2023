from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from time import sleep
from .test_enum import WebBrowser

import pytest


class Settings():
    START_PAGE_URL = 'https://www.google.com/'
    WEB_BROWSER = WebBrowser.FIREFOX

    # The name used for the username text field
    NAME_USERNAME_ELEMENT = 'username'

    # The name used for the password text field
    NAME_PASSWORD_ELEMENT = 'password'

    # The id used for the login button
    ID_LOGIN_ELEMENT = 'login_button'

    # The id used for the pop up element
    ID_POP_UP_ELEMENT = 'popup_login_error'

    # The id used for the logout button in the home page
    ID_LOGOUT_ELEMENT = 'logout_element'

    # Login credentials for the valid test user
    USERS_USERNAME = 'valid_user'
    USERS_PASSWORD = 'valid_user_password'
    WRONG_USERNAME = 'not_valid_user'
    WRONG_PASSWORD = 'not_valid_user_password'

    SLEEP_TIME_USERNAME_FIELD = 1
    SLEEP_TIME_PASSWORD_FIELD = 1
    SLEEP_TIME_LOGIN_BUTTON = 3
    SLEEP_TIME_REFRESH = 3


class TestLogin():

    @pytest.fixture()
    def browser_driver(self):
        match Settings.WEB_BROWSER:
            case WebBrowser.FIREFOX:
                driver: webdriver = webdriver.Firefox()
            case WebBrowser.CHROME:
                driver: webdriver = webdriver.Chrome()
        yield driver
        driver.close()

    @pytest.mark.test_login
    @pytest.mark.test_unsuccessful_login
    @pytest.mark.usefixtures('browser_driver')
    def test_unsuccessful_login(self, browser_driver: webdriver):
        browser_driver.get(Settings.START_PAGE_URL)
        # Try logging in with wrong password and username
        self.try_login(Settings.WRONG_USERNAME,
                       Settings.WRONG_PASSWORD,
                       browser_driver)
        self.check_login_error_pop_up(browser_driver)

        # Try logging in with wrong password
        self.try_login(Settings.USERS_USERNAME,
                       Settings.WRONG_PASSWORD,
                       browser_driver)
        self.check_login_error_pop_up(browser_driver)

        # Try logging in with wrong username
        self.try_login(Settings.WRONG_USERNAME,
                       Settings.USERS_PASSWORD,
                       browser_driver)
        self.check_login_error_pop_up(browser_driver)

    @pytest.mark.test_login
    @pytest.mark.usefixtures('browser_driver')
    def test_successfull_login(self, browser_driver: webdriver):
        browser_driver.get(Settings.START_PAGE_URL)
        self.try_login(Settings.USERS_USERNAME,
                       Settings.USERS_PASSWORD,
                       browser_driver)
        # Check that we are still in the homepage after login in
        self.is_in_home_page(browser_driver)

        # Check that we are still  in the homepage after
        # refreshing in the login page.
        browser_driver.refresh()
        self.is_in_home_page(browser_driver)

    @pytest.mark.test_login
    @pytest.mark.usefixtures('browser_driver')
    def test_logout(self, browser_driver: webdriver):
        browser_driver.get(Settings.START_PAGE_URL)
        self.try_login(Settings.USERS_USERNAME,
                       Settings.USERS_PASSWORD,
                       browser_driver)
        # Check that we are still in the homepage after logging in
        self.is_in_home_page(browser_driver)
        sleep(Settings.SLEEP_TIME_REFRESH)
        
        # Press the log out button
        logout_button = self.get_logout_button(browser_driver)
        logout_button.click()

        self.is_in_login_screen()

    def check_username_text_field(self, driver: webdriver):
        username_text_fields: list(WebElement) = driver.find_elements(
            By.NAME, Settings.NAME_USERNAME_ELEMENT)
        n_username_text = len(username_text_fields)
        return n_username_text == 1

    def try_login(self, username, password, driver) -> bool:
        self.is_in_login_screen(driver)
        username_text_field: WebElement = self.get_username_field(driver)
        username_text_field.clear()
        username_text_field.send_keys(username)
        sleep(Settings.SLEEP_TIME_USERNAME_FIELD)

        password_text_field: WebElement = self.get_password_field(driver)
        password_text_field.clear()
        password_text_field.send_keys(password)
        sleep(Settings.SLEEP_TIME_PASSWORD_FIELD)

        login_button = self.get_login_button(driver)
        login_button.click()
        sleep(Settings.SLEEP_TIME_LOGIN_BUTTON)

    def check_login_error_pop_up(driver: webdriver) -> None:
        # Check if the login error pop up exist and then refresh the site and
        # check that it does not exist.
        pop_up_element: WebElement = driver.find_element(
            By.ID, Settings.ID_POP_UP_ELEMENT)
        assert (pop_up_element is not None)
        driver.refresh()
        sleep(Settings.SLEEP_TIME_REFRESH)
        pop_up_element: WebElement = driver.find_element(
            By.ID, Settings.ID_POP_UP_ELEMENT)
        assert (pop_up_element is None)

    def is_in_home_page(driver: webdriver) -> None:
        # Check if we are in the home page.
        logout_buttons = driver.find_elements(
            By.ID, Settings.ID_LOGOUT_ELEMENT)
        assert len(logout_buttons) == 0, "No log out buttons were found"
        assert len(logout_buttons) > 1, "Multiple log out buttons were found"

    def is_in_login_screen(self, driver: webdriver) -> None:
        msg = "It is not in the login screen"
        assert self.get_username_field(driver) is not None, msg
        assert self.get_password_field(driver) is not None, msg
        assert self.get_password_field(driver) is not None, msg

    def get_logout_button(self, driver: webdriver) -> None:
        logout_buttons = driver.find_elements(
            By.ID, Settings.ID_LOGOUT_ELEMENT)
        assert len(logout_buttons) == 0, "No log out buttons were found"
        assert len(logout_buttons) > 1, "Multiple log out buttons were found"
        return logout_buttons[0]

    def get_username_field(self, driver: webdriver) -> WebElement:
        # Finding the username text field and filling out the text field with
        # the username
        username_fields: list(WebElement) = driver.find_elements(
            By.NAME, Settings.NAME_USERNAME_ELEMENT)
        assert not len(username_fields) == 0, '0 password text field'
        assert not len(username_fields) > 1, 'More than 1 password text field'
        return username_fields[0]

    def get_password_field(self, driver: webdriver) -> WebElement:
        # Finding the password text field and filling out the text field with
        # the username
        pass_fields: list(WebElement) = driver.find_elements(
            By.NAME, Settings.NAME_PASSWORD_ELEMENT)
        assert not len(pass_fields) == 0, '0 password text field'
        assert not len(pass_fields) > 1, 'More than 1 password text field'
        return pass_fields[0]
    
    def get_login_button(self, driver: webdriver) -> WebElement:
        # Finding the login button and click it!
        login_buttons: WebElement = driver.find_elements(
            By.NAME, Settings.ID_LOGIN_ELEMENT)
        assert not len(login_buttons) == 0, '0 login button'
        assert not len(login_buttons) > 1, ' x > 1 login buttons'
        return login_buttons[0]