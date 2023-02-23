from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from time import sleep
from .test_enum import WebBrowser

import pytest


class LoginSettings():
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
    SLEEP_TIME_LOGIN_BUTTON = 5
    SLEEP_TIME_REFRESH = 5


class TestLogin():

    @pytest.fixture
    def browser_driver(self):
        match LoginSettings.WEB_BROWSER:
            case WebBrowser.FIREFOX:
                self.driver = webdriver.Firefox()
            case WebBrowser.CHROME:
                self.driver = webdriver.Chrome()
        self.driver.get(LoginSettings.START_PAGE_URL)
        yield
        self.driver.close()

    @pytest.mark.usefixtures('browser_driver')
    def test_unsuccessful_login(self):

        # Try logging in with wrong password and username
        self.try_login(LoginSettings.WRONG_USERNAME,
                       LoginSettings.WRONG_PASSWORD,
                       self.driver)
        self.check_login_error_pop_up(self.driver)

        # Try logging in with wrong password
        self.try_login(LoginSettings.USERS_USERNAME,
                       LoginSettings.WRONG_PASSWORD,
                       self.driver)
        self.check_login_error_pop_up(self.driver)

        # Try logging in with wrong username
        self.try_login(LoginSettings.WRONG_USERNAME,
                       LoginSettings.USERS_PASSWORD,
                       self.driver)
        self.check_login_error_pop_up(self.driver)
    
    @pytest.mark.usefixtures('browser_driver')
    def test_successfull_login(self):
        self.try_login(LoginSettings.USERS_USERNAME,
                       LoginSettings.USERS_PASSWORD,
                       self.driver)
        # Check that we are still in the homepage after login in
        assert (self.is_in_home_page(self.driver))

        # Check that we are still  in the homepage after
        # refreshing in the login page.
        self.driver.refresh()
        assert (self.is_in_home_page(self.driver))

        self.driver.close()

    # @pytest.mark.usefixtures('browser_driver')
    # def test_logout(self):
    #     sleep(2)
    #     # try_login(LoginSettings.USERS_USERNAME,
    #     #           LoginSettings.USERS_PASSWORD,
    #     #           browser_driver)
    #     # Check that we are still in the homepage after login in
    #     # assert (is_in_home_page(browser_driver))

    #     self.driver.close()

    def check_username_text_field(self, driver: webdriver):
        username_text_field_candidates: list(WebElement) = driver.find_elements(
            By.NAME, LoginSettings.NAME_USERNAME_ELEMENT)
        n_username_text = len(username_text_field_candidates)
        return n_username_text == 1

    def try_login(self, username, password, driver) -> bool:
        # Finding the username text field and filling out the text field with
        # the username
        name_text_fields: list(WebElement) = driver.find_elements(
            By.NAME, LoginSettings.NAME_USERNAME_ELEMENT)
        assert not len(name_text_fields) == 0, '0 username text field'
        assert not len(name_text_fields) > 1, 'More than 1 name text field'

        username_text_field: WebElement = name_text_fields[0]
        username_text_field.clear()
        username_text_field.send_keys(username)
        sleep(LoginSettings.SLEEP_TIME_USERNAME_FIELD)

        # Finding the password text field and filling out the text field with
        # the username
        pass_fields: list(WebElement) = driver.find_elements(
            By.NAME, LoginSettings.NAME_PASSWORD_ELEMENT)
        assert not len(pass_fields) == 0, '0 password text field'
        assert not len(pass_fields) > 1, 'More than 1 password text field'

        password_text_field: WebElement = pass_fields[0]
        password_text_field.clear()
        password_text_field.send_keys(password)
        sleep(LoginSettings.SLEEP_TIME_PASSWORD_FIELD)

        # Finding the login button and click it!
        login_buttons: WebElement = driver.find_elements(
            By.NAME, LoginSettings.ID_LOGIN_ELEMENT)
        assert not len(login_buttons) == 0, '0 login button'
        assert not len(login_buttons) > 1, ' x > 1 login buttons'

        login_button = login_buttons[0]
        login_button.click()
        sleep(LoginSettings.SLEEP_TIME_LOGIN_BUTTON)


    def check_login_error_pop_up(driver: webdriver) -> None:
        # Check if the login error pop up exist and then refresh the site and
        # check that it does not exist.
        pop_up_element: WebElement = driver.find_element(
            By.ID, LoginSettings.ID_POP_UP_ELEMENT)
        assert (pop_up_element is not None)
        driver.refresh()
        sleep(LoginSettings.SLEEP_TIME_REFRESH)
        pop_up_element: WebElement = driver.find_element(
            By.ID, LoginSettings.ID_POP_UP_ELEMENT)
        assert (pop_up_element is None)


    def is_in_home_page(driver: webdriver) -> None:
        # Check if we are in the home page.
        in_home_page: bool = driver.find_element(
            By.ID, LoginSettings.ID_LOGOUT_ELEMENT) is not None
        return in_home_page
